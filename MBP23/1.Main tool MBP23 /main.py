import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui.WebDriverWait
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
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "searchform")))
        search_box = driver.find_element(By.ID, "txtEntityName")
        search_box.clear()
        search_box.send_keys(business_name)
        search_button = driver.find_element(By.ID, "SearchSubmit")
        search_button.click()
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "entityData")))
        entity_name_links = driver.find_elements(By.CSS_SELECTOR, "#entityData tbody tr.GridRow a.link")
        links = [link.get_attribute('href') for link in entity_name_links]
        return links
    except Exception as e:
        print(f"Error searching for business: {e}")
        return []

def get_registered_agent_name(link, driver):
    try:
        driver.get(link)
        registered_agent_element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, 'MainContent_lblResidentAgentName')))
        return registered_agent_element.text
    except TimeoutException:
        return "Not Found"

def main(input_dir, output_dir, csv_file_name):
    print("Starting script...")
    driver = setup_driver()

    csv_file_path = os.path.join(input_dir, csv_file_name)
    print(f"Reading CSV file: {csv_file_path}")
    data = pd.read_csv(csv_file_path)

    if 'BusinessName' not in data.columns:
        print("Error: 'BusinessName' column not found.")
        driver.quit()
        exit()

    data.insert(1, 'Registered Agent', "")

    for index, row in data.iterrows():
        if index >= 5:
            break

        business_name = row['BusinessName']
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
    output_file_name = f'results_{timestamp}.csv'
    output_file_path = os.path.join(output_dir, output_file_name)
    data.to_csv(output_file_path, index=False)
    print(f"Updated data saved to: {output_file_path}")

    driver.quit()

if __name__ == "__main__":
    input_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/MBP23/1.Main tool MBP23 /1.Start'
    output_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/MBP23/1.Main tool MBP23 /2.Results'
    csv_file_name = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/MBP23/1.Main tool MBP23 /1.Start/test sheet.csv'
    main(input_dir, output_dir, csv_file_name)


# pyhton3 main.py