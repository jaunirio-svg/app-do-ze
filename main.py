# PROMPT "VACINA" DO ZÉ (PARA NÃO ALUCINAR MAIS)
        prompt_final = f"""
        CONTEXTO: Você é o 'Zé', o maior minerador de produtos virais do TikTok Shop.
        PRODUTO NO LINK: {url_produto}

        SUA MISSÃO EM 3 PASSOS:
        1. IDENTIFICAÇÃO REAL: O que é esse objeto no vídeo? (Ex: É um carregador de bateria, um drone, um liquidificador?)
        2. DOR DO CLIENTE: Que problema ele resolve na prática? (Ex: Bateria arriada, falta de praticidade, filmagem amadora).
        3. ROTEIRO DE 15s (Obrigatório):
           - GANCHO: Comece parando o scroll com o problema real (Ex: 'Bateria arriou e você tá na mão?').
           - PROPOSTA: Mostre o produto funcionando e cite o benefício técnico principal.
           - CTA: Finalize com "Link na Bio/Carrinho com desconto!".

        REGRA DE OURO: Se o produto for uma ferramenta de manutenção, NÃO fale de velocidade ou corrida. Foque em UTILIDADE e ECONOMIA.
        """
        
        # Chamada da Groq (Llama-3.3-70b)
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_final}],
            model="llama-3.3-70b-versatile", 
        )
