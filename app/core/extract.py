from pycelonis.ems.data_integration.data_model import DataModel
from pycelonis.ems.data_integration.data_model_table import DataModelTable
from pycelonis.ems.data_integration.data_model_table_column import DataModelTableColumn
from pandas import DataFrame
from saolapy.pql.base import PQL, PQLColumn, PQLFilter
import pycelonis.pql as pql

def get_data_model_table(data_model:DataModel, table_name:str) -> DataModelTable:
    tables = data_model.get_tables()
    table = [t for t in tables if t.name == table_name]
    if len(table) == 0:
        raise ValueError(f'Table: {table_name} not found in DataModel: {data_model.id}')
    elif len(table) > 1:
        raise ValueError(f'Table name must be unique. {len(table)} matches found for Table: {table_name} in DataModel: {data_model.id}')
    else:
        return table[0]

def extract_data(data_model_table:DataModelTable) -> DataFrame:
    columns = data_model_table.get_columns()
    query = build_pql_query(columns) #TODO: Add filters
    return pql.DataFrame.from_pql(
        query=query
    ).to_pandas()
    

def build_pql_query(columns:list[PQLColumn|DataModelTableColumn], filters:list[PQLFilter]=[]):
    query = PQL()
    for col in columns:
        if isinstance(col, DataModelTableColumn):
            col = data_model_table_column_to_pql_column(col)
        query += col
    
    for fil in filters:
        query += fil 

    return query
    
def data_model_table_column_to_pql_column(data_model_table_column:DataModelTableColumn)->PQLColumn:
    query = f'"{data_model_table_column.table_name}"."{data_model_table_column.name}"'
    return PQLColumn(name=data_model_table_column.name, query=query)
