import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

def search_michigan_business_registry(business_name, driver):
    url = 'https://cofs.lara.state.mi.us/CorpWeb/CorpSearch/CorpSearch.aspx'
    driver.get(url)
    
    try:
        # Wait until the search form is visible
        search_form = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "searchform")))
        
        # Find and interact with the search elements
        search_box = search_form.find_element(By.ID, "txtEntityName")
        search_box.clear()
        search_box.send_keys(business_name)
        
        search_button = search_form.find_element(By.ID, "SearchSubmit")
        search_button.click()

        # Wait for search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "entityData")))
        
        # Extract relevant information
        entity_name_links = driver.find_elements(By.CSS_SELECTOR, "#entityData tbody tr.GridRow a.link")
        links = [link.get_attribute('href') for link in entity_name_links]
        
        return links
    except Exception as e:
        print(f"Error searching for business: {e}")
        return []

def get_registered_agent_name(link, driver):
    driver.get(link)
    try:
        registered_agent_element = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.ID, 'MainContent_lblResidentAgentName'))
        )
        registered_agent_name = registered_agent_element.text
        return registered_agent_name
    except TimeoutException:
        return ""

def main():
    print("Starting script...")
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)

    csv_file_path = 'Cold Calling _ Cold email CRM orgainzation - Copy of Cold Calling.csv'
    print(f"Reading CSV file: {csv_file_path}")
    data = pd.read_csv(csv_file_path)

    # Check if 'Business Name' column exists
    if 'Business Name' not in data.columns:
        print("Error: 'Business Name' column not found.")
        driver.quit()  # Quit the driver if there's an error
        exit()  # Exit the script

    # Add a new column for the registered agent
    data['B'] = ""

    print("Company Name\tRegistered Agent")
    for index, row in data.iterrows():
        if index >= 10:  # Limit to the first 25 entries
            break

        business_name = row['Business Name']
        if pd.notna(business_name):
            links = search_michigan_business_registry(business_name, driver)
            if links:
                registered_agent_name = get_registered_agent_name(links[0], driver)
                if registered_agent_name:
                    data.at[index, 'B'] = registered_agent_name
                    print(f"{business_name}\t{registered_agent_name}")
            else:
                print(f"{business_name}\tInfo not found")

    # Save the updated data to a CSV file with timestamp in the file name
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    output_file_path = f'results_{timestamp}.csv'
    data.to_csv(output_file_path, index=False)
    print(f"Updated data saved to: {output_file_path}")

    driver.quit()  # Quit the driver after completing the script

if __name__ == "__main__":
    main()
