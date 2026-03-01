import streamlit as st
import pandas as pd
from groq import Groq

# 1. Conexão com a Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("🔑 Configure a GROQ_API_KEY nos Secrets do Streamlit!")

if 'historico_ze' not in st.session_state:
    st.session_state.historico_ze = []

st.set_page_config(page_title="O Zé v2.5", page_icon="🤖", layout="wide")

st.title("🤖 O Zé - Inteligência de Vendas")
st.caption("Especialista em Drones, Ferramentas e Utilidades")

# --- ENTRADA DE DADOS ---
with st.container():
    url_prod = st.text_input("🔗 Link do TikTok:")
    detalhe = st.text_input("📦 O que é o produto? (Ex: Carregador de bateria, Mini Drone, Liquidificador)")

if url_prod and detalhe:
    if st.button("🚀 Gerar Estratégia"):
        with st.spinner("O Zé está trabalhando..."):
            try:
                # Prompt que impede alucinações sobre carros
                prompt_real = f"""
                PRODUTO: {detalhe}
                LINK: {url_prod}
                
                TAREFA: Crie um roteiro de 15 segundos para TikTok Ads/Organic.
                REGRAS: 
                - Foque 100% na UTILIDADE do {detalhe}.
                - Se for automotivo, foque na solução do problema (ex: bateria arriada).
                - NÃO fale de corridas ou luxo. Fale de PRATICIDADE.
                - Use Gancho, Benefício e CTA.
                """
                
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_real}],
                    model="llama3-8b-8192",
                )
                
                resultado = chat.choices[0].message.content
                link_dl = f"https://www.tikwm.com/video/media?url={url_prod}"

                # Salvar no Histórico
                st.session_state.historico_ze.append({
                    "Hora": pd.Timestamp.now().strftime("%H:%M"),
                    "Produto": detalhe,
                    "Status": "✅ OK"
                })

                st.success("Tudo pronto!")
                st.markdown(f"### 🎙️ Roteiro Sugerido:\n{resultado}")
                st.link_button("📥 BAIXAR VÍDEO SEM MARCA D'ÁGUA", link_dl)

            except Exception as e:
                st.error(f"Erro na Groq: {e}")

# --- TABELA DE HISTÓRICO ---
st.divider()
if st.session_state.historico_ze:
    st.subheader("📜 Histórico desta Sessão")
    st.table(pd.DataFrame(st.session_state.historico_ze))
