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
DB_PASS = "1Motdepasse"
DB_PORT="5432"
 
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)

@app.route("/")
def locataires():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM immo.locataires"
    cur.execute(s) # Execute the SQL
    list_locataires = cur.fetchall()
    return render_template('index.html', list_locataires=list_locataires)

@app.route("/ajout_locataire", methods = ['POST'])
def ajout_locataire():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        code_postal = request.form['CP']
        ville = request.form['ville']
        telephone = request.form['telephone']
        email = request.form['email']
        cur.execute("INSERT INTO immo.locataires (nom, prenom, adresse, code_postal, ville, telephone, email) VALUES(%s, %s, %s, %s, %s, %s, %s)", (nom, prenom, adresse, code_postal, ville, telephone, email))
        conn.commit()
        flash('Locataire ajouté avec succès')
        return redirect(url_for('locataires'))


@app.route("/locataire/<id>", methods=['POST', 'GET'])
def locataire_modif(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM immo.locataires WHERE id_locataire = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('locataire_modif.html', locataire = data[0])

@app.route("/locataire/<id>/modif", methods=['POST'])
def locataire_modif_post(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        adresse = request.form['adresse']
        code_postal = request.form['CP']
        ville = request.form['ville']
        telephone = request.form['telephone']
        email = request.form['email']
        cur.execute("""
            UPDATE immo.locataires
            SET nom=%s, prenom=%s, adresse=%s, code_postal=%s, ville=%s, telephone=%s, email=%s
            WHERE id_locataire=%s
        """, (nom, prenom, adresse, code_postal, ville, telephone, email, id))
        conn.commit()
        flash('Locataire modifié avec succès')
        return redirect(url_for('locataires'))

@app.route("/locataire/<string:id>/suppr", methods=['POST', 'GET'])
def locataire_suppr(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM immo.locataires WHERE id_locataire = {0}'.format(id))
    conn.commit()
    flash('Locataire supprimé avec succès')
    return redirect(url_for('locataires'))

app.run(
    host="0.0.0.0",
    port=int("8080"),
    debug=True
)
#flask --app python --debug run

