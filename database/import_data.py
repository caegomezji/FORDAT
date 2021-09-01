import pandas as pd
from pandas.io.pytables import Selection

if __name__ == '__main__':
    import sys
    import os
    sys.path.append(os.path.abspath('../'))
    
       
from database.database_manager import connect_db



def validate_data(data : pd.DataFrame):
    """Validando que las columnas que se van a ingresar a la base de datos coincidan y no genere daños a la base de datos"""
    assert len(data.columns) == 8 , "las columnas no coinciden"
    assert (data.columns == ["Cadena","Sector","Subsector","FOBDOL","Date","CodeCountry","Country","Empresa"]).all() ,  "Las Columnas no coinciden!!"


def check_if_not_repeted(row):
    """Se revisa que no haya data repetida"""
    
    sql = """
    SELECT * from FORDAT 
    WHERE 
    Cadena = %s 
    AND Sector = %s 
    AND Subsector = %s 
    AND FOBDOL = %s 
    AND Date = %s 
    AND CodeCountry = %s 
    AND Country = %s 
    AND Empresa = %s 
    """
    
    cur = conn.cursor()
    cur.execute(sql , list(row) )
    print(cur.fetchall())
    assert 0 == len(cur.fetchall())
   
     
    
def insert(row):
 
    
    try:         
        check_if_not_repeted(row)
        
        query = """
        INSERT INTO fordat (Cadena,Sector,Subsector,FOBDOL,Date,CodeCountry,Country,Empresa) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """  
        cur = conn.cursor()
        cur.execute(query , list(row))
        conn.commit()
    except Exception:
        print("Repeted")





def import_data(data : pd.DataFrame):
    
    validate_data(data)
    
    data.apply(lambda row : insert(row), axis=1)
    
    
    
    
    
if __name__ == '__main__':
    conn  = connect_db()

    df = pd.read_pickle('../base_datos_corregida.pkl')
    filteredData = df[["Cadena 2020","Sector 2020","Subsector 2020","FOBDOL","Year_month","COD_PAI4","Destination country","RAZ_SIAL"]].copy()
    filteredData.dropna(inplace=True)
    filteredData.columns = ["Cadena","Sector","Subsector","FOBDOL","Date","CodeCountry","Country","Empresa"]
    # transforming date in due format
    filteredData["Date"] = pd.to_datetime(filteredData["Date"], format="%Y-%m-%d")

    import_data(filteredData)
    