import airflow
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from sodapy import Socrata

from pubmedscrapper import *
from user_definition import *
from pubmed_aggregate import *


with DAG(dag_id="pubmed_data",
         start_date=datetime(2023, 2, 14),
         catchup=False,
         schedule_interval='@daily') as dag:

    create_insert_aggregate = SparkSubmitOperator(
        task_id="aggregate_creation",
        packages="com.google.cloud.bigdataoss:gcs-connector:hadoop2-1.9.17,org.mongodb.spark:mongo-spark-connector_2.12:3.0.1",
        exclude_packages="javax.jms:jms,com.sun.jdmk:jmxtools,com.sun.jmx:jmxri",
        conf={"spark.driver.userClassPathFirst": True,
              "spark.executor.userClassPathFirst": True,
              #  "spark.hadoop.fs.gs.impl":"com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem",
              #  "spark.hadoop.fs.AbstractFileSystem.gs.impl":"com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS",
              #  "spark.hadoop.fs.gs.auth.service.account.enable":True,
              #  "google.cloud.auth.service.account.json.keyfile":service_account_key_file,
              },
        verbose=True,
        # change to relative path
        application=f'{dag_folder}/pubmed_aggregate.py'
    )

    pubmed_data_gcp = PythonOperator(task_id="import_pubmed_data_gcp",
                                     python_callable=pubmed_upload_data,
                                     dag=dag)

    pubmed_data_gcp >> create_insert_aggregate
