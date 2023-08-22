#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 15:21:08 2023

@author: christalehr
"""

import pandas as pd
import csv
import os
import sys

def filter_rows_by_blocking_column(df, threshold, source):
    if 11 in df.columns:
        df[11] = pd.to_numeric(df[11], errors='coerce')
        filtered_df = df[df[11] >= threshold].copy()
        filtered_df['Source'] = source
        return filtered_df
    else:
        df['Source'] = source
        return df

def find_matching_graduation_file(residual_file_path, graduation_folder_path):
    title_res = os.path.splitext(os.path.basename(residual_file_path))[0]
    grad_files = os.listdir(graduation_folder_path)
    matching_grad_file = next((file for file in grad_files if file.startswith(title_res) and file.endswith('.csv')), None)
    return matching_grad_file

def add_commas_to_13_fields(input_file):
    encodings = ['utf-8', 'ISO-8859-1', 'cp1252']  # List of encodings to try

    for encoding in encodings:
        try:
            with open(input_file, 'r', newline='', encoding=encoding) as infile:
                reader = csv.reader(infile)
                modified_data = []
                for row in reader:
                    num_fields = len(row)
                    if num_fields < 14:
                        row += [''] * (14 - num_fields)  # Add empty strings for missing fields
                    elif num_fields > 14:
                        row = row[:14]  # Truncate the row if it has more than 15 fields
                
                    modified_data.append(row)

            # Write the modified data back to the original file
            with open(input_file, 'w', newline='') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(modified_data)

            return input_file  # Return the modified file path

        except UnicodeDecodeError:
            continue

    raise Exception(f"Failed to read {input_file} with the provided encodings.")


def main(input_folder_path_res, input_folder_path_grad):
    output_folder = os.path.join(input_folder_path_res, 'output')
    os.makedirs(output_folder, exist_ok=True)
    residual_files = [file for file in os.listdir(input_folder_path_res) if file.endswith('.csv')]
    
    for residual_file in residual_files:
        input_file_path_res = os.path.join(input_folder_path_res, residual_file)
        matching_grad_file = find_matching_graduation_file(input_file_path_res, input_folder_path_grad)

        if matching_grad_file is not None:
            input_file_path_grad_matching = os.path.join(input_folder_path_grad, matching_grad_file)
            modified_res_path = add_commas_to_13_fields(input_file_path_res)
            modified_grad_path = add_commas_to_13_fields(input_file_path_grad_matching)

            try:
                df_grad = pd.read_csv(modified_grad_path, header=None)
                df_res = pd.read_csv(modified_res_path, header=None)

                numeric_columns = [0, 7, 10, 11, 12, 13]
                for col in numeric_columns:
                    if col < df_grad.shape[1]:
                        df_grad[col] = pd.to_numeric(df_grad[col], errors='coerce')
                    if col < df_res.shape[1]:
                        df_res[col] = pd.to_numeric(df_res[col], errors='coerce')

                complexity_total_grad = df_grad[10].sum()
                complexity_total_res = df_res[10].sum()

                df_filtered_grad = filter_rows_by_blocking_column(df_grad, 5.00, 'Graduation')
                df_filtered_res = filter_rows_by_blocking_column(df_res, 5.00, 'Residual')

                residual_complexity_difference = complexity_total_grad - complexity_total_res

                df_filtered_grad['Source'] = 'Graduation'
                df_filtered_res['Source'] = 'Residual'

                df_new = pd.concat([df_filtered_grad, df_filtered_res], ignore_index=True)

                output_file_path = os.path.join(output_folder, os.path.splitext(residual_file)[0] + '_output.csv')
                with open(output_file_path, 'w', newline='') as output_file:
                    csv_writer = csv.writer(output_file)

                    for _, row in df_res.head(5).iterrows():
                        data_row = row.fillna('').tolist()
                        csv_writer.writerow(data_row)

                    csv_writer.writerow(['Residual Complexity Total:', complexity_total_res, '', '', '', '', '', '', '', '', '', '', '', '', ''])
                    csv_writer.writerow(['Graduation Complexity Total:', complexity_total_grad, '', '', '', '', '', '', '', '', '', '', '', '', ''])
                    csv_writer.writerow(['Residual Difference:', residual_complexity_difference, '', '', '', '', '', '', '', '', '', '', '', '', '', ''])
                    csv_writer.writerow([])

                    header_row = ["Course ID", "Course Name", "Prefix", "Number", "Prerequisites", "Corequisites",
                                  "Strict-Corequisites", "Credit Hours", "Institution", "Canonical Name", "Complexity",
                                  "Blocking", "Delay", "Centrality", "Source"]
                    csv_writer.writerow(header_row)

                    for _, row in df_new.iterrows():
                        data_row = row.fillna('').tolist()
                        csv_writer.writerow(data_row)

            except Exception as e:
                print(f"An error occurred while processing {residual_file}: {e}")

    print(f"Filtered data and desired rows have been written to the output folder: {output_folder}.")

if __name__ == "__main__":
    input_folder_path_res = sys.argv[1]
    input_folder_path_grad = sys.argv[2]
    main(input_folder_path_res, input_folder_path_grad)






