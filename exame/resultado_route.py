from flask import Blueprint, request, jsonify, render_template
from config import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from exame.exame_model import Resultado 
from encaminhamento.encaminhamento_model import Encaminhamento
from notificacao.notificacao_model import Notificacao

resultado_bp = Blueprint('resultado_routes', __name__, url_prefix='/resultados')


@resultado_bp.route('/', methods=['POST'])
def criar_resultado():
    try:
        data = request.get_json()
        arquivo_url = data.get("arquivo_url")
        encaminhamento_id = data.get("encaminhamento_id")
        descricao = data.get("descricao")
        
        if not arquivo_url or not encaminhamento_id:
            return jsonify({"erro": "O link do arquivo (arquivo_url) e o ID do encaminhamento são obrigatórios."}), 400

        encaminhamento = Encaminhamento.query.get(encaminhamento_id)
        if not encaminhamento:
            return jsonify({"erro": "Encaminhamento não encontrado."}), 404

        novo = Resultado(
            arquivo_url=arquivo_url,
            encaminhamento_id=encaminhamento_id,
            descricao=descricao
        )

        db.session.add(novo)
        
        if encaminhamento.paciente_id:
            paciente_id_dono = encaminhamento.paciente_id
        elif hasattr(encaminhamento, 'dependente') and encaminhamento.dependente:
            paciente_id_dono = encaminhamento.dependente.titular.id
        else:
            db.session.rollback()
            return jsonify({"erro": "Não foi possível determinar o paciente responsável pela notificação."}), 500


        nova_notificacao = Notificacao(
            mensagem=f"O resultado do exame {encaminhamento.exame.descricao} já está disponível para visualização.",
            paciente_id=paciente_id_dono,
        )
        db.session.add(nova_notificacao)
        db.session.commit()

        return jsonify({
            "mensagem": "Resultado criado com sucesso.",
            "resultado": novo.to_dict()
        }), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"erro": "Erro de integridade (Verifique chaves estrangeiras)."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro inesperado: {str(e)}"}), 500


@resultado_bp.route('/', methods=['GET'])
def listar_resultados():
    resultados = Resultado.query.all()
    lista_resultados = [r.to_dict() for r in resultados]
    return render_template('resultados.html', 
                           resultados=lista_resultados), 200


@resultado_bp.route('/<int:id_res>', methods=['GET'])
def obter_resultado(id_res):
    resultado = Resultado.query.get_or_404(id_res)
    return render_template('resultados.html',
                           resultado=resultado.to_dict()), 200

@resultado_bp.route('/<int:id_res>', methods=['PUT'])
def atualizar_resultado(id_res):
    resultado = Resultado.query.get_or_404(id_res)
    data = request.get_json()

    if 'arquivo_url' in data:
        resultado.arquivo_url = data['arquivo_url']
        
    if 'descricao' in data:
        resultado.descricao = data['descricao']

    try:
        db.session.commit()
        return jsonify({
            'mensagem': 'Resultado atualizado com sucesso.',
            'resultado': resultado.to_dict()
        }), 200
    except Exception:
        db.session.rollback()
        return jsonify({"erro": "Erro ao atualizar resultado."}), 500


@resultado_bp.route('/<int:id_res>', methods=['DELETE'])
def deletar_resultado(id_res):
    resultado = Resultado.query.get_or_404(id_res)
    
    db.session.delete(resultado)
    db.session.commit()

    return jsonify({'mensagem': 'Resultado deletado com sucesso.'}), 200