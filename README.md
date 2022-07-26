# About the Project

## Project Goal

###  The goal of this project is to identify the drivers that determine the price of single family properties by constructing an ML Regression model. 

## Project Description

### The cost of living and inflation is on the rise. The price of rent is also increasing and there is higher demand to purchase a home more than ever. Buyers want to find the home that works best for them. Location and home features can impact the value of the home. We will analayze data of homes that were purchased in the year 2017 from Zillow. The data will be helpful to  determine factors that impact the value of a home. 

## Initial Questions

### - Does square footage (continuous variable) factor into the home value (continuous variable)?


### - Does the lot size (continuous variable) help impact the home value (continuous variable)?


### - Does having features like a garage size, pool, fire place, spa or hot tub (categorical variable) increase the home value (continuous variable)?


### - Does location (categorical variable) of a home impacts the home value (continuous variable)?

## Data Dictionary

|   Variable     |                  Meaning                   |
| -------------- | ------------------------------------------ |
| year           | The year the home was built                |
| home_value     | The total tax assessed value of the parcel |
| squarefeet     | The total square feet of a home            |
| lot_size       | The total square feet of a property lot    |
| fips           | Location of a home by county code          |
| bedrooms       | The total number of bedrooms in a home     |
| bathrooms      | The total number of bathrooms in a home    |
| hashottuborspa | Is there a hot tub or spa in home          |
| garagecarcount | The total number of car slots in a garage  |
| fireplace      | Is there a fireplace in home               |
| pool           | Is there a home pool                       |
| fips_encoded   | The location of a home by county, encoded  |
| home_age       | The age of the home since year built       |


## Steps to Reproduce

### The Plan
- Acquire the data
- Wrangle (prepare and clean) the data
- Split the data into three samples: `train`, `validate`, and `test`
- Conduct exploration of `train` sample and find relationships in data by plotting visuals and statistical testing
- Scale the `train` sample to normalize the values prior to modeling. Will transform `validate` and `test` samples also
- Generate model predictions by fitting models to only the scaled `train` and `validate` samples to avoid data leakage into `test` sample
- Evaluate the performance of the models with root mean square error (RMSE) calculation and pick the best performing model
- Evaluate the performance of best model.
- Draw conclusion


### Acquistion of zillow family home data

To acquire the zillow home data, I used the zillow_db in our mySQL server using the query below. 

"""

            select yearbuilt, taxvaluedollarcnt, calculatedfinishedsquarefeet, lotsizesquarefeet, fips, regionidzip, bedroomcnt, bathroomcnt,hashottuborspa, garagecarcnt, fireplacecnt,poolcnt
            from properties_2017 
            left join propertylandusetype  using (propertylandusetypeid)
            left join airconditioningtype  using (airconditioningtypeid)
            left join buildingclasstype  using (buildingclasstypeid)
            left join architecturalstyletype  using (architecturalstyletypeid)
            right join predictions_2017  using (parcelid)
            where propertylandusedesc = 'Single Family Residential'
            and predictions_2017.transactiondate like "2017%%";
                
                """

- Should acquire Raw dataset that has 52441 rows and  12 columns
- The query will bring results with null values

### Preparation of data

To clean the data I did the following things in order

- review the details of the data to counts on non null values and data types per column. Use code df.info(show_counts=True)
-  `poolcnt` filled null values with 0 
-  `garagecarcnt` filled null values with 0
-  `fireplacecnt` filled null values with 0
-  `hashottuborspa` filled null values with 0
-  Drop all records that had null values. 488 records was dropped. Equivalent to .01% of acquired data.
- Refined dataset has 51953 rows and  12 columns after dropping null values after filling in below columns null values with '0'
- Convert columns `yearbuilt`, `bedroomcnt`, `fireplacecnt`, `fips`, `regionzip`, `garagecarcnt`, `poolcnt`, `hashottuborspa` to integer
- Drop column `regionidzip` from data. determined not needed at point of time. would incorpate in future modeling
-  Rename columns   'yearbuilt':'year', 'taxvaluedollarcnt':'home_value', 'calculatedfinishedsquarefeet':'squarefeet', 'lotsizesquarefeet':'lot_size', 'bedroomcnt':'bedrooms', 'bathroomcnt':'bathrooms', 'fireplacecnt':'fireplace', 'poolcnt':'pool'
- Encoded `fips` to help normalize my data through mapping. 6059: 2, 6037: 1, 6111: 3
- Added `home_age` to dataset by subtracting the `year` from 2017 since data acquired is from the year 2017.

### Split the data

To split the data

- Split the refined dataframe into 3 samples using the train_test_split function from sklearn.model_selection using a random seed of "123"

### Scale the `train` sample and transform other samples using RobustScaler

-  Create function with columns to scale with code scale_columns = [ 'squarefeet', 'lot_size', 'bedrooms', 'bathrooms','garagecarcnt', 'fips_encoded', 'home_age' ]
-   made copy of each sample train_scaled = train.copy() , validate_scaled = validate.copy() , test_scaled = test.copy()
-  imported  sklearn.preprocessing.RobustScaler() as rbs
-  fit scaler object to `train` with code rbs.fit(train[scale_columns])
- transformed other samples with code :
    -  train_scaled[scale_columns] = rbs.transform(train[scale_columns])
    - validate_scaled[scale_columns] = rbs.transform(validate[scale_columns])
    - test_scaled[scale_columns] = rbs.transform(test[scale_columns])


### Make X_train and y_train

- Create x_train by using scaled train sample using code:
     - X_train = train_s.drop(columns=['home_value', 'fips', 'year'])

- Create y-train by using target variable only
     - y_train = train.home_value

### Modeling the data and evaluating which model performs the best on scaled `train` and `validate` samples
- from sklearn.linear_model import LinearRegression, LassoLars, TweedieRegressor 
- Create prediction DataFrames with the actual home value of `train`  and  home value baseline prediction by using the mean of the `home_value` in `train` sample
- Create prediction DataFrames with the actual home value of `validate` and  home value baseline prediction by using the mean of the `home_value` in `train` sample
- Create model object and fit model to `x_train` and ` y_train`
- Use the model object to make prediction on both scaled `train` and `validate` samples by omitting columns 'home_value', 'fips', 'year'.
- Add model predictions to both prediction dataframes created earlier
- Evaluate the performce of the models by using root mean square error (RMSE) on the predictions using similar code:
    - from scipy import stats
    - from math import sqrt
    - from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
    - train_s_rmse = sqrt(mean_squared_error(home_value_mean['home_value'], home_value_mean.baseline))

    - def calculate_rmse(t):
        return sqrt(mean_squared_error(home_value_mean['home_value'], t))

    - print('Train baseline RMSE: {}.'.format(train_s_rmse))
    - home_value_mean.apply(calculate_rmse).sort_values()
- Review the results and pick the model with the lowest RMSE to run on scaled `test` sample

### Running best model on scaled `test` sample

- Create prediction DataFrame with the actual home value of `train`  and  home value baseline prediction by using the mean of the `home_value` in `train` sample
- Use the model object to make prediction on  scaled `test`  samples by omitting columns 'home_value', 'fips', 'year'.
- Add model predictions to both prediction dataframes created earlier
- Evaluate the performce of the models by using root mean square error (RMSE) on the predictions using similar code:
    - from scipy import stats
    - from math import sqrt
    - from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
    - train_s_rmse = sqrt(mean_squared_error(home_value_mean['home_value'], home_value_mean.baseline))

    - def calculate_rmse(t):
        return sqrt(mean_squared_error(home_value_mean['home_value'], t))

    - print('Train baseline RMSE: {}.'.format(train_s_rmse))
    - home_value_mean.apply(calculate_rmse).sort_values()
- Review the results of model performance on scaled `test` sample

### Conclusion

- Summary of the project
    - After creating three Regression models, the top performing model is LinearRegression (OLS). It beat the baseline prediction (home value average) by $107,522.44. It has an prediction error of $507729.22
We know square feet, location and added features to the home impact the value of the home.

- Recommendation
    - To acquire more recent family home data to get a more accurate prediction since the housing market has change since 2017.
    - Incorporate a cost of living index possible. I believe cost of living impacts the value of the home.

- Next Steps
    - Create submodels to predict home value buy zipcode to get more accurate predictions
    - Do feature enginering to create new feature to incorparate in the model.

