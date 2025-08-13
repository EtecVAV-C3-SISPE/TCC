from peewee import Model, CharField
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
