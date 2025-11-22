from flask import Blueprint, request, jsonify
from paciente.paciente_model import Paciente

paciente_auth_bp = Blueprint('paciente_auth_routes', __name__, url_prefix='/auth')

@paciente_auth_bp.route('/login', methods=['POST'])
def login_paciente_simples():
    data = request.get_json()
    identificador = data.get('identificador')  # CPF ou Email
    senha = data.get('senha')

    if not identificador or not senha:
        return jsonify({"erro": "Identificador e senha são obrigatórios."}), 400

    paciente = Paciente.query.filter(
        (Paciente.cpf == identificador) | (Paciente.email == identificador)
    ).first()

    if paciente is None or not paciente.verificar_senha(senha):
        return jsonify({"erro": "Credenciais inválidas."}), 401
    
    return jsonify({
        "mensagem": "Login realizado com sucesso!",
        "paciente": paciente.to_dict() # Retorna o dicionário de dados do paciente
    }), 200

# POSTMAN: LOCALHOST/AUTH/LOGIN = POST
# {
#     "identificador": "teste@exemplo.com",
#     "senha": "minhasenha123"
# }