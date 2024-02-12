import io
import pandas as pd
import requests
import time

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@data_loader
def load_data_from_api(*args, **kwargs):
    
    # explicitly specifying the year and months for the sake of exercise.
    target_year = 2022
    initial_month = 1
    final_month = 12
    
    ini=time.time()
    for month in range(initial_month,final_month+1):
        start = time.time()
        month = '0'+(str(month)) if month < 10 else month
        try:
            # base url
            url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_{target_year}-{month}.parquet'
            # get the response from url request
            response = requests.get(url)
            # parquet file mount 
            parquet_file = io.BytesIO(response.content)
            # create df from parquet file
            df = pd.read_parquet(parquet_file, engine='pyarrow')
            # prepare output df
            output = df if month == '01' else pd.concat([output, df], ignore_index=True)
        except Exception as e:
            print(f'Exception: {e}')
            break
        end = time.time()
        print(f'Finished month {month} after: {round((end-start),2)}s')
    end = time.time()
    print(f'Process finished after {round(end-ini,2)}s \n\n')
    # print(output.info())
    return output

# @test
# def test_output(output, *args) -> None:
#     """
#     Template code for testing the output of the block.
#     """
#     assert output is not None, 'The output is undefined'ta