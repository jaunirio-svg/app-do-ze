# PROMPT DE ELITE PARA DROPSHIPPING (NICHO TÉCNICO/UTILITÁRIO)
        prompt_especifico = f"""
        PRODUTO: {url_produto}
        CONTEXTO: Você é o Zé, minerador de produtos vencedores.
        
        INSTRUÇÕES:
        1. Se o produto for AUTOMOTIVO, identifique se é ACESSÓRIO ou FERRAMENTA (Ex: Carregador/Reparador de Bateria).
        2. FOCO NO PROBLEMA: Bateria descarregada, frio, carro que não liga.
        3. FOCO NA SOLUÇÃO: Função 'Pulse Repair', carrega bateria de carro e moto, automático e seguro.
        4. ROTEIRO (15s): 
           - GANCHO: "Sua bateria arriou? Não chama o guincho ainda!"
           - BENEFÍCIO: "Esse carregador inteligente recupera baterias de 12V e 24V com um clique."
           - CTA: "Link na bio/carrinho pra não ficar na mão!"
        """
        
        chat = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt_especifico}],
            model="llama-3.3-70b-versatile", 
        )
