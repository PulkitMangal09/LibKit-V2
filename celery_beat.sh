#!/bin/bash

cd $(pwd)/backend

celery -A app.celery_app beat -l info
