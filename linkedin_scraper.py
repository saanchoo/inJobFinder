from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class LinkedInScraper:
    def __init__(self, driver):
        self.driver = driver

    def login(self, user, password):
        self.driver.get("https://www.linkedin.com/login")
        self.driver.find_element(By.ID, "username").send_keys(user)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
        time.sleep(15)

    def go_to_jobs(self):
        # Aquí ya tienes el click en "Empleos"
        self.driver.find_element(By.XPATH, '//span[text()="Empleos"]/parent::a').click()
        time.sleep(3)  # Esperamos a que cargue la página

    def click_show_all(self):
        # Esperamos un par de segundos por si la página aún carga
        time.sleep(2)
        # Localizamos el botón "Mostrar todo" usando el aria-label
        show_all_button = self.driver.find_element(
            By.XPATH, '//a[@aria-label="Mostrar todo Principales empleos que te recomendamos"]'
        )
        show_all_button.click()
        # Esperamos a que cargue la nueva sección
        time.sleep(2)

    def get_job_cards(self):
        return self.driver.find_elements(By.CSS_SELECTOR, "ul.GjoAkyOazLcNFWlLoIqzErpRGHIYJlShlaJI > li")

    def extract_job_info(self, job_card):
        job_card.click()
        time.sleep(2)

        title_element = job_card.find_element(By.XPATH, './/a[contains(@class,"job-card-container__link")]')
        title = title_element.text

        company_element = self.driver.find_element(By.CSS_SELECTOR, "div.job-details-jobs-unified-top-card__company-name a")
        company = company_element.text.strip()

        link = title_element.get_attribute("href").strip()  # Convertimos a string y quitamos espacios

        description_element = self.driver.find_element(By.ID, "job-details")
        description = description_element.text
        return {"title": title, "company": company, "link": link, "description": description}