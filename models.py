from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(100), nullable=False)
    data_vencimento = db.Column(db.Date, nullable=False)
    prioridade = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'data_vencimento': self.data_vencimento.isoformat(),
            'prioridade': self.prioridade
        }

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Relatorio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_geracao = db.Column(db.Date, nullable=False, default=db.func.current_date())
    tarefas = db.relationship('Tarefa', backref='relatorio', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'data_geracao': self.data_geracao.isoformat(),
            'tarefas': [tarefa.to_dict() for tarefa in self.tarefas]
        }
