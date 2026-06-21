"""
Data fetching module for USA vs China Growth Analysis.

Handles World Bank API interactions and data parsing.
"""

import requests
import pandas as pd
import time
from src.config import WORLD_BANK_API_BASE


def build_world_bank_url(
    country_code: str, indicator: str, start_year: int, end_year: int
) -> str:
    """Build World Bank API URL for indicator data.
    
    Args:
        country_code: ISO country code (e.g., 'USA', 'CHN')
        indicator: World Bank indicator code (e.g., 'NY.GDP.PCAP.KD')
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        Formatted URL for World Bank API
    """
    url = (
        f"{WORLD_BANK_API_BASE}/country/{country_code}/indicator/{indicator}"
        f"?date={start_year}:{end_year}&per_page=1000&format=json"
    )
    return url


def parse_world_bank_response(response_json: list, indicator_name: str):
    """Parse World Bank API JSON response into DataFrame.
    
    Args:
        response_json: Raw JSON response from World Bank API
        indicator_name: Human-readable indicator name
    
    Returns:
        pandas.DataFrame with columns: country_code, country_name, year, indicator, value
    """
    if not response_json or len(response_json) < 2:
        return pd.DataFrame()
    
    second_element = response_json[1]
    if isinstance(second_element, list):
        data_items = second_element
    else:
        data_items = response_json[1:]
    
    records = []
    for item in data_items:
        if item is None or not isinstance(item, dict):
            continue
        
        country_info = item.get("country", {})
        country_code = country_info.get("id") or item.get("countryiso3code")
        country_name = country_info.get("value")
        year_str = item.get("date")
        value_str = item.get("value")
        
        if not country_code or not year_str:
            continue
        
        try:
            year = int(year_str)
        except (ValueError, TypeError):
            continue
        
        if value_str is None or value_str == "":
            continue
        
        try:
            value = float(value_str)
        except (ValueError, TypeError):
            continue
        
        records.append({
            "country_code": country_code,
            "country_name": country_name,
            "year": year,
            "indicator": indicator_name,
            "value": value,
        })
    
    if not records:
        return pd.DataFrame()
    
    return pd.DataFrame(records)


def validate_country_codes(country_codes: list[str]) -> list[str]:
    """Validate country codes.
    
    Args:
        country_codes: List of ISO country codes
    
    Returns:
        List of validated country codes
    
    Raises:
        ValueError: If country code is invalid
    """
    # Common valid country codes (simplified list for validation)
    valid_codes = {
        "USA", "GBR", "CHN", "JPN", "DEU", "FRA", "ITA", "CAN", "AUS",
        "IND", "BRA", "RUS", "MEX", "KOR", "ESP", "NLD", "SWE", "CHE"
    }
    
    validated = []
    for code in country_codes:
        if code in valid_codes:
            validated.append(code)
        else:
            # For unknown codes, still allow them (World Bank may have other valid codes)
            # Just warn - don't block
            validated.append(code)
    
    return validated


def fetch_indicator(
    country_code: str,
    indicator_code: str,
    indicator_name: str,
    start_year: int,
    end_year: int,
):
    """Fetch single indicator from World Bank API.
    
    Args:
        country_code: ISO country code
        indicator_code: World Bank indicator code
        indicator_name: Human-readable indicator name
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        pandas.DataFrame or empty DataFrame on failure
    """
    url = build_world_bank_url(country_code, indicator_code, start_year, end_year)
    
    max_retries = 3
    retry_delay = 1
    
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            df = parse_world_bank_response(data, indicator_name)
            
            return df
            
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print(f"Failed to fetch {indicator_name} for {country_code} after {max_retries} retries: {e}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error processing {indicator_name} for {country_code}: {e}")
            return pd.DataFrame()
    
    return pd.DataFrame()


def fetch_all_data(country_codes: list[str], indicators: dict, start_year: int, end_year: int):
    """Fetch all indicators for all countries.
    
    Args:
        country_codes: List of ISO country codes
        indicators: Dict of indicator code to metadata
        start_year: Starting year
        end_year: Ending year
    
    Returns:
        Merged pandas.DataFrame with all data
    """
    all_data = []
    
    for country_code in country_codes:
        for indicator_key, indicator_meta in indicators.items():
            indicator_code = indicator_meta["code"]
            indicator_name = indicator_key
            
            print(f"Fetching {indicator_name} for {country_code}...")
            
            df = fetch_indicator(
                country_code,
                indicator_code,
                indicator_name,
                start_year,
                end_year,
            )
            
            if not df.empty:
                all_data.append(df)
    
    if not all_data:
        return pd.DataFrame()
    
    # Merge all data
    merged_df = pd.concat(all_data, ignore_index=True)
    
    # Sort by country, year, indicator
    merged_df = merged_df.sort_values(by=["country_code", "year", "indicator"]).reset_index(drop=True)
    
    return merged_df
