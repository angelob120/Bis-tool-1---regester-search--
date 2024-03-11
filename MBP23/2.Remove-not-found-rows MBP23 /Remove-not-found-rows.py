import pandas as pd
from datetime import datetime
import os

def clean_csv(input_dir, output_dir, csv_file_name):
    try:
        # Construct the full path of the input CSV file
        csv_file_path = os.path.join(input_dir, csv_file_name)

        # Read the CSV file
        df = pd.read_csv(csv_file_path)

        # Check 'Registered Agent' column and remove rows with 'Not Found'
        df_cleaned = df[df['Registered Agent'] != 'Not Found']

        # Generate the new file name with the current date
        today = datetime.now().strftime('%Y-%m-%d')
        new_file_name = f'{today}_cleaned.csv'

        # Construct the full path of the output CSV file
        output_file_path = os.path.join(output_dir, new_file_name)

        # Save the modified dataframe to the new CSV file
        df_cleaned.to_csv(output_file_path, index=False)

        print(f"Cleaned data saved to: {output_file_path}")
        return output_file_path
    except Exception as e:
        print(str(e))
        return None

# Usage example (replace with actual paths and file name)
input_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/Remove-not-found-rows/1.Start'
output_dir = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/Remove-not-found-rows/1.Start'
csv_file_name = '/Users/angelobrown/Downloads/Bis-tool-1---regester-search--/Remove-not-found-rows/1.Start/test sheet _ uplaoded to be filtered- Sheet1 (4) - Sheet1.csv'
cleaned_file_path = clean_csv(input_dir, output_dir, csv_file_name)


# The file_path will be replaced with the path of the uploaded file
# For example:
# file_path = '/mnt/data/uploaded_file.csv'
# cleaned_file = clean_csv(file_path)
# print(f"Cleaned file saved as: {cleaned_file}")




# python3 Remove-not-found-rows.py