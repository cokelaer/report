"""Tests for sequana_report.utils.datatables_js module."""
import pytest

try:
    import pandas as pd
except ImportError:
    pd = None

from sequana_report.utils.datatables_js import DataTable, DataTableFunction


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["NYC", "LA", "Chicago"]
    })


@pytest.fixture
def sample_df_with_index():
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["NYC", "LA", "Chicago"]
    })
    df.index = ["row1", "row2", "row3"]
    return df


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_function_init(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")

    assert dtf.html_id == "id_test_table"
    assert dtf.index is False
    assert isinstance(dtf.datatable_options, dict)
    assert isinstance(dtf.datatable_columns, dict)


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_function_init_with_index(sample_df):
    dtf = DataTableFunction(sample_df, "test_table", index=True)

    assert dtf.index is True
    assert "" in dtf.datatable_columns


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_columns_set(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    columns = dtf.datatable_columns

    assert "name" in columns
    assert "age" in columns
    assert "city" in columns


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_function_set_options(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    dtf.datatable_options = {"pageLength": 15, "dom": "Bfrtip"}

    assert dtf.datatable_options["pageLength"] == 15
    assert dtf.datatable_options["dom"] == "Bfrtip"


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_function_set_options_with_buttons(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    dtf.datatable_options = {"buttons": ["copy", "csv"]}

    buttons = dtf.datatable_options["buttons"]
    assert len(buttons) == 2
    for button in buttons:
        assert isinstance(button, dict)
        assert "exportOptions" in button
        assert "filename" in button


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_function_delete_options(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    dtf.datatable_options = {"pageLength": 15}
    del dtf.datatable_options

    assert len(dtf.datatable_options) == 0


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_javascript_function(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    js = dtf.create_javascript_function()

    assert "<script" in js
    assert "Papa.parse" in js
    assert "parseCsv_id_test_table" in js
    assert "</script>" in js


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_check_type_string(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    assert dtf._check_type("hello") == "'hello'"


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_check_type_boolean(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    assert dtf._check_type("true") == "true"
    assert dtf._check_type("false") == "false"


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_check_type_function(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    result = dtf._check_type("function(data) { return data; }")
    assert result == "function(data) { return data; }"


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_check_type_number(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    assert dtf._check_type(123) == 123
    assert dtf._check_type(45.67) == 45.67


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_check_type_list(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    result = dtf._check_type("[1, 2, 3]")
    assert result == "[1, 2, 3]"


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_dict_to_string(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    d = {"key1": "value1", "key2": 123}
    result = dtf._dict_to_string(d)

    assert "key1:'value1'" in result
    assert "key2:123" in result


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_set_links_to_column(sample_df):
    df = sample_df.copy()
    df["link"] = ["url1", "url2", "url3"]
    dtf = DataTableFunction(df, "test_table")

    dtf.set_links_to_column("link", "name")

    assert dtf.datatable_columns["link"]["visible"] == "false"
    assert "render" in dtf.datatable_columns["name"]
    assert "href" in dtf.datatable_columns["name"]["render"]


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_set_links_to_column_same_page(sample_df):
    df = sample_df.copy()
    df["link"] = ["url1", "url2", "url3"]
    dtf = DataTableFunction(df, "test_table")

    dtf.set_links_to_column("link", "name", new_page=False)

    assert 'target="_blank"' not in dtf.datatable_columns["name"]["render"]


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_set_tooltips_to_column(sample_df):
    df = sample_df.copy()
    df["tooltip"] = ["tip1", "tip2", "tip3"]
    dtf = DataTableFunction(df, "test_table")

    dtf.set_tooltips_to_column("tooltip", "name")

    assert dtf.datatable_columns["tooltip"]["visible"] == "false"
    assert "render" in dtf.datatable_columns["name"]
    assert "data-toggle=" in dtf.datatable_columns["name"]["render"]


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_init(sample_df):
    dt = DataTable(sample_df, "test_table")

    assert dt.html_id == "id_test_table"
    assert len(dt) == 3
    assert isinstance(dt.datatable, DataTableFunction)


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_init_with_existing_datatable_function(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    dt = DataTable(sample_df, "test_table2", datatable=dtf)

    assert dt.datatable is dtf


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_len(sample_df):
    dt = DataTable(sample_df, "test_table")
    assert len(dt) == 3


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_df_property(sample_df):
    dt = DataTable(sample_df, "test_table")
    assert dt.df is sample_df


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_html(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable()

    assert "<table" in html
    assert 'id="table_id_test_table"' in html
    assert "<thead>" in html
    assert "<th>" in html
    assert "width:100%" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_html_custom_style(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable(style="width:80%; height:500px;")

    assert "width:80%; height:500px;" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_html_no_style(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable(style="")

    assert 'style=""' not in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_html_columns_header(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable()

    assert ">name<" in html
    assert ">age<" in html
    assert ">city<" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_hidden_csv(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable()

    assert 'id="csv_id_test_table"' in html
    assert "display:none" in html
    assert "name,age,city" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_javascript(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable()

    assert "<script" in html
    assert "$(document).ready" in html
    assert "parseCsv_" in html
    assert "</script>" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_with_index(sample_df_with_index):
    dt = DataTable(sample_df_with_index, "test_table", index=True)
    html = dt.create_datatable()

    assert "<th></th>" in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_create_datatable_javascript_function(sample_df):
    dt = DataTable(sample_df, "test_table")
    js = dt.create_javascript_function()

    assert "<script" in js
    assert "Papa.parse" in js
    assert "</script>" in js


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_multiple_tables_same_function(sample_df):
    dtf = DataTableFunction(sample_df, "shared_function")
    dtf.datatable_options = {"pageLength": 20}

    dt1 = DataTable(sample_df, "table1", datatable=dtf)
    dt2 = DataTable(sample_df, "table2", datatable=dtf)

    assert dt1.datatable is dt2.datatable
    assert dt1.datatable.datatable_options["pageLength"] == 20


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_csv_generation(sample_df):
    dt = DataTable(sample_df, "test_table")
    html = dt.create_datatable()

    csv_content = sample_df.to_csv(index=False)
    for line in csv_content.strip().split('\n'):
        assert line in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_datatable_csv_with_index_false(sample_df):
    dt = DataTable(sample_df, "test_table", index=False)
    html = dt.create_datatable()

    csv_content = sample_df.to_csv(index=False)
    csv_with_index = sample_df.to_csv(index=True)

    assert csv_content.strip() in html
    assert csv_with_index not in html


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_coloption_2_str_without_options(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    result = dtf._coloption_2_str("name", {})

    assert "data:'name'" in result


@pytest.mark.skipif(pd is None, reason="pandas not available")
def test_coloption_2_str_with_options(sample_df):
    dtf = DataTableFunction(sample_df, "test_table")
    result = dtf._coloption_2_str("name", {"visible": "false"})

    assert "data:'name'" in result
    assert "visible:false" in result
