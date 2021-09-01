import sys
import os

sys.path.append(os.path.abspath('../../'))

from database.database_manager import connect_db




def create_table():
    
    query = """
    CREATE TABLE fordat (
        id SERIAL PRIMARY KEY ,
        Cadena varchar NOT NULL,
        Sector varchar NOT NULL,
        Subsector varchar NOT NULL,
        FOBDOL double precision NOT NULL,
        Date DATE NOT NULL,
        CodeCountry varchar NOT NULL,
        Country varchar NOT NULL,
        Empresa varchar NOT NULL,
        
        UNIQUE (Cadena, Sector, Subsector , FOBDOL , Date , CodeCountry , Country , Empresa)
   )
    """  
    conn  = connect_db()
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()
    
    
if __name__ == '__main__':
    create_table()
    
