"""
Chart generation module for USA vs China Growth Analysis.

Handles Plotly chart creation and rendering.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd


def create_line_chart(df, x_col: str, y_col: str, color_col: str, title: str, y_label: str) -> str:
    """Create generic line chart.
    
    Args:
        df: DataFrame with data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        color_col: Column name for color grouping
        title: Chart title
        y_label: Y-axis label
    
    Returns:
        HTML string of Plotly chart
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        labels={x_col: "Rok", y_col: y_label},
        markers=True,
    )
    
    fig.update_layout(
        hovermode="x unified",
        height=400,
        template="plotly_white",
    )
    
    div_id = "chart_" + ''.join(
        ch if ch.isalnum() or ch == '_' else '_' for ch in title.replace(" ", "_").lower()
    )
    return fig.to_html(include_plotlyjs='cdn', full_html=False, div_id=div_id)


def create_gdp_chart(df) -> str:
    """Create GDP per capita comparison chart.
    
    Args:
        df: DataFrame with gdp_per_capita data
    
    Returns:
        HTML string of Plotly chart
    """
    gdp_data = df[df["indicator"] == "gdp_per_capita"].copy()
    
    if gdp_data.empty:
        return "<p>Brak dostępnych danych PKB per capita</p>"
    
    return create_line_chart(
        gdp_data,
        x_col="year",
        y_col="value",
        color_col="country_name",
        title="PKB per capita (USD stały 2015)",
        y_label="PKB per capita (USD)"
    )


def create_growth_chart(df) -> str:
    """Create annual GDP growth rate chart.
    
    Args:
        df: DataFrame with growth rate data
    
    Returns:
        HTML string of Plotly chart
    """
    if df.empty:
        return "<p>Brak dostępnych danych tempa wzrostu</p>"
    
    # Calculate annual growth from GDP data
    gdp_data = df[df["indicator"] == "gdp_per_capita"].copy()
    gdp_data = gdp_data.sort_values(by=["country_code", "year"])
    gdp_data["annual_growth"] = gdp_data.groupby("country_code")["value"].pct_change()
    
    growth_data = gdp_data[gdp_data["annual_growth"].notna()].copy()
    growth_data["annual_growth_pct"] = growth_data["annual_growth"] * 100
    
    if growth_data.empty:
        return "<p>Brak dostępnych danych tempa wzrostu</p>"
    
    return create_line_chart(
        growth_data,
        x_col="year",
        y_col="annual_growth_pct",
        color_col="country_name",
        title="Roczne tempo wzrostu PKB per capita (%)",
        y_label="Wzrost roczny (%)"
    )


def create_ratio_chart(df) -> str:
    """Create China-to-USA GDP per capita ratio chart.
    
    Args:
        df: DataFrame with ratio data
    
    Returns:
        HTML string of Plotly chart
    """
    gdp_data = df[df["indicator"] == "gdp_per_capita"].copy()
    
    if gdp_data.empty:
        return "<p>Brak dostępnych danych PKB dla obliczenia stosunku</p>"
    
    # Pivot to get USA and China values by year
    pivoted = gdp_data.pivot_table(
        index="year",
        columns="country_code",
        values="value",
        aggfunc="first"
    )
    
    if "USA" not in pivoted.columns or "CHN" not in pivoted.columns:
        return "<p>Brak danych USA lub Chin dla obliczenia stosunku</p>"
    
    pivoted["ratio"] = pivoted["CHN"] / pivoted["USA"]
    ratio_data = pivoted[["ratio"]].reset_index()
    ratio_data.columns = ["year", "China_to_USA_Ratio"]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ratio_data["year"],
        y=ratio_data["China_to_USA_Ratio"],
        mode="lines+markers",
        name="Stosunek Chiny/USA",
        line=dict(color="red", width=3),
    ))
    
    fig.update_layout(
        title="Stosunek PKB per capita Chin do USA",
        xaxis_title="Rok",
        yaxis_title="Stosunek",
        height=400,
        template="plotly_white",
        hovermode="x unified",
    )
    
    return fig.to_html(include_plotlyjs='cdn', full_html=False, div_id="ratio_chart")


def create_indicator_chart(df, indicator_name: str, title: str, y_label: str) -> str:
    """Create generic indicator comparison chart.
    
    Args:
        df: DataFrame with indicator data
        indicator_name: Name of indicator column
        title: Chart title
        y_label: Y-axis label
    
    Returns:
        HTML string of Plotly chart
    """
    indicator_data = df[df["indicator"] == indicator_name].copy()
    
    if indicator_data.empty:
        return f"<p>No data available for {indicator_name}</p>"
    
    return create_line_chart(
        indicator_data,
        x_col="year",
        y_col="value",
        color_col="country_name",
        title=title,
        y_label=y_label
    )
