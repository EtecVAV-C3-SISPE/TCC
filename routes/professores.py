from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from database.models.pais import Professores, Noticias, Diario, Aluno, Presenca, Pais
from peewee import DoesNotExist
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date

professores_route = Blueprint('professores', __name__)

def _is_professor():
    # Verifica a sessão: adapte conforme você guarda role/user_id
    return session.get("role") == "professor" or session.get("professor_id") or session.get("user_id") and session.get("role") == "professor"

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

@professores_route.route('/aprovar_pais')
def aprovar_pais():
    if not _is_professor():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.index"))

    pendentes = Pais.select().where(Pais.aprovado == False)
    return render_template("aprovar_pais.html", pendentes=pendentes)

@professores_route.route("/aprovar_pai/<int:pai_id>/<acao>")
def aprovar_pai(pai_id, acao):
    if not _is_professor():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.dashboard"))

    pai = Pais.get_or_none(Pais.id == pai_id)
    if not pai:
        flash("Pai não encontrado.", "warning")
        return redirect(url_for("professores.aprovar_pais"))

    if acao == "aceitar":
        pai.aprovado = True
        pai.save()
        flash("Cadastro aprovado.", "success")
    elif acao == "recusar":
        pai.delete_instance()
        flash("Cadastro recusado.", "info")

    return redirect(url_for("professores.aprovar_pais"))

@professores_route.route("/aprovar_pai/<int:pai_id>", methods=["POST"])
def aprovar_pai_confirmar(pai_id):
    pai = Pais.get_or_none(Pais.id == pai_id)
    if pai:
        pai.aprovado = True
        pai.save()
    return redirect(url_for("professores.aprovar_pai"))

@professores_route.route('/diario', methods=['GET', 'POST'])
def diario():

    if not _is_professor():
        flash("Acesso negado. Faça login como professor.", "danger")
        return redirect(url_for("main.dashboard"))

    prof_id = session.get("user_id") or session.get("professor_id")
    hoje = date.today()

     # pegar alunos que o professor gerencia (opcional)
    # se tiver campo Aluno.professor_responsavel -> filtra por ele:
    try:
        alunos_query = Aluno.select().where(Aluno.professor_responsavel == prof_id)
        if not alunos_query.exists():
            alunos_query = Aluno.select()  # fallback: todos os alunos
    except Exception:
        alunos_query = Aluno.select()  # se o campo não existir, pega todos

    # carregar presenças já existentes hoje para pré-check
    presenca_hoje = {p.aluno.id: p.presente for p in Presenca.select().where(Presenca.data == hoje)}

    if request.method == "POST":
        for aluno in alunos_query:
            checked = request.form.get(f"aluno_{aluno.id}")  # 'on' se marcado
            presente = True if checked == "on" else False

            # atualiza se já existe registro para o aluno na data, senão cria
            existing = Presenca.get_or_none((Presenca.aluno == aluno) & (Presenca.data == hoje))
            if existing:
                existing.presente = presente
                existing.professor = prof_id  # aceita id ou instância
                existing.save()
            else:
                Presenca.create(aluno=aluno, professor=prof_id, data=hoje, presente=presente)

        flash("Presenças registradas com sucesso.", "success")
        return redirect(url_for("professores.ver_presencas"))

    return render_template("diario.html", alunos=alunos_query, hoje=hoje, presenca_hoje=presenca_hoje)




    alunos = Aluno.select()
    hoje = date.today()

    if request.method == 'POST':
        for aluno in alunos:
            marcado = request.form.get(f'aluno_{aluno.id}')
            Diario.create(
                aluno=aluno,
                professor=session['professor_id'],
                data=hoje,
                presente=(marcado == 'on')
            )
        return redirect(url_for('professores.ver_presencas'))

    return render_template('diario.html', alunos=alunos, hoje=hoje)
    
@professores_route.route('/diario/lista')
def ver_presencas():
    if not _is_professor():
        flash("Acesso negado.", "danger")
        return redirect(url_for("main.dashboard"))

    presencas = Presenca.select().order_by(Presenca.data.desc(), Presenca.aluno)
    return render_template("lista_presencas.html", presencas=presencas)
