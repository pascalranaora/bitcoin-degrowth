# Bitcoin Degrowth Dashboard

> **HODL = Entropy Killer.**  
> A live, animated, thermodynamically sound dashboard proving **Bitcoin avoids more CO₂ than it emits**.

Live demo: [https://pascalranaora.github.io/bitcoin-degrowth/](https://pascalranaora.github.io/bitcoin-degrowth/)
or in `index.html` (open locally or deploy)

---

## Overview

This dashboard calculates **net CO₂ avoided** by Bitcoin since 2018 by comparing:
- **Gross CO₂ avoided** = Market Cap × 0.409 g CO₂/$ (diverted from high-entropy sectors)
- **Mining emissions** = Hashrate × ASIC Efficiency × Grid Intensity (live from Cambridge CBECI)

**Result (Nov 10, 2025):**  
> **Net CO₂ Avoided: ~1,800,000 Mt**  
> **Bitcoin avoids 2.8× more CO₂ than it emits**

---

## Features

| Feature | Status |
|-------|--------|
| Live Cambridge CBECI emissions | Working |
| Real-time BTC price, cap, hashrate (TradingView) | Working |
| Power-law ASIC efficiency trend (J/TH) | Working |
| Animated net CO₂ counter | Working |
| Scrollable, responsive layout | Working |
| Motto banner below header | Working |
| Default-open computation details | Working |

---

## Setup & Run

### 1. Install Dependencies

```bash
pip install pandas requests beautifulsoup4 tvdatafeed numpy scipy
```

> `tvdatafeed` requires **no login** for public data.

### 2. Run the Generator

```bash
python generate_dashboard.py
```

> Generates `index.html` in the same folder.

### 3. Open Dashboard

```bash
open index.html
# or
python -m http.server 8000
```

---

## Data Sources

| Data | Source | Symbol |
|------|--------|--------|
| Price | Coinbase | `BTCUSD` |
| Market Cap | CryptoCap | `BTC` |
| Hashrate | Blockchain.com | `HRATE@BCHAIN` (GH/s → EH/s) |
| Emissions | Cambridge CBECI | [ccaf.io/cbnsi/cbeci/ghg](https://ccaf.io/cbnsi/cbeci/ghg) |
| Efficiency | Historical ASIC data (CoinShares, Cambridge) | Power-law fit |

---

## Entropy Sectors (2025 est.)

| Sector | Spend | CO₂ | g CO₂/$ |
|-------|--------|--------|----------|
| Fast Fashion | $2.5T | 1,200 Mt | 0.480 |
| Luxury Yachts | $35B | 1 Mt | 0.029 |
| Luxury Resorts | $120B | 363 Mt | 0.302 |
| Real Estate Spec | $8.0T | 2,800 Mt | 0.350 |
| **Total** | **$10.655T** | **4,364 Mt** | **0.409** |

---

## Customization

| Want to change? | Edit |
|----------------|------|
| Entropy sectors | `ENTROPY` dict |
| CO₂ per kWh | `CO2_PER_KWH = 0.475` |
| Efficiency curve | `eff_jth` array |
| Start year | `START_DATE` |

---

## Deployment

Deploy `index.html` anywhere:
- GitHub Pages
- Vercel / Netlify
- IPFS

```bash
# GitHub Pages
git push origin main
# Settings → Pages → main → /root
```

---

## Contributing

1. Fork
2. Improve
3. PR with **thermodynamic rigor**

---
> *Stack sats. Reduce entropy. Purify the system.*
> — **@BitcoinDegrowth**, November 10, 2025

--- 

