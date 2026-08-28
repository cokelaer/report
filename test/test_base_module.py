"""Tests for sequana_report.base_module module."""
import os
import shutil
import tempfile
from pathlib import Path

import pytest

from sequana_report import config
from sequana_report.base_module import SequanaBaseModule


@pytest.fixture
def tmpdir_fixture(tmpdir):
    """Fixture to set config.output_dir to temp directory."""
    original_output_dir = config.output_dir
    config.output_dir = str(tmpdir)
    yield tmpdir
    config.output_dir = original_output_dir


def test_base_module_init_default(tmpdir_fixture):
    module = SequanaBaseModule()
    assert module.output_dir == config.output_dir
    assert module.path == "./"
    assert module.template is not None
    assert module._fotorama_js_added is False
    assert module.required_dir == ("css", "js", "images")


def test_base_module_init_custom_template():
    with tempfile.TemporaryDirectory() as tmpdir:
        original_output_dir = config.output_dir
        config.output_dir = tmpdir
        try:
            module = SequanaBaseModule(template_fn="standard.html")
            assert module.template is not None
        finally:
            config.output_dir = original_output_dir


def test_base_module_init_report_creates_directories(tmpdir_fixture):
    module = SequanaBaseModule()

    assert os.path.isdir(config.output_dir)
    assert os.path.isdir(os.path.join(config.output_dir, "css"))
    assert os.path.isdir(os.path.join(config.output_dir, "js"))
    assert os.path.isdir(os.path.join(config.output_dir, "images"))


def test_base_module_custom_required_dir(tmpdir_fixture):
    custom_dirs = ("custom1", "custom2")
    module = SequanaBaseModule(required_dir=custom_dirs)
    assert module.required_dir == custom_dirs

    for directory in custom_dirs:
        assert os.path.isdir(os.path.join(config.output_dir, directory))


def test_create_html(tmpdir_fixture):
    module = SequanaBaseModule()
    output_filename = "test_report.html"

    module.create_html(output_filename)

    html_file = os.path.join(config.output_dir, output_filename)
    assert os.path.isfile(html_file)

    with open(html_file, "r") as f:
        content = f.read()
        assert len(content) > 0


def test_create_html_none_output(tmpdir_fixture):
    module = SequanaBaseModule()
    module.create_html(None)


def test_create_link_basic(tmpdir_fixture):
    module = SequanaBaseModule()
    link = module.create_link("test", "http://example.com")
    assert 'href="http://example.com"' in link
    assert "test" in link
    assert 'target="_blank"' in link


def test_create_link_no_newtab(tmpdir_fixture):
    module = SequanaBaseModule()
    link = module.create_link("test", "http://example.com", newtab=False)
    assert 'href="http://example.com"' in link
    assert 'target="_blank"' not in link


def test_create_link_download(tmpdir_fixture):
    module = SequanaBaseModule()
    link = module.create_link("test", "file.txt", download=True)
    assert 'href="file.txt"' in link
    assert 'download="file.txt"' in link


def test_create_hide_section(tmpdir_fixture):
    module = SequanaBaseModule()
    link, content = module.create_hide_section("test_id", "Click me", "Hidden content")

    assert "test_id" in link
    assert "Click me" in link
    assert "Hidden content" in content
    assert "slidingDiv" in content
    assert "show_hide" in link


def test_create_hide_section_hidden(tmpdir_fixture):
    module = SequanaBaseModule()
    link, content = module.create_hide_section("test_id", "Click me", "Hidden content", hide=True)

    assert "slidingDiv" in content
    assert "hide()" in content


def test_copy_file(tmpdir_fixture):
    module = SequanaBaseModule()

    test_file = os.path.join(str(tmpdir_fixture), "test_input.txt")
    with open(test_file, "w") as f:
        f.write("test content")

    relative_path = module.copy_file(test_file, "custom_dir")

    assert "custom_dir" in relative_path
    assert "test_input.txt" in relative_path

    target_file = os.path.join(config.output_dir, relative_path)
    assert os.path.isfile(target_file)

    with open(target_file, "r") as f:
        assert f.read() == "test content"


def test_copy_file_not_found(tmpdir_fixture):
    module = SequanaBaseModule()

    with pytest.raises(FileNotFoundError):
        module.copy_file("nonexistent_file.txt", "custom_dir")


def test_add_float_right(tmpdir_fixture):
    module = SequanaBaseModule()
    html = module.add_float_right("Test content")

    assert 'float:right' in html
    assert "Test content" in html


def test_add_code_section(tmpdir_fixture):
    module = SequanaBaseModule()
    html = module.add_code_section("print('hello')", "python")

    assert "code" in html
    assert "python" in html
    assert "print('hello')" in html


def test_include_svg_image(tmpdir_fixture):
    module = SequanaBaseModule()
    html = module.include_svg_image("image.svg", alt="Test image")

    assert "image.svg" in html
    assert "image/svg+xml" in html
    assert "Test image" in html


def test_png_to_embedded_png(tmpdir_fixture):
    module = SequanaBaseModule()

    test_png = os.path.join(str(tmpdir_fixture), "test.png")
    with open(test_png, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"fake png data")

    html = module.png_to_embedded_png(test_png, alt="Test", title="Test title")

    assert 'data:image/png;base64,' in html
    assert "Test" in html
    assert "Test title" in html


def test_png_to_embedded_png_with_style(tmpdir_fixture):
    module = SequanaBaseModule()

    test_png = os.path.join(str(tmpdir_fixture), "test.png")
    with open(test_png, "wb") as f:
        f.write(b"\x89PNG\r\n\x1a\n" + b"fake png data")

    html = module.png_to_embedded_png(test_png, style="width:100px;", alt="Test")

    assert 'data:image/png;base64,' in html
    assert "width:100px;" in html


def test_create_embedded_png(tmpdir_fixture):
    module = SequanaBaseModule()

    def plot_func(output):
        output.write(b"\x89PNG\r\n\x1a\n" + b"fake png data")

    html = module.create_embedded_png(plot_func, "output")

    assert 'data:image/png;base64,' in html
    assert "<img" in html


def test_create_embedded_png_with_kwargs(tmpdir_fixture):
    module = SequanaBaseModule()

    def plot_func(output, **kwargs):
        output.write(b"\x89PNG\r\n\x1a\n" + b"fake png data")

    html = module.create_embedded_png(plot_func, "output", style="width:100px;")

    assert 'data:image/png;base64,' in html
    assert 'style="width:100px;"' in html


def test_create_embedded_png_error(tmpdir_fixture):
    module = SequanaBaseModule()

    def plot_func(output):
        raise ValueError("Test error")

    html = module.create_embedded_png(plot_func, "output")

    assert "image not created" in html


def test_create_combobox(tmpdir_fixture):
    module = SequanaBaseModule()

    paths = ["file1.html", "file2.html", "file3.html"]
    html = module.create_combobox(paths, "test_id")

    assert "jq-dropdown-test_id" in html
    for path in paths:
        assert path in html


def test_add_fotorama(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg"), Path("image2.jpg"), Path("image3.jpg")]
    html = module.add_fotorama(files)

    assert "fotorama" in html
    assert "image1.jpg" in html
    assert "image2.jpg" in html
    assert "image3.jpg" in html
    assert module._fotorama_js_added is True


def test_add_fotorama_without_thumbnails(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg"), Path("image2.jpg")]
    html = module.add_fotorama(files, thumbnails=False)

    assert "fotorama" in html
    assert 'data-nav="thumbs"' not in html


def test_add_fotorama_without_loop(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg"), Path("image2.jpg")]
    html = module.add_fotorama(files, loop=False)

    assert "fotorama" in html
    assert 'data-loop="true"' not in html


def test_add_fotorama_with_captions(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg"), Path("image2.jpg")]
    captions = ["First image", "Second image"]
    html = module.add_fotorama(files, captions=captions)

    assert "First image" in html
    assert "Second image" in html


def test_add_fotorama_with_bad_captions(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg"), Path("image2.jpg")]
    captions = ["Only one caption"]

    with pytest.raises(ValueError):
        module.add_fotorama(files, captions=captions)


def test_add_fotorama_js_added_once(tmpdir_fixture):
    module = SequanaBaseModule()

    files = [Path("image1.jpg")]
    html1 = module.add_fotorama(files)
    html2 = module.add_fotorama(files)

    assert "cdnjs.cloudflare.com" in html1
    assert "cdnjs.cloudflare.com" not in html2
