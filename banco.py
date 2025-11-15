import sqlite3
from datetime import datetime


DB_PATH = 'dados.db'


def conecta():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn


def cria_tabelas():
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razao_social TEXT NOT NULL,
            cnpj TEXT NOT NULL UNIQUE,
            criado_em TEXT NOT NULL
        );
    """)


    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_documento(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL UNIQUE,
            criado_em TEXT NOT NULL
        );
    """)
    
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            tipo_id INTEGER NOT NULL,
            numero_documento TEXT NOT NULL,
            data_emissao TEXT NOT NULL,
            data_vencimento NOT NULL,
            observacoes TEXT,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id),
            FOREIGN KEY (tipo_id) REFERENCES tipos_documento(id),
            UNIQUE(empresa_id, tipo_id, numero_documento)
        );
    """)
    
    conn.commit()
    conn.close()
    print('Tabelas criadas (ou já existiam).')
    

   
if __name__ == '__main__':
    cria_tabelas()
