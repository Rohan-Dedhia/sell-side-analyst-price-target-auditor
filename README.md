# Sell-Side Analyst Price Target Auditor

### A 24-Year Audit of Wall Street Price Targets (2001–2024)

An independent quantitative study of **734,331 analyst price targets** issued by **23 major sell-side research firms** across **771 U.S. stocks**, evaluated against realized 12-month returns.

This project investigates a simple but important question:

> **Do sell-side analysts actually forecast future stock performance accurately, and which firms consistently provide the most reliable guidance?**

Using historical IBES analyst forecasts and realized market outcomes, every forecast was graded on calibration, directional accuracy, and magnitude of error to build one of the largest publicly documented audits of analyst forecasting performance.

---
### Live Dashboard

[![Live Dashboard](https://img.shields.io/badge/Live-Dashboard-success)](https://sell-side-analyst-price-target-auditor-8w5mxdkfrxeakcecrw9vvh.streamlit.app/)

[![GitHub](https://img.shields.io/badge/GitHub-Repository-blue)](https://github.com/Rohan-Dedhia/sell-side-analyst-price-target-auditor)

---

## Executive Summary

### Key Findings

* Analysts remain directionally useful, correctly predicting stock direction **64.6% of the time**.
* However, analysts systematically overestimate future returns by an average of **33.2 percentage points**.
* Every major brokerage firm in the dataset exhibits a positive long-term bullish bias.
* Forecast calibration has improved dramatically, with average bias falling from **118.5pp in 2001** to approximately **1pp in 2024**.
* During major market dislocations, forecast quality deteriorates sharply:

  * **2007:** Directional accuracy collapsed to **32.5%**, worse than random chance.
  * **2020:** Analysts became excessively conservative just before the COVID recovery.
* Independent research firms consistently outperform many bulge-bracket institutions on forecast calibration.
* The highest-performing analyst in the dataset achieved:

  * **14.9pp Mean Absolute Error**
  * **83.6% Directional Accuracy**
  * Near-zero systematic bias

---

## Research Questions

This study was designed to answer:

1. Which firms produce the most realistic price targets?
2. Which analysts consistently outperform peers?
3. How reliable are analyst forecasts during bull and bear markets?
4. Has forecast quality improved over time?
5. Are independent research firms more accurate than investment-bank-affiliated research teams?

---

## Dataset

| Metric                | Value                  |
| --------------------- | ---------------------- |
| Forecasts Evaluated   | 734,331                |
| Raw Records Processed | 2.2M+                  |
| Stocks Covered        | 771                    |
| Brokerage Firms       | 23                     |
| Time Period           | 2001–2024              |
| Forecast Horizon      | 12 Months              |
| Market                | United States Equities |

### Sources

* IBES/Refinitiv analyst forecast database
* Yahoo Finance Historical Prices
* Custom Forecast Evaluation Engine

---

## Forecast Evaluation Framework

Each analyst forecast was converted into an implied expected return:

Implied Return = (Price Target − Current Price) ÷ Current Price

The forecast was then compared against the stock's realized return exactly 12 months later.

For every forecast, the following metrics were calculated:

### Systematic Bias

Measures whether analysts consistently overestimate or underestimate future returns.

### Mean Absolute Error (MAE)

Measures forecast magnitude accuracy regardless of direction.

### Directional Accuracy

Measures whether the analyst correctly predicted the stock's future direction.

### Calibration Score

Measures how closely expected returns aligned with realized outcomes over time.

---

## Major Findings

### Analysts Are Consistently Bullish

Across more than 700,000 forecasts, every major brokerage firm displayed positive long-term bias.

Average forecast optimism:

**+33.2 percentage points**

No firm was conservative on average.

---

### Accuracy Breaks Down During Crises

Forecast performance deteriorates precisely when investors need guidance most.

| Event                   | Directional Accuracy |
| ----------------------- | -------------------- |
| Dot-Com Bust            | 52.2%                |
| Global Financial Crisis | 32.5%                |
| COVID Shock             | 48.7%                |
| Recovery Period         | 68.2%                |

---

### Independent Research Firms Outperform

Several independent research houses consistently ranked among the most calibrated organizations:

* Wolfe Research
* Evercore ISI
* Needham & Company

These firms generally produced tighter and more realistic forecasts than many large investment banks.

---

## Interactive Dashboard

The project includes a fully interactive Streamlit dashboard featuring:

* Firm performance rankings
* 24-year forecast accuracy trends
* Market regime analysis
* Individual analyst leaderboards
* Forecast bias visualizations
* Downloadable ranking tables

Dashboard sections:

1. Overview
2. Firm Rankings
3. Time Trends
4. Analyst Leaderboards

---

## Technology Stack

| Layer           | Technology               |
| --------------- | ------------------------ |
| Data Collection | WRDS IBES, Yahoo Finance |
| Data Processing | Python, Pandas           |
| Analytics       | NumPy, SciPy             |
| Storage         | Parquet, CSV             |
| Visualization   | Plotly                   |
| Dashboard       | Streamlit                |
| Version Control | Git, GitHub              |

---

## Project Architecture

```text
sell_side_auditor/
│
├── data/
│   ├── raw/
│   ├── prices/
│   └── processed/
│
├── src/
│   ├── 01_clean.py
│   ├── 02_prices.py
│   ├── 03_accuracy.py
│   └── 04_analysis.py
│
├── outputs/
│   ├── analyst_accuracy.csv
│   ├── firm_accuracy.csv
│   ├── regime_accuracy.csv
│   └── yearly_accuracy.csv
│
├── app.py
├── requirements.txt
└── README.md
```

---

## Reproducing the Research

```bash
git clone https://github.com/yourusername/sell_side_auditor.git

cd sell_side_auditor

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py
```

Raw IBES data is not distributed due to licensing restrictions.

Researchers with WRDS access may reproduce the full pipeline by placing the PTGDET dataset in:

```text
data/raw/ptgdet.csv
```

and executing the processing scripts sequentially.

---

## Why This Project Matters

Analyst price targets influence billions of dollars of capital allocation decisions each year.

Despite their importance, very little public work evaluates analyst forecasting performance at scale across decades of market history.

This project combines large-scale financial data engineering, statistical analysis, and interactive visualization to provide an evidence-based assessment of analyst forecasting skill.

---

## Author

Rohan Dedhia

B.Tech Data Science

Built using Python, SQL, statistical analysis, and interactive dashboard development.
