# Prompt for GitHub Copilot: Generate the Python Project Implementation

<role>
You are GitHub Copilot acting as a senior Python developer and business analyst. You build clean, tested, lightweight academic web/report projects.
</role>

<context>
Implement a Python project that compares economic growth factors of the USA and China. The project will be used by economics students. It should generate a static HTML report and be deployable to GitHub Pages with GitHub Actions.
</context>

<academic_task>
Zadanie empiryczne: USA vs Chiny

Cel zadania:
Prepare Python code that compares economic growth factors of the USA and China from the perspective of the Solow model and endogenous growth theory.

The code must:
- download data for USA and China: GDP per capita, investment, population, employment, human capital, and R&D,
- compare GDP per capita growth dynamics,
- evaluate capital accumulation through investment and capital-per-worker proxies,
- evaluate population growth and whether it may dilute capital per worker,
- evaluate technology and knowledge through R&D, patents, or productivity,
- indicate which mechanisms are better explained by the Solow model and which by endogenous growth theory.

Research question:
Does growth in the USA and China result mainly from capital accumulation, demography, or technological progress? Connect the findings with the USA-China technology war discussion.
</academic_task>

<implementation_goal>
Create a working Python project that passes the tests generated for this task and produces a static HTML report at output/index.html.
</implementation_goal>

<project_structure>
Create this structure:

usa-china-growth-analysis/
├── app.py
├── requirements.txt
├── README.md
├── Opis.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_fetch.py
│   ├── indicators.py
│   ├── analysis.py
│   ├── charts.py
│   └── report.py
├── tests/
└── .github/
    └── workflows/
        ├── tests.yml
        └── pages.yml
</project_structure>

<dependencies>
Use these dependencies:
- pandas
- requests
- plotly
- jinja2
- pytest
- pytest-mock

Optional:
- numpy
- ruff
</dependencies>

<data_source>
Use the World Bank API without API keys.

Default countries:
- USA
- CHN

Default period:
- 2000 to latest available year, but allow overriding with constants or command-line arguments.

Use these indicators when available:
- GDP per capita, constant 2015 USD: NY.GDP.PCAP.KD
- Gross capital formation, % of GDP: NE.GDI.TOTL.ZS
- Population total: SP.POP.TOTL
- Employment-to-population ratio: SL.EMP.TOTL.SP.ZS
- Human capital proxy: SE.SEC.ENRR or SE.TER.ENRR or HD.HCI.OVRL
- R&D expenditure, % of GDP: GB.XPD.RSDV.GD.ZS
- Patent applications, residents: IP.PAT.RESD
</data_source>

<functional_requirements>
Implement the following behavior:

1. Download World Bank data for the selected countries and indicators.
2. Convert API responses into tidy DataFrames.
3. Clean and normalize country codes, country names, years, indicator names, and values.
4. Calculate GDP per capita annual growth and CAGR.
5. Calculate China-to-USA GDP per capita ratio by year.
6. Calculate investment intensity comparison.
7. Calculate population growth rates.
8. Calculate patent applications per million people where data exists.
9. Create a data availability table.
10. Create interactive Plotly charts.
11. Render a static HTML report.
12. Save the report as output/index.html.
13. Do not crash when optional indicators are missing.
</functional_requirements>

<required_functions>
Implement these functions so that tests can call them.

src.indicators:
```python
calculate_cagr(start_value: float, end_value: float, years: int) -> float
calculate_annual_growth(df: pandas.DataFrame, value_col: str) -> pandas.DataFrame
calculate_ratio(numerator: float, denominator: float) -> float | None
calculate_per_million(value: float, population: float) -> float | None
safe_pct_change(series: pandas.Series) -> pandas.Series
```

src.analysis:
```python
summarize_gdp_growth(df: pandas.DataFrame) -> pandas.DataFrame
calculate_china_usa_ratio(df: pandas.DataFrame) -> pandas.DataFrame
create_data_availability_table(df: pandas.DataFrame) -> pandas.DataFrame
build_theory_interpretation(summary: dict) -> dict
```

src.data_fetch:
```python
build_world_bank_url(country_code: str, indicator: str, start_year: int, end_year: int) -> str
parse_world_bank_response(response_json: list, indicator_name: str) -> pandas.DataFrame
validate_country_codes(country_codes: list[str]) -> list[str]
fetch_indicator(country_code: str, indicator_code: str, indicator_name: str, start_year: int, end_year: int) -> pandas.DataFrame
fetch_all_data(country_codes: list[str], indicators: dict[str, str], start_year: int, end_year: int) -> pandas.DataFrame
```

src.charts:
```python
create_line_chart(df, x_col, y_col, color_col, title, y_label) -> str
create_gdp_chart(df) -> str
create_growth_chart(df) -> str
create_ratio_chart(df) -> str
create_indicator_chart(df, indicator_name, title, y_label) -> str
```

src.report:
```python
render_html_report(context: dict, output_path: str) -> str
```
</required_functions>

<report_content>
The HTML report must include:

- project title,
- research question,
- methodology,
- data source,
- data availability table,
- charts,
- GDP growth comparison,
- capital accumulation interpretation,
- demographic interpretation,
- technology and knowledge interpretation,
- theory mapping: Solow vs endogenous growth,
- connection to USA-China technology competition,
- limitations,
- final conclusion.
</report_content>

<interpretation_rules>
Use cautious academic wording.

Do:
- say "the data suggest" instead of "the data prove";
- explain that indicators such as R&D and patents are proxies;
- distinguish descriptive comparison from causal inference;
- explain that a full causal answer would require econometric modeling.

Do not:
- make political claims without data;
- claim that one factor fully explains all growth;
- invent missing values;
- hide missing data.
</interpretation_rules>

<github_actions>
Create:

.github/workflows/tests.yml
- checkout code
- setup Python
- install dependencies
- run pytest

.github/workflows/pages.yml
- checkout code
- setup Python
- install dependencies
- run python app.py
- upload output directory as GitHub Pages artifact
- deploy to GitHub Pages
</github_actions>

<coding_style>
- Use simple plain English comments.
- Keep functions small and testable.
- Use type hints where practical.
- Avoid complex architecture.
- Avoid unnecessary classes.
- Handle errors with clear messages.
- Use pathlib for file paths.
</coding_style>

<deliverables>
Generate all project files needed to run the project locally and in GitHub Actions.
The command below must work:

```bash
pip install -r requirements.txt
python app.py
```

After running the command, output/index.html must exist.
</deliverables>

<quality_bar>
The generated project should be understandable for junior Python developers and useful for economics students.
</quality_bar>
