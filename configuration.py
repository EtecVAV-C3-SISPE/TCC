from routes.main import main_route, calendario_bp
from routes.pais import pais_route
from routes.professores import professores_route
from database.database import db
from database.models.pais import Pais, Professores, Noticias, Calendario

def configure_all(app):
    configure_routes(app)
    configure_db()

def configure_routes(app):
    app.register_blueprint(pais_route, url_prefix='/pais')
    app.register_blueprint(professores_route, url_prefix='/professores')
    app.register_blueprint(main_route)
    app.register_blueprint(calendario_bp)

def configure_db():
    db.connect()
    db.create_tables([Pais])
    db.create_tables([Professores])
    db.create_tables([Noticias])
    db.create_tables([Calendario])
