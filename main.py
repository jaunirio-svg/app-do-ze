import streamlit as st
import os
import json
from groq import Groq

# ... (seu código de setup e verificação de chave continua igual)

def engine_do_ze(produto):
    if not groq_key:
        return {"error": "Sem API Key"}
        
    client = Groq(api_key=groq_key)
    
    # Prompt do Zé atualizado com a inteligência para os novos modelos de mídia
    prompt_sistema = (
        "Você é 'O Zé', Minerador e Copywriter de elite. "
        "Sua missão é criar copy de alta conversão e prompts de mídia blindados. "
        "Responda EXCLUSIVAMENTE em formato JSON."
    )
    
    prompt_usuario = f"""
    PRODUTO: {produto}
    
    Gere um JSON com:
    1. 'copy': Texto persuasivo de vendas.
    2. 'prompt_img': Prompt poderoso para Nano Banana (8k, Hasselblad, Octane Render).
    3. 'prompt_vid': Prompt dinâmico para Veo (Orbital shot, 60fps, Cinematic).
    """

    try:
        # ATUALIZADO: Usando o modelo llama-3.3-70b-versatile (O sucessor do que deu erro)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model="llama-3.3-70b-versatile", 
            response_format={"type": "json_object"}
        )
        return json.loads(chat_completion.choices[0].message.content)
    except Exception as e:
        # Se o 3.3 também falhar por cota, tentamos o 3.1-8b como backup automático
        try:
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt_usuario}],
                model="llama-3.1-8b-instant",
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except:
            return {"error": f"Erro na Groq: {str(e)}"}

# ... (resto da sua interface Streamlit)
