import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

def search_michigan_business_registry(business_name, driver):
    print(f"Searching for business: {business_name}")
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
        entity_names = [link.text for link in entity_name_links]
        
        return links, entity_names
    except Exception as e:
        print(f"Error searching for business: {e}")
        return [], []

def main():
    print("Starting script...")
    chrome_options = Options()
    driver = webdriver.Chrome(options=chrome_options)

    csv_file_path = '/Users/angelobrown/Bis tool 1 ( regester search )/Cold Calling _ Cold email CRM orgainzation - Copy of Cold Calling.csv'
    print(f"Reading CSV file: {csv_file_path}")
    data = pd.read_csv(csv_file_path)

    # Check if 'Business Name' column exists
    if 'Business Name' not in data.columns:
        print("Error: 'Business Name' column not found.")
        driver.quit()  # Quit the driver if there's an error
        exit()  # Exit the script

    # Prepare new columns for data
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    new_columns = [timestamp + '_Link', timestamp + '_Name']
    business_name_index = data.columns.get_loc('Business Name') + 1
    for col in new_columns:
        data.insert(business_name_index, col, '')

    print(f"Total rows to process: {min(len(data), 25)}")
    for index, row in data.iterrows():
        if index >= 25:  # Limit to the first 25 entries
            break

        business_name = row['Business Name']
        if pd.notna(business_name):
            links, entity_names = search_michigan_business_registry(business_name, driver)
            if links:
                data.at[index, timestamp + '_Link'] = ', '.join(links)
                data.at[index, timestamp + '_Name'] = ', '.join(entity_names)
                print(f"Search results for '{business_name}':")
                for i, name in enumerate(entity_names):
                    print(f"{i+1}. {name}: {links[i]}")
            else:
                data.at[index, timestamp + '_Link'] = "No results found"
                data.at[index, timestamp + '_Name'] = "No results found"
                print(f"No search results found for '{business_name}'")

    # Save the results to a CSV file in the project folder
    project_folder = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(project_folder, f'search_results_{timestamp}.csv')
    data.to_csv(output_file_path, index=False)
    print(f"Results saved to: {output_file_path}")

    driver.quit()  # Quit the driver after completing the script

if __name__ == "__main__":
    main()
