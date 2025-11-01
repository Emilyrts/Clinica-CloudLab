from config import db

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

