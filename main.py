import streamlit as st
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="O Zé - Minerador", layout="centered")

st.title("🤖 O Zé - Minerador de Produtos")
st.write("Versão 4.0 - Focada em Dropshipping")

# 1. Conexão com a Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    st.sidebar.success("✅ Conectado à IA")
except Exception as e:
    st.sidebar.error(f"❌ Erro de conexão: {e}")

# 2. Entradas do Usuário
url = st.text_input("🔗 1. Cole o link do TikTok:")
nome_produto = st.text_input("📦 2. Nome do Produto (Ex: Carregador de Bateria):")

# 3. O BOTÃO (Gatilho)
if st.button("🚀 GERAR ROTEIRO E DOWNLOAD", type="primary"):
    if url and nome_produto:
        with st.spinner(f"O Zé está analisando o {nome_produto}..."):
            try:
                # Prompt blindado contra erros
                prompt = f"""
                Analise o produto: {nome_produto}.
                Crie um roteiro de 15 segundos para venda (Dropshipping).
                Foque na UTILIDADE e no PROBLEMA que o {nome_produto} resolve.
                NÃO fale de carros de luxo ou corridas. 
                Use o link apenas como referência: {url}
                """
                
                chat = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                
                # Resultados
                st.subheader("📝 Roteiro Sugerido:")
                st.info(chat.choices[0].message.content)
                
                # Link de Download
                link_download = f"https://www.tikwm.com/video/media?url={url}"
                st.link_button("📥 BAIXAR VÍDEO AGORA", link_download)
                
            except Exception as e:
                st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("⚠️ Você precisa preencher o link e o nome do produto!")

st.divider()
st.caption("Dica: Se o site não atualizar, faça o 'Reboot' no painel do Streamlit.")
