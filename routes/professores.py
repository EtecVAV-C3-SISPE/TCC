from flask import Blueprint, render_template, request, redirect, url_for
from database.models.pais import Professores
from peewee import DoesNotExist

professores_route = Blueprint('professores', __name__)

@professores_route.route('/login', methods=["GET", "POST"])
def login_professores():
    if request.method == "POST":
        email = request.form.get("email_inst")
        senha = request.form.get("senha")
        try:
        # busca no banco de dados pelo email
            professor = Professores.get(Professores.email_inst == email)

        # verifica senha
            if professor.senha == senha:
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('form_professores.html', erro="E-mail ou senha incorretos.")

        except DoesNotExist:
            # email não encontrado
            return render_template('form_professores.html', erro="E-mail ou senha incorretos.")

    return render_template('form_professores.html')
        
""" for p in PROFESSORES:
            if p["email_inst"] == email and p["senha"] == senha:
                
                return redirect(url_for('main.dashboard'))

        
        return render_template('form_professores.html', erro="E-mail ou senha incorretos.")
    
    return render_template('form_professores.html')"""