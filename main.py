import streamlit as st
import pandas as pd
from groq import Groq

# 1. Configuração da API Groq com tratamento de erro
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("🔑 Erro: Chave da Groq não encontrada nos Secrets!")

if 'historico_vendas' not in st.session_state:
    st.session_state.historico_vendas = []

st.set_page_config(page_title="O Zé v2.0", page_icon="🤖", layout="wide")
st.title("🤖 O Zé - Inteligência de Vendas")

url_produto = st.text_input("🔗 Cole o link do TikTok aqui:")

if url_produto:
    with st.spinner("O Zé está processando..."):
        try:
            # Trocando para o modelo mais estável da Groq (Llama-3.3-70b-versatile)
            chat = client.chat.completions.create(
                messages=[{"role": "user", "content": f"Crie um roteiro de 15s e hashtags para: {url_produto}"}],
                model="llama-3.3-70b-versatile", 
            )
            roteiro = chat.choices[0].message.content
            
            link_download = f"https://www.tikwm.com/video/media?url={url_produto}"
            st.session_state.historico_vendas.append({"Data": pd.Timestamp.now().strftime("%H:%M"), "Produto": url_produto[:30], "Status": "✅ OK"})

            st.success("Análise Finalizada!")
            st.info(roteiro)
            st.link_button("📥 BAIXAR VÍDEO (SEM MARCA D'ÁGUA)", link_download)
            
        except Exception as e:
            st.error(f"❌ O Zé teve um problema com a Groq. Verifique sua chave API ou o limite de uso. Erro: {e}")

# Histórico
st.divider()
if st.session_state.historico_vendas:
    st.table(pd.DataFrame(st.session_state.historico_vendas))
