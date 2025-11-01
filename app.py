from config import app, db
from paciente.paciente_route import paciente_bp
from agendamento.agendamento_route import agendamento_bp
from exame.exame_route import exame_bp
app.register_blueprint(paciente_bp)
app.register_blueprint(agendamento_bp)
app.register_blueprint(exame_bp)

@app.route("/", methods=['GET'])
def home():
    return {"message": "API Laboratorio CloudLab funcionando :)"}, 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )