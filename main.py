# Dentro do seu main.py
def elevar_estilo_ze(descricao_simples):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    # O "Zé" agora atua como um Diretor de Arte
    instrucao = (
        "Transforme a descrição em uma copy de luxo e gere prompts de mídia. "
        "Para a imagem, use especificações de lentes Hasselblad. "
        "Para o vídeo, use física de luz dinâmica e 60fps."
    )
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", # O MODELO CORRETO PARA 2026
        messages=[
            {"role": "system", "content": instrucao},
            {"role": "user", "content": descricao_simples}
        ],
        response_format={"type": "json_object"}
    )
    return response
