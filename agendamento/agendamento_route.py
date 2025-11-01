from flask import Blueprint, request, jsonify
from .agendamento_model import Agendamento
from config import db
from datetime import datetime

agendamento_bp = Blueprint('agedamento_routes', __name__, url_prefix= '/agendamentos')

@agendamento_bp.route('/', methods=['POST'])
@agendamento_bp.route('/', methods=['POST'])
def criar_agendamento():
    try:
        data = request.get_json()

        novo = Agendamento(
            data_hora=datetime.strptime(data['data_hora'], "%Y-%m-%d %H:%M:%S"),
            status=data.get('status', 'pendente'),  # default 'pendente'
            fk_paciente=data['fk_paciente'],
            fk_exame=data['fk_exame']
        )

        db.session.add(novo)
        db.session.commit()

        return jsonify({"mensagem": "Agendamento criado com sucesso!", "agendamento": novo.to_dict()}), 201

    except Exception as e:
        return jsonify({"erro": str(e)}), 400


@agendamento_bp.route('/', methods=['GET'])
def listar_agendamentos():
    agendamentos = Agendamento.query.all()

    if not agendamentos:
        return jsonify({'mensagem': 'Nenhum agendamento encontrado.'}), 404
   
    return jsonify([agendamento.to_dict() for agendamento in agendamentos]), 200

@agendamento_bp.route('/<int:id>', methods=['GET'])
def obter_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    if agendamento:
        return jsonify({'mensagem': 'Voce esta tentando buscar uma agndamento que nao existe'}), 404
    
    return jsonify(agendamento.to_dict()), 200


@agendamento_bp.route('/<int:id_agendamento>', methods=['PUT'])
def atualizar_agendamento(id_agendamento):
    agendamento = Agendamento.query.get(id_agendamento)
    if not agendamento:
        return jsonify({'mensagem': 'Agendamento não encontrado.'}), 404

    data = request.get_json()

    # Atualiza apenas os campos enviados
    agendamento.data_hora = data.get('data_hora', agendamento.data_hora)
    agendamento.status = data.get('status', agendamento.status)

    db.session.commit()

    return jsonify({
        'mensagem': 'Agendamento atualizado com sucesso.',
        'agendamento': agendamento.to_dict()
    }), 200

@agendamento_bp.route('/<int:id_agendamento>', methods=['DELETE'])
def deletar_agendamento(id_agendamento):
    agendamento = Agendamento.query.get(id_agendamento)
    if not agendamento:
        return jsonify({'mensagem': 'Agendamento não encontrado.'}), 404

    db.session.delete(agendamento)
    db.session.commit()

    return jsonify({'mensagem': 'Agendamento deletado com sucesso.'}), 200




