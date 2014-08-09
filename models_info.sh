#!/usr/bin/env bash

python manage.py models_info --settings="cups_profile.settings" 2>> ./$(date +"%Y%m%d").dat
