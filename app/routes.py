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
            aceite_termo = request.form.get('aceite_termo')

            #CAMPOS BRIEFING STEP1
            Endereco = request.form.get('Endereco')
            Razao_social = request.form.get('Razao_social')
            Nome_Fantasia = request.form.get('Nome_Fantasia')
            Site = request.form.get('Site')
            data_entrega = request.form.get('data_entrega')
            Nome_Responsavel = request.form.get('Nome_Responsavel')
            telefone = request.form.get('telefone')
            Email = request.form.get('Email')
            Evento = request.form.get('Evento')
            Local = request.form.get('Local')
            Stand =  request.form.get('Stand')
            data_evento = request.form.get('data_evento')
            Informacoes_adicionas = request.form.get('Informacoes_adicionas')
            #STEP2
            Valor_verba = request.form.get('Valor_verba')
            Contato = request.form.get('Contato')
            data_atual = request.form.get('data_atual')
            Espaco_stand = request.form.get('Espaco_stand')
            medida_Frente = request.form.get('medida_Frente')
            medida_Fundo = request.form.get('medida_Fundo')
            Area_total = request.form.get('Area_total')
            Construido = request.form.get('Construido')
            Especial = request.form.get('Especial')
            Piso_elevado = request.form.get('Piso_elevado')
            Forracao = request.form.get('Forracao')
            mdf = request.form.get('mdf')
            Decorflex = request.form.get('Decorflex')
            Sala_VIP = request.form.get('Sala_VIP')
            Louge = request.form.get('Louge')
            Copa = request.form.get('Copa')
            Deposito = request.form.get('Deposito')
            Bar = request.form.get('Bar')
            Vitrines = request.form.get('Vitrines')
            Prateleiras = request.form.get('Prateleiras')
            Balcao = request.form.get('Balcao')
            Balcao_vitrine = request.form.get('Balcao_vitrine')
            Display = request.form.get('Display')
            Bancada = request.form.get('Bancada')
            Nicho = request.form.get('Nicho')
            Cores_empresa = request.form.get('Cores_empresa')
            produtos = request.form.get('produtos')
            listaMobiliario = request.form.get('listaMobiliario')
            descricao_projeto = json.dumps({
                "Endereco": Endereco,
                "Razao_social": Razao_social,
                "Nome_Fantasia": Nome_Fantasia,
                "Site": Site,
                "data_entrega": data_entrega,
                "Nome_Responsavel": Nome_Responsavel,
                "telefone": telefone,
                "Email": Email,
                "Evento": Evento,
                "Local": Local,
                "Stand": Stand,
                "data_evento": data_evento,
                "Informacoes_adicionas": Informacoes_adicionas,
                "Valor_verba": Valor_verba,
                "Contato": Contato,
                "data_atual": data_atual,
                "Espaco_stand": Espaco_stand,
                "medida_Frente": medida_Frente,
                "medida_Fundo": medida_Fundo,
                "Area_total": Area_total,
                "Construido": Construido,
                "Especial": Especial,
                "Piso_elevado": Piso_elevado,
                "Forracao": Forracao,
                "mdf": mdf,
                "Decorflex": Decorflex,
                "Sala_VIP": Sala_VIP,
                "Louge": Louge,
                "Copa": Copa,
                "Deposito": Deposito,
                "Bar": Bar,
                "Vitrines": Vitrines,
                "Prateleiras": Prateleiras,
                "Balcao": Balcao,
                "Balcao_vitrine": Balcao_vitrine,
                "Display": Display,
                "Bancada": Bancada,
                "Nicho": Nicho,
                "Cores_empresa": Cores_empresa,
                "produtos": produtos,
                "listaMobiliario": listaMobiliario
            })

            
            doc_briefing = request.files.get('doc_briefing')
            if doc_briefing:
                doc_briefing_data = doc_briefing.read()  # Converte o arquivo para binário
            else:
                doc_briefing_data = None




            # Conexão com o banco
            connection = mysql.connector.connect(**config)
            cursor = connection.cursor()

            try:  
                # Inserção no banco (barbeiro)
                sql = "INSERT INTO agendamento (nome, telefone,email , data, descricao_projeto, aceite_termo , doc_briefing) VALUES ( %s, %s, %s, %s, %s, %s, %s)"
                valores = (nome, telefone,email , data, descricao_projeto, aceite_termo, doc_briefing_data)
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

    cursor.execute(f"""
        select id,nome,telefone, email,DATE_FORMAT(data,'%d/%m/%Y') as data, descricao_projeto,doc_briefing ,   
                CASE 
                WHEN aceite_termo = 'on' THEN 'sim' 
                ELSE 'não' 
                END AS aceite_termo from agendamento;
    """)
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
            "doc_briefing": row[6],
            "aceite_termo": row[7]
        }
        for row in agendamentos
    ])