"""Column Explorer page: deep-dive into a single column's statistics and charts."""
from __future__ import annotations

import streamlit as st

from utils.statistics import (
    get_categorical_summary,
    get_numeric_columns,
    get_numerical_summary,
    get_value_counts,
)
from utils.ui import inject_custom_css, render_explanation, render_page_header
from utils.visualizations import (
    plot_box,
    plot_count,
    plot_distribution,
    plot_histogram,
    plot_pie,
    plot_scatter,
)

st.set_page_config(page_title="DataPilot | Column Explorer", page_icon="🔍", layout="wide")
inject_custom_css()
render_page_header("🔍 Column Explorer", "Select a single column to inspect its distribution and quality.")

df = st.session_state.get("df")

if df is None:
    st.info("👆 No dataset loaded yet. Go to the **Dataset** page and upload a file first.")
    st.stop()

numeric_cols = get_numeric_columns(df)
column = st.selectbox("Choose a column to explore", options=df.columns.tolist())
is_numeric = column in numeric_cols

total_rows = len(df)
missing_count = int(df[column].isna().sum())
missing_pct = round((missing_count / total_rows) * 100, 2) if total_rows else 0.0

st.markdown(f"### {'🔢' if is_numeric else '🔤'} `{column}`")
meta_cols = st.columns(3)
meta_cols[0].metric("Data Type", str(df[column].dtype))
meta_cols[1].metric("Missing Values", f"{missing_count} ({missing_pct}%)")
meta_cols[2].metric("Unique Values", int(df[column].nunique(dropna=True)))

st.divider()

# --------------------------------------------------------------------------- #
# Numeric column view
# --------------------------------------------------------------------------- #
if is_numeric:
    stats = get_numerical_summary(df, column)

    if not stats:
        st.warning("This column has no non-missing values to analyze.")
        st.stop()

    stat_cols = st.columns(4)
    for idx, (label, value) in enumerate(stats.items()):
        stat_cols[idx % 4].metric(label, f"{value:.3f}")

    st.divider()

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(plot_histogram(df, column), width='stretch')
    with chart_col2:
        st.plotly_chart(plot_box(df, column), width='stretch')

    try:
        st.plotly_chart(plot_distribution(df, column), width='stretch')
    except ValueError:
        st.caption("Distribution plot unavailable: not enough distinct values in this column.")

    st.info(
        "📦 **Reading the box plot:** points shown beyond the whiskers are potential "
        "outliers — values unusually far from the rest of the data."
    )

    skew_value = stats.get("Skewness", 0.0)
    if abs(skew_value) < 0.5:
        skew_note = "this column is roughly **symmetric**."
    elif skew_value > 0:
        skew_note = "this column is **right-skewed** (a long tail toward higher values)."
    else:
        skew_note = "this column is **left-skewed** (a long tail toward lower values)."
    st.caption(f"Skewness = {skew_value:.3f} — {skew_note}")

    render_explanation("skewness", "What is skewness?")
    render_explanation("kurtosis", "What is kurtosis?")
    render_explanation("outliers", "What counts as an outlier?")

    other_numeric = [c for c in numeric_cols if c != column]
    if other_numeric:
        with st.expander("🔗 Compare with another numeric column (scatter plot)"):
            compare_col = st.selectbox("Compare against", options=other_numeric, key="scatter_compare")
            st.plotly_chart(plot_scatter(df, column, compare_col), width='stretch')

# --------------------------------------------------------------------------- #
# Categorical column view
# --------------------------------------------------------------------------- #
else:
    summary = get_categorical_summary(df, column)

    if not summary:
        st.warning("This column has no non-missing values to analyze.")
        st.stop()

    stat_cols = st.columns(3)
    stat_cols[0].metric("Unique Values", summary["Unique Values"])
    stat_cols[1].metric("Most Frequent Value", str(summary["Most Frequent Value"]))
    stat_cols[2].metric("Frequency", summary["Frequency"])

    st.divider()

    chart_col1, chart_col2 = st.columns(2)
    with chart_col1:
        st.plotly_chart(plot_count(df, column), width='stretch')
    with chart_col2:
        st.plotly_chart(plot_pie(df, column), width='stretch')

    st.markdown("#### Frequency Table — Top Categories")
    st.dataframe(get_value_counts(df, column, top_n=20), width='stretch', hide_index=True)

st.divider()
render_explanation("missing_values", "Why do missing values matter?")
