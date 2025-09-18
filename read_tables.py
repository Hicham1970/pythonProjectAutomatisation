import pandas as pd

############### Read a .csv file from an URL
# reading csv from website
target_web = 'https://www.football-data.co.uk/mmz4281/2324/E0.csv'  # Example: Premier League 2023-2024 data

try:
    df = pd.read_csv(target_web)
    print("DataFrame loaded successfully:")
    print(df.head())  # showing dataframe

    # rename columns (example: rename 'old_column' to 'new_column' if applicable)
    # df.rename(columns={'old_column': 'new_column'}, inplace=True)
    # print("Columns renamed.")
    # print(df.head())

except Exception as e:
    print(f"Error reading CSV: {e}")
    print("Note: The URL might not point to a direct CSV file. Please verify the URL or provide a direct CSV link from the website.")
