"""DataPilot — Interactive Machine Learning Workbench.

Home page: introduces the project, its purpose, and current features.
Use the sidebar to navigate to the Dataset and Column Explorer pages.
"""
from __future__ import annotations

import streamlit as st

from utils.config import APP_ICON, APP_NAME, APP_TAGLINE
from utils.ui import inject_custom_css

st.set_page_config(
    page_title=f"{APP_NAME} | ML Workbench",
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()

st.title(f"{APP_ICON} {APP_NAME}")
st.markdown(f"#### {APP_TAGLINE}")
st.write(
    "DataPilot helps you **understand your data before you model it**. "
    "Upload a dataset and explore its structure, statistics, and quality "
    "through an interactive, education-first dashboard."
)

st.divider()

# --------------------------------------------------------------------------- #
# Purpose
# --------------------------------------------------------------------------- #
st.markdown("### 🎯 Purpose")
st.write(
    "Most AutoML tools optimize for speed and automation, often hiding the "
    "reasoning behind every step. DataPilot takes the opposite approach: "
    "every chart, statistic, and quality check comes with a plain-language "
    "explanation, so students, beginners, and educators can build real "
    "intuition about their data — not just look at numbers."
)

st.divider()

# --------------------------------------------------------------------------- #
# Features
# --------------------------------------------------------------------------- #
st.markdown("### ✨ Features in This Phase")

FEATURES = [
    ("📁", "Flexible Data Upload", "Upload CSV or Excel files with built-in validation and clear error messages."),
    ("📊", "Dataset Overview", "Instantly see row/column counts, memory usage, duplicates, and missing values."),
    ("🔍", "Column Explorer", "Dive into any single column with statistics and interactive charts tailored to its type."),
    ("📐", "Statistical Summary", "Full descriptive statistics for both numerical and categorical columns."),
    ("🩺", "Quality Report", "Automatic detection of duplicates, constant columns, and other data issues."),
    ("📚", "Built-In Explanations", "Every concept is explained in plain language as you explore the data."),
]

feature_cols = st.columns(3)
for idx, (icon, name, desc) in enumerate(FEATURES):
    with feature_cols[idx % 3]:
        st.markdown(
            f'<div class="dp-card"><h4>{icon} {name}</h4><p>{desc}</p></div>',
            unsafe_allow_html=True,
        )

st.divider()

# --------------------------------------------------------------------------- #
# Workflow
# --------------------------------------------------------------------------- #
st.markdown("### 🧩 Workflow")
st.caption("This phase implements the first stage of the full DataPilot pipeline.")

FLOW_STEPS = ["Upload", "Explore", "Clean*", "Engineer*", "Train*", "Evaluate*", "Report*"]
flow_cols = st.columns(len(FLOW_STEPS))
for col, step in zip(flow_cols, FLOW_STEPS):
    with col:
        st.markdown(f'<div class="dp-flow-step">{step}</div>', unsafe_allow_html=True)
st.caption("* Planned for future phases — not available yet.")

st.divider()

# --------------------------------------------------------------------------- #
# Get started + footer
# --------------------------------------------------------------------------- #
st.markdown("### 🚀 Get Started")
st.write("Open **Dataset** in the sidebar and upload a CSV or Excel file to begin exploring.")

st.markdown(
    f'<div class="dp-footer">{APP_NAME} — Phase 1: Data Explorer · Built with Streamlit · '
    "For educational use</div>",
    unsafe_allow_html=True,
)
