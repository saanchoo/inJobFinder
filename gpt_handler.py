import os
from dotenv import load_dotenv
import openai

class ChatGPTHandler:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.job_filter_prompt = os.getenv("JOB_FILTER_PROMPT")

        if not self.api_key:
            raise ValueError("❌ No se encontró OPENAI_API_KEY en tu .env")

        openai.api_key = self.api_key

    def summarize_job(self, job_description):
        job_description = job_description[:300]
        prompt = (
            f"{self.job_filter_prompt}\n"
            f"Descripcion del trabajo:\n{job_description}\n"
            "Responde EXACTAMENTE con el formato:\n"
            "Resumen:\n<resumen breve estilo bulletpoints con cosas que le puedan interesar al candidato y paga si esta descrita cuanto va a ser mensualmente>\n"
            "Decision:\n<1-5>\n"
            "Justificacion:\n<breve justificación de pq si o pq no>\n"
        )

        print(f"DEBUG: Prompt enviado a ChatGPT:\n{prompt}")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0
        )

        respuesta_texto = response['choices'][0]['message']['content'].strip()

        print(f"DEBUG: Respuesta recibida de ChatGPT:\n{respuesta_texto}")

        resumen = ""
        decision = ""
        justificacion = ""

        lines = respuesta_texto.splitlines()
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if line == "Resumen:" and i + 1 < len(lines):
                resumen = lines[i + 1].strip()
                i += 1
            elif line == "Decision:" and i + 1 < len(lines):
                decision = lines[i + 1].strip()
                i += 1
            elif line == "Justificacion:" and i + 1 < len(lines):
                justificacion = lines[i + 1].strip()
                i += 1
            i += 1

        if not resumen:
            resumen = "No se proporcionó resumen."
        if not decision:
            decision = "No"
        if not justificacion:
            justificacion = "No se proporcionó justificación."

        return resumen, decision, justificacion