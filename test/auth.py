#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Response, jsonify, make_response, session, Flask
from flask import Flask, render_template, request, flash, redirect, url_for, session
import psycopg2
import psycopg2.extras
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

DB_HOST = get_env_variable("POSTGRES_DB_HOST")
DB_NAME = get_env_variable("POSTGRES_DB_NAME")
DB_USER = get_env_variable("POSTGRES_DB_USER")
DB_PASS = get_env_variable("POSTGRES_DB_PASS")
DB_PORT = get_env_variable("POSTGRES_DB_PORT")
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)


def login(username, password):
    username = username
    password = password
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        cur.execute("""
            SELECT * FROM immo.accounts 
            WHERE username = %s
        """, (username,))
        user = cur.fetchone()
        conn.commit()
        cur.close()#
        #conn.close()#
        if check_password_hash(user['password'], password):
            return "success"
        else:
            return "wrong password"
    except:
        return "wrong username"


def test_jwt(username, secret_key):
    token = jwt.encode({'user': username, 'exp': datetime.utcnow() + timedelta(hours=24)}, secret_key)
    decode = jwt.decode(token, secret_key, algorithms=['HS256'])
    return decode['user']

def add(x, y):
    """Add Function"""
    return x + y


def subtract(x, y):
    """Subtract Function"""
    return x - y


def multiply(x, y):
    """Multiply Function"""
    return x * y


def divide(x, y):
    """Divide Function"""
    if y == 0:
        raise ValueError('Can not divide by zero!')
    return x / y