from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.models.pais import Pais, Diario, Aluno, Presenca
from peewee import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash

pais_route = Blueprint('pais', __name__)

@pais_route.route('/login_pais', methods=["GET", "POST"])
def login_pais():
    if request.method == "POST":
        email = request.form["email"]
        senha = request.form["senha"]

        pai = Pais.get_or_none(Pais.email == email)
        if not pai or not check_password_hash(pai.senha, senha):
            flash("E-mail ou senha inválidos.", "danger")
            return redirect(url_for("auth.login_pai"))

        if not pai.aprovado:
            flash("Cadastro ainda não aprovado por um professor.", "warning")
            return redirect(url_for("auth.login_pai"))

        # Aqui você seta a sessão
        session["user_id"] = pai.id
        session["role"] = "pai"
        flash("Bem-vindo!", "success")
        return redirect(url_for("main.dashboard"))

    return render_template("login_pai.html")
        

@pais_route.route('/registrar', methods=["GET", "POST"])
def registro_pais():
    if request.method == "POST":
        nome = request.form["nome"]
        email = request.form["email"]
        senha = request.form["senha"]

        # Verifica se já existe usuário
        if Pais.select().where((Pais.nome == nome) | (Pais.email == email)).exists():
            return redirect(url_for("main.home"))

        Pais.create(
            nome=nome,
            email=email,
            senha=generate_password_hash(senha),
            aprovado=False
        )
        flash("Cadastro enviado! Aguarde aprovação de um professor.", "info")
        return redirect(url_for("main.dashboard"))

    return render_template("registro_pai.html")

"""
@pais_route.route("/presencas")
def presencas_pais():
    # verificar sessão do pai
    if session.get("role") != "pai" and session.get("pai_id") is None:
        flash("Acesso negado. Faça login como responsável.", "danger")
        return redirect(url_for("main.dashboard"))

    pai_id = session.get("user_id") if session.get("role") == "pai" else session.get("pai_id")

    # pegar filhos do pai (ajuste o campo se seu Aluno usa outro nome, ex: aluno.pai)
    filhos = Aluno.select().where(Aluno.pai == pai_id)
    if not filhos.exists():
        # se não há relação, você pode querer mostrar mensagem
        flash("Nenhum filho encontrado vinculado à sua conta.", "warning")
        return render_template("lista_presencas_pais.html", presencas=[])

    presencas = Presenca.select().where(Presenca.aluno.in_(filhos)).order_by(Presenca.data.desc())
    return render_template("lista_presencas_pais.html", presencas=presencas)
"""