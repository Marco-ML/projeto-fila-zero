import sqlite3

# Conectando ao banco de dados (ou criando, se não existir)
conn = sqlite3.connect('db/cardapio.db')
cursor = conn.cursor()

cursor.executescript('''
DROP TABLE IF EXISTS cardapio;

CREATE TABLE cardapio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    salada1 TEXT NOT NULL,
    salada2 TEXT NOT NULL,
    prato_principal TEXT NOT NULL,
    vegetariano TEXT NOT NULL,
    guarnicao1 TEXT NOT NULL,
    guarnicao2 TEXT NOT NULL,
    acompanhamento1 TEXT NOT NULL,
    acompanhamento2 TEXT NOT NULL,
    acompanhamento3 TEXT NOT NULL,
    sobremesa1 TEXT NOT NULL,
    sobremesa2 TEXT NOT NULL,
    dia DATETIME DEFAULT (datetime('now', '-3 hours'))
);
''')

# Comitando as mudanças e fechando a conexão
conn.commit()
conn.close()
