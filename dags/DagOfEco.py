'''
[네이버 뉴스- 경제]
@author JunHyeon.Kim
@email sleep4725@gmail.com
'''
import os
from datetime import datetime
import pendulum
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# -------------------------------------------------
# Timezone setup
local_tz = pendulum.timezone("Asia/Seoul")
# -------------------------------------------------

DAG_ID, _ = os.path.splitext(os.path.basename(__file__))
print(DAG_ID)

default_args = {
    'owner': 'airflow',
    'catchup': False,
    'execution_timeout': timedelta(hours=6),
    'depends_on_past': False,
}

with DAG (
    DAG_ID
    , schedule_interval = "@once"
    , start_date = datetime(2022, 12, 23, tzinfo= local_tz)
    , default_args = default_args
    , tags = ["Teddy", "NaverNews", "Economics"]
) as dag:
    run_script= "{py_interpreter} {py_file} {news_category}".format(
        py_interpreter='/opt/homebrew/bin/python3.10'
        ,py_file='/Users/kimjunhyeon/tedy-playground-01/toy-project/cllct-naver-news/ProjMain.py'
        ,news_category='ModelOfEco'
    )
    naver_news_eco= BashOperator(
        task_id= 'naver-news-eco'
        , bash_command= run_script
        , dag= dag
    )

    naver_news_eco