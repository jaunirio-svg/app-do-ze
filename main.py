import streamlit as st
from groq import Groq
import sqlite3
from datetime import datetime

# --- 1. CONFIGURAÇÃO DE SEGURANÇA ---
# Aqui o app busca a chave no "cofre" (Secrets) do Streamlit Cloud
try:
    minha_chave = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=minha_chave)
except Exception:
    st.error("Erro: A chave GROQ_API_KEY não foi configurada nos Secrets do Streamlit.")
    st.stop()

# --- 2. FUNÇÕES DO BANCO DE DADOS ---
def iniciar_banco():
    conn = sqlite3.connect('dados_do_ze.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS roteiros 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  data TEXT, produto TEXT, roteiro TEXT)''')
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
    c.execute("SELECT data, produto, roteiro FROM roteiros ORDER BY id DESC")
    dados = c.fetchall()
    conn.close()
    return dados

# --- 3. INTERFACE ---
st.set_page_config(page_title="Assistente do Zé", layout="wide", page_icon="🤖")
iniciar_banco()

st.title("🤖 AI Assistant Manager (O Zé)")
st.write("App rodando na nuvem - Foco: TikTok Shop")

tab_criar, tab_historico = st.tabs(["🎥 Novo Roteiro", "📂 Histórico"])

with tab_criar:
    nome_produto = st.text_input("Qual o produto vamos vender?", placeholder="Ex: Ring Light Profissional")
    
    if st.button("Gerar Roteiro Estilo Zé"):
        if nome_produto:
            with st.spinner('O Zé está preparando o roteiro...'):
                try:
                    chat = client.chat.completions.create(
                        messages=[
                            {"role": "system", "content": "Você é o Zé, criador de conteúdo no Rio de Janeiro. Linguagem natural, carismática e com gírias leves. NUNCA fale preços ou valores. Foque em benefícios e curiosidades."},
                            {"role": "user", "content": f"Crie um roteiro de vídeo curto para o TikTok Shop sobre: {nome_produto}"}
                        ],
                        model="llama-3.3-70b-versatile",
                    )
                    texto_final = chat.choices[0].message.content
                    salvar_no_banco(nome_produto, texto_final)
                    st.success("Roteiro gerado!")
                    st.markdown(f"### 📝 Sugestão do Zé:\n\n{texto_final}")
                except Exception as e:
                    st.error(f"Erro ao falar com a IA: {e}")
        else:
            st.warning("Coloque o nome do produto primeiro!")

with tab_historico:
    st.subheader("Roteiros que você já criou")
    dados = buscar_historico()
    if not dados:
        st.info("O histórico está vazio por enquanto.")
    for r in dados:
        with st.expander(f"📅 {r[0]} | 📦 {r[1]}"):
            st.write(r[2])