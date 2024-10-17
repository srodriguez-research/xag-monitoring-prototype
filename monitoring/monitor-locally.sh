
# export SERVICE_NAME=coffee-mock
# export SERVICE_NAME=coffee-sarl
export SERVICE_NAME=coffee-sarl-bugs
export TEMPO_URL=http://localhost:3200/api

export TRACES_DIR=data/traces_store
export REPORTS_DIR=data/reports

poetry run python monitor.py
