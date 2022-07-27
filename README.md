# About the Project

## Project Goal

###  The goal of this project is to identify the drivers that determine the price of single family properties by constructing an ML Regression model. 

## Project Description

### The cost of living and inflation is on the rise. There is more a demand to purchase a home.

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
- Wrangle the data
- Split the data into three samples: `train`, `validate`, and `test`
- Conduct exploration of `train` sample and find relationships in data by plotting visuals and statistical testing
- Scale the `train` sample to normalize the values prior to modeling. Will transform `validate` and `test` samples also
- Generate model predictions by fitting models to only the scaled `train` and `validate` samples to avoid data leakage into `test` sample
- Evaluate the performance of the models with root mean square error (RMSE) calculation

### Acquistion of zillow family home data

To acquire the zillow home data, I used the zillow_db in our mySQL server, and selected all columns from the customers, contract_types, internet_service, and payment_types table. 

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

### Preparation of data

