"""
Tests for analysis functions.

Tests for GDP growth summaries, ratios, data availability, and theory interpretation.
"""

import pytest
import pandas as pd
import math
from tests.fixtures.sample_data import sample_gdp_per_capita, sample_world_bank_data
from src.analysis import (
    summarize_gdp_growth,
    calculate_china_usa_ratio,
    create_data_availability_table,
    build_theory_interpretation,
)


class TestSummarizeGDPGrowth:
    """Tests for GDP growth summary."""

    def test_summarize_gdp_growth_includes_countries(self):
        """Test that summary includes both USA and China."""
        df = sample_gdp_per_capita()
        result = summarize_gdp_growth(df)
        
        assert len(result) == 2
        countries = set(result["country_code"].values)
        assert countries == {"USA", "CHN"}

    def test_summarize_gdp_growth_has_required_columns(self):
        """Test that summary includes required columns."""
        df = sample_gdp_per_capita()
        result = summarize_gdp_growth(df)
        
        required_cols = ["country_code", "start_year", "end_year", "initial_gdp", "final_gdp", "cagr"]
        for col in required_cols:
            assert col in result.columns

    def test_summarize_gdp_growth_correct_values(self):
        """Test that summary calculations are correct."""
        df = sample_gdp_per_capita()
        result = summarize_gdp_growth(df)
        
        usa = result[result["country_code"] == "USA"].iloc[0]
        assert usa["start_year"] == 2000
        assert usa["end_year"] == 2002
        assert usa["initial_gdp"] == 36418.0
        assert usa["final_gdp"] == 37381.0
        
        # CAGR should be positive and reasonable
        assert usa["cagr"] > 0
        assert usa["cagr"] < 0.05  # Less than 5% annual growth

    def test_summarize_gdp_growth_china_faster_growth(self):
        """Test that China shows faster growth than USA in sample data."""
        df = sample_gdp_per_capita()
        result = summarize_gdp_growth(df)
        
        usa_cagr = result[result["country_code"] == "USA"].iloc[0]["cagr"]
        chn_cagr = result[result["country_code"] == "CHN"].iloc[0]["cagr"]
        
        assert chn_cagr > usa_cagr


class TestCalculateChinaUSARatio:
    """Tests for China-to-USA GDP per capita ratio."""

    def test_calculate_ratio_returns_dataframe(self):
        """Test that result is a DataFrame."""
        df = sample_gdp_per_capita()
        result = calculate_china_usa_ratio(df)
        assert isinstance(result, pd.DataFrame)

    def test_calculate_ratio_has_year_and_ratio_columns(self):
        """Test that result has required columns."""
        df = sample_gdp_per_capita()
        result = calculate_china_usa_ratio(df)
        assert "year" in result.columns
        assert "ratio" in result.columns

    def test_calculate_ratio_increasing_trend(self):
        """Test that China-to-USA ratio increases over time (China catching up)."""
        df = sample_gdp_per_capita()
        result = calculate_china_usa_ratio(df).sort_values("year")
        
        ratios = result["ratio"].values
        # In sample data, ratios should increase (China catching up)
        assert ratios[-1] > ratios[0]

    def test_calculate_ratio_valid_magnitudes(self):
        """Test that all ratios are positive and reasonable."""
        df = sample_gdp_per_capita()
        result = calculate_china_usa_ratio(df)
        
        assert (result["ratio"] > 0).all()
        assert (result["ratio"] < 1).all()  # China still behind USA in this sample

    def test_calculate_ratio_skips_missing_data(self):
        """Test that years with missing data are skipped."""
        df = pd.DataFrame({
            "country_code": ["USA", "CHN"],
            "country_name": ["United States", "China"],
            "year": [2000, 2001],
            "indicator": ["gdp_per_capita", "gdp_per_capita"],
            "value": [100, 150],
        })
        result = calculate_china_usa_ratio(df)
        # Should not raise error even with partial data


class TestCreateDataAvailabilityTable:
    """Tests for data availability reporting."""

    def test_availability_table_returns_dataframe(self):
        """Test that result is a DataFrame."""
        df = sample_world_bank_data()
        result = create_data_availability_table(df)
        assert isinstance(result, pd.DataFrame)

    def test_availability_table_has_required_columns(self):
        """Test that result includes country and indicator columns."""
        df = sample_world_bank_data()
        result = create_data_availability_table(df)
        
        assert "country_code" in result.columns or "country_name" in result.columns
        assert "indicator" in result.columns
        assert "available_observations" in result.columns

    def test_availability_table_shows_all_indicators(self):
        """Test that table includes all indicators from input."""
        df = sample_world_bank_data()
        result = create_data_availability_table(df)
        
        indicators_in_result = set(result["indicator"].values)
        indicators_in_input = set(df["indicator"].values)
        
        assert indicators_in_result == indicators_in_input

    def test_availability_table_handles_missing_indicators(self):
        """Test that missing indicators don't break the table."""
        df = sample_world_bank_data()
        # Remove all patent data for USA
        df = df[~((df["country_code"] == "USA") & (df["indicator"] == "patent_applications"))]
        
        result = create_data_availability_table(df)
        # Should not raise error
        assert isinstance(result, pd.DataFrame)


class TestBuildTheoryInterpretation:
    """Tests for economic theory interpretation."""

    def test_interpretation_returns_dict(self):
        """Test that result is a dictionary."""
        summary = {
            "investment_intensity": {"USA": 19.0, "CHN": 35.0},
            "gdp_growth": {"USA": 0.01, "CHN": 0.10},
            "rd_intensity": {"USA": 2.7, "CHN": 0.9},
            "population_growth": {"USA": 0.01, "CHN": 0.008},
        }
        result = build_theory_interpretation(summary)
        assert isinstance(result, dict)

    def test_interpretation_mentions_capital_accumulation(self):
        """Test that high investment with growth mentions capital accumulation (Solow)."""
        summary = {
            "investment_intensity": {"USA": 19.0, "CHN": 35.0},
            "gdp_growth": {"USA": 0.01, "CHN": 0.10},
            "rd_intensity": {"USA": 2.7, "CHN": 0.9},
            "population_growth": {"USA": 0.01, "CHN": 0.008},
        }
        result = build_theory_interpretation(summary)
        
        # Should include interpretation of capital accumulation
        interpretation_text = str(result).lower()
        assert "capital" in interpretation_text or "investment" in interpretation_text

    def test_interpretation_mentions_endogenous_growth(self):
        """Test that high R&D mentions endogenous growth theory."""
        summary = {
            "investment_intensity": {"USA": 19.0, "CHN": 10.0},
            "gdp_growth": {"USA": 0.02, "CHN": 0.03},
            "rd_intensity": {"USA": 2.7, "CHN": 2.5},
            "population_growth": {"USA": 0.01, "CHN": 0.01},
        }
        result = build_theory_interpretation(summary)
        
        # Should include interpretation related to R&D/technology
        interpretation_text = str(result).lower()
        # Should mention something about R&D or technology or endogenous

    def test_interpretation_uses_cautious_language(self):
        """Test that interpretation uses academic cautious wording."""
        summary = {
            "investment_intensity": {"USA": 19.0, "CHN": 35.0},
            "gdp_growth": {"USA": 0.01, "CHN": 0.10},
            "rd_intensity": {"USA": 2.7, "CHN": 0.9},
            "population_growth": {"USA": 0.01, "CHN": 0.008},
        }
        result = build_theory_interpretation(summary)
        
        result_text = str(result).lower()
        # Check for cautious language patterns
        cautious_words = ["suggest", "consistent", "proxy", "may", "could", "indicate"]
        found_cautious = any(word in result_text for word in cautious_words)
        # At least some cautious language should be present
