import requests
import pandas as pd
import json
import logging
import sqlite3
from bs4 import BeautifulSoup

# Set up logging for tracking the scraping process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RealEstateScraper:
    def __init__(self):
        self.listings = []
        self.base_url = 'https://www.realtor.com/realestateandhomes-search/'
        self.database = 'real_estate_listings.db'
        self.create_database()

    def create_database(self):
        """Create an SQLite database and a table for listings."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS listings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    address TEXT,
                    bedrooms TEXT,
                    bathrooms TEXT,
                    square_footage TEXT,
                    price_value REAL UNIQUE
                )
            ''')
            conn.commit()

    def scrape_page(self, location):
        """Scrape property listings from a specific location."""
        page_url = f'{self.base_url}{location}'
        logging.info(f'Scraping {page_url}...')
        
        try:
            response = requests.get(page_url)
            response.raise_for_status()  # Raise an error for bad responses
            
            soup = BeautifulSoup(response.text, 'html.parser')
            properties = soup.find_all('li', class_='component_property-card')

            for property in properties:
                title_tag = property.find('span', class_='listing-price')
                address_tag = property.find('span', class_='listing-address')
                beds_tag = property.find('li', class_='data-value beds')
                baths_tag = property.find('li', class_='data-value baths')
                sqft_tag = property.find('li', class_='data-value sq ft')

                # Extracting data with fallback for missing information
                title = title_tag.get_text(strip=True) if title_tag else 'No Price'
                address = address_tag.get_text(strip=True) if address_tag else 'No Address'
                beds = beds_tag.get_text(strip=True) if beds_tag else 'N/A'
                baths = baths_tag.get_text(strip=True) if baths_tag else 'N/A'
                sqft = sqft_tag.get_text(strip=True) if sqft_tag else 'N/A'

                # Clean and convert price to a number for sorting
                price_value = self.clean_price(title)

                # Append to the listings list as a dictionary
                self.listings.append({
                    'Title': title,
                    'Address': address,
                    'Bedrooms': beds,
                    'Bathrooms': baths,
                    'Square Footage': sqft,
                    'Price Value': price_value  # Store numeric value for sorting
                })

            logging.info(f'Found {len(properties)} properties on {page_url}.')

        except requests.exceptions.RequestException as e:
            logging.error(f"Request error: {e}")

    def clean_price(self, price_str):
        """Convert price string to a numeric value."""
        try:
            return float(price_str.replace('$', '').replace(',', '').strip())
        except ValueError:
            return float('inf')  # Assign a high value for sorting if conversion fails

    def scrape_all_listings(self, location):
        """Scrape all listings for a given location."""
        self.scrape_page(location)

    def save_to_database(self):
        """Insert or update listings in the SQLite database."""
        with sqlite3.connect(self.database) as conn:
            cursor = conn.cursor()
            for listing in self.listings:
                try:
                    cursor.execute('''
                        INSERT INTO listings (title, address, bedrooms, bathrooms, square_footage, price_value)
                        VALUES (?, ?, ?, ?, ?, ?)
                    ''', (listing['Title'], listing['Address'], listing['Bedrooms'], listing['Bathrooms'], listing['Square Footage'], listing['Price Value']))
                except sqlite3.IntegrityError:
                    logging.info(f"Listing already exists in database: {listing['Title']}")
                    # Optionally update existing record here if needed

            conn.commit()
            logging.info(f'Saved {len(self.listings)} listings to the database.')

def main():
    location = 'Los-Angeles_CA'  # Change this to your desired location
    scraper = RealEstateScraper()
    
    try:
        scraper.scrape_all_listings(location)
        
        # Save results to the SQLite database
        scraper.save_to_database()

    except Exception as e:
        logging.error(f'An error occurred: {e}')

if __name__ == '__main__':
    main()