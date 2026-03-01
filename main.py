import os
# Supondo que você use a lib oficial: pip install groq
from groq import Groq 

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

class ZeEngine:
    def __init__(self):
        self.modelo = "llama3-70b-8192" # Modelo potente da Groq

    def minerar_e_criar(self, produto):
        # 1. Lógica de Copy e Mineração (Sua função anterior otimizada)
        prompt_sistema = (
            "Você é 'O Zé', especialista em Mineração e Copywriting. "
            "Sua tarefa é criar uma copy de alta conversão e, ao mesmo tempo, "
            "gerar prompts altamente poderosos para imagem (Nano Banana) e vídeo (Veo)."
        )

        prompt_usuario = f"""
        Produto: {produto}
        
        Tarefas:
        1. Crie uma Copy de vendas (Direct Response).
        2. Crie um PROMPT DE IMAGEM BLINDADO: Use termos de fotografia Hasselblad, 8k, Octane Render.
        3. Crie um PROMPT DE VÍDEO PODEROSO: Use termos como 60fps, orbital move, cinematic.
        
        Responda em JSON para facilitar o uso no App.
        """

        # Chamada ultra-rápida da Groq
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": prompt_usuario}
            ],
            model=self.modelo,
            response_format={"type": "json_object"} # Força o retorno organizado
        )
        
        return chat_completion.choices[0].message.content

# --- Exemplo de como os prompts saem do Groq "blindados" ---
# Imagem: "{produto}, realistic studio photo, 85mm, f/1.8, cinematic lighting, high detail"
# Vídeo: "{produto}, product reveal, camera tracking, slow motion 120fps, 4k"
