from flask import Flask, render_template, request, url_for, redirect, session, jsonify # type: ignore 
from functools import wraps
import mysql.connector # type: ignore
from datetime import datetime, timedelta
import json
from app import app

# Configurações da conexão
config = {
    'host': 'localhost',
    'user': 'SYS',
    'password': 'ab100423*',
    'database': 'polystands'
}

# Test de conecta ao banco
try:
    connection = mysql.connector.connect(**config)
    print("Conexão bem-sucedida!")
except mysql.connector.Error as err:
    print(f"Erro: {err}")
finally:
    if connection.is_connected():
        connection.close()


#Etapas de agendamento
@app.route('/agendamento')
def agendar():
    return render_template('agendamento.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/consulta')
def consulta():
    return render_template('consulta.html')




# agendamento de usuário
@app.route('/agendamento', methods=['POST'])
def agendamento():
         if request.method == 'POST':
            nome = request.form.get('nome')
            telefone = request.form.get('telefone')
            email = request.form.get('email')
            data = request.form.get('data')
            objetivo = request.form.get('objetivo')
            publico = request.form.get('publico')
            detalhes = request.form.get('detalhes')
            aceite_termo = request.form.get('aceite_termo')
            descricao_projeto = f"#objetivo: {objetivo}# #publico: {publico}# #detalhes: {detalhes}#"
            # Conexão com o banco
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            try:  
                # Inserção no banco (barbeiro)
                sql = "INSERT INTO agendamento (nome, telefone,email , data, descricao_projeto, aceite_termo ) VALUES ( %s, %s, %s, %s, %s, %s)"
                valores = (nome, telefone,email , data, descricao_projeto, aceite_termo)
                cursor.execute(sql, valores)
                connection.commit()
                
                print("Agendamento feito com sucesso!")
                return render_template('agendamento.html', mensagem_sucesso="Agendamento feito com sucesso!")
            
            except Exception as e:
                connection.rollback()
                return f"Erro: {e}"
            finally:
                cursor.close()
                connection.close()

# Rota para buscar agendamentos do banco de dados
@app.route('/api/agendamentos', methods=['GET'])
def api_agendamentos():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("""select id,nome,telefone,email, DATE_FORMAT(data,'%d/%m/%Y') as data, descricao_projeto,    CASE 
        WHEN aceite_termo = 'on' THEN 'sim' 
        ELSE 'não' 
    END AS aceite_termo from agendamento;""")
    agendamentos = cursor.fetchall()
    connection.close()

    return jsonify([
        {
            "id": row[0],
            "nome": row[1],
            "telefone": row[2],
            "email": row[3],
            "data": row[4],
            "descricao_projeto": row[5],
            "aceite_termo": row[6]
        }
        for row in agendamentos
    ])