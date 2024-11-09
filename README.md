# AskTech

AskTech is a free and open source website. Django REST API technology is used in
the back-end of this site.

## Authors

- [@AbolfazlKameli](https://github.com/AbolfazlKameli/) (back-end dev)

## Run with Docker

```shell
docker compose up
```

## Run Locally

install required packages

```shell
sudo apt install erlang rabbitmq-server
```

start rabbitmq-server service

```shell
sudo systemctl start rabbitmq-server
```

Clone the project

```shell
git clone https://github.com/AbolfazlKameli/AskTech.git
```

Go to the project directory

```shell
cd AskTech/
```

make a virtual environment

```shell
python3 -m venv .venv
```

activate virtual environment

```shell
source .venv/bin/activate 
```

install requirements

```shell
pip install -r requirements.txt
```

start celery project

```shell
celery -A core worker -l INFO  
```

Create your own `.env` file

```shell
cp .env_example .env
```

start the django server

```shell
python manage.py runserver
```
