# PROMPT "VACINA" DO ZÉ (PARA NÃO ALUCINAR MAIS)
        prompt_final = f"""
        CONTEXTO: Você é o Zé, o maior minerador de produtos virais do TikTok.
        PRODUTO NO LINK: {url_produto}

        SUA MISSÃO EM 3 PASSOS:
        1. IDENTIFICAÇÃO REAL: O que é esse objeto? (Ex: É um carregador de bateria, um drone, um liquidificador?)
        2. DOR DO CLIENTE: Que problema ele resolve? (Ex: Carro que não liga, falta de praticidade, filmagem ruim).
        3. ROTEIRO DE 15s (Obrigatório):
           - GANCHO: Pare o scroll com uma pergunta sobre o problema.
           - PROPOSTA: Mostre o produto funcionando e o benefício principal.
           - CTA: "Link na Bio/Carrinho com desconto!"

        REGRA DE OURO: Se for uma ferramenta automotiva, não fale de corrida. Fale de SEGURANÇA e PRATICIDADE.
        """
        
        # Chamada da Groq (Llama-3.3-70b)
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_final}],
            model="llama-3.3-70b-versatile", 
        )
