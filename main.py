import streamlit as st
from groq import Groq

# 1. Configuração de Página
st.set_page_config(page_title="O Zé V4.5", layout="centered", page_icon="🎬")

st.title("🤖 O Zé - Minerador Profissional")
st.markdown("---")

# 2. Conexão com a Groq
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except Exception as e:
    st.error("Erro nos Secrets: Verifique sua chave API.")
    st.stop()

# 3. Interface
url_tiktok = st.text_input("🔗 Link do TikTok:", placeholder="Cole o link aqui...")
nome_produto = st.text_input("📦 Nome do Produto:", placeholder="Ex: Mini Projetor")

# 4. Ação
if st.button("🚀 GERAR ESTRATÉGIA E VÍDEO", type="primary"):
    if url_tiktok and nome_produto:
        # LIMPEZA DO LINK: Remove rastreadores do TikTok que quebram o download
        link_limpo = url_tiktok.split('?')[0]
        
        with st.spinner("O Zé está preparando tudo..."):
            try:
                # Gerar Roteiro com modelo atualizado
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "Você é um copywriter de elite para Reels."},
                        {"role": "user", "content": f"Roteiro de 15s para vender: {nome_produto}."}
                    ],
                    model="llama-3.1-8b-instant",
                )
                
                # Exibir Roteiro
                st.success("✅ Roteiro Criado!")
                st.info(chat.choices[0].message.content)
                
                st.divider()
                
                # ÁREA DE DOWNLOAD
                st.subheader("📥 Obter Vídeo Sem Marca D'água")
                
                # Criamos um link que leva direto para o processamento do vídeo
                download_url = f"https://www.tikwm.com/video/media?url={link_limpo}"
                
                st.write("Clique no botão abaixo. Se o vídeo abrir em outra aba, clique com o **botão direito** e selecione **'Salvar vídeo como...'**.")
                
                st.link_button("🔥 BAIXAR VÍDEO AGORA", download_url)
                
                st.caption("Nota: Se o vídeo não baixar automaticamente, é devido às novas travas de segurança do TikTok de 2025.")

            except Exception as e:
                st.error(f"Erro na IA: {e}")
    else:
        st.warning("⚠️ Preencha o link e o nome do produto.")

st.markdown("---")
st.caption("Zé António Tech - Versão Estável 2026")
