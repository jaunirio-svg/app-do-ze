import streamlit as st
import pandas as pd
from groq import Groq

# 1. Conexão Segura
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("Configura a chave GROQ_API_KEY nos Secrets do Streamlit!")

if 'historico_ze' not in st.session_state:
    st.session_state.historico_ze = []

st.set_page_config(page_title="O Zé v2.0", layout="wide")
st.title("🤖 O Zé - Inteligência de Vendas")

# --- ENTRADA DE DADOS ---
col1, col2 = st.columns([2, 1])

with col1:
    url_prod = st.text_input("🔗 Cole o link do TikTok:")
    nicho = st.selectbox("📦 Qual o nicho do produto?", 
                         ["Automotivo (Ferramentas)", "Cozinha/Casa", "Eletrônicos/Drones", "Beleza/Saúde"])

if url_prod:
    with st.spinner("O Zé está analisando..."):
        try:
            # PROMPT ULTRA-RIGIDO
            prompt = f"""
            PRODUTO: {url_prod}
            NICHO SELECIONADO: {nicho}
            
            TAREFA: Escreva um roteiro de 15 segundos para venda direta (Dropshipping).
            REGRAS:
            - Se o nicho for Automotivo, foque em UTILIDADE (carregadores, reparos, limpeza). 
            - NÃO fale de carros esportivos ou corrida.
            - Fale do PROBLEMA (ex: bateria morta) e da SOLUÇÃO (esse produto).
            - Use um tom de 'Dica de Ouro'.
            """
            
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model="llama3-8b-8192", # Modelo mais estável
            )
            
            resposta = completion.choices[0].message.content
            link_dl = f"https://www.tikwm.com/video/media?url={url_prod}"

            st.session_state.historico_ze.append({
                "Data": pd.Timestamp.now().strftime("%H:%M"),
                "Nicho": nicho,
                "Status": "✅ Sucesso"
            })

            st.success("Roteiro Gerado!")
            st.write(resposta)
            st.link_button("📥 BAIXAR VÍDEO SEM MARCA D'ÁGUA", link_dl)

        except Exception as e:
            st.error(f"Erro na Groq: {e}. Tente novamente em instantes.")

# --- HISTÓRICO ---
st.divider()
if st.session_state.historico_ze:
    st.subheader("📜 Últimas Minerações")
    st.table(pd.DataFrame(st.session_state.historico_ze))
