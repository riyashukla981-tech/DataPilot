"""Dataset page: upload, overview, preview, column info, statistics, and quality report."""
from __future__ import annotations

import pandas as pd
import streamlit as st

from utils.explanations import get_explanation
from utils.loader import load_dataset
from utils.quality_report import generate_quality_report
from utils.statistics import (
    get_categorical_columns,
    get_categorical_summary,
    get_column_info,
    get_numerical_summary,
    get_numeric_columns,
    get_overview_metrics,
)
from utils.ui import inject_custom_css, render_explanation, render_page_header, render_quality_finding
from utils.visualizations import plot_missing_values

st.set_page_config(page_title="DataPilot | Dataset", page_icon="📁", layout="wide")
inject_custom_css()
render_page_header("📁 Dataset", "Upload a dataset and explore its structure, statistics, and quality.")

# --------------------------------------------------------------------------- #
# Upload
# --------------------------------------------------------------------------- #
uploaded_file = st.file_uploader(
    "Upload a CSV or Excel (.xlsx) file",
    type=["csv", "xlsx"],
    help="Your file is processed only in this browser session and is not saved anywhere.",
)

if uploaded_file is not None:
    dataframe, error = load_dataset(uploaded_file)
    if error:
        st.error(f"❌ {error}")
    else:
        st.session_state["df"] = dataframe
        st.session_state["df_name"] = uploaded_file.name
        st.success(
            f"✅ '{uploaded_file.name}' loaded successfully — "
            f"{dataframe.shape[0]:,} rows, {dataframe.shape[1]} columns."
        )

df = st.session_state.get("df")

if df is None:
    st.info("👆 Upload a dataset above to begin exploring.")
    st.stop()

st.caption(f"Currently exploring: **{st.session_state.get('df_name', 'dataset')}**")

tab_overview, tab_preview, tab_columns, tab_stats, tab_quality = st.tabs(
    ["📊 Overview", "👁️ Preview", "🗂️ Column Info", "📐 Statistical Summary", "🩺 Quality Report"]
)

# --------------------------------------------------------------------------- #
# Overview
# --------------------------------------------------------------------------- #
with tab_overview:
    metrics = get_overview_metrics(df)

    row1 = st.columns(4)
    row1[0].metric("Rows", f"{metrics['rows']:,}")
    row1[1].metric("Columns", f"{metrics['columns']:,}")
    row1[2].metric("Memory Usage", f"{metrics['memory_usage_mb']} MB")
    row1[3].metric("Duplicate Rows", f"{metrics['duplicate_rows']:,}")

    row2 = st.columns(3)
    row2[0].metric("Missing Values", f"{metrics['missing_values']:,}")
    row2[1].metric("Numerical Columns", metrics["numeric_columns"])
    row2[2].metric("Categorical Columns", metrics["categorical_columns"])

    st.write("")
    render_explanation("missing_values", "Why do missing values matter?")
    render_explanation("memory_usage", "What is memory usage?")

    if metrics["missing_values"] > 0:
        st.plotly_chart(plot_missing_values(df), width='stretch')

# --------------------------------------------------------------------------- #
# Preview
# --------------------------------------------------------------------------- #
with tab_preview:
    view_option = st.radio(
        "Choose a view", ["Head", "Tail", "Random Sample", "Entire Dataset"], horizontal=True,
    )

    max_rows = len(df)
    if view_option != "Entire Dataset":
        n_rows = st.slider("Number of rows", min_value=1, max_value=min(100, max_rows), value=min(5, max_rows))
    else:
        n_rows = max_rows
        st.caption(f"Showing all {max_rows:,} rows.")

    if view_option == "Head":
        st.dataframe(df.head(n_rows), width='stretch')
    elif view_option == "Tail":
        st.dataframe(df.tail(n_rows), width='stretch')
    elif view_option == "Random Sample":
        st.dataframe(df.sample(n=min(n_rows, max_rows)), width='stretch')
    else:
        st.dataframe(df, width='stretch')

# --------------------------------------------------------------------------- #
# Column Info
# --------------------------------------------------------------------------- #
with tab_columns:
    st.dataframe(get_column_info(df), width='stretch', hide_index=True)
    render_explanation("unique_values", "What do 'Unique Values' tell us?")

# --------------------------------------------------------------------------- #
# Statistical Summary
# --------------------------------------------------------------------------- #
with tab_stats:
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)

    st.markdown("#### Numerical Columns")
    if numeric_cols:
        numeric_summary = {col: get_numerical_summary(df, col) for col in numeric_cols}
        summary_df = pd.DataFrame(numeric_summary)
        st.dataframe(summary_df.style.format("{:.3f}"), width='stretch')

        with st.expander("📚 Understand these statistics"):
            for key, title in [
                ("mean", "Mean"), ("median", "Median"), ("mode", "Mode"),
                ("variance", "Variance"), ("std_dev", "Standard Deviation"),
                ("range", "Range"), ("iqr", "Interquartile Range (IQR)"),
                ("skewness", "Skewness"), ("kurtosis", "Kurtosis"),
            ]:
                st.markdown(f"**{title}**")
                st.caption(get_explanation(key))
    else:
        st.info("No numerical columns found in this dataset.")

    st.markdown("#### Categorical Columns")
    if categorical_cols:
        cat_summary = {col: get_categorical_summary(df, col) for col in categorical_cols}
        st.dataframe(pd.DataFrame(cat_summary), width='stretch')
    else:
        st.info("No categorical columns found in this dataset.")

# --------------------------------------------------------------------------- #
# Quality Report
# --------------------------------------------------------------------------- #
with tab_quality:
    st.markdown("#### Dataset Health Report")
    for finding in generate_quality_report(df):
        render_quality_finding(finding.status, finding.message)

    st.write("")
    render_explanation("duplicate_rows", "Why do duplicate rows matter?")
    render_explanation("constant_columns", "What is a constant column?")
    render_explanation("high_cardinality", "What is high cardinality?")
