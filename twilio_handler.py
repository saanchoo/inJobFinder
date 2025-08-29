import pandas as pd
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
target_number = os.getenv("TARGET_NUMBER")


class TwilioHandler:
    def __init__(self, cooked_csv_path=None, jobs_list=None):
        """
        Puedes pasar un CSV con los trabajos evaluados o una lista de diccionarios.
        """
        if cooked_csv_path:
            self.jobs_df = pd.read_csv(cooked_csv_path)
        elif jobs_list:
            self.jobs_df = pd.DataFrame(jobs_list)
        else:
            raise ValueError("Debes pasar un CSV o una lista de trabajos")

        self.client = Client(account_sid, auth_token)

    def select_top_jobs(self, max_jobs=5):
        try:
            decision_col = 'Decision'
            top_jobs = self.jobs_df[self.jobs_df[decision_col] == 5]
        except KeyError:
            decision_col = self.jobs_df.columns[-2]
            top_jobs = self.jobs_df[self.jobs_df[decision_col] == 5]

        if top_jobs.shape[0] < max_jobs:
            remaining_slots = max_jobs - top_jobs.shape[0]
            top_4_jobs = self.jobs_df[self.jobs_df[decision_col] == 4]
            top_jobs = pd.concat([top_jobs, top_4_jobs.head(remaining_slots)])

        if top_jobs.shape[0] < max_jobs:
            remaining_slots = max_jobs - top_jobs.shape[0]
            top_3_jobs = self.jobs_df[self.jobs_df[decision_col] == 3]
            top_jobs = pd.concat([top_jobs, top_3_jobs.head(remaining_slots)])

        return top_jobs.head(max_jobs)

    def format_for_twilio(self, max_jobs=5):
        selected_jobs = self.select_top_jobs(max_jobs)
        messages = []
        for _, job in selected_jobs.iterrows():
            msg = f"{job['title']} (Nota: {job['Decision']})\nLink: {job['link']}"
            messages.append(msg)
        return messages

    def send_whatsapp_jobs(self, max_jobs=5):
        messages = self.format_for_twilio(max_jobs)
        for msg in messages:
            self.client.messages.create(
                body=msg,
                from_=f'whatsapp:{twilio_number}',
                to=f'whatsapp:{target_number}'
            )
            print(f"Enviado WhatsApp:\n{msg}\n")

    def send_jobs(self, max_jobs=5):
        self.send_whatsapp_jobs(max_jobs)