from pandas import DataFrame
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import sklearn.preprocessing
from sklearn.preprocessing import MinMaxScaler, StandardScaler, RobustScaler
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
    df.rename(columns = {'yearbuilt':'year', 'taxvaluedollarcnt':'home_value', 'calculatedfinishedsquarefeet':'squarefeet', 'lotsizesquarefeet':'lot_size', 'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'fireplacecnt':'fireplace', 'poolcnt':'pool'}, inplace = True)
    df['fips_encoded'] = df.fips.map({6059: 2, 6037: 1, 6111: 3,})
    df['home_age'] = 2017 - df.year
    return df

# split  data into train test and validate samples

def split_familyhome17(df):
    train, test = train_test_split(df, test_size=.2, random_state=123)
    train, validate = train_test_split(train, test_size=.3, random_state=123)
    return train, validate, test



# Scale the data samples

def scale_data(train, validate, test):
    
    scale_columns = [ 'squarefeet', 'lot_size', 'bedrooms', 'bathrooms','garagecarcnt', 'fips_encoded', 'home_age' ]
    
    train_scaled = train.copy()
    validate_scaled = validate.copy()
    test_scaled = test.copy()
    
    rbs = RobustScaler()
    
    rbs.fit(train[scale_columns])
    
    train_scaled[scale_columns] = rbs.transform(train[scale_columns])
    validate_scaled[scale_columns] = rbs.transform(validate[scale_columns])
    test_scaled[scale_columns] = rbs.transform(test[scale_columns])
    
    return train_scaled, validate_scaled, test_scaled


# Create x and y train
#def create_x_y_train():
    # drop target variable and encoded variable from train sample 
   # X_train = train_s.drop(columns=['home_value', 'fips', 'year'])
    
    # dataframe with the target variable only
    #y_train = train.home_value
    #return X_train, y_train


