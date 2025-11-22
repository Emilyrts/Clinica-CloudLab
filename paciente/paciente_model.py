from config import db
from werkzeug.security import generate_password_hash, check_password_hash

class Paciente(db.Model):
    __tablename__ = "pacientes"

    id = db.Column(db.Integer, primary_key=True, unique=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), nullable=False, unique=True)
    data_nasc = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(100))
    senha_hash = db.Column(db.String(128), nullable=False)
    telefone = db.Column(db.String(15))
    dependentes = db.relationship("Dependente", back_populates="titular")

    def __init__(self, nome, cpf, data_nasc, email, senha, telefone):
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.email = email
        self.set_senha(senha)  
        self.telefone = telefone

    def set_senha(self, senha):
        # Gera o hash seguro da senha
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):

        return check_password_hash(self.senha_hash, senha)

    def to_dict(self):

        return {
            'id': self.id,
            'nome': self.nome,
            'cpf': self.cpf,
            'data_nasc': self.data_nasc,
            'email': self.email,
            'telefone': self.telefone
        }
