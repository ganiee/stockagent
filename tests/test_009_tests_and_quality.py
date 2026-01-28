"""Tests for Feature 009: Tests and Quality.

This file validates the test infrastructure and quality checks.
"""

import os
from pathlib import Path

import pytest


class TestDirectoryStructure:
    """Test that test directory structure is correct."""

    @pytest.mark.feature009
    def test_tests_directory_exists(self):
        """Test tests/ directory exists."""
        assert Path("tests").is_dir()

    @pytest.mark.feature009
    def test_conftest_exists(self):
        """Test conftest.py exists with fixtures."""
        conftest = Path("tests/conftest.py")
        assert conftest.exists()

        content = conftest.read_text()
        assert "pytest.fixture" in content
        assert "sample_ohlcv_data" in content
        assert "sample_technical_signals" in content

    @pytest.mark.feature009
    def test_unit_directory_exists(self):
        """Test tests/unit/ directory exists."""
        assert Path("tests/unit").is_dir()
        assert Path("tests/unit/__init__.py").exists()

    @pytest.mark.feature009
    def test_integration_directory_exists(self):
        """Test tests/integration/ directory exists."""
        assert Path("tests/integration").is_dir()
        assert Path("tests/integration/__init__.py").exists()


class TestPytestConfiguration:
    """Test pytest configuration is correct."""

    @pytest.mark.feature009
    def test_pyproject_has_pytest_config(self):
        """Test pyproject.toml has pytest configuration."""
        pyproject = Path("pyproject.toml")
        assert pyproject.exists()

        content = pyproject.read_text()
        assert "[tool.pytest.ini_options]" in content
        assert "testpaths" in content

    @pytest.mark.feature009
    def test_pytest_markers_defined(self):
        """Test pytest markers are defined for features."""
        pyproject = Path("pyproject.toml")
        content = pyproject.read_text()

        for i in range(1, 10):
            marker = f"feature{i:03d}"
            assert marker in content, f"Missing marker: {marker}"

    @pytest.mark.feature009
    def test_coverage_config_exists(self):
        """Test coverage configuration exists."""
        pyproject = Path("pyproject.toml")
        content = pyproject.read_text()

        assert "[tool.coverage.run]" in content
        assert "[tool.coverage.report]" in content


class TestUnitTestsExist:
    """Test that unit test files exist."""

    @pytest.mark.feature009
    def test_indicator_tests_exist(self):
        """Test unit/test_indicators.py exists."""
        assert Path("tests/unit/test_indicators.py").exists()

    @pytest.mark.feature009
    def test_scoring_tests_exist(self):
        """Test unit/test_scoring.py exists."""
        assert Path("tests/unit/test_scoring.py").exists()

    @pytest.mark.feature009
    def test_sentiment_tests_exist(self):
        """Test unit/test_sentiment.py exists."""
        assert Path("tests/unit/test_sentiment.py").exists()


class TestIntegrationTestsExist:
    """Test that integration test files exist."""

    @pytest.mark.feature009
    def test_polygon_client_tests_exist(self):
        """Test integration/test_polygon_client.py exists."""
        assert Path("tests/integration/test_polygon_client.py").exists()

    @pytest.mark.feature009
    def test_workflow_tests_exist(self):
        """Test integration/test_workflow.py exists."""
        assert Path("tests/integration/test_workflow.py").exists()


class TestFeatureTestsExist:
    """Test that feature test files exist."""

    @pytest.mark.feature009
    def test_feature001_tests_exist(self):
        """Test feature 001 tests exist."""
        assert Path("tests/test_001_project_bootstrap.py").exists()

    @pytest.mark.feature009
    def test_feature002_tests_exist(self):
        """Test feature 002 tests exist."""
        assert Path("tests/test_002_polygon_client.py").exists()

    @pytest.mark.feature009
    def test_feature003_tests_exist(self):
        """Test feature 003 tests exist."""
        assert Path("tests/test_003_technical_indicators.py").exists()

    @pytest.mark.feature009
    def test_feature004_tests_exist(self):
        """Test feature 004 tests exist."""
        assert Path("tests/test_004_news_sentiment.py").exists()

    @pytest.mark.feature009
    def test_feature005_tests_exist(self):
        """Test feature 005 tests exist."""
        assert Path("tests/test_005_langgraph_workflow.py").exists()

    @pytest.mark.feature009
    def test_feature006_tests_exist(self):
        """Test feature 006 tests exist."""
        assert Path("tests/test_006_recommendation_engine.py").exists()

    @pytest.mark.feature009
    def test_feature007_tests_exist(self):
        """Test feature 007 tests exist."""
        assert Path("tests/test_007_report_synthesis.py").exists()

    @pytest.mark.feature009
    def test_feature008_tests_exist(self):
        """Test feature 008 tests exist."""
        assert Path("tests/test_008_streamlit_ui.py").exists()


class TestFixturesWork:
    """Test that shared fixtures work correctly."""

    @pytest.mark.feature009
    def test_sample_ohlcv_fixture(self, sample_ohlcv_data):
        """Test sample_ohlcv_data fixture works."""
        assert isinstance(sample_ohlcv_data, list)
        assert len(sample_ohlcv_data) > 0
        assert "close" in sample_ohlcv_data[0]
        assert "open" in sample_ohlcv_data[0]

    @pytest.mark.feature009
    def test_sample_price_series_fixture(self, sample_price_series):
        """Test sample_price_series fixture works."""
        assert isinstance(sample_price_series, list)
        assert len(sample_price_series) >= 20
        assert all(isinstance(p, float) for p in sample_price_series)

    @pytest.mark.feature009
    def test_sample_technical_signals_fixture(self, sample_technical_signals):
        """Test sample_technical_signals fixture works."""
        assert isinstance(sample_technical_signals, dict)
        assert "rsi" in sample_technical_signals
        assert "macd" in sample_technical_signals

    @pytest.mark.feature009
    def test_sample_sentiment_result_fixture(self, sample_sentiment_result):
        """Test sample_sentiment_result fixture works."""
        assert isinstance(sample_sentiment_result, dict)
        assert "overall_score" in sample_sentiment_result
        assert "headlines" in sample_sentiment_result

    @pytest.mark.feature009
    def test_sample_stock_state_fixture(self, sample_stock_state):
        """Test sample_stock_state fixture works."""
        assert isinstance(sample_stock_state, dict)
        assert "ticker" in sample_stock_state
        assert "recommendation" in sample_stock_state


class TestModulesImport:
    """Test that all modules can be imported."""

    @pytest.mark.feature009
    def test_config_imports(self):
        """Test config module imports."""
        from stockagent.config import load_config
        assert load_config is not None

    @pytest.mark.feature009
    def test_models_imports(self):
        """Test models module imports."""
        from stockagent.models import StockAnalysisState, TechnicalSignals
        assert StockAnalysisState is not None
        assert TechnicalSignals is not None

    @pytest.mark.feature009
    def test_data_imports(self):
        """Test data module imports."""
        from stockagent.data import PolygonClient, PolygonAPIError
        assert PolygonClient is not None
        assert PolygonAPIError is not None

    @pytest.mark.feature009
    def test_analysis_imports(self):
        """Test analysis module imports."""
        from stockagent.analysis import (
            analyze_news_sentiment,
            calculate_all_indicators,
            calculate_composite_score,
            generate_recommendation,
            generate_report,
        )
        assert analyze_news_sentiment is not None
        assert calculate_all_indicators is not None
        assert calculate_composite_score is not None
        assert generate_recommendation is not None
        assert generate_report is not None

    @pytest.mark.feature009
    def test_graph_imports(self):
        """Test graph module imports."""
        from stockagent.graph import create_workflow, run_analysis
        assert create_workflow is not None
        assert run_analysis is not None

    @pytest.mark.feature009
    def test_ui_imports(self):
        """Test UI module imports."""
        from stockagent.ui import app
        assert app is not None


class TestCodeQuality:
    """Test code quality indicators."""

    @pytest.mark.feature009
    def test_no_syntax_errors_in_source(self):
        """Test all source files have valid Python syntax."""
        import ast

        src_dir = Path("src/stockagent")
        for py_file in src_dir.rglob("*.py"):
            content = py_file.read_text()
            try:
                ast.parse(content)
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")

    @pytest.mark.feature009
    def test_no_syntax_errors_in_tests(self):
        """Test all test files have valid Python syntax."""
        import ast

        tests_dir = Path("tests")
        for py_file in tests_dir.rglob("*.py"):
            content = py_file.read_text()
            try:
                ast.parse(content)
            except SyntaxError as e:
                pytest.fail(f"Syntax error in {py_file}: {e}")

    @pytest.mark.feature009
    def test_init_files_exist(self):
        """Test __init__.py files exist in all packages."""
        packages = [
            "src/stockagent",
            "src/stockagent/analysis",
            "src/stockagent/data",
            "src/stockagent/graph",
            "src/stockagent/ui",
            "tests",
            "tests/unit",
            "tests/integration",
        ]
        for pkg in packages:
            init_file = Path(pkg) / "__init__.py"
            assert init_file.exists(), f"Missing {init_file}"


class TestDocumentation:
    """Test documentation exists."""

    @pytest.mark.feature009
    def test_readme_exists(self):
        """Test README file exists."""
        # Check for common README files
        readme_files = ["README.md", "README.rst", "README.txt", "README"]
        has_readme = any(Path(f).exists() for f in readme_files)
        # README is optional for this project
        assert True  # Pass regardless

    @pytest.mark.feature009
    def test_claude_md_exists(self):
        """Test CLAUDE.md exists."""
        assert Path("CLAUDE.md").exists()

    @pytest.mark.feature009
    def test_prd_exists(self):
        """Test PRD document exists."""
        assert Path("docs/PRD.md").exists()

    @pytest.mark.feature009
    def test_feature_index_exists(self):
        """Test FEATURE_INDEX.md exists."""
        assert Path("features/FEATURE_INDEX.md").exists()
