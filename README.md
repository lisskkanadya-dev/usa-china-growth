# USA-China Growth Analysis

A Python project that downloads World Bank data for the United States and China, compares growth-related indicators, and generates a static HTML report suitable for GitHub Pages.

## Features

- Fetches World Bank indicators for USA and China
- Computes growth statistics and Solow/endogenous growth interpretations
- Generates interactive charts and a static HTML report in `output/index.html`
- Includes a full Python test suite with `pytest`
- Ready for GitHub Pages deployment via `.github/workflows/pages.yml`

## Requirements

- Python 3.11+
- `pip` installed

## Setup

1. Create a virtual environment:

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```powershell
   python -m pip install -r requirements.txt
   ```

## Usage

Run the application to fetch data, analyze growth, and generate the report:

```powershell
python app.py
```

The report will be written to `output/index.html`.

## Testing

Run the test suite with:

```powershell
python -m pytest -q
```

## Output

- `output/index.html`: static report
- `output/charts/`: generated chart HTML fragments

## Project Structure

- `app.py`: main application entry point
- `src/`: Python modules for config, data fetching, analysis, charts, and report generation
- `tests/`: unit tests for core functionality
- `output/`: generated report and chart assets

## Notes

- The project uses the World Bank API for indicator data.
- If the World Bank API is unavailable, tests still validate internal parsing and analysis logic.
- The repository includes GitHub Actions workflows for test execution and GitHub Pages deployment.
