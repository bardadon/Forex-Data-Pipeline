# Forex-Data-Pipeline
![oie_dlxTDEAlYwYX](https://user-images.githubusercontent.com/65648983/200797626-0e6e61cc-a0c7-4049-bcd8-190346b22be8.png)

The ETL process will extract data from fixer.io API, transform it, and load it to a PostgreSQL database. This project aims to have an automated process that constantly feeds the PostgreSQL database with data. Every 2 minutes, the ETL process will load an updated batch of Forex data.

### The components of the architecture are:

1. Airflow Webserver
2. Airflow Scheduler
3. Airflow Worker
4. Airflow Trigger
5. Flower
6. Postgres Database
7. pgAdmin UI
8. Redis Database

__Note__
To learn how to set everything up, check out my Medium article. Follow every step to create the Forex Data Pipeline.

https://medium.com/@bdadon50/etl-process-using-airflow-and-docker-226aa5c7a41a

## Creating the Pipeline
1. Run docker-compose up -d to set up Airflow.
2. Log in to Airflow at localhost:8080.
3. Create the necessary connections.
4. Execute the Pipeline.
5. Log in to PgAdmin at localhost:5050.
6. Set up a new server.
7. Query the data.
