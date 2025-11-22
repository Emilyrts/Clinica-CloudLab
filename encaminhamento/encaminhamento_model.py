from config import db
from datetime import datetime

class Encaminhamento(db.Model):
    __tablename__ = "encaminhamentos"

    id = db.Column(db.Integer, primary_key=True)
    data_emissao = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    descricao = db.Column(db.Text)
    arquivo_url = db.Column(db.String(255))
    medico_nome = db.Column(db.String(120), nullable=True)
    medico_crm = db.Column(db.String(20), nullable=True)

    paciente_id = db.Column(db.Integer, db.ForeignKey("pacientes.id"), nullable=True)
    dependente_id = db.Column(db.Integer, db.ForeignKey("dependentes.id"), nullable=True)
    exame_id = db.Column(db.Integer, db.ForeignKey("exames.id"), nullable=False)

    paciente = db.relationship("Paciente", backref="encaminhamentos", lazy=True)
    dependente = db.relationship("Dependente", backref="encaminhamentos", lazy=True)
    exame = db.relationship("Exame", backref="encaminhamentos", lazy=True)
    resultado = db.relationship("Resultado", back_populates="encaminhamento", uselist=False)

    def __init__(self, descricao, arquivo_url, medico_nome, medico_crm,
                paciente_id=None, dependente_id=None, exame_id=None):

        self.descricao = descricao
        self.arquivo_url = arquivo_url
        self.medico_nome = medico_nome
        self.medico_crm = medico_crm
        self.paciente_id = paciente_id
        self.dependente_id = dependente_id
        self.exame_id = exame_id


    def to_dict(self):
        data_formatada = self.data_emissao.strftime('%Y-%m-%d %H:%M') if self.data_emissao else None
        return {
            'id': self.id,
            'data_emissao': data_formatada,
            'descricao': self.descricao,
            'arquivo_url': self.arquivo_url,
            'medico_nome': self.medico_nome,
            'medico_crm': self.medico_crm,
            'paciente_id': self.paciente_id,
            'dependente_id': self.dependente_id,
            'exame_id': self.exame_id
        }
