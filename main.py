import streamlit as st
import pandas as pd
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="O Zé v4.0", layout="wide")

# Título visível para sabermos que o código atualizou
st.title("🤖 O Zé - Versão 4.0 (Teste de Botão)")

# 1. Conexão com a Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Erro na Chave API: {e}")

# 2. Campos de Entrada
url = st.text_input("🔗 Link do TikTok:")
produto = st.text_input("📦 Nome do Produto (Ex: Carregador de Bateria):")

# 3. O BOTÃO (Gatilho)
if st.button("🚀 CLIQUE AQUI PARA GERAR"):
    if url and produto:
        with st.spinner("O Zé está processando..."):
            try:
                # Chamada da IA
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": f"Crie um roteiro de 15s para o produto: {produto}. Use o link como referência: {url}. Foque na utilidade!"}],
                    model="llama3-8b-8192",
                )
                
                roteiro = chat.choices[0].message.content
                st.success("Gerado com sucesso!")
                st.markdown(f"### Roteiro:\n{roteiro}")
                
                # Botão de Download
                link_dl = f"https://www.tikwm.com/video/media?url={url}"
                st.link_button("📥 BAIXAR VÍDEO", link_dl)
                
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("Preencha o link e o nome do produto!")
