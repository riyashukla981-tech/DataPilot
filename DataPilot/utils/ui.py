"""Shared Streamlit UI helpers for DataPilot.

Keeping styling and small rendering helpers here avoids repeating
markup logic across the home page and the feature pages.
"""
from __future__ import annotations

import streamlit as st

from utils.explanations import get_explanation

_STATUS_ICONS = {"success": "✔", "warning": "⚠", "error": "✖"}

_CUSTOM_CSS = """
<style>
    .block-container {padding-top: 2rem; padding-bottom: 3rem;}
    h1, h2, h3 {font-weight: 700; letter-spacing: -0.02em;}
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 12px;
        padding: 1rem 1.1rem;
        box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04);
    }
    div[data-testid="stMetricLabel"] {font-weight: 500; color: #495057;}
    .dp-card {
        background-color: #FFFFFF;
        border: 1px solid #E9ECEF;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        box-shadow: 0 1px 3px rgba(16, 24, 40, 0.05);
        margin-bottom: 1rem;
        height: 100%;
    }
    .dp-card h4 {margin-top: 0;}
    .dp-flow-step {
        background-color: #F1F3FF;
        border: 1px solid #DBE0FF;
        border-radius: 10px;
        padding: 0.9rem 0.6rem;
        text-align: center;
        font-weight: 600;
        color: #364FC7;
    }
    .dp-footer {
        text-align: center;
        color: #868E96;
        font-size: 0.85rem;
        padding-top: 2rem;
    }
</style>
"""


def inject_custom_css() -> None:
    """Inject the shared DataPilot stylesheet into the current page."""
    st.markdown(_CUSTOM_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: str = "") -> None:
    """Render a consistent page title and optional subtitle.

    Args:
        title: The page heading, including any emoji icon.
        subtitle: An optional one-line description shown as a caption.
    """
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    st.divider()


def render_explanation(key: str, title: str = "What does this mean?") -> None:
    """Render a beginner-friendly explanation inside an expander.

    Args:
        key: The explanation identifier, matching a key in
            :data:`utils.explanations.EXPLANATIONS`.
        title: The expander's clickable label.
    """
    with st.expander(f"ℹ️ {title}"):
        st.info(get_explanation(key))


def render_quality_finding(status: str, message: str) -> None:
    """Render a single quality-report line with a status icon.

    Args:
        status: One of ``"success"``, ``"warning"``, or ``"error"``.
        message: The finding text to display.
    """
    icon = _STATUS_ICONS.get(status, "•")
    if status == "success":
        st.success(f"{icon} {message}")
    elif status == "warning":
        st.warning(f"{icon} {message}")
    else:
        st.error(f"{icon} {message}")
