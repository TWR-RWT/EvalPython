#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from flask import Flask, render_template, request, flash, redirect, url_for
from jinja2 import Template
import psycopg2
import psycopg2.extras
import json
import sys
from urllib import parse
import pandas as pd


app = Flask(__name__)

app.secret_key = "very-secret-key"

DB_HOST = "localhost"
DB_NAME = "mydb"
DB_USER = "postgres"
DB_PASS = "***"
DB_PORT="5432"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

@app.route("/")
def index():
    return render_template('/base.html')

from app import locataires_views
from app import locations_views

