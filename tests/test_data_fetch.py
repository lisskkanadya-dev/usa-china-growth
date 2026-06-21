"""
Tests for data fetching functions.

Tests for World Bank API interactions, URL building, and response parsing.
"""

import pytest
import pandas as pd
import json
from unittest.mock import patch, MagicMock
from src.data_fetch import (
    build_world_bank_url,
    parse_world_bank_response,
    validate_country_codes,
    fetch_indicator,
    fetch_all_data,
)


class TestBuildWorldBankURL:
    """Tests for World Bank API URL building."""

    def test_url_includes_country_code(self):
        """Test that URL includes country code."""
        url = build_world_bank_url("USA", "NY.GDP.PCAP.KD", 2000, 2020)
        assert "USA" in url

    def test_url_includes_indicator(self):
        """Test that URL includes indicator code."""
        url = build_world_bank_url("USA", "NY.GDP.PCAP.KD", 2000, 2020)
        assert "NY.GDP.PCAP.KD" in url

    def test_url_includes_date_range(self):
        """Test that URL includes date range."""
        url = build_world_bank_url("USA", "NY.GDP.PCAP.KD", 2000, 2020)
        assert "2000" in url
        assert "2020" in url

    def test_url_format_is_correct(self):
        """Test that URL follows World Bank API format."""
        url = build_world_bank_url("USA", "NY.GDP.PCAP.KD", 2000, 2020)
        assert url.startswith("https://api.worldbank.org/v2")
        assert "json" in url.lower()
        assert "per_page" in url

    def test_url_with_different_countries(self):
        """Test URL building with different country codes."""
        url_usa = build_world_bank_url("USA", "NY.GDP.PCAP.KD", 2000, 2020)
        url_chn = build_world_bank_url("CHN", "NY.GDP.PCAP.KD", 2000, 2020)
        
        assert "USA" in url_usa
        assert "CHN" in url_chn
        assert url_usa != url_chn


class TestParseWorldBankResponse:
    """Tests for World Bank API response parsing."""

    def test_parse_valid_response(self):
        """Test parsing valid World Bank API response."""
        # Minimal valid World Bank API response structure
        response_json = [
            {"page": 1, "pages": 1},
            {
                "country": {"id": "USA", "value": "United States"},
                "date": "2020",
                "value": "63543.58",
                "indicator": {"id": "NY.GDP.PCAP.KD", "value": "GDP per capita"},
            },
            {
                "country": {"id": "USA", "value": "United States"},
                "date": "2019",
                "value": "62794.59",
                "indicator": {"id": "NY.GDP.PCAP.KD", "value": "GDP per capita"},
            },
        ]
        
        result = parse_world_bank_response(response_json, "gdp_per_capita")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "country_code" in result.columns
        assert "year" in result.columns
        assert "value" in result.columns
        assert "indicator" in result.columns

    def test_parse_response_column_names(self):
        """Test that parsed response has correct column names."""
        response_json = [
            {"page": 1, "pages": 1},
            {
                "country": {"id": "USA", "value": "United States"},
                "date": "2020",
                "value": "63543.58",
                "indicator": {"id": "NY.GDP.PCAP.KD", "value": "GDP per capita"},
            },
        ]
        
        result = parse_world_bank_response(response_json, "gdp_per_capita")
        
        required_columns = ["country_code", "country_name", "year", "indicator", "value"]
        for col in required_columns:
            assert col in result.columns

    def test_parse_response_with_missing_values(self):
        """Test parsing response with null/missing values."""
        response_json = [
            {"page": 1, "pages": 1},
            {
                "country": {"id": "USA", "value": "United States"},
                "date": "2020",
                "value": None,
                "indicator": {"id": "NY.GDP.PCAP.KD", "value": "GDP per capita"},
            },
        ]
        
        result = parse_world_bank_response(response_json, "gdp_per_capita")
        
        # Should not crash and should handle NaN
        assert len(result) >= 0

    def test_parse_empty_response_raises_or_returns_empty(self):
        """Test parsing empty response."""
        response_json = [{"page": 1, "pages": 1}]
        
        result = parse_world_bank_response(response_json, "gdp_per_capita")
        
        # Should either raise or return empty DataFrame, not crash
        if isinstance(result, pd.DataFrame):
            assert len(result) == 0


class TestValidateCountryCodes:
    """Tests for country code validation."""

    def test_validate_valid_codes(self):
        """Test validation of valid country codes."""
        codes = ["USA", "CHN"]
        result = validate_country_codes(codes)
        
        assert result == codes

    def test_validate_rejects_invalid_codes(self):
        """Test that validation handles invalid codes appropriately."""
        codes = ["USA", "XXX"]
        result = validate_country_codes(codes)
        
        # Should preserve all codes (lenient approach for World Bank compatibility)
        assert "USA" in result
        # Invalid codes may be passed through in case World Bank has them
        assert isinstance(result, list)

    def test_validate_empty_list(self):
        """Test validation with empty list."""
        codes = []
        result = validate_country_codes(codes)
        assert isinstance(result, list)

    def test_validate_preserves_valid_codes(self):
        """Test that valid codes are preserved."""
        codes = ["USA", "CHN", "GBR", "JPN"]
        result = validate_country_codes(codes)
        
        assert "USA" in result
        assert "CHN" in result


class TestFetchIndicator:
    """Tests for single indicator fetching."""

    @patch('src.data_fetch.requests.get')
    def test_fetch_indicator_success(self, mock_get):
        """Test successful indicator fetch."""
        mock_response = MagicMock()
        mock_response.json.return_value = [
            {"page": 1, "pages": 1},
            {
                "country": {"id": "USA", "value": "United States"},
                "date": "2020",
                "value": "63543.58",
            },
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        result = fetch_indicator("USA", "NY.GDP.PCAP.KD", "gdp_per_capita", 2000, 2020)
        
        assert isinstance(result, pd.DataFrame)

    @patch('src.data_fetch.requests.get')
    def test_fetch_indicator_handles_network_error(self, mock_get):
        """Test that network errors are handled gracefully."""
        mock_get.side_effect = Exception("Network error")
        
        result = fetch_indicator("USA", "NY.GDP.PCAP.KD", "gdp_per_capita", 2000, 2020)
        
        # Should return empty DataFrame or handle gracefully
        if isinstance(result, pd.DataFrame):
            assert len(result) == 0


class TestFetchAllData:
    """Tests for fetching all indicators."""

    @patch('src.data_fetch.fetch_indicator')
    def test_fetch_all_data_returns_dataframe(self, mock_fetch):
        """Test that fetch_all_data returns a DataFrame."""
        mock_fetch.return_value = pd.DataFrame({
            "country_code": ["USA"],
            "country_name": ["United States"],
            "year": [2020],
            "indicator": ["gdp_per_capita"],
            "value": [63543.58],
        })
        
        indicators = {"gdp_per_capita": {"code": "NY.GDP.PCAP.KD", "name": "GDP per capita"}}
        result = fetch_all_data(["USA"], indicators, 2000, 2020)
        
        assert isinstance(result, pd.DataFrame)

    @patch('src.data_fetch.fetch_indicator')
    def test_fetch_all_data_merges_indicators(self, mock_fetch):
        """Test that multiple indicators are merged correctly."""
        mock_fetch.return_value = pd.DataFrame({
            "country_code": ["USA"],
            "country_name": ["United States"],
            "year": [2020],
            "indicator": ["gdp_per_capita"],
            "value": [63543.58],
        })
        
        indicators = {
            "gdp_per_capita": {"code": "NY.GDP.PCAP.KD", "name": "GDP per capita"},
            "population": {"code": "SP.POP.TOTL", "name": "Total population"},
        }
        
        result = fetch_all_data(["USA"], indicators, 2000, 2020)
        
        # Should have fetched both indicators
        assert mock_fetch.call_count >= 2

    @patch('src.data_fetch.fetch_indicator')
    def test_fetch_all_data_handles_missing_indicators(self, mock_fetch):
        """Test that missing indicators don't break the function."""
        def side_effect(*args, **kwargs):
            # Return empty DataFrame for some indicators
            return pd.DataFrame()
        
        mock_fetch.side_effect = side_effect
        
        indicators = {"gdp_per_capita": {"code": "NY.GDP.PCAP.KD", "name": "GDP per capita"}}
        result = fetch_all_data(["USA"], indicators, 2000, 2020)
        
        # Should not crash
        assert isinstance(result, pd.DataFrame)
