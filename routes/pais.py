from flask import Blueprint, render_template, request, redirect, url_for, session
from database.models.pais import Pais
from peewee import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

pais_route = Blueprint('pais', __name__)

@pais_route.route('/login', methods=["GET", "POST"])
def login_pais():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        try:
            # busca no banco de dados pelo email
            pai = Pais.get(Pais.email == email)

            # verifica senha com hash
            if check_password_hash(pai.senha, senha):
                pai = Pais.get(Pais.email == email)
                session["user_id"] = pai.id
                session["role"] = "pai"
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('form_pais.html', erro="E-mail ou senha incorretos.")

        except DoesNotExist:
            # email não encontrado
            return render_template('form_pais.html', erro="E-mail ou senha incorretos.")

    return render_template('form_pais.html')
        

@pais_route.route('/registrar', methods=["GET", "POST"])
def registro_pais():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verifica se já existe usuário
        if Pais.select().where((Pais.nome == nome) | (Pais.email == email)).exists():
            return redirect(url_for("registro_pais"))

        # Cria o usuário com a senha criptografada
        senha_hash = generate_password_hash(senha)
        Pais.create(nome=nome, email=email, senha=senha_hash)

        return redirect(url_for("main.dashboard"))

    return render_template("registro.html")