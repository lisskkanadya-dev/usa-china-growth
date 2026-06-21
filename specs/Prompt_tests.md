# Prompt for GitHub Copilot: Generate Automated Tests First

<role>
You are GitHub Copilot acting as a senior Python QA automation engineer and TDD mentor.
</role>

<context>
We are building a lightweight academic Python web/report project. The project compares economic growth factors of the United States and China using World Bank data. The final application will generate a static HTML report and will be deployed with GitHub Actions to GitHub Pages.
</context>

<academic_task>
Zadanie empiryczne: USA vs Chiny

Prepare Python code that compares growth factors of the USA and China from the perspective of the Solow model and endogenous growth theory.

The code should:
- download data for USA and China: GDP per capita, investment, population, employment, human capital, and R&D,
- compare GDP per capita dynamics,
- evaluate capital accumulation through investment and capital-per-worker proxies,
- evaluate population growth and possible dilution of capital per worker,
- evaluate technology and knowledge through R&D, patents, or productivity proxies,
- indicate which mechanisms are better explained by the Solow model and which by endogenous growth theory.

Research question:
Does growth in the USA and China result mainly from capital accumulation, demography, or technological progress? Connect the findings with the USA-China technology war discussion.
</academic_task>

<goal>
Generate automated tests before implementation. The tests should define the expected behavior of the future Python code and support a TDD workflow.
</goal>

<project_structure>
Assume the following structure:

usa-china-growth-analysis/
├── app.py
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_fetch.py
│   ├── indicators.py
│   ├── analysis.py
│   ├── charts.py
│   └── report.py
└── tests/
    ├── test_indicators.py
    ├── test_analysis.py
    ├── test_data_fetch.py
    ├── test_report.py
    └── fixtures/
        └── sample_data.py
</project_structure>

<technology_stack>
Use:
- Python 3.11+
- pytest
- pandas
- requests mocking where needed
- no real external API calls in unit tests
</technology_stack>

<testing_principles>
- Tests must be deterministic.
- Tests must not depend on live World Bank API responses.
- Use small in-memory pandas DataFrames.
- Prefer clear assertions over excessive abstraction.
- Test pure calculation functions first.
- Test missing-data behavior explicitly.
- Test that generated report contains required sections.
</testing_principles>

<functions_to_expect>
Design tests for these expected functions. If implementation names differ, adapt consistently.

In src.indicators:
- calculate_cagr(start_value: float, end_value: float, years: int) -> float
- calculate_annual_growth(df: pandas.DataFrame, value_col: str) -> pandas.DataFrame
- calculate_ratio(numerator: float, denominator: float) -> float | None
- calculate_per_million(value: float, population: float) -> float | None
- safe_pct_change(series: pandas.Series) -> pandas.Series

In src.analysis:
- summarize_gdp_growth(df: pandas.DataFrame) -> pandas.DataFrame
- calculate_china_usa_ratio(df: pandas.DataFrame) -> pandas.DataFrame
- create_data_availability_table(df: pandas.DataFrame) -> pandas.DataFrame
- build_theory_interpretation(summary: dict) -> dict

In src.data_fetch:
- build_world_bank_url(country_code: str, indicator: str, start_year: int, end_year: int) -> str
- parse_world_bank_response(response_json: list, indicator_name: str) -> pandas.DataFrame
- validate_country_codes(country_codes: list[str]) -> list[str]

In src.report:
- render_html_report(context: dict, output_path: str) -> str
</functions_to_expect>

<test_cases>
Create tests for the following cases:

1. CAGR calculation
- start=100, end=200, years=10 should return approximately 0.071773
- start value <= 0 should raise ValueError
- years <= 0 should raise ValueError

2. Annual growth calculation
- for GDP values [100, 110, 121], annual growth should be 10% and 10% after the first missing value
- growth should be calculated separately by country

3. Ratio calculation
- China GDP per capita divided by USA GDP per capita should return a valid ratio
- denominator zero or missing should return None

4. Patents per million people
- 1,000,000 patents with population 1,000,000,000 should return 1000 patents per million
- zero or missing population should return None

5. Data availability table
- should show number of available observations per country and indicator
- should not fail when an indicator is fully missing

6. GDP growth summary
- should include start year, end year, initial GDP per capita, final GDP per capita, CAGR
- should handle USA and China independently

7. China-to-USA ratio
- should return a time series containing year and ratio
- should skip years where either country is missing GDP data

8. World Bank URL builder
- should include country code, indicator, date range, JSON format, and per_page parameter

9. World Bank response parser
- should parse valid World Bank API JSON into tidy DataFrame columns: country_code, country_name, year, indicator, value
- should handle empty or malformed API response with a clear exception

10. Report rendering
- should create an HTML file
- HTML should contain title, research question, methodology, charts section, results section, theory interpretation, limitations, conclusion
- report should be generated even if optional indicators are missing

11. Theory interpretation
- high investment with fast GDP growth should produce interpretation mentioning capital accumulation
- high R&D or patent intensity should produce interpretation mentioning endogenous growth
- population growth should be interpreted cautiously as a possible capital dilution factor, not as direct proof
</test_cases>

<fixtures>
Create a small fixture dataset with years 2000, 2001, 2002 for USA and China.
Include columns:
- country_code
- country_name
- year
- indicator
- value

Indicators in fixture:
- gdp_per_capita
- investment_pct_gdp
- population
- rd_pct_gdp
- patent_applications

Make the data small but realistic enough for calculations.
</fixtures>

<output_requirements>
Generate complete pytest files with imports and executable test functions.
Do not write implementation code except minimal fixtures needed for tests.
Use plain English comments only where helpful.
</output_requirements>

<quality_bar>
The tests should be clear enough that another AI agent can implement the project by making these tests pass.
</quality_bar>
