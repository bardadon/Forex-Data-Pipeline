import airflow
from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.hooks.postgres_hook import PostgresHook


from datetime import datetime, timedelta
from pendulum import date
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
from pandas import json_normalize


# Grab current date
current_date = datetime.today().strftime('%Y-%m-%d')

# Default settings for all the dags in the pipeline
default_args = {

    "owner": "Airflow", 
    "start_date" : datetime(2022,8,1),
    "retries" : 1,
    "retry_delay": timedelta(minutes=5)

}

def _process_data(ti):

    data = ti.xcom_pull(task_ids = 'extract_user') # Extract the json object from XCom
    data = data['rates'] # Extract the symbols and the rates in a dictionary 
    processed_data = pd.DataFrame(columns=['rate', 'symbol']) # Create an empty DataFrame
    temp_df = dict() # Create an empty dictionary

    # Iterate through the symbols, create a temp dataframe from each symbol and append it to the DataFrame
    for symbol,rate in data.items():
    
        temp_df = json_normalize({
            
            'rate': float(rate),
            'symbol' :symbol
            
        })
    
        processed_data = processed_data.append(temp_df)
    
    # Export DataFrame to CSV
    processed_data.to_csv('/tmp/processed_data.csv', index=None, header=False)


def _store_data():
    '''
    This function uses the Postgres Hook to copy users from processed_data.csv
    and into the table
    
    '''
    # Connect to the Postgres connection
    hook = PostgresHook(postgres_conn_id = 'postgres')

    # Insert the data from the CSV file into the postgres database
    hook.copy_expert(
        sql = "COPY rates FROM stdin WITH DELIMITER as ','",
        filename='/tmp/processed_data.csv'
    )


with DAG('forex_pipeline', default_args=default_args, schedule_interval=timedelta(minutes=2), catchup=False) as dag:


    # Dag #1 - Check if the API is available
    is_api_available = HttpSensor(
        task_id='is_api_available',
        method='GET',
        http_conn_id='is_api_available',
        endpoint= current_date + '?access_key=720ead7bdefed8501715c6d714293717',
        response_check= lambda response: 'EUR' in response.text,
        poke_interval = 5
    )


    # Dag #2 - Create a table
    create_table = PostgresOperator(
        task_id = 'create_table',
        postgres_conn_id='postgres',
        sql='''
            drop table if exists rates;
            create table rates(
                rate float not null,
                symbol text not null
            );
        '''
    )


    # DAG #3 - Extract Data
    extract_data = SimpleHttpOperator(
            task_id = 'extract_user',
            http_conn_id='is_api_available',
            method='GET',
            endpoint= current_date + '?access_key=720ead7bdefed8501715c6d714293717',
            response_filter=lambda response: json.loads(response.text),
            log_response=True
    )

    # Dag #4 - Process data
    transform_data = PythonOperator(
        task_id = 'transform_data',
        python_callable=_process_data

    )

    # Dag #5 - Load data
    load_data = PythonOperator(
        task_id = 'load_data',
        python_callable=_store_data

    )

    # Dependencies
    is_api_available >> create_table >> extract_data >> transform_data >> load_data
