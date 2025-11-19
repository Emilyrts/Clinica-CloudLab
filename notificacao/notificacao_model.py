from config import db
from datetime import datetime
from sqlalchemy.orm import relationship

class Notificacao(db.Model):
    __tablename__ = "notificacoes"

    id = db.Column(db.Integer, primary_key=True)
    mensagem = db.Column(db.Text, nullable=False)
    data_envio = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    lida = db.Column(db.Boolean, default=False)
    data_leitura = db.Column(db.DateTime, nullable=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    paciente = relationship("Paciente", backref="notificacoes", lazy=True)

    def __init__(self, titulo, mensagem,paciente_id):
        self.titulo = titulo
        self.mensagem = mensagem
        self.paciente_id = paciente_id
        
    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'mensagem': self.mensagem,
            'data_envio': self.data_envio.isoformat(),
            'lida': self.lida,
            'data_leitura': self.data_leitura.isoformat() if self.data_leitura else None,
            'paciente_id': self.paciente_id,
        }