import streamlit as st
from groq import Groq

# 1. Configuração de Página
st.set_page_config(page_title="O Zé V4.4", layout="centered", page_icon="🎬")

st.title("🤖 O Zé - Minerador & Roteirista")
st.info("Atualizado para as novas travas do TikTok (Março/2026)")

# 2. Conexão com a Groq
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except Exception as e:
    st.error("Erro nos Secrets: Verifique sua chave GROQ_API_KEY.")
    st.stop()

# 3. Interface de Usuário
url_tiktok = st.text_input("🔗 Cole o link do TikTok aqui:", placeholder="https://vm.tiktok.com/...")
nome_produto = st.text_input("📦 Qual o nome do produto?", placeholder="Ex: Bicicleta Elétrica")

# 4. Ação do Zé
if st.button("🚀 GERAR ESTRATÉGIA AGORA", type="primary"):
    if url_tiktok and nome_produto:
        # Limpeza básica do link para evitar erros de servidor
        link_limpo = url_tiktok.split('?')[0]
        
        with st.spinner("O Zé está analisando o nicho..."):
            try:
                # MODELO ATUALIZADO 2026: Llama 3.1 8B Instant
                completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é um especialista em Reels e TikTok Ads."},
                        {"role": "user", "content": f"Crie um roteiro de 15s para o produto: {nome_produto}. Use uma linguagem que venda muito!"}
                    ],
                    model="llama-3.1-8b-instant",
                    temperature=0.8,
                )
                
                # Resultado da IA
                st.success("✅ Roteiro Gerado!")
                st.markdown(f"### 📝 Sugestão de Copy:\n{completion.choices[0].message.content}")
                
                st.divider()
                
                # Botão de Download com Servidor Alternativo
                st.subheader("📥 Download do Criativo")
                st.warning("Se o vídeo não abrir, aguarde 5 segundos e tente novamente (Limitação do TikTok).")
                
                # Link do servidor que você estava tentando usar
                link_servidor = f"https://www.tikwm.com/video/media?url={link_limpo}"
                st.link_button("📥 BAIXAR VÍDEO (Servidor HD)", link_servidor)
                
            except Exception as e:
                st.error(f"Erro técnico: {e}")
    else:
        st.warning("⚠️ O Zé precisa do link e do nome do produto!")

st.markdown("---")
st.caption("O Zé v4.4 - Inteligência Artificial aplicada ao Dropshipping")
