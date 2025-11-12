import sqlite3
from datetime import datetime
from pathlib import Path


DB_PATH = 'dados.db'


def conecta():
    '''Abre conexão com o arquivo SQLite'''
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def cria_tabelas():
    """Cria as tabelas 'empresas' e 'documentos' se não existirem"""
    conn = conecta()
    cur = conn.cursor()
    
    # --- tabela empresas ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            razao_social TEXT NOT NULL,
            cnpj TEXT NOT NULL,
            criado_em TEXT NOT NULL
        );    
    """)
    
    # --- tabela tipo de documentos ---
    cur.execute("""
        CREATE TABLE IF NOT EXISTS tipos_documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            criado_em TEXT NOT NULL
        );
    """)
    
    
    # --- tabela documentos
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            tipo_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            numero_documento TEXT NOT NULL,
            data_emissao TEXT NOT NULL,
            data_vencimento TEXT NOT NULL,
            observacoes TEXT,
            criado_em TEXT NOT NULL,
            FOREIGN KEY (empresa_id) REFERENCES empresas (id),
            FOREIGN KEY (tipo_id) REFERENCES tipos_documentos (id)
        );
    """)
    
    conn.commit()
    conn.close()
    print('Tabelas criadas (ou já existiam)')
    

if __name__ == '__main__':
    cria_tabelas()