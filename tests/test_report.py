"""
Tests for report generation functions.

Tests for HTML report rendering and content generation.
"""

import pytest
import os
import tempfile
from pathlib import Path
from src.report import render_html_report


class TestRenderHTMLReport:
    """Tests for HTML report rendering."""

    def test_render_creates_file(self):
        """Test that render_html_report creates an output file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            context = {
                "title": "USA vs China Growth Analysis",
                "research_question": "Does growth result from capital, demography, or technology?",
                "methodology": "Using World Bank data and economic theory.",
                "data_availability_table": "<table><tr><td>Test</td></tr></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Test summary</p>",
                "capital_interpretation": "<p>Capital analysis</p>",
                "demographic_interpretation": "<p>Demographic analysis</p>",
                "technology_interpretation": "<p>Technology analysis</p>",
                "theory_mapping": "<table><tr><td>Theory</td></tr></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            result = render_html_report(context, output_path)
            
            assert os.path.exists(output_path)
            assert Path(output_path).stat().st_size > 0

    def test_render_returns_file_path(self):
        """Test that function returns the output file path."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            context = {
                "title": "USA vs China Growth Analysis",
                "research_question": "Does growth result from capital, demography, or technology?",
                "methodology": "Using World Bank data.",
                "data_availability_table": "<table></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            result = render_html_report(context, output_path)
            
            assert result == output_path

    def test_render_contains_title(self):
        """Test that generated HTML contains the title."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            context = {
                "title": "USA vs China Growth Analysis",
                "research_question": "Test question",
                "methodology": "Test methodology",
                "data_availability_table": "<table></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            render_html_report(context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "USA vs China Growth Analysis" in content

    def test_render_contains_research_question(self):
        """Test that generated HTML contains research question."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            research_q = "Does economic growth result mainly from capital, demographic, or technological factors?"
            context = {
                "title": "Test",
                "research_question": research_q,
                "methodology": "Test methodology",
                "data_availability_table": "<table></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            render_html_report(context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert research_q in content

    def test_render_contains_sections(self):
        """Test that report contains all required sections."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            context = {
                "title": "Test",
                "research_question": "Test",
                "methodology": "Test",
                "data_availability_table": "<table></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            render_html_report(context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read().lower()
            
            # Check for key sections
            sections = ["methodology", "limitation", "conclusion"]
            for section in sections:
                assert section in content

    def test_render_with_charts(self):
        """Test that report renders correctly with charts."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            chart_html = '<div id="chart1"><p>Sample chart</p></div>'
            context = {
                "title": "Test",
                "research_question": "Test",
                "methodology": "Test",
                "data_availability_table": "<table></table>",
                "charts": [{"html": chart_html, "title": "GDP per capita"}],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            render_html_report(context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert "chart" in content.lower() or "Sample chart" in content

    def test_render_is_valid_html(self):
        """Test that output is valid HTML."""
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "report.html")
            
            context = {
                "title": "Test",
                "research_question": "Test",
                "methodology": "Test",
                "data_availability_table": "<table></table>",
                "charts": [],
                "gdp_growth_summary": "<p>Summary</p>",
                "capital_interpretation": "<p>Capital</p>",
                "demographic_interpretation": "<p>Demographic</p>",
                "technology_interpretation": "<p>Technology</p>",
                "theory_mapping": "<table></table>",
                "limitations": "<p>Limitations</p>",
                "conclusion": "<p>Conclusion</p>",
            }
            
            render_html_report(context, output_path)
            
            with open(output_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic HTML validation
            assert "<html" in content.lower()
            assert "</html>" in content.lower()
            assert "<body" in content.lower()
            assert "</body>" in content.lower()
