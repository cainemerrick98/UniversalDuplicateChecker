# Skeleton code for logic
from settings import CelonisConnection, DataExtraction, DuplicateLogic
from core import connect
from core.extract import get_data_model_table, extract_data
from core.duplicate_checker import DuplicateChecker
from pycelonis.config import Config

#Establish connection and get the datamodel
celonis = connect.connect(CelonisConnection.CELONIS_BASE_URL, CelonisConnection.CELONIS_API_TOKEN, CelonisConnection.CELONIS_APP_KEY)
data_model = connect.get_data_model(celonis, CelonisConnection.DATA_POOL_ID, CelonisConnection.DATA_MODEL_ID)

#Get the relevant object tables
group_object_table = get_data_model_table(data_model, DataExtraction.GROUP_OBJECT_TABLE_NAME)
object_table = get_data_model_table(data_model, DataExtraction.OBJECT_TABLE_NAME)

#Get the data
group_object_df = extract_data(group_object_table)
object_df = extract_data(object_table)#TODO: object df index must be ID column for script to work correctly

#Loop through patterns - finding groups
duplicate_checker = DuplicateChecker(object_df)
found_groups = set()
found_groups_with_pattern_name = set()
for pattern_name, pattern in DuplicateLogic.SEARCH_PATTERNS.items():
    groups = duplicate_checker.find_duplicates(pattern_name, pattern)
    for group in groups:
        if group not in found_groups:
            found_groups.add(group)
            found_groups_with_pattern_name.add((group, pattern_name))
    
    
    



