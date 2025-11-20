import sqlite3
import utils
from datetime import datetime
from banco import conecta


data_atual = datetime.now().date().strftime('%d/%m/%Y')


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


def inserir_empresa(razao_social:str, cnpj:str, criado_em = data_atual):
    if not razao_social:
        return None, 'Razão social obrigatória'
    cnpj_norm = utils.normaliza_cnpj(cnpj)
    if not cnpj_norm:
        return None, 'CNPJ inválido'
    
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


# -----------------------------
# TIPOS DE DOCUMENTO
# -----------------------------

def listar_tipos():
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM tipos_documento ORDER BY descricao")
    rows = cur.fetchall()
    conn.close()
    print(rows)
    return rows



def inserir_tipo(descricao:str, criado_em = data_atual):
    if not descricao or not descricao.strip():
        return None, 'Descrição obrigatória'
    
    conn = conecta()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO tipos_documento
                (descricao, criado_em)
            VALUES
                (?, ?)
        """, (descricao, criado_em)
        )
        conn.commit()
        return cur.lastrowid, None
    except sqlite3.IntegrityError:
        return None, 'Tipo já existe'
    finally:
        conn.close()



def atualizar_tipo(tipo_id: int, descricao: str):
    if not descricao or not descricao.strip():
        return None, 'Descrição obrigatória.'
    
    try:
        conn = conecta()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE tipos_documento
            SET descricao = ?
            WHERE id = ?
        """, (descricao, tipo_id)
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, 'Tipo de documento não encontrado'
        return True, None
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if 'foreign' in msg:
            return False, 'Tipo inexistente'
        return False, 'Possível duplicidade'
    finally:
        conn.close()



def excluir_tipo(tipo_id: int):
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute('DELETE FROM tipos_documento WHERE id = ?', (tipo_id,))
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    return ok


# -----------------------------
# DOCUMENTOS
# -----------------------------

def listar_documentos():
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT d.id, d.empresa_id, d.tipo_id,
            e.razao_social AS empresa,
            t.descricao AS tipo,
            d.numero_documento,
            d.data_emissao,
            d.data_vencimento,
            d.observacoes,
            d.criado_em
        FROM documentos d
        JOIN empresas e ON e.id = d.empresa_id
        JOIN tipos_document t ON t.id = d.tipo_id
        ORDER BY e.razao_social, d.data_vencimento;
    """)
    rows = cur.fetchall()
    conn.close()
    return rows


def inserir_documentos(empresa_id: int, tipo_id: int, numero_documento:str, data_emissao: str = None, data_vencimento: str = None, observacoes: str = None, criado_em = data_atual):
    if not numero_documento or not numero_documento.strip():
        return None, 'Número do documento obrigatório'
    
    conn = conecta()
    cur = conn.cursor()
    
    criado_em = datetime.now().date().strftime('%d/%m/%Y')
    
    try:
        cur.execute("""
            INSERT INTO documentos
                (empresa_id, tipo_id, numero_documento, data_emissao, data_vencimento, observacoes, criado_em)
            VALUES
                (?, ?, ?, ?, ?, ?, ?)
        """, (empresa_id, tipo_id, numero_documento, data_emissao, data_vencimento, observacoes, criado_em)
        )
        conn.commit()
        return cur.lastrowid, None
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if 'foreign' in msg:
            return None, 'Empresa ou tipo inexistente'
        return None, 'Documento duplicado'
    finally:
        conn.close()



def atualizar_documento(doc_id: int, empresa_id: int, tipo_id: int, numero_documento: str, data_emissao: str=None, data_vencimento: str=None, observacoes: str=None):
    numero_documento = (numero_documento or '').strip()
    if not numero_documento:
        return False, 'Número do documento obrigatório.'
    
    conn = conecta()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE documentos
            SET empresa_id = ?, tipo_id = ?, numero_documento = ?, data_emissao = ?, data_vencimento = ?, observacoes = ?
            WHERE id = ? 
        """, (empresa_id, tipo_id, numero_documento, data_emissao, data_vencimento, observacoes, doc_id)
        )
        conn.commit()
        if cur.rowcount == 0:
            return False, 'Documento não encontrado.'
        return True, None
    except sqlite3.IntegrityError as e:
        msg = str(e).lower()
        if 'foreign' in msg:
            return False, 'Empresa ou tipo inexistente'
        return False, 'Possível duplicidade.'
    finally:
        conn.close()



def excluir_documento(doc_id: int):
    conn = conecta()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM documentos WHERE id = ?", (doc_id,))
    
    conn.commit()
    ok = cur.rowcount > 0
    conn.close()
    return ok


    