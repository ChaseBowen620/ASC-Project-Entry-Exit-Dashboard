#!/bin/bash
cd /home/ubuntu/ASC-Project-Entry-Exit-Dashboard
source .venv/bin/activate
cd backend
python manage.py runserver 0.0.0.0:8000

