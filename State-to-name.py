import pandas as pd
import datetime

def modify_business_names(csv_file_path):
    # Load the CSV file
    df = pd.read_csv(csv_file_path)

    # Check if 'BusinessName' column exists
    if 'BusinessName' not in df.columns:
        raise ValueError("The CSV file does not have a 'BusinessName' column.")

    # Ask the user for the state name
    state_name = input("What state are you adding? ")

    # Prepend state name to each business name in the 'BusinessName' column
    df['BusinessName'] = state_name + " " + df['BusinessName']

    # Generate a filename based on the current date
    date_str = datetime.datetime.now().strftime("%Y%m%d")
    new_file_name = f"{date_str}_modified.csv"

    # Save the modified DataFrame to a new CSV file
    df.to_csv(new_file_name, index=False)
    print(f"File saved as '{new_file_name}' in the project folder.")

# Replace 'your_file.csv' with the path to your CSV file
csv_file_name = 'test sheet _ uplaoded to be filtered- Sheet1 (4) - Sheet1.csv'
modify_business_names(csv_file_name)

