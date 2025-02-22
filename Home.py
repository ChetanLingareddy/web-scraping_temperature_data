from datetime import datetime
import requests
import selectorlib
import time
from db_connection import connect_db, create_table  # Import the database functions

# Headers and URL for Web Scraping
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
}
URL = "https://programmer100.pythonanywhere.com"

# Function to scrape data from the website
def scrape(url):
    request = requests.get(url, headers=HEADERS)
    return request.text

# Function to extract data using selectorlib
def extract(source):
    extractor = selectorlib.Extractor.from_yaml_file("extract.yaml")
    value = extractor.extract(source)["Home"]
    return value

# Function to store extracted data in PostgreSQL
def store_to_db(extracted):
    conn = connect_db()
    if conn:
        cur = conn.cursor()
        extracted_time = datetime.now ().strftime ( "%Y-%m-%d %H:%M:%S" )
        cur.execute("""
            INSERT INTO scraped_data (temperature,timestamp) 
            VALUES (%s,%s);
        """, (extracted,extracted_time))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Data saved: {extracted}")
        with open ( "data.txt", "a" ) as file :
            file.write ( f"{extracted_time},{extracted}\n" )

# Main Execution
if __name__ == "__main__":
    create_table()  # Ensure table exists before inserting data
    while True:
        scraped = scrape(URL)
        extracted = extract(scraped)
        if extracted:
            store_to_db(extracted)
            print(f"Extracted Data: {extracted}")
        else:
            print("No data extracted.")
        time.sleep(20)  # Wait before next request