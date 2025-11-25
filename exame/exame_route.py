from flask import Blueprint, request, jsonify, render_template
from config import db
from exame.exame_model import Exame

exame_bp = Blueprint('exame_bp', __name__, url_prefix='/exames')

@exame_bp.route('/', methods=['GET'])
def mostrar_pagina():
    pass
    # return render_template('')

@exame_bp.route('/criar_exame', methods=['POST'])
def criar_exame():
    data = request.get_json()
    novo_exame = Exame(
        tipo=data.get('tipo'),
        descricao=data.get('descricao')
    )
    db.session.add(novo_exame)
    db.session.commit()
    return jsonify({
        "id": novo_exame.id,
        "tipo": novo_exame.tipo,
        "descricao": novo_exame.descricao
    }), 201

@exame_bp.route('/<int:id>', methods=['GET'])
def buscar_exame(id):
    exame = Exame.query.get(id)
    if not exame:
        return jsonify({"mensagem": "Exame não encontrado"}), 404
    return jsonify(exame.to_dict()), 200


@exame_bp.route('/', methods=['GET'])
def listar_exames():
    exames = Exame.query.all()
    return jsonify([{
        "id": exame.id,
        "tipo": exame.tipo,
        "descricao": exame.descricao
    } for exame in exames]), 200

@exame_bp.route('/<int:id>', methods=['PUT'])
def atualizar_exame(id):
    exame = Exame.query.get(id)
    if not exame:
        return jsonify({"mensagem": "Exame não encontrado"}), 404

    data = request.get_json()
    exame.tipo = data.get('tipo', exame.tipo)
    exame.descricao = data.get('descricao', exame.descricao)

    db.session.commit()
    return jsonify(exame.to_dict()), 200


@exame_bp.route('/<int:id>', methods=['DELETE'])
def deletar_exame(id):
    exame = Exame.query.get(id)
    if not exame:
        return jsonify({"mensagem": "Exame não encontrado"}), 404
    db.session.delete(exame)
    db.session.commit()
    return jsonify({"mensagem": f"Exame {id} deletado com sucesso"}), 200
