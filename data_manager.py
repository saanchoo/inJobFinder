import pandas as pd
import os

class DataManager:
    def __init__(self, filename="jobs_raw.csv", cooked_filename="jobs_cooked.csv", folder="jobs"):
        self.folder = folder
        self.filename = filename
        self.cooked_filename = cooked_filename
        self.filepath = os.path.join(self.folder, self.filename)
        self.cooked_path = os.path.join(self.folder, self.cooked_filename)

        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def save_jobs(self, job_list):
        df = pd.DataFrame(job_list)
        df.to_csv(self.filepath, index=False)
        print(f"Archivo guardado en: {self.filepath}")

    def load_jobs(self):
        if os.path.exists(self.filepath):
            return pd.read_csv(self.filepath)
        else:
            print(f"No se encontró el archivo: {self.filepath}")
            return pd.DataFrame()

    def evaluate_jobs(self, chatgpt_handler):
        df = self.load_jobs()
        if df.empty:
            print("No hay jobs para procesar.")
            return

        df["interesante"] = False

        for index, row in df.iterrows():
            description = row.get("description", "")
            if not description:
                continue

            result = chatgpt_handler.summarize_job(description)
            df.at[index, "interesante"] = "Sí, interesa aplicar" in result
            print(f"Job {index + 1}/{len(df)} evaluado: {df.at[index, 'interesante']}")

        df.to_csv(self.cooked_path, index=False)
        print(f"CSV procesado guardado en: {self.cooked_path}")