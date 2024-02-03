import pyarrow as pa
import pyarrow.parquet as pq
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter


# Env variables
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/home/src/credentials.json'

# gcs bucket
bucket_name='mage-zoomcamp-plpc'

project_id='terraform-demo-411919'

table_name='green_taxi'

root_path=f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    # Prepare pyarrow table
    table = pa.Table.from_pandas(data)
    
    # Load environ credentials
    gcs = pa.fs.GcsFileSystem()

    # pyarrow parquet - write to gcp
    pq.write_to_dataset(
        table, 
        root_path=root_path,
        partition_cols=['lpep_pickup_date'],
        filesystem=gcs
    )


