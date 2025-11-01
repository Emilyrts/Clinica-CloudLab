from flask import Blueprint, request, jsonify
from .paciente_model import Paciente
from config import db
from sqlalchemy.exc import IntegrityError

paciente_bp = Blueprint('paciente_routes', __name__, url_prefix='/pacientes')

@paciente_bp.route('/', methods=['POST'])
def criar_paciente():
    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    data_nasc = request.json.get('data_nasc')
    email = request.json.get('email')
    senha = request.json.get('senha')
    telefone = request.json.get('telefone')

    novo_paciente = Paciente(
    nome=nome,
    cpf=cpf,
    data_nasc=data_nasc,
    email=email,
    senha=senha,
    telefone=telefone
)
    
    db.session.add(novo_paciente)

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "CPF já cadastrado"}), 400
    return jsonify(novo_paciente.to_dict()), 201 


@paciente_bp.route('/', methods=['GET'])
def listar_paciente():

    pacientes = Paciente.query.all()
    return jsonify([paciente.to_dict() for paciente in pacientes]), 200

@paciente_bp.route('/<int:id>', methods=['GET'])
def obter_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    return jsonify(paciente.to_dict()), 200

@paciente_bp.route('/<int:id>', methods=['PUT'])
def atualizar_paciente(id):
    paciente = Paciente.query.get_or_404(id)

    nome = request.json.get('nome')
    cpf = request.json.get('cpf')
    data_nasc = request.json.get('data_nasc')
    email = request.json.get('email')
    senha = request.json.get('senha')
    telefone = request.json.get('telefone')

    if cpf and Paciente.query.filter(Paciente.cpf == cpf, Paciente.id != id).first():
        return jsonify({"error": "CPF já cadastrado para outro paciente"}), 400

    if nome: paciente.nome = nome
    if cpf: paciente.cpf = cpf
    if data_nasc: paciente.data_nasc 
    if email: paciente.email = email
    if senha: paciente.senha = senha
    if telefone: paciente.telefone = telefone

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Erro ao atualizar paciente"}), 500

    return jsonify(paciente.to_dict()), 200

@paciente_bp.route('/<int:id>', methods=['DELETE'])
def deletar_paciente(id):
    paciente = Paciente.query.get_or_404(id)
    db.session.delete(paciente)
    db.session.commit()
    return '', 204
