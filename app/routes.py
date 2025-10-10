import io
from flask import Flask, render_template, request, send_file, url_for, redirect, session, jsonify # type: ignore 
from functools import wraps
import mysql.connector # type: ignore
from datetime import datetime, timedelta
import json
from app import app
import base64
from docx import Document
import io
from app.conexao import config
from app.conexao import key  # importa sua chave (sem subir pro GitHub!)




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
    google_maps_api_key = key
    return render_template('home.html', key=google_maps_api_key)

@app.route('/consulta')
def consulta():
    if 'user' not in session:
        return redirect('/login')
    return render_template('consulta.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    if request.method == 'POST':
        user = request.form['user']
        pwd = request.form['pwd']
        cursor.execute("SELECT * FROM user WHERE user=%s AND pwd=%s", (user, pwd))
        result = cursor.fetchone()
        connection.close()
        if result:
            session['user'] = user
            return redirect('/links')
        else:
            return "Usuário ou senha inválidos"
    return render_template('login.html')

@app.route('/links')
def links():
    if 'user' not in session:
        return redirect('/login')
    return render_template('links.html')  # Sua tela de links protegida

@app.route("/politica-privacidade")
def politica_privacidade():
    return render_template("politica-privacidade.html")


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
            telefone_responsavel = request.form.get('telefone_responsavel')
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
            Espaço_stand = request.form.get('Espaço stand')
            medida_Frente = request.form.get('medida_Frente')
            medida_Fundo = request.form.get('medida_Fundo')
            Area_total = request.form.get('Area_total')
            Estilo_construção = request.form.get('Estilo construção')
            Adicionais = request.form.get('Adicionais')
            cor_mdf = request.form.get('cor_mdf_input')
            cor_forracao = request.form.get('cor_forracao')
            sala = request.form.get('sala')
            Área_exposição = request.form.get('Área de exposição')
            Cores_empresa = request.form.get('Cores_empresa')
            produtos = request.form.get('produtos')
            listaMobiliario = request.form.getlist('listaMobiliario')
            # Transformar lista de mobiliário em string com quebras de linha
            listaMobiliario_str = "\n".join(listaMobiliario) if listaMobiliario else ""

            campos = {
                "Endereço": Endereco,
                "Razão Social": Razao_social,
                "Nome Fantasia": Nome_Fantasia,
                "Data de Entrega": data_entrega,
                "Nome do Responsável": Nome_Responsavel,
                "Telefone do Responsável": telefone_responsavel,
                "Email": Email,
                "Site": Site+ "\n",
                "Evento": Evento,
                "Local": Local,
                "Stand": Stand,
                "Valor da verba": Valor_verba,
                "Data do Evento": data_evento,
                "Informações adicionais": Informacoes_adicionas,
                "Contato": Contato,
                "Data atual": data_atual+ "\n",
                "Espaço stand": Espaço_stand,
                "Estilo construção": Estilo_construção, 
                "Medida Frente": medida_Frente,
                "Medida Fundo": medida_Fundo,
                "Área Total": Area_total+ "\n",
                "Adicionais": Adicionais,
                "Cor MDF": cor_mdf,
                "Cor Forração": cor_forracao,
                "Sala": sala,
                "Área de exposição": Área_exposição,
                "Cores da Empresa": Cores_empresa,
                "Produtos": produtos,
                "Lista de Mobiliário": listaMobiliario_str
                }


                # Criar documento
            document = Document()
            document.add_heading("Briefing de Agendamento"+"\n", level=1)

            for chave, valor in campos.items():
                if valor:  # só adiciona se não for vazio / None
                    document.add_paragraph(f"{chave}: {valor}")

                # Salvar em memória (não em arquivo físico)
                doc_io = io.BytesIO()
                document.save(doc_io)
                doc_io.seek(0)  # Voltar para o início do arquivo




                descricao_projeto = doc_io.read()


                
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

    query = """
    SELECT id, nome, telefone, email, DATE_FORMAT(data, '%d/%m/%Y') as data,
           descricao_projeto, doc_briefing,
           CASE
               WHEN aceite_termo = 'on' THEN 'sim'
               ELSE 'não'
           END AS aceite_termo
    FROM agendamento;"""

    cursor.execute(query)  # sem f-string aqui
    agendamentos = cursor.fetchall()
    connection.close()

    return jsonify([
        {
            "id": row[0],
            "nome": row[1],
            "telefone": row[2],
            "email": row[3],
            "data": row[4],
            "descricao_projeto": base64.b64encode(row[5]).decode('utf-8') if row[5] else None,
            "doc_briefing": base64.b64encode(row[6]).decode('utf-8') if row[6] else None,
            "aceite_termo": row[7]
        }
        for row in agendamentos
    ])

@app.route("/download_projeto/<int:id>", methods=["GET"])
def download_projeto(id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    cursor.execute("SELECT descricao_projeto FROM agendamento WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    connection.close()

    if resultado and resultado[0]:
        arquivo_binario = resultado[0]
        arquivo_io = io.BytesIO(arquivo_binario)

        return send_file(
            arquivo_io,
            as_attachment=True,
            download_name=f"projeto_{id}.docx",
            mimetype="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        return "Documento do projeto não encontrado", 404



@app.route("/download/<int:id>", methods=["GET"])
def download_arquivo(id):
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()
    
    cursor.execute("SELECT doc_briefing FROM agendamento WHERE id = %s", (id,))
    resultado = cursor.fetchone()
    connection.close()

    if resultado and resultado[0]:  
        arquivo_binario = resultado[0]

        # Criar um objeto de Bytes
        arquivo_io = io.BytesIO(arquivo_binario)

        return send_file(
            arquivo_io, 
            as_attachment=True, 
            download_name=f"briefing_{id}.docx",  # Nome do arquivo baixado
            mimetype="application/docx"  # Ajuste conforme necessário
        )
    else:
        return "Arquivo não encontrado", 404