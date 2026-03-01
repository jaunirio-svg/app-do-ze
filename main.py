import streamlit as st
from groq import Groq

# Configuração
st.set_page_config(page_title="O Zé V4.6", layout="centered", page_icon="🚀")

st.title("🤖 O Zé - Minerador & Copywriter")
st.markdown("---")

# 1. Conexão IA
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except:
    st.error("Erro na chave API nos Secrets.")
    st.stop()

# 2. Interface
url_input = st.text_input("🔗 Link do TikTok:", placeholder="Cole o link aqui...")
produto_input = st.text_input("📦 Nome do Produto:", placeholder="Ex: Depilador a Laser")

# 3. Processamento
if st.button("🚀 GERAR TUDO", type="primary"):
    if url_input and produto_input:
        # Limpeza do link (essencial para o download funcionar)
        link_limpo = url_input.split('?')[0]
        
        with st.spinner("O Zé está criando sua estratégia..."):
            try:
                # Gerar Roteiro
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é um especialista em anúncios de dropshipping."},
                        {"role": "user", "content": f"Crie um roteiro de 15s para o produto: {produto_input}."}
                    ],
                    model="llama-3.1-8b-instant",
                )
                
                # Exibição
                st.success("✅ Roteiro Criado!")
                st.info(chat.choices[0].message.content)
                
                st.divider()
                st.subheader("📥 Download do Vídeo")
                
                # Instrução de como baixar
                st.write("Escolha uma das opções abaixo para baixar sem marca d'água:")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Opção TikWM (A que você está usando)
                    url_tikwm = f"https://www.tikwm.com/video/media?url={link_limpo}"
                    st.link_button("💾 Servidor 1 (TikWM)", url_tikwm)
                
                with col2:
                    # Opção Alternativa (Caso a primeira falhe)
                    url_snaptik = f"https://snaptik.app/abc.php?url={link_limpo}"
                    st.link_button("💾 Servidor 2 (SnapTik)", url_snaptik)

                st.warning("⚠️ **Como baixar:** Se o vídeo abrir no navegador, clique com o botão direito nele e escolha **'Salvar vídeo como...'**.")

            except Exception as e:
                st.error(f"Erro na IA: {e}")
    else:
        st.warning("Preencha o link e o nome do produto!")

st.markdown("---")
st.caption("Zé António - Atualizado para as travas do TikTok 2026")
