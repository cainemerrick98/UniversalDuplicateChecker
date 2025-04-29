from pycelonis import get_celonis
from pycelonis.celonis import Celonis
from pycelonis.ems.data_integration.data_model import DataModel

def connect(base_url:str, api_token:str, app_key:str)->Celonis:
    celonis = get_celonis(base_url, api_token, app_key)
    return celonis