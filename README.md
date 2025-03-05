# stock_ETL

ETL pipeline for extracting FinLab stock price & volume data

## Installation

I recommended using `uv` for faster installation & less package conflict issues

```
uv venv && source .venv/bin/activate

uv pip install -r requirements.txt
```

## Using the ETL pipeline

1. create a `.env` file to store the api key from your FinLab account (sensitive informations)

```plaintext
API_KEY="you_api_key"
```

2. Change the home path of airflow and python to your project

```bash
export AIRFLOW_HOME="$(pwd)"
export PYTHONPATH=$PYTHONPATH:/path/to/your/airflow_project/scripts
```

3. Initialize DB

```bash
airflow init db
```

4. add user to apache-airflow and check if it works

```bash
airflow users create \
	--username \
	--firstname \
	--lastname \
	--email \
	--password \
	--role Admin
	
airflow users list
```

5. Run webserver & scheduler

```bash
airflow webserver -H 0.0.0.0 -p 8888
airflow scheduler
```
