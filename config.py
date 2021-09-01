import os

from dotenv import load_dotenv
load_dotenv(override=True) 

app_name = os.getenv('APP_NAME' , 'FORDAT') 

app_host =  os.getenv('APP_HOST' , 'localhost')
app_port = os.getenv('APP_PORT' , '8050')

app_debug = os.getenv('APP_DEBUG' , 'FORDAT') 
app_env = os.getenv('APP_ENV' , 'FORDAT') 


db_name = os.getenv('DB_NAME' , 'fordat')
db_user = os.getenv('DB_USER' , 'postgres')
db_host = os.getenv('DB_HOST' , 'localhost')
db_port = os.getenv('DB_PORT' , '5432')
db_password = os.getenv('DB_PASSWORD' , '')
db_schema = os.getenv('DB_SCHEMA' , '')

kernels=os.getenv("SERVER_KERNELS" , 1)
