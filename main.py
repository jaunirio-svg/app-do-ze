import streamlit as st
import os
import json
from groq import Groq
from huggingface_hub import HfApi

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="O Zé - Minerador & Copy", layout="wide")

# --- CONEXÃO COM A API (GROQ) ---
# Usando try/except para evitar que o app quebre se a chave estiver errada
try:
    if "GROQ_API_KEY" in os.environ:
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    elif "groq_key" in st.secrets:
        client = Groq(api_key=st.secrets["groq_key"])
    else:
        st.error("⚠️ Chave GROQ não encontrada! Configure nas Variáveis de Ambiente.")
        st.stop()
except Exception as e:
    st.error(f"Erro ao conectar com a Groq: {e}")
    st.stop()

# --- FUNÇÃO MESTRE DO ZÉ ---
def chamar_o_ze(produto_input):
    # Prompt que define o comportamento do Zé e injeta os comandos poderosos
    prompt_sistema = (
        "Você é o 'O Zé', assistente de elite para minerar produtos e criar copy. "
        "Sua resposta deve ser obrigatoriamente um objeto JSON puro, sem explicações fora do JSON."
    )
    
    prompt_usuario = f"""
    PRODUTO: {produto_input}
    
    TAREFAS:
    1. Crie uma Copy de vendas persuasiva.
    2. Crie um PROMPT DE IMAGEM para o Nano Banana: Use termos de fotografia Hasselblad, lens 85mm, 8k, Octane Render, Studio Lighting.
    3. Crie um PROMPT DE VÍDEO para o Veo: Use orbital tracking shot, cinematic, 60fps, realistic physics.

    RESPONDA NESTE FORMATO JSON:
    {{
        "copy": "...",
        "prompt_imagem": "...",
        "prompt_video": "..."
    }}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model="llama3-70b-8192",
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": f"Falha na API: {str(e)}"}

# --- INTERFACE DO USUÁRIO ---
st.title("🤖 O Zé - Minerador & Copywriter v2.1")
st.markdown("---")

# Campo de entrada
produto_nome = st.text_input("Nome do produto para o Zé minerar:", placeholder="Ex: Smartwatch Ultra...")

if st.button("🚀 Gerar com Poder Máximo"):
    if produto_nome:
        with st.spinner("O Zé está processando os dados..."):
            res = chamar_o_ze(produto_nome)
            
            if "error" in res:
                st.error(res["error"])
            else:
                # Layout em colunas
                col1, col2 = st.columns(2)
                
                with col1:
                    st.success("📝 Copywriter do Zé")
                    st.write(res["copy"])
                
                with col2:
                    st.info("🖼️ Criativos de Mídia")
                    st.markdown("**Prompt p/ Imagem (Nano Banana):**")
                    st.code(res["prompt_imagem"], language="text")
                    
                    st.markdown("**Prompt p/ Vídeo (Veo):**")
                    st.code(res["prompt_video"], language="text")
    else:
        st.warning("Por favor, informe o produto.")

# --- FOOTER ---
st.sidebar.markdown("---")
st.sidebar.write("⚡ Powered by Groq & HuggingFace Hub")
