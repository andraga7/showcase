import time
import random
import pandas as pd
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from bs4 import BeautifulSoup

# Set up logging for tracking the scraping process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class QuoteScraper:
    def __init__(self):
        # Set up Chrome options and initialize WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(service=ChromeService(), options=chrome_options)
        self.quotes_list = []

    def scrape_page(self, page_url):
        """Scrape quotes from a single page."""
        try:
            logging.info(f'Scraping {page_url}...')
            self.driver.get(page_url)
            time.sleep(random.uniform(1, 3))  # Random sleep to avoid detection
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            quotes = soup.find_all('div', class_='quote')

            for quote in quotes:
                text = quote.find('span', class_='text').get_text()
                author = quote.find('small', class_='author').get_text()
                tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]  # Extract tags

                # Append to the quotes list as a dictionary
                self.quotes_list.append({
                    'Quote': text,
                    'Author': author,
                    'Tags': ', '.join(tags)  # Join tags into a single string
                })

            logging.info(f'Found {len(quotes)} quotes on {page_url}.')

        except (NoSuchElementException, TimeoutException) as e:
            logging.error(f"Error while scraping {page_url}: {e}")
        
        except WebDriverException as e:
            logging.error(f"WebDriver error: {e}")

    def scrape_all_quotes(self):
        """Scrape all quotes from multiple pages until no more pages are available."""
        base_url = 'http://quotes.toscrape.com/page/'
        page_number = 1
        
        while True:
            page_url = f'{base_url}{page_number}/'
            self.scrape_page(page_url)

            # Check if there's a next page
            try:
                next_button = self.driver.find_element(By.CSS_SELECTOR, 'li.next > a')
                if 'next' in next_button.get_attribute('class'):
                    page_number += 1
                else:
                    break
            except NoSuchElementException:
                break

    def save_to_csv(self, file_path):
        """Save scraped quotes to a CSV file."""
        df = pd.DataFrame(self.quotes_list)
        df.to_csv(file_path, index=False)
        logging.info(f'Saved quotes to {file_path}.')

    def save_to_json(self, file_path):
        """Save scraped quotes to a JSON file."""
        with open(file_path, 'w') as json_file:
            json.dump(self.quotes_list, json_file, indent=4)
        logging.info(f'Saved quotes to {file_path}.')

    def close_driver(self):
        """Close the WebDriver."""
        self.driver.quit()

def main():
    scraper = QuoteScraper()
    
    try:
        scraper.scrape_all_quotes()
        
        # Save results to CSV and JSON formats
        scraper.save_to_csv('quotes.csv')
        scraper.save_to_json('quotes.json')

    finally:
        scraper.close_driver()

if __name__ == '__main__':
    main()
