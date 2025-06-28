from flask import Flask, make_response, jsonify, render_template, redirect, url_for, request, flash, session
import sqlite3
from datetime import datetime, timedelta
import random

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
        matricula = request.form.get('matricula')
        senha = request.form.get('senha')
        conn = sqlite3.connect('db/alunos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Senha FROM alunos WHERE Matricula = ?', (matricula,))
        row = cursor.fetchone()
        conn.close()
        if row and row[0] == senha:
            session['matricula'] = matricula  # Salva a matrícula na sessão
            return redirect(url_for('aluno_serv'))
        else:
            flash('Usuário e/ou Senha incorreta(s)')
            return redirect(url_for('login'))
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
    matricula = session.get('matricula')
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
    return render_template('aluno_serv.html', cardapio=cardapio, matricula=matricula)

@app.route('/obter', methods=['GET'])
def obter_pedidos():
    conn = sqlite3.connect('db/pedidos.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pedidos')
    pedidos = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return pedidos

def atualizar_pedido(pedido_codigo):
    conn = sqlite3.connect('db/pedidos.db')
    cursor = conn.cursor()
    timestamp = datetime.now()
    cursor.execute('UPDATE pedidos SET status = ?, timestamp_pronto = ? WHERE codigo = ?', ('pronto', timestamp, pedido_codigo))
    conn.commit()
    conn.close()

@app.route('/marcar_pronto/', methods = ['GET'])
def marcar_pronto():
    pedido_codigo = request.args.get('id')  # 'id' na URL é o codigo do pedido
    atualizar_pedido(pedido_codigo)
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

@app.route('/criar_pedido', methods=['POST'])
def criar_pedido():
    # Coleta correta dos campos do formulário
    saladas = request.form.getlist('saladas')
    salada1 = saladas[0] if len(saladas) > 0 else None
    salada2 = saladas[1] if len(saladas) > 1 else None

    acompanhamentos = request.form.getlist('acompanhamentos')
    acompanhamento1 = acompanhamentos[0] if len(acompanhamentos) > 0 else None
    acompanhamento2 = acompanhamentos[1] if len(acompanhamentos) > 1 else None
    acompanhamento3 = acompanhamentos[2] if len(acompanhamentos) > 2 else None

    # Recupere o cardápio do dia novamente
    current_date = datetime.now().strftime("%Y-%m-%d")
    conn_cardapio = sqlite3.connect('db/cardapio.db')
    cursor_cardapio = conn_cardapio.cursor()
    cursor_cardapio.execute("SELECT * FROM cardapio WHERE date(dia) = ?", (current_date,))
    cardapio = cursor_cardapio.fetchone()
    conn_cardapio.close()

    # Prato principal e vegetariano
    prato_veg = request.form.get('prato_veg')
    prato_principal = prato_veg if cardapio and prato_veg == cardapio[3] else None
    vegetariano = prato_veg if cardapio and prato_veg == cardapio[4] else None

    # Guarnições
    guarnicao = request.form.get('guarnicao')
    guarnicao1 = guarnicao if cardapio and guarnicao == cardapio[5] else None
    guarnicao2 = guarnicao if cardapio and guarnicao == cardapio[6] else None

    # Sobremesas
    sobremesa = request.form.get('sobremesa')
    sobremesa1 = sobremesa if cardapio and sobremesa == cardapio[10] else None
    sobremesa2 = sobremesa if cardapio and sobremesa == cardapio[11] else None

    refeicao = request.form.get('refeicao')
    dia = True if refeicao == "Almoço" else False
    noite = True if refeicao == "Jantar" else False

    # Gera código único
    conn_pedidos = sqlite3.connect('db/pedidos.db')
    cursor_pedidos = conn_pedidos.cursor()
    while True:
        codigo = str(random.randint(10**9, 10**10 - 1))
        cursor_pedidos.execute('SELECT 1 FROM pedidos WHERE codigo = ?', (codigo,))
        if not cursor_pedidos.fetchone():
            break

    cursor_pedidos.execute('''
        INSERT INTO pedidos (
            salada1, salada2, prato_principal, vegetariano,
            guarnicao1, guarnicao2,
            acompanhamento1, acompanhamento2, acompanhamento3,
            sobremesa1, sobremesa2,
            codigo, status, dia, noite
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        salada1, salada2,
        prato_principal, vegetariano,
        guarnicao1, guarnicao2,
        acompanhamento1, acompanhamento2, acompanhamento3,
        sobremesa1, sobremesa2,
        codigo,
        'preparando',
        int(dia),
        int(noite)
    ))
    conn_pedidos.commit()
    conn_pedidos.close()
    session['pedido_numero'] = codigo
    return redirect(url_for('tela_qr_code'))

@app.route('/tela_qr_code')
def tela_qr_code():
    matricula = session.get('matricula')
    nome = None
    categoria = None
    valor = "R$ 3,00"
    pedido_numero = session.get('pedido_numero')
    if matricula:
        conn = sqlite3.connect('db/alunos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Nome, Categoria FROM alunos WHERE Matricula = ?', (matricula,))
        row = cursor.fetchone()
        conn.close()
        if row:
            nome = row[0]
            categoria = row[1]
            if categoria == "Cotista":
                valor = "R$ 2,00"
            elif categoria == "Servidor":
                valor = "R$ 14,50"
            else:
                valor = "R$ 3,00"
    # Se não veio da sessão, gera um novo número (fallback)
    if not pedido_numero:
        conn_pedidos = sqlite3.connect('db/pedidos.db')
        cursor_pedidos = conn_pedidos.cursor()
        while True:
            pedido_numero = str(random.randint(10**9, 10**10 - 1))
            cursor_pedidos.execute('SELECT 1 FROM pedidos WHERE codigo = ?', (pedido_numero,))
            if not cursor_pedidos.fetchone():
                break
        conn_pedidos.close()
    return render_template('TELA_QR_CODE.html', nome=nome, matricula=matricula, valor=valor, pedido_numero=pedido_numero)

@app.route('/tela_pagamento')
def tela_pagamento():
    matricula = session.get('matricula')
    pedido_numero = session.get('pedido_numero')
    nome = None
    valor = "R$ 3,00"
    dia = None
    noite = None

    if matricula and pedido_numero:
        # Busca nome e categoria
        conn = sqlite3.connect('db/alunos.db')
        cursor = conn.cursor()
        cursor.execute('SELECT Nome, Categoria FROM alunos WHERE Matricula = ?', (matricula,))
        row = cursor.fetchone()
        if row:
            nome = row[0]
            categoria = row[1]
            if categoria == "Cotista":
                valor = "R$ 2,00"
            elif categoria == "Servidor":
                valor = "R$ 14,50"
            else:
                valor = "R$ 3,00"
        conn.close()

        # Busca se o pedido é almoço ou jantar
        conn_pedidos = sqlite3.connect('db/pedidos.db')
        cursor_pedidos = conn_pedidos.cursor()
        cursor_pedidos.execute('SELECT dia, noite FROM pedidos WHERE codigo = ?', (pedido_numero,))
        row_pedido = cursor_pedidos.fetchone()
        conn_pedidos.close()
        if row_pedido:
            dia, noite = row_pedido
            # Atualiza o campo Dia ou Noite do aluno
            conn = sqlite3.connect('db/alunos.db')
            cursor = conn.cursor()
            if dia:
                cursor.execute('UPDATE alunos SET Dia = ? WHERE Matricula = ?', (pedido_numero, matricula))
            elif noite:
                cursor.execute('UPDATE alunos SET Noite = ? WHERE Matricula = ?', (pedido_numero, matricula))
            conn.commit()
            conn.close()

    return render_template('Tela_pagamento.html', nome=nome, matricula=matricula, valor=valor, pedido_numero=pedido_numero)

app.run(debug=True)