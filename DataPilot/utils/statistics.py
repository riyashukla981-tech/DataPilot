"""Statistical computation utilities for DataPilot.

All functions here are pure (no Streamlit calls) so they can be
reused or unit tested independently of the UI layer.
"""
from __future__ import annotations

from typing import Dict, List, Union

import numpy as np
import pandas as pd

Number = Union[int, float]


def get_numeric_columns(df: pd.DataFrame) -> List[str]:
    """Return the list of numeric column names in the dataframe."""
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> List[str]:
    """Return the list of non-numeric (categorical/text) column names."""
    return df.select_dtypes(exclude=[np.number]).columns.tolist()


def get_overview_metrics(df: pd.DataFrame) -> Dict[str, Number]:
    """Compute high-level dataset metrics for the overview dashboard.

    Args:
        df: The dataset to summarize.

    Returns:
        A dictionary of headline metrics (rows, columns, memory usage,
        duplicate rows, missing values, and column-type counts).
    """
    numeric_cols = get_numeric_columns(df)
    categorical_cols = get_categorical_columns(df)
    memory_bytes = df.memory_usage(deep=True).sum()

    return {
        "rows": int(df.shape[0]),
        "columns": int(df.shape[1]),
        "memory_usage_mb": round(memory_bytes / (1024 ** 2), 3),
        "duplicate_rows": int(df.duplicated().sum()),
        "missing_values": int(df.isna().sum().sum()),
        "numeric_columns": len(numeric_cols),
        "categorical_columns": len(categorical_cols),
    }


def get_column_info(df: pd.DataFrame) -> pd.DataFrame:
    """Build a summary table describing every column in the dataset.

    Args:
        df: The dataset to describe.

    Returns:
        A DataFrame with one row per column, showing data type,
        missing-value counts, and cardinality.
    """
    total_rows = len(df)
    records = []
    for column in df.columns:
        missing = int(df[column].isna().sum())
        records.append(
            {
                "Column Name": column,
                "Data Type": str(df[column].dtype),
                "Missing Values": missing,
                "Missing %": round((missing / total_rows) * 100, 2) if total_rows else 0.0,
                "Unique Values": int(df[column].nunique(dropna=True)),
                "Non-Null Count": int(df[column].count()),
            }
        )
    return pd.DataFrame.from_records(records)


def get_numerical_summary(df: pd.DataFrame, column: str) -> Dict[str, Number]:
    """Compute descriptive statistics for a single numeric column.

    Args:
        df: The dataset containing the column.
        column: Name of the numeric column to summarize.

    Returns:
        A dictionary of descriptive statistics, or an empty dictionary
        if the column has no non-missing values.
    """
    series = df[column].dropna()

    if series.empty:
        return {}

    q1, q2, q3 = series.quantile([0.25, 0.5, 0.75])
    mode_series = series.mode()

    return {
        "Mean": float(series.mean()),
        "Median": float(series.median()),
        "Mode": float(mode_series.iloc[0]) if not mode_series.empty else float("nan"),
        "Variance": float(series.var()),
        "Std Dev": float(series.std()),
        "Minimum": float(series.min()),
        "Maximum": float(series.max()),
        "Range": float(series.max() - series.min()),
        "25% (Q1)": float(q1),
        "50% (Q2)": float(q2),
        "75% (Q3)": float(q3),
        "IQR": float(q3 - q1),
        "Skewness": float(series.skew()),
        "Kurtosis": float(series.kurt()),
    }


def get_categorical_summary(df: pd.DataFrame, column: str) -> Dict[str, Union[str, int]]:
    """Compute descriptive statistics for a single categorical column.

    Args:
        df: The dataset containing the column.
        column: Name of the categorical column to summarize.

    Returns:
        A dictionary with unique-value count, most frequent value, and
        its frequency, or an empty dictionary if the column has no
        non-missing values.
    """
    series = df[column].dropna()

    if series.empty:
        return {}

    value_counts = series.value_counts()

    return {
        "Unique Values": int(series.nunique()),
        "Most Frequent Value": str(value_counts.index[0]),
        "Frequency": int(value_counts.iloc[0]),
    }


def get_value_counts(df: pd.DataFrame, column: str, top_n: int = 10) -> pd.DataFrame:
    """Return the top N most frequent values in a column as a dataframe.

    Args:
        df: The dataset containing the column.
        column: Name of the column to tabulate.
        top_n: Maximum number of distinct values to return.

    Returns:
        A two-column DataFrame of ``Value`` and ``Count``.
    """
    counts = df[column].value_counts(dropna=True).head(top_n)
    return counts.rename_axis("Value").reset_index(name="Count")
