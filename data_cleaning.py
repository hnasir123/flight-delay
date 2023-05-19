def clean_fuel_df(filepath):
    '''
    Given local filepath of fuel_consumption.csv, imports and cleans  file, then returns final dataframe. 
    '''

    import pandas as pd
    
    # import data
    fuel_cols = ['month', 'airline_id', 'unique_carrier', 'carrier', 'carrier_name', 'carrier_group_new', 'sdomt_gallons', 'satl_gallons', 'spac_gallons', 'slat_gallons', 'sint_gallons', 'ts_gallons', 'tdomt_gallons', 'tint_gallons', 'total_gallons', 'sdomt_cost', 'satl_cost', 'spac_cost', 'slat_cost', 'sint_cost', 'ts_cost', 'tdomt_cost', 'tint_cost', 'total_cost', 'year']
    fuel_df = pd.read_csv(filepath, header=None, names=fuel_cols)

    # First row missing values can be matched to row beneath it
    fuel_df.iloc[0,2] = '0JQ'
    fuel_df.iloc[0,1] = 21236
    fuel_df.iloc[0,4] = 'Vision Airlines'

    # calculate missing tint_cost
    fuel_df['tint_cost'].fillna(value=(fuel_df['total_cost'] - fuel_df['tdomt_cost']), inplace=True)

    # calculate missing total_gallons
    fuel_df['total_gallons'].fillna(value=(fuel_df['tdomt_gallons'] + fuel_df['tint_gallons']), inplace=True)

    # calculate missing tdomt_gallons
    fuel_df['tdomt_gallons'].fillna(value=(fuel_df['total_gallons'] - fuel_df['tint_gallons']), inplace=True)

    # drop remaining rows with null values.
    fuel_df.dropna(inplace=True)

    # drop unneeded columns
    fuel_df.drop(columns=['carrier', 'carrier_name'])
    return fuel_df



def clean_passengers_df(filepath):
    '''
    Given local filepath of passengers.csv, imports and cleans  file, then returns final dataframe. 
    '''

    import pandas as pd

    # import data
    passenger_cols = ['departures_scheduled', 'departures_performed', 'payload', 'seats', 'passengers', 'freight', 'mail', 'distance', 'ramp_to_ramp', 'air_time', 'unique_carrier', 'airline_id', 'unique_carrier_name', 'region', 'carrier', 'carrier_name', 'carrier_group', 'carrier_group_new', 'origin_airport_id', 'origin_city_market_id', 'origin', 'origin_city_name', 'origin_country', 'origin_country_name', 'dest_airport_id', 'dest_city_market_id', 'dest', 'dest_city_name', 'dest_country', 'dest_country_name', 'aircraft_group', 'aircraft_type', 'aircraft_config', 'year', 'month', 'distance_group', 'class', 'data_source']
    passengers_df = pd.read_csv(filepath, header=None, names=passenger_cols)

    # fill in missing country code for Namibia
    passengers_df['origin_country'].fillna(passengers_df['origin_country_name'].map({'Namibia': 'NA'}), inplace=True)

    # drop unneeded columns
    passengers_df = passengers_df.drop(columns=['data_source'])
    return passengers_df


def clean_flights_df(filepath):
    '''
    Given local filepath of flights.csv, imports and cleans  file, then returns final dataframe. 
    '''

    import pandas as pd

    # import data
    flights_df = pd.read_csv(filepath)

    flights_df['fl_date'] = pd.to_datetime(flights_df['fl_date'], errors='coerce')
    flights_df['year'] = flights_df['fl_date'].dt.year
    flights_df['month'] = flights_df['fl_date'].dt.month
    flights_df['day_of_month'] = flights_df['fl_date'].dt.day
    flights_df['day_of_week'] = flights_df['fl_date'].dt.dayofweek
    flights_df['dep_hour'] = flights_df['crs_dep_time'] // 100
  

    # drop useless columns
    flights_df.drop(columns=['fl_date', 'branded_code_share','mkt_carrier_fl_num','tail_num','op_carrier_fl_num', 'origin_airport_id','origin_city_name','dest_airport_id','dest_city_name','wheels_off', 'wheels_on','cancelled', 'air_time', 'flights','carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay', 'first_dep_time','total_add_gtime', 'longest_add_gtime',], inplace=True)
    return flights_df



def avg_passengers(flights_df, passengers_df):
    '''
    Adds column to flights_df: 'monthly_avg_passengers' - the average number of passengers per month on that route.
    '''
    
    import pandas as pd

    # find averages from passengers_df
    passengers_df['route'] = passengers_df['origin'] + ' to ' + passengers_df['dest']
    route_month_avg_dict = round(passengers_df.groupby(['route', 'month'])['passengers'].mean(), 0).to_dict()


    # create route and mapping columns on flights_df
    flights_df['route'] = flights_df['origin'] + ' to ' + flights_df['dest']
    flights_df['map_key'] = list(zip(flights_df['route'], flights_df['month']))

    # map averages into new column then delete route and map columns
    flights_df['monthly_avg_passengers'] = flights_df['map_key'].map(route_month_avg_dict)
    flights_df.drop(columns=['route', 'map_key'], inplace=True)

    return flights_df 


def avg_fuel_use(flights_df, fuel_df):
    '''
    Adds two columns to flights_df 'avg_monthly_fuel_cost' and 'avg_monthly_fuel_gallons' - The average fuel consumption for
    that carrier for that month.
    '''

    import pandas as pd

    # find averages from fuel_df
    carrier_month_avg_gallons_dict = round(fuel_df.groupby(['unique_carrier', 'month'])['total_gallons'].mean(), 0).to_dict()
    carrier_month_avg_cost_dict = round(fuel_df.groupby(['unique_carrier', 'month'])['total_cost'].mean(), 0).to_dict()

    # create mapping column on flights_df
    flights_df['map_key'] = list(zip(flights_df['mkt_unique_carrier'], flights_df['month']))

    # map averages into new columns then delete map_key column
    flights_df['avg_monthly_fuel_gallons'] = flights_df['map_key'].map(carrier_month_avg_gallons_dict)
    flights_df['avg_monthly_fuel_cost'] = flights_df['map_key'].map(carrier_month_avg_cost_dict)
    flights_df.drop(columns='map_key', inplace=True)

    return flights_df


def import_flights_test(filepath):
    import pandas as pd
    
    col_names = ['fl_date', 'mkt_unique_carrier', 'branded_code_share', 'mkt_carrier', 'mkt_carrier_fl_num', 'op_unique_carrier', 'tail_num', 'op_carrier_fl_num', 'origin_airport_id', 'origin', 'origin_city_name', 'dest_airport_id', 'dest', 'dest_city_name', 'crs_dep_time', 'crs_arr_time', 'dup', 'crs_elapsed_time', 'flights', 'distance']
    flights_test = pd.read_csv(filepath, header=None, names=col_names)

    return flights_test



# These two functions actually need to be applied manually to the training data so the dictionaries can be used
# again to map onto the test data without recalculating averages.

def avg_carrier_arr_delay(flights_df):
    '''
    Given flights_df dataframe, calculate the average arrival delay for each op carrier. Add this column to dataframe.
    '''
    import pandas as pd
    avg_carrier_arr_delay_dict = round(flights_df.groupby('op_unique_carrier')['arr_delay'].mean(), 2).to_dict()
    flights_df['avg_carrier_arr_delay'] = flights_df['op_unique_carrier'].map(avg_carrier_arr_delay_dict)

    return flights_df


def avg_taxi_time(flights_df):
    '''
    Given flights_df dataframe, calculate the average taxi time for each hour. Add taxi_dep_mean_time and
    taxi_arr_mean_time columns to dataframe.
    '''
    import pandas as pd
    # Convert 'dep_time' and 'arr_time' to datetime format
    flights_df['dep_time'] = pd.to_datetime(flights_df['dep_time'], format='%H%M', errors='coerce')
    flights_df['arr_time'] = pd.to_datetime(flights_df['arr_time'], format='%H%M', errors='coerce')

    # Calculate mean taxi time per hour
    flights_df['taxi_dep_mean_time'] = round(flights_df.groupby(flights_df['dep_time'].dt.hour)['taxi_out'].transform('mean'), 2)
    flights_df['taxi_arr_mean_time'] = round(flights_df.groupby(flights_df['arr_time'].dt.hour)['taxi_in'].transform('mean'), 2)

    return flights_df