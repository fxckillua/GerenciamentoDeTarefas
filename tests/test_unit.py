# tests/test_unit.py
import sys
import os
import pytest

# Adicione o diretório raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# tests/test_unit.py
import pytest
from GerenciamentoDeTarefas.app import app, db
from GerenciamentoDeTarefas.models import Tarefa, Usuario, Relatorio


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_cadastrar_tarefa(client):
    response = client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['titulo'] == 'Título'
    assert data['descricao'] == 'Descrição'
    assert data['responsavel'] == 'Usuário1'
    assert data['data_vencimento'] == '2024-07-01'
    assert data['prioridade'] == 'Alta'

def test_editar_tarefa(client):
    client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    response = client.put('/tarefas/1', json={
        'titulo': 'Novo Título',
        'descricao': 'Nova Descrição',
        'responsavel': 'Usuário2',
        'data_vencimento': '2024-08-01',
        'prioridade': 'Baixa'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data['titulo'] == 'Novo Título'
    assert data['descricao'] == 'Nova Descrição'
    assert data['responsavel'] == 'Usuário2'
    assert data['data_vencimento'] == '2024-08-01'
    assert data['prioridade'] == 'Baixa'

def test_remover_tarefa(client):
    client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    response = client.delete('/tarefas/1')
    assert response.status_code == 204
    tarefas = Tarefa.query.all()
    assert len(tarefas) == 0
