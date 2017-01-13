#!/usr/bin/env python

BROKER_HOST = "localhost"
BROKER_PORT = 5672
BROKER_USER = "admin"
BROKER_PASSWORD = "root"
BROKER_VHOST = "admin_vhost"

CELERY_RESULT_BACKEND = "mongodb"
CELERY_MONGODB_BACKEND_SETTINGS = {
    "host": "localhost",
    "port": 27017,
    "database": "celery",
    "taskmeta_collection": "my_taskmeta_collection",
}

CELERY_IMPORTS = ("tasks", )
