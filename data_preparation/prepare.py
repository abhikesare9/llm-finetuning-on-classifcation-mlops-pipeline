import pandas as pd
from sklearn.model_selection import train_test_split
import pandas as pd
import requests
import zipfile
from io import BytesIO

class data_preparation():
   
    @staticmethod
    def download_and_extract_zip(url, output_dir):
        """
        Downloads a ZIP file from Google Drive and extracts it.

        :param gdrive_file_id: The ID of the Google Drive file.
        :param output_dir: The directory where the ZIP file will be extracted.
        """

        # Make a request to get the file
        response = requests.get(url, allow_redirects=True)
        
        if response.status_code == 200:
            # Open the ZIP file in memory
            with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
                # Extract all contents to the output directory
                zip_file.extractall(output_dir)
                print(f"Extracted files to {output_dir}")
        else:
            print(f"Failed to download file: {response.status_code}")

    @staticmethod        
    def split_data(input_file, train_file, test_file, test_size=0.2, random_state=None):
        """
        Splits the dataset into training and testing sets and saves them to separate files.

        :param input_file: Path to the input dataset (CSV file).
        :param train_file: Path to save the training set (CSV file).
        :param test_file: Path to save the testing set (CSV file).
        :param test_size: Proportion of the dataset to include in the test split (default is 0.2).
        :param random_state: Controls the shuffling applied to the data before applying the split.
        """
        # Load the dataset
        data = pd.read_csv(input_file)

        # Split the dataset into training and testing sets
        train_data, test_data = train_test_split(data, test_size=test_size, random_state=random_state)

        # Save the training and testing sets to new CSV files
        train_data.to_csv(train_file, index=False)
        test_data.to_csv(test_file, index=False)

        print(f"Data has been split into train and test sets.")
        print(f"Training data saved to: {train_file}")
        print(f"Testing data saved to: {test_file}")

    @staticmethod
    def convert_tsv_to_csv(tsv_file, csv_file):
        """
        Converts a TSV file to a CSV file.

        :param tsv_file: Path to the input TSV file.
        :param csv_file: Path to save the output CSV file.
        """
        # Read the TSV file
        try:
            data = pd.read_csv(tsv_file, sep='\t')
            
            # Save the DataFrame as a CSV file
            data.to_csv(csv_file, index=False)
            print(f"Successfully converted {tsv_file} to {csv_file}")
        except Exception as e:
            print(f"Error during conversion: {e}")

    @staticmethod
    def save_selected_columns(input_file: str, output_file: str, columns: list):
        """
        Load a DataFrame from a CSV file, select specified columns, and save them to a new CSV file.

        Parameters:
        - input_file (str): Path to the input CSV file.
        - output_file (str): Path to save the output CSV file.
        - columns (list): List of columns to select from the DataFrame.

        Returns:
        - None
        """
        # Load the DataFrame from the input CSV file
        df = pd.read_csv(input_file)

        # Select the specified columns
        selected_df = df[columns]

        # Save the selected columns to a new CSV file
        selected_df.to_csv(output_file, index=False)
        print(f"Selected columns saved to {output_file}.")

    @staticmethod
    def merge_and_save_columns(input_file, output_file):
        """
        Merges 'claim', 'main_text', and 'explanation' columns from a CSV file into a single 'text' column 
        and saves the modified DataFrame to a new CSV file.

        Parameters:
        input_file (str): Path to the input CSV file.
        output_file (str): Path to save the modified CSV file.
        """
        # Load the DataFrame from the CSV file
        df = pd.read_csv(input_file)

        # Check if the required columns are present
        if not all(col in df.columns for col in ['claim', 'main_text', 'explanation']):
            raise ValueError("Input DataFrame must contain 'claim', 'main_text', and 'explanation' columns.")

        # Merge the columns into a new column 'text'
        df['text'] = df['claim'] + ' ' + df['main_text'] + ' ' + df['explanation']

        # Save the updated DataFrame to a new CSV file
        df.to_csv(output_file, index=False)
        
        print(f"DataFrame saved to {output_file}")
