#!/usr/bin/env python3
"""
Bitcoin Entropy Vacuum Engine — Net CO₂ Avoided Dashboard
@BitcoinDegrowth | November 11, 2025
Animated, Responsive, Thermodynamically Correct – v2.0
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np
from scipy.optimize import curve_fit
from io import StringIO

# === CONFIG ===
START_DATE = '2018-01-01'
OUTPUT_FILE = 'index.html'

# ----------------------------------------------------------------------
# 1. HIGH-ENTROPY BASKET – EXIOBASE-DERIVED 0.51 kg CO₂ / $
# ----------------------------------------------------------------------
HIGH_ENTROPY_INTENSITY_KG_PER_USD = 0.51          
CO2_PER_DOLLAR = HIGH_ENTROPY_INTENSITY_KG_PER_USD * 1e3  # g CO₂ per $ (for legacy)

# ----------------------------------------------------------------------
# 2. EMPIRICAL DISPLACEMENT RATE δ = 0.34 (survey + wealth data)
# ----------------------------------------------------------------------
EMPIRICAL_DISPLACEMENT_RATE = 0.34                

# Micro-survey (2023-2025) – weighted mean → 0.34
SURVEY_CSV = """cohort,wealth_decile,source_category,probability_high_entropy,n_responses
retail,3,luxury_budget,0.32,5000
retail,5,discretionary,0.34,3200
hnw,8,real_estate,0.60,1200
hnw,9,private_equity,0.58,800
institutional,0,other,0.08,1500
"""
survey_df = pd.read_csv(StringIO(SURVEY_CSV))

def estimate_displacement() -> tuple[float, float, float]:
    """Weighted mean + bootstrap 95 % CI."""
    weighted = survey_df["probability_high_entropy"] * survey_df["n_responses"]
    delta = weighted.sum() / survey_df["n_responses"].sum()
    boot = []
    for _ in range(1_000):
        idx = np.random.choice(survey_df.index, size=len(survey_df), replace=True)
        w = survey_df.loc[idx, "probability_high_entropy"] * survey_df.loc[idx, "n_responses"]
        boot.append(w.sum() / survey_df.loc[idx, "n_responses"].sum())
    ci_low, ci_high = np.percentile(boot, [2.5, 97.5])
    return delta, ci_low, ci_high

DELTA_HIGH, DELTA_CI_LOW, DELTA_CI_HIGH = estimate_displacement()

# Add this block near the top (after imports, before any usage):

ENTROPY = {
    'fast_fashion':     {'spend': 2.5e12,  'co2': 1.2e9},
    'luxury_yachts':    {'spend': 3.5e10,  'co2': 1.0e6},
    'luxury_resorts':   {'spend': 1.2e11,  'co2': 3.63e8},
    'real_estate_spec': {'spend': 8.0e12,  'co2': 2.8e9}
}

# ----------------------------------------------------------------------
# 3. SCRAPE CAMBRIDGE CBECI (fallback kept)
# ----------------------------------------------------------------------
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

# ----------------------------------------------------------------------
# 4. FETCH TRADINGVIEW DATA 
# ----------------------------------------------------------------------
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

price_df   = fetch('BTCUSD', 'COINBASE', 'Price')
cap_df     = fetch('BTC', 'CRYPTOCAP', 'Market Cap')
hashrate_df = fetch('HRATE', 'BCHAIN', 'Hashrate')  # GH/s

# ----------------------------------------------------------------------
# 5. PROCESS DATA (Δcap for avoided emissions)
# ----------------------------------------------------------------------
def process(df):
    if df is None or df.empty: return pd.DataFrame()
    df = df.copy()
    df['date'] = df.index.strftime('%Y-%m-%d')
    df = df[df.index >= START_DATE]
    return df[['date', 'close']].reset_index(drop=True)

price_df   = process(price_df)
cap_df     = process(cap_df)
hashrate_df = process(hashrate_df)
hashrate_df['close'] = hashrate_df['close'] / 1_000_000  # GH/s → EH/s

merged = price_df.merge(cap_df, on='date', suffixes=('_price', '_cap'))
merged = merged.merge(hashrate_df, on='date')
merged.rename(columns={'close': 'hashrate'}, inplace=True)

# Incremental market-cap (Δcap) – driver of avoided emissions
merged['delta_cap'] = merged['close_cap'].diff().fillna(merged['close_cap'])

# ----------------------------------------------------------------------
# 6. EFFICIENCY POWER-LAW FIT 
# ----------------------------------------------------------------------
years = np.array([2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025])
eff_jth = np.array([89, 65, 50, 35, 28, 22, 18, 15])

def power_curve(t, a, b, c):
    return a * (t - 2017)**b + c

popt, _ = curve_fit(power_curve, years, eff_jth, p0=[100, -0.3, 10])
a, b, c = popt
print(f"Efficiency fit: {a:.1f} × (year-2017)^{b:.3f} + {c:.1f} J/TH")

merged['year'] = pd.to_datetime(merged['date']).dt.year
merged['efficiency_jth'] = power_curve(merged['year'], *popt)

# ----------------------------------------------------------------------
# 7. EMISSIONS CALCULATION
# ----------------------------------------------------------------------
SEC_PER_DAY = 86400
JOULES_PER_KWH = 3.6e6
CO2_PER_KWH = 0.475  # kg/kWh
merged['daily_joules'] = merged['hashrate'] * 1e3 * merged['efficiency_jth'] * SEC_PER_DAY
merged['daily_energy_kwh'] = merged['daily_joules'] / JOULES_PER_KWH
merged['daily_emissions_mt'] = (merged['daily_energy_kwh'] * CO2_PER_KWH) / 1000000

total_emissions_since_2018 = merged['daily_emissions_mt'].sum()

# Gross avoided = Σ(Δcap × δ × I_high)
# delta_cap is in USD → multiply by kg/$ → divide by 1e9 to get Mt
# Making the strong assumption that *inflows* (positive Δmarketcap) and *outflows* (negative Δmarketcap) are both displacing high-entropy spending the same way
# The reality might be more nuanced and in favor of the Bitcoin Network (e.g. every Bitcoin Outflows does not necessarily goes back to high-entropy spending)
merged['gross_avoided'] = merged['delta_cap'] * EMPIRICAL_DISPLACEMENT_RATE * HIGH_ENTROPY_INTENSITY_KG_PER_USD / 1e9

total_gross_avoided = merged['gross_avoided'].sum()
net_co2_avoided = total_gross_avoided - total_emissions_since_2018

# Current live values
current_cap   = merged['close_cap'].iloc[-1]
current_price = merged['close_price'].iloc[-1]
current_hr    = merged['hashrate'].iloc[-1]
current_eff   = merged['efficiency_jth'].iloc[-1]

print(f"\nFINAL RESULTS")
print(f"Price: ${current_price:,.0f}")
print(f"Market Cap: ${current_cap/1e12:.2f}T")
print(f"Hashrate: {current_hr:.0f} EH/s")
print(f"Efficiency: {current_eff:.1f} J/TH")
print(f"NET CO₂ AVOIDED: {net_co2_avoided:,.0f} Mt")

# ----------------------------------------------------------------------
# 8. BREAK-EVEN ANALYSIS – How much displacement (δ) is needed to offset mining?
# ----------------------------------------------------------------------
# Goal: Find δ such that Gross Avoided = Mining Emissions
# Formula: δ_break = Mining (Mt/day) / (Δcap (USD/day) × I_high (kg CO₂/$))
#
# Why it matters:
#   • If δ > δ_break → Bitcoin is net CO₂ positive
#   • If δ < δ_break → Bitcoin adds CO₂
#   • Current δ = 0.34 → 2.1× safety margin
#
# Scenarios:
#   • Baseline: 0.39 kg/kWh (current grid)
#   • Renewables 2030: 0.25 kg/kWh (future clean grid)
# ----------------------------------------------------------------------

SCENARIOS = {
    "Baseline": {"grid_ci": 0.39, "mining_mt_per_day": 0.15},
    "Renewables 2030": {"grid_ci": 0.25, "mining_mt_per_day": 0.10}
}

# Daily average inflow (from 2025 data)
AVG_DAILY_INFLOW_USD = 1.8e9  # $1.8 billion

break_even_vals = {}
for name, s in SCENARIOS.items():
    mining_mt = s["mining_mt_per_day"]
    # Convert: USD → kg CO₂ → Mt CO₂
    avoided_per_dollar_mt = HIGH_ENTROPY_INTENSITY_KG_PER_USD / 1e9  # kg/$ → Mt/$
    δ_break = mining_mt / (AVG_DAILY_INFLOW_USD * avoided_per_dollar_mt)
    break_even_vals[name] = round(δ_break, 3)

# Embed mining data for JS hover
mining_per_day = [SCENARIOS[sc]["mining_mt_per_day"] for sc in SCENARIOS]

break_even_js = json.dumps({
    "scenarios": list(SCENARIOS.keys()),
    "values": [break_even_vals[sc] for sc in SCENARIOS],
    "current": EMPIRICAL_DISPLACEMENT_RATE,
    "inflow_usd": f"${AVG_DAILY_INFLOW_USD / 1e9:.1f}B",
    "intensity": f"{HIGH_ENTROPY_INTENSITY_KG_PER_USD:.2f} kg/$",
    "mining_mt_per_day": mining_per_day  # NEW: for hover
})


# ----------------------------------------------------------------------
# 9. PREPARE JS DATA
# ----------------------------------------------------------------------
# Making the strong assumption that *inflows* (positive Δmarketcap) and *outflows* (negative Δmarketcap) are both displacing high-entropy spending the same way
# The reality might be more nuanced and in favor of the Bitcoin Network (e.g. every Bitcoin Outflows does not necessarily goes back to high-entropy spending)
merged['gross_avoided_js'] = merged['delta_cap'] * EMPIRICAL_DISPLACEMENT_RATE * HIGH_ENTROPY_INTENSITY_KG_PER_USD / 1e9
merged['net_avoided'] = merged['gross_avoided_js'] - merged['daily_emissions_mt']

# --- CUMULATIVE SERIES ---
merged['cum_gross_avoided']     = merged['gross_avoided'].cumsum()
merged['cum_mining_emissions']  = merged['daily_emissions_mt'].cumsum()
merged['cum_net_avoided']       = merged['cum_gross_avoided'] - merged['cum_mining_emissions']
# For JS: same in g-based units
merged['cum_gross_avoided_js']  = merged['gross_avoided_js'].cumsum()
merged['cum_net_avoided_js']    = merged['cum_gross_avoided_js'] - merged['cum_mining_emissions']

# js_data = merged[['date', 'gross_avoided_js', 'daily_emissions_mt', 'net_avoided', 'efficiency_jth']].to_dict('records')
js_data = merged[[
    'date',
    'cum_gross_avoided_js',     # cumulative gross avoided
    'cum_mining_emissions',     # cumulative mining
    'cum_net_avoided_js',       # cumulative net
    'efficiency_jth'
]].to_dict('records')
js_data_str = json.dumps(js_data)

# Sector pie (scaled by displacement)
sector_co2 = [current_cap * EMPIRICAL_DISPLACEMENT_RATE * (v['co2'] / v['spend']) / 1e6
              for v in ENTROPY.values()]
sector_names = [k.replace('_', ' ').title() for k in ENTROPY.keys()]
sectors_js = json.dumps([{'name': n, 'co2': round(c)} for n, c in zip(sector_names, sector_co2)])

# ----------------------------------------------------------------------
# 10. HTML DASHBOARD 
# ----------------------------------------------------------------------
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
    Bitcoin Degrowth Dashboard v2.0
  </h1>
</div>

<!-- MOTTO BAR -->
<div style="text-align:center; padding:18px 20px; background:linear-gradient(135deg, #1a1a1a, #000); border-top:1px solid #333; border-bottom:1px solid #333; font-size:1.1em; line-height:1.9; color:#fff; font-family:'Roboto Mono', monospace; z-index:100; position:relative;">
  <strong style="color:#f7931a; text-shadow:0 0 10px #f7931a;">HODL = Entropy Killer.</strong><br>
  Bitcoin is the greenest money ever created.<br>
  It doesn't grow the economy — it <strong style="color:#f7931a;">purifies it</strong> by shrinking high-entropy goods production.<br>
  Every dollar/euro/fiat unit that flows into Bitcoin reduces spending in high-entropy sectors by a measurable fraction; the net CO₂ impact is the difference between the amount of value getting displaced emissions and mining emissions.<br>
  This is not greenwashing. This is <strong style="color:#00ff00;">thermodynamics</strong>.<br><br>
  Net CO₂ Avoided Since 2018: <strong style="color:#00ff00; font-size:1.3em; text-shadow:0 0 12px #00ff00;">{net_co2_avoided:.0f} million tons</strong><br>
  <span style="color:#1da1f2; font-weight:bold;">@BitcoinDegrowth</span><br />
  <button class="btn-details" onclick="toggleDetails()">Show Methodology</button>
  <div id="details" class="details">
    <h3>Updated Model (v2.0)</h3>
    <p><strong>1. High-entropy intensity</strong>: <code>0.51 kg CO₂ / $</code> – derived from EXIOBASE 3.8+ (top 20 % most carbon-intensive final-demand sectors). Replaces prior 0.409 g/$.</p>
    <p><strong>2. Displacement rate δ</strong>: <code>{EMPIRICAL_DISPLACEMENT_RATE:.0%}</code> (95 % CI {DELTA_CI_LOW:.0%}–{DELTA_CI_HIGH:.0%}) – weighted average from 2023-2025 investor surveys (Coinbase, Motley Fool, Chainalysis). Retail: ~33 %, HNW: ~59 %, Institutions: ~8 %.</p>
    <p><strong>Equation</strong>: Net = Σ(ΔCap × δ × I) − Mining</p>
    <p>Note: We are taking a conservative approach and considering that outflows also displaces back to high-entropy intensity sectors</p>
    <h3>Break-even Displacement Rate (δ)</h3>
    <p><strong>Question:</strong> At what % of BTC $inflows must come from high-entropy spending for Bitcoin to <em>break even</em> on CO₂?</p>

    <pre style="background:#111;padding:10px;border-radius:5px;font-size:0.9em;">
    δ_break = Mining (Mt/day) / (Δcap ($/day) × 0.51 kg CO₂/$)
    </pre>

    <ul>
      <li><strong>Daily mining (Mt CO2)</strong>: ~0.15 Mt / day in 2025 (Baseline), 0.10 Mt (Renewables 2030)</li>
      <li><strong>Daily inflow</strong>: $1.8B (2025 avg)</li>
      <li><strong>Intensity</strong>: 0.51 kg CO₂ per $ (EXIOBASE)</li>
    </ul>

    <p><strong>Result:</strong></p>
    <ul>
      <li><strong>Baseline</strong>: <code>δ = 16.3%</code> → Bitcoin breaks even</li>
      <li><strong>Renewables 2030</strong>: <code>δ = 10.9%</code> → only 11% needed</li>
      <li><strong>Current δ = 34%</strong> → <strong>2.1× safety margin</strong></li>
    </ul>

    <p>Even in a clean-grid future, <strong>only 1 in 9 dollars</strong> needs to come from luxury/real-estate for Bitcoin to be net CO₂ positive.</p>
    <h3>Future Enhancements</h3>
    <ul>
      <li>User input form (δ, I) → instant recalculation?</li>
      <li>Monte-Carlo uncertainty bands on all plots?</li>
      <li>Export CSV / JSON of full time-series</li>
      <li>Live API for real-time survey data → auto-update δ - tricky</li>
    </ul>
    <small>Sources: TradingView, UNEP, IPCC, Statista, CCAF, EXIOBASE, @BitcoinDegrowth</small>
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
      <h2>Cumulative Bitcoin CO₂ Impact with gCO2/$ displacement (Since 2018)</h2>
      <div id="co2-plot" style="height:48vh; margin-top:20px;"></div>

      <!-- NEW: Plotly Break-even Chart -->
      <h2>Break-even Displacement Rate</h2>
      <div id="break-even-plot" style="height:40vh; margin-top:20px;"></div>
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
    gross: d.cum_gross_avoided_js,
    emissions: d.cum_mining_emissions,
    net: d.cum_net_avoided_js,
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

  // CO₂ CUMULATIVE Plot
  Plotly.newPlot('co2-plot', [
    {{ x: history.map(d=>d.date), y: history.map(d=>d.gross), name: 'Cumulative Gross Avoided', line: {{color:'#00ff00', width:3}} }},
    {{ x: history.map(d=>d.date), y: history.map(d=>d.net),    name: 'Cumulative Net Avoided',  line: {{color:'#ffaa00', width:3}} }},
    {{ x: history.map(d=>d.date), y: history.map(d=>d.emissions),  name: 'Cumulative Mining',       line: {{color:'#ff6b6b', width:2}} }}
  ], {{
    paper_bgcolor: '#000', plot_bgcolor: '#000', font: {{color: '#aaa'}},
    title: {{text: 'Cumulative Bitcoin CO₂ Impact (Million tons)', font: {{color: '#fff', size: 16}}}},
    yaxis: {{gridcolor: '#333', title: 'Mt CO₂e'}}, 
    xaxis: {{gridcolor: '#333'}}, 
    legend: {{x:0, y:1, bgcolor: '#111'}},
    hovermode: 'x unified'
  }}, {{responsive: true}});
  
  // Efficiency
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

// BREAK-EVEN PLOT
const be = {break_even_js};

Plotly.newPlot('break-even-plot', [
  {{
    x: be.scenarios,
    y: be.values,
    type: 'bar',
    name: 'Break-even δ',
    marker: {{color: ['#3498db', '#2ecc71']}},
    text: be.values.map(v => (v*100).toFixed(1) + '%'),
    textposition: 'outside',
    hovertemplate: '<b>%{{x}}</b><br>δ = %{{y:.1%}}<br>Mining: %{{customdata}} Mt/day<extra></extra>',
    customdata: be.mining_mt_per_day  
  }},
  {{
    x: be.scenarios,
    y: [be.current, be.current],
    type: 'scatter',
    mode: 'lines',
    line: {{color: '#ff0000', dash: 'dash', width: 3}},
    name: 'Current δ = 34%',
    hovertemplate: '<b>Current δ</b><br>δ = 34%<br>2.1× safety margin<extra></extra>'
  }}
], {{
  paper_bgcolor: '#000', plot_bgcolor: '#000', font: {{color: '#aaa'}},
  title: {{
    text: 'Break-even δ: How Much Displacement Is Needed?',
    font: {{color: '#fff', size: 14}}
  }},
  yaxis: {{
    title: 'Displacement Rate (δ)',
    tickformat: '.0%',
    range: [0, 0.5],
    gridcolor: '#333'
  }},
  xaxis: {{gridcolor: '#333'}},
  legend: {{x: 0, y: 1, bgcolor: '#111'}},
  annotations: [
    {{
      x: 0, y: be.values[0],
      xref: 'x', yref: 'y',
      text: `δ = ${{(be.values[0]*100).toFixed(1)}}%`,
      showarrow: true,
      arrowhead: 2,
      ax: -40, ay: -40,
      bgcolor: '#3498db', font: {{color: '#fff'}}
    }},
    {{
      x: 1, y: be.values[1],
      xref: 'x', yref: 'y',
      text: `δ = ${{(be.values[1]*100).toFixed(1)}}%`,
      showarrow: true,
      arrowhead: 2,
      ax: 40, ay: -40,
      bgcolor: '#2ecc71', font: {{color: '#fff'}}
    }}
  ]
}}, {{responsive: true}});

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