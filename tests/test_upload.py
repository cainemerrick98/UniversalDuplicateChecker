from tests.test_data.test_groups import groups
from pandas import DataFrame
from app.core.upload import (
    create_data_model_dfs_from_groups
)

def test_output_of_create_data_model_dfs():
    output = create_data_model_dfs_from_groups(groups, {'object':'OBJECT_ID', 'group':'GROUP_ID'})

    assert isinstance(output, tuple)
    assert isinstance(output[0], DataFrame)
    assert isinstance(output[1], DataFrame)
    assert ['ID', 'Pattern'] == output[0].columns.to_list()
    assert ['OBJECT_ID', 'GROUP_ID'] == output[1].columns.to_list()
    assert len(output[0]) < len(output[1])
    
    
