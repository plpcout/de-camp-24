## Week 3 Homework
<b><u>Important Note:</b></u> <p> For this homework we will be using the 2022 Green Taxi Trip Record Parquet Files from the New York
City Taxi Data found here: </br> https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page </br>
If you are using orchestration such as Mage, Airflow or Prefect do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>
<u>NOTE:</u> You will need to use the PARQUET option files when creating an External Table</br>

<b>SETUP:</b></br>
Create an external table using the Green Taxi Trip Records Data for 2022. </br>
```SQL
CREATE OR REPLACE EXTERNAL TABLE `ny_taxi.external_2022_green_tripdata`
OPTIONS (
  format = 'parquet',
  uris = ['https://storage.cloud.google.com/03-homework/green_taxi_2022.parquet']
);
```
Create a table in BQ using the Green Taxi Trip Records for 2022 (do not partition or cluster this table). </br>
</p>

```SQL
CREATE OR REPLACE TABLE `ny_taxi.2022_green_tripdata` AS
SELECT * FROM `ny_taxi.external_2022_green_tripdata`
```

## Question 1:
Question 1: What is count of records for the 2022 Green Taxi Data??
- 65,623,481
- **840,402**
- 1,936,423
- 253,647
### Answer: 840,402


## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?

- **0 MB for the External Table and 6.41MB for the Materialized Table**
- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table
- 2.14 MB for the External Table and 0MB for the Materialized Table
### Answer: 0 MB for the External Table and 6.41MB for the Materialized Table


## Question 3:
How many records have a fare_amount of 0?
- 12,488
- 128,219
- 112
- 1,622
### Answer: 1,622
```SQL
SELECT 
COUNT(*) 
FROM `ny_taxi.external_2022_green_tripdata`
WHERE fare_amount = 0
```



  
## Question 4:
What is the best strategy to make an optimized table in Big Query if your query will always order the results by PUlocationID and filter based on lpep_pickup_datetime? (Create a new table with this strategy)

```sql
CREATE OR REPLACE TABLE `ny_taxi.2022_green_tripdata_partitioned`
PARTITION BY lpep_pickup_date
CLUSTER BY PULocationID
AS
SELECT
VendorID
,lpep_pickup_datetime
,lpep_dropoff_datetime
,store_and_fwd_flag
,RatecodeID
,PULocationID
,DOLocationID
,passenger_count
,trip_distance
,fare_amount
,extra
,mta_tax
,tip_amount
,tolls_amount
,ehail_fee
,improvement_surcharge
,total_amount
,payment_type
,trip_type
,congestion_surcharge
-- WORKAROUND TO FIX THE BUGGY DATETIME IMPORT FROM GCS file.parquet TO BQ
-- Might not be the best aproach, but it works for the sake of concluding the exercise.
,DATE(TIMESTAMP_MILLIS(CAST(LEFT(CAST(lpep_pickup_datetime AS string),13) AS integer))) lpep_pickup_date

FROM `ny_taxi.2022_green_tripdata`

```


- Cluster on lpep_pickup_datetime Partition by PUlocationID
- **Partition by lpep_pickup_datetime  Cluster on PUlocationID**
- Partition by lpep_pickup_datetime and Partition by PUlocationID
- Cluster on by lpep_pickup_datetime and Cluster on PUlocationID
### Answer: Partition by lpep_pickup_datetime  Cluster on PUlocationID


## Question 5:
Write a query to retrieve the distinct PULocationID between lpep_pickup_datetime
06/01/2022 and 06/30/2022 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 4 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 22.82 MB for non-partitioned table and 647.87 MB for the partitioned table
- **12.82 MB for non-partitioned table and 1.12 MB for the partitioned table**
- 5.63 MB for non-partitioned table and 0 MB for the partitioned table
- 10.31 MB for non-partitioned table and 10.31 MB for the partitioned table
### Answer: 12.82 MB for non-partitioned table and 1.12 MB for the partitioned table

```sql
SELECT
DISTINCT
PULocationID
FROM `ny_taxi.2022_green_tripdata`
-- FROM `ny_taxi.2022_green_tripdata_partitioned`
WHERE lpep_pickup_date between '2022-06-01' and '2022-06-30' 
```

## Question 6: 
Where is the data stored in the External Table you created?

- Big Query
- **GCP Bucket**
- Big Table
- Container Registry
### Answer: GCP Bucket


## Question 7:
It is best practice in Big Query to always cluster your data:
- True
- **False**
### Answer: False

## (Bonus: Not worth points) Question 8:
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?
### Answer: 0 bytes processed. This particular query is not using any filtering nor scanning any columns, it's just a consult to the table's metadata, therefore bytes will not be processed, as expected
 
## Submitting the solutions

* Form for submitting: TBD
* You can submit your homework multiple times. In this case, only the last submission will be used. 

Deadline: TBD

