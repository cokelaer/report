"""Tests for sequana_report.config module."""
from pathlib import Path

from sequana_report import config


def test_package_dir():
    assert config.PACKAGE_DIR.exists()
    assert config.PACKAGE_DIR.is_dir()


def test_resources_dir():
    assert config.RESOURCES_DIR.exists()
    assert config.RESOURCES_DIR.is_dir()


def test_css_dir():
    assert config.CSS_DIR.exists()
    assert config.CSS_DIR.is_dir()


def test_js_dir():
    assert config.JS_DIR.exists()
    assert config.JS_DIR.is_dir()


def test_images_dir():
    assert config.IMAGES_DIR.exists()
    assert config.IMAGES_DIR.is_dir()


def test_templates_dir():
    assert config.TEMPLATES_DIR.exists()
    assert config.TEMPLATES_DIR.is_dir()


def test_css_list():
    assert isinstance(config.css_list, list)
    for css_file in config.css_list:
        assert isinstance(css_file, str)
        assert css_file.endswith(".css")


def test_js_list():
    assert isinstance(config.js_list, list)
    for js_file in config.js_list:
        assert isinstance(js_file, str)
        assert js_file.endswith(".js")


def test_logo():
    if config.logo is not None:
        assert isinstance(config.logo, str)
        logo_path = Path(config.logo)
        assert logo_path.suffix in {".png", ".jpg", ".jpeg", ".gif"}


def test_version():
    assert isinstance(config.__version__, str)
    assert len(config.__version__) > 0


def test_output_dir():
    assert isinstance(config.output_dir, str)


def test_sample_name():
    assert isinstance(config.sample_name, str)
