#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, conn, request, render_template, flash, redirect, url_for, psycopg2
import sys
from flask import Response
from functools import wraps
from flask import jsonify, session
import jwt

##### token verification #####
def token_required_contr(func):
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


##### Page Index #####
@app.route("/contrats")
@token_required_contr
def contrats():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    #s = "SELECT * FROM immo.contrats_loc"
    s= open("app/sql/list_contratspaiements.sql").read()
    cur.execute(s) # Execute the SQL
    list_contrats = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('contrats/index.html', list_contrats=list_contrats)




##### Page Index #####
@app.route("/contrats/page_ajout_contrat")
@token_required_contr
def page_ajout_contrat():
    return render_template('contrats/contrat_ajout.html')

@app.route("/contrats/ajout_contrat", methods = ['POST'])
@token_required_contr
def ajout_contrat():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id_location = request.form['id_location']
        id_locataire = request.form['id_locataire']

        agence = request.form['agence']
        frais_agence = request.form['frais_agence']

        date_debut = request.form['date_debut']
        depot_garantie = request.form['depot_garantie']

        loyer = request.form['loyer']
        charges = request.form['charges']

        cur.execute("""INSERT INTO immo.contrats_loc (id_location, id_locataire, agence, frais_agence, 
        date_debut, depot_garantie, loyer, charges) 
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", 
        (id_location, id_locataire, agence, frais_agence, 
        date_debut, depot_garantie, loyer, charges))
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Contrat ajouté avec succès')
        return redirect(url_for('contrats'))

@app.route("/contrats/contrat/<string:id>/suppr", methods=['POST', 'GET'])
@token_required_contr
def contrat_suppr(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute('DELETE FROM immo.contrats_loc WHERE id_contrat = {0}'.format(id))
    conn.commit()
    cur.close()#
    #conn.close()#
    flash('Contrat supprimé avec succès')
    return redirect(url_for('contrats'))




##### Page contrat_modif #####
@app.route("/contrats/contrat/<string:id>", methods=['POST', 'GET'])
@token_required_contr
def contrat_modif(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
            SELECT * FROM immo.contrats_loc
            WHERE (id_contrat = %s)
        """, (id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('contrats/contrat_modif.html', contrat = data[0])

@app.route("/contrats/contrat/<string:id>/modif", methods=['POST'])
@token_required_contr
def contrat_modif_post(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id_location = request.form['id_location']
        id_locataire = request.form['id_locataire']

        agence = request.form['agence']
        frais_agence = request.form['frais_agence']

        depot_garantie = request.form['depot_garantie']
        loyer = request.form['loyer']
        charges = request.form['charges']

        date_debut = request.form['date_debut']

        cur.execute("""
            UPDATE immo.contrats_loc
            SET id_location=%s, id_locataire=%s, agence=%s, frais_agence=%s, 
            depot_garantie=%s, loyer=%s, charges=%s, 
            date_debut=%s
            WHERE id_contrat = %s
        """, (id_location, id_locataire, agence, frais_agence, depot_garantie, loyer, charges, date_debut, id))

        if request.form['date_fin'] != '':
            date_fin = request.form['date_fin']
            cur.execute("""
            UPDATE immo.contrats_loc
            SET date_fin=%s
            WHERE id_contrat = %s
        """, (date_fin,  id))
            

        if request.form['date_etat_des_lieux'] != '':
            date_etat_des_lieux = request.form['date_etat_des_lieux']
            cur.execute("""
            UPDATE immo.contrats_loc
            SET date_etat_des_lieux=%s
            WHERE id_contrat = %s
        """, (date_etat_des_lieux,  id))

        if request.form['montant_etat_des_lieux'] != '':
            montant_etat_des_lieux = request.form['montant_etat_des_lieux']
            cur.execute("""
            UPDATE immo.contrats_loc
            SET montant_etat_des_lieux=%s
            WHERE id_contrat = %s
        """, (montant_etat_des_lieux,  id))
        
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Contrat modifié avec succès')
        return redirect(url_for('contrats'))
    


##########################################
#### Page paiements ####
@app.route("/contrats/contrat/<string:id>/paiements")
@token_required_contr
def page_paiements(id):

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s= open("app/sql/paiements.sql").read()
    cur.execute(s.format(id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('contrats/paiements.html', paiements = data, id_contrat = id)

@app.route("/contrats/contrat/page_ajout_paiement/<id>", methods = ['POST', 'GET'])
@token_required_contr
def page_ajout_paiement(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
            SELECT * FROM immo.contrats_loc
            WHERE (id_contrat = %s)
        """, (id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('/contrats/paiement_ajout.html', contrat = data[0])




###### Page ajout paiement #####
@app.route("/contrats/contrat/<string:id>/paiement_ajout", methods=['POST'])
@token_required_contr
def paiement_ajout(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        id_contrat = request.form['id_contrat']
        date_paiement = request.form['date_paiement']
        montant = request.form['montant']
        paiement_type = request.form['paiement_type']
        complement = request.form['complement']
        cur.execute("""INSERT INTO immo.paiements (id_contrat, date_paiement, montant, paiement_type, complement) 
        VALUES(%s, %s, %s, %s, %s)""", 
        (id_contrat, date_paiement, montant, paiement_type, complement))
        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Paiement ajouté avec succès')
        return redirect(url_for('page_paiements', id = id))







#### Page paiement_modif ####
@app.route("/paiement/<id>/paiement_modif", methods=['POST', 'GET'])
@token_required_contr
def paiement_modif(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
            SELECT * FROM immo.paiements
            WHERE (id_paiement = %s)
        """, (id))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    #conn.close()#
    return render_template('contrats/paiement_modif.html', paiement = data[0])

@app.route("/contrat/<idcontrat>/paiement/<idpaiement>/suppr", methods=['POST', 'GET'])
@token_required_contr
def paiement_supprimer(idcontrat, idpaiement):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute("""
            DELETE FROM immo.paiements
            WHERE (id_paiement = %s)
        """, (idpaiement))
    conn.commit()
    cur.close()#
    #conn.close()#
    flash('Paiement supprimé avec succès')
    return redirect(url_for('page_paiements', id = idcontrat))

@app.route("/contrat/<idcontrat>/paiement/<idpaiement>/modif", methods=['POST'])
@token_required_contr
def paiement_modif_post(idcontrat, idpaiement):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        date_paiement = request.form['date_paiement']
        paiement_type = request.form['paiement_type']

        montant = request.form['montant']
        complement = request.form['complement']

        cur.execute("""
            UPDATE immo.paiements
            SET date_paiement=%s, paiement_type=%s, complement=%s, montant=%s 
            WHERE id_paiement=%s
        """, (date_paiement, paiement_type, complement, montant, idpaiement))

        conn.commit()
        cur.close()#
        #conn.close()#
        flash('Contrat modifié avec succès')
        return redirect(url_for('page_paiements', id = idcontrat))