# Skeleton code for logic
from settings import CelonisConnection, DataExtraction, MATCH_COLUMNS
from core import connect
from core.extract import get_data_model_table, extract_data
from pycelonis.config import Config

#Establish connection and get the datamodel
celonis = connect.connect(CelonisConnection.CELONIS_BASE_URL, CelonisConnection.CELONIS_API_TOKEN, CelonisConnection.CELONIS_APP_KEY)
data_model = connect.get_data_model(celonis, CelonisConnection.DATA_POOL_ID, CelonisConnection.DATA_MODEL_ID)

#Get the relevant object tables
group_object_table = get_data_model_table(data_model, DataExtraction.GROUP_OBJECT_TABLE_NAME)
object_table = get_data_model_table(data_model, DataExtraction.OBJECT_TABLE_NAME)

#Get the data
group_object_df = extract_data(group_object_table)
object_df = extract_data(object_table)

#Set the index as the ID
object_df.set_index('ID')

#Set of object ids
object_ids = set(object_df['ID'])



