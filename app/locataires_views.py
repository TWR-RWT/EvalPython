#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, conn, request, render_template, flash, redirect, url_for, psycopg2, pd
from functools import wraps
from flask import jsonify, session
import jwt

##### token verification #####
def token_required_loc(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = session.get('token')
        if not token:
            return jsonify({'Alert!': 'Token is missing!'}), 401
        try:#
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:#
            return jsonify({'Message': 'Invalid token'}), 403#
        return func(*args, **kwargs)
    return decorated


@app.route("/locataires")
@token_required_loc
def locataires():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM immo.locataires"
    cur.execute(s) # Execute the SQL
    list_locataires = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('locataires/index.html', list_locataires=list_locataires)

@app.route("/locataires/ajout_locataire", methods = ['POST'])
@token_required_loc
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
        cur.close()#
        #conn.close()#
        flash('Locataire ajouté avec succès')
        return redirect(url_for('locataires'))


@app.route("/locataires/locataire/<id>", methods=['POST', 'GET'])
@token_required_loc
def locataire_modif(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM immo.locataires WHERE id_locataire = %s', (id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('locataires/locataire_modif.html', locataire = data[0])

@app.route("/locataires/locataire/<id>/modif", methods=['POST'])
@token_required_loc
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
        cur.close()#
        #conn.close()#
        flash('Locataire modifié avec succès')
        return redirect(url_for('locataires'))

@app.route("/locataires/locataire/<string:id>/suppr", methods=['POST', 'GET'])
@token_required_loc
def locataire_suppr(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM immo.locataires WHERE id_locataire = {0}'.format(id))
    conn.commit()
    cur.close()#
    #conn.close()#
    flash('Locataire supprimé avec succès')
    return redirect(url_for('locataires'))