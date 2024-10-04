import pandas as pd

# Path to your CSV file
INPUT_CSV = 'lawyers100.csv'
OUTPUT_CSV = 'lawyers100_sorted.csv'

def count_na(row, na_values=['N/A', 'n/a', 'NaN', '', None]):
    """
    Counts the number of 'N/A' or equivalent values in a row.
    
    Parameters:
    - row (pd.Series): A row from the DataFrame.
    - na_values (list): List of values to consider as 'N/A'.
    
    Returns:
    - int: Count of 'N/A' values in the row.
    """
    return row.isin(na_values).sum()

def sort_csv_by_na(input_csv, output_csv):
    """
    Sorts the CSV rows based on the number of 'N/A' values, ascending.
    
    Parameters:
    - input_csv (str): Path to the input CSV file.
    - output_csv (str): Path to save the sorted CSV file.
    """
    # Read the CSV into a DataFrame
    try:
        df = pd.read_csv(input_csv)
        print(f"Successfully loaded '{input_csv}'.")
    except FileNotFoundError:
        print(f"Error: The file '{input_csv}' does not exist.")
        return
    except Exception as e:
        print(f"An error occurred while reading '{input_csv}': {e}")
        return
    
    # Display initial data summary
    print("\nInitial Data Summary:")
    print(df.info())
    
    # Define columns to check for 'N/A'
    # You can adjust this list if certain columns should be excluded
    columns_to_check = ['Name', 'Law Firm', 'Key Practice Areas', 'Image URL', 
                        'Phone Number', 'Email', 'city', 'Latitude', 'Longitude']
    
    # Ensure all columns exist
    missing_columns = [col for col in columns_to_check if col not in df.columns]
    if missing_columns:
        print(f"Warning: The following columns are missing in the CSV and will be ignored: {missing_columns}")
        columns_present = [col for col in columns_to_check if col in df.columns]
    else:
        columns_present = columns_to_check
    
    # Count 'N/A's in each row
    df['NA_Count'] = df[columns_present].apply(count_na, axis=1)
    
    # Display NA counts
    print("\nSample 'NA_Count' Values:")
    print(df[['Name', 'NA_Count']].head())
    
    # Sort the DataFrame by 'NA_Count' ascending
    df_sorted = df.sort_values(by='NA_Count', ascending=True)
    
    # Optionally, reset the index
    df_sorted.reset_index(drop=True, inplace=True)
    
    # Drop the temporary 'NA_Count' column
    df_sorted.drop(columns=['NA_Count'], inplace=True)
    
    # Save the sorted DataFrame to a new CSV
    try:
        df_sorted.to_csv(output_csv, index=False)
        print(f"\nSuccessfully saved the sorted data to '{output_csv}'.")
    except Exception as e:
        print(f"An error occurred while writing to '{output_csv}': {e}")
        return
    
    # Optional: Display a summary of the sorted data
    print("\nSorted Data Summary:")
    print(df_sorted.info())

if __name__ == "__main__":
    sort_csv_by_na(INPUT_CSV, OUTPUT_CSV)
