import streamlit as st
import os
import json

# 1. Tenta importar a Groq com segurança
try:
    from groq import Groq
except ImportError:
    st.error("Erro: Instale a biblioteca groq: pip install groq")
    st.stop()

# 2. Configuração de Página (Deve ser a primeira linha do Streamlit)
st.set_page_config(page_title="O Zé - v2.1", layout="wide")

# 3. Verificação de Chave API
api_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")

if not api_key:
    st.warning("⚠️ Configure a GROQ_API_KEY nas Variáveis de Ambiente ou Secrets.")
    st.stop()

client = Groq(api_key=api_key)

# 4. Função Principal com o Modelo Novo (Llama 3.3)
def processar_ze(texto_input):
    prompt_sistema = (
        "Você é o Zé. Transforme a descrição em Copy de Luxo e Prompts de Mídia. "
        "Responda APENAS em JSON puro."
    )
    
    try:
        # ATENÇÃO: Usando o modelo que NÃO dá erro 400
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": texto_input}
            ],
            response_format={"type": "json_object"}
        )
        return json.loads(completion.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# 5. Interface UI
st.title("🤖 O Zé - Minerador & Copy")

produto = st.text_input("Cole a descrição do produto aqui:", key="prod_input")

if st.button("🚀 Gerar com Poder Máximo"):
    if produto:
        with st.spinner("O Zé está processando..."):
            resultado = processar_ze(produto)
            
            if "error" in resultado:
                st.error(f"Erro: {resultado['error']}")
            else:
                c1, c2 = st.columns(2)
                with c1:
                    st.subheader("📝 Copy de Luxo")
                    st.write(resultado.get("copy", "Sem copy gerada."))
                with c2:
                    st.subheader("📸 Prompts Blindados")
                    st.info(f"**Imagem (Nano):** {resultado.get('prompt_img', 'Sem prompt.')}")
                    st.warning(f"**Vídeo (Veo):** {resultado.get('prompt_vid', 'Sem prompt.')}")
    else:
        st.info("Aguardando descrição...")
