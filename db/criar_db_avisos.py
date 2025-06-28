import sqlite3

# Conectando ao banco de dados (ou criando, se não existir)
conn = sqlite3.connect('db/avisos.db')
cursor = conn.cursor()

# Cria a tabela avisos
cursor.executescript('''
DROP TABLE IF EXISTS avisos;
CREATE TABLE avisos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATETIME DEFAULT (datetime('now', '-3 hours')),
    mensagem TEXT NOT NULL
);
''')

conn.commit()
conn.close()
