"""Tests for sequana_report.utils.canvasjs_base module."""
import pytest

from sequana_report.utils.canvasjs_base import CanvasJS


def test_canvasjs_init():
    chart = CanvasJS("chart1")
    assert chart.html_id == "chart1"
    assert isinstance(chart.title_section, dict)
    assert isinstance(chart.legend_section, dict)
    assert isinstance(chart.axis_section, dict)
    assert isinstance(chart.data_section, list)
    assert isinstance(chart.options, dict)


def test_set_title():
    chart = CanvasJS("chart1")
    chart.set_title("Test Title")

    assert chart.title_section["text"] == "Test Title"


def test_set_title_with_attributes():
    chart = CanvasJS("chart1")
    attrs = {"fontFamily": "verdana", "fontSize": 16}
    chart.set_title("Test Title", title_attr=attrs)

    assert chart.title_section["text"] == "Test Title"
    assert chart.title_section["fontFamily"] == "verdana"
    assert chart.title_section["fontSize"] == 16


def test_set_legend():
    chart = CanvasJS("chart1")
    chart.set_legend()

    assert isinstance(chart.legend_section, dict)


def test_set_legend_with_attributes():
    chart = CanvasJS("chart1")
    attrs = {"fontFamily": "verdana", "fontSize": 12}
    chart.set_legend(legend_attr=attrs)

    assert chart.legend_section["fontFamily"] == "verdana"
    assert chart.legend_section["fontSize"] == 12


def test_set_legend_hide_on_click_default():
    chart = CanvasJS("chart1")
    chart.set_legend()

    assert "itemclick" in chart.legend_section


def test_set_legend_hide_on_click_false():
    chart = CanvasJS("chart1")
    chart.set_legend(hide_on_click=False)

    assert "itemclick" not in chart.legend_section


def test_set_options():
    chart = CanvasJS("chart1")
    options = {"responsive": True, "animationEnabled": True}
    chart.set_options(options)

    assert chart.options["responsive"] is True
    assert chart.options["animationEnabled"] is True


def test_set_options_multiple_calls():
    chart = CanvasJS("chart1")
    chart.set_options({"option1": "value1"})
    chart.set_options({"option2": "value2"})

    assert chart.options["option1"] == "value1"
    assert chart.options["option2"] == "value2"


def test_set_axis():
    chart = CanvasJS("chart1")
    axis_attrs = {"title": "X axis", "titleFontSize": 16}
    chart._set_axis("axisX", axis_attrs)

    assert "axisX" in chart.axis_section
    assert chart.axis_section["axisX"]["title"] == "X axis"


def test_set_multiple_axes():
    chart = CanvasJS("chart1")
    chart._set_axis("axisX", {"title": "X axis"})
    chart._set_axis("axisY", {"title": "Y axis"})

    assert "axisX" in chart.axis_section
    assert "axisY" in chart.axis_section


def test_set_data():
    chart = CanvasJS("chart1")
    data_dict = {"type": "line", "dataPoints": [{"x": 1, "y": 10}]}
    chart.set_data(data_dict)

    assert len(chart.data_section) == 1
    assert chart.data_section[0]["type"] == "line"


def test_set_data_multiple():
    chart = CanvasJS("chart1")
    chart.set_data({"type": "line"})
    chart.set_data({"type": "column"})

    assert len(chart.data_section) == 2


def test_set_data_update_at_index():
    chart = CanvasJS("chart1")
    chart.set_data({"type": "line", "dataPoints": []})
    chart.set_data({"dataPoints": [{"x": 1, "y": 10}]}, index=0)

    assert chart.data_section[0]["type"] == "line"
    assert len(chart.data_section[0]["dataPoints"]) == 1


def test_check_type_string():
    chart = CanvasJS("chart1")
    result = chart._check_type("test_string")

    assert result == '"test_string"'


def test_check_type_boolean():
    chart = CanvasJS("chart1")
    assert chart._check_type("true") == "true"
    assert chart._check_type("false") == "false"


def test_check_type_function():
    chart = CanvasJS("chart1")
    result = chart._check_type("function(e) { return e; }")

    assert result == "function(e) { return e; }"


def test_check_type_number():
    chart = CanvasJS("chart1")
    assert chart._check_type(123) == 123
    assert chart._check_type(45.67) == 45.67


def test_check_type_data_variable():
    chart = CanvasJS("chart1")
    result = chart._check_type("data_var")

    assert result == "data_var"


def test_check_type_object():
    chart = CanvasJS("chart1")
    result = chart._check_type("{key: value}")

    assert result == "{key: value}"


def test_dict_to_string():
    chart = CanvasJS("chart1")
    d = {"key1": "value1", "key2": 123}
    result = chart._dict_to_string(d)

    assert 'key1:"value1"' in result
    assert "key2:123" in result


def test_dict_to_string_with_function():
    chart = CanvasJS("chart1")
    d = {"callback": "function(e) { return e; }"}
    result = chart._dict_to_string(d)

    assert "function(e)" in result
    assert '"function' not in result


def test_create_div_chart_container():
    chart = CanvasJS("chart1")
    html = chart.create_div_chart_container()

    assert 'id="chartContainer_chart1"' in html
    assert "<div" in html


def test_create_div_chart_container_with_style():
    chart = CanvasJS("chart1")
    html = chart.create_div_chart_container(style_option="width:100%; height:400px;")

    assert 'id="chartContainer_chart1"' in html
    assert "width:100%; height:400px;" in html


def test_create_canvas_js_object_basic():
    chart = CanvasJS("chart1")
    chart.set_title("Test Chart")
    chart.set_data({"type": "line", "dataPoints": [{"x": 1, "y": 10}]})

    js = chart.create_canvas_js_object()

    assert "title:" in js
    assert '"Test Chart"' in js
    assert "data:" in js
    assert "type" in js


def test_create_canvas_js_object_with_legend():
    chart = CanvasJS("chart1")
    chart.set_legend()
    chart.set_data({"type": "line"})

    js = chart.create_canvas_js_object()

    assert "legend:" in js


def test_create_canvas_js_object_with_axes():
    chart = CanvasJS("chart1")
    chart._set_axis("axisX", {"title": "X Axis"})
    chart._set_axis("axisY", {"title": "Y Axis"})
    chart.set_data({"type": "line"})

    js = chart.create_canvas_js_object()

    assert "axisX:" in js
    assert "axisY:" in js


def test_create_canvas_js_object_with_options():
    chart = CanvasJS("chart1")
    chart.set_options({"responsive": True})
    chart.set_data({"type": "line"})

    js = chart.create_canvas_js_object()

    assert "responsive" in js


def test_create_canvas_js_object_complete():
    chart = CanvasJS("chart1")
    chart.set_title("Complete Chart")
    chart.set_legend()
    chart._set_axis("axisX", {"title": "X"})
    chart._set_axis("axisY", {"title": "Y"})
    chart.set_options({"responsive": True})
    chart.set_data({"type": "line", "dataPoints": [{"x": 1, "y": 5}, {"x": 2, "y": 10}]})

    js = chart.create_canvas_js_object()

    assert "title:" in js
    assert "legend:" in js
    assert "axisX:" in js
    assert "axisY:" in js
    assert "responsive" in js
    assert "data:" in js
    assert js.startswith("{")
    assert js.endswith("}")


def test_create_canvas_js_object_is_valid_javascript():
    chart = CanvasJS("chart1")
    chart.set_title("Test")
    chart.set_data({"type": "line"})

    js = chart.create_canvas_js_object()

    assert js.count("{") == js.count("}")
    assert js.count("[") == js.count("]")
