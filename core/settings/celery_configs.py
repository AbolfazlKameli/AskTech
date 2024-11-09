from datetime import timedelta

from decouple import config

broker_connection_retry_on_startup = True
broker_url = "amqp://guest:guest@rabbitmq:5672//"
result_backend = 'rpc://'
worker_prefetch_multiplier = 3
timezone = config('TIME_ZONE')
task_serializer = 'json'
result_serializer = 'pickle'
accept_content = ['json', 'pickle']
result_expire = timedelta(minutes=1)
