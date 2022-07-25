import pandas as pd
import numpy as np
import os

import env

from env import host, user, password

def get_db_url(db):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_familyhome17_data():
    '''
    This function reads the telco data from the Codeup db into a df.
    '''
    sql_query = """
            SELECT yearbuilt, taxvaluedollarcnt, calculatedfinishedsquarefeet, lotsizesquarefeet, fips, regionidzip, bedroomcnt, bathroomcnt,hashottuborspa, garagecarcnt, fireplacecnt,poolcnt
FROM properties_2017 
LEFT JOIN propertylandusetype  USING (propertylandusetypeid)
LEFT JOIN airconditioningtype  USING (airconditioningtypeid)
LEFT JOIN buildingclasstype  USING (buildingclasstypeid)
LEFT JOIN architecturalstyletype  USING (architecturalstyletypeid)
RIGHT JOIN predictions_2017  USING (parcelid)
WHERE propertylandusedesc = 'Single Family Residential'
AND predictions_2017.transactiondate LIKE "2017%%";
"""
    
    # Read in DataFrame from Codeup db.
    df = pd.read_sql(sql_query, get_db_url('zillow'))
    
    return df

def get_familyhome17_data():
    '''
    This function reads in zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('family_home_2017.csv'):
        
        # If csv file exists read in data from csv file.
        df = pd.read_csv('family_home_2017.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame
        df = new_familyhome17_data()
        
        # Cache data
        df.to_csv('family_home_2017.csv')
        
    return df