# Flight Predictions
#### Midterm Project for Lighthouse Labs
<br><br>
## Objectives

The goal is to predict arrival delays of commercial flights. Often, there isn't much airlines can do to avoid the delays, therefore, they play an important role in both profits and loss of the airlines. It is critical for airlines to estimate flight delays as accurate as possible because the results can be applied to both, improvements in customer satisfaction and income of airline agencies.
<br><br>
## Files

- **nasir_exploratory_analysis.ipynb**: Contains EDA of the flights data.
- **nasir_modeling.ipynb**: Contains Nasir's models
- **Ben_models2.ipynb**: Contains Ben's models
- **data_cleaning.py**: Contains functions used for data cleaning and feature engineering.
- **predictions.csv**: Contains our predictions for the first week of 2020 flights using our best performing model.
- **data_description.md**: when you need to look for any information regarding specific attributes in the data this is the file to look in.
- **sample_submission.csv**: this file is the example of how the submission of the results should look like.
<br><br>
## Data

We will be working with data from air travel industry.The data comes from four separate tables stored in a Postgres Database:

1. **flights**: The departure and arrival information about flights in US in years 2018 and 2019.
2. **fuel_comsumption**: The fuel comsumption of different airlines from years 2015-2019 aggregated per month.
3. **passengers**: The passenger totals on different routes from years 2015-2019 aggregated per month.
5. **flights_test**: The departure and arrival information about flights in US in January 2020. This table will be used for evaluation. For submission, we are required to predict delays on flights from first 7 days of 2020 (1st of January - 7th of January).

<br>

## Process

1. Import the data sets from the Postgres DB
2. Data Cleaning and EDA
3. Feature Engineering Discussion
4. Sample Data
5. Encode Categorical Variables
6. Train/Test Split
7. Add Engineered Features
8. Scale/Normalize Data
9. Train and Evaluate Model (repeated for various model types)
10. Predictions Based on Best Model
<br><br>
## Feature Engineering
After an initial exploration of the data, we discussed other possible features we could engineer from the different datasets. We considered what sorts of things could potentially lead to flight delays and created several additional features to use in our modeling:
* **Average Monthly Passengers** - the average number of passengers each month on a given route.
    Our hypothesis: Flights along popular routes with more passengers may have more delays .
* **Average Monthly Fuel** - the average amount of fuel each carrier consumes each month. We calculated both the quantity in gallons and cost.
    Our hypothesis: There may be a correlation because airlines sometimes attempt to make up for delays by flying faster, hence using more fuel.
* **Average Taxi Times** - Calculated by hour, the average amount of time planes spend taxiing along the tarmac. We calculated both departure and arrival taxi times.
    Our hypothesis: Flights at times with more traffic spend more time between the gate and the air, leading to more delays.
* **Average Carrier Arrival Delay** - Calculated the average arrival delay for each operating carrier.
    Our hypothesis: Some delays are caused by staffing shortages, overbooking, or other operational issues. Airlines that have a history of longer delays will continue to have longer delays.

To ensure the integrity of our validation process, these features were added in after the train/test split. Average taxi times and delays were calculated just based on the training dataset, then mapped to the test set based on scheduled flight times. The passenger and fuel averages were calculated from separate datasets and therefore were not impacted by the train/test split. 
<br><br>
## Sampling and Model Building
Because of the large size of the flights dataset (over 15 million observations) and the limits of our resources, we were only able to work with a small fraction of the data. Our models were train on random samples of only a few hundred thousand rows.


Once we had our sample data prepared, we each selected a handful of different models to train and compare. The results of those models are below.
<br><br>
## Results
<br>

| Modeler | Model | RMSE | R^2 Score |
| ------- | ----- | ---- | --------- |
| Nasir   | SVM | 49.1 | .12 |
| Nasir   | Linear Reg| 50.75 | .064 |
| Ben     | ElasticNet| 49.13 | .014    |
| Ben     | RidgeCV| 49.16 | .014    |
| Ben     | RandomForest| 50.91 | -.058  |
| Ben     | XGBoost| 50.99 | -.061   |
| Ben     | AdaBoost| 51.59 | -.087  |
| Nasir   | AdaBoost | 149.1 | -9.33 |

<br>
As indicated by the low R^2 scores of all of our models, we were not able to producevaccurate predictions of delays. 
<br><br>

## Challenges
The biggest challenge with this project was dealing with our limited computing resources. The enormous file size of the original data set meant that it took a long time to export from the SQL database and then import into our notebooks. We tried rerunning things, chopping our samples down to smaller and smaller sizes until the operations were manageable.

As a result, our models are all built on a small subset of the data. They would likely be more accurate if we were able to train them using significantly larger datasets.

Our models also do not include weather data. This is a major factor in flight delays, but difficult to predict accurately a week in advance, so we excluded it from our feature engineering.
<br><br>
## Next Steps
Next steps in this project would be to choose different features to base our models on and look for ways to pull in other pertinent information such as weather forecasts.