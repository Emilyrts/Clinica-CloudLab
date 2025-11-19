from flask import Blueprint, request, jsonify
from config import db
from notificacao.notificacao_model import Notificacao
from datetime import datetime

notificacao_bp = Blueprint('notificacao_routes', __name__, url_prefix='/notificacoes')

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