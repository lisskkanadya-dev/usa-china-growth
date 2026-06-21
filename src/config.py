"""
Configuration module for USA vs China Growth Analysis.

Central place for all configurable constants.
"""

# Countries to analyze
DEFAULT_COUNTRIES = ["USA", "CHN"]

# Time period for analysis
DEFAULT_START_YEAR = 2000
DEFAULT_END_YEAR = None  # Will default to current year - 1 at runtime

# World Bank indicator codes
INDICATORS = {
    "gdp_per_capita": {
        "code": "NY.GDP.PCAP.KD",
        "name": "GDP per capita (constant 2015 US$)",
        "required": True,
    },
    "investment_pct_gdp": {
        "code": "NE.GDI.TOTL.ZS",
        "name": "Gross capital formation (% of GDP)",
        "required": True,
    },
    "population": {
        "code": "SP.POP.TOTL",
        "name": "Total population",
        "required": True,
    },
    "employment_ratio": {
        "code": "SL.EMP.TOTL.SP.ZS",
        "name": "Employment to population ratio (% ages 15+)",
        "required": False,
    },
    "human_capital": {
        "code": "HD.HCI.OVRL",
        "name": "Human Capital Index",
        "required": False,
    },
    "rd_pct_gdp": {
        "code": "GB.XPD.RSDV.GD.ZS",
        "name": "Research and development expenditure (% of GDP)",
        "required": False,
    },
    "patent_applications": {
        "code": "IP.PAT.RESD",
        "name": "Patent applications (residents)",
        "required": False,
    },
}

# World Bank API base URL
WORLD_BANK_API_BASE = "https://api.worldbank.org/v2"

# Data caching
CACHE_DIR = "data"
# Output directory for generated report and assets (GitHub Pages uses /docs)
OUTPUT_DIR = "docs"

# Report settings
REPORT_OUTPUT_PATH = "docs/index.html"
