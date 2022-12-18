#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, conn, request, render_template, flash, redirect, url_for, psycopg2
from functools import wraps
from flask import jsonify, session
import jwt

##### token verification #####
def token_required_location(func):
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


@app.route("/locations")
@token_required_location
def locations():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM immo.locations"
    cur.execute(s) # Execute the SQL
    list_locations = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('locations/index.html', list_locations=list_locations)

@app.route("/locations/ajout_location", methods = ['POST'])
@token_required_location
def ajout_location():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        adresse = request.form['adresse']
        complement = request.form['complement']
        code_postal = request.form['CP']
        ville = request.form['ville']
        cur.execute("INSERT INTO immo.locations (adresse, complement, code_postal, ville) VALUES(%s, %s, %s, %s)", (adresse, complement, code_postal, ville))
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Location ajouté avec succès')
        return redirect(url_for('locations'))

@app.route("/locations/location/<id>", methods=['POST', 'GET'])
@token_required_location
def location_modif(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('SELECT * FROM immo.locations WHERE id_location = %s', (id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('locations/location_modif.html', location = data[0])

@app.route("/locations/location/<id>/modif", methods=['POST'])
@token_required_location
def location_modif_post(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        adresse = request.form['adresse']
        complement = request.form['complement']
        code_postal = request.form['CP']
        ville = request.form['ville']
        cur.execute("""
            UPDATE immo.locations
            SET adresse=%s, complement=%s, code_postal=%s, ville=%s
            WHERE id_location=%s
        """, (adresse, complement, code_postal, ville, id))
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Bien modifié avec succès')
        return redirect(url_for('locations'))

@app.route("/locations/location/<string:id>/suppr", methods=['POST', 'GET'])
@token_required_location
def location_suppr(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM immo.locations WHERE id_location = {0}'.format(id))
    conn.commit()
    cur.close()#
    #conn.close()#
    flash('Bien supprimé avec succès')
    return redirect(url_for('locations'))