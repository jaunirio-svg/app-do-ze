import streamlit as st
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="O Zé V4.3", layout="centered", page_icon="🤖")

st.title("🤖 O Zé - Minerador (Atualizado 2026)")
st.markdown("---")

# 1. Conexão com a Groq
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except Exception as e:
    st.error("Erro nos Secrets: Chave API não configurada.")
    st.stop()

# 2. Entrada de Dados
url_tiktok = st.text_input("🔗 Link do TikTok:", placeholder="Cole o link do vídeo aqui...")
nome_produto = st.text_input("📦 Nome do Produto:", placeholder="Ex: Mini Processador")

# 3. Processamento com o Novo Modelo (Llama 3.1 ou 3.3)
if st.button("🚀 GERAR ESTRATÉGIA", type="primary"):
    if url_tiktok and nome_produto:
        with st.spinner("O Zé está consultando o novo modelo da IA..."):
            try:
                # ATUALIZAÇÃO: Usando o modelo sucessor que está ativo em 2026
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é um redator de anúncios de alta conversão para Dropshipping."},
                        {"role": "user", "content": f"Crie um roteiro de 15s para o produto: {nome_produto}. Foco em benefícios reais."}
                    ],
                    model="llama-3.1-8b-instant", # Este modelo substituiu o antigo 8b-8192
                    temperature=0.7
                )
                
                st.success("✅ Roteiro Atualizado!")
                st.markdown(f"### 📝 Sugestão de Copy:\n{chat.choices[0].message.content}")
                
                st.divider()
                st.subheader("📥 Download do Vídeo")
                link_servidor = f"https://www.tikwm.com/video/media?url={url_tiktok}"
                st.link_button("📥 BAIXAR VÍDEO AGORA", link_servidor)

            except Exception as e:
                # Caso a Groq mude o nome de novo, este erro nos avisará
                st.error(f"Erro na IA: {e}")
    else:
        st.warning("⚠️ Preencha os campos para continuar.")

st.markdown("---")
st.caption("O Zé v4.3 - Modelo Llama 3.1 Instant (Sucessor)")
