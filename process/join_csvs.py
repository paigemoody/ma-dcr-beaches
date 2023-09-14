import os
import pandas as pd

# Function to process and join CSV files
def process_csv_files(input_dir, output_file):
    df_list = []
    date_columns = {}  # Dictionary to store date-to-column mapping

    # Iterate through CSV files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            file_path = os.path.join(input_dir, filename)
            date = filename.split('-')[1:]  # Extract year, month, and day from the filename
            date_str = "_".join(date)
            df = pd.read_csv(file_path)

            # Rename the "Type of Beach" column to "Beach Type" if it exists
            if "Type of Beach" in df.columns:
                df.rename(columns={"Type of Beach": "Beach Type"}, inplace=True)

            # Rename the "Posting Reason" column to match the desired format
            new_column_name = f"posting_reason_{date_str}".replace("pm.csv", "")
            df.rename(columns={"Posting Reason": new_column_name}, inplace=True)

            # Set the index for joining
            df.set_index(["Municipality", "Beach", "Beach Type"], inplace=True)

            # Store the date-to-column mapping
            date_columns[date_str] = new_column_name

            # Append the modified DataFrame to the list
            df_list.append(df)

    # Perform a full join on the specified columns
    merged_df = pd.concat(df_list, axis=1, join="outer")

    # Reset the index to convert the columns back to regular columns
    merged_df.reset_index(inplace=True)

    # Sort the DataFrame by "Municipality" column
    merged_df.sort_values(by="Municipality", inplace=True)

    # Sort columns by date from left to right
    sorted_columns = ["Municipality", "Beach", "Beach Type"] + [date_columns[date] for date in sorted(date_columns.keys())]
    merged_df = merged_df[sorted_columns]

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(output_file, index=False)

if __name__ == "__main__":
    input_directory = os.path.join("process", "outputs")  # Directory containing the CSV files
    output_csv = os.path.join(input_directory, "joined_output.csv")  # Output CSV file name
    process_csv_files(input_directory, output_csv)
