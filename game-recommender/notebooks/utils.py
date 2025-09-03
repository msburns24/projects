from __future__ import annotations
from typing import Optional
import pandas as pd
from IPython.display import display, Markdown


def print_header(text: str, underline: str='-') -> None:
    text = text.strip()
    print(text)
    print(underline * len(text))
    return


def summarize_nulls(df: pd.DataFrame, formatted: bool=False) -> pd.DataFrame:
    '''
    Summarize null values in the DataFrame, similar to calling `df.info()`.

    Parameters
    ----------
    df : DataFrame
        The data to summarize.
    formatted : bool, default: False
        Whether to apply string formatting to numbers for cleaner output.
    
    Returns
    -------
    summary : DataFrame
        The null summary for the DataFrame.
    '''
    summary = df.dtypes.to_frame(name="Dtype")
    summary["Null Count"] = df.isna().sum()
    summary["Total"] = len(df)
    summary["% Null"] = summary["Null Count"] / summary["Total"]

    if formatted:
        summary["Null Count"] = summary["Null Count"].map("{:,}".format)
        summary["Total"] = summary["Total"].map("{:,}".format)
        summary["% Null"] = summary["% Null"].map("{:.1%}".format)
    
    return summary


def display_df_info(
        df: pd.DataFrame,
        title: Optional[str]=None,
        *,
        nulls: bool=True,
        head: Optional[int]=5,
) -> None:
    '''
    Display a cleaner output of `df.info()`, better suited for notebook
    viewing.

    Parameters
    ----------
    df : pd.DataFrame
        The data to summarize.
    title : str, default: None
        The title to display above the info.
    nulls : bool, default: True
        Whether to display a null summary table.
    head : int | None, default: 5
        The number of rows to display. When `head=None`, will not display the
        DataFrame.
    '''
    if not (title or nulls or head):
        raise ValueError('Nothing to display.')

    if title:
        display(Markdown(f"### {title}"))
    if nulls:
        display(summarize_nulls(df, formatted=True))
    if head:
        display(df.head(head))
    return