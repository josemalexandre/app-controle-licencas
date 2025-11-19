import sqlite3
import utils
from datetime import datetime
from banco import conecta

# -----------------------------
# EMPRESAS
# -----------------------------

def listar_empresas():
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute("SELECT id, razao_social, cnpj, criado_em FROM empresas ORDER BY razao_social;")
    rows = cur.fetchall()
    conn.close()
    return rows


def inserir_empresa(razao_social:str, cnpj:str):
    if not razao_social:
        return None, 'Razão social obrigatória'
    cnpj_norm = utils.normaliza_cnpj(cnpj)
    if not cnpj_norm:
        return None, 'CNPJ inválido'
    
    criado_em = datetime.now().date().strftime('%d/%m/%Y')
    
    conn = conecta()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO empresas
                (razao_social, cnpj, criado_em)
            VALUES
                (?, ?, ?)
        """, (razao_social, cnpj_norm, criado_em)
        )
        
        conn.commit()
        return None
    except sqlite3.IntegrityError:
        return None, 'CNPJ já cadastrado.'
    finally:
        conn.close()


def excluir_empresa(empresa_id: int):
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM empresas WHERE id = ?', (empresa_id,))
    
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    return ok
    