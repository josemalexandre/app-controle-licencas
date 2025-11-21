import streamlit as st
import pandas as pd
import consultas as db


st.set_page_config(page_title='Controle de Documentos', layout='wide', page_icon='📃')


# ---------- Helpers ----------
def contar_tabelas():
    """Retorna (empresas, tipos, documentos) como inteiros usando consultas.py"""
    try:
        empresas = len(db.listar_empresas()) if callable(db.listar_empresas) else 0
    except Exception:
        empresas = 0
    try:
        tipos = len(db.listar_tipos()) if callable(db.listar_tipos) else 0
    except Exception:
        tipos = 0
    try:
        docs = len(db.listar_documentos()) if callable(db.listar_documentos) else 0
    except Exception:
        docs = 0
    return empresas, tipos, docs
        
