from saolapy.pql.base import PQLColumn, PQLFilter

class CelonisConnection:
    CELONIS_API_TOKEN = None
    CELONIS_BASE_URL = None
    CELONIS_APP_KEY = None
    DATA_POOL_ID = None
    DATA_MODEL_ID = None
    
class DataExtraction:
    OBJECT_TABLE_NAME = None #Table name of the object you want to find dupluicates for e.g. "o_celonis_Invoice"
    GROUP_OBJECT_TABLE_NAME = None #The table name of the object you created to represent groups of duplicates
    ADDITIONAL_COLUMNS = [] #Add additional columns to your object table extraction by writing pql queries 
    FILTERS = [] #Define additional filters based on your business requirements

class DuplicateLogic:
    COLUMNS = [] #These are the columns the matching algorithm should use to create duplicate groups
    MAX_NON_EXACT_MATCHES = 1
    


