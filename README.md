# Bitcoin Degrowth Dashboard Full Scope 3

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/pascalranaora/bitcoin-degrowth)  
[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-green?logo=web)](https://www.bitcoin-degrowth.org/)

**HODL = Entropy Killer.** Bitcoin isn't just digital gold—it's the greenest money ever created. By capping supply at 21 million coins, Bitcoin incentivizes holding over endless consumption, shrinking high-entropy (carbon-intensive) economic activity. This project aims to model Bitcoin's net environmental impact by accounting for what we would call **Value Displacement**: the CO₂ emissions *displaced* from reduced spending on wasteful goods minus the emissions from mining and operating the network day-to-day (BAU). **Spoiler: It's a net positive, with a growing safety margin as adoption rises and renewables scale.**

**As of November 13, 2025**, the dashboard shows Bitcoin has avoided **24 million tons of CO₂ since 2018**, with daily net savings accelerating.  
**Live Dashboard →** [https://www.bitcoin-degrowth.org/](https://www.bitcoin-degrowth.org/)

---

## Quick Start

### Prerequisites
- Python 3.8+
- Required libraries: `numpy`, `pandas`, `matplotlib`, `requests` (for API data), `scipy`, `beautifulsoup`, `tvdatafeed`

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Model Locally
1. Clone the repo:
   ```bash
   git clone https://github.com/pascalranaora/bitcoin-degrowth.git
   cd bitcoin-degrowth
   ```

2. Run the core model:
   ```bash
   python code_degrowth.py
   ```
   This executes the simulation, outputs key metrics (e.g., net CO₂ avoided), and generates a **full HTML dashboard** with cumulative impacts, efficiency curves, and interactive visualizations.

### Example Output
Running `code_degrowth.py` prints:
```
Dashboard FULL SCOPE 3 + v2 DETAILS generated: index.html
Open → file://Desktop/bitcoin-degrowth/index.html

Bitcoin has avoided 24 million tons of CO₂ since 2018 — FULL SCOPE 3.
You are thermodynamically correct.

FINAL RESULTS — FULL SCOPE 3
Price: $101,639
Market Cap: $2.03T
Hashrate: 1087 EH/s
Efficiency: 13.1 J/TH
BAU Emissions: 1.00 Mt/year
Secondary Emissions: 12.9 Mt/year
Gross Avoided: 352 Mt
Total Gross Emissions: 328 Mt
NET CO₂ AVOIDED: 24 Mt
```

---

## Dashboard Overview — Full Scope 3

The dashboard visualizes Bitcoin's "entropy vacuum" effect: inflows displace high-entropy spending, creating a feedback loop of reduced emissions. **v3.5 uses the original v2 displacement logic** — **including outflows reversing displacement** — for maximum conservatism.

### Key Sections & Metrics (Updated Nov 13, 2025)
- **Header & Summary**:
  - "HODL = Entropy Killer" – Core thesis on Bitcoin as degrowth money.
  - Live data: Market Cap ($2.03T), Hash Rate (1087 EH/s), Efficiency (13.1 J/TH).

- **Net CO₂ Impact**:
  - **Gross Avoided**: **352 Mt** (total displaced emissions since 2018).
  - **Mining Emissions**: **313 Mt** (conservative estimate, 52% renewables).
  - **Secondary Emissions (Scope 3)**: **12.9 Mt/year** (ASIC manufacturing + e-waste + facilities).
  - **BAU Emissions**: **1.0 Mt/year** (full nodes + Lightning).
  - **Total Gross Emissions**: **328 Mt**
  - **Net Avoided**: **24 Mt** (positive offset; daily: ~0.066 Mt saved).

- **Displacement Rate (δ)**:
  - Weighted average: **34%** (95% CI: 29%–39%).
  - Breakdown:
    - Retail: ~33% (from consumer spending shifts).
    - High-Net-Worth (HNW): ~59% (long-term holds via ETFs).
    - Institutions: ~8% (conservative reserve allocation).
  - Derived from 2023–2025 surveys (Coinbase, Motley Fool, Chainalysis).

- **High-Entropy Intensity (I)**:
  - **0.51 kg CO₂ per $ displaced** (from EXIOBASE 3.8+ multi-regional IO database).

- **Break-Even Analysis**:
  - **Baseline (2025)**: $$\delta_{\text{break}} = 20.5\%$$
  - **Realistic 2030 Scenario**: $$\delta_{\text{break}} = 4.9\%$$
  - **Safety Margin**: **1.66× today → 6.94× by 2030** (current δ exceeds break-even robustly).

- **Core Equation (Full Scope 3)**:
  ![CoreEquation](https://github.com/pascalranaora/bitcoin-degrowth/blob/main/CoreEquation.png)
  - $$\Delta \text{Cap}_t$$: **Full daily market cap change** (positive = inflow, negative = outflow).  
  - **Outflows reverse displacement** — money leaving Bitcoin is assumed to return to high-entropy spending.  
  - **Maximum conservatism**: No credit for HODLing during bear markets.  

### Visualizations
- **Cumulative Net CO₂ Chart**: Line plot showing avoided vs. mining + BAU + ASIC lifecycle (2018–2030 projection).
- **δ Breakdown Bar Chart**: Stacked bars by investor type (retail/HNW/institutions).
- **Sector CO₂ Avoidance**: CO₂ displaced per sector (fast fashion, yachts, resorts, real estate).
- **Mining Efficiency**: Power-law decline in J/TH (from 89 J/TH in 2018 to 13.1 J/TH in 2025).

### Future Enhancements (Roadmap)
- The static displacement is a good first approximation but we need more robust regular surveys and longitudinal studies consumer spending/sentiment/investing portfolio to evaluate effects of Bitcoin HODLing on consumerism
- User input form for custom δ/I with instant Monte-Carlo uncertainty bands.
- Export to PDF/CSV for reports.
- Live API integration and more accurate surveys and peer-reviewed studies on consumer consumption behaviors deviation and/or portfolio investment allocation for real-time inflows and displacement rate computations.
- Mobile-responsive design.

Data last refreshed: Real-time (hash rate/efficiency from TradingView; cap from CryptoCap).

---

## The Model: Mathematics & Assumptions

This project quantifies Bitcoin's degrowth potential using a **net emissions framework under full Scope 3 accounting**. Bitcoin's fixed supply promotes low-time-preference behavior: HODLers spend less on high-entropy goods, displacing ~0.51 kg CO₂ per $ shifted.

### Key Formula Derivation

1. **Displacement Calculation**:  
   - $$\delta = \sum (w_i \times \delta_i)$$
   where $$w_i$$ are inflow weights (retail: 60%, HNW: 30%, inst: 10%)  
   Example: $$(0.6 \times 0.33) + (0.3 \times 0.59) + (0.1 \times 0.08) = 0.34$$  
   CI via bootstrapping survey SE (5–10%).

2. **Daily Net CO₂**:  
   - $$\text{Net} = (\Delta \text{Cap} \times \delta \times I) - (E_{\text{mining}} + E_{\text{BAU}} + E_{\text{ASIC}} + E_{\text{facilities}})$$     
   Example (2025): $$\left(1.8 \times 10^9 \times 0.34 \times 0.51\right) - 0.19 = 0.122 \text{ Mt/day saved}$$

3. **Break-Even δ**:  
   - $\delta_{\text{break}} = \frac{E_{\text{total}}}{\Delta \text{Cap} \times I}$$
   - Solve by setting Net = 0:  
     $$\delta = \frac{E_{\text{mining}} + E_{\text{BAU}} + E_{\text{ASIC}} + E_{\text{facilities}}}{\Delta \text{Cap} \times I}$$
   - **2025**: $$\delta_{\text{break}} = 20.5\%$$
   - **2030 (realistic)**: $$\delta_{\text{break}} = 4.9\%$$

### Components (Full Scope 3)

| Component | Formula | Value (2025) | Source |
|---------|--------|-------------|--------|
| $E_{\text{BAU}}$ | $$\frac{(N_{\text{nodes}} \times P_{\text{node}} + N_{\text{LN}} \times P_{\text{LN}}) \times 8760}{10^6} \times 0.475$$ | **1.0 Mt/year** | Bitnodes.io, 1ml.com, Springer 2025 |
| $E_{\text{ASIC}}$ | $$\frac{H \times 0.10 \times 1000}{10^9} + \frac{H \times 0.10 \times 50}{10^9}$$ | **12.4 Mt/year** | Talens-Perales (2025), Onat et al. (2025), de Vries (2021) |
| $E_{\text{facilities}}$ | $$\frac{15 \times 10^3 \times 500}{4 \times 10^6}$$ | **0.5 Mt/year** | Industry LCA averages |

> **Total Scope 3 addition**: **~13.9 Mt/year** → **~100 Mt since 2018**

### Assumptions & Sensitivities
- **Inflows**: $1.8B/day avg (2025; from Chainalysis/TradingView).
- **Mining Emissions**: 0.86 Mt/day (UNEP/IPCC/CCAF; drops to 0.21 Mt/day by 2030 w/ 90% renewables + 35% efficiency).
- **Conservative Bias**: Assumes **outflows fully reverse displacement**; no compounding HODL effects.
- Sensitivities: ±20% on δ yields Net range **0.02–0.10 Mt/day** (still positive).
- Full code in `code_degrowth.py` includes Monte-Carlo sims for CI.

---

## Sources & Data

### Detailed Investor Survey Sources
*(Unchanged from v2 — see full table below)*

| Survey | Date & Methodology | Sample Size & Scope | Key Findings Relevant to δ | Direct Link |
|--------|--------------------|---------------------|----------------------------|-------------|
| **Coinbase Institutional: 2025 Institutional Investor Digital Assets Survey** | January 2025; Conducted by Coinbase Institutional in collaboration with EY-Parthenon. | 352 institutional investors globally. | 59% plan >5% AUM to digital assets. | [Link](https://www.coinbase.com/institutional/research-insights/research/market-intelligence/2025-institutional-investor-survey) |
| **Motley Fool: 2025 Cryptocurrency Investor Trends Survey** | January–May 2025; Distributed via Pollfish. | ~1,000+ U.S. respondents. | 33% cite "replacing wasteful spending". | [Link](https://www.fool.com/money/research/study-americans-cryptocurrency/) |
| **Chainalysis: 2025 Global Crypto Adoption Index** | September–October 2025; Annual report. | Global dataset (millions of txns). | HNW/ETFs up 59%. | [Link](https://www.chainalysis.com/blog/2025-global-crypto-adoption-index/) |

- **Aggregation for δ**: Weighted average: **34%**. 95% CI (29%–39%) from bootstrapping.

### Full Scope 3

| Component | Source | Link |
|---------|--------|------|
| **ASIC Manufacturing** | Talens-Perales et al. (2025) – *Life Cycle Assessment of Bitcoin Mining Hardware* | https://arxiv.org/abs/2401.17512 |
| **ASIC Imports & E-waste** | Onat et al. (2025) – *Sustainability Science* | https://doi.org/10.1007/s11625-024-01576-5 |
| **E-Waste CO₂e** | de Vries (2021) – *Joule* | https://doi.org/10.1016/j.joule.2021.04.007 |
| **Full Nodes** | Bitnodes.io API | https://bitnodes.io |
| **Lightning Nodes** | 1ml.com | https://1ml.com |
| **Node Power** | Springer 2025 Bitcoin node benchmarks | — |
| **Facility Construction** | Industry LCA (amortized 500 t CO₂/MW over 15 yr) | — |

- **Emissions Data**: EXIOBASE 3.8+ (embodied CO₂), UNEP/IPCC (mining baselines), Statista/CCAF (efficiency).
- **Market Data**: TradingView (cap/inflows, hashrate, bitcoin price).
- **Broader Reading**:
  - [Bitcoin Sufficiency Protocol](https://www.sufficiencyprotocol.org) (Nov 2025).
  - [Bitcoin Magazine: The Degrowth of Bitcoin](https://bitcoinmagazine.com/culture/the-degrowth-of-bitcoin) (Aug 2024).
  - [Medium: Radical System Change—Bitcoin & Degrowth](https://medium.com/@example/radical-system-change-bitcoin-degrowth) (Sep 2022).

---

## Contributing
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/entropy-viz`).
3. Commit changes (`git commit -m "Add entropy gauge chart"`).
4. Push & PR.

Issues? Open a ticket. Discussions welcome on X: [@BitcoinDegrowth](https://x.com/BitcoinDegrowth).

---

## License
MIT License – Free to fork, extend, and HODL. See [LICENSE](LICENSE).

---

## Acknowledgments
- Built with love by @BitcoinDegrowth.
- Thanks to EXIOBASE team, Talens-Perales, Onat, de Vries, Bitnodes, 1ml.com, Chainalysis researchers, and the Bitcoin Community.
- Powered by open-source: NumPy, Pandas, Plotly.

**Bitcoin: Shrinking the entropy beast, one satoshi at a time.**  
**Full Scope 3, maximum conservatism, still net positive.**  
— @BitcoinDegrowth, November 13, 2025
