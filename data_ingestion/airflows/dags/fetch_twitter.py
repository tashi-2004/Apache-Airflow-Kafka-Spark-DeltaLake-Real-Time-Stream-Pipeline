import tweepy
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

TWITTER_API_KEY = '160xl53FUKfuDjMceaJzaE6yz'
TWITTER_API_SECRET = 'vAk8ykuyoNVmNbqfv3tXcV3lqZQA4fyAxaKK7wgvVkbbGrMmK7'
TWITTER_ACCESS_TOKEN = '1901215733557637120-PRxOwlNCYqJcbG9e0fVkCPekKdykSH'
TWITTER_ACCESS_SECRET = 'aCvkwZPr2u3M7QpDUUcUM7hQ5rhWmOJmXL7FbrgPm1n6L'

def fetch_twitter_data():
    auth = tweepy.OAuth1UserHandler(
        TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
    )
    api = tweepy.API(auth)
    try:
        tweets = api.user_timeline(screen_name="transit", count=10)
        for tweet in tweets:
            print(f"Tweet: {tweet.text}")
    except tweepy.TweepyException as e: 
        print(f"Error fetching tweets: {e}")

dag = DAG(
    'fetch_twitter',
    description='Fetch Twitter Data',
    schedule_interval='@hourly',  
    start_date=datetime(2025, 3, 21),
    catchup=False,
    default_args={
        'retries': 3,  
        'retry_delay': timedelta(minutes=5),  
        'max_retry_delay': timedelta(minutes=10),  
        'execution_timeout': timedelta(minutes=10), 
    }
)

fetch_twitter_task = PythonOperator(
    task_id='fetch_twitter_data_task',
    python_callable=fetch_twitter_data,
    dag=dag,
)
