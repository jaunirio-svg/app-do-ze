import streamlit as st
import pandas as pd
from groq import Groq

# 1. Conexão com a Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("ERRO: Chave GROQ_API_KEY não encontrada nos Secrets!")

if 'historico' not in st.session_state:
    st.session_state.historico = []

st.set_page_config(page_title="O Zé v4.0", layout="wide")
st.title("🤖 O Zé - Mineração de Elite")

# --- ENTRADA DE DADOS ---
st.info("Preencha os dois campos abaixo e clique no botão.")

url = st.text_input("🔗 1. Cole o link do TikTok:")
produto_nome = st.text_input("📦 2. O que é o produto? (Ex: Carregador de Bateria, Drone, etc)")

# BOTÃO DE AÇÃO (O que estava faltando)
botao_gerar = st.button("🚀 GERAR ROTEIRO E DOWNLOAD")

if botao_gerar:
    if url and produto_nome:
        with st.spinner(f"O Zé está analisando o {produto_nome}..."):
            try:
                # Prompt direto ao ponto
                prompt = f"""
                PRODUTO: {produto_nome}
                LINK: {url}
                TAREFA: Crie um roteiro de 15s para Dropshipping.
                FOCO: Utilidade real e solução de problemas. 
                NÃO fale de carros esportivos se for ferramenta.
                """
                
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama3-8b-8192",
                )
                
                roteiro = completion.choices[0].message.content
                download_link = f"https://www.tikwm.com/video/media?url={url}"

                # Salva no Histórico
                st.session_state.historico.append({"Produto": produto_nome, "Status": "✅ Pronto"})

                # MOSTRAR RESULTADOS
                st.success("O Zé terminou!")
                st.subheader(f"🎙️ Roteiro para {produto_nome}:")
                st.write(roteiro)
                
                st.link_button("📥 BAIXAR VÍDEO AGORA", download_link)

            except Exception as e:
                st.error(f"Erro: {e}")
    else:
        st.warning("⚠️ Por favor, preencha o link e o nome do produto!")

# --- HISTÓRICO ---
st.divider()
if st.session_state.historico:
    st.subheader("📜 Itens Minerados")
    st.table(pd.DataFrame(st.session_state.historico))
