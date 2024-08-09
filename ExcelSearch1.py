import pandas as pd

# Load the Excel file
file_path = "C:/Users/Rameysh/Documents/file/attendance.xlsx"
raw_df = pd.read_excel(file_path, header=None)  # Load without header

# Find the row that contains the column names
def find_header_row(df):
    for i, row in df.iterrows():
        if 'Unique Id' in row.values:
            return i
    return None

header_row_index = find_header_row(raw_df)

if header_row_index is None:
    raise ValueError("Header row not found. Make sure the file contains a row with 'Unique Id'.")

# Load the DataFrame with the identified header row
df = pd.read_excel(file_path, header=header_row_index)

# Strip whitespace from the column names
df.columns = df.columns.str.strip()

# Strip whitespace from the data in each column, but only for string values
for col in df.columns:
    if df[col].dtype == "object":
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

# Function to search by Unique ID and select a column to return
def search_by_unique_id(unique_id):
    if 'Unique Id' not in df.columns:
        return "Error: 'Unique Id' column not found in the DataFrame."

    result = df[df['Unique Id'] == unique_id]
    if not result.empty:
        while True:
            print("Available columns:")
            for i, column in enumerate(result.columns):
                print(f"{i+1}. {column}")

            # Prompt user to select a column
            try:
                column_index = int(input("Enter the number corresponding to the column you want to retrieve (or type '0' to go back): ")) - 1
                if column_index == -1:
                    break
                if 0 <= column_index < len(result.columns):
                    selected_column = result.columns[column_index]
                    print(f"Value from column '{selected_column}': {result[selected_column].iloc[0]}")
                else:
                    print("Invalid selection. Please choose a valid number.")
            except ValueError:
                print("Please enter a valid number.")
    else:
        print(f"No record found with Unique Id: {unique_id}")

# Loop to allow multiple searches
while True:
    unique_id_to_search = input("Enter the Unique Id to search (or type 'exit' to quit): ")
    if unique_id_to_search.lower() == 'exit':
        print("Exiting the search program.")
        break
    try:
        unique_id_to_search = int(unique_id_to_search)
        search_by_unique_id(unique_id_to_search)
    except ValueError:
        print("Please enter a valid number for the Unique Id.")
