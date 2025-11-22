from config import db
from datetime import datetime

class Agendamento(db.Model):
    __tablename__ = "agendamentos"  

    id_agendamento = db.Column(db.Integer, primary_key=True, unique=True)
    data_hora = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), default="pendente")

    fk_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    fk_exame = db.Column(db.Integer, db.ForeignKey('exames.id'), nullable=False)

    paciente = db.relationship('Paciente', backref='agendamentos', lazy=True)
    exame = db.relationship('Exame', backref='agendamentos', lazy=True)

    def __init__(self, data_hora, status, fk_paciente, fk_exame):
        self.data_hora = data_hora
        self.status = status
        self.fk_paciente = fk_paciente
        self.fk_exame = fk_exame

    def to_dict(self):
        return {
            'id_agendamento': self.id_agendamento,
            'data_hora': self.data_hora.strftime("%Y-%m-%d %H:%M"),
            'status': self.status,
            'fk_paciente': self.fk_paciente,
            'fk_exame': self.fk_exame
        }

    def __repr__(self):
        return f"<Agendamento {self.id_agendamento} - {self.status}>"



'''Tipo de criação:'''

#     novo_agendamento = Agendamento(
#     data_hora=datetime(2025, 11, 10, 10, 30),
#     status="pendente",
#     fk_paciente=1,
#     fk_exame=2
# )

