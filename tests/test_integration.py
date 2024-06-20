# tests/test_integration.py
import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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

def test_cadastro_visualizacao_tarefa(client):
    client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['titulo'] == 'Título'
    assert data[0]['descricao'] == 'Descrição'
    assert data[0]['responsavel'] == 'Usuário1'
    assert data[0]['data_vencimento'] == '2024-07-01'
    assert data[0]['prioridade'] == 'Alta'

def test_edicao_tarefa(client):
    client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    client.put('/tarefas/1', json={
        'titulo': 'Novo Título',
        'descricao': 'Nova Descrição',
        'responsavel': 'Usuário2',
        'data_vencimento': '2024-08-01',
        'prioridade': 'Baixa'
    })
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]['titulo'] == 'Novo Título'
    assert data[0]['descricao'] == 'Nova Descrição'
    assert data[0]['responsavel'] == 'Usuário2'
    assert data[0]['data_vencimento'] == '2024-08-01'
    assert data[0]['prioridade'] == 'Baixa'

def test_remocao_tarefa(client):
    client.post('/tarefas', json={
        'titulo': 'Título',
        'descricao': 'Descrição',
        'responsavel': 'Usuário1',
        'data_vencimento': '2024-07-01',
        'prioridade': 'Alta'
    })
    client.delete('/tarefas/1')
    response = client.get('/tarefas')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 0
