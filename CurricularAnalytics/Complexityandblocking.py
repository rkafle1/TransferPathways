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

input_file_path_res = sys.argv[1]  # input residual CSV file
input_file_path_grad = sys.argv[2]  # input graduation CSV file

# Function to filter rows based on blocking values
def filter_rows_by_blocking_column(df, threshold, source):
    if 'Blocking' in df.columns:
        filtered_df = df[df['Blocking'] >= threshold].copy()  # Ensure a copy is made
        filtered_df['Source'] = source
        return filtered_df
    else:
        df['Source'] = source
        return df

# Read the grad CSV file and convert numeric columns to appropriate data types
lines_grad = []
with open(input_file_path_grad, 'r', newline='') as csv_file:
    csv_reader_grad = csv.reader(csv_file)
    for row in csv_reader_grad:
        lines_grad.append(row)

# Find the index of the row that contains the header
header_row_index_grad = -1
for i, row in enumerate(lines_grad):
    if row[0].startswith("Course ID"):
        header_row_index_grad = i
        break

# Extract header and data separately
header_grad = [col.strip() for col in lines_grad[header_row_index_grad]]
data_grad = lines_grad[header_row_index_grad + 1:]

# Create the DataFrame for graduation data
df_grad = pd.DataFrame(data_grad, columns=header_grad)

# Convert numeric columns to appropriate data types
numeric_columns_grad = ['Course ID', 'Credit Hours', 'Complexity', 'Blocking', 'Delay', 'Centrality']
for col in numeric_columns_grad:
    df_grad[col] = pd.to_numeric(df_grad[col], errors='coerce')

# Calculate the sum of blocking column for graduation data
complexity_total_grad = df_grad['Complexity'].sum()

# Determine the threshold based on the complexity_total value for graduation data
if complexity_total_grad >= 100:
    threshold_grad = 12.00
else:
    threshold_grad = 8.00

# Filter rows based on blocking column using the correct threshold for graduation data
df_filtered_grad = filter_rows_by_blocking_column(df_grad, threshold_grad, 'Graduation')


# Read the residual CSV file and convert numeric columns to appropriate data types
lines_res = []
with open(input_file_path_res, 'r', newline='') as csv_file:
    csv_reader_res = csv.reader(csv_file)
    for row in csv_reader_res:
        lines_res.append(row)

# Find the index of the row that contains the header
header_row_index_res = -1
for i, row in enumerate(lines_res):
    if row[0].startswith("Course ID"):
        header_row_index_res = i
        break

# Extract header and data separately
header_res = [col.strip() for col in lines_res[header_row_index_res]]
data_res = lines_res[header_row_index_res + 1:]

# Create the DataFrame for residual data
df_res = pd.DataFrame(data_res, columns=header_res)

# Convert numeric columns to appropriate data types
numeric_columns_res = ['Course ID', 'Credit Hours', 'Complexity', 'Blocking', 'Delay', 'Centrality']
for col in numeric_columns_res:
    df_res[col] = pd.to_numeric(df_res[col], errors='coerce')

# Calculate the sum of blocking column for residual data
complexity_total_res = df_res['Complexity'].sum()

# Determine the threshold based on the complexity_total value for residual data
if complexity_total_res >= 100:
    threshold_res = 12.00
else:
    threshold_res = 8.00

# Filter rows based on blocking column using the correct threshold for residual data
df_filtered_res = filter_rows_by_blocking_column(df_res, threshold_res, 'Residual')

# Calculate the difference between residual and graduation complexities
residual_complexity_difference = complexity_total_res - complexity_total_grad

# Create a new DataFrame with rows from both graduation and residual data, and label the source
df_new = pd.concat([df_filtered_grad, df_filtered_res])

# Write the filtered data to a new CSV file
output_file_path = os.path.splitext(input_file_path_res)[0] + '_output.csv'
with open(output_file_path, 'w', newline='') as output_file:
    csv_writer = csv.writer(output_file)
    

    # Write the header rows from graduation data
    for row in lines_res[:header_row_index_res]:
        csv_writer.writerow(row)

    csv_writer.writerow([])  # Add an empty row

    # Write the complexity and residual difference totals on separate lines with headers
    csv_writer.writerow(['Residual Complexity Total:', complexity_total_res])
    csv_writer.writerow(['Graduation Complexity Total:', complexity_total_grad])
    csv_writer.writerow(['Residual Difference:', residual_complexity_difference])

    # Write the remaining data from df_new with column headers
    df_new.to_csv(output_file, index=False)

print(f"Filtered data and desired rows have been written to {output_file_path}.")

















