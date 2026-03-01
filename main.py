import streamlit as st
from groq import Groq

st.set_page_config(page_title="O Zé V4 - Estável", layout="centered")

st.title("🤖 O Zé - Minerador (Versão HD 2025)")
st.caption("Ajustado para as novas limitações do TikTok")

# 1. Conexão com a Groq
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except Exception as e:
    st.error("Erro nos Secrets: Chave API não encontrada.")
    st.stop()

# 2. Interface de Usuário
url_bruta = st.text_input("🔗 Cole o link do TikTok:", placeholder="https://www.tiktok.com/...")
produto = st.text_input("📦 Nome do Produto:", placeholder="Ex: Mini Projetor Portátil")

# 3. Processamento
if st.button("🚀 GERAR ESTRATÉGIA", type="primary"):
    if url_bruta and produto:
        with st.spinner("O Zé está processando..."):
            try:
                # Limpando o link para evitar erro na Groq
                url_limpa = url_bruta.split('?')[0]
                
                # Chamada da IA
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "user", "content": f"Crie um roteiro de 15s para o produto {produto}. Foque em Reels/TikTok."}
                    ],
                    model="llama3-8b-8192",
                )
                
                st.success("✅ Roteiro Pronto!")
                st.info(completion.choices[0].message.content)
                
                st.divider()
                st.subheader("📥 Download do Vídeo")
                st.warning("Nota: Devido às mudanças no TikTok (Maio/2025), o download será na máxima qualidade disponível (1080p Low Bitrate).")
                
                # Link de Download Direto
                link_servidor = f"https://www.tikwm.com/video/media?url={url_limpa}"
                st.link_button("📥 BAIXAR AGORA (Servidor 1)", link_servidor)
                
            except Exception as e:
                st.error(f"Erro ao processar: {e}")
                st.info("Dica: Tente atualizar a página e colar o link novamente.")
    else:
        st.warning("⚠️ Preencha todos os campos!")

st.markdown("---")
st.caption("Zé António & IA - 2025")
