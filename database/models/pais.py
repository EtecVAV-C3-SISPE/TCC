import datetime
from peewee import Model, CharField, TextField, DateTimeField, DateField
from database.database import db #importa o banco de dados db instanciado no arquivo database da pasta database

class BaseModel(Model):
    class Meta:
        database = db

class Pais(BaseModel):
    nome = CharField()
    email = CharField()
    senha = CharField()

class Professores(BaseModel):
    nome = CharField()
    email = CharField()
    senha = CharField()

class Noticias(BaseModel):
    titulo = CharField()
    conteudo = TextField()
    autor = CharField()  # pode ser nome do professor, admin, etc.
    data_publicacao = DateTimeField(default=datetime.datetime.now)

class Calendario(BaseModel):
    titulo = CharField()
    descricao = TextField()
    data_evento = DateField()
    criado_em = DateField(default=datetime.datetime.now)