import os
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

#load .env variables
load_dotenv()
google_form = os.getenv('GOOGLE_FORM')
zillow_url = os.getenv('CUSTOM_ZILLOW_URL')
##HEADERS
headers =\
    {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,en;q=0.8,",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Chromium\";v=\"130\", \"Opera GX\";v=\"115\", \"Not?A_Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Sec-Gpc": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0",
    }
##PULL ZILLOW RENTALS IN MY AREA
response = requests.get(url=zillow_url, headers=headers)

##Make soup
soup = BeautifulSoup(response.text, 'html.parser')
rental_listings = soup.find_all(class_='ListItem-c11n-8-107-0__sc-13rwu5a-0 StyledListCardWrapper-srp-8-107-0__sc-wtsrtn-0 dAZKuw xoFGK')

##GET LISTING LINKS
listing_links = [listing.get('href') for listing in (soup.find_all(class_='StyledPropertyCardDataArea-c11n-8-107-0__sc-10i1r6-0 iwOFcv property-card-link'))]
print(listing_links)

##GET PRICES OF LISTINGS
listing_prices = [price.text.replace("+", "") for price in (soup.find_all(class_='Text-c11n-8-107-0__sc-aiai24-0 PropertyCardInventoryBox__PriceText-srp-8-107-0__sc-1jotqb7-3 eawGuS kgaGKJ'))]
print(listing_prices)

##GET ADDRESSES OF LISTINGS
listing_address = [address.find('address').text for address in soup.find_all(class_='StyledPropertyCardDataArea-c11n-8-107-0__sc-10i1r6-0 iwOFcv property-card-link')]
print(listing_address)



# Set options to keep the Chrome browser open after script execution
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option('detach', True)

# Initiate a driver with our options
driver = webdriver.Chrome(options=chrome_options)
# URL To Load
driver.get(url=google_form)
time.sleep(3)  # Let's give some time for the page to fully load
for n in range(len(listing_links)):
    #find & input listing address
    address_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address_input.send_keys(f'{listing_address[n]}')
    #find & input rent
    rent_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    rent_input.send_keys(f'{listing_prices[n]}')
    #find & input links
    link_input = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input.send_keys(f'{listing_links[n]}')
    #Submit
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    submit_button.click()
    time.sleep(2)
    #Clear Form
    new_form = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    new_form.click()





