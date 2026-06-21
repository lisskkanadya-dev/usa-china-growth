# USA vs China Growth Analysis

This is a lightweight Python project for an academic empirical task in economic growth theory. The project compares the United States and China using indicators related to the Solow growth model and endogenous growth theory.

## Research Question

Does economic growth in the United States and China result mainly from capital accumulation, demographic factors, or technological progress?

The generated report also connects the results with the discussion about USA-China technology competition.

## What the Project Does

The application downloads data from the World Bank API and generates a static HTML report with charts, tables, and interpretation.

Default countries:

- United States (`USA`)
- China (`CHN`)

Default indicators:

- GDP per capita, constant 2015 USD
- Gross capital formation as percentage of GDP
- Population
- Employment-to-population ratio, if available
- Human capital proxy, if available
- R&D expenditure as percentage of GDP
- Patent applications by residents

## Main Analytical Sections

The report covers:

1. GDP per capita growth dynamics.
2. Capital accumulation through investment indicators.
3. Demographic trends and population growth.
4. Technology and knowledge indicators such as R&D and patents.
5. Mapping of findings to Solow and endogenous growth theory.
6. Discussion of USA-China technology competition.
7. Limitations and final conclusion.

## Installation

```bash
git clone <repository-url>
cd usa-china-growth-analysis
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run Locally

```bash
python app.py
```

The generated report will be saved to:

```text
output/index.html
```

Open this file in a browser.

## Run Tests

```bash
pytest
```

## Deployment

The project is designed to be deployed with GitHub Actions to GitHub Pages.

Expected workflow:

1. Tests are executed with `tests.yml`.
2. The report is generated with `python app.py`.
3. The `output/` directory is published to GitHub Pages.

## Data Source

The project uses the World Bank API. No API key is required.

Because some indicators may be missing for some years or countries, the project should display a data availability table and avoid hiding missing values.

## Development Notes

The code should be simple and readable:

- simple plain English comments,
- small functions,
- type hints where practical,
- no unnecessary framework,
- robust handling of missing data,
- reproducible output.

## Important Limitation

This project is descriptive. It compares indicators and explains whether the observed patterns are consistent with economic growth theories. It does not prove causality. A full causal answer would require more advanced econometric modeling.
