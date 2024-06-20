from flask import Flask, request, jsonify
import sys
import os
from models import db, Tarefa, Usuario, Relatorio

# Adicione o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tarefas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def index():
    return 'Bem-vindo ao sistema de gerenciamento de tarefas!'

@app.route('/tarefas', methods=['POST'])
def cadastrar_tarefa():
    data = request.get_json()
    nova_tarefa = Tarefa(
        titulo=data['titulo'],
        descricao=data['descricao'],
        responsavel=data['responsavel'],
        data_vencimento=data['data_vencimento'],
        prioridade=data['prioridade']
    )
    db.session.add(nova_tarefa)
    db.session.commit()
    return jsonify(nova_tarefa.to_dict()), 201

@app.route('/tarefas/<int:id>', methods=['PUT'])
def editar_tarefa(id):
    data = request.get_json()
    tarefa = Tarefa.query.get_or_404(id)
    tarefa.titulo = data['titulo']
    tarefa.descricao = data['descricao']
    tarefa.responsavel = data['responsavel']
    tarefa.data_vencimento = data['data_vencimento']
    tarefa.prioridade = data['prioridade']
    db.session.commit()
    return jsonify(tarefa.to_dict()), 200

@app.route('/tarefas/<int:id>', methods=['DELETE'])
def remover_tarefa(id):
    tarefa = Tarefa.query.get_or_404(id)
    db.session.delete(tarefa)
    db.session.commit()
    return '', 204

@app.route('/tarefas', methods=['GET'])
def visualizar_tarefas():
    tarefas = Tarefa.query.all()
    return jsonify([tarefa.to_dict() for tarefa in tarefas]), 200

@app.route('/relatorios', methods=['POST'])
def gerar_relatorio():
    tarefas = Tarefa.query.all()
    relatorio = Relatorio(tarefas=tarefas)
    db.session.add(relatorio)
    db.session.commit()
    return jsonify(relatorio.to_dict()), 201

if __name__ == '__main__':
    app.run(debug=True)
