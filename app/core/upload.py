from pycelonis.ems.data_integration.data_pool import DataPool
from pycelonis.ems.data_integration.job import Job
from pycelonis.ems.data_integration.task import Task
from pycelonis.service.data_ingestion.service import ColumnTransport, ColumnType
from pandas import DataFrame

def create_column_config(df) -> list[ColumnTransport]:
    ...

def create_data_model_dfs_from_groups(groups:set[tuple], 
                                      relationship_table_columns:dict[str:str], groups_table_columns:list[str]=['ID', 'Pattern']):
    """
    tuple is ids in group, pattern name, group_id

    this function needs to create two dataframes

    1. groups table
    2. relationships table (M:N)

    return tuple of (groups table, relationship table)
    """
    relationship_table = {col:[] for col in relationship_table_columns.values()}
    duplicate_group_table = {col:[] for col in groups_table_columns}

    for group in groups:
        object_ids, pattern_name, group_id = group

        #Update dupe group data
        duplicate_group_table['ID'].append(group_id)
        duplicate_group_table['Pattern'].append(pattern_name)

        #Update relationship data
        for id_ in object_ids:
            relationship_table[relationship_table_columns['object']].append(id_)
            relationship_table[relationship_table_columns['group']].append(group_id)
    

    #Create dataframes
    duplicate_group_df = DataFrame(data=duplicate_group_table)
    relationship_df = DataFrame(data=relationship_table)

    return duplicate_group_df, relationship_df


#TODO: Add error handling
def add_dupe_group_relationships_tables_to_data_model(data_pool:DataPool, 
                                                      relationships_table:DataFrame, relationships_table_name:str, 
                                                      duplicate_group_table:DataFrame, duplicate_group_table_name:str) -> None:
    #Create configs
    reltionship_column_config = create_column_config(reltionship_column_config)
    duplicate_group_column_config = create_column_config(duplicate_group_table)

    #Create temp_tables
    temp_relationship_table = data_pool.create_table(
        df=relationships_table,
        table_name=f'{relationships_table_name}_tmp',
        column_config=reltionship_column_config,
    )
    temp_duplicate_group_table = data_pool.create_table(
        df=duplicate_group_table,
        table_name=f'{duplicate_group_table_name}_tmp',
        column_config=duplicate_group_column_config,
    )

    job = data_pool.create_job(f'Update duplicate group and relationship table in OCPM Schema')
    transformation = job.create_transformation(f'transformation')
    
    #TODO: is <%-BUSINESS_GRPAH_SCHEMA%> okay here?
    transformation.update_statement(
        f"""
        DROP TABLE <%=BUSINESS_SCHEMA%>."{relationships_table_name}";
        DROP TABLE <%=BUSINESS_SCHEMA%>."{duplicate_group_table}";

        CREATE TABLE <%=BUSINESS_SCHEMA%>."{relationships_table_name}" FROM(
            SELECT * FROM {temp_relationship_table.name}
        );
        CREATE TABLE <%=BUSINESS_SCHEMA%>."{duplicate_group_table_name}" FROM(
            SELECT * FROM {temp_duplicate_group_table.name}
        );

        DROP TABLE {temp_relationship_table.name};
        DROP TABLE {temp_duplicate_group_table.name};
        """
    )

    job.execute()
    job.delete()

    return