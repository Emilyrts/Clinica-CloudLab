from flask import Blueprint, request, jsonify
from config import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

from encaminhamento.encaminhamento_model import Encaminhamento
from paciente.paciente_model import Paciente
from dependente.dependente_model import Dependente
from exame.exame_model import Exame

encaminhamento_bp = Blueprint('encaminhamento_routes', __name__, url_prefix='/encaminhamentos')


@encaminhamento_bp.route('/', methods=['POST'])
def criar_encaminhamento():
    try:
        data = request.get_json()
        descricao = data.get("descricao")
        arquivo_url = data.get("arquivo_url")
        medico_nome = data.get("medico_nome")
        medico_crm = data.get("medico_crm")

        paciente_id = data.get("paciente_id")
        dependente_id = data.get("dependente_id")
        exame_id = data.get("exame_id")

        if not paciente_id and not dependente_id:
            return jsonify({"erro": "Informe paciente_id ou dependente_id."}), 400

        if paciente_id:
            paciente = Paciente.query.get(paciente_id)
            if not paciente:
                return jsonify({"erro": "Paciente não encontrado."}), 404

        if dependente_id:
            dependente = Dependente.query.get(dependente_id)
            if not dependente:
                return jsonify({"erro": "Dependente não encontrado."}), 404

            if paciente_id and dependente.titular_id != paciente_id:
                return jsonify({"erro": "Este dependente não pertence ao paciente informado."}), 403

        exame = Exame.query.get(exame_id) 
        if not exame:
            return jsonify({"erro": "Tipo de exame não encontrado."}), 404

        novo = Encaminhamento(
            descricao=descricao,
            arquivo_url=arquivo_url,
            medico_nome=medico_nome,
            medico_crm=medico_crm,
            paciente_id=paciente_id,
            dependente_id=dependente_id,
            exame_id=exame_id
        )

        db.session.add(novo)
        db.session.commit()

        return jsonify({
            "mensagem": "Encaminhamento criado com sucesso!",
            "encaminhamento": novo.to_dict()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"erro": "Erro de integridade no banco de dados."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500


@encaminhamento_bp.route('/<int:id_enc>', methods=['PUT'])
def atualizar_encaminhamento(id_enc):
    enc = Encaminhamento.query.get_or_404(id_enc)
    data = request.get_json()

    enc.descricao = data.get("descricao", enc.descricao)
    enc.arquivo_url = data.get("arquivo_url", enc.arquivo_url)
    enc.medico_nome = data.get("medico_nome", enc.medico_nome)
    enc.medico_crm = data.get("medico_crm", enc.medico_crm)

    paciente_id = data.get("paciente_id")
    dependente_id = data.get("dependente_id")

    if paciente_id is not None:
        if paciente_id and not Paciente.query.get(paciente_id):
            return jsonify({"erro": "Paciente não encontrado."}), 404
        enc.paciente_id = paciente_id

    if dependente_id is not None:
        dependente = None
        if dependente_id:
            dependente = Dependente.query.get(dependente_id)
            if not dependente:
                return jsonify({"erro": "Dependente não encontrado."}), 404

        paciente_a_validar = paciente_id if paciente_id is not None else enc.paciente_id

        if dependente and paciente_a_validar and dependente.titular_id != paciente_a_validar:
            return jsonify({"erro": "Este dependente não pertence ao paciente informado."}), 403

        enc.dependente_id = dependente_id

    if "exame_id" in data:
        exame = Exame.query.get(data["exame_id"]) 
        if not exame:
            return jsonify({"erro": "Exame não encontrado."}), 404
        enc.exame_id = data["exame_id"]

    try:
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({"erro": "Erro de integridade ao atualizar encaminhamento."}), 500

    return jsonify({
        'mensagem': 'Encaminhamento atualizado com sucesso.',
        'encaminhamento': enc.to_dict()
    }), 200


# Listar todos
@encaminhamento_bp.route('/', methods=['GET'])
def listar_encaminhamentos():
    encaminhamentos = Encaminhamento.query.all()

    if not encaminhamentos:
        return jsonify({'mensagem': 'Nenhum encaminhamento encontrado.'}), 404

    return jsonify([e.to_dict() for e in encaminhamentos]), 200



# Obter por ID
@encaminhamento_bp.route('/<int:id_enc>', methods=['GET'])
def obter_encaminhamento(id_enc):
    enc = Encaminhamento.query.get(id_enc)
    if not enc:
        return jsonify({'mensagem': 'Encaminhamento não encontrado.'}), 404

    return jsonify(enc.to_dict()), 200


# Deletar
@encaminhamento_bp.route('/<int:id_enc>', methods=['DELETE'])
def deletar_encaminhamento(id_enc):
    enc = Encaminhamento.query.get(id_enc)
    if not enc:
        return jsonify({'mensagem': 'Encaminhamento não encontrado.'}), 404

    db.session.delete(enc)
    db.session.commit()

    return jsonify({'mensagem': 'Encaminhamento deletado com sucesso.'}), 200
