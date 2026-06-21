"""
Report generation module for USA vs China Growth Analysis.

Handles HTML report rendering and output.
"""

from pathlib import Path
from jinja2 import Template


HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 40px 20px;
            margin-bottom: 40px;
            border-radius: 8px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        header p {
            font-size: 1.1em;
            opacity: 0.95;
        }
        section {
            background: white;
            padding: 30px;
            margin-bottom: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h2 {
            color: #1e3c72;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #2a5298;
        }
        h3 {
            color: #2a5298;
            margin-top: 20px;
            margin-bottom: 15px;
        }
        p {
            margin-bottom: 15px;
            text-align: justify;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 0.95em;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #2a5298;
            color: white;
        }
        tr:hover {
            background-color: #f5f5f5;
        }
        .chart-container {
            margin: 30px 0;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 6px;
            border-left: 4px solid #2a5298;
        }
        .data-table {
            overflow-x: auto;
        }
        .note {
            background-color: #e8f4f8;
            padding: 15px;
            border-left: 4px solid #2a5298;
            margin: 20px 0;
            font-style: italic;
            color: #555;
        }
        footer {
            text-align: center;
            padding: 20px;
            color: #777;
            font-size: 0.9em;
            border-top: 1px solid #ddd;
            margin-top: 40px;
        }
        .interpretation {
            background-color: #f0f4f8;
            padding: 20px;
            margin: 15px 0;
            border-radius: 6px;
            border-left: 4px solid #2a5298;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>{{ title }}</h1>
            <p>{{ research_question }}</p>
        </header>

        <section>
            <h2>Methodology & Data Source</h2>
            <p>{{ methodology }}</p>
            <div class="note">
                <strong>Data Source:</strong> World Bank Open Data API
                <br><strong>Countries:</strong> United States (USA) and China (CHN)
                <br><strong>Analysis Approach:</strong> Comparative analysis using economic growth models
            </div>
        </section>

        <section>
            <h2>Data Availability</h2>
            <div class="data-table">
                {{ data_availability_table | safe }}
            </div>
        </section>

        {% for chart in charts %}
        <section>
            <h2>{{ chart.title }}</h2>
            <div class="chart-container">
                {{ chart.html | safe }}
            </div>
        </section>
        {% endfor %}

        <section>
            <h2>Results & Analysis</h2>
            
            <h3>GDP Growth Comparison</h3>
            {{ gdp_growth_summary | safe }}
            
            <h3>Capital Accumulation Analysis</h3>
            {{ capital_interpretation | safe }}
            
            <h3>Demographic Factors</h3>
            {{ demographic_interpretation | safe }}
            
            <h3>Technology & R&D</h3>
            {{ technology_interpretation | safe }}
        </section>

        <section>
            <h2>Theoretical Framework</h2>
            
            <h3>Solow Model vs. Endogenous Growth Theory</h3>
            {{ theory_mapping | safe }}
            
            <h3>Key Insights</h3>
            {{ theory_summary | safe }}
        </section>

        <section>
            <h2>Limitations</h2>
            <div class="note">
                {{ limitations | safe }}
            </div>
        </section>

        <section>
            <h2>Conclusion</h2>
            {{ conclusion | safe }}
        </section>

        <footer>
            <p>USA vs China Growth Analysis | Generated Report</p>
            <p><small>This analysis uses descriptive statistics and economic theory. Causal inferences require additional econometric modeling.</small></p>
        </footer>
    </div>
</body>
</html>
"""


def render_html_report(context: dict, output_path: str) -> str:
    """Render HTML report from context and save to file.
    
    Args:
        context: Dict with all report data and content
        output_path: Path where HTML file will be saved
    
    Returns:
        Path to generated HTML file
    """
    template = Template(HTML_TEMPLATE)
    html_content = template.render(**context)
    
    # Create output directory if it doesn't exist
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write HTML file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return output_path
