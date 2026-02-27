import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime

# --- CONFIGURAÇÃO DE SEGURANÇA ---
try:
    minha_chave = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=minha_chave)
except Exception:
    st.error("Erro: Configure a GROQ_API_KEY nos Secrets.")
    st.stop()

# --- BANCO DE DADOS (COM CORREÇÃO DE COLUNA) ---
def iniciar_banco():
    conn = sqlite3.connect('dados_do_ze.db')
    c = conn.cursor()
    # Cria a tabela se não existir
    c.execute('''CREATE TABLE IF NOT EXISTS roteiros 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  data TEXT, produto TEXT, roteiro TEXT)''')
    
    # LINHA MÁGICA: Se a coluna 'conteudo' não existir, nós usamos a 'roteiro'
    # Para evitar erros, vamos garantir que o código sempre use o nome 'roteiro'
    conn.commit()
    conn.close()

def salvar_no_banco(produto, texto):
    conn = sqlite3.connect('dados_do_ze.db')
    c = conn.cursor()
    data_hora = datetime.now().strftime("%d/%m/%Y %H:%M")
    c.execute("INSERT INTO roteiros (data, produto, roteiro) VALUES (?, ?, ?)", 
              (data_hora, produto, texto))
    conn.commit()
    conn.close()

def buscar_historico():
    conn = sqlite3.connect('dados_do_ze.db')
    c = conn.cursor()
    try:
        c.execute("SELECT data, produto, roteiro FROM roteiros ORDER BY id DESC")
        dados = c.fetchall()
    except:
        dados = []
    conn.close()
    return dados

# --- INTERFACE ---
st.set_page_config(page_title="Zé: Roteiro + Vídeo", layout="wide", page_icon="🎬")
iniciar_banco()

st.title("🎬 O Zé: Diretor de Conteúdo")
st.write("Gere roteiros para venda e prompts para IAs de vídeo (Veo/Luma).")

tab1, tab2 = st.tabs(["🎥 Novo Roteiro", "📂 Histórico"])

with tab1:
    nome_produto = st.text_input("Qual o produto?", placeholder="Ex: Mini Projetor 4K")
    
    if st.button("🚀 Gerar Estratégia Completa"):
        if nome_produto:
            with st.spinner('O Zé está roteirizando e dirigindo a cena...'):
                try:
                    chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é o Zé. Escreva um roteiro para TikTok Shop (sem preços) e, abaixo dele, escreva '---' e um 'VIDEO PROMPT' em inglês técnico para IA de vídeo 4K cinematográfica (estilo Veo/Luma)."},
                            {"role": "user", "content": f"Produto: {nome_produto}"}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    resposta_completa = chat.choices[0].message.content
                    salvar_no_banco(nome_produto, resposta_completa)
                    
                    st.success("Tudo pronto!")
                    
                    # Divide o roteiro do prompt de vídeo
                    if '---' in resposta_completa:
                        partes = resposta_completa.split('---')
                        st.subheader("📝 Roteiro Sugerido")
                        st.markdown(partes[0])
                        st.subheader("🎥 Prompt para IA de Vídeo (Copie e cole no Veo/Luma)")
                        st.code(partes[1].strip(), language="text")
                    else:
                        st.markdown(resposta_completa)
                        
                except Exception as e:
                    st.error(f"Erro na IA: {e}")
        else:
            st.warning("Digite o nome do produto!")

with tab2:
    st.subheader("Histórico de Criações")
    historico = buscar_historico()
    for h in historico:
        with st.expander(f"{h[0]} - {h[1]}"):
            st.write(h[2])
