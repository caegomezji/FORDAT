import psycopg2
import config

def connect_db():
    DB_NAME = config.db_name
    DB_USER = config.db_user
    DB_HOST = config.db_host
    DB_PASSWORD = config.db_password
    DB_SCHEMA = config.db_schema
    
    if DB_SCHEMA == "":
        DB_SCHEMA="public"
    
    connector_string = "dbname='{0}' user='{1}' host='{2}' password='{3}' ".format ( DB_NAME , DB_USER , DB_HOST , DB_PASSWORD )

    #print(connector_string)
    conn = psycopg2.connect(connector_string , options='-c search_path={0}'.format(DB_SCHEMA) )

    #conn = psycopg2.connect("dbname='mineria_datos' user='twitter' host='192.168.73.242' password='twitter' ")
    return conn


if __name__ == '__main__':
    conn  = connect_db()
    c = conn.cursor()
    c.execute("SELECT 1")