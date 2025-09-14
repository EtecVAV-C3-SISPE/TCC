from flask import Blueprint, render_template, request, redirect, url_for
from database.models.pais import Professores, Noticias
from peewee import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

professores_route = Blueprint('professores', __name__)

@professores_route.route('/login', methods=["GET", "POST"])
def login_professores():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")
        try:
            # busca no banco de dados pelo email
            professor = Professores.get(Professores.email == email)

            # verifica senha com hash
            if check_password_hash(professor.senha, senha):
                professor = Professores.get(Professores.email == email)
                session["user_id"] = professor.id
                session["role"] = "professor" 
                return redirect(url_for('main.dashboard'))
            else:
                return render_template('form_professores.html', erro="E-mail ou senha incorretos.")

        except DoesNotExist:
            # email não encontrado
            return render_template('form_professores.html', erro="E-mail ou senha incorretos.")

    return render_template('form_professores.html')
        

@professores_route.route('/registrar', methods=["GET", "POST"])
def registro_professores():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verifica se já existe usuário
        if Professores.select().where((Professores.nome == nome) | (Professores.email == email)).exists():
            return redirect(url_for("professores.registro_professores"))

        # Cria o usuário com a senha criptografada
        senha_hash = generate_password_hash(senha)
        Professores.create(nome=nome, email=email, senha=senha_hash)

        return redirect(url_for("main.dashboard"))

    return render_template("registro.html")

@professores_route.route('/registrar_noticia', methods=["GET", "POST"])
def registrar_noticia():
    if session.get("role") != "professor":
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        titulo = request.form["titulo"]
        conteudo = request.form["conteudo"]
        autor = request.form["autor"]

        # cria a notícia no banco
        Noticias.create(titulo=titulo, conteudo=conteudo, autor=autor)

        return redirect(url_for("main.listar_noticias"))

    return render_template("registrar_noticia.html")