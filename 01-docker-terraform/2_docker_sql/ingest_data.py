#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from time import time
import os
import argparse

# create a conn to postgres to create the specific DDL
from sqlalchemy import create_engine


def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    
    if url.endswith('.csv.gz'):
        csv_name = 'output.csv.gz'
    else:
        csv_name = 'output.csv'
    
    
    # use the system comand bash to download the csv file
    os.system(f'wget {url} -O {csv_name}')
    
    # engine is a connection with the specified database
    #        create_engine('db://user:password@host:port/db_name')
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    #this is an iterator 
    df_iter = pd.read_csv(csv_name, chunksize=100000, iterator=True)

    df = next(df_iter)

    #Adjust following columns from text to datetime
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    # this will create the table with the column names.
    # if it exists, then replace it
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    
    df.to_sql(name=table_name, con=engine, if_exists='append')

    # this loop is gonna call the next iter until next() throws an exception.
    while True:
        #TODO implemen
        t_start = time()
        # calling with next get a chunk of 100000 rows, as defined above
        df = next(df_iter)
        
        #Adjust following columns from text to datetime
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        t_end = time()
        
        print(f'Chunk proccessed after {round(t_end-t_start,3)} seconds.')
  
  
if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for postgres')
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table-name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()
    #print(args.accumulate(args.integers))
    
    main(args)