from app.core import extract
from pydantic import BaseModel
import pytest
from saolapy.pql.base import PQL, PQLColumn, PQLFilter

class Table(BaseModel):
    name: str

class DataModelTableColumn(BaseModel):
    table_alias:str|None
    table_name:str
    name:str


def test_extract_table_success(mocker):
    mock_data_model = mocker.Mock()
    mock_data_model.get_tables.return_value = [
        Table(name='table_1'),
        Table(name='table_2')
    ]
    table = extract.get_data_model_table(mock_data_model, 'table_1')

    assert hasattr(table, 'name')
    assert table.name == 'table_1'

def test_extract_table_failure(mocker):
    mock_data_model = mocker.Mock()
    mock_data_model.get_tables.return_value = [
        Table(name='table_1'),
        Table(name='table_2')
    ]

    with pytest.raises(ValueError):
        table = extract.get_data_model_table(mock_data_model, 'table_3')

def test_data_model_table_column_to_pql_column():
    data_model_table_column = DataModelTableColumn(table_alias=None, table_name="Table1", name="Column1")
    expected_pql_column = PQLColumn(name="Column1", query='"Table1"."Column1"')
    output_pql_column = extract.data_model_table_column_to_pql_column(data_model_table_column)
    
    assert expected_pql_column.name == output_pql_column.name
    assert expected_pql_column.query == output_pql_column.query

def test_data_model_table_column_to_pql_column_with_alias():
    data_model_table_column = DataModelTableColumn(table_alias='T1', table_name="Table1", name="Column1")
    expected_pql_column = PQLColumn(name="Column1", query='"T1"."Column1"')
    output_pql_column = extract.data_model_table_column_to_pql_column(data_model_table_column)
    
    assert expected_pql_column.name == output_pql_column.name
    assert expected_pql_column.query == output_pql_column.query
    
def test_build_pql_query():
    columns = [
        PQLColumn(name='column1', query='"Table"."Column1"'),
        PQLColumn(name='column2', query='"Table"."Column2"')
    ]
    filters = [
        PQLFilter(query='FILTER "Table"."Column1">10')
    ]

    query = extract.build_pql_query(columns, filters)

    assert len(query.columns) == 2
    assert len(query.filters) == 1

def test_build_pql_query_with_data_model_table_column(mocker):

    def is_data_model_col(obj, cls):
        return isinstance(obj, DataModelTableColumn)

    mocker.patch('app.core.extract.isinstance', side_effect=is_data_model_col)
        
    columns = [
        PQLColumn(name='column1', query='"Table"."Column1"'),
        PQLColumn(name='column2', query='"Table"."Column2"'),
        DataModelTableColumn(table_alias=None, table_name="Table1", name="Column1")
    ]
    filters = [
        PQLFilter(query='FILTER "Table"."Column1">10')
    ]

    query = extract.build_pql_query(columns, filters)

    assert len(query.columns) == 3
    assert len(query.filters) == 1
    assert isinstance(query.columns[2], PQLColumn)