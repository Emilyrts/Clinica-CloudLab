from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from config import db
from notificacao.notificacao_model import Notificacao
from datetime import datetime

from paciente.paciente_model import Paciente

notificacao_bp = Blueprint('notificacao_routes', __name__, url_prefix='/notificacoes')


@notificacao_bp.route('/', methods=['POST'])
def criar_notificação():
    try:
        data = request.get_json()
        mensagem = data.get("mensagem")
        paciente_id = data.get("paciente_id")

        if not mensagem:
            return jsonify({"erro": "É necessário uma mensagem."}), 400
        
        if not paciente_id:
            return jsonify({"erro": "Informe paciente_id."}), 400

        paciente = Paciente.query.get(paciente_id)
        if not paciente:
            return jsonify({"erro": "Paciente não encontrado."}), 404
        
        nova_notificacao = Notificacao(
            mensagem=mensagem,
            paciente_id=paciente_id,
        )
        db.session.add(nova_notificacao)
        db.session.commit()
        return jsonify({
            "mensagem": "Notificação criada com sucesso!",
            "notificacao": nova_notificacao.to_dict()
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": "Erro de integridade no banco de dados."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500


# colocar ?paciente_id=1 na frente para acessar o paciente
@notificacao_bp.route('/minhasnotificacoes', methods=['GET'])
def listar_minhas_notificacoes():
    paciente_id = request.args.get('paciente_id', type=int) 
    
    if not paciente_id:
        return jsonify({"erro": "ID do paciente é obrigatório."}), 400

    notificacoes = Notificacao.query.filter_by(paciente_id=paciente_id).order_by(Notificacao.data_envio.desc()).all()

    return jsonify([n.to_dict() for n in notificacoes]), 200


@notificacao_bp.route('/<int:id_notificacao>/lida', methods=['PATCH'])
def marcar_como_lida(id_notificacao):
    notificacao = Notificacao.query.get_or_404(id_notificacao)

    if notificacao.lida:
        return jsonify({"mensagem": "Notificação já estava lida."}), 200

    notificacao.lida = True
    notificacao.data_leitura = datetime.utcnow()
    
    try:
        db.session.commit()
        return jsonify({
            'mensagem': 'Notificação marcada como lida.',
            'notificacao': notificacao.to_dict()
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Erro ao marcar notificação como lida."}), 500