import sqlite3

# Conectando ao banco de dados (ou criando, se não existir)
conn = sqlite3.connect('db/pedidos.db')
cursor = conn.cursor()

# Corrige o erro de sintaxe: fecha o parêntese da tabela corretamente
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
    codigo TEXT PRIMARY KEY,
    status TEXT DEFAULT 'preparando',
    dia BOOLEAN,
    noite BOOLEAN,
    timestamp_pronto DATETIME,
    matricula TEXT,
    data DATETIME DEFAULT (datetime('now', '-3 hours'))
);
''')

# Comitando as mudanças e fechando a conexão
conn.commit()
conn.close()