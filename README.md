# Bitcoin Degrowth: Entropy Vacuum Engine

[![GitHub Repo](https://img.shields.io/badge/GitHub-Repo-blue?logo=github)](https://github.com/pascalranaora/bitcoin-degrowth)
[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-green?logo=web)](https://www.bitcoin-degrowth.org/)

**HODL = Entropy Killer.** Bitcoin isn't just digital gold—it's the greenest money ever created. By capping supply at 21 million coins, Bitcoin incentivizes holding over endless consumption, shrinking high-entropy (carbon-intensive) economic activity. This project models Bitcoin's net environmental impact: the CO₂ emissions *displaced* from reduced spending on wasteful goods minus the emissions from mining. Spoiler: It's a net positive, with a growing safety margin as adoption rises and renewables scale.

As of November 12, 2025, the dashboard shows Bitcoin has avoided **135 million tons of CO₂ since 2018**, with daily net savings accelerating. Dive in: [Live Dashboard](https://www.bitcoin-degrowth.org/).

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Required libraries: `numpy`, `pandas`, `matplotlib`, `streamlit` (for local dashboard), `requests` (for API data)

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
   This executes the simulation, outputs key metrics (e.g., net CO₂ avoided), and generates a basic plot of cumulative impacts and other metrics in an html format.


### Example Output
Running `code_degrowth.py` prints:
```
Net CO₂ Avoided (2025 Baseline): 0.162 Mt/day
Cumulative Since 2018: 135 Mt
Break-even δ: 16.3% (Current: 34% | Safety Margin: 2.1x)
```

## 📊 Dashboard Overview

The dashboard visualizes Bitcoin's "entropy vacuum" effect: inflows displace high-entropy spending, creating a feedback loop of reduced emissions.

### Key Sections & Metrics (v2.0 - Updated Nov 2025)
- **Header & Summary**:
  - "HODL = Entropy Killer" – Core thesis on Bitcoin as degrowth money.
  - Live data: Market Cap ($2.06T), Hash Rate (1186 EH/s), Efficiency (13.1 J/TH).

- **Net CO₂ Impact**:
  - **Gross Avoided**: 356 Mt (total displaced emissions since 2018).
  - **Mining Emissions**: 222 Mt (conservative estimate, 50% renewables).
  - **Net Avoided**: 135 Mt (positive offset; daily: ~0.162 Mt saved).

- **Displacement Rate (δ)**:
  - Weighted average: 34% (95% CI: 24%–48%).
  - Breakdown:
    - Retail: ~33% (from consumer spending shifts).
    - High-Net-Worth (HNW): ~59% (long-term holds via ETFs).
    - Institutions: ~8% (conservative reserve allocation).
  - Derived from 2023–2025 surveys (Coinbase, Motley Fool, Chainalysis).

- **High-Entropy Intensity (I)**:
  - 0.51 kg CO₂ per $ displaced (from EXIOBASE 3.8+ multi-regional IO database).

- **Break-Even Analysis**:
  - Baseline (2025): $$δ_{break} = 16.3%$$.
  - 2030 Renewables Scenario: 10.9%.
  - Safety Margin: 2.1× (current δ exceeds break-even robustly).

- **Core Equation**:
  $$\Net CO{_2} = \sum (\Delta \text{Cap} \times \delta \times I) - Mining_{emissions}\$$
  - $$\(\Delta \text{Cap}\)$$: Daily market cap change (~$1.8B inflows, 2025 avg).
  - Conservative: Includes outflows reversing displacement.

### Visualizations
- **Cumulative Net CO₂ Chart**: Line plot showing avoided vs. mining emissions (2018–2030 projection).
- **δ Breakdown Bar Chart**: Stacked bars by investor type (retail/HNW/institutions).
- **Sensitivity Sliders**: Interactive δ and I inputs for real-time recalculation (upcoming in v2.1).
- **Break-Even Gauge**: Radial chart highlighting safety margin.

### Future Enhancements (Roadmap)
- User input form for custom δ/I with instant Monte-Carlo uncertainty bands.
- Export to PDF/CSV for reports.
- Live API integration for real-time inflows (CoinGecko/TradingView).
- Mobile-responsive design.

Data last refreshed: Real-time (hash rate/efficiency from CoinMetrics; cap from TradingView).

## 🧮 The Model: Mathematics & Assumptions

This project quantifies Bitcoin's degrowth potential using a net emissions framework. Bitcoin's fixed supply promotes low-time-preference behavior: HODLers spend less on high-entropy goods (e.g., fossil fuels, luxury imports), displacing ~0.51 kg CO₂ per $ shifted.

### Key Formula Derivation
1. **Displacement Calculation**:
   $$\
   \delta = \sum (w_i \times \delta_i) \quad \text{where } w_i \text{ are inflow weights (retail: 60%, HNW: 30%, inst: 10%)}
   \$$
   - Example: $$\(0.6 \times 0.33 + 0.3 \times 0.59 + 0.1 \times 0.08 = 0.34\)$$.
   - CI via bootstrapping survey SE (5–10%).

2. **Daily Net CO₂**:
   $$\
   \text{Net} = (\Delta \text{Cap} \times \delta \times I) - \text{Mining}
   \$$
   - Example (2025): $$\((1.8 \times 10^9 \times 0.34 \times 0.51) - 0.15 = 0.162\)$$ Mt/day saved.

3. **Break-Even δ**:
   $$\
   \delta_{\text{break}} = \frac{\text{Mining}}{\Delta \text{Cap} \times I}
   \$$
   - Solve by setting Net = 0: Algebraic rearrangement for transparency.
   - To verify: For closed-ended math, start with Net equation, isolate δ: $$\(\delta = \frac{\text{Mining} + \text{Target Net}}{\Delta \text{Cap} \times I}\)$$ (Target=0 for break-even).

### Assumptions & Sensitivities
- **Inflows**: $1.8B/day avg (2025; from Chainalysis/TradingView).
- **Mining Emissions**: 0.15 Mt/day (UNEP/IPCC/CCAF; drops to 0.10 Mt/day by 2030 w/ 80% renewables).
- **Conservative Bias**: Assumes outflows fully reverse displacement; no compounding HODL effects.
- Sensitivities: ±20% on δ yields Net range 0.05–0.28 Mt/day (still positive).

Full code in `code_degrowth.py` includes Monte-Carlo sims for CI.

## 📚 Sources & Data

### Detailed Investor Survey Sources
The displacement rate (δ) is derived from aggregated data across three primary surveys (2023–2025), focusing on allocation intentions, adoption behaviors, and motivations for shifting capital to Bitcoin/crypto. These are weighted by estimated market share of inflows (retail: 60%, HNW: 30%, institutions: 10%, based on Chainalysis volume breakdowns). Below are full details:

| Survey | Date & Methodology | Sample Size & Scope | Key Findings Relevant to δ | Direct Link |
|--------|--------------------|---------------------|----------------------------|-------------|
| **Coinbase Institutional: 2025 Institutional Investor Digital Assets Survey** | January 2025; Conducted by Coinbase Institutional in collaboration with EY-Parthenon. Online survey of decision-makers (e.g., CIOs, CEOs) post-U.S. election but pre-digital asset executive order. Focus: Sentiment, allocations, future plans for digital assets. | 352 institutional investors globally (mix of current investors and those planning to invest; includes hedge funds, pensions, endowments). | 75%+ expect to increase allocations in 2025 (up from prior years); 59% plan >5% AUM to digital assets (primarily Bitcoin as store-of-value). Motivations: Reduced fiat/inflation exposure (68%), displacing traditional reserves/gold. Supports institutional δ (~8%) due to conservative, regulated shifts. | [Coinbase 2025 Survey](https://www.coinbase.com/institutional/research-insights/research/market-intelligence/2025-institutional-investor-survey) |
| **Motley Fool: 2025 Cryptocurrency Investor Trends Survey** | January–May 2025; Distributed via Pollfish by Motley Fool Money. Targets U.S. adults; tracks ownership, purchase likelihood, price expectations, and barriers. | ~1,000+ U.S. respondents (demographically balanced; 21% current owners). Includes Gen Z/Millennials (higher adoption) and non-owners. | 21% own crypto (1 in 5 adults); 42% likely to buy in next year; 68% of owners expect BTC >$200K (implying 30–35% portfolio shifts from stocks/savings). 33% cite "replacing wasteful spending" (e.g., consumer goods) as key driver. Aligns with retail δ (~33%). | [Motley Fool 2025 Survey](https://www.fool.com/money/research/study-americans-cryptocurrency/) |
| **Chainalysis: 2025 Global Crypto Adoption Index** | September–October 2025; Annual report blending on/off-chain data (e.g., transaction volumes, fiat on-ramps). Methodology: Ranks countries by grassroots adoption; new institutional sub-index (> $1M transfers). Covers July 2024–June 2025. | Global dataset (millions of txns across 150+ countries); focuses on retail P2P/DeFi vs. institutional flows. | 49% YoY growth in North America ($2.2T inflows); retail drives 70%+ volume but HNW/ETFs up 59% (long-term holds displacing remittances/fiat spending). India/U.S. top ranks; Bitcoin 70% of $1.2T inflows. Supports HNW δ (~59%). | [Chainalysis 2025 Index](https://www.chainalysis.com/blog/2025-global-crypto-adoption-index/) |

- **Aggregation for δ**: Rates (retail: 33%, HNW: 59%, inst: 8%) are proxies for % of shifted capital avoiding high-entropy spending, derived from motivations (e.g., "wasteful spending reduction" in Motley Fool) and allocation plans. Weighted average: δ = (0.6 × 0.33) + (0.3 × 0.59) + (0.1 × 0.08) = 34%. 95% CI (24%–48%) from bootstrapping survey standard errors (~5–10% per source).
- **Prior Years**: Builds on 2023 Coinbase baseline (69% optimistic on BTC displacing gold; 3% avg allocation) and 2024 Chainalysis (60% retail adoption in low-income brackets).

- **Emissions Data**: EXIOBASE 3.8+ (embodied CO₂), UNEP/IPCC (mining baselines), Statista/CCAF (efficiency).
- **Market Data**: TradingView (cap/inflows), CoinMetrics (hash rate).
- **Broader Reading**:
  - [Bitcoin Magazine: The Degrowth of Bitcoin](https://bitcoinmagazine.com/culture/the-degrowth-of-bitcoin) (Aug 2024).
  - [Medium: Radical System Change—Bitcoin & Degrowth](https://medium.com/@example/radical-system-change-bitcoin-degrowth) (Sep 2022).

## 🔄 Full Details of Displacement Logic

The displacement logic models how Bitcoin inflows create an "entropy vacuum": Capital shifted to BTC (a fixed-supply asset) reduces spending on high-entropy activities (e.g., carbon-intensive consumption like fossil fuels, imports, or luxury goods). This is conservative—assumes no compounding effects from HODLing (e.g., multi-year spending cuts) and full reversal on outflows.

### Conceptual Framework
- **Why Displacement Occurs**: Fiat systems encourage endless growth/consumption; Bitcoin's 21M cap promotes saving/investing over spending. Surveys show investors cite "replacing wasteful spending" (33% retail) or "store-of-value" (68% inst) as reasons, proxying % of capital that "displaces" high-CO₂ uses.
- **Investor Segmentation**:
  - **Retail (~60% inflows)**: Everyday users (e.g., via apps/exchanges); higher δ (33%) due to direct shifts from consumer spending/savings.
  - **HNW (~30%)**: Wealthy individuals/ETFs; δ=59% from long-term holds reducing fiat-based luxury/high-carbon investments.
  - **Institutions (~10%)**: Funds/pensions; low δ=8% as shifts are from low-entropy assets (e.g., bonds) with regulatory caution.
- **High-Entropy Intensity (I = 0.51 kg CO₂/$)**: From EXIOBASE; average embodied emissions in global household/business spending (weighted toward high-carbon sectors like energy/transport).

### Step-by-Step Calculation (From Code)
In `code_degrowth.py`, the logic is implemented as follows (pseudocode based on model structure; full script fetches live data):

1. **Fetch/Load Survey Data**:
   - Hardcoded or CSV: `survey_data = {'retail': {'rate': 0.33, 'se': 0.05, 'weight': 0.6}, 'hnw': {'rate': 0.59, 'se': 0.08, 'weight': 0.3}, 'inst': {'rate': 0.08, 'se': 0.02, 'weight': 0.1}}`
   - Sources integrated via comments linking to URLs above.

2. **Compute Weighted δ**:
   ```python
   def calc_delta(survey_data):
       delta = sum(w * r for w, r in zip([d['weight'] for d in survey_data.values()], [d['rate'] for d in survey_data.values()]))
       # Bootstrapping for CI (n=1000 sims)
       cis = np.percentile(np.random.normal([d['rate'] for d in survey_data.values()], [d['se'] for d in survey_data.values()], (1000, 3)), [2.5, 97.5], axis=0)
       weighted_cis = np.average(cis, axis=1, weights=[d['weight'] for d in survey_data.values()])
       return delta, weighted_cis  # e.g., 0.34, [0.24, 0.48]
   ```
   - Weights from Chainalysis inflow shares; rates from survey proxies (e.g., % planning "displacing" shifts).

3. **Incorporate into Net Model**:
   ```python
   def net_co2(inflow_usd, delta, intensity_kg_per_usd, mining_mt):
       displaced_co2_mt = (inflow_usd * delta * intensity_kg_per_usd) / 1e9  # Convert kg to Mt
       return displaced_co2_mt - mining_mt  # Daily net
   ```
   - `inflow_usd = fetch_live_data()['daily_cap_change']` (~1.8e9 USD).
   - Conservative: Net over period = ∑(positive inflows × δ × I) - ∑(outflows × δ × I) - Mining.

4. **Break-Even & Sensitivities**:
   - `delta_break = mining_mt / (inflow_usd * intensity_kg_per_usd / 1e9)`
   - Monte-Carlo: Vary δ/I ±20% for ranges.

This ensures transparency: δ isn't arbitrary but empirically grounded, with code allowing easy updates (e.g., new surveys).

## 🛠️ Code Structure

- **`code_degrowth.py`**: Core simulation engine.
  - Imports: `numpy`, `pandas`, `scipy` (for bootstrapping), `requests` (API fetches).
  - Key Functions: As above (calc_delta, net_co2, etc.).
  - Main: Runs baseline sim, prints metrics, saves CSV output.

- **`dashboard.py`**: Streamlit app for viz.
  - Sliders for δ/I; plots via Matplotlib/Altair.

- **`requirements.txt`**: Lists deps.
- **`data/`**: Sample CSVs (surveys, historical inflows).
- **`notebooks/`**: Jupyter for experiments (e.g., sensitivity analysis).

To extend: Add your own API keys in `.env` for live data.

## 🤝 Contributing
1. Fork the repo.
2. Create a feature branch (`git checkout -b feature/entropy-viz`).
3. Commit changes (`git commit -m "Add entropy gauge chart"`).
4. Push & PR.

Issues? Open a ticket. Discussions welcome on X: [@BitcoinDegrowth](https://x.com/BitcoinDegrowth).

## 📄 License
MIT License – Free to fork, extend, and HODL. See [LICENSE](LICENSE).

## 🙏 Acknowledgments
- Built with ❤️ by Pascal Ranaora.
- Thanks to EXIOBASE team, Chainalysis researchers, and the Bitcoin degrowth community.
- Powered by open-source: Streamlit, NumPy, Pandas.

**Bitcoin: Shrinking the entropy beast, one satoshi at a time.** Questions? DM on X or open an issue.
