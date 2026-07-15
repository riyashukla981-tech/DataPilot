# 🧭 DataPilot — Interactive Machine Learning Workbench

**Phase 1: Data Explorer**

DataPilot is an educational Machine Learning Workbench built with Python and Streamlit. Unlike traditional AutoML tools, DataPilot is designed to help you *understand* your dataset — not just process it — by pairing every statistic and chart with a plain-language explanation.

This repository currently implements **Phase 1: the Data Explorer module**. Preprocessing, feature engineering, and model training are intentionally out of scope for this phase and will arrive in future releases.

---

## 📖 Overview

Point DataPilot at a CSV or Excel file and it will help you answer the questions every analysis should start with:

- What does this dataset actually contain?
- Are there missing values, duplicates, or other quality issues?
- What do individual columns look like — their shape, spread, and outliers?
- What do these statistics *mean*, in plain English?

The app is aimed at students, data science beginners, instructors, and anyone who wants a guided first look at a new dataset.

---

## ✨ Features

### Dataset Page
- Upload CSV or Excel (`.xlsx`) files with validation for empty, invalid, or corrupted files
- **Overview** — row/column counts, memory usage, duplicate rows, missing values, and column-type breakdown as metric cards
- **Preview** — view the head, tail, a random sample, or the entire dataset with an adjustable row count
- **Column Info** — a table of data types, missing values, missing %, and cardinality per column
- **Statistical Summary** — full descriptive statistics (mean, median, mode, variance, std dev, min/max, range, quartiles, IQR, skewness, kurtosis) for numerical columns, and unique/most-frequent/frequency for categorical columns
- **Quality Report** — automatic checks for duplicate rows, missing values, constant columns, high-cardinality columns, empty columns, and irregular column names

### Column Explorer Page
- Select any single column and get a tailored view:
  - **Numerical columns:** histogram, box plot, distribution plot, descriptive statistics, missing-value summary, and a skewness explanation
  - **Categorical columns:** count plot, pie chart, and a frequency table of top categories
- Every section includes an expandable, beginner-friendly explanation of the underlying concept

### Design
- Wide, responsive dashboard layout with a clean sidebar
- Interactive Plotly charts with titles, axis labels, and hover tooltips
- Metric cards, expanders, and a minimal color palette for a professional feel

---

## 🚀 Installation

1. **Clone or download this repository.**

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app:**
   ```bash
   streamlit run app.py
   ```

5. Open the URL shown in your terminal (typically `http://localhost:8501`).

A small sample dataset is included at `datasets/sample_employee_data.csv` if you'd like to try the app immediately.

---

## 🗂️ Project Structure

```
DataPilot/
│
├── app.py                     # Home page: project overview and navigation
│
├── pages/
│   ├── 01_Dataset.py          # Upload, overview, preview, column info, stats, quality report
│   └── 02_Column_Explorer.py  # Per-column deep dive with tailored charts
│
├── utils/
│   ├── config.py              # App-wide constants and thresholds
│   ├── loader.py               # File loading and validation
│   ├── statistics.py          # Descriptive statistics computations
│   ├── visualizations.py      # Plotly chart builders
│   ├── quality_report.py      # Data quality checks
│   ├── explanations.py        # Beginner-friendly concept explanations
│   └── ui.py                  # Shared styling and rendering helpers
│
├── assets/                    # Static assets (icons, images)
├── datasets/                  # Sample dataset(s) for quick testing
│
├── .streamlit/
│   └── config.toml            # Theme configuration
│
├── requirements.txt
└── README.md
```

The code is intentionally modular: statistical logic, chart building, quality checks, and UI rendering each live in their own module so that future phases (cleaning, feature engineering, modeling, explainability) can be added without restructuring what already exists.

---

## 🖼️ Screenshots

> _Add screenshots of the Home, Dataset, and Column Explorer pages here._

| Home | Dataset Overview | Column Explorer |
|------|-------------------|------------------|
| _placeholder_ | _placeholder_ | _placeholder_ |

---

## 🛣️ Future Roadmap

Planned for later phases of the DataPilot ML Workbench:

- **Data Cleaning** — missing value imputation, duplicate removal, type correction
- **Feature Engineering** — encoding, scaling, transformations, PCA
- **Model Training** — classification and regression model training
- **Evaluation** — metrics, cross-validation, confusion matrices
- **Explainability** — feature importance, SHAP values
- **Report Generation** — exportable analysis and model reports

---

## 📄 License

This project is provided for educational purposes. Feel free to adapt it for coursework, teaching, or personal learning.
