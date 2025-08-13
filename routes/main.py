from flask import Blueprint, render_template, request, redirect, url_for

main_route = Blueprint('main', __name__)


@main_route.route('/')
def home():
    return render_template('1-login.html')

@main_route.route('/dashboard')
def dashboard():
    return render_template('2-dashboard.html')

@main_route.route('/noticias')
def noticias():
    return render_template('3-noticias.html')

@main_route.route('/calendario')
def calendario():
    return render_template('4-calendario.html')

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

@main_route.route('/diario')
def diario():
    return render_template('5-diario.html')

@main_route.route('/faltas')
def faltas():
    return render_template('5-faltas.html')

