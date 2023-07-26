#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 14:01:29 2023

@author: christalehr
"""

import pandas as pd
import csv
import os
import sys

input_folder = sys.argv[1]  # input folder containing CSV files
output_folder = sys.argv[2]  # output folder for CSV files

# Function to filter rows based on blocking values
def filter_rows_by_blocking_column(df, threshold):
    if 'Blocking' in df.columns:
        return df[df['Blocking'] >= threshold]
    else:
        return df

# Process each CSV file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)

        # Read the CSV file and convert numeric columns to appropriate data types
        lines = []
        with open(input_file_path, 'r', newline='') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                lines.append(row)

        # Find the index of the row that contains the header
        header_row_index = -1
        for i, row in enumerate(lines):
            if row[0].startswith("Course ID"):
                header_row_index = i
                break

        # Extract header and data separately
        header = [col.strip() for col in lines[header_row_index]]
        data = lines[header_row_index + 1:]


        # Create the DataFrame
        df = pd.DataFrame(data, columns=header)

        # Convert numeric columns to appropriate data types
        numeric_columns = ['Course ID', 'Credit Hours', 'Complexity', 'Blocking', 'Delay', 'Centrality']
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # Calculate the sum of blocking column
        complexity_total = df['Complexity'].sum()

        # Determine the threshold based on the complexity_total value
        if complexity_total >= 100:
            threshold = 12.00
        else:
            threshold = 8.00

        # Filter rows based on blocking column using the correct threshold
        df_filtered = filter_rows_by_blocking_column(df, threshold)

        # Create a new DataFrame with rows from 'df_filtered', the blocking_total value in a new row, and the rest of 'df'
        df_new = pd.concat([df_filtered, pd.DataFrame([complexity_total], columns=['Complexity Total'])])


        # Create a new DataFrame with the desired rows (Curriculum, Institution, Degree Type, System Type, CIP, and Courses)
        desired_rows = lines[:header_row_index]

        # Write the desired rows and filtered data to a new CSV file
        os.makedirs(output_folder, exist_ok=True)  # Create output folder if it doesn't exist
        with open(output_file_path, 'w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            for row in desired_rows:
                csv_writer.writerow(row)
            csv_writer.writerow([])  # Add an empty row
            df_new.to_csv(output_file, index=False)

        print(f"Filtered data and desired rows have been written to {output_file_path}.")




