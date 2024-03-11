import pandas as pd
import datetime
import os

def modify_business_names(input_dir, output_dir, csv_file_name):
    # Construct the full path of the input CSV file
    csv_file_path = os.path.join(input_dir, csv_file_name)

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

    # Construct the full path of the output CSV file
    output_file_path = os.path.join(output_dir, new_file_name)

    # Save the modified DataFrame to a new CSV file in the specified output directory
    df.to_csv(output_file_path, index=False)
    print(f"File saved as '{new_file_name}' in '{output_dir}'.")

# Specify the input and output directories
input_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/Add State Name/1.Start'
output_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/Add State Name/2.Results'

# Replace this with your actual CSV file name
csv_file_name = 'test sheet _ uplaoded to be filtered- Sheet1 (4) - Sheet1.csv'

# Call the function with the specified directories and file name
modify_business_names(input_dir, output_dir, csv_file_name)





# update the input / out directories for what ever comupter iam using



# pyhton3 State-to-name.py