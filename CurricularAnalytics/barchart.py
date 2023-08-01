#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 14:43:23 2023

@author: christalehr
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv

folder_path = sys.argv[1]

def add_commas_to_15_fields(input_file):

    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)

        modified_data = []
        for row in reader:
            num_fields = len(row)
            if num_fields < 15:
                row += [''] * (15 - num_fields)  # Add empty strings for missing fields
            elif num_fields > 15:
                row = row[:15]  # Truncate the row if it has more than 15 fields
            
            modified_data.append(row)

    # Write the modified data back to the file
    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_data)

    return input_file  # Return the modified file path

def get_data_from_file(file_path):
    data_file_delimiter = ","

    # The max column count a line in the file could have
    largest_column_count = 0

    # Loop the data lines
    with open(file_path, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        for l in lines:
            # Count the column count for the current line
            column_count = len(l.split(data_file_delimiter)) + 1
        
            # Set the new most column count
            largest_column_count = column_count if largest_column_count < column_count else largest_column_count

            # Generate column names (will be 0, 1, 2, ..., largest_column_count - 1)
            column_names = [i for i in range(0, largest_column_count)]

            # Read csv
            df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
            
    value = df.iloc[7, 1]  # Indexing starts from 0, so row 8 would be at index 7, column 2 would be at index 1
    return float(value)  # Convert the value to a float (if it's numeric)

def build_bar_chart(data, labels):
    # Create a bar chart using matplotlib
    plt.figure(figsize=(8, 6))
    plt.bar(labels, data)
    plt.title('Data Distribution')
    plt.xlabel('Files')
    plt.ylabel('Values')
    plt.show()

def main(folder_path):
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
    data = []
    labels = []
    
    for file_path in file_paths:
        modified_path = add_commas_to_15_fields(file_path)
        value = get_data_from_file(modified_path)
        data.append(value)
        labels.append(os.path.basename(modified_path))
    
    build_bar_chart(data, labels)

if __name__ == "__main__":
    main(folder_path)
