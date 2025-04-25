from pycelonis.ems.data_integration.data_pool import DataPool
from pycelonis.ems.data_integration.job import Job
from pycelonis.ems.data_integration.task import Task
from pycelonis.service.data_ingestion.service import ColumnTransport, ColumnType
from pandas import DataFrame

def create_column_config(df) -> list[ColumnTransport]:
    ...

#TODO: Add error handling
def upload_duplicate_groups_table(data_pool:DataPool, df:DataFrame, target_table:str) -> None:
    column_config = create_column_config(df)

    temp_table = data_pool.create_table(
        df=df,
        table_name=f'{target_table}_tmp',
        column_config=column_config,
    )

    job = data_pool.create_job(f'Update {target_table} in OCPM Schema')
    transformation = job.create_transformation(f'Update {target_table} in OCPM Schema')
    transformation.update_statement(
        f"""
        DROP TABLE <%=BUSINESS_SCHEMA%>."{target_table}";
        CREATE TABLE <%=BUSINESS_SCHEMA%>."{target_table}" FROM(
            SELECT * FROM {temp_table.name}
        );
        DROP TABLE {temp_table.name};
        """
    )

    job.execute()
    job.delete()