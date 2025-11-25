from config import app, db
from flask import render_template
from paciente.paciente_route import paciente_bp
from agendamento.agendamento_route import agendamento_bp
from dependente.dependente_route import dependente_bp
from exame.exame_route import exame_bp
from exame.resultado_route import resultado_bp
from encaminhamento.encaminhamento_route import encaminhamento_bp
from login.auth import paciente_auth_bp
from notificacao.notificacao_route import notificacao_bp

### MODELS 
from exame.exame_model import Exame, Resultado
from paciente.paciente_model import Paciente 
from dependente.dependente_model import Dependente
from encaminhamento.encaminhamento_model import Encaminhamento
from notificacao.notificacao_model import Notificacao

## BLUEPRINT
app.register_blueprint(paciente_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(exame_bp)
app.register_blueprint(dependente_bp)
app.register_blueprint(encaminhamento_bp)
app.register_blueprint(paciente_auth_bp)
app.register_blueprint(resultado_bp)
app.register_blueprint(notificacao_bp)

@app.route("/", methods=['GET'])
def home():
    return {"message": "API Laboratorio CloudLab funcionando :) ",
    "message 2":"Acesse /index para visualizar principal"}, 200

@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )