from flask import Flask, make_response, jsonify, render_template, redirect, url_for, request, flash
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)

app.secret_key = 'uma_chave_secreta_unica_e_segura'

# Nova rota raiz: Tela de Login
@app.route('/', methods=['GET'])
def login():
    return render_template('login.html')

# Nova rota para processar o login
@app.route('/login', methods=['POST'])
def realizar_login():
    role = request.form.get('role')
    if role == 'cozinha':
        return redirect(url_for('index'))
    elif role == 'aluno_serv':
        return redirect(url_for('aluno_serv'))
    else:
        flash('Escolha uma opção válida!')
        return redirect(url_for('login'))

# Rota para Cozinha (já existente: função index)
@app.route('/index')
def index():
    pedidos = obter_pedidos()
    return render_template('index.html', pedidos=pedidos)

@app.route('/aluno_serv')
def aluno_serv():
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect('db/cardapio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cardapio WHERE date(dia) = ?", (current_date,))
    cardapio = cursor.fetchone()
    conn.close()
    if not cardapio:
        # Dummy tuple: (id, salada1, salada2, prato_principal, vegetariano, guarnicao1, guarnicao2, 
        # acompanhamento1, acompanhamento2, acompanhamento3, sobremesa1, sobremesa2, dia)
        cardapio = (0, "Não preenchido", "Não preenchido", "Não preenchido", "Não preenchido",
                    "Não preenchido", "Não preenchido", "Não preenchido", "Não preenchido",
                    "Não preenchido", "Não preenchido", "Não preenchido", current_date)
    return render_template('aluno_serv.html', cardapio=cardapio)

@app.route('/obter', methods=['GET'])
def obter_pedidos():
    # Conectando ao banco de dados
    conn = sqlite3.connect('db/pedidos.db')
    cursor = conn.cursor()
    # Consultando todos os pedidos
    cursor.execute('SELECT * FROM pedidos')
    pedidos = cursor.fetchall()
    # Fechando a conexão
    conn.close()
    # Convertendo os dados para um formato de lista de dicionários
    pedidos_json = [
        {'id': pedido[0], 'opcao': pedido[1], 'codigo': pedido[2], 'status': pedido[3]}
        for pedido in pedidos
    ]
    return pedidos_json

def atualizar_pedido(pedido_id):
    conn = sqlite3.connect('db/pedidos.db')
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute('UPDATE pedidos SET status = ?, timestamp_pronto = ? WHERE id = ?', ('pronto', timestamp, pedido_id))
    conn.commit()
    conn.close()

@app.route('/marcar_pronto/', methods = ['GET'])
def marcar_pronto():
    pedido_id = request.args.get('id',type=int)
    atualizar_pedido(pedido_id)
    return redirect(url_for('index'))

@app.route('/deletar_prontos', methods=['POST'])
def deletar_pedidos_prontos():
    # Conectar ao banco de dados SQLite
    conn = sqlite3.connect('db/pedidos.db')
    cursor = conn.cursor()
    # Excluir os pedidos com status 'pronto'
    cursor.execute("DELETE FROM pedidos WHERE status = 'pronto'")
    # Confirmar a transação
    conn.commit()
    # Fechar a conexão com o banco de dados
    conn.close()
    # Redirecionar para a página principal
    return redirect(url_for('index'))

@app.route('/aviso')
def aviso():
    return render_template('aviso.html')

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    mensagem = request.form.get('mensagem')
    # Lógica para processar a mensagem (por exemplo, salvar no banco de dados)

    # Envia a mensagem de feedback
    flash('Sua mensagem foi enviada com sucesso!')
    return render_template('aviso.html')

@app.route('/cardapio')
def cardapio():
    return render_template('cardapio.html')

@app.route('/cadastrar_cardapio', methods=['POST'])
def cadastrar_cardapio():
    # Coleta os dados do formulário
    salada1 = request.form.get('salada1')
    salada2 = request.form.get('salada2')
    prato_principal = request.form.get('prato_principal')
    vegetariano = request.form.get('vegetariano')
    guarnicao1 = request.form.get('guarnicao1')
    guarnicao2 = request.form.get('guarnicao2')
    acompanhamento1 = request.form.get('acompanhamento1')
    acompanhamento2 = request.form.get('acompanhamento2')
    acompanhamento3 = request.form.get('acompanhamento3')
    sobremesa1 = request.form.get('sobremesa1')
    sobremesa2 = request.form.get('sobremesa2')
    
    # Insere os dados no banco de dados cardapio.db
    conn = sqlite3.connect('db/cardapio.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO cardapio (salada1, salada2, prato_principal, vegetariano, guarnicao1, guarnicao2, 
                              acompanhamento1, acompanhamento2, acompanhamento3, sobremesa1, sobremesa2)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (salada1, salada2, prato_principal, vegetariano, guarnicao1, guarnicao2, 
          acompanhamento1, acompanhamento2, acompanhamento3, sobremesa1, sobremesa2))
    conn.commit()
    conn.close()
    
    flash('Cardápio cadastrado com sucesso!')
    return redirect(url_for('cardapio'))

@app.route('/cardapio_dia')
def cardapio_dia():
    from datetime import datetime
    current_date = datetime.now().strftime("%Y-%m-%d")
    conn = sqlite3.connect('db/cardapio.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cardapio WHERE date(dia) = ?", (current_date,))
    cardapio = cursor.fetchone()
    conn.close()
    if not cardapio:
        # Dummy tuple: (id, salada1, salada2, prato_principal, vegetariano, guarnicao1, guarnicao2, 
        # acompanhamento1, acompanhamento2, acompanhamento3, sobremesa1, sobremesa2, dia)
        cardapio = (0, "Não preenchido", "Não preenchido", "Não preenchido", "Não preenchido",
                    "Não preenchido", "Não preenchido", "Não preenchido", "Não preenchido",
                    "Não preenchido", "Não preenchido", "Não preenchido", current_date)
    return render_template('cardapio_dia.html', cardapio=cardapio)

@app.route('/tela_qr_code')
def tela_qr_code():
    return render_template('TELA_QR_CODE.html')

@app.route('/tela_pagamento')
def tela_pagamento():
    return render_template('Tela_pagamento.html')

app.run(debug=True)