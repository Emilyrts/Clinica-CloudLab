from flask import Blueprint, request, jsonify
from .dependente_model import Dependente
from datetime import datetime
from config import db
from sqlalchemy.exc import IntegrityError

dependente_bp = Blueprint('dependente_routes', __name__, url_prefix='/dependente')

@dependente_bp.route('/', methods=['POST'])
def criar_dependente():
    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    data_nasc = request.json.get('data_nasc')
    titular_id = request.json.get('titular_id')

    data_nasc_objeto = datetime.strptime(data_nasc, '%Y-%m-%d').date()

    novo_dependente = Dependente(
        nome=nome,
        cpf=cpf,
        data_nasc=data_nasc_objeto,
        titular_id=titular_id
    )
    
    db.session.add(novo_dependente)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "CPF já cadastrado"}), 400
        
    return jsonify(novo_dependente.to_dict()), 201


@dependente_bp.route('/', methods=['GET'])
def listar_dependente():
    dependentes = Dependente.query.all()
    if not dependentes:
        return jsonify({'mensagem': 'Nenhum Dependente encontrado.'}), 404
    return jsonify([dependentes.to_dict() for dependentes in dependentes]), 200

@dependente_bp.route('/<int:id>', methods=['GET'])
def obter_dependente(id):
    dependente = Dependente.query.get_or_404(id)
    return jsonify(dependente.to_dict()), 200

@dependente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_dependente(id):
    dependente = Dependente.query.get_or_404(id)

    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    data_nasc = request.json.get('data_nasc')

    if cpf and Dependente.query.filter(Dependente.cpf == cpf, Dependente.id != id).first():
        return jsonify({"error": "CPF já cadastrado para outro dependente"}), 400

    if nome:
        dependente.nome = nome
        
    if cpf:
        dependente.cpf = cpf

    if data_nasc:
        try:
            data_nasc_objeto = datetime.strptime(data_nasc, '%Y-%m-%d').date()
            dependente.data_nasc = data_nasc_objeto
        except ValueError:
            return jsonify({"error": "Formato de data inválido. Use AAAA-MM-DD"}), 400

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erro de integridade ao atualizar dependente (CPF ou outro campo)"}), 500
    
    return jsonify(dependente.to_dict()), 200

@dependente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_dependente(id):
    dependente = Dependente.query.get_or_404(id)
    db.session.delete(dependente)
    db.session.commit()
    return '', 204