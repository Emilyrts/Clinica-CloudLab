from flask import Blueprint, request, jsonify, render_template, redirect, url_for
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
    agendamentos = Agendamento.query.all()
    return render_template('agendamentos.html', agendamentos=agendamentos) #MOSTRA TODOS OS EXAMES AGENDADOS

# agendamento_route.py (Função criar_agendamento modificada)

@agendamento_bp.route('/criar_agendamento', methods=['POST'])
def criar_agendamento():
    try:
        # 1. Pega os dados do formulário HTML
        data_form = request.form
        
        # 🛑 Lógica para encontrar FK_PACIENTE: 
        # Você deve ter uma forma de associar o CPF ou o usuário logado ao ID do paciente.
        # Por enquanto, SIMULAMOS que o paciente tem ID 1.
        # Você deve implementar a busca na tabela Paciente.
        fk_paciente = 1 
        
        fk_exame = data_form.get('fk_exame')
        data_agendamento = data_form.get('data_agendamento')
        hora_agendamento = data_form.get('hora_agendamento')
        
        # 2. Validação básica (verifique se os campos principais foram preenchidos)
        if not all([data_agendamento, hora_agendamento, fk_exame]):
             # Retorna o usuário para o formulário com uma mensagem de erro, se necessário
             return "Campos obrigatórios ausentes!", 400

        # 3. Combina Data e Hora e converte para datetime
        data_hora_completa_str = f"{data_agendamento} {hora_agendamento}:00"
        data_hora_agendamento = datetime.strptime(data_hora_completa_str, "%Y-%m-%d %H:%M:%S")

        # 4. Cria o objeto e salva no banco de dados
        novo = Agendamento(
            data_hora=data_hora_agendamento,
            status='pendente',
            fk_paciente=fk_paciente,
            fk_exame=fk_exame
        )

        db.session.add(novo)
        db.session.commit()

        # 5. Redireciona para a página de visualização de agendamentos ou sucesso
        # Use o nome da sua rota de destino:
        return redirect(url_for('agendamento_routes.mostrarAgendamentos')) 

    except Exception as e:
        db.session.rollback()
        # Em caso de erro (ex: erro no formato da data, erro de integridade), notifique o usuário
        return f"Erro ao criar agendamento: {str(e)}", 500

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




