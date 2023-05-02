from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/vanis/PycharmProjects/GestordeTarefas/database/tarefas.db'

db = SQLAlchemy(app)  # aponta para a base de dados


# criando classe para modelar o banco de dados
class Tarefa(db.Model):
    __tablename__ = "tarefas"
    id = db.Column(db.Integer, primary_key=True)  # identifica tarefa com id unico)
    conteudo = db.Column(db.String(200))  # limitar descrição da tarefa a 200 caracteres
    feita = db.Column(db.Boolean)  # boleano para confirmar tarega se feita ou nao.


with app.app_context():
    db.create_all()  # cria a tabela
    db.session.commit()  # executa tarefas por fazer


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    tarefa = Tarefa(conteudo=request.form['conteúdo_tarefa'], feita=False)
    db.session.add(tarefa)
    db.session.commit()
    return "Tarefa guardada"

if __name__ == '__main__':
    app.run(debug=True)
