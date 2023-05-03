from flask import Flask, render_template, request, redirect, url_for
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
    mostrar_tarefas = Tarefa.query.all()
    return render_template('index.html', to_do=mostrar_tarefas)

@app.route('/criar-tarefa', methods=['POST'])
def criar():
    tarefa = Tarefa(conteudo=request.form['conteúdo_tarefa'], feita=False)
    db.session.add(tarefa)
    db.session.commit()
    return redirect(url_for('home'))


# rota para apagar a tarefa
@app.route('/eliminar-tarefa/<id>')
def eliminar(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).delete()
    db.session.commit()
    return redirect(url_for('home'))


# criando rota para alterar o boleano de tarefa
@app.route('/tarefa-feita/<id>')
def feita(id):
    tarefa = Tarefa.query.filter_by(id=int(id)).first()  # Encontra a tarefa filtrando pelo id
    tarefa.feita = not (tarefa.feita)  # grava a alteração no boleano de 0 pra 1 e de 1 pra 0
    db.session.commit()  # executa a ação
    return redirect(url_for('home'))  # volta para a home


if __name__ == '__main__':
    app.run(debug=True)
