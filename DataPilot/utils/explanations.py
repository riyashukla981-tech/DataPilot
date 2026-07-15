"""Beginner-friendly explanations of statistical and data-quality concepts.

Centralizing this content keeps the feature pages free of long
strings of educational text and makes explanations easy to reuse and
update in one place.
"""
from __future__ import annotations

from typing import Dict

EXPLANATIONS: Dict[str, str] = {
    "mean": (
        "The **mean** is the average of all values: sum them up and divide by "
        "the count. It is sensitive to extreme values (outliers)."
    ),
    "median": (
        "The **median** is the middle value when the data is sorted. It is "
        "more robust to outliers than the mean, which makes it useful for "
        "skewed data."
    ),
    "mode": (
        "The **mode** is the most frequently occurring value in the column. "
        "A dataset can have one mode, several, or none at all."
    ),
    "variance": (
        "**Variance** measures how spread out values are from the mean. A "
        "higher variance means the data points are more scattered."
    ),
    "std_dev": (
        "**Standard deviation** is the square root of variance, expressed in "
        "the same units as the data. It shows how much values typically "
        "differ from the mean."
    ),
    "range": (
        "The **range** is the difference between the maximum and minimum "
        "values — a quick sense of how far the data spreads."
    ),
    "iqr": (
        "The **Interquartile Range (IQR)** is the range between the 25th and "
        "75th percentiles. It captures the spread of the middle 50% of the "
        "data and resists the influence of outliers."
    ),
    "skewness": (
        "**Skewness** measures the asymmetry of a distribution. A value near "
        "0 means roughly symmetric data; positive skew means a long right "
        "tail; negative skew means a long left tail."
    ),
    "kurtosis": (
        "**Kurtosis** measures how heavy-tailed a distribution is compared "
        "to a normal distribution. Higher kurtosis means extreme values are "
        "more likely."
    ),
    "missing_values": (
        "**Missing values** occur when data was not recorded or is "
        "unavailable. They can bias analysis and often need to be addressed "
        "before modeling."
    ),
    "duplicate_rows": (
        "**Duplicate rows** are records that appear more than once. If not "
        "handled, they can inflate counts and skew statistics."
    ),
    "constant_columns": (
        "A **constant column** holds the same value in every row. It carries "
        "no information and is usually a candidate for removal later on."
    ),
    "high_cardinality": (
        "A **high-cardinality** column has a very large number of unique "
        "values relative to the number of rows (for example, IDs or free "
        "text), which makes it hard to summarize or visualize directly."
    ),
    "outliers": (
        "**Outliers** are data points that differ significantly from the "
        "rest. On a box plot, they appear as individual points beyond the "
        "whiskers."
    ),
    "unique_values": (
        "**Unique values** counts how many distinct values appear in a "
        "column, ignoring missing entries. Very low or very high counts can "
        "both be informative."
    ),
    "memory_usage": (
        "**Memory usage** is how much RAM the dataset occupies while loaded. "
        "It matters for performance, especially with large files."
    ),
}


def get_explanation(key: str) -> str:
    """Return the explanation text for a concept key.

    Args:
        key: Identifier of the concept, e.g. ``"skewness"``.

    Returns:
        The explanation string, or a fallback message if the key is
        not recognized.
    """
    return EXPLANATIONS.get(key, "No explanation available for this concept yet.")
