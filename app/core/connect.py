from pycelonis import get_celonis
from pycelonis.celonis import Celonis
from pycelonis.ems.data_integration.data_model import DataModel

def connect(base_url:str, api_token:str, app_key:str)->Celonis:
    celonis = get_celonis(base_url, api_token, app_key)
    return celonis

def get_data_model(celonis:Celonis, data_pool_id:str, data_model_id:str) -> DataModel:
    return celonis.data_integration.get_data_pool(
        data_pool_id
    ).get_data_model(
        data_model_id
    )
