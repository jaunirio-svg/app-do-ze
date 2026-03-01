import streamlit as st
import pandas as pd
from groq import Groq

# 1. Configuração da API Groq (Puxando dos Secrets do Streamlit)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Inicializando o Histórico na Sessão
if 'historico_vendas' not in st.session_state:
    st.session_state.historico_vendas = []

st.set_page_config(page_title="O Zé v2.0", page_icon="🤖", layout="wide")

st.title("🤖 O Zé - Inteligência de Vendas")
st.caption("Automação de Roteiros, Histórico e Download de Vídeos")

# --- ÁREA DE OPERAÇÃO ---
url_produto = st.text_input("🔗 Cole o link do TikTok aqui:")

if url_produto:
    with st.spinner("O Zé está processando via Groq..."):
        # Chamada da Inteligência Groq para criar o roteiro
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Crie um roteiro de 15s, título e hashtags para: {url_produto}"}],
            model="llama3-8b-8192",
        )
        roteiro = chat.choices[0].message.content
        
        # Link para Download (Serviço externo de bypass)
        link_download = f"https://www.tikwm.com/video/media?url={url_produto}"

        # Adicionando ao Histórico
        st.session_state.historico_vendas.append({
            "Data": pd.Timestamp.now().strftime("%H:%M"),
            "Produto": url_produto[:40] + "...",
            "Status": "✅ Concluído"
        })

        # Exibindo os Resultados
        st.success("Análise Finalizada!")
        st.subheader("🎙️ Roteiro e Estratégia")
        st.info(roteiro)
        
        st.link_button("📥 BAIXAR VÍDEO (SEM MARCA D'ÁGUA)", link_download)

# --- TABELA DE HISTÓRICO ---
st.divider()
st.subheader("📜 Histórico de Mineração")
if st.session_state.historico_vendas:
    df_hist = pd.DataFrame(st.session_state.historico_vendas)
    st.table(df_hist)
else:
    st.write("Nenhum item minerado nesta sessão.")
