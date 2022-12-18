from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'catchup': False,
    'execution_timeout': timedelta(hours=6),
    'depends_on_past': False,
}

dag = DAG(
    'sample_dag',
    default_args = default_args,
    description = "sample description",
    schedule_interval = "@once",
    start_date = days_ago(2),
    tags = ['daily'],
    max_active_runs=3,
    concurrency=1
)
run_script= "{py_interpreter} {py_file} {news_category}".format(
    py_interpreter='/Library/Frameworks/Python.framework/Versions/3.10/bin/python3.10'
    ,py_file='/Users/kimjunhyeon/teddy-toy-proj/news/cllct-naver-news/ProjMain.py'
    ,news_category='ModelOfEco'
)
naver_news_eco= BashOperator(
    task_id= 'naver-news-eco'
    , bash_command= run_script
    , dag= dag
)

naver_news_eco