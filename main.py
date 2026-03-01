import streamlit as st
import os
import json
from groq import Groq

# 1. Configuração Inicial e Segurança
st.set_page_config(page_title="O Zé - Minerador & Copywriter", layout="wide")

# Inicializa o cliente Groq (Certifique-se de ter a Key nas Secrets ou Env)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# 2. A "Mente" do Zé - Lógica de Prompts Blindados
def processar_ze(produto_nome):
    prompt_mestre = f"""
    Aja como O Zé, Minerador e Copywriter. 
    Produto: {produto_nome}
    
    Retorne EXATAMENTE um JSON com:
    1. "copy": Uma copy de alta conversão.
    2. "prompt_img": Um prompt altamente poderoso (estilo Nano Banana) com lentes 85mm, 8k, Hasselblad, iluminação de estúdio.
    3. "prompt_vid": Um prompt de vídeo (estilo Veo) com movimento orbital, 60fps, cinematic e slow motion.
    
    Responda APENAS o JSON, sem texto antes ou depois.
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[{"role": "user", "content": prompt_mestre}],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {"error": f"Erro na Groq: {str(e)}"}

# 3. Interface do App (Evita a Tela Branca)
st.title("🤖 O Zé - Minerador & Copywriter v2.0")
st.markdown("---")

produto = st.text_input("Qual produto o Zé deve minerar hoje?", placeholder="Ex: Smartwatch à prova d'água")

if st.button("🚀 Gerar Estratégia Completa"):
    if produto:
        with st.spinner("O Zé está minerando e criando os prompts..."):
            resultado = processar_ze(produto)
            
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📝 Copy de Vendas")
                    st.write(resultado["copy"])
                
                with col2:
                    st.subheader("🖼️ Prompts de Mídia (Poderosos)")
                    st.info("**Prompt de Imagem (Nano Banana):**")
                    st.code(resultado["prompt_img"])
                    
                    st.info("**Prompt de Vídeo (Veo):**")
                    st.code(resultado["prompt_vid"])
    else:
        st.warning("Por favor, digite o nome de um produto!")
