# __init__.py
from flask import Flask
from .config import Config

# Initialize the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Import the routes from main.py
from .main import *
