from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import os

urls = [
    "https://www.muet.edu.pk/",
    "https://www.muet.edu.pk/admissions",
    "https://www.muet.edu.pk/faculties"
]

# start browser
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

all_text = ""

for url in urls:

    driver.get(url)

    time.sleep(5)   # allow page to load

    soup = BeautifulSoup(driver.page_source, "html.parser")

    text = soup.get_text(separator=" ", strip=True)

    all_text += text + "\n\n"

    print(f"Scraped: {url}")

driver.quit()

os.makedirs("data", exist_ok=True)

with open("data/muet_data.txt", "w", encoding="utf-8") as f:

    
    f.write(all_text)

print("Scraping completed and saved in data/muet_data.txt")