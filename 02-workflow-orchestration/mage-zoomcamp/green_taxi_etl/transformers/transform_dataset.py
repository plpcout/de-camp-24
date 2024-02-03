if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@transformer
def transform(data, *args, **kwargs):
    
    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    data = data[data['passenger_count'] > 0]
    data = data[data['trip_distance'] > 0]
    
    # Create a new column lpep_pickup_date by converting lpep_pickup_datetime to a date.
    data['lpep_pickup_date'] = pd.to_datetime(data['lpep_pickup_datetime']).dt.date 
    
    # Rename columns in Camel Case to Snake Case, e.g. VendorID to vendor_id.
    data.columns = data.columns.str.replace('(?<=[a-z])(?=[A-Z])', '_', regex=True).str.lower()
    return data
    

@test
def valid_vendor_id(output, *args):
    assert output['vendor_id'].isin([1,2]).sum() == len(output), 'There are invalid user_id\'s'

@test
def valid_passengers(output, *args):
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'

@test
def valid_distances(output, *args):
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rides with zero trip distance'