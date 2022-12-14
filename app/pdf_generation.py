#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app, DB_HOST, DB_NAME, DB_USER, DB_PASS, DB_PORT, request, render_template, flash, redirect, url_for, psycopg2
import sys
from flask import Response, Flask, render_template, make_response
from datetime import datetime
import pdfkit
#config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
from functools import wraps
from flask import jsonify, session
import jwt

##### token verification #####
def token_required_pdf(func):
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


##### Pdf facture #####
@app.route("/<idcontrat>/pdf")
@token_required_pdf
def pdf(idcontrat):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)#
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s= open("app/sql/paiements.sql").read()
    cur.execute(s.format(idcontrat))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    conn.close()#
    rendered = render_template('pdf/facture.html', paiements = data, id_contrat = idcontrat)
    pdf= pdfkit.from_string(rendered, False) #, configuration=config
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

@app.route("/<idcontrat>/pdf_cloture")
@token_required_pdf
def pdf_cloturation(idcontrat):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)#
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s= open("app/sql/paiements.sql").read()
    cur.execute(s.format(idcontrat))
    data = cur.fetchall()
    conn.commit()
    cur.close()#
    conn.close()#
    rendered = render_template('pdf/facture_finale.html', paiements = data, id_contrat = idcontrat)
    pdf= pdfkit.from_string(rendered, False)#, configuration=config
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
    return response

@app.route("/contrats/contrat/<string:id>/quittance", methods=['POST'])
@token_required_pdf
def quittance(id):
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT)#
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        date_quittance = request.form['date_quittance']
        s= open("app/sql/paiements.sql").read()
        cur.execute(s.format(id))
        data = cur.fetchall()
        conn.commit()
        cur.close()#
        conn.close()#

        date_cible = datetime.strptime(date_quittance, '%Y-%m-%d').date()

        Bool_date_quittance_max = data[0][37].date() > date_cible
        Bool_date_debut = data[0][21] < date_cible

        liste_mois = ["de janvier", "de f??vrier", "de mars", "d'avril", "de mai", "de juin", "de juillet", "d'ao??t", "de septembre", "d'octobre", "de novembre", "de d??cembre"]

        if Bool_date_debut:
            if Bool_date_quittance_max:
                if data[0][37].year > date_cible.year:
                    message_quittance = "Quittance de loyer accord??e pour le mois " + liste_mois[date_cible.month-1] + " " + str(date_cible.year)
                elif data[0][37].month > date_cible.month:
                    message_quittance = "Quittance de loyer accord??e pour le mois " + liste_mois[date_cible.month-1] + " " + str(date_cible.year)
                elif data[0][37].month == date_cible.month:
                    message_quittance = "Le mois " + liste_mois[date_cible.month-1] + " n'est pas encore r??gl?? en totalit?? "
                else:
                    message_quittance = "Erreur, veuillez contacter l'administrateur"
            else:
                message_quittance = "Quittance refus??e pour la date demand??e"
        else:
            message_quittance = "la date demand??e pour la quittance est ant??rieur ?? la date de d??but du contrat"

        rendered = render_template('pdf/quittance.html', paiements = data, id_contrat = id, date_quittance = date_quittance, message_quittance = message_quittance)
        pdf= pdfkit.from_string(rendered, False) #, configuration=config
        response = make_response(pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'inline; filename=output.pdf'
        return response