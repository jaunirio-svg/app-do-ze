import streamlit as st
import pandas as pd
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="O Zé v4.0", page_icon="🤖")

st.title("🤖 O Zé - Inteligência de Vendas")
st.markdown("---")

# 1. Verificação da Chave Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.sidebar.success("✅ Conectado à Groq")
except:
    st.sidebar.error("❌ Erro na Chave API (Secrets)")

# 2. Entradas do Usuário
url_tiktok = st.text_input("🔗 1. Cole o link do TikTok:")
nome_produto = st.text_input("📦 2. Nome do Produto (Ex: Carregador de Bateria):")

# 3. BOTÃO DE AÇÃO (Essencial para funcionar)
if st.button("🚀 GERAR ESTRATÉGIA AGORA"):
    if url_tiktok and nome_produto:
        with st.spinner(f"O Zé está analisando o {nome_produto}..."):
            try:
                # Comando para a IA não errar o nicho
                prompt = f"Crie um roteiro de 15s focado na UTILIDADE do produto: {nome_produto}. Use o link {url_tiktok} apenas como referência. Fale de solução de problemas e não de carros esportivos."
                
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                
                resposta = chat.choices[0].message.content
                link_dl = f"https://www.tikwm.com/video/media?url={url_tiktok}"

                # Mostrar Resultados
                st.success("Análise Concluída!")
                st.subheader("🎙️ Roteiro Sugerido")
                st.info(resposta)
                
                st.link_button("📥 BAIXAR VÍDEO (SEM LOGO)", link_dl)

            except Exception as e:
                st.error(f"Erro no processamento: {e}")
    else:
        st.warning("⚠️ Preencha o link e o nome do produto!")

# 4. Histórico Simples
if 'hist' not in st.session_state: st.session_state.hist = []
if url_tiktok and nome_produto and 'resposta' in locals():
    st.session_state.hist.append({"Hora": pd.Timestamp.now().strftime("%H:%M"), "Item": nome_produto})

st.divider()
if st.session_state.hist:
    st.subheader("📜 Histórico")
    st.table(pd.DataFrame(st.session_state.hist))
