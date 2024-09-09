import pandas as pd
import re

# Define file names
input_csv_file = 'merojob_listings_selenium.csv'
output_csv_file = 'cleaned_merojob_listings.csv'

def parse_deadline(deadline_text):
    """
    Parse the deadline text and classify it into categories.
    """
    if pd.isna(deadline_text) or deadline_text.strip().upper() == 'N/A':
        return deadline_text, 4  # Return 'N/A' and a fallback category

    deadline_text = str(deadline_text).lower()  # Convert to string and lowercase for consistency

    # Initialize the return values
    hours = days = weeks = None

    # Check for hours, days, and weeks in the deadline_text
    if "hour" in deadline_text:
        hours = int(re.search(r'\d+', deadline_text).group())
    if "day" in deadline_text:
        days = int(re.search(r'\d+', deadline_text).group())
    if "week" in deadline_text:
        weeks = int(re.search(r'\d+', deadline_text).group())
    
    # Determine category based on the presence of hours, days, and weeks
    if weeks is not None:
        category = 3  # Weeks
    elif days is not None and hours is not None:
        category = 2  # Days and Hours
    elif days is not None:
        category = 1  # Days only
    elif hours is not None:
        category = 0  # Hours only
    else:
        category = 4  # Fallback for any unexpected cases
    
    return deadline_text, category

def clean_and_sort_csv():
    """
    Clean the CSV file and sort the data by deadline.
    """
    # Load the data
    df = pd.read_csv(input_csv_file)

    # Drop rows where 'Deadline' is 'N/A'
    df = df[df['Deadline'].str.strip().ne('N/A')]

    # Apply the parse_deadline function and expand the result into separate columns
    parsed_data = df['Deadline'].apply(parse_deadline)
    parsed_df = pd.DataFrame(parsed_data.tolist(), columns=['Original_Deadline', 'Category'])
    
    # Ensure the lengths match
    assert len(df) == len(parsed_df), "Mismatch between original and parsed data lengths."

    # Assign the parsed columns to the DataFrame
    df[['Original_Deadline', 'Category']] = parsed_df

    # Sort by Category (0: hours only, 1: days only, 2: days and hours, 3: weeks) and then by Original_Deadline
    df = df.sort_values(by=['Category', 'Original_Deadline'])

    # Drop the 'Category' column as it's no longer needed
    df = df.drop(columns=['Category'])

    # Save the cleaned and sorted data
    df.to_csv(output_csv_file, index=False)
    print(f"Data cleaned and sorted by deadline. Saved to {output_csv_file}")

if __name__ == '__main__':
    clean_and_sort_csv()


