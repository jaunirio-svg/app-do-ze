import streamlit as st
import os
import json
from groq import Groq

# 1. Configuração de Interface
st.set_page_config(page_title="O Zé - Minerador & Copy", layout="wide")

# 2. Inicialização da API
api_key = os.environ.get("GROQ_API_KEY")
if not api_key:
    st.error("⚠️ GROQ_API_KEY não configurada nas variáveis de ambiente.")
    st.stop()

client = Groq(api_key=api_key)

# 3. Mente do Zé (Lógica de Prompts Blindados)
def processar_ze(texto_input):
    prompt_sistema = (
        "Você é o 'Zé - Minerador & Copywriter'. Seu papel é gerar materiais de luxo. "
        "Obrigatório: Retorne um JSON com as chaves: 'copy', 'img', 'vid'."
    )
    
    prompt_usuario = f"""
    Transforme este produto em uma oferta de elite: {texto_input}
    
    REGRAS TÉCNICAS PARA OS PROMPTS DE MÍDIA:
    - No campo 'img': Crie um prompt para Nano Banana (Hasselblad, 8k, Octane Render, luz de estúdio).
    - No campo 'vid': Crie um prompt para Veo (Movimento orbital, 60fps, cinematic, física real).
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={"type": "json_object"}
        )
        
        # Leitura e Fallback de chaves (Garante que o texto apareça)
        res_json = json.loads(completion.choices[0].message.content)
        return {
            "copy": res_json.get("copy", "Erro ao gerar texto."),
            "img": res_json.get("img", res_json.get("prompt_img", "Erro no prompt de imagem.")),
            "vid": res_json.get("vid", res_json.get("prompt_vid", "Erro no prompt de vídeo."))
        }
    except Exception as e:
        return {"error": str(e)}

# 4. Interface do App
st.title("🤖 O Zé - Minerador & Copywriter")
st.markdown("---")

entrada = st.text_area("Descreva o produto (ou cole a copy base):", height=100)

if st.button("🚀 Gerar com Poder Máximo"):
    if entrada:
        with st.spinner("O Zé está processando..."):
            resultado = processar_ze(entrada)
            
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                c1, c2 = st.columns(2)
                with c1:
                    st.success("📝 Copy de Luxo")
                    st.write(resultado["copy"])
                with c2:
                    st.info("📸 Prompts Blindados")
                    st.markdown("**Imagem (Nano Banana):**")
                    st.code(resultado["img"], language="text")
                    st.markdown("**Vídeo (Veo):**")
                    st.code(resultado["vid"], language="text")
    else:
        st.warning("O Zé precisa de uma descrição para começar!")
