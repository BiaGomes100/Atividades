from db import db
from flask import jsonify, request
from sqlalchemy.dialects.postgresql import JSON

class Atividade(db.Model):
    __tablename__ = 'atividades'

    id = db.Column(db.Integer, primary_key=True)
    id_disciplina = db.Column(db.Integer, nullable=False)
    enunciado = db.Column(db.String(255), nullable=False)
    respostas = db.Column(JSON, nullable=True)  # Lista de dicionários

    def __init__(self, id_disciplina, enunciado, respostas=None):
        self.id_disciplina = id_disciplina
        self.enunciado = enunciado
        self.respostas = respostas or []

    def to_dict(self):
        return {
            'id': self.id,
            'id_disciplina': self.id_disciplina,
            'enunciado': self.enunciado,
            'respostas': self.respostas
        }

class AtividadeNotFound(Exception):
    pass


# Funções auxiliares
def listar_atividades():
    atividades = Atividade.query.all()
    return jsonify([a.to_dict() for a in atividades])


def obter_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        raise AtividadeNotFound()
    return atividade


def criar_atividade():
    dados = request.json
    id_disciplina = dados.get("id_disciplina")
    enunciado = dados.get("enunciado")
    respostas = dados.get("respostas", [])

    nova_atividade = Atividade(
        id_disciplina=id_disciplina,
        enunciado=enunciado,
        respostas=respostas
    )

    db.session.add(nova_atividade)
    db.session.commit()

    return jsonify({"mensagem": "Atividade criada com sucesso", "atividade": nova_atividade.to_dict()}), 201


def deletar_atividade(id_atividade):
    atividade = Atividade.query.get(id_atividade)
    if not atividade:
        return jsonify({"mensagem": "Atividade não encontrada"}), 404

    db.session.delete(atividade)
    db.session.commit()
    return jsonify({"mensagem": "Atividade deletada com sucesso"}), 200
