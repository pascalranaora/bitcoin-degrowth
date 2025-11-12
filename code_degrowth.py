#!/usr/bin/env python3
"""
Bitcoin Entropy Vacuum Engine — Net CO₂ Avoided Dashboard
@BitcoinDegrowth | November 10, 2025
Animated, Responsive, Thermodynamically Correct
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit

# === CONFIG ===
START_DATE = '2018-01-01'
OUTPUT_FILE = 'index.html'

# Entropy sectors (2025 est.)
ENTROPY = {
    'fast_fashion':     {'spend': 2.5e12,  'co2': 1.2e9},
    'luxury_yachts':    {'spend': 3.5e10,  'co2': 1.0e6},
    'luxury_resorts':   {'spend': 1.2e11,  'co2': 3.63e8},
    'real_estate_spec': {'spend': 8.0e12,  'co2': 2.8e9}
}

TOTAL_SPEND = sum(v['spend'] for v in ENTROPY.values())
TOTAL_CO2 = sum(v['co2'] for v in ENTROPY.values())
CO2_PER_DOLLAR = TOTAL_CO2 / TOTAL_SPEND  # g CO₂ per $1

# === SCRAPE CAMBRIDGE CBECI ===
def scrape_cambridge_emissions():
    url = "https://ccaf.io/cbnsi/cbeci/ghg"
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
    try:
        r = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        h2 = soup.find('h2', style=lambda x: x and 'font-size: 48px' in x)
        if h2:
            annual_mt = float(h2.text.strip().replace(',', ''))
            print(f"Cambridge CBECI: Current annual emissions = {annual_mt:.1f} Mt CO₂e")
            return annual_mt
    except Exception as e:
        print(f"Scrape failed: {e}")
    print("Using fallback: 108 Mt")
    return 108.0

annual_emissions_mt = scrape_cambridge_emissions()

# === FETCH TRADINGVIEW DATA ===
from tvDatafeed import TvDatafeed, Interval
tv = TvDatafeed("", "")

def fetch(symbol, exchange, name):
    for _ in range(5):
        try:
            df = tv.get_hist(symbol=symbol, exchange=exchange, interval=Interval.in_daily, n_bars=4000)
            if df is not None and len(df) > 100:
                print(f"{name}: {len(df)} days")
                return df
        except Exception as e:
            print(f"Retry {name}: {e}")
    return None

price_df = fetch('BTCUSD', 'COINBASE', 'Price')
cap_df = fetch('BTC', 'CRYPTOCAP', 'Market Cap')
hashrate_df = fetch('HRATE', 'BCHAIN', 'Hashrate')  # GH/s

# === PROCESS DATA ===
def process(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    df['date'] = df.index.strftime('%Y-%m-%d')
    df = df[df.index >= START_DATE]
    return df[['date', 'close']].reset_index(drop=True)

price_df = process(price_df)
cap_df = process(cap_df)
hashrate_df = process(hashrate_df)
hashrate_df['close'] = hashrate_df['close'] / 1_000_000  # GH/s → EH/s

# Merge
merged = price_df.merge(cap_df, on='date', suffixes=('_price', '_cap'))
merged = merged.merge(hashrate_df, on='date')
merged.rename(columns={'close': 'hashrate'}, inplace=True)

# === EFFICIENCY POWER-LAW FIT ===
years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
eff_jth = np.array([89, 65, 50, 35, 28, 22, 18, 15])

def power_curve(t, a, b, c):
    return a * (t - 2017)**b + c

popt, _ = curve_fit(power_curve, years, eff_jth, p0=[100, -0.3, 10])
a, b, c = popt
print(f"Efficiency fit: {a:.1f} × (year-2017)^{b:.3f} + {c:.1f} J/TH")

merged['year'] = pd.to_datetime(merged['date']).dt.year
merged['efficiency_jth'] = power_curve(merged['year'], *popt)

# === EMISSIONS CALCULATION ===
SEC_PER_DAY = 86400
JOULES_PER_KWH = 3.6e6
CO2_PER_KWH = 0.475  # kg/kWh

merged['daily_joules'] = merged['hashrate'] * 1e6 * merged['efficiency_jth'] * SEC_PER_DAY
merged['daily_energy_kwh'] = merged['daily_joules'] / JOULES_PER_KWH
merged['daily_emissions_mt'] = (merged['daily_energy_kwh'] * CO2_PER_KWH) / 1e6

total_emissions_since_2018 = merged['daily_emissions_mt'].sum()
total_gross_avoided = merged['close_cap'].sum() * CO2_PER_DOLLAR / 1e6
net_co2_avoided = total_gross_avoided - total_emissions_since_2018

current_cap = merged['close_cap'].iloc[-1]
current_price = merged['close_price'].iloc[-1]
current_hr = merged['hashrate'].iloc[-1]
current_eff = merged['efficiency_jth'].iloc[-1]

print(f"\nFINAL RESULTS")
print(f"Price: ${current_price:,.0f}")
print(f"Market Cap: ${current_cap/1e12:.2f}T")
print(f"Hashrate: {current_hr:.0f} EH/s")
print(f"Efficiency: {current_eff:.1f} J/TH")
print(f"NET CO₂ AVOIDED: {net_co2_avoided:,.0f} Mt")

# === PREPARE JS DATA ===
merged['gross_avoided'] = merged['close_cap'] * CO2_PER_DOLLAR / 1e6
merged['net_avoided'] = merged['gross_avoided'] - merged['daily_emissions_mt']

js_data = merged[['date', 'gross_avoided', 'daily_emissions_mt', 'net_avoided', 'efficiency_jth']].to_dict('records')
js_data_str = json.dumps(js_data)

sector_co2 = [current_cap * (v['co2'] / v['spend']) / 1e6 for v in ENTROPY.values()]
sector_names = [k.replace('_', ' ').title() for k in ENTROPY.keys()]
sectors_js = json.dumps([{'name': n, 'co2': round(c)} for n, c in zip(sector_names, sector_co2)])

# === HTML DASHBOARD WITH ANIMATIONS ===
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Bitcoin Entropy Vacuum Engine | @BitcoinDegrowth</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Roboto+Mono&display=swap');
    body {{ margin:0; padding:0; background:#000; color:#fff; font-family: 'Roboto Mono', monospace; overflow:auto; }}
    .container {{ display: flex; flex-wrap: wrap; height: auto; min-height: 100vh; opacity: 0; animation: fadeIn 1.5s forwards; }}
    @keyframes fadeIn {{ to {{ opacity:1; }} }}
    .panel {{ flex:1; min-width:500px; padding:25px; box-sizing:border-box; border:1px solid #333; position:relative; }}
    h1 {{ font-family: 'Orbitron', sans-serif; color:#f7931a; font-size:2.2em; margin:0; text-shadow: 0 0 10px #f7931a; }}
    h2 {{ color:#f7931a; margin:10px 0; font-size:1.4em; }}
    .live {{ color:#0f0; animation:pulse 2s infinite; font-weight:bold; }}
    @keyframes pulse {{ 50% {{ opacity:0.7; }} }}
    .stats {{ font-size:1.4em; margin:20px 0; line-height:1.8; }}
    .stats strong {{ color:#0f0; text-shadow: 0 0 8px #0f0; }}
    .btn-details {{ background:#222; color:#fff; border:2px solid #f7931a; padding:10px 20px; cursor:pointer; font-size:0.9em; margin:15px 0; border-radius:8px; transition:0.3s; }}
    .btn-details:hover {{ background:#f7931a; color:#000; transform:scale(1.05); box-shadow:0 0 15px #f7931a; }}
    .details {{ display: none; background:#111; padding:20px; border-radius:10px; margin:15px 0; font-size:0.9em; line-height:1.6; border:1px solid #444; animation: slideDown 0.6s; }}
    @keyframes slideDown {{ from {{ opacity:0; transform:translateY(-20px); }} to {{ opacity:1; transform:translateY(0); }} }}
    .details table {{ width:100%; border-collapse:collapse; margin:12px 0; }}
    .details th, .details td {{ border:1px solid #555; padding:8px; text-align:left; }}
    .details th {{ background:#222; }}
    .details code {{ background:#000; padding:3px 8px; border-radius:4px; color:#0f0; }}
    .motto {{ position:fixed; bottom:0; left:0; width:100%; text-align:center; padding:25px; background:linear-gradient(to top,#000,transparent); font-size:1.1em; line-height:1.9; z-index:100; animation: fadeIn 2s; }}
    .motto strong {{ color:#f7931a; text-shadow:0 0 10px #f7931a; }}
    .handle {{ color:#1da1f2; font-weight:bold; }}
    .net-positive {{ color:#00ff00; font-size:1.6em; font-weight:bold; text-shadow:0 0 15px #00ff00; animation: glow 2s infinite alternate; }}
    @keyframes glow {{ from {{ text-shadow:0 0 15px #00ff00; }} to {{ text-shadow:0 0 25px #00ff00; }} }}
    .counter {{ font-family:'Orbitron'; font-size:2em; color:#0f0; text-shadow:0 0 15px #0f0; }}
  </style>
</head>
<body>
<div style="text-align:center; padding:15px 0; background:#000; border-bottom:1px solid #333; position:relative; z-index:10;">
  <h1 style="margin:0; font-family:'Orbitron',sans-serif; color:#f7931a; font-size:2.4em; text-shadow:0 0 12px #f7931a;">
    Bitcoin Degrowth Dashboard v1.0
  </h1>
</div>
<!-- MOTTO BAR -->
<div style="
  text-align:center; 
  padding:18px 20px; 
  background:linear-gradient(135deg, #1a1a1a, #000); 
  border-top:1px solid #333; 
  border-bottom:1px solid #333; 
  font-size:1.1em; 
  line-height:1.9; 
  color:#fff; 
  font-family:'Roboto Mono', monospace;
  z-index:100; 
  position:relative;
">
  <strong style="color:#f7931a; text-shadow:0 0 10px #f7931a;">HODL = Entropy Killer.</strong><br>
  Bitcoin is the greenest money ever created.<br>
  It doesn't grow the economy — it <strong style="color:#f7931a;">purifies it</strong> by shrinking high-entropy goods production.<br>
  Every satoshi you stack and hold removes one dollar from waste, extraction, and/or disorder.<br>
  This is not greenwashing. This is <strong style="color:#00ff00;">thermodynamics</strong>.<br><br>
  Net CO₂ Avoided Since 2018: <strong style="color:#00ff00; font-size:1.3em; text-shadow:0 0 12px #00ff00;">{net_co2_avoided:.0f} million tons</strong><br>
  <span style="color:#1da1f2; font-weight:bold;">@BitcoinDegrowth</span><br />
  <button class="btn-details" onclick="toggleDetails()">Show Methodology</button>
    <div id="details" class="details">
      <h3>Entropy Reduction per $ Invested</h3>
      <p><strong>High-entropy sectors</strong> = high material throughput, waste, and emissions.<br>
      <strong>Bitcoin</strong> = digital, finite, low-maintenance → <strong>low entropy</strong>.</p>
      <p><strong>Every $1 in BTC avoids 1$ spent in:</strong></p>
      <table>
        <tr><th>Sector</th><th>Spend (T$)</th><th>CO₂ (Mt)</th><th>g CO₂/$</th></tr>
        <tr><td>Fast Fashion</td><td>2.5</td><td>1,200</td><td><strong>0.480</strong></td></tr>
        <tr><td>Luxury Yachts</td><td>0.035</td><td>1</td><td><strong>0.029</strong></td></tr>
        <tr><td>Luxury Resorts</td><td>0.12</td><td>363</td><td><strong>0.302</strong></td></tr>
        <tr><td>Real Estate Spec</td><td>8.0</td><td>2,800</td><td><strong>0.350</strong></td></tr>
        <tr><td><strong>Total</strong></td><td><strong>10.655</strong></td><td><strong>4,364</strong></td><td><strong>0.409</strong></td></tr>
      </table>
      <p><strong>Weighted Average:</strong> <code>CO₂/$ = 4,364e6 tons / 10.655e12 USD = 0.409 g CO₂ per $1</code></p>
      <p><strong>Net CO₂ Avoided(t)</strong> = (Bitcoin Market Cap(t) × 0.409) − Mining Emissions(t)</p>
      <p><strong>Mining Emissions(t)</strong>: Hashrate(t) × Efficiency(t) × 0.475 kg CO₂/kWh</p>
      <p><strong>Efficiency(t)</strong>: Power-law fit on historical ASIC data (J/TH)</p>
      <small>Sources: TradingView, UNEP, IPCC, Statista, CCAF, @BitcoinDegrowth</small>
    </div>
    <a class="btn-details" target='_blank' href="https://github.com/pascalranaora/bitcoin-degrowth" style="text-decoration:none">Open Source Model</a>
</div>
<div class="container">
  <div class="panel">
    <h1>Bitcoin : an Entropy Vacuum Engine</h1>
    <div style="font-size:0.9em; color:#888; margin-bottom:12px;">
    Data Last Refreshed: <span id="generated-time"></span>
    </div>
    <div class="stats">
      <span class="live">LIVE:</span> 
      <strong>${current_cap/1e12:.2f}T</strong> Cap → 
      <strong>{current_hr:.0f} EH/s</strong> → 
      <strong>{current_eff:.1f} J/TH</strong>
      <br><br>
      Gross Avoided: <strong>{total_gross_avoided:,.0f} Mt</strong><br>
      Mining Emissions: <b style="color:red;">{total_emissions_since_2018:,.0f} Mt</b><br>
      <strong>Net Avoided CO2 (Million Tons):</strong><br>
      <div class="counter" id="net-counter">0 Mt</div>
      <h2>Bitcoin Net CO₂ Avoidance (Since 2018)</h2>
      <div id="co2-plot" style="height:48vh; margin-top:20px;"></div>
    </div>

    
  </div>

  <div class="panel">
    
    <h2>Sector CO₂ Avoidance</h2>
    <div id="sector-pie" style="height:48vh;"></div>
    <h2>Mining Efficiency Power Law Progress</h2>
    <div id="efficiency-plot" style="height:48vh; margin-top:20px;"></div>
  </div>
</div>


<script>
document.getElementById('generated-time').textContent = new Date().toLocaleString('en-US', {{
  timeZone: 'America/Los_Angeles',
  month: 'short', day: 'numeric', year: 'numeric',
  hour: 'numeric', minute: '2-digit', second: '2-digit'
}}) + ' PST';

  const data = {js_data_str};
  const finalNet = {net_co2_avoided:.0f};

  const history = data.map(d => ({{
    date: new Date(d.date),
    gross: d.gross_avoided,
    emissions: d.daily_emissions_mt,
    net: d.net_avoided,
    eff: d.efficiency_jth
  }}));

  function toggleDetails() {{
    const el = document.getElementById('details');
    el.style.display = el.style.display === 'block' ? 'none' : 'block';
  }}

  // Animated Counter
  function animateCounter() {{
    let start = 0;
    const duration = 3000;
    const step = () => {{
      const progress = Math.min((Date.now() - startTime) / duration, 1);
      const value = Math.floor(progress * finalNet);
      document.getElementById('net-counter').textContent = value.toLocaleString() + ' Mt';
      if (progress < 1) requestAnimationFrame(step);
    }};
    const startTime = Date.now();
    requestAnimationFrame(step);
  }}

  // CO₂ Plot
  Plotly.newPlot('co2-plot', [
    {{x: history.map(d=>d.date), y: history.map(d=>d.gross), name: 'Gross Avoided', line: {{color:'#00ff00', width:3}}}},
    {{x: history.map(d=>d.date), y: history.map(d=>d.net), name: 'Net Avoided', line: {{color:'#ffaa00', dash:'dot', width:3}}}},
    {{x: history.map(d=>d.date), y: history.map(d=>d.emissions), name: 'Mining Emissions', line: {{color:'#ff6b6b', width:2}}}}
  ], {{
    paper_bgcolor: '#000', plot_bgcolor: '#000', font: {{color: '#aaa'}},
    title: {{text: 'Bitcoin Net CO₂ Avoided (Million tons)', font: {{color: '#fff', size: 16}}}},
    yaxis: {{gridcolor: '#333'}}, xaxis: {{gridcolor: '#333'}}, legend: {{x:0, y:1, bgcolor: '#111'}},
    hovermode: 'x unified'
  }}, {{responsive: true}});

  // Efficiency (Declining!)
  Plotly.newPlot('efficiency-plot', [{{
    x: history.map(d=>d.date), y: history.map(d=>d.eff),
    mode: 'lines', line: {{color: '#4ecdc4', width: 3}}, name: 'J/TH'
  }}], {{
    title: {{text: 'ASIC Efficiency (J/TH) — Power-Law Decline', font: {{color: '#fff', size: 14}}}},
    paper_bgcolor: '#000', plot_bgcolor: '#000', font: {{color: '#aaa', size: 11}},
    yaxis: {{title: 'J/TH', gridcolor: '#333'}}
  }}, {{responsive: true}});

  // Sector Pie
  const sectors = {sectors_js};
  Plotly.newPlot('sector-pie', [{{
    values: sectors.map(s=>s.co2),
    labels: sectors.map(s=>s.name),
    type: 'pie', textinfo: 'label+percent', textposition: 'inside',
    marker: {{colors: ['#ff6b6b','#4ecdc4','#45b7d1','#f9ca24']}},
    hoverinfo: 'label+value+percent'
  }}], {{
    title: {{text: 'CO₂ Avoided by Sector (Current Year)', font: {{color: '#fff', size: 16}}}},
    paper_bgcolor: '#000', plot_bgcolor: '#000', font: {{color: '#aaa'}}
  }}, {{responsive: true}});

  // Start counter
  setTimeout(animateCounter, 800);
</script>

</body>
</html>"""

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write(html)

print(f"\nDashboard generated: {OUTPUT_FILE}")
print(f"Open → file://{os.path.abspath(OUTPUT_FILE)}")
print(f"\nBitcoin has avoided {net_co2_avoided:,.0f} million tons of CO₂ since 2018.")
print(f"You are not early. You are right.")
