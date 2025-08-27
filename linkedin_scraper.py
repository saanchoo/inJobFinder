from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LinkedInScraper:
    def __init__(self, driver):
        self.driver = driver

    def login(self, user, password):
        self.driver.get("https://www.linkedin.com/login")
        print("Navegando a la página de login")
        self.driver.find_element(By.ID, "username").send_keys(user)
        print("Usuario ingresado")
        self.driver.find_element(By.ID, "password").send_keys(password)
        print("Contraseña ingresada")
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        print("Formulario enviado")
        time.sleep(15)  # Esperamos a que cargue la página después de login
        print("Espera post-login completada")

    def go_to_jobs(self):
        # Click en "Empleos"
        self.driver.find_element(By.XPATH, '//span[text()="Empleos"]/parent::a').click()
        print("Click en Empleos realizado")
        time.sleep(3)
        print("Espera después de ir a Empleos completada")

    def click_show_all(self):
        time.sleep(2)
        print("Esperando antes de hacer click en Mostrar todo")
        show_all_button = self.driver.find_element(
            By.XPATH, '//a[@aria-label="Mostrar todo Principales empleos que te recomendamos"]'
        )
        show_all_button.click()
        print("Click en Mostrar todo realizado")
        time.sleep(2)
        print("Espera después de click en Mostrar todo completada")

    def get_job_cards(self):
        # UL con las jobs cards (actualizado para la nueva estructura de LinkedIn)
        all_cards = self.driver.find_elements(By.CSS_SELECTOR, "ul.BhfUEgJEYTGtIqejguYThjuDZXHk > li")
        job_cards = [li for li in all_cards if li.find_elements(By.CSS_SELECTOR, "div.job-card-container")]
        print(f"Se encontraron {len(job_cards)} tarjetas de trabajo con contenido")
        return job_cards

    def extract_job_info(self, job_card):
        job_card.click()
        print("Tarjeta de trabajo clickeada")
        time.sleep(2)
        print("Espera después de click en tarjeta completada")

        title_element = job_card.find_element(By.XPATH, './/a[contains(@class,"job-card-container__link")]')
        title = title_element.text
        print(f"Título obtenido: {title}")

        company_element = self.driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__company-name a")
        company = company_element.text.strip()
        print(f"Compañía obtenida: {company}")

        link = title_element.get_attribute("href").strip()
        print(f"Link obtenido: {link}")

        description_element = self.driver.find_element(By.ID, "job-details")
        description = description_element.text
        print("Descripción obtenida")

        return {"title": title, "company": company, "link": link, "description": description}