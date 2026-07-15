"""Application-wide constants for DataPilot.

Centralizing configuration values here avoids magic numbers and
hardcoded strings scattered across the UI layer.
"""
from __future__ import annotations

APP_NAME: str = "DataPilot"
APP_TAGLINE: str = "An Interactive Machine Learning Workbench"
APP_ICON: str = "🧭"

SUPPORTED_EXTENSIONS: tuple[str, ...] = ("csv", "xlsx")

# Quality-report thresholds
HIGH_CARDINALITY_RATIO: float = 0.9
CONSTANT_COLUMN_UNIQUE_COUNT: int = 1

# UI defaults
DEFAULT_PREVIEW_ROWS: int = 5
MAX_PREVIEW_ROWS: int = 100
DEFAULT_TOP_N_CATEGORIES: int = 10

# Chart palette
PRIMARY_COLOR: str = "#4C6EF5"
ACCENT_COLOR: str = "#12B886"
CHART_TEMPLATE: str = "plotly_white"
