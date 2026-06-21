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
            "Capital accumulation (Solow model perspective): "
        )
        
        if chn_inv > usa_inv:
            capital_text += (
                f"China's investment intensity ({chn_inv:.1f}% of GDP) exceeds that of the USA ({usa_inv:.1f}% of GDP). "
                f"According to the Solow model, higher investment rates facilitate capital deepening and can sustain "
                f"relatively faster short- to medium-term growth. This is consistent with China's observed higher growth rate ({chn_growth:.1%}) "
                f"compared to the USA ({usa_growth:.1%}). However, the data suggest that investment alone does not fully explain "
                f"all growth differences, warranting examination of other mechanisms."
            )
        else:
            capital_text += (
                f"Despite similar investment levels (USA: {usa_inv:.1f}%, China: {chn_inv:.1f}% of GDP), "
                f"growth rates differ significantly. This suggests that capital accumulation, while important, may not be the sole driver "
                f"of growth differences in this period."
            )
        
        interpretation["capital_accumulation"] = capital_text
    
    # R&D and Endogenous Growth Interpretation
    if "rd_intensity" in summary:
        usa_rd = summary.get("rd_intensity", {}).get("USA", 0)
        chn_rd = summary.get("rd_intensity", {}).get("CHN", 0)
        
        rd_text = (
            "Technology and endogenous growth (endogenous growth theory perspective): "
        )
        
        if usa_rd > chn_rd:
            rd_text += (
                f"The USA exhibits higher R&D intensity ({usa_rd:.2f}% of GDP) relative to China ({chn_rd:.2f}% of GDP). "
                f"This pattern is consistent with endogenous growth theory, which emphasizes that R&D, innovation, and knowledge creation "
                f"drive long-term growth. The USA's research-intensive economy suggests a focus on technological progress and human capital. "
                f"China's lower R&D share may reflect a catch-up phase emphasizing capital and technology adoption over original innovation, "
                f"though this is changing rapidly in recent years."
            )
        elif chn_rd > usa_rd:
            rd_text += (
                f"China's R&D intensity ({chn_rd:.2f}% of GDP) has increased and now exceeds or closely matches the USA ({usa_rd:.2f}% of GDP). "
                f"This trend suggests a transition from capital-driven to knowledge-driven growth, consistent with endogenous growth theory. "
                f"Rising R&D investment indicates an emerging focus on technological innovation and endogenous knowledge creation."
            )
        else:
            rd_text += (
                f"Both economies maintain comparable R&D intensities at {usa_rd:.2f}% of GDP, suggesting convergence in innovation strategies."
            )
        
        interpretation["technology_and_innovation"] = rd_text
    
    # Population and Demographics
    if "population_growth" in summary:
        usa_pop = summary.get("population_growth", {}).get("USA", 0)
        chn_pop = summary.get("population_growth", {}).get("CHN", 0)
        
        demo_text = (
            "Demographic factors (Solow model perspective): "
        )
        
        if chn_pop > usa_pop:
            demo_text += (
                f"China's population growth rate ({chn_pop:.2%}) exceeds that of the USA ({usa_pop:.2%}). "
                f"In the Solow model framework, higher population growth can dilute capital per worker, potentially slowing growth per capita "
                f"(ceteris paribus). However, a larger working-age population can also expand markets and human capital availability. "
                f"The observed GDP per capita growth in China suggests that capital accumulation and productivity gains have outpaced "
                f"demographic dilution effects."
            )
        else:
            demo_text += (
                f"The USA has maintained relatively stable population growth ({usa_pop:.2%}), similar to or exceeding China's rate ({chn_pop:.2%}). "
                f"This demographic context provides relative stability for capital accumulation."
            )
        
        interpretation["demographics"] = demo_text
    
    # Summary Theory Mapping
    interpretation["theory_summary"] = (
        "Theoretical synthesis: The Solow model emphasizes capital accumulation and factor inputs as drivers of growth. "
        "The data suggest that capital intensity plays a significant role, particularly in China's rapid development phase. "
        "However, endogenous growth theory highlights the importance of R&D, human capital, and knowledge. "
        "Both theories contribute insights: the Solow framework explains medium-term convergence dynamics and capital's role, "
        "while endogenous growth theory illuminates technology's role and long-term growth sustainability. "
        "Full causal inference would require econometric modeling beyond this descriptive analysis."
    )
    
    return interpretation
