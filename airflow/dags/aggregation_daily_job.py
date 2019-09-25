#!/usr/bin/python

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta
import os


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2016, 6, 15),
    'email': [],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'daily_aggregate_votes_comments',
    default_args=default_args,
    schedule_interval=timedelta(days=1))

aggregate_votes_comments = BashOperator(
    task_id="daily_aggregate_votes_comments",
    bash_command="/home/ubuntu/stackoverflow/3_s3_spark_aggregation_postgredb/aggregation_over_parquet.py {{ ds }}",
    dag=dag)
