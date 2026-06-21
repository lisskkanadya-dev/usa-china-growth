"""
Tests for indicator calculation functions.

Tests for CAGR, growth rates, ratios, and other derived indicators.
"""

import pytest
import pandas as pd
import math
from src.indicators import (
    calculate_cagr,
    calculate_annual_growth,
    calculate_ratio,
    calculate_per_million,
    safe_pct_change,
)


class TestCalculateCAGR:
    """Tests for CAGR calculation."""

    def test_cagr_valid_calculation(self):
        """Test CAGR calculation with valid inputs."""
        # start=100, end=200, years=10
        # CAGR = (200/100)^(1/10) - 1 ≈ 0.071773
        result = calculate_cagr(100, 200, 10)
        assert math.isclose(result, 0.071773, rel_tol=0.0001)

    def test_cagr_no_growth(self):
        """Test CAGR when start and end values are equal."""
        result = calculate_cagr(100, 100, 5)
        assert result == 0.0

    def test_cagr_negative_growth(self):
        """Test CAGR with declining values."""
        # start=100, end=50, years=5
        # (50/100)^(1/5) - 1 ≈ -0.1294
        result = calculate_cagr(100, 50, 5)
        assert result < 0
        assert math.isclose(result, -0.1294, rel_tol=0.001)

    def test_cagr_zero_start_value_raises(self):
        """Test that zero start value raises ValueError."""
        with pytest.raises(ValueError):
            calculate_cagr(0, 100, 5)

    def test_cagr_negative_start_value_raises(self):
        """Test that negative start value raises ValueError."""
        with pytest.raises(ValueError):
            calculate_cagr(-100, 200, 5)

    def test_cagr_zero_years_raises(self):
        """Test that zero years raises ValueError."""
        with pytest.raises(ValueError):
            calculate_cagr(100, 200, 0)

    def test_cagr_negative_years_raises(self):
        """Test that negative years raises ValueError."""
        with pytest.raises(ValueError):
            calculate_cagr(100, 200, -5)


class TestCalculateAnnualGrowth:
    """Tests for annual growth calculation."""

    def test_annual_growth_simple(self):
        """Test annual growth calculation with simple data."""
        df = pd.DataFrame({
            "country_code": ["USA", "USA"],
            "year": [2000, 2001],
            "value": [100, 110],
        })
        result = calculate_annual_growth(df, "value")
        assert len(result) == 1  # One growth rate for two values
        assert math.isclose(result.iloc[0]["annual_growth"], 0.10, rel_tol=0.001)

    def test_annual_growth_by_country(self):
        """Test that growth is calculated separately by country."""
        df = pd.DataFrame({
            "country_code": ["USA", "USA", "CHN", "CHN"],
            "country_name": ["United States", "United States", "China", "China"],
            "year": [2000, 2001, 2000, 2001],
            "value": [100, 110, 100, 120],
        })
        result = calculate_annual_growth(df, "value")
        assert len(result) == 2  # Two countries, one growth each
        
        usa_growth = result[result["country_code"] == "USA"].iloc[0]["annual_growth"]
        chn_growth = result[result["country_code"] == "CHN"].iloc[0]["annual_growth"]
        
        assert math.isclose(usa_growth, 0.10, rel_tol=0.001)
        assert math.isclose(chn_growth, 0.20, rel_tol=0.001)

    def test_annual_growth_with_missing_data(self):
        """Test that NaN values are handled gracefully."""
        df = pd.DataFrame({
            "country_code": ["USA", "USA", "USA"],
            "year": [2000, 2001, 2002],
            "value": [100.0, pd.NA, 110.0],
        })
        result = calculate_annual_growth(df, "value")
        # Should not raise and should handle missing values


class TestCalculateRatio:
    """Tests for ratio calculation."""

    def test_ratio_valid(self):
        """Test valid ratio calculation."""
        result = calculate_ratio(50, 100)
        assert result == 0.5

    def test_ratio_greater_than_one(self):
        """Test ratio greater than 1."""
        result = calculate_ratio(200, 100)
        assert result == 2.0

    def test_ratio_zero_denominator_returns_none(self):
        """Test that zero denominator returns None."""
        result = calculate_ratio(100, 0)
        assert result is None

    def test_ratio_none_denominator_returns_none(self):
        """Test that None denominator returns None."""
        result = calculate_ratio(100, None)
        assert result is None

    def test_ratio_nan_denominator_returns_none(self):
        """Test that NaN denominator returns None."""
        result = calculate_ratio(100, float('nan'))
        assert result is None or (isinstance(result, float) and math.isnan(result))


class TestCalculatePerMillion:
    """Tests for per-million scaling."""

    def test_per_million_scaling(self):
        """Test basic per-million scaling."""
        # 1,000,000 patents per 1,000,000,000 population = 1000 per million
        result = calculate_per_million(1000000, 1000000000)
        assert result == 1000.0

    def test_per_million_small_population(self):
        """Test per-million with small population."""
        # 100 items per 1,000,000 population = 100 per million
        result = calculate_per_million(100, 1000000)
        assert result == 100.0

    def test_per_million_zero_population_returns_none(self):
        """Test that zero population returns None."""
        result = calculate_per_million(100, 0)
        assert result is None

    def test_per_million_none_population_returns_none(self):
        """Test that None population returns None."""
        result = calculate_per_million(100, None)
        assert result is None


class TestSafePercentChange:
    """Tests for safe percentage change calculation."""

    def test_safe_pct_change_simple(self):
        """Test percentage change with simple series."""
        series = pd.Series([100, 110, 121])
        result = safe_pct_change(series)
        
        assert math.isclose(result.iloc[1], 0.10, rel_tol=0.001)
        assert math.isclose(result.iloc[2], 0.10, rel_tol=0.001)

    def test_safe_pct_change_with_nan(self):
        """Test that NaN values are handled gracefully."""
        series = pd.Series([100, pd.NA, 121])
        result = safe_pct_change(series)
        # Should not raise exception
        assert len(result) == len(series)

    def test_safe_pct_change_returns_series(self):
        """Test that result is a pandas Series."""
        series = pd.Series([100, 110, 121])
        result = safe_pct_change(series)
        assert isinstance(result, pd.Series)
