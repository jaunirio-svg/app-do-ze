import streamlit as st
from groq import Groq

st.set_page_config(page_title="O Zé V4", layout="centered")

st.title("🤖 O Zé - Minerador")

# 1. Conexão com a Groq
try:
    # Usando a chave dos secrets
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Erro na chave: {e}")

# 2. Entradas
url = st.text_input("🔗 Link do TikTok:")
produto = st.text_input("📦 Nome do Produto (Ex: Carregador de Bateria):")

# 3. Botão de Ação
if st.button("🚀 GERAR AGORA"):
    if url and produto:
        with st.spinner("O Zé está processando..."):
            try:
                # Mudamos o modelo para o 70b (mais robusto) e limpamos o prompt
                chat = client.chat.completions.create(
                    messages=[
                        {
                            "role": "system", 
                            "content": "Você é um especialista em marketing de dropshipping."
                        },
                        {
                            "role": "user", 
                            "content": f"Crie um roteiro de 15 segundos para vender este produto: {produto}. Foque em utilidade."
                        }
                    ],
                    model="llama-3.3-70b-versatile", # Trocamos o modelo aqui
                )
                
                st.success("Gerado com sucesso!")
                st.markdown(f"### 📝 Roteiro:\n{chat.choices[0].message.content}")
                
                # Link de Download
                link_dl = f"https://www.tikwm.com/video/media?url={url}"
                st.link_button("📥 BAIXAR VÍDEO", link_dl)
                
            except Exception as e:
                # Se der erro de novo, ele vai mostrar o nome do erro aqui
                st.error(f"Erro na Groq: {e}")
    else:
        st.warning("⚠️ Preencha o link e o nome do produto!")
