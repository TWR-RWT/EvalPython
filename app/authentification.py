#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, conn, request, render_template, flash, redirect, url_for, psycopg2, pd
import sys
from flask import Response, jsonify, make_response, session, Flask
import jwt
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash



##### token verification #####
def token_required_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        #try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        #except:
        #    return jsonify({'Message': 'Invalid token'}), 403
        return func(*args, **kwargs)
    return decorated

#############################


##### Page login #####
@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        try:#
            cur.execute("""
                    SELECT * FROM immo.accounts 
                    WHERE username = %s
                """, (username,))
            user = cur.fetchone()
            conn.commit()
            cur.close()#
            #conn.close()#
            if check_password_hash(user['password'], password):
                token = jwt.encode({'user': user['username'], 'exp': datetime.utcnow() + timedelta(hours=24)}, app.config['SECRET_KEY'])
                session['username'] = username
                session['logged_in'] = True
                session['token'] = token
                return redirect(url_for('index'))
            else:
                return jsonify({'Message': 'Invalid password'})
        except:#
            return jsonify({'Message': 'Invalid username'})


##### Page logout #####
@app.route("/logout")

def logout():
    session.clear()
    return redirect(url_for('index'))

##### Page Gestion utilisateurs #####
@app.route("/users")
@token_required_auth
def users():
    return render_template("authentification/auth.html")

##### Page creation login #####
@app.route('/create', methods=['POST'])
@token_required_auth
def create_user():
#    data = request.get_json()
    
    if request.method == 'POST':
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        username = request.form['username']
        hashed_password = generate_password_hash(request.form['password'], method='sha256')

        cur.execute("INSERT INTO immo.accounts (username, password) VALUES (%s, %s)", (username, hashed_password))
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Compte créée avec succès')
        return redirect(url_for('users'))

