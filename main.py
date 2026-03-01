import streamlit as st
from groq import Groq

st.set_page_config(page_title="O Zé V4")

# Teste Visual Simples
st.title("🤖 O Zé - Teste de Vida")
st.write("Se você está lendo isso, o código atualizou!")

# 1. Tentar ler a chave
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.success("API Conectada!")
except Exception as e:
    st.error(f"Erro nos Secrets: {e}")

# 2. Entradas
url = st.text_input("Link do TikTok:")
produto = st.text_input("Nome do Produto:")

# 3. Botão
if st.button("GERAR AGORA"):
    if url and produto:
        st.write(f"Buscando informações para: {produto}")
        # Chamada simples para testar
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": f"Roteiro curto para {produto}"}],
            model="llama3-8b-8192",
        )
        st.info(chat.choices[0].message.content)
    else:
        st.warning("Preencha os campos!")
