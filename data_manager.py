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
            try:
                df = pd.read_csv(self.filepath)
                if df.empty:
                    print(f"El archivo {self.filepath} está vacío. Creando DataFrame vacío con columnas necesarias.")
                    df = pd.DataFrame(columns=["title", "company", "location", "description"])
                return df
            except pd.errors.EmptyDataError:
                print(f"El archivo {self.filepath} no tiene datos. Creando DataFrame vacío.")
                return pd.DataFrame(columns=["title", "company", "location", "description"])
        else:
            print(f"No se encontró el archivo: {self.filepath}")
            return pd.DataFrame(columns=["title", "company", "location", "description"])

    def evaluate_jobs(self, handler):
        df = self.load_jobs()
        if df.empty:
            print("No hay jobs para procesar.")
            return

        df["Resumen"] = ""
        df["Decision"] = ""
        df["Justificacion"] = ""

        # Detectar la columna de descripción correcta
        if "description" in df.columns:
            desc_col = "description"
        elif "Description" in df.columns:
            desc_col = "Description"
        else:
            print("No se encontró ninguna columna de descripción válida.")
            return

        for index, row in df.iterrows():
            description = row.get(desc_col, "")
            if not description:
                continue

            # Recortar la descripción a 1000 caracteres para evitar errores de tokens largos
            description = description[:1000]

            # Llamada al handler para obtener resumen y decisión
            resumen, decision, justificacion = handler.summarize_job(description)

            df.at[index, "Resumen"] = resumen
            df.at[index, "Decision"] = decision
            df.at[index, "Justificacion"] = justificacion

            print(f"Job {index + 1}/{len(df)} evaluado: {decision}")

        # Eliminar la columna description antes de guardar
        if desc_col in df.columns:
            df = df.drop(columns=[desc_col])

        df.to_csv(self.cooked_path, index=False)
        print(f"CSV procesado guardado en: {self.cooked_path}")