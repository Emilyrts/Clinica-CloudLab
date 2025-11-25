from config import db
from datetime import datetime

class Exame(db.Model):
    __tablename__ = "exames"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200))

    def __init__(self, tipo, descricao):
        self.tipo = tipo
        self.descricao = descricao

    def to_dict(self):
        return{
            'id': self.id,
            'tipo': self.tipo,
            'descricao': self.descricao
        }


class Resultado(db.Model):
    __tablename__ = "resultados"

    id = db.Column(db.Integer, primary_key=True)
    data_resultado = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    arquivo_url = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text, nullable=True)

    encaminhamento_id = db.Column(db.Integer, db.ForeignKey('encaminhamentos.id'), nullable=False)
    encaminhamento = db.relationship("Encaminhamento", back_populates="resultado")

    def __init__(self, arquivo_url, encaminhamento_id, descricao=None):
        self.arquivo_url = arquivo_url
        self.encaminhamento_id = encaminhamento_id
        self.descricao = descricao

    def to_dict(self):
        nome_exame = None
        tipo_exame = None

        if self.encaminhamento and self.encaminhamento.exame:
            exame_obj = self.encaminhamento.exame
            nome_exame = exame_obj.descricao
            tipo_exame = exame_obj.tipo
            
        return {
            'id': self.id,
            'data_resultado': self.data_resultado.isoformat(),
            'arquivo_url': self.arquivo_url,
            'descricao_resultado': self.descricao, 
            'encaminhamento_id': self.encaminhamento_id,
            
            'nome_exame': nome_exame,
            'tipo_exame': tipo_exame,
        }