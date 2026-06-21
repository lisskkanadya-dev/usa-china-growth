"""
Analysis module for USA vs China Growth Analysis.

Handles data analysis and economic interpretation.
"""

import pandas as pd
from src.indicators import calculate_cagr


def summarize_gdp_growth(df):
    """Summarize GDP per capita growth for each country.
    
    Args:
        df: DataFrame with gdp_per_capita data
    
    Returns:
        DataFrame with summary: start_year, end_year, initial_gdp, final_gdp, cagr
    """
    # Filter for GDP per capita data
    gdp_data = df[df["indicator"] == "gdp_per_capita"].copy()
    
    summary_records = []
    
    for country_code in gdp_data["country_code"].unique():
        country_data = gdp_data[gdp_data["country_code"] == country_code].sort_values("year")
        
        if len(country_data) < 2:
            continue
        
        country_name = country_data.iloc[0]["country_name"]
        start_year = int(country_data.iloc[0]["year"])
        end_year = int(country_data.iloc[-1]["year"])
        initial_gdp = country_data.iloc[0]["value"]
        final_gdp = country_data.iloc[-1]["value"]
        years = end_year - start_year
        
        if years > 0 and initial_gdp > 0:
            cagr = calculate_cagr(initial_gdp, final_gdp, years)
        else:
            cagr = None
        
        summary_records.append({
            "country_code": country_code,
            "country_name": country_name,
            "start_year": start_year,
            "end_year": end_year,
            "initial_gdp": initial_gdp,
            "final_gdp": final_gdp,
            "cagr": cagr,
        })
    
    return pd.DataFrame(summary_records)


def calculate_china_usa_ratio(df):
    """Calculate China-to-USA GDP per capita ratio over time.
    
    Args:
        df: DataFrame with gdp_per_capita data
    
    Returns:
        DataFrame with columns: year, ratio
    """
    gdp_data = df[df["indicator"] == "gdp_per_capita"].copy()
    
    # Pivot to get USA and China in separate columns
    pivoted = gdp_data.pivot_table(
        index="year",
        columns="country_code",
        values="value",
        aggfunc="first"
    )
    
    # Calculate ratio
    if "USA" in pivoted.columns and "CHN" in pivoted.columns:
        pivoted["ratio"] = pivoted["CHN"] / pivoted["USA"]
    else:
        pivoted["ratio"] = None
    
    # Return year and ratio
    result = pivoted[["ratio"]].reset_index()
    result.columns = ["year", "ratio"]
    result = result[result["ratio"].notna()]
    
    return result


def create_data_availability_table(df):
    """Create table showing data availability by country and indicator.
    
    Args:
        df: Merged DataFrame with all data
    
    Returns:
        DataFrame with availability summary
    """
    availability = df.groupby(["country_code", "country_name", "indicator"]).size().reset_index(name="available_observations")
    
    return availability


def build_theory_interpretation(summary: dict) -> dict:
    """Build interpretations of growth factors through economic theory lenses.
    
    Args:
        summary: Dict with analysis results
    
    Returns:
        Dict with theory interpretations
    """
    interpretation = {}
    
    # Capital Accumulation Interpretation (Solow Model)
    if "investment_intensity" in summary and "gdp_growth" in summary:
        usa_inv = summary.get("investment_intensity", {}).get("USA", 0)
        chn_inv = summary.get("investment_intensity", {}).get("CHN", 0)
        usa_growth = summary.get("gdp_growth", {}).get("USA", 0)
        chn_growth = summary.get("gdp_growth", {}).get("CHN", 0)
        
        capital_text = (
            "Akumulacja kapitału (perspektywa modelu Solowa): "
        )
        
        if chn_inv > usa_inv:
            capital_text += (
                f"Wskaźnik inwestycji w Chinach ({chn_inv:.1f}% PKB) przewyższa wskaźnik USA ({usa_inv:.1f}% PKB). "
                f"Zgodnie z modelem Solowa wyższe stopy inwestycji sprzyjają pogłębianiu kapitału i mogą utrzymywać "
                f"stosunkowo szybszy wzrost w perspektywie krótkiej i średniej. Jest to zgodne z obserwowanym wyższym tempem wzrostu Chin ({chn_growth:.1%}) "
                f"w porównaniu z USA ({usa_growth:.1%}). Jednak same inwestycje nie wyjaśniają wszystkich różnic we wzroście, co wymaga analizy innych mechanizmów."
            )
        else:
            capital_text += (
                f"Mimo podobnego poziomu inwestycji (USA: {usa_inv:.1f}%, Chiny: {chn_inv:.1f}% PKB), tempo wzrostu różni się znacząco. "
                f"Sugeruje to, że akumulacja kapitału, choć ważna, nie jest jedynym czynnikiem wyjaśniającym różnice we wzroście w tym okresie."
            )
        
        interpretation["capital_accumulation"] = capital_text
    
    # R&D and Endogenous Growth Interpretation
    if "rd_intensity" in summary:
        usa_rd = summary.get("rd_intensity", {}).get("USA", 0)
        chn_rd = summary.get("rd_intensity", {}).get("CHN", 0)
        
        rd_text = (
            "Technologia i wzrost endogeniczny (perspektywa teorii wzrostu endogenicznego): "
        )
        
        if usa_rd > chn_rd:
            rd_text += (
                f"USA odnotowuje wyższą intensywność B+R ({usa_rd:.2f}% PKB) w porównaniu do Chin ({chn_rd:.2f}% PKB). "
                f"Taki wzorzec jest zgodny z teorią wzrostu endogenicznego, która podkreśla rolę B+R, innowacji i tworzenia wiedzy w długoterminowym wzroście. "
                f"Gospodarka USA koncentruje się na postępie technologicznym i kapitale ludzkim. Niższy udział B+R w Chinach może odzwierciedlać etap nadrabiania zaległości, "
                f"choć obserwuje się szybki wzrost wydatków na B+R w ostatnich latach."
            )
        elif chn_rd > usa_rd:
            rd_text += (
                f"Intensywność B+R w Chinach ({chn_rd:.2f}% PKB) wzrosła i obecnie dorównuje lub przewyższa USA ({usa_rd:.2f}% PKB). "
                f"Trend ten sugeruje przejście od wzrostu napędzanego kapitałem do wzrostu opartego na wiedzy, zgodnie z teorią endogeniczną. "
                f"Rosnące inwestycje w B+R wskazują na rosnące znaczenie innowacji i tworzenia wiedzy."
            )
        else:
            rd_text += (
                f"Obie gospodarki utrzymują podobną intensywność B+R na poziomie {usa_rd:.2f}% PKB, co może sugerować konwergencję strategii innowacyjnych."
            )
        
        interpretation["technology_and_innovation"] = rd_text
    
    # Population and Demographics
    if "population_growth" in summary:
        usa_pop = summary.get("population_growth", {}).get("USA", 0)
        chn_pop = summary.get("population_growth", {}).get("CHN", 0)
        
        demo_text = (
            "Czynniki demograficzne (perspektywa modelu Solowa): "
        )
        
        if chn_pop > usa_pop:
            demo_text += (
                f"Wzrost liczby ludności w Chinach ({chn_pop:.2%}) przewyższa tempo w USA ({usa_pop:.2%}). "
                f"W ramach modelu Solowa wyższe tempo demograficzne może rozcieńczać kapitał na pracownika, co potencjalnie spowalnia wzrost PKB per capita (przy innych czynnikach niezmiennych). "
                f"Jednocześnie większa populacja w wieku produkcyjnym może powiększać rynek i zasoby ludzkie. Obserwowany wzrost PKB per capita w Chinach sugeruje, że akumulacja kapitału i wzrost produktywności przewyższyły efekt rozcieńczenia demograficznego."
            )
        else:
            demo_text += (
                f"USA utrzymują stosunkowo stabilne tempo wzrostu ludności ({usa_pop:.2%}), porównywalne lub wyższe od Chin ({chn_pop:.2%}). "
                f"Taka sytuacja demograficzna sprzyja stabilności w akumulacji kapitału."
            )
        
        interpretation["demographics"] = demo_text
    
    # Summary Theory Mapping
    interpretation["theory_summary"] = (
        "Synteza teoretyczna: Model Solowa podkreśla rolę akumulacji kapitału i zasobów czynników produkcji jako motorów wzrostu. "
        "Dane wskazują, że intensywność kapitałowa odgrywa istotną rolę, szczególnie w szybkiej fazie rozwoju Chin. "
        "Jednocześnie teoria wzrostu endogenicznego uwypukla znaczenie B+R, kapitału ludzkiego i wiedzy. "
        "Obie perspektywy dostarczają wartościowych wniosków: model Solowa tłumaczy dynamikę konwergencji i znaczenie kapitału w perspektywie krótkiej/średniej, "
        "a teoria endogeniczna wyjaśnia rolę technologii i trwałość wzrostu w długim okresie. Pełna inferencja przyczynowa wymagałaby jednak modelowania ekonometrycznego wykraczającego poza zakres tej analizy."
    )
    
    return interpretation
