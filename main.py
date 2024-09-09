import subprocess
import logging

# Define file names
raw_csv_file = 'merojob_listings_selenium.csv'
cleaned_csv_file = 'cleaned_merojob_listings.csv'

# Set up logging
logging.basicConfig(filename='process.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_scraper():
    """
    Runs the web scraper script to collect job data and save it to a CSV file.
    """
    try:
        # Run the scraper script using subprocess
        subprocess.run(['python', 'scraper.py'], check=True)
        logging.info("Data scraping completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during scraping: {e}")
        raise

def run_cleaner():
    """
    Runs the CSV cleaner script to clean the scraped data.
    """
    try:
        # Run the cleaner script using subprocess
        subprocess.run(['python', 'cleancsv.py'], check=True)
        logging.info("Data cleaning completed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error occurred during cleaning: {e}")
        raise

if __name__ == '__main__':
    # Run the scraper and cleaner in sequence
    try:
        run_scraper()
        run_cleaner()
    except Exception as e:
        logging.error(f"Failed to complete the process: {e}")
