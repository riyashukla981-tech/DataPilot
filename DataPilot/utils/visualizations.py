"""Plotly-based visualization builders for DataPilot.

Every function returns a ``plotly.graph_objects.Figure``. None of them
call Streamlit directly, which keeps charting logic independent of
the UI layer and reusable across pages.
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.config import ACCENT_COLOR, CHART_TEMPLATE, PRIMARY_COLOR

_DEFAULT_MARGIN = dict(t=60, l=10, r=10, b=10)


def plot_histogram(df: pd.DataFrame, column: str, bins: int = 30) -> go.Figure:
    """Build a histogram for a numeric column."""
    fig = px.histogram(
        df, x=column, nbins=bins, template=CHART_TEMPLATE,
        color_discrete_sequence=[PRIMARY_COLOR],
        title=f"Histogram of {column}",
    )
    fig.update_layout(
        xaxis_title=column, yaxis_title="Frequency",
        bargap=0.05, margin=_DEFAULT_MARGIN,
    )
    return fig


def plot_box(df: pd.DataFrame, column: str) -> go.Figure:
    """Build a box plot for a numeric column, useful for spotting outliers."""
    fig = px.box(
        df, y=column, template=CHART_TEMPLATE,
        color_discrete_sequence=[PRIMARY_COLOR],
        points="outliers", title=f"Box Plot of {column}",
    )
    fig.update_layout(yaxis_title=column, margin=_DEFAULT_MARGIN)
    return fig


def _gaussian_kde(values: np.ndarray, grid: np.ndarray, bandwidth: float) -> np.ndarray:
    """Compute a Gaussian kernel density estimate using only NumPy.

    Args:
        values: Sample points to estimate the density from.
        grid: Points at which to evaluate the estimated density.
        bandwidth: Smoothing bandwidth (kernel standard deviation).

    Returns:
        The estimated density at each point in ``grid``.
    """
    diffs = (grid[:, None] - values[None, :]) / bandwidth
    kernel = np.exp(-0.5 * diffs ** 2) / np.sqrt(2 * np.pi)
    return kernel.sum(axis=1) / (len(values) * bandwidth)


def plot_distribution(df: pd.DataFrame, column: str) -> go.Figure:
    """Build a density-normalized histogram with a smoothed curve overlay.

    Raises:
        ValueError: If the column has fewer than two distinct values.
    """
    series = df[column].dropna().astype(float)
    if series.empty or series.nunique() < 2:
        raise ValueError("Not enough distinct values to plot a distribution.")

    values = series.to_numpy()
    std = values.std()
    bandwidth = 1.06 * std * (len(values) ** (-1 / 5)) if std > 0 else 1.0
    bandwidth = bandwidth if bandwidth > 0 else 1.0

    grid = np.linspace(values.min(), values.max(), 200)
    density = _gaussian_kde(values, grid, bandwidth)

    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=values, histnorm="probability density", name="Histogram",
        marker_color=PRIMARY_COLOR, opacity=0.55, nbinsx=30,
    ))
    fig.add_trace(go.Scatter(
        x=grid, y=density, mode="lines", name="Density Curve",
        line=dict(color=ACCENT_COLOR, width=2.5),
    ))
    fig.update_layout(
        template=CHART_TEMPLATE, title=f"Distribution Plot of {column}",
        xaxis_title=column, yaxis_title="Density",
        margin=_DEFAULT_MARGIN, legend=dict(orientation="h", y=1.1),
    )
    return fig


def plot_count(df: pd.DataFrame, column: str, top_n: int = 15) -> go.Figure:
    """Build a bar chart of value counts for a categorical column."""
    counts = df[column].value_counts(dropna=True).head(top_n).reset_index()
    counts.columns = [column, "Count"]
    fig = px.bar(
        counts, x=column, y="Count", template=CHART_TEMPLATE,
        color_discrete_sequence=[PRIMARY_COLOR],
        title=f"Top Categories in {column}",
    )
    fig.update_layout(margin=_DEFAULT_MARGIN)
    return fig


def plot_pie(df: pd.DataFrame, column: str, top_n: int = 10) -> go.Figure:
    """Build a pie chart of the top category proportions."""
    counts = df[column].value_counts(dropna=True).head(top_n).reset_index()
    counts.columns = [column, "Count"]
    fig = px.pie(
        counts, names=column, values="Count", template=CHART_TEMPLATE,
        title=f"Category Share of {column}", hole=0.35,
    )
    fig.update_traces(textinfo="percent+label")
    fig.update_layout(margin=_DEFAULT_MARGIN)
    return fig


def plot_missing_values(df: pd.DataFrame) -> go.Figure:
    """Build a bar chart summarizing missing values per column."""
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False).reset_index()
    missing.columns = ["Column", "Missing Count"]
    fig = px.bar(
        missing, x="Column", y="Missing Count", template=CHART_TEMPLATE,
        color_discrete_sequence=[ACCENT_COLOR], title="Missing Values by Column",
    )
    fig.update_layout(margin=_DEFAULT_MARGIN)
    return fig


def plot_scatter(df: pd.DataFrame, x_column: str, y_column: str) -> go.Figure:
    """Build a scatter plot comparing two numeric columns."""
    fig = px.scatter(
        df, x=x_column, y=y_column, template=CHART_TEMPLATE,
        color_discrete_sequence=[PRIMARY_COLOR], opacity=0.7,
        title=f"{y_column} vs {x_column}",
    )
    fig.update_layout(margin=_DEFAULT_MARGIN)
    return fig
