# Technical Requirements: USA vs China Growth Factors Empirical Project

## 1. Project Overview

This project is a lightweight Python web application for academic purposes. It automatically downloads economic data for the United States and China, compares their growth patterns, and interprets the results through the Solow growth model and endogenous growth theory.

The project should be deployable with GitHub Actions and published as an externally viewable static website, preferably through GitHub Pages. The final output should be a static HTML report with charts, tables, and written conclusions.

## 2. Business Goal

The application should answer the research question:

> Does economic growth in the United States and China result mainly from capital accumulation, demographic factors, or technological progress?

The report should also connect the findings with the discussion about the USA-China technological competition and technology war.

The target audience includes economics students and lecturers. The implementation should be technically correct, reproducible, and easy to explain in academic discussion.

## 3. Project Type

- Language: Python 3.11 or newer
- Project style: lightweight static web/report project
- Main output: static HTML report
- Deployment target: GitHub Pages through GitHub Actions
- Development approach: test-driven development where practical
- AI coding assistant target: GitHub Copilot

## 4. Recommended Repository Structure

```text
usa-china-growth-analysis/
├── app.py
├── requirements.txt
├── README.md
├── Opis.md
├── data/
│   └── .gitkeep
├── output/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_fetch.py
│   ├── indicators.py
│   ├── analysis.py
│   ├── charts.py
│   └── report.py
├── tests/
│   ├── test_indicators.py
│   ├── test_analysis.py
│   ├── test_report.py
│   └── fixtures/
│       └── sample_world_bank_data.json
└── .github/
    └── workflows/
        ├── tests.yml
        └── pages.yml
```

A simpler single-file script is acceptable for academic use, but the recommended modular structure should be preferred if time allows.

## 5. Data Requirements

### 5.1 Countries

The application must compare exactly two default countries:

- United States: `USA`
- China: `CHN`

The country list should be configurable, but the default academic task is USA vs China.

### 5.2 Time Period

Default period:

- Start year: `2000`
- End year: latest available year returned by the data source, but not later than the current year minus one

The period should be configurable through constants, environment variables, or command-line arguments.

### 5.3 Core Indicators

The project must download or calculate the following indicators where available:

| Concept | Preferred World Bank Indicator | Description |
|---|---|---|
| GDP per capita | `NY.GDP.PCAP.KD` | GDP per capita, constant 2015 US dollars |
| Gross capital formation | `NE.GDI.TOTL.ZS` | Investment as percentage of GDP |
| Population | `SP.POP.TOTL` | Total population |
| Employment | `SL.EMP.TOTL.SP.ZS` or alternative | Employment-to-population ratio |
| Human capital proxy | `SE.SEC.ENRR`, `SE.TER.ENRR`, or `HD.HCI.OVRL` | Education or human capital index proxy |
| R&D expenditure | `GB.XPD.RSDV.GD.ZS` | Research and development expenditure as percentage of GDP |
| Patent applications | `IP.PAT.RESD` | Resident patent applications |

Because international data availability differs by country and year, the code must handle missing indicators gracefully.

### 5.4 Derived Indicators

The application should calculate:

- GDP per capita growth rate,
- compound annual growth rate of GDP per capita,
- population growth rate,
- investment intensity,
- approximate capital accumulation proxy,
- GDP per worker or GDP per employed person if employment data is available,
- R&D intensity,
- patent applications per million people,
- basic technology score proxy using R&D and patents where available.

The project does not need to estimate a full production function. It should remain lightweight and transparent.

## 6. Functional Requirements

### 6.1 Data Download

The application must:

- automatically download data from the World Bank API,
- support retry or clear failure messages if API calls fail,
- cache downloaded raw data locally in `data/` where practical,
- avoid requiring API keys,
- convert all data into tidy pandas DataFrames.

### 6.2 Data Cleaning

The application must:

- normalize country codes, country names, years, and indicator names,
- convert numeric values safely,
- sort data by country and year,
- remove or flag missing observations,
- keep a data availability table for transparency,
- avoid silently inventing missing values.

Interpolation is allowed only for visualization continuity and must be clearly marked. Main conclusions should be based on observed data.

### 6.3 GDP Growth Analysis

The application must:

- compare GDP per capita levels for USA and China,
- calculate annual percentage changes,
- calculate CAGR for both countries,
- show whether China is catching up with the USA in GDP per capita terms,
- calculate the China-to-USA GDP per capita ratio over time.

### 6.4 Capital Accumulation Analysis

The application must:

- compare gross capital formation as a percentage of GDP,
- evaluate whether higher investment intensity is associated with faster GDP per capita growth,
- describe capital deepening using available proxies,
- explain that the project uses proxies because direct comparable capital stock data may be unavailable in the selected source.

### 6.5 Demography and Labor Analysis

The application must:

- compare population growth patterns,
- assess whether population growth can dilute capital per worker according to the Solow model,
- use employment data where available to approximate output per worker,
- clearly state limitations if employment data is incomplete.

### 6.6 Technology and Knowledge Analysis

The application must:

- compare R&D expenditure as a percentage of GDP,
- compare patent applications or patent applications per million people,
- interpret technology indicators as proxies for innovation capacity,
- connect these indicators with endogenous growth theory,
- discuss the technology competition between USA and China in a neutral academic tone.

### 6.7 Theory Mapping

The report must include a section that maps empirical findings to theory:

| Mechanism | Solow Model | Endogenous Growth Theory |
|---|---|---|
| Capital accumulation | Central short- and medium-term driver | Important but not sufficient |
| Population growth | Can dilute capital per worker | Can increase market size and knowledge creation |
| Technological progress | Exogenous long-run driver | Internal result of R&D, human capital, and innovation |
| Human capital | Usually treated indirectly | Central growth factor |
| R&D and patents | Not core in basic Solow model | Central mechanism |

### 6.8 Report Generation

The application must generate a static HTML report in `output/index.html`.

The report must include:

- title and research question,
- methodology summary,
- data source explanation,
- data availability table,
- charts,
- key results table,
- theoretical interpretation,
- limitations,
- final conclusion in plain language.

### 6.9 Charts

The project must generate readable charts, at minimum:

1. GDP per capita over time for USA and China.
2. GDP per capita annual growth rate.
3. China-to-USA GDP per capita ratio.
4. Investment share of GDP.
5. Population growth rate.
6. R&D expenditure as percentage of GDP.
7. Patent applications per million people, if available.
8. Optional summary dashboard chart.

Charts may be generated with Plotly for interactive HTML or matplotlib for static images embedded into HTML. Plotly is preferred for a lightweight web report.

## 7. Non-Functional Requirements

### 7.1 Simplicity

The code should be simple enough for students and junior developers to understand.

### 7.2 Reproducibility

The project must run from a clean checkout with:

```bash
pip install -r requirements.txt
python app.py
```

### 7.3 Robustness

The project must handle:

- unavailable indicators,
- missing years,
- World Bank API temporary errors,
- empty datasets,
- partial data for one country,
- division by zero in derived indicators.

### 7.4 Comments and Style

- Code comments must be simple and in plain English.
- Avoid excessive comments for obvious operations.
- Use descriptive function names.
- Keep functions small and testable.
- Use type hints where practical.

### 7.5 Testing

The project must include automated tests for:

- CAGR calculation,
- annual growth calculation,
- ratio calculation,
- patent-per-million calculation,
- handling missing data,
- report generation with minimal sample data,
- stable behavior when one indicator is absent.

Testing framework:

- `pytest`

### 7.6 GitHub Actions

The repository should include two workflows:

1. `tests.yml`
   - install dependencies,
   - run pytest,
   - optionally run linting.

2. `pages.yml`
   - install dependencies,
   - run `python app.py`,
   - publish `output/` to GitHub Pages.

## 8. Suggested Dependencies

```text
pandas
requests
plotly
jinja2
pytest
pytest-mock
```

Optional:

```text
numpy
python-dateutil
ruff
```

## 9. Acceptance Criteria

The project is accepted when:

- `python app.py` creates `output/index.html`,
- the report contains USA and China data,
- at least GDP per capita, investment, population, and R&D indicators are attempted,
- missing data does not break the application,
- charts are visible in the HTML report,
- the conclusion answers the research question,
- tests pass in GitHub Actions,
- GitHub Pages can publish the generated report.

## 10. Expected Academic Conclusion Style

The conclusion should not overclaim causality. It should use careful language such as:

- "The data suggest..."
- "The results are consistent with..."
- "The indicators used here are proxies..."
- "A full causal explanation would require a deeper econometric model..."

The report should distinguish between descriptive evidence and causal inference.
