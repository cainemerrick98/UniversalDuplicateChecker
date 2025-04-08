import pytest
from app.core import connect

class Settings:
    CELONIS_API_TOKEN = "api_token"
    CELONIS_BASE_URL = "www.celonis.com"
    CELONIS_APP_KEY = "user_key"
    DATA_POOL_ID = "data_pool_id"
    DATA_MODEL_ID = "data_model_id"
    OBJECT_NAME = None
    GROUP_OBJECT_NAME = None

def test_connect_success(mocker):
    mock = mocker.patch('app.core.connect.get_celonis')

    mock.return_value 
    
    celonis = connect.connect(Settings.CELONIS_BASE_URL, Settings.CELONIS_API_TOKEN, Settings.CELONIS_APP_KEY)