import streamlit as st
import pandas as pd
from groq import Groq

# 1. Conexão com a Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("ERRO: Chave GROQ_API_KEY não encontrada nos Secrets!")

# 2. Inicialização do Histórico
if 'historico' not in st.session_state:
    st.session_state.historico = []

st.set_page_config(page_title="O Zé v4.0", layout="wide", page_icon="🤖")

st.title("🤖 O Zé - Mineração de Elite")
st.markdown("---")

# --- ENTRADA DE DADOS ---
st.subheader("🚀 Nova Mineração")
url = st.text_input("🔗 1. Cole o link do TikTok aqui:")
produto_nome = st.text_input("📦 2. O que é este produto? (Ex: Carregador de Bateria, Drone, Liquidificador)")

# O BOTÃO QUE FALTAVA
botao_gerar = st.button("🔥 GERAR ROTEIRO E DOWNLOAD")

if botao_gerar:
    if url and produto_nome:
        with st.spinner(f"O Zé está analisando o {produto_nome}..."):
            try:
                # Prompt que impede alucinações
                prompt_final = f"""
                PRODUTO: {produto_nome}
                LINK: {url}
                TAREFA: Escreva um roteiro de 15 segundos para Reels/TikTok.
                ESTILO: Venda direta, focado na UTILIDADE e na solução do problema.
                IMPORTANTE: Se for ferramenta, fale de utilidade. NÃO fale de corrida ou luxo.
                """
                
                completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt_final}],
                    model="llama3-8b-8192",
                )
                
                roteiro = completion.choices[0].message.content
                download_link = f"https://www.tikwm.com/video/media?url={url}"

                # Atualiza Histórico
                st.session_state.historico.insert(0, {"Produto": produto_nome, "Hora": pd.Timestamp.now().strftime("%H:%M")})

                # MOSTRAR RESULTADOS
                st.success("Análise Concluída com Sucesso!")
                st.subheader(f"🎙️ Roteiro Sugerido:")
                st.info(roteiro)
                
                st.link_button("📥 BAIXAR VÍDEO AGORA", download_link)

            except Exception as e:
                st.error(f"Erro na Groq: {e}")
    else:
        st.warning("⚠️ O Zé precisa que você preencha o LINK e o NOME DO PRODUTO!")

# --- HISTÓRICO ---
st.markdown("---")
if st.session_state.historico:
    st.subheader("📜 Itens Minerados Hoje")
    st.table(pd.DataFrame(st.session_state.historico))
