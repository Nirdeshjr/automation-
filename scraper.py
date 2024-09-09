import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

def get_job_data_selenium():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    service = Service('E:/Scraping/chromedriver.exe')  # Update path to chromedriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get('https://merojob.com/category/it-telecommunication/')

    job_listings = []

    # Max number of pages to scrape
    max_pages = 15
    current_page = 1

    while current_page <= max_pages:
        print(f"Scraping page {current_page}...")

        # Parse the page source with BeautifulSoup
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for job in soup.find_all('div', class_='card'):  # Update the class based on actual HTML
            try:
                job_title = job.find('a', title=True)  # Update tag/class based on actual HTML
                company_name = job.find('a', class_='text-dark')  # Update class based on actual HTML
                
                # Extract location
                location_div = job.find('div', class_='location')
                location_span = location_div.find('span', itemprop='addressLocality') if location_div else None
                location_text = location_span.text.strip() if location_span else 'N/A'

                # Extract skills
                skills_div = job.find('span', itemprop='skills')
                if skills_div:
                    skills = [skill.text.strip() for skill in skills_div.find_all('span', class_='badge')]
                    skills_text = ', '.join(skills)
                else:
                    skills_text = 'N/A'

                # Extract deadline
                deadline_div = job.find('div', class_='card-footer')
                if deadline_div:
                    deadline_meta = deadline_div.find('meta', itemprop='validThrough')
                    deadline_text = deadline_meta['content'] if deadline_meta else 'N/A'
                else:
                    deadline_text = 'N/A'

                # Extract apply before text
                apply_before_span = deadline_div.find('span', text=True) if deadline_div else None
                apply_before_text = apply_before_span.text.strip().replace('\xa0', ' ') if apply_before_span else 'N/A'

                job_listings.append({
                    'Job Title': job_title.text.strip() if job_title else 'N/A',
                    'Company Name': company_name.text.strip() if company_name else 'N/A',
                    'Location': location_text,
                    'Skills': skills_text,
                    'Deadline': apply_before_text if apply_before_text != 'N/A' else deadline_text
                })

            except Exception as e:
                print(f"Error extracting job data: {e}")

        try:
            # Scroll to the 'Next' button to ensure it's in view
            next_button = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.pagination-next'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(2)  # Wait for smooth scrolling

            # Click the 'Next' button using JavaScript
            driver.execute_script("arguments[0].click();", next_button)

            # Wait for the page to load
            time.sleep(15)

            current_page += 1

        except Exception as e:
            print(f"Error navigating to the next page: {e}")
            break

    driver.quit()
    return job_listings

def save_to_csv(job_listings, filename='merojob_listings_selenium.csv'):
    df = pd.DataFrame(job_listings)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

if __name__ == '__main__':
    jobs = get_job_data_selenium()
    if jobs:
        save_to_csv(jobs)






