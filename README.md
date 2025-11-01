# Clinica-CloudLab

# CloudLab API

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Framework-black?logo=flask)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey?logo=sqlite)
![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-yellow)
![License](https://img.shields.io/badge/Licença-MIT-green)

---

## Descrição

A **CloudLab API** é uma aplicação backend desenvolvida para o gerenciamento de uma clínica laboratorial.  
Ela permite cadastrar pacientes, agendar exames, registrar resultados e gerenciar informações administrativas.  
O projeto tem foco em **organização, integração e escalabilidade**, utilizando boas práticas de desenvolvimento com **Flask e SQLAlchemy**.

---

## Tecnologias Utilizadas

- **Python 3.x**
- **Flask** — framework web principal  
- **Flask SQLAlchemy** — ORM para manipulação de dados  
- **Flask-CORS** — integração com front-end  
- **SQLite** — banco de dados local  
- **Werkzeug** — segurança e gerenciamento de rotas  

---

## Estrutura do Projeto

API/
│
├── agendamento/ # Rotas e modelos de agendamento
│ ├── agendamento_model.py
│ └── agendamento_route.py
│
├── exame/ # Rotas e modelos de exames
│ ├── exame_model.py
│ └── exame_route.py
│
├── paciente/ # Rotas e modelos de pacientes
│ ├── paciente_model.py
│ └── paciente_route.py
│
├── instance/
│ └── app.db # Banco de dados SQLite
│
├── app.py # Arquivo principal da aplicação Flask
├── config.py # Configurações de ambiente e banco de dados
├── requirements.txt # Dependências do projeto
└── README.md # Documentação

Acesse o diretório

cd Clinica-CloudLab/API

Crie e ative um ambiente virtual (opcional)
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac


Instale as dependências

pip install -r requirements.txt

Execute o servidor

python app.py

O servidor será iniciado em:

http://127.0.0.1:5000/

Endpoints Principais
Módulo	Método	Rota	Descrição
Paciente	GET	/paciente/	Lista todos os pacientes
Paciente	POST	/paciente/	Cadastra um novo paciente
Exame	GET	/exame/	Lista todos os exames
Agendamento	POST	/agendamento/	Cria um novo agendamento
Agendamento	GET	/agendamento/	Lista agendamentos existentes

(As rotas podem variar conforme a implementação atual.)

Melhorias Futuras

Autenticação e autorização de usuários (JWT)

Envio de notificações por e-mail

Painel administrativo web

Integração com aplicação mobile

Migração para servidor em nuvem (AWS)

Autora

Emily Rafaela
Desenvolvedora Web & Backend
GitHub @Emilyrts
