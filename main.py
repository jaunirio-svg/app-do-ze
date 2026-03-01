import streamlit as st
import os
import json

# Tenta importar as bibliotecas. Se falhar, avisa na tela em vez de ficar branco.
try:
    from groq import Groq
    from huggingface_hub import HfApi
except ImportError:
    st.error("Erro: Bibliotecas faltando. Verifique seu requirements.txt (streamlit, groq, huggingface_hub)")
    st.stop()

# 1. Configuração de Página (Sempre a primeira coisa do Streamlit)
st.set_page_config(page_title="O Zé - Minerador", layout="wide")

# 2. Inicialização de Chaves com Fallback
groq_key = os.environ.get("GROQ_API_KEY") or st.secrets.get("groq_key", "")

st.title("🤖 O Zé - Minerador & Copywriter")

# 3. Lógica de Processamento (Com os modelos novos da Groq)
def executar_ze(produto):
    if not groq_key:
        return {"error": "Chave API não configurada!"}
    
    client = Groq(api_key=groq_key)
    
    # Prompt Blindado para Imagem (Nano Banana) e Vídeo (Veo)
    prompt_sistema = "Você é o 'Zé'. Responda apenas com JSON puro."
    prompt_usuario = f"""
    Crie para o produto '{produto}':
    1. Copy de vendas.
    2. Prompt Imagem (Estilo Nano Banana): Hasselblad, 8k, profissional.
    3. Prompt Vídeo (Estilo Veo): Orbital, 60fps, cinematic.
    
    Retorne no formato: 
    {{"copy": "...", "img": "...", "vid": "..."}}
    """

    try:
        # Usando o modelo Llama 3.3 (substituto do que deu erro)
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model="llama-3.3-70b-versatile",
            response_format={"type": "json_object"}
        )
        return json.loads(chat.choices[0].message.content)
    except Exception as e:
        return {"error": str(e)}

# 4. Interface de Usuário
produto_nome = st.text_input("Nome do Produto:", placeholder="Ex: Relógio Inteligente")

if st.button("🚀 Iniciar Mineração"):
    if produto_nome:
        with st.spinner("O Zé está processando..."):
            resultado = executar_ze(produto_nome)
            
            if "error" in resultado:
                st.error(f"Erro no processamento: {resultado['error']}")
            else:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("📝 Copy")
                    st.write(resultado.get("copy"))
                with col2:
                    st.subheader("📸 Prompts de Mídia")
                    st.info(f"**Imagem:** {resultado.get('img')}")
                    st.warning(f"**Vídeo:** {resultado.get('vid')}")
    else:
        st.warning("Digite o nome de um produto.")

st.markdown("---")
st.caption("Versão 2.1 - Groq Engine Atualizada")
