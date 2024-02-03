import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    
   
    taxi_dtypes = {
                'VendorID': pd.Int64Dtype(),
                'passenger_count': pd.Int64Dtype(),
                'trip_distance': float,
                'RatecodeID':pd.Int64Dtype(),
                'store_and_fwd_flag':str,
                'PULocationID':pd.Int64Dtype(),
                'DOLocationID':pd.Int64Dtype(),
                'payment_type': pd.Int64Dtype(),
                'fare_amount': float,
                'extra':float,
                'mta_tax':float,
                'tip_amount':float,
                'tolls_amount':float,
                'improvement_surcharge':float,
                'total_amount':float,
                'congestion_surcharge':float
            }
    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']
    
    initial_month = 10
    final_month = 12
    for month in range(initial_month, final_month+1 ):
        try:
            url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{month}.csv.gz'
            if month == initial_month:
                output = output = pd.read_csv(url, sep=',', dtype=taxi_dtypes, compression='gzip', parse_dates=parse_dates)
            else:
                output = pd.concat(
                    [
                        output,
                        pd.read_csv(url, sep=',', dtype=taxi_dtypes, compression='gzip', parse_dates=parse_dates)
                    ]
                )
        except Exception as e:
            print(f'Exception: {e}')

    return output
