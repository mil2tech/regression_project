from pandas import DataFrame
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import acquire

def prep_familyhome17():
    df = acquire.new_familyhome17_data()
    df["poolcnt"].fillna(0, inplace = True)
    df["garagecarcnt"].fillna(0, inplace = True)
    df["fireplacecnt"].fillna(0, inplace = True)
    df["hashottuborspa"].fillna(0, inplace = True)
    df.dropna(inplace=True)
    df['yearbuilt'] = df.yearbuilt.astype(int)
    df['fips'] = df.fips.astype(int)
    df['regionidzip'] = df.regionidzip.astype(int)
    df['bedroomcnt'] = df.bedroomcnt.astype(int) 
    df['hashottuborspa'] = df.hashottuborspa.astype(int)
    df['garagecarcnt'] = df.garagecarcnt.astype(int)
    df['fireplacecnt'] = df.fireplacecnt.astype(int)
    df['poolcnt'] = df.poolcnt.astype(int)
    df.drop('regionidzip', axis=1, inplace=True)
    return df

