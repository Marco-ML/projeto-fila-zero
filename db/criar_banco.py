import sqlite3

# Conectando ao banco de dados (ou criando, se não existir)
conn = sqlite3.connect('db/pedidos.db')
cursor = conn.cursor()

# Criando a tabela 'pedidos' com os campos id, opcao, codigo e status
cursor.execute('''
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opcao INTEGER,
    codigo INTEGER,
    status TEXT DEFAULT 'pendente'
)
''')

# Comitando as mudanças e fechando a conexão
conn.commit()
conn.close()