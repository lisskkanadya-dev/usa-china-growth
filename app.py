"""
Main application orchestrator for USA vs China Growth Analysis.

Coordinates data fetching, analysis, chart generation, and report creation.
"""

import datetime
from src.config import (
    DEFAULT_COUNTRIES,
    DEFAULT_START_YEAR,
    DEFAULT_END_YEAR,
    INDICATORS,
    REPORT_OUTPUT_PATH,
)
from src.data_fetch import fetch_all_data, validate_country_codes
from src.analysis import (
    summarize_gdp_growth,
    calculate_china_usa_ratio,
    create_data_availability_table,
    build_theory_interpretation,
)
from src.charts import (
    create_gdp_chart,
    create_growth_chart,
    create_ratio_chart,
    create_indicator_chart,
)
from src.report import render_html_report


def main():
    """Main entry point for the application."""
    print("=" * 60)
    print("USA vs China Growth Analysis")
    print("=" * 60)
    
    # Configuration
    countries = DEFAULT_COUNTRIES
    start_year = DEFAULT_START_YEAR
    end_year = DEFAULT_END_YEAR or (datetime.datetime.now().year - 1)
    
    print(f"\nConfiguration:")
    print(f"  Countries: {', '.join(countries)}")
    print(f"  Period: {start_year} - {end_year}")
    print(f"  Indicators: {len(INDICATORS)}")
    
    # Validate countries
    print("\nValidating country codes...")
    countries = validate_country_codes(countries)
    print(f"  Validated: {', '.join(countries)}")
    
    # Fetch data
    print("\nFetching data from World Bank API...")
    data = fetch_all_data(countries, INDICATORS, start_year, end_year)
    
    if data.empty:
        print("ERROR: No data fetched. Please check your internet connection or API availability.")
        return
    
    print(f"  Downloaded {len(data)} data points")
    print(f"  Indicators: {', '.join(data['indicator'].unique())}")
    
    # Create data availability table
    print("\nGenerating data availability table...")
    availability = create_data_availability_table(data)
    availability_html = availability.to_html(index=False, border=0)
    print(f"  {len(availability)} indicator-country combinations")
    
    # Analysis
    print("\nPerforming analysis...")
    
    # GDP Growth Summary
    gdp_summary = summarize_gdp_growth(data)
    print("\nGDP Per Capita Summary:")
    for _, row in gdp_summary.iterrows():
        print(f"  {row['country_name']}:")
        print(f"    Start (2000): ${row['initial_gdp']:.2f}")
        print(f"    End ({int(row['end_year'])}): ${row['final_gdp']:.2f}")
        print(f"    CAGR: {row['cagr']:.2%}")
    
    # Build summary dict for interpretation
    summary_dict = {
        "investment_intensity": {},
        "gdp_growth": {},
        "rd_intensity": {},
        "population_growth": {},
    }
    
    # Populate summary dict
    for country_code in countries:
        gdp_data = data[(data["country_code"] == country_code) & (data["indicator"] == "gdp_per_capita")]
        if not gdp_data.empty:
            gdp_row = gdp_summary[gdp_summary["country_code"] == country_code]
            if not gdp_row.empty:
                summary_dict["gdp_growth"][country_code] = gdp_row.iloc[0]["cagr"]
        
        # Investment
        inv_data = data[(data["country_code"] == country_code) & (data["indicator"] == "investment_pct_gdp")]
        if not inv_data.empty:
            summary_dict["investment_intensity"][country_code] = inv_data["value"].mean()
        
        # R&D
        rd_data = data[(data["country_code"] == country_code) & (data["indicator"] == "rd_pct_gdp")]
        if not rd_data.empty:
            summary_dict["rd_intensity"][country_code] = rd_data["value"].mean()
        
        # Population growth
        pop_data = data[(data["country_code"] == country_code) & (data["indicator"] == "population")]
        if not pop_data.empty:
            pop_data_sorted = pop_data.sort_values("year")
            if len(pop_data_sorted) > 1:
                first = pop_data_sorted.iloc[0]["value"]
                last = pop_data_sorted.iloc[-1]["value"]
                years = pop_data_sorted.iloc[-1]["year"] - pop_data_sorted.iloc[0]["year"]
                if years > 0 and first > 0:
                    pop_growth = ((last / first) ** (1 / years)) - 1
                    summary_dict["population_growth"][country_code] = pop_growth
    
    # Theory interpretation
    print("\nBuilding theory interpretation...")
    interpretation = build_theory_interpretation(summary_dict)
    
    # Generate charts
    print("\nGenerating charts...")
    charts = []
    
    # GDP Chart
    try:
        gdp_chart = create_gdp_chart(data)
        charts.append({"title": "GDP per Capita Comparison", "html": gdp_chart})
        print("  ✓ GDP per capita chart")
    except Exception as e:
        print(f"  ✗ GDP chart failed: {e}")
    
    # Growth Chart
    try:
        growth_chart = create_growth_chart(data)
        charts.append({"title": "Annual Growth Rates", "html": growth_chart})
        print("  ✓ Growth rate chart")
    except Exception as e:
        print(f"  ✗ Growth chart failed: {e}")
    
    # Ratio Chart
    try:
        ratio_chart = create_ratio_chart(data)
        charts.append({"title": "China-to-USA Ratio", "html": ratio_chart})
        print("  ✓ Ratio chart")
    except Exception as e:
        print(f"  ✗ Ratio chart failed: {e}")
    
    # Investment Chart
    try:
        inv_chart = create_indicator_chart(data, "investment_pct_gdp", "Investment Intensity (% of GDP)", "% of GDP")
        charts.append({"title": "Investment Intensity", "html": inv_chart})
        print("  ✓ Investment chart")
    except Exception as e:
        print(f"  ✗ Investment chart failed: {e}")
    
    # R&D Chart
    try:
        rd_chart = create_indicator_chart(data, "rd_pct_gdp", "R&D Expenditure (% of GDP)", "% of GDP")
        charts.append({"title": "R&D Expenditure", "html": rd_chart})
        print("  ✓ R&D chart")
    except Exception as e:
        print(f"  ✗ R&D chart failed: {e}")
    
    # Patents Chart
    try:
        patent_chart = create_indicator_chart(data, "patent_applications", "Patent Applications", "Applications")
        charts.append({"title": "Patent Applications", "html": patent_chart})
        print("  ✓ Patent chart")
    except Exception as e:
        print(f"  ✗ Patent chart failed: {e}")
    
    # Build HTML context
    print("\nBuilding report context...")
    
    # GDP Summary HTML
    gdp_html = "<p>"
    for _, row in gdp_summary.iterrows():
        gdp_html += (
            f"<strong>{row['country_name']}:</strong> GDP per capita grew from ${row['initial_gdp']:.2f} "
            f"in {int(row['start_year'])} to ${row['final_gdp']:.2f} in {int(row['end_year'])}, "
            f"representing a CAGR of {row['cagr']:.2%}. "
        )
    gdp_html += "</p>"
    
    # Capital interpretation
    capital_html = f"<div class='interpretation'>{interpretation.get('capital_accumulation', 'N/A')}</div>"
    
    # Demographic interpretation
    demographic_html = f"<div class='interpretation'>{interpretation.get('demographics', 'N/A')}</div>"
    
    # Technology interpretation
    tech_html = f"<div class='interpretation'>{interpretation.get('technology_and_innovation', 'N/A')}</div>"
    
    # Theory mapping
    theory_html = (
        "<table>"
        "<tr><th>Mechanism</th><th>Solow Model</th><th>Endogenous Growth Theory</th></tr>"
        "<tr><td>Capital Accumulation</td><td>Central driver (short/medium-term)</td><td>Important but not sufficient</td></tr>"
        "<tr><td>Population Growth</td><td>Dilutes capital per worker</td><td>Expands market size and knowledge</td></tr>"
        "<tr><td>Technological Progress</td><td>Exogenous long-run driver</td><td>Result of R&D and human capital</td></tr>"
        "<tr><td>Human Capital</td><td>Indirect effects</td><td>Central growth factor</td></tr>"
        "<tr><td>R&D and Patents</td><td>Not core mechanism</td><td>Central driver of innovation</td></tr>"
        "</table>"
    )
    
    theory_summary = f"<p>{interpretation.get('theory_summary', 'N/A')}</p>"
    
    # Limitations
    limitations_html = (
        "<p>This analysis is descriptive and correlative, not causal. Key limitations:</p>"
        "<ul>"
        "<li>Data availability varies by country, year, and indicator</li>"
        "<li>Missing values are excluded; no imputation is performed</li>"
        "<li>Causal inference requires econometric modeling beyond this scope</li>"
        "<li>External shocks and policy changes are not explicitly modeled</li>"
        "<li>Proxy indicators (e.g., patents for innovation) may not capture all dimensions</li>"
        "<li>Growth determinants are multifaceted; this analysis highlights key patterns only</li>"
        "</ul>"
    )
    
    # Conclusion
    conclusion_html = (
        "<p>This analysis compares economic growth factors for the USA and China from 2000 to the most recent available year. "
        "The data suggest that both capital accumulation (consistent with Solow theory) and technological progress "
        "(consistent with endogenous growth theory) play roles in shaping growth trajectories. "
        "China's rapid growth reflects sustained high investment rates and increasing innovation, while the USA demonstrates "
        "a developed economy pattern with lower population growth and higher R&D intensity. "
        "Ongoing USA-China technological competition underscores the strategic importance of R&D and innovation for future growth. "
        "A comprehensive causal analysis would require econometric modeling with instrumental variables and other advanced techniques.</p>"
    )
    
    # Build context
    context = {
        "title": "USA vs China: Economic Growth Analysis",
        "research_question": "Does economic growth in the USA and China result mainly from capital accumulation, demographic factors, or technological progress?",
        "methodology": (
            "This project analyzes economic growth factors using data from the World Bank API. "
            "The analysis employs the Solow growth model (emphasizing capital, labor, and exogenous technology) "
            "and endogenous growth theory (emphasizing R&D, human capital, and innovation) as interpretive frameworks. "
            "Indicators include GDP per capita, investment intensity, population dynamics, employment, human capital proxies, R&D expenditure, and patent applications. "
            "Growth is measured using Compound Annual Growth Rates (CAGR). The analysis connects findings with the USA-China technological competition."
        ),
        "data_availability_table": availability_html,
        "charts": charts,
        "gdp_growth_summary": gdp_html,
        "capital_interpretation": capital_html,
        "demographic_interpretation": demographic_html,
        "technology_interpretation": tech_html,
        "theory_mapping": theory_html,
        "theory_summary": theory_summary,
        "limitations": limitations_html,
        "conclusion": conclusion_html,
    }
    
    # Render report
    print(f"\nRendering HTML report to {REPORT_OUTPUT_PATH}...")
    output_path = render_html_report(context, REPORT_OUTPUT_PATH)
    
    print(f"\n✓ Report successfully generated: {output_path}")
    print("\n" + "=" * 60)
    print("Analysis complete! Open the HTML file in your browser to view the report.")
    print("=" * 60)


if __name__ == "__main__":
    main()
