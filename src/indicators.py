"""
Indicator calculation module for USA vs China Growth Analysis.

Handles calculations of derived indicators and statistical measures.
"""

import pandas as pd
import numpy as np
import math


def calculate_cagr(start_value: float, end_value: float, years: int) -> float:
    """Calculate compound annual growth rate.
    
    Formula: CAGR = (end_value / start_value) ^ (1 / years) - 1
    
    Args:
        start_value: Initial value
        end_value: Final value
        years: Number of years
    
    Returns:
        CAGR as a decimal (e.g., 0.05 for 5%)
    
    Raises:
        ValueError: If start_value <= 0 or years <= 0
    """
    if start_value <= 0:
        raise ValueError("start_value must be positive")
    if years <= 0:
        raise ValueError("years must be positive")
    
    if end_value == start_value:
        return 0.0
    
    cagr = (end_value / start_value) ** (1 / years) - 1
    return cagr


def calculate_annual_growth(df, value_col: str):
    """Calculate annual percentage growth by country.
    
    Args:
        df: DataFrame with columns: country_code, country_name, year, indicator, value
        value_col: Name of value column to calculate growth for
    
    Returns:
        DataFrame with annual growth rates
    """
    # Ensure dataframe is sorted by country and year
    df = df.sort_values(by=["country_code", "year"]).reset_index(drop=True)
    
    # Group by country and calculate pct_change
    df = df.copy()
    df["annual_growth"] = df.groupby("country_code")[value_col].pct_change()
    
    # Return only rows with calculated growth (skip first row per country which has NaN)
    result = df[df["annual_growth"].notna()].copy()
    
    return result


def calculate_ratio(numerator: float, denominator: float):
    """Calculate safe ratio handling division by zero.
    
    Args:
        numerator: Numerator value
        denominator: Denominator value
    
    Returns:
        Ratio or None if denominator is zero/missing
    """
    if denominator is None or denominator == 0:
        return None
    
    if pd.isna(denominator):
        return None
    
    if pd.isna(numerator):
        return None
    
    try:
        return numerator / denominator
    except (ZeroDivisionError, TypeError):
        return None


def calculate_per_million(value: float, population: float):
    """Scale value per million people.
    
    Args:
        value: Raw value
        population: Total population
    
    Returns:
        Value per million or None if population is zero/missing
    """
    if population is None or population == 0:
        return None
    
    if pd.isna(population) or pd.isna(value):
        return None
    
    try:
        return (value / population) * 1_000_000
    except (ZeroDivisionError, TypeError):
        return None


def safe_pct_change(series):
    """Calculate percentage change handling NaN/missing values.
    
    Args:
        series: pandas.Series to calculate pct_change for
    
    Returns:
        pandas.Series with percentage changes
    """
    return series.pct_change()
