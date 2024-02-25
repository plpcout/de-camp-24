{{
    config(
        materialized='table'
    )
}}

with dim_zones as
(
    select * from {{ref("dim_zones")}}
    where borough != 'Unknown'
)


select 

tripid
,dispatching_base_num
,pickup_locationid
,pu_zones.borough as pickup_borough
,dropoff_locationid
,do_zones.borough as dropoff_borough
,sr_flag
,affiliated_base_number
,pickup_datetime
,dropoff_datetime

from {{ ref('stg_fhv_tripdata') }} fact
inner join dim_zones as pu_zones
on fact.pickup_locationid = pu_zones.locationid
inner join dim_zones as do_zones
on fact.dropoff_locationid = do_zones.locationid
