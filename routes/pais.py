from flask import Blueprint, render_template, request, redirect, url_for
from database.models.pais import Pais
from peewee import DoesNotExist

pais_route = Blueprint('pais', __name__)

@pais_route.route('/login', methods=["GET", "POST"])
def login_pais():
    if request.method == "POST":
        email = request.form.get("email_inst")
        senha = request.form.get("senha")
        try:
            pai = Pais.get(Pais.email_inst==email)
            if pai.senha == senha:
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('form_pais.html', erro="E-mail ou senha incorretos.")

        except DoesNotExist:
            return render_template('form_pais.html', erro="E-mail ou senha incorretos.")
    return render_template('form_pais.html')
