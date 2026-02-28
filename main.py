import streamlit as st
from groq import Groq
from huggingface_hub import InferenceClient
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÕES DE SEGURANÇA ---
try:
    GROQ_KEY = st.secrets["GROQ_API_KEY"]
    HF_TOKEN = st.secrets["HF_TOKEN"]
    
    client_groq = Groq(api_key=GROQ_KEY)
    # Cliente para o "motor" de vídeo (Software Livre)
    client_video = InferenceClient(token=HF_TOKEN)
except Exception as e:
    st.error(f"Erro de Configuração: Verifique seus Secrets. {e}")
    st.stop()

# --- BANCO DE DADOS ---
def iniciar_banco():
    conn = sqlite3.connect('dados_do_ze.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS roteiros 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  data TEXT, produto TEXT, conteudo TEXT)''')
    conn.commit()
    conn.close()

# --- INTERFACE ---
st.set_page_config(page_title="Zé: Plataforma de Vídeo", layout="wide", page_icon="🎬")
iniciar_banco()

st.title("🎬 O Zé: Sua Plataforma de Vídeo IA")
st.write("Gere roteiros e tente criar vídeos grátis usando modelos Open Source.")

nome_produto = st.text_input("Qual o produto?", placeholder="Ex: Relógio Inteligente")

if st.button("🚀 Gerar Estratégia e Vídeo"):
    if nome_produto:
        with st.spinner('O Zé está trabalhando...'):
            try:
                # 1. GERAR TEXTO COM GROQ
                chat = client_groq.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é o Zé. Escreva um roteiro para TikTok Shop e um PROMPT DE VÍDEO técnico em inglês (cinematographic, 4k, high detail). Separe-os com '---'."},
                        {"role": "user", "content": f"Produto: {nome_produto}"}
                    ],
                    model="llama-3.3-70b-versatile",
                )
                res = chat.choices[0].message.content
                partes = res.split('---')
                roteiro = partes[0]
                prompt_video = partes[1].strip() if len(partes) > 1 else "Professional product shot, 4k"

                st.subheader("📝 Roteiro Sugerido")
                st.markdown(roteiro)

                # 2. TENTAR GERAR VÍDEO COM HUGGING FACE (Mochi-1 ou HunyuanVideo)
                st.subheader("🎥 Sua Geração de Vídeo (Beta)")
                with st.spinner('Tentando gerar vídeo no servidor gratuito...'):
                    try:
                        # Usando o modelo HunyuanVideo (referência em 2026 para T2V open source)
                        video_data = client_video.text_to_video(
                            prompt_video, 
                            model="tencent/HunyuanVideo" 
                        )
                        st.video(video_data)
                        st.success("Vídeo gerado com sucesso!")
                    except Exception as ve:
                        st.warning("O servidor gratuito de vídeo está ocupado ou em fila.")
                        st.info("Copie o prompt abaixo e use no Kling ou Luma como alternativa:")
                        st.code(prompt_video, language="text")

            except Exception as e:
                st.error(f"Erro geral: {e}")
    else:
        st.warning("Digite o produto!")
