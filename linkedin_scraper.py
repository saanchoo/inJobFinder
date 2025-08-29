from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        time.sleep(5)  # Esperamos a que cargue la página después de login
        print("Espera post-login completada")

    def go_to_jobs(self):
        # Click en "Empleos"
        self.driver.find_element(By.XPATH, '//span[text()="Empleos"]/parent::a').click()
        print("Click en Empleos realizado")
        time.sleep(3)
        print("Espera después de ir a Empleos completada")

    def click_show_all(self):
        print("Esperando a que el botón 'Mostrar todo' esté disponible...")
        # Buscamos el span con texto Mostrar todo y hacemos click en su padre
        show_all_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Mostrar todo"]/parent::*'))
        )
        show_all_button.click()
        print("Click en 'Mostrar todo' realizado")
        time.sleep(5)  # Esperamos a que cargue la sección de ofertas

    def get_job_cards(self, max_jobs=10):
        job_cards = []
        seen_cards = set()

        while len(job_cards) < max_jobs:
            current_cards = self.driver.find_elements(By.CSS_SELECTOR, "div.job-card-list__entity-lockup")

            for card in current_cards:
                card_id = card.get_attribute("id")
                if card_id not in seen_cards:
                    seen_cards.add(card_id)
                    job_cards.append(card)
                    print(f"Tarjeta añadida: {card_id}, total: {len(job_cards)}")
                    if len(job_cards) >= max_jobs:
                        break

            if len(job_cards) >= max_jobs or not current_cards:
                break

            # Scroll al último card visible para cargar más
            self.driver.execute_script("arguments[0].scrollIntoView(true);", current_cards[-1])
            time.sleep(2)

        print(f"Se han cargado {len(job_cards)} tarjetas de trabajo")
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