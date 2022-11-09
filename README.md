# Forex-Data-Pipeline
This ETL process will extract data from fixer.io API, transform it, and load it to a PostgreSQL database. At the end of the project you will have an automated process that constantly feeds the PostgreSQL database with data. Every 2 minutes, the ETL process will load an updated batch of Forex data.

__Note__:

To learn how to set everything up in more details, check out my Medium article. Follow every step to create the Forex Data Pipeline.

https://medium.com/@bdadon50/etl-process-using-airflow-and-docker-226aa5c7a41a

# Project Architecture
![oie_dlxTDEAlYwYX](https://user-images.githubusercontent.com/65648983/200797626-0e6e61cc-a0c7-4049-bcd8-190346b22be8.png)
![document-1-1](https://user-images.githubusercontent.com/65648983/200800954-abc1754e-1a69-4f2d-b806-926e822018e1.png)


# Deploying the Pipeline
1. Run docker-compose up -d to set up Airflow.
2. Log in to Airflow at localhost:8080.
3. Create the necessary connections.
4. Execute the Pipeline.
5. Log in to PgAdmin at localhost:5050.
6. Set up a new server.
7. Query the data.

# End Result
Clean Forex data ready to be analyzed!
![pgadmin](https://user-images.githubusercontent.com/65648983/200799154-191f9922-6ebb-4b30-b9b7-199d46db3910.png)
