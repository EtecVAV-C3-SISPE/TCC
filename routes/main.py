from flask import Blueprint, render_template, request, redirect, url_for
from database.models.pais import Noticias, Calendario

main_route = Blueprint('main', __name__)
calendario_bp = Blueprint("calendario", __name__)


@main_route.route('/')
def home():
    return render_template('1-login.html')

@main_route.route('/dashboard')
def dashboard():
    return render_template('2-dashboard.html')

@main_route.route('/noticias')
def listar_noticias():
    noticias = Noticias.select().order_by(Noticias.data_publicacao.desc())
    return render_template('3-noticias.html', noticias=noticias)

@calendario_bp.route('/calendario', methods =["GET", "POST"])
def calendario():
    if request.method == "POST":
        titulo = request.form.get("titulo")
        descricao = request.form.get("descricao")
        data_evento = request.form.get("data_evento")

        Calendario.create(
            titulo=titulo,
            descricao=descricao,
            data_evento=data_evento
        )
        return redirect(url_for("calendario.calendario"))

    eventos = Calendario.select().order_by(Calendario.data_evento)
    return render_template("4-calendario.html", eventos=eventos )

@calendario_bp.route("/calendario/editar/<int:evento_id>", methods=["GET", "POST"])
def editar_evento(evento_id):
    evento = Calendario.get_or_none(Calendario.id == evento_id)
    if not evento:
        return "Evento não encontrado", 404

    if request.method == "POST":
        evento.titulo = request.form.get("titulo")
        evento.descricao = request.form.get("descricao")
        evento.data_evento = request.form.get("data_evento")
        evento.save()
        return redirect(url_for("calendario.calendario"))

    return render_template("editar_evento.html", evento=evento)

@calendario_bp.route("/calendario/excluir/<int:evento_id>", methods=["POST"])
def excluir_evento(evento_id):
    evento = Calendario.get_or_none(Calendario.id == evento_id)
    if not evento:
        return "Evento não encontrado", 404

    evento.delete_instance()
    return redirect(url_for("calendario.calendario"))

@main_route.route('/passeios')
def passeios():
   return render_template('4-passeios.html')

@main_route.route('/passeios/<int:id>')
def detalhes_passeio(id):
    return render_template('4-passeio_detalhes.html', id=id)

@main_route.route('/passeios/<int:id>/anexos', methods=['GET', 'POST'])
def anexos(id):
    if request.method == 'POST':
        pass  
    return render_template('4-passeio_anexos.html', id=id)


