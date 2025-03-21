from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")

service = Service(ChromeDriverManager().install())
browser = webdriver.Chrome(service=service, options=chrome_options)
olx_url = "https://www.olx.in/items/q-car-cover?isSearchCall=true"
browser.get(olx_url)
time.sleep(7) 

for _ in range(3):
    browser.execute_script("window.scrollBy(0, 600)")
    time.sleep(3)

ads_data = []
try:
    listings = browser.find_elements(By.XPATH, '//li[contains(@data-aut-id, "itemBox")]')

    if not listings:
        print("No ads found! Trying alternate XPATH...")  
        listings = browser.find_elements(By.XPATH, '//div[contains(@class, "listing")]')

    for ad in listings:
        try:
            ad_title = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "itemTitle")]').text or "N/A"
            ad_price = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "itemPrice")]').text or "N/A"
            ad_location = ad.find_element(By.XPATH, './/span[contains(@data-aut-id, "item-location")]').text or "N/A"
        except:
            ad_title, ad_price, ad_location = "N/A", "N/A", "N/A"

        ads_data.append([ad_title, ad_price, ad_location])

except Exception as e:
    print(f"Error: {e}")

browser.quit()

if ads_data:
    print(tabulate(ads_data, headers=["Title", "Price", "Location"], tablefmt="grid"))
else:
    print("Still no ads found! Try manually checking the website structure.")



