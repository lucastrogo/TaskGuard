'''Arquivo para as classes do banco de dados'''

from . import db
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(150), unique=True)
    senha = db.Column(db.String(150))
    nome = db.Column(db.String(150))
    materias = db.relationship('Materia')

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    nome = db.Column(db.String(150))
    topicos = db.relationship('Topico')

class Topico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_materia = db.Column(db.Integer, db.ForeignKey('materia.id'))
    nome = db.Column(db.String(150))
    completo = db.Column(db.Boolean, default=False)
    prazo = db.Column(db.String(10))
    anotacoes = db.relationship('Anotacao')

class Anotacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_topico = db.Column(db.Integer, db.ForeignKey('topico.id'))
    texto = db.Column(db.Text, nullable=False)