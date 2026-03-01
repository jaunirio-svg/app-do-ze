import streamlit as st
import os
import json
from groq import Groq
from huggingface_hub import HfApi

# 1. Setup inicial sem frescura
st.set_page_config(page_title="O Zé - Debug Mode", layout="wide")

# 2. Verificação de Chaves (Onde a maioria dos erros acontece)
groq_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("groq_key")

st.title("🤖 O Zé - Minerador (Modo de Manutenção)")

if not groq_key:
    st.error("⚠️ Erro: Chave GROQ não configurada. O App não vai funcionar sem ela.")
else:
    st.success("✅ Chave Groq detectada. Pronto para testar.")

# 3. Bloco de Função (Preparado para conserto)
def engine_do_ze(produto):
    if not groq_key:
        return {"error": "Sem API Key"}
        
    client = Groq(api_key=groq_key)
    
    # Prompt Blindado que o Zé vai usar
    prompt_sistema = "Você é o 'Zé', responda apenas em JSON."
    prompt_usuario = f"Crie copy e prompts de imagem/vídeo para: {produto}"

    try:
        # Tentativa de chamada
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
        return {"error": str(e)}

# 4. Interface Simples
produto_input = st.text_input("Produto:")

if st.button("Tentar Gerar"):
    resultado = engine_do_ze(produto_input)
    if "error" in resultado:
        st.warning(f"Erro detectado: {resultado['error']}")
        st.info("Dica: Verifique se o modelo 'llama3-70b-8192' está disponível ou se a cota da Groq acabou.")
    else:
        st.json(resultado)

st.markdown("---")
st.write("🛠️ *Código salvo. Aguardando próximas instruções para conserto.*")
