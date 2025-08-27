from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from linkedin_scraper import LinkedInScraper
from data_manager import DataManager
from hface_handler import HuggingFaceHandler
import os
from dotenv import load_dotenv

# Cargar credenciales desde .env
load_dotenv()
user = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASS")

# Crear el Service con la ruta del driver
service = Service(ChromeDriverManager().install())

# Inicializar el navegador usando el service
driver = webdriver.Chrome(service=service)

# Instanciar el scraper
scraper = LinkedInScraper(driver)
scraper.login(user, password)

# Ir a la sección de empleos
scraper.go_to_jobs()
scraper.click_show_all()
# Obtener las tarjetas de trabajos y extraer info
job_cards = scraper.get_job_cards()

jobs_data = []
for job in job_cards[:4]: # Solo tomamos los primeros 5 jobs
    try:
        info = scraper.extract_job_info(job)
        jobs_data.append(info)
    except Exception as e:
        print("Error al extraer la oferta:", e)

# Guardar en CSV
dm = DataManager()
dm.save_jobs(jobs_data)

# Cerrar el navegador
driver.quit()

# Evaluar los jobs usando HuggingFaceHandler
huggingface = HuggingFaceHandler()
dm.evaluate_jobs(huggingface)