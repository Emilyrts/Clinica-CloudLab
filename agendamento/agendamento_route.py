from flask import Blueprint, request, jsonify, render_template
from .agendamento_model import Agendamento
from exame.exame_model import Exame
from config import db
from datetime import datetime

agendamento_bp = Blueprint('agendamento_routes', __name__, url_prefix= '/agendamentos')

@agendamento_bp.route('/agendar', methods=['GET'])
def realizar_agendamento():
    exames = Exame.query.all()
    return render_template('agendar.html', exames_disponiveis=exames) #VAI PARA A PAGINA DE AGENDAR EXAME

@agendamento_bp.route('/visualizarAgendamentos', methods=['GET'])
def mostrarAgendamentos():
    return render_template('agendamentos.html') #MOSTRA TODOS OS EXAMES AGENDADOS

@agendamento_bp.route('/criar_agendamento', methods=['POST'])
def criar_agendamento():
    try:
        data = request.get_json()

        if not all(k in data for k in ('data_hora', 'fk_paciente', 'fk_exame')):
            return jsonify({"erro": "Campos obrigatórios ausentes."}), 400
        
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

# LISTA UM HISTORICO COM OUTROS DADOS
@agendamento_bp.route('/historico', methods=['GET'])
def listar_historico():
    agendamentos = Agendamento.query.all()
    lista_agendamentos = [agendamento.to_dict() for agendamento in agendamentos]
    return render_template('historico.html', 
                            agendamentos=lista_agendamentos), 200

@agendamento_bp.route('/<int:id>', methods=['GET'])
def obter_agendamento(id):
    agendamento = Agendamento.query.get_or_404(id)
    return jsonify(agendamento.to_dict()), 200


@agendamento_bp.route('/<int:id_agendamento>', methods=['PUT'])
def atualizar_agendamento(id_agendamento):
    agendamento = Agendamento.query.get(id_agendamento)
    if not agendamento:
        return jsonify({'mensagem': 'Agendamento não encontrado.'}), 404

    data = request.get_json()

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




