import streamlit as st
import pandas as pd
from supabase import create_client, Client

SUPABASE_URL = "https://wjelqoiakkyljdxupmyf.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndqZWxxb2lha2t5bGpkeHVwbXlmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDY5MTIyMjQsImV4cCI6MjA2MjQ4ODIyNH0.tVkJdo_6Tu2blnfgSiBdaoYM5b2635nYuaR5MzRiRGo"

@st.cache_resource
def init_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

supabase = init_supabase()

st.title("Visualização da Tabela 'alunos'")

with st.spinner("Carregando dados..."):
    response = supabase.table("alunos").select("*").execute()

df = pd.DataFrame(response.data)
if df.empty:
    st.info("Nenhum dado encontrado na tabela.")
else:
    st.success("Dados carregados com sucesso!")
    st.dataframe(df)
