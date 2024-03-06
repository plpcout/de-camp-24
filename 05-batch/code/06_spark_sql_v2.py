#!/usr/bin/env python
# coding: utf-8

# In[1]:

import argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql import functions as F


parser = argparse.ArgumentParser()

parser.add_argument('--input_green', required=True)
parser.add_argument('--input_yellow', required=True)
parser.add_argument('--output', required=True)


args = parser.parse_args()


input_green = args.input_green
input_yellow = args.input_yellow
output = args.output

##############################################
# spark = SparkSession.builder \
#     .master('spark://pedro:7077') \
#     .appName('test') \
#     .getOrCreate()
#
# ###### Run code bellow.
# python 06_spark_sql-Copy1.py \
# 	--input_green=data/pq/green/2020/* \
# 	--input_yellow=data/pq/yellow/2020/* \
# 	--output=data/report-2020 \
##############################################
    
    
    

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

##############################################
# Define master as a spark-submit arg
# Master url
# URL='spark://pedro:7077'

# spark-submit \
# 	--master=${URL} \
# 	06_spark_sql-Copy1.py \
# 	--input_green=data/pq/green/2021/* \
# 	--input_yellow=data/pq/yellow/2021/* \
# 	--output=data/report-2021
##############################################


df_green = spark.read.parquet(input_green)
df_yellow = spark.read.parquet(input_yellow)

# #check what columns are common beteen the two dfs
# set(df_green.columns) & set(df_yellow.columns)

df_green = df_green \
    .withColumnRenamed('lpep_pickup_datetime','pickup_datetime') \
    .withColumnRenamed('lpep_dropoff_datetime','dropoff_datetime')

df_yellow = df_yellow \
    .withColumnRenamed('tpep_pickup_datetime','pickup_datetime') \
    .withColumnRenamed('tpep_dropoff_datetime','dropoff_datetime')


# In[10]:


#order the common columns order (as it is in green df
common_columns = []

yellow_columns = set(df_yellow.columns)

for col in df_green.columns:
    if col in yellow_columns:
        common_columns.append(col)


# In[11]:


common_columns


# In[13]:



# In[14]:


df_green_sel = df_green.select(common_columns).withColumn('service_type', F.lit('green'))

df_yellow_sel = df_yellow.select(common_columns).withColumn('service_type', F.lit('yellow'))

df_trips_data = df_green_sel.unionAll(df_yellow_sel)


# tell spark that this df is a usable table
df_trips_data.registerTempTable('trips_data')


df_result = spark.sql("""
SELECT 
    -- Reveneue grouping 
    PULocationID AS revenue_zone,
    date_trunc('month', pickup_datetime) AS revenue_month, 
    service_type, 

    -- Revenue calculation 
    SUM(fare_amount) AS revenue_monthly_fare,
    SUM(extra) AS revenue_monthly_extra,
    SUM(mta_tax) AS revenue_monthly_mta_tax,
    SUM(tip_amount) AS revenue_monthly_tip_amount,
    SUM(tolls_amount) AS revenue_monthly_tolls_amount,
    SUM(improvement_surcharge) AS revenue_monthly_improvement_surcharge,
    SUM(total_amount) AS revenue_monthly_total_amount,
    SUM(congestion_surcharge) AS revenue_monthly_congestion_surcharge,

    -- Additional calculations
    AVG(passenger_count) AS avg_montly_passenger_count,
    AVG(trip_distance) AS avg_montly_trip_distance
FROM
    trips_data
GROUP BY
    1, 2, 3

""")


df_result.coalesce(1).write.parquet(output , mode='overwrite')

