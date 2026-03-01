def processar_ze(texto_input):
    # Instrução ultra-direta para não ter erro de mapeamento
    prompt_sistema = (
        "Você é o 'Zé'. Seu objetivo é gerar criativos de luxo. "
        "Você DEVE retornar um JSON com EXATAMENTE estas três chaves: "
        "'copy', 'prompt_img', 'prompt_vid'. "
        "Não adicione comentários, apenas o JSON."
    )
    
    prompt_usuario = f"""
    Converta este produto em uma oferta de luxo:
    PRODUTO: {texto_input}
    
    REGRAS TÉCNICAS:
    - copy: Texto persuasivo focado em elegância.
    - prompt_img: Prompt para Nano Banana (Hasselblad, 8k, Octane Render).
    - prompt_vid: Prompt para Veo (Orbital shot, 60fps, Cinematic).
    """
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            response_format={"type": "json_object"}
        )
        
        # Carrega o JSON da resposta
        dados = json.loads(completion.choices[0].message.content)
        
        # Normalização: Garante que as chaves existam mesmo se a IA errar o nome
        final = {
            "copy": dados.get("copy") or dados.get("copywriting") or "Erro ao gerar copy.",
            "prompt_img": dados.get("prompt_img") or dados.get("imagem") or "Erro ao gerar prompt de imagem.",
            "prompt_vid": dados.get("prompt_vid") or dados.get("video") or "Erro ao gerar prompt de vídeo."
        }
        return final

    except Exception as e:
        return {"error": str(e)}
