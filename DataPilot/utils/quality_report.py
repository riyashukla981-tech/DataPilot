"""Dataset quality checks for DataPilot.

Each check inspects one aspect of data quality and returns a
structured :class:`QualityFinding`, so the UI layer can render a
consistent health report regardless of how many checks exist.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List

import pandas as pd

from utils.config import CONSTANT_COLUMN_UNIQUE_COUNT, HIGH_CARDINALITY_RATIO


@dataclass
class QualityFinding:
    """A single quality-check result.

    Attributes:
        status: One of ``"success"``, ``"warning"``, or ``"error"``.
        message: A human-readable description of the finding.
    """

    status: str
    message: str


def check_duplicates(df: pd.DataFrame) -> QualityFinding:
    """Flag duplicate rows in the dataset."""
    count = int(df.duplicated().sum())
    if count == 0:
        return QualityFinding("success", "No duplicate rows found.")
    return QualityFinding("warning", f"{count} duplicate row(s) found.")


def check_missing_values(df: pd.DataFrame) -> QualityFinding:
    """Flag missing values anywhere in the dataset."""
    total_missing = int(df.isna().sum().sum())
    if total_missing == 0:
        return QualityFinding("success", "No missing values detected.")
    affected_columns = df.columns[df.isna().any()].tolist()
    return QualityFinding(
        "warning",
        f"{total_missing} missing value(s) found across {len(affected_columns)} column(s).",
    )


def check_constant_columns(df: pd.DataFrame) -> QualityFinding:
    """Flag columns that contain a single unique value everywhere."""
    constant_cols = [
        col for col in df.columns
        if df[col].nunique(dropna=True) <= CONSTANT_COLUMN_UNIQUE_COUNT
    ]
    if not constant_cols:
        return QualityFinding("success", "No constant columns found.")
    return QualityFinding("warning", f"Constant column(s) detected: {', '.join(constant_cols)}.")


def check_high_cardinality(df: pd.DataFrame) -> QualityFinding:
    """Flag categorical columns whose unique-value ratio is very high."""
    total_rows = len(df)
    if total_rows == 0:
        return QualityFinding("success", "No high-cardinality columns found.")

    flagged = [
        col for col in df.select_dtypes(exclude="number").columns
        if df[col].nunique(dropna=True) > 1
        and (df[col].nunique(dropna=True) / total_rows) >= HIGH_CARDINALITY_RATIO
    ]
    if not flagged:
        return QualityFinding("success", "No high-cardinality columns found.")
    return QualityFinding("warning", f"High-cardinality column(s) detected: {', '.join(flagged)}.")


def check_empty_columns(df: pd.DataFrame) -> QualityFinding:
    """Flag columns that are entirely missing."""
    empty_cols = [col for col in df.columns if df[col].isna().all()]
    if not empty_cols:
        return QualityFinding("success", "No completely empty columns found.")
    return QualityFinding("error", f"Empty column(s) detected: {', '.join(empty_cols)}.")


def check_column_names(df: pd.DataFrame) -> QualityFinding:
    """Flag blank, auto-generated, irregular, or duplicated column names."""
    issues: List[str] = []
    seen: set[str] = set()

    for col in df.columns:
        name = str(col)
        if name.strip() == "" or name.lower().startswith("unnamed"):
            issues.append(f"'{name}' looks auto-generated or blank")
        elif name != name.strip() or re.search(r"\s{2,}", name):
            issues.append(f"'{name}' has irregular spacing")
        if name in seen:
            issues.append(f"'{name}' is duplicated")
        seen.add(name)

    if not issues:
        return QualityFinding("success", "Column names look valid.")
    return QualityFinding("warning", "; ".join(issues))


def generate_quality_report(df: pd.DataFrame) -> List[QualityFinding]:
    """Run every quality check and return the full list of findings.

    Args:
        df: The dataset to evaluate.

    Returns:
        A list of :class:`QualityFinding` objects, one per check.
    """
    return [
        check_duplicates(df),
        check_missing_values(df),
        check_constant_columns(df),
        check_high_cardinality(df),
        check_empty_columns(df),
        check_column_names(df),
    ]
