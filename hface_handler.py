import os
from dotenv import load_dotenv
from transformers import pipeline

class HuggingFaceHandler:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("HFACE_API_KEY")
        self.job_filter_prompt = os.getenv("JOB_FILTER_PROMPT")

        if not self.api_key:
            raise ValueError("❌ No se encontró HFACE_API_KEY en tu .env")

        self.summarizer = pipeline("summarization", model="google/flan-t5-xl", use_auth_token=self.api_key)

    def summarize_job(self, job_description):
        prompt = f"{self.job_filter_prompt}\n\n{job_description}"

        summary = self.summarizer(prompt, max_length=300, do_sample=False)
        return summary[0]['summary_text']