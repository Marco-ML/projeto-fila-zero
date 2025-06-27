import sqlite3

# Conectando ao banco de dados (ou criando, se não existir)
conn = sqlite3.connect('db/pedidos.db')
cursor = conn.cursor()

# Criando a tabela 'pedidos' com as colunas especificadas
cursor.executescript('''
DROP TABLE IF EXISTS pedidos;
CREATE TABLE IF NOT EXISTS pedidos (
    salada1 TEXT,
    salada2 TEXT,
    prato_principal TEXT,
    vegetariano TEXT,
    guarnicao1 TEXT,
    guarnicao2 TEXT,
    acompanhamento1 TEXT,
    acompanhamento2 TEXT,
    acompanhamento3 TEXT,
    sobremesa1 TEXT,
    sobremesa2 TEXT,
    codigo INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT DEFAULT 'preparando',
    dia_noite TEXT
)
''')

# Comitando as mudanças e fechando a conexão
conn.commit()
conn.close()