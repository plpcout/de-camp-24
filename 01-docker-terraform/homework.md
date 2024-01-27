## Module 1 Homework

## Docker & SQL

In this homework we'll prepare the environment 
and practice with Docker and SQL


## Question 1. Knowing docker tags

Run the command to get information on Docker 

```docker --help```

Now run the command to get help on the "docker build" command:

```docker build --help```

Do the same for "docker run".

Which tag has the following text? - *Automatically remove the container when it exits* 

- `--delete`
- `--rc`
- `--rmc`
- `--rm`

**Answer**: `--rm`

## Question 2. Understanding docker first run 

Run docker with the python:3.9 image in an interactive mode and the entrypoint of bash.
Now check the python modules that are installed ( use ```pip list``` ). 

What is version of the package *wheel* ?

- 0.42.0
- 1.0.0
- 23.0.1
- 58.1.0

**Answer**: wheel 0.41.3

# Prepare Postgres

Run Postgres and load data as shown in the videos
We'll use the green taxi trips from September 2019:

```wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz```


## How this was done
  - pipeline for homework
  - minor edit to previous ingestion code 
  - docker build using hw_ingest_data.py

```bash
docker build -t hw_ingestion_1.py:homework .
```

```bash
URL=https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz

docker run -it --network=2_docker_sql_default hw_ingestion_1:homework \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table-name=yellow_taxi_trips_2019 \
  --url=${URL}


```


You will also need the dataset with zones:

```wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv```

Download this data and put it into Postgres (with jupyter notebooks or with a pipeline)


```bash
docker build -t hw_ingestion_2.py:homework .
```

```bash
URL=https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv

docker run -it --network=2_docker_sql_default hw_ingestion_2:homework \
  --user=root \
  --password=root \
  --host=pgdatabase \
  --port=5432 \
  --db=ny_taxi \
  --table-name=taxi_zone_lookup \
  --url=${URL}

```


## Question 3. Count records 

How many taxi trips were totally made on September 18th 2019?

Tip: started and finished on 2019-09-18. 

Remember that `lpep_pickup_datetime` and `lpep_dropoff_datetime` columns are in the format timestamp (date and hour+min+sec) and not in date.

- 15767
- 15612
- 15859
- 89009

**Answer: 15612**

## Question 4. Largest trip for each day

Which was the pick up day with the largest trip distance
Use the pick up time for your calculations.

- 2019-09-18
- 2019-09-16
- 2019-09-26
- 2019-09-21

**Answer: 2019-09-26 - 341.64**


## Question 5. Three biggest pick up Boroughs

Consider lpep_pickup_datetime in '2019-09-18' and ignoring Borough has Unknown

Which were the 3 pick up Boroughs that had a sum of total_amount superior to 50000?
 
- "Brooklyn" "Manhattan" "Queens"
- "Bronx" "Brooklyn" "Manhattan"
- "Bronx" "Manhattan" "Queens" 
- "Brooklyn" "Queens" "Staten Island"

**Answer: "Brooklyn" "Manhattan" "Queens"**

```sql
SELECT 
fact.lpep_pickup_datetime::date
,pu."Borough"
,sum(fact.total_amount) as sum_total

FROM public.yellow_taxi_trips_2019 fact
left join public.taxi_zone_lookup pu
on fact."PULocationID" = pu."LocationID"
where lpep_pickup_datetime::date = '2019-09-18'
and pu."Borough" <> 'Unknown'
group by 1,2
order by 3 desc
limit 3
```


## Question 6. Largest tip

For the passengers picked up in September 2019 in the zone name Astoria which was the drop off zone that had the largest tip?
We want the name of the zone, not the id.

Note: it's not a typo, it's `tip` , not `trip`

- Central Park
- Jamaica
- JFK Airport
- Long Island City/Queens Plaza

**Answer: JFK Airport**
```sql
SELECT
fact.lpep_pickup_datetime::date
,concat(pu."Borough",' - ' ,pu."Zone")
,concat(doff."Borough",' - ' ,doff."Zone")
,fact.tip_amount

FROM public.yellow_taxi_trips_2019 fact
left join public.taxi_zone_lookup pu
on fact."PULocationID" = pu."LocationID"
left join public.taxi_zone_lookup doff
on fact."DOLocationID" = doff."LocationID"
where extract('year' from lpep_pickup_datetime) = '2019'
and extract('month' from lpep_pickup_datetime) = '09'
and pu."Zone" = 'Astoria'
order by 4 desc
limit 1
```


## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform. 
Copy the files from the course repo
[here](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Creating Resources

After updating the main.tf and variable.tf files run:

```
terraform apply
```

Paste the output of this command into the homework submission form.


```bash
(base) pedro@instance-1:~/data-engineering-zoomcamp/01-docker-terraform/1_terraform_gcp/terraform/terraform_with_variables$ terraform apply
google_bigquery_dataset.demo_dataset: Refreshing state... [id=projects/terraform-demo-411919/datasets/demo_dataset]

Terraform used the selected providers to generate the following execution plan. Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # google_storage_bucket.demo-bucket will be created
  + resource "google_storage_bucket" "demo-bucket" {
      + effective_labels            = (known after apply)
      + force_destroy               = true
      + id                          = (known after apply)
      + location                    = "US"
      + name                        = "terraform-demo--411919-terra-bucket"
      + project                     = (known after apply)
      + public_access_prevention    = (known after apply)
      + self_link                   = (known after apply)
      + storage_class               = "STANDARD"
      + terraform_labels            = (known after apply)
      + uniform_bucket_level_access = (known after apply)
      + url                         = (known after apply)

      + lifecycle_rule {
          + action {
              + type = "AbortIncompleteMultipartUpload"
            }
          + condition {
              + age                   = 1
              + matches_prefix        = []
              + matches_storage_class = []
              + matches_suffix        = []
              + with_state            = (known after apply)
            }
        }
    }

Plan: 1 to add, 0 to change, 0 to destroy.

Do you want to perform these actions?
  Terraform will perform the actions described above.
  Only 'yes' will be accepted to approve.

  Enter a value: yes

google_storage_bucket.demo-bucket: Creating...
google_storage_bucket.demo-bucket: Creation complete after 0s [id=terraform-demo--411919-terra-bucket]

Apply complete! Resources: 1 added, 0 changed, 0 destroyed.
```
