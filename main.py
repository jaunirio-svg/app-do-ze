import streamlit as st
from groq import Groq

# Configuração da Página
st.set_page_config(page_title="O Zé V4.2", layout="centered", page_icon="🤖")

st.title("🤖 O Zé - Minerador de Elite")
st.markdown("---")

# 1. Conexão com a Groq
try:
    key = st.secrets["GROQ_API_KEY"].strip()
    client = Groq(api_key=key)
except Exception as e:
    st.error("Erro nos Secrets: Chave API não configurada corretamente.")
    st.stop()

# 2. Entrada de Dados
url_tiktok = st.text_input("🔗 Link do TikTok:", placeholder="Cole o link do vídeo aqui...")
nome_produto = st.text_input("📦 Nome do Produto:", placeholder="Ex: Mini Processador de Alimentos")

# 3. Processamento e Inteligência
if st.button("🚀 GERAR ROTEIRO E PREPARAR VÍDEO", type="primary"):
    if url_tiktok and nome_produto:
        with st.spinner("O Zé está analisando e criando seu roteiro..."):
            try:
                # Prompt otimizado para não dar erro de BadRequest
                prompt_sistema = "Você é um mestre em copywriting para Dropshipping."
                prompt_usuario = f"Crie um roteiro de 15s para o produto: {nome_produto}. Foco total em benefícios e venda rápida."
                
                chat = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": prompt_sistema},
                        {"role": "user", "content": prompt_usuario}
                    ],
                    model="llama3-8b-8192",
                    temperature=0.7
                )
                
                # Exibição do Roteiro
                st.success("✅ Roteiro Gerado com Sucesso!")
                st.markdown("### 📝 Sugestão de Copy:")
                st.info(chat.choices[0].message.content)
                
                st.divider()
                
                # Parte do Download (Lidando com as travas do TikTok)
                st.subheader("📥 Download do Criativo")
                st.write("O TikTok está limitando a qualidade. Clique abaixo para tentar o download em 1080p:")
                
                # Link de Download Limpo
                link_servidor = f"https://www.tikwm.com/video/media?url={url_tiktok}"
                st.link_button("📥 BAIXAR VÍDEO (VIA TIKWM)", link_servidor)
                st.caption("Nota: Se o site de download avisar sobre 'bitrate baixo', é uma limitação do próprio TikTok em 2026.")

            except Exception as e:
                st.error(f"Erro na IA: {e}")
                st.info("Dica: Verifique se sua chave Groq ainda tem saldo/limite.")
    else:
        st.warning("⚠️ Preencha o link e o nome do produto para o Zé trabalhar!")

st.markdown("---")
st.caption("O Zé v4.2 - Atualizado para as novas diretrizes de vídeo.")
