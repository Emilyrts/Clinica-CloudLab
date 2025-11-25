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
    exame = db.relationship('Exame', backref='agendamentos', lazy=True) # Relacionamento com o modelo Exame

    def __init__(self, data_hora, status, fk_paciente, fk_exame):
        self.data_hora = data_hora
        self.status = status
        self.fk_paciente = fk_paciente
        self.fk_exame = fk_exame

    def to_dict(self):
        # Inicializa variáveis para evitar AttributeError
        nome_servico = "Exame Indefinido"
        
        # Acessa o nome do exame através do relacionamento
        if self.exame:
            # Assumindo que a descrição do Exame é o nome principal do serviço
            nome_servico = self.exame.descricao
            
        return {
            'id': self.id_agendamento,
            'data_hora_raw': self.data_hora.isoformat(), # Manter o formato ISO para uso técnico
            
            # Campos formatados para uso no HTML (exemplo da sua rota)
            'data_agendamento': self.data_hora.strftime("%A, %d de %B de %Y"), # Ex: segunda-feira, 22 de Setembro de 2025
            'hora_agendamento': self.data_hora.strftime("%H:%M"),             # Ex: 08:30
            
            'status': self.status,
            'servico': nome_servico, # Nome do serviço (do Exame)
            'fk_paciente': self.fk_paciente,
            'fk_exame': self.fk_exame
        }

    def __repr__(self):
        return f"<Agendamento {self.id_agendamento} - {self.status}>"

