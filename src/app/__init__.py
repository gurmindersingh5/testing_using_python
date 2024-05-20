from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import logging
from logging.handlers import RotatingFileHandler
import os
from prometheus_flask_exporter import PrometheusMetrics

# __name__ = data
app = Flask(__name__)

DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
# use host accordingly ( example: use postgresql svc name \
# in k8s to make connection)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'postgres')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = "secret123"
# Define the log directory
log_directory = 'logs'

# Ensure the log directory exists
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
# app.config['SQLALCHEMY_DATABASE_URI'] = \
# f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = \
# False  # Optional: but it's good to disable it for performance reasons

db = SQLAlchemy(app)

# Configure logging
handler = RotatingFileHandler('logs/user.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
app.logger.addHandler(handler)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Application info', version='Version 1 (ONLY TO TEST LOG METRIC), this log is from microservice: user')

# Configure JWT settings
# # app.config['JWT_SECRET_KEY'] = 'ABC123ABC123'  # Replace with your secret key
# # jwt = JWTManager(app)

from . import routes
from . import models

with app.app_context():
    db.create_all()
