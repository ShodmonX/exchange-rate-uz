import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException



class ScraperClient:
    def __init__(self, url) -> None:
        self.url = url
        self.options = Options()
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument('--headless=new')
        # self.options.add_argument('--disable-gpu')
        # self.options.add_argument('--no-sandbox')
        # self.options.add_argument('--disable-dev-shm-usage')
        
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_driver(self):
        """Creates and configures a Selenium WebDriver instance with stealth settings."""
        try:
            driver = webdriver.Chrome(options=self.options)
            # from selenium_stealth import stealth
            # stealth(driver,
            #         languages=["en-US", "en"],
            #         vendor="Google Inc.",
            #         platform="Win32",
            #         webgl_vendor="Intel Inc.",
            #         renderer="Intel Iris OpenGL Engine",
            #         fix_hairline=True)
            return driver
        except WebDriverException as e:
            logging.error(f"Failed to create WebDriver: {e}")
            raise

    def get_page_source(self) -> str | None:
        """Retrieves the HTML page source for a given URL."""
        driver = self.create_driver()
        try:
            driver.get(self.url)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            html = driver.page_source
            return html
        except TimeoutException:
            logging.warning(f"Timeout waiting for page elements at {self.url}")
            return driver.page_source
        except WebDriverException as e:
            logging.error(f"Error fetching page {self.url}: {e}")
            return None
        finally:
            driver.quit()

    def main(self) -> None:
        page_source = self.get_page_source()
        with open("test.html", "w", encoding="utf-8") as f:
            if page_source:
                f.write(page_source)

    def __call__(self) -> None:
        self.main()


if __name__ == '__main__':
    scraper = ScraperClient("https://nbu.uz/jismoniy-shaxslar-valyutalar-kursi")
    scraper()