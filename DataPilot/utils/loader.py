"""Data loading and validation utilities for DataPilot.

This module is responsible for reading uploaded CSV/Excel files into
pandas DataFrames and validating that the resulting data is usable.
It intentionally contains no Streamlit calls beyond type references,
so it can be reused or unit tested independently of the UI layer.
"""
from __future__ import annotations

from typing import Optional, Tuple

import pandas as pd
from pandas.errors import EmptyDataError, ParserError

from utils.config import SUPPORTED_EXTENSIONS


def get_file_extension(filename: str) -> str:
    """Return the lowercase file extension of a filename, without the dot."""
    return filename.rsplit(".", 1)[-1].lower() if "." in filename else ""


def load_dataset(uploaded_file) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """Load an uploaded CSV or Excel file into a pandas DataFrame.

    Args:
        uploaded_file: The file-like object returned by
            ``st.file_uploader``.

    Returns:
        A ``(dataframe, error_message)`` tuple. Exactly one element is
        ``None``: on success ``error_message`` is ``None``; on failure
        ``dataframe`` is ``None`` and ``error_message`` explains why.
    """
    if uploaded_file is None:
        return None, "No file was provided."

    extension = get_file_extension(uploaded_file.name)

    if extension not in SUPPORTED_EXTENSIONS:
        supported = ", ".join(f".{ext}" for ext in SUPPORTED_EXTENSIONS)
        return None, f"Unsupported file type '.{extension}'. Please upload one of: {supported}."

    try:
        if extension == "csv":
            dataframe = pd.read_csv(uploaded_file)
        else:
            dataframe = pd.read_excel(uploaded_file, engine="openpyxl")
    except EmptyDataError:
        return None, "The uploaded file is empty. Please upload a file that contains data."
    except ParserError:
        return None, "The uploaded file could not be parsed. It may be corrupted or malformed."
    except ValueError as exc:
        return None, f"The uploaded file could not be read: {exc}"
    except Exception as exc:  # noqa: BLE001 - surfaced to the user as a friendly message
        return None, f"An unexpected error occurred while reading the file: {exc}"

    validation_error = validate_dataframe(dataframe)
    if validation_error:
        return None, validation_error

    return dataframe, None


def validate_dataframe(dataframe: Optional[pd.DataFrame]) -> Optional[str]:
    """Validate that a loaded DataFrame is usable.

    Args:
        dataframe: The DataFrame to validate, or ``None``.

    Returns:
        An error message string if the DataFrame is invalid, otherwise
        ``None``.
    """
    if dataframe is None:
        return "The file could not be loaded into a dataframe."
    if dataframe.empty:
        return "The uploaded file contains no rows of data."
    if len(dataframe.columns) == 0:
        return "The uploaded file contains no columns."
    return None
