import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime


def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-images")  # Disable images
    return webdriver.Chrome(options=chrome_options)

def search_michigan_business_registry(business_name, driver):
    url = 'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSearch.aspx'
    driver.get(url)
    
    try:
        WebDriverWait(driver, 1).until(EC.visibility_of_element_located((By.ID, "searchform")))
        search_box = driver.find_element(By.ID, "txtEntityName")
        search_box.clear()
        search_box.send_keys(business_name)
        search_button = driver.find_element(By.ID, "SearchSubmit")
        search_button.click()
        WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.ID, "entityData")))
        entity_name_links = driver.find_elements(By.CSS_SELECTOR, "#entityData tbody tr.GridRow a.link")
        links = [link.get_attribute('href') for link in entity_name_links]
        return links
    except Exception as e:
        print(f"Error searching for business: {e}")
        return []

def get_registered_agent_name(link, driver):
    try:
        driver.get(link)
        registered_agent_element = WebDriverWait(driver, 2).until(EC.visibility_of_element_located((By.ID, 'MainContent_lblResidentAgentName')))
        return registered_agent_element.text
    except TimeoutException:
        return "Not Found"

def main():
    print("Starting script...")
    driver = setup_driver()

    csv_file_path = '/Users/angelobrown/Bis tool 1 ( regester search )/test sheet _ uplaoded to be filtered- Sheet1 (4) - Sheet1.csv'
    print(f"Reading CSV file: {csv_file_path}")
    data = pd.read_csv(csv_file_path)

    if 'BusinessName' not in data.columns:
        print("Error: 'BusinessName' column not found.")
        driver.quit()
        exit()

    data.insert(1, 'Registered Agent', "")

    for index, row in data.iterrows():
        if index >= 894:
            break

        business_name = row['BusinessName']  # Changed from 'Business Name' to 'BusinessName'
        if pd.notna(business_name):
            links = search_michigan_business_registry(business_name, driver)
            registered_agent_name = "Not Found"
            if links:
                name = get_registered_agent_name(links[0], driver)
                if name:
                    registered_agent_name = name
            data.at[index, 'Registered Agent'] = registered_agent_name

    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = f'results_{timestamp}.csv'
    data.to_csv(output_file_path, index=False)
    print(f"Updated data saved to: {output_file_path}")

    driver.quit()

if __name__ == "__main__":
    main()


# python3 main.py
# change the number in the index to the number of lines there are in the spread sheet
# update the path the the search file




# python3 --version
# pip3 install pandas
# pip3 install selenium
# Download and set up ChromeDriver manually
# Check your Chrome version
# google-chrome --version

# Go to the ChromeDriver download page (https://sites.google.com/chromium.org/driver/) and download the matching version for your OS.

# After downloading, unzip the file
# unzip chromedriver_linux64.zip

# Move ChromeDriver to /usr/local/bin (or any directory in your PATH)
# sudo mv chromedriver /usr/local/bin/

# Verify installation
# chromedriver --version
