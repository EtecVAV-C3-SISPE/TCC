import datetime
from peewee import Model, CharField, TextField, DateTimeField, DateField, ForeignKeyField, BooleanField
from database.database import db #importa o banco de dados db instanciado no arquivo database da pasta database
from datetime import date

class BaseModel(Model):
    class Meta:
        database = db

class Pais(BaseModel):
    nome = CharField()
    email = CharField()
    senha = CharField()
    aprovado = BooleanField(default=False)

class Professores(BaseModel):
    nome = CharField()
    email = CharField()
    senha = CharField()

class Noticias(BaseModel):
    titulo = CharField()
    conteudo = TextField()
    autor = CharField()  # pode ser nome do professor, admin, etc.
    data_publicacao = DateTimeField(default=datetime.datetime.now)

class Aluno(BaseModel):
    nome = CharField()
    serie = CharField()            # série/turma
    professor_responsavel = ForeignKeyField(Professores, backref='alunos')

class Calendario(BaseModel):
    titulo = CharField()
    descricao = TextField()
    data_evento = DateField()
    criado_em = DateField(default=datetime.datetime.now)



class Diario(BaseModel):
    aluno = ForeignKeyField(Aluno, backref="presencas")
    professor = ForeignKeyField(Professores, backref="presencas")
    data = DateField(default=date.today)
    presente = BooleanField(default=True)

class Presenca(BaseModel):
    aluno = ForeignKeyField(Aluno, backref='presencas')           # refere-se ao modelo Aluno
    professor = ForeignKeyField(Professores, backref='presencas') # refere-se ao modelo Professores
    data = DateField(default=date.today)
    presente = BooleanField(default=True)