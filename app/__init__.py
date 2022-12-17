#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from flask import Flask, render_template, request, flash, redirect, url_for, session
from jinja2 import Template
import psycopg2
import psycopg2.extras
import json
import sys
from urllib import parse
import jwt
from dotenv import load_dotenv
import os

# loads the environment variable file
load_dotenv()

# Function to get the environmental variables
def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = "Expected env variable '{}' not set.".format(name)
        raise Exception(message)

app = Flask(__name__)

app.secret_key = "very-secret-key"

DB_HOST = "dpg-ceevc3h4reb3r0p0mlng-a.frankfurt-postgres.render.com" #get_env_variable("POSTGRES_DB_HOST")
DB_NAME = "mydb_3gut" #get_env_variable("POSTGRES_DB_NAME")
DB_USER = "postgres_user" #get_env_variable("POSTGRES_DB_USER")
DB_PASS = "iKXtSSMu6hxGBDyNyA0BGuJQpnAftFK4" #get_env_variable("POSTGRES_DB_PASS")
DB_PORT = "5432"#get_env_variable("POSTGRES_DB_PORT")
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


@app.route("/")
def index():
    if not session.get('logged_in'):
        return render_template('/authentification/login.html')
    else:
        return contrats_views.contrats()

from app import locataires_views
from app import locations_views
from app import contrats_views
from app import pdf_generation
from app import authentification