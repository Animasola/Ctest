SHELL=/bin/sh

# constants
PROJECT_NAME=cups_profile

MANAGE=PYTHONPATH=$(CURDIR) python manage.py

# commands
run:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups_profile.settings $(MANAGE) runserver
	
shell:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups_profile.settings $(MANAGE) shell

test:
	PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=cups_profile.settings $(MANAGE) test my_info