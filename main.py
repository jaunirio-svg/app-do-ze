import streamlit as st
import pandas as pd
from groq import Groq

# 1. Configuração da Página
st.set_page_config(page_title="O Zé - Minerador V4", layout="centered", page_icon="🚀")

st.title("🤖 O Zé - Minerador de Produtos")
st.markdown("---")

# 2. Conexão com a Groq (IA)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.sidebar.success("✅ IA Conectada")
except Exception as e:
    st.sidebar.error(f"❌ Erro de Chave API: {e}")

# 3. Campos de Entrada
st.subheader("📦 Nova Mineração")
url_input = st.text_input("🔗 1. Cole o link do TikTok:")
produto_input = st.text_input("🏷️ 2. O que é este produto? (Ex: Carregador de Bateria)")

# 4. O GATILHO (O Botão de Ação)
if st.button("🚀 GERAR ESTRATÉGIA E DOWNLOAD", type="primary"):
    if url_input and produto_input:
        with st.spinner(f"O Zé está analisando o {produto_input}..."):
            try:
                # Prompt para evitar que a IA invente carros
                prompt_ze = f"""
                PRODUTO: {produto_input}
                CONTEXTO: Dropshipping / Venda Direta
                TAREFA: Crie um roteiro de 15 segundos focado na utilidade.
                REGRAS: 
                1. Não fale de carros esportivos se o produto for uma ferramenta.
                2. Foque no problema que o {produto_input} resolve.
                3. Termine com uma chamada para ação (CTA).
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
                st.error(f"Erro ao processar com a IA: {e}")
    else:
        st.warning("⚠️ O Zé precisa que você preencha o link E o nome do produto.")

st.markdown("---")
st.caption("Dica: Se as mudanças não aparecerem, faça o 'Reboot' no painel do Streamlit.")
