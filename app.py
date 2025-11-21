import streamlit as st
import pandas as pd
import consultas as db


st.set_page_config(page_title='Controle de Documentos', layout='wide', page_icon='📃')


# ---------- Helpers ----------
def contar_tabelas():
    """Retorna (empresas, tipos, documentos) como inteiros usando consultas.py"""
    empresas = db.contar_empresas() if db.contar_empresas() > 0 else 0
    tipos = db.contar_tipos() if db.contar_tipos() > 0 else 0
    docs = db.contar_documentos() if db.contar_documentos() > 0 else 0
    return empresas, tipos, docs


# ---------- Layout de abas ----------
tabs = st.tabs(['Principal', 'Consulta','Cadastro'])
tab_principal, tab_consulta, tab_cadastro = tabs


# -------------------------
# Aba: Principal
# -------------------------
with tab_principal:
    st.title('📃 Controle de Documentos - Página Principal')

    empresas_count, tipos_count, docs_count = contar_tabelas()

    c1, c2, c3 = st.columns(3)
    c1.metric('Empresas cadastradas', empresas_count)
    c2.metric('Tipos cadastrados', tipos_count)
    c3.metric('Documentos cadastrados', docs_count)


