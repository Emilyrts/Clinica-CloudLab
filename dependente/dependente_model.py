from config import db
import datetime

class Dependente(db.Model):
    __tablename__ = "dependentes"

    id = db.Column(db.Integer, primary_key=True)
    titular_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=False)
    titular = db.relationship("Paciente", back_populates="dependentes")
    nome = db.Column(db.String(100), nullable=False)
    data_nasc = db.Column(db.Date, nullable=False, default=datetime.date.today)
    cpf = cpf = db.Column(db.String(11), nullable=False, unique=True)

    def __init__(self, nome, data_nasc, cpf, titular_id):
        self.nome = nome
        self.data_nasc = data_nasc
        self.cpf = cpf
        self.titular_id = titular_id

    def to_dict(self):

        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nasc': self.data_nasc,
            'titular': self.titular.to_dict() if self.titular else None
        }