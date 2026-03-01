import streamlit as st
import os
import json
from groq import Groq
from huggingface_hub import HfApi

# 1. Configurações de Página
st.set_page_config(page_title="O Zé - Minerador & Copy", page_icon="🤖", layout="wide")

# 2. Inicialização de APIs (Segurança contra tela branca)
GROQ_KEY = os.environ.get("GROQ_API_KEY")
HF_TOKEN = os.environ.get("HUGGINGFACE_HUB_TOKEN")

if not GROQ_KEY:
    st.error("Erro: A variável GROQ_API_KEY não foi encontrada nas configurações.")
    st.stop()

client = Groq(api_key=GROQ_KEY)

# 3. Lógica do "Zé" (Copy + Prompts de Elite)
def engine_do_ze(produto_input):
    # O Prompt do sistema força o Zé a usar as técnicas de Nano Banana e Veo
    prompt_sistema = (
        "Você é 'O Zé', o melhor Minerador de produtos e Copywriter do mundo. "
        "Sua resposta deve ser sempre um objeto JSON puro."
    )
    
    prompt_usuario = f"""
    Analise o produto: {produto_input}
    Crie:
    1. Uma Copy matadora para anúncios.
    2. Um prompt de imagem altamente poderoso para o modelo Nano Banana (use termos como: Hasselblad, 8k, Octane Render, Studio Lighting).
    3. Um prompt de vídeo altamente poderoso para o modelo Veo (use termos como: Orbital shot, 60fps, fluid physics, cinematic).
    
    Retorne apenas este formato JSON:
    {{
        "copy": "texto aqui",
        "prompt_imagem": "prompt técnico aqui",
        "prompt_video": "prompt técnico aqui"
    }}
    """

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model="llama3-70b-8192", # Modelo Groq ultra-rápido
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# 4. Interface Streamlit (UI)
st.title("🤖 O Zé - Minerador & Copywriter")
st.info("Mineração rápida com Groq e Prompts de Mídia para Nano Banana & Veo")

with st.sidebar:
    st.header("Configurações")
    if HF_TOKEN:
        st.success("HuggingFace Conectado!")
    else:
        st.warning("HF Token não configurado.")

produto = st.text_input("Qual produto vamos minerar?", placeholder="Ex: Fone de ouvido por condução óssea")

if st.button("Gerar Estratégia do Zé"):
    if produto:
        with st.spinner("O Zé está trabalhando..."):
            dados = engine_do_ze(produto)
            
            if "error" in dados:
                st.error(f"Ocorreu um erro: {dados['error']}")
            else:
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.subheader("📝 Copy de Alta Conversão")
                    st.markdown(f"> {dados['copy']}")
                
                with col2:
                    st.subheader("📸 Prompts para Mídia")
                    st.write("**Imagem (Nano Banana):**")
                    st.code(dados['prompt_imagem'], language="text")
                    
                    st.write("**Vídeo (Veo):**")
                    st.code(dados['prompt_video'], language="text")
    else:
        st.warning("Digite o nome de um produto para começar.")
