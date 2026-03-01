import streamlit as st
import pandas as pd
from groq import Groq

# 1. Configuração Visual
st.set_page_config(page_title="O Zé - Minerador V4", layout="centered", page_icon="🚀")

st.title("🤖 O Zé - Minerador de Produtos")
st.markdown("---")

# 2. Conexão com a Groq (IA)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.sidebar.success("✅ IA Conectada")
except Exception as e:
    st.sidebar.error("❌ Erro: Configure a GROQ_API_KEY nos Secrets do Streamlit.")

# 3. Entradas
st.subheader("📦 Nova Mineração")
url_input = st.text_input("🔗 1. Cole o link do TikTok:")
produto_input = st.text_input("🏷️ 2. O que é este produto? (Ex: Carregador de Bateria)")

# 4. O BOTÃO (O gatilho que faltava)
if st.button("🚀 GERAR ESTRATÉGIA E DOWNLOAD", type="primary"):
    if url_input and produto_input:
        with st.spinner(f"O Zé está analisando o {produto_input}..."):
            try:
                # Prompt para evitar que a IA invente carros esportivos
                prompt_ze = f"""
                PRODUTO: {produto_input}
                CONTEXTO: Dropshipping / Venda Direta
                TAREFA: Crie um roteiro de 15 segundos focado na utilidade prática.
                REGRAS: 
                1. Não fale de carros se o produto for uma ferramenta.
                2. Foque na dor/problema que o {produto_input} resolve.
                3. Termine com uma CTA (Chamada para ação).
                """
                
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_ze}],
                    model="llama3-8b-8192",
                )
                
                # Exibição dos Resultados
                st.success("Análise Concluída!")
                st.subheader("🎙️ Sugestão de Roteiro:")
                st.info(chat_completion.choices[0].message.content)
                
                # Link de Download (TikWM)
                download_final = f"https://www.tikwm.com/video/media?url={url_input}"
                st.link_button("📥 BAIXAR VÍDEO AGORA (SEM LOGO)", download_final)

            except Exception as e:
                st.error(f"Erro ao processar: {e}")
    else:
        st.warning("⚠️ Preencha o link e o nome do produto antes de clicar.")

st.markdown("---")
st.caption("Se o site não mudar, use o botão 'Reboot' no painel do Streamlit Cloud.")
