# Importamos Selenium para controlar el navegador
from errno import ESRCH

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
# Importamos By para localizar elementos y Keys para simular teclas
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# Importamos ChromeDriverManager para gestionar automáticamente la versión del driver
from webdriver_manager.chrome import ChromeDriverManager
# Importamos time para usar sleep() y dar tiempo a que cargue la página
import time
# Importamos datetime para manejar fechas y horas si las necesitamos
import datetime as dt
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

# Creamos un service con el driver descargado
service = Service(ChromeDriverManager().install())

# Inicializamos el navegador usando el service
driver = webdriver.Chrome(service=service)
driver.get("https://www.linkedin.com/login/es")
time.sleep(2) # Esperamos a que cargue la pagina

# Localizamos los campos usuario y contraseña
username = driver.find_element(By.ID, "username")
password = driver.find_element(By.ID, "password")

##### LOGIN EN LINKEDIN

# Obtenemos las credenciales desde el .env
linkedin_user = os.getenv("LINKEDIN_USER")
linkedin_pass = os.getenv("LINKEDIN_PASS")

# Introducimos las credenciales
username.send_keys(linkedin_user)
password.send_keys(linkedin_pass)

password.send_keys(Keys.RETURN) # "Presionamos" enter para el login
time.sleep(5) # Que cargue la pagina

###### Entrar en empleos
job_link = driver.find_element(By.XPATH, '//span[@title="Empleos"]/parent::a')
job_link.click()
time.sleep(2)

###### Darle a mostrar todos
show_all_jobs = driver.find_element(By.XPATH, '//a[@aria-label="Mostrar todo Principales empleos que te recomendamos"]')
show_all_jobs.click()
time.sleep(5)

# # Filtrar por ubicación
# ubi_mad = "Madrid, Comunidad de Madrid, España"
# location_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Ciudad, estado o código postal"]')
# location_input.send_keys(Keys.RETURN)
# time.sleep(10)

# Entrar en las ofertas
job_cards = driver.find_elements(By.CSS_SELECTOR, "ul.GjoAkyOazLcNFWlLoIqzErpRGHIYJlShlaJI > li")

for job in job_cards:
    try:
        job.click() # Entramos en la oferta
        # Obtenemos la descripcion
        job_description = driver.find_element(By.CLASS_NAME, "jobs-description__container")
        # Imprimimos descipción
        print(job_description.text)
        time.sleep(2)
    except Exception as e:
        print("No se podo hacer click", e)
