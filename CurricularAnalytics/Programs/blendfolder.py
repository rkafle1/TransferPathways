#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 10:02:48 2023

@author: christalehr
"""

import pandas as pd
import os
import sys
import csv

folder_admission = sys.argv[1]  # Folder containing admission CSV files
folder_graduation = sys.argv[2]  # Folder containing graduation CSV files
output_folder = sys.argv[3]  # Folder to store the resulting residual files

def add_commas_to_15_fields(input_file):
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252']  # List of encodings to try

    for encoding in encodings:
        try:
            with open(input_file, 'r', newline='', encoding=encoding) as infile:
                reader = csv.reader(infile)

                modified_data = []
                for row in reader:
                    num_fields = len(row)
                    if num_fields < 15:
                        row += [''] * (15 - num_fields)  # Add empty strings for missing fields
                    elif num_fields > 15:
                        row = row[:15]  # Truncate the row if it has more than 15 fields
                
                    modified_data.append(row)

            # Write the modified data to a temporary file
            temp_file = input_file + '.tmp'
            with open(temp_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(modified_data)

            return temp_file  # Return the modified file path without the .tmp extension

        except UnicodeDecodeError:
            continue

    raise Exception(f"Failed to read {input_file} with the provided encodings.")

def remove_matching_value(x, value_to_remove):
    if pd.notna(x):
        values_list = [item.strip() for item in str(x).split(';') if item.strip() != value_to_remove]
        return ';'.join(values_list)
    return x

def process_matching_files(file_admission, file_graduation):
    # Read the CSV files and convert columns 'E', 'F', and 'G' to string data type to work with pd.NA
    df_admission = pd.read_csv(file_admission, header=0)
    df_graduation = pd.read_csv(file_graduation, header=0)
    df_graduation.iloc[:, 4] = df_graduation.iloc[:, 4].astype('string')
    df_graduation.iloc[:, 5] = df_graduation.iloc[:, 5].astype('string')
    df_graduation.iloc[:, 6] = df_graduation.iloc[:, 6].astype('string')

    starting_row_index = 6

    # Keep the classes in graduation that are not in admission
    for index, row in df_admission.iloc[starting_row_index:].iterrows():
        c_value = row[2]
        d_value = row[3]

        matched_rows_df_graduation = df_graduation[(df_graduation.iloc[:, 2] == c_value) & (df_graduation.iloc[:, 3] == d_value)]

        for _, matched_row_df_graduation in matched_rows_df_graduation.iterrows():
            target_row_index = int(matched_row_df_graduation.name)
            value_in_column_a = df_graduation.iat[target_row_index, 0]

            # Remove the data from all rows in df_graduation except row 'a'
            for col in df_graduation.columns[1:]:
                df_graduation.at[target_row_index, col] = pd.NA

            # Apply the remove_matching_value function to each cell in columns 'E', 'F', and 'G'
            df_graduation.iloc[:, 4] = df_graduation.iloc[:, 4].apply(remove_matching_value, value_to_remove=value_in_column_a)
            df_graduation.iloc[:, 5] = df_graduation.iloc[:, 5].apply(remove_matching_value, value_to_remove=value_in_column_a)
            df_graduation.iloc[:, 6] = df_graduation.iloc[:, 6].apply(remove_matching_value, value_to_remove=value_in_column_a)

    # Save the updated DataFrame to a new CSV file without printing NaN or <NA> values
    base_file_name = os.path.splitext(os.path.basename(file_graduation))[0]
    output_file_path = os.path.join(output_folder, base_file_name)
    df_graduation.to_csv(output_file_path, index=False, na_rep='', float_format='%.0f')

    print(f"Processed data from {file_admission} and {file_graduation} has been written to {output_file_path}.")


# Find matching file names and process them together
for file_admission in os.listdir(folder_admission):
    base_name = os.path.splitext(file_admission)[0]
    file_graduation = os.path.join(folder_graduation, base_name + '.csv')

    if os.path.isfile(file_graduation):
        modified_path_admission = add_commas_to_15_fields(os.path.join(folder_admission, file_admission))
        modified_path_graduation = add_commas_to_15_fields(file_graduation)

        # Process matching files if both admission and graduation files are modified successfully
        if os.path.isfile(modified_path_admission) and os.path.isfile(modified_path_graduation):
            process_matching_files(modified_path_admission, modified_path_graduation)

            # Clean up temporary files (optional)
            os.remove(modified_path_admission)
            os.remove(modified_path_graduation)
        else:
            print(f"Skipping {base_name}.csv pair because one or both files could not be processed.")
    else:
        print(f"Skipping {base_name}.csv pair because the corresponding graduation file was not found.")


