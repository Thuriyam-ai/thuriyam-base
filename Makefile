# Uncomment below line and add consumers
# CORE_CONSUMERS := consumers

export LC_ALL=en_US.UTF-8
export LANG=en_US.UTF-8
export LC_TYPE=en_US.UTF-8

help:
	@echo "Makefile for wi-job-notification-ms"
	@echo "When running any of run commands ensure that you have activated your python virtual environment"
	@echo "\033[33;36m"
	@echo "init			Install required packages."
	@echo "runserver		Run django server 5000"
# 	@echo "runworker		Run celery worker"
# 	@echo "runconsumers		Run kafka consumers in parallel"

init:
	npm i -g ttab
	pip install -r app/requirements/development.txt
	pre-commit install

runserver:
	ttab "cd $(PWD)/app; source $(VIRTUAL_ENV)/bin/activate; python3 manage.py runserver 0.0.0.0:5000"

shell:
	ttab "cd $(PWD)/app; source $(VIRTUAL_ENV)/bin/activate; python3 manage.py shell"

# Uncomment below lines if using celery worker
# runworker:
# 	ttab "cd $(PWD)/app; source $(VIRTUAL_ENV)/bin/activate; celery -A wi-job-notification-ms worker --loglevel=INFO --concurrency=10 -n worker1.%%h "

# Uncomment below lines if using kafka consumers
# runconsumers:
# 	for consumer in $(CORE_CONSUMERS); do \
# 	   ttab "cd $(PWD)/app; source $(VIRTUAL_ENV)/bin/activate; python3 manage.py $$consumer" ; \
# 	done
