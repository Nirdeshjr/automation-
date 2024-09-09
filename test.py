from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def test_chromedriver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service('C:/Users/nente/Downloads/chromedriver-win64/chromedriver.exe')  # Correct path
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://www.google.com")
    print(driver.title)
    driver.quit()

if __name__ == '__main__':
    test_chromedriver()
