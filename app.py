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
        charts.append({"title": "Porównanie PKB per capita", "html": gdp_chart})
        print("  ✓ GDP per capita chart")
    except Exception as e:
        print(f"  ✗ GDP chart failed: {e}")
    
    # Growth Chart
    try:
        growth_chart = create_growth_chart(data)
        charts.append({"title": "Roczne tempo wzrostu", "html": growth_chart})
        print("  ✓ Growth rate chart")
    except Exception as e:
        print(f"  ✗ Growth chart failed: {e}")
    
    # Ratio Chart
    try:
        ratio_chart = create_ratio_chart(data)
        charts.append({"title": "Stosunek Chiny/USA", "html": ratio_chart})
        print("  ✓ Ratio chart")
    except Exception as e:
        print(f"  ✗ Ratio chart failed: {e}")
    
    # Investment Chart
    try:
        inv_chart = create_indicator_chart(data, "investment_pct_gdp", "Intensywność inwestycji (% PKB)", "% PKB")
        charts.append({"title": "Intensywność inwestycji", "html": inv_chart})
        print("  ✓ Investment chart")
    except Exception as e:
        print(f"  ✗ Investment chart failed: {e}")
    
    # R&D Chart
    try:
        rd_chart = create_indicator_chart(data, "rd_pct_gdp", "Wydatki na B+R (% PKB)", "% PKB")
        charts.append({"title": "Wydatki na B+R", "html": rd_chart})
        print("  ✓ R&D chart")
    except Exception as e:
        print(f"  ✗ R&D chart failed: {e}")
    
    # Patents Chart
    try:
        patent_chart = create_indicator_chart(data, "patent_applications", "Zgłoszenia patentowe", "Zgłoszenia")
        charts.append({"title": "Zgłoszenia patentowe", "html": patent_chart})
        print("  ✓ Patent chart")
    except Exception as e:
        print(f"  ✗ Patent chart failed: {e}")
    
    # Build HTML context
    print("\nBuilding report context...")
    
    # Podsumowanie PKB (HTML)
    gdp_html = "<p>"
    for _, row in gdp_summary.iterrows():
        gdp_html += (
            f"<strong>{row['country_name']}:</strong> PKB per capita wzrósł z ${row['initial_gdp']:.2f} "
            f"w {int(row['start_year'])} do ${row['final_gdp']:.2f} w {int(row['end_year'])}, "
            f"co odpowiada skumulowanej rocznej stopie wzrostu (CAGR) na poziomie {row['cagr']:.2%}. "
        )
    gdp_html += "</p>"
    
    # Capital interpretation
    capital_html = f"<div class='interpretation'>{interpretation.get('capital_accumulation', 'N/A')}</div>"
    
    # Demographic interpretation
    demographic_html = f"<div class='interpretation'>{interpretation.get('demographics', 'N/A')}</div>"
    
    # Technology interpretation
    tech_html = f"<div class='interpretation'>{interpretation.get('technology_and_innovation', 'N/A')}</div>"
    
    # Mapowanie teorii (tabela)
    theory_html = (
        "<table>"
        "<tr><th>Mechanizm</th><th>Model Solowa</th><th>Teoria wzrostu endogenicznego</th></tr>"
        "<tr><td>Akumulacja kapitału</td><td>Główny czynnik (krótkie/średnie perspektywy)</td><td>Ważny, lecz niewystarczający</td></tr>"
        "<tr><td>Wzrost demograficzny</td><td>Rozcieńcza kapitał na pracownika</td><td>Poszerza rynek i zasoby wiedzy</td></tr>"
        "<tr><td>Postęp technologiczny</td><td>Egzogeniczny czynnik długookresowy</td><td>Efekt B+R i kapitału ludzkiego</td></tr>"
        "<tr><td>Kapitał ludzki</td><td>Efekty pośrednie</td><td>Kluczowy czynnik wzrostu</td></tr>"
        "<tr><td>B+R i patenty</td><td>Nieobowiązkowy mechanizm w modelu bazowym</td><td>Główny motor innowacji</td></tr>"
        "</table>"
    )
    
    theory_summary = f"<p>{interpretation.get('theory_summary', 'N/A')}</p>"
    
    # Ograniczenia analizy
    limitations_html = (
        "<p>Ta analiza ma charakter opisowy i korelacyjny — nie jest analizą przyczynowo-skutkową. Najważniejsze ograniczenia:</p>"
        "<ul>"
        "<li>Dostępność danych różni się w zależności od kraju, roku i wskaźnika</li>"
        "<li>Wartości brakujące są pomijane; nie dokonano imputacji</li>"
        "<li>Wnioski przyczynowe wymagałyby modelowania ekonometrycznego wykraczającego poza zakres</li>"
        "<li>Wstrząsy zewnętrzne i zmiany polityki nie są tutaj modelowane</li>"
        "<li>Proksy wskaźników (np. patenty dla innowacji) mogą nie uchwycić wszystkich wymiarów</li>"
        "<li>Determinanty wzrostu są złożone; analiza uwypukla wybrane wzorce</li>"
        "</ul>"
    )
    
    # Wnioski
    conclusion_html = (
        "<p>Analiza porównuje czynniki wzrostu gospodarczego w USA i Chinach od 2000 roku do najnowszych dostępnych danych. "
        "Dane wskazują, że zarówno akumulacja kapitału (zgodna z modelem Solowa), jak i postęp technologiczny "
        "(zgodny z teorią wzrostu endogenicznego) odgrywają rolę w kształtowaniu trajektorii wzrostu. "
        "Szybki wzrost Chin odzwierciedla utrzymywanie wysokich stóp inwestycji oraz rosnące znaczenie innowacji, natomiast USA "
        "charakteryzują się wzorcem gospodarki rozwiniętej: niższym tempem przyrostu ludności i wyższą intensywnością B+R. "
        "Rywalizacja technologiczna między USA a Chinami podkreśla strategiczne znaczenie wydatków na badania i rozwój. "
        "Pełna analiza przyczynowa wymagałaby zaawansowanego modelowania ekonometrycznego.</p>"
    )
    
    # Build context
    context = {
        "title": "USA vs Chiny: Analiza wzrostu gospodarczego",
        "research_question": "Czy wzrost gospodarczy w USA i Chinach wynika głównie z akumulacji kapitału, czynników demograficznych czy postępu technologicznego?",
        "methodology": (
            "Projekt wykorzystuje dane z API Banku Światowego do analizy czynników wzrostu gospodarczego. "
            "Analiza opiera się na modelu Solowa (akcent na kapitał, pracę i egzogeniczny postęp technologiczny) "
            "oraz na teorii wzrostu endogenicznego (akcent na B+R, kapitał ludzki i innowacje) jako ramach interpretacyjnych. "
            "Wskaźniki obejmują PKB per capita, intensywność inwestycji, dynamikę populacji, zatrudnienie, miary kapitału ludzkiego, wydatki na B+R i wnioski patentowe. "
            "Wzrost mierzony jest skumulowaną roczną stopą wzrostu (CAGR)."
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
