"""
Test fixtures for USA vs China Growth Analysis.

Provides sample data for unit tests.
"""

import pandas as pd


def sample_world_bank_data() -> pd.DataFrame:
    """Create sample World Bank-style data for testing.
    
    Returns:
        DataFrame with columns: country_code, country_name, year, indicator, value
        Data covers years 2000-2002 for USA and China with key indicators.
    """
    data = [
        # USA GDP per capita
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "gdp_per_capita", "value": 36418.0},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "gdp_per_capita", "value": 36703.0},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "gdp_per_capita", "value": 37381.0},
        
        # China GDP per capita
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "gdp_per_capita", "value": 959.0},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "gdp_per_capita", "value": 1044.0},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "gdp_per_capita", "value": 1149.0},
        
        # USA Investment
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "investment_pct_gdp", "value": 19.2},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "investment_pct_gdp", "value": 18.8},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "investment_pct_gdp", "value": 18.1},
        
        # China Investment
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "investment_pct_gdp", "value": 35.1},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "investment_pct_gdp", "value": 35.8},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "investment_pct_gdp", "value": 37.2},
        
        # USA Population
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "population", "value": 282424554.0},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "population", "value": 285082303.0},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "population", "value": 287625193.0},
        
        # China Population
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "population", "value": 1295604000.0},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "population", "value": 1306314000.0},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "population", "value": 1317045000.0},
        
        # USA R&D
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "rd_pct_gdp", "value": 2.72},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "rd_pct_gdp", "value": 2.81},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "rd_pct_gdp", "value": 2.79},
        
        # China R&D
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "rd_pct_gdp", "value": 0.84},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "rd_pct_gdp", "value": 0.88},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "rd_pct_gdp", "value": 1.07},
        
        # USA Patent applications
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "patent_applications", "value": 176043.0},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "patent_applications", "value": 166176.0},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "patent_applications", "value": 167345.0},
        
        # China Patent applications
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "patent_applications", "value": 25098.0},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "patent_applications", "value": 27537.0},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "patent_applications", "value": 32841.0},
    ]
    
    return pd.DataFrame(data)


def sample_gdp_per_capita() -> pd.DataFrame:
    """Create sample GDP per capita data.
    
    Returns:
        DataFrame with columns: country_code, country_name, year, indicator, value
    """
    data = [
        {"country_code": "USA", "country_name": "United States", "year": 2000, "indicator": "gdp_per_capita", "value": 36418.0},
        {"country_code": "USA", "country_name": "United States", "year": 2001, "indicator": "gdp_per_capita", "value": 36703.0},
        {"country_code": "USA", "country_name": "United States", "year": 2002, "indicator": "gdp_per_capita", "value": 37381.0},
        {"country_code": "CHN", "country_name": "China", "year": 2000, "indicator": "gdp_per_capita", "value": 959.0},
        {"country_code": "CHN", "country_name": "China", "year": 2001, "indicator": "gdp_per_capita", "value": 1044.0},
        {"country_code": "CHN", "country_name": "China", "year": 2002, "indicator": "gdp_per_capita", "value": 1149.0},
    ]
    return pd.DataFrame(data)
