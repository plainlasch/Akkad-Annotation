import os
import csv

def combine_csv_files(input_directory, output_file):
    # List all files in the directory
    files = [f for f in os.listdir(input_directory) if f.endswith('.csv')]

    # Check if there are any CSV files to process
    if not files:
        print("No CSV files found in the directory.")
        return

    # Open the output file in write mode
    with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
        csv_writer = csv.writer(outfile)

        # Initialize a flag to check if we need to write the header
        header_written = False

        # Iterate over each CSV file in the directory
        for file in files:
            file_path = os.path.join(input_directory, file)
            
            with open(file_path, mode='r', encoding='utf-8') as infile:
                csv_reader = csv.reader(infile)
                header = next(csv_reader)  # Read the header row

                # Write the header only once (for the first file)
                if not header_written:
                    csv_writer.writerow(header)
                    header_written = True

                # Write the rows from each CSV file
                for row in csv_reader:
                    csv_writer.writerow(row)

    print(f"All CSV files have been combined into {output_file}.")

# Example usage
input_directory = 'sign_lists'  # Replace with the path to your directory containing CSV files
output_file = 'sign_dict.csv'  # The path where the combined CSV will be saved
combine_csv_files(input_directory, output_file)
