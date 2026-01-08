import pandas as pd

def read_csv(file_path):
    """
    Reads a CSV file using pandas.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame: A DataFrame containing the data from the CSV file.
    """

    try:
        # Attempt to read the CSV file
        df = pd.read_csv(file_path)
        
        return df
    
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    
    except pd.errors.EmptyDataError:
        print(f"Error: The file {file_path} is empty.")
    
    except pd.errors.ParserError as e:
        print(f"Error parsing the CSV file: {e}")
    
    return None

# Usage example:
file_path = "data.csv"
df = read_csv(file_path)

if df is not None:
    # Process the DataFrame as needed
    print(df.head())  # Print the first few rows of the DataFrame
else:
    print("Failed to read the CSV file.")
