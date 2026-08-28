"""Tests for sequana_report.utils.canvasjs_linegraph module."""
import pytest

from sequana_report.utils.canvasjs_linegraph import CanvasJSLineGraph


@pytest.fixture
def sample_csv():
    return """x,y1,y2
1,10,20
2,15,25
3,20,30
4,25,35"""


@pytest.fixture
def sample_csv_with_spaces():
    return """x, y1, y2
1, 10, 20
2, 15, 25
3, 20, 30
4, 25, 35"""


def test_canvasjs_linegraph_init(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1", "y2"])

    assert graph.html_id == "graph1"
    assert graph.x_column == "x"
    assert graph.y_columns == ["y1", "y2"]
    assert graph.csv is not None


def test_canvasjs_linegraph_strip_csv(sample_csv_with_spaces):
    csv_with_newlines = f"\n\n{sample_csv_with_spaces}\n\n"
    graph = CanvasJSLineGraph(csv_with_newlines, "graph1", "x", ["y1", "y2"])

    assert graph.csv == sample_csv_with_spaces.strip()


def test_create_hidden_csv(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    html = graph._create_hidden_csv()

    assert 'id="graph1"' in html
    assert "display:none" in html
    assert "x,y1" in html


def test_create_js_csv_parser(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1", "y2"])
    js_func = graph._create_js_csv_parser()

    assert "processData_graph1" in js_func
    assert "Papa.parse" in js_func
    assert "data_y1" in js_func
    assert "data_y2" in js_func
    assert "drawChart_graph1" in js_func
    assert graph.variables == "data_y1, data_y2"


def test_create_js_csv_parser_single_column(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    js_func = graph._create_js_csv_parser()

    assert "processData_graph1" in js_func
    assert "data_y1" in js_func
    assert "data_y2" not in js_func


def test_set_axis_x(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    graph.set_axis_x({"title": "Time", "titleFontSize": 16})

    assert "axisX" in graph.axis_section
    assert graph.axis_section["axisX"]["title"] == "Time"


def test_set_axis_y(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    graph.set_axis_y({"title": "Values", "titleFontSize": 14})

    assert "axisY" in graph.axis_section
    assert graph.axis_section["axisY"]["title"] == "Values"


def test_set_axis_y2(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1", "y2"])
    graph.set_axis_y2({"title": "Secondary Values", "titleFontSize": 12})

    assert "axisY2" in graph.axis_section
    assert graph.axis_section["axisY2"]["title"] == "Secondary Values"


def test_html_cjs_contains_script(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])

    assert "<script type=" in graph.html_cjs
    assert '<pre id="graph1">' in graph.html_cjs


def test_create_canvasjs_complete(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1", "y2"])
    graph.set_title("Test Chart")
    graph.set_axis_x({"title": "X Axis"})
    graph.set_axis_y({"title": "Y Axis"})

    output = graph.create_canvasjs()

    assert "<pre" in output
    assert "processData_graph1" in output
    assert "drawChart_graph1" in output
    assert "$(document).ready" in output
    assert 'id="chartContainer_graph1"' in output
    assert "CanvasJS.Chart" in output


def test_create_canvasjs_has_default_style(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    output = graph.create_canvasjs()

    assert "height: 450px" in output
    assert "width: 100%" in output


def test_create_canvasjs_inheritance(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    graph.set_legend()

    output = graph.create_canvasjs()

    assert "legend:" in output


def test_data_section_initialized(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1", "y2"])

    assert len(graph.data_section) == 2
    assert graph.data_section[0]["dataPoints"] == "data_y1"
    assert graph.data_section[1]["dataPoints"] == "data_y2"


def test_multiple_y_columns(sample_csv):
    y_columns = ["y1", "y2"]
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", y_columns)
    js_func = graph._create_js_csv_parser()

    for col in y_columns:
        assert f"data_{col}" in js_func


def test_custom_x_column():
    csv = """time,temperature,humidity
0,20,30
1,21,31
2,22,32"""
    graph = CanvasJSLineGraph(csv, "graph1", "time", ["temperature", "humidity"])

    assert graph.x_column == "time"
    js_func = graph._create_js_csv_parser()
    assert "curow.time" in js_func


def test_csv_with_comments():
    csv = """x,y
# This is a comment
1,10
# Another comment
2,20"""
    graph = CanvasJSLineGraph(csv, "graph1", "x", ["y"])
    js_func = graph._create_js_csv_parser()

    assert "comments: '#'" in js_func


def test_canvasjs_linegraph_inheritance():
    csv = "x,y\n1,10\n2,20"
    graph = CanvasJSLineGraph(csv, "graph1", "x", ["y"])

    assert hasattr(graph, "set_title")
    assert hasattr(graph, "set_legend")
    assert hasattr(graph, "set_options")
    assert hasattr(graph, "create_canvas_js_object")


def test_create_canvasjs_closing_script_tag(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "graph1", "x", ["y1"])
    output = graph.create_canvasjs()

    assert output.count("</script>") == 1
    assert "</script>" in output


def test_html_id_in_all_parts(sample_csv):
    graph = CanvasJSLineGraph(sample_csv, "mytest123", "x", ["y1"])
    output = graph.create_canvasjs()

    assert "mytest123" in output
    assert 'id="mytest123"' in output or 'id="chartContainer_mytest123"' in output
