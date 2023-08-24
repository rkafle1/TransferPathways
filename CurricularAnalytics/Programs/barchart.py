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

folder_path = sys.argv[1] #single folder input


#evens the files so there should be no missing (or extra) field errors
def add_commas_to_15_fields(input_file):
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)

        modified_data = []
        for row in reader:
            num_fields = len(row)
            if num_fields < 16:
                row += [''] * (16 - num_fields)  # Add empty strings for missing fields
            elif num_fields > 16:
                row = row[:16]  # Truncate the row if it has more than 15 fields
            
            modified_data.append(row)

    # Write the modified data back to the file
    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_data)

    return input_file  # Return the modified file path

def get_data_and_label_from_file(file_path):
    data_file_delimiter = ","

    # Loop the data lines
    with open(file_path, 'r') as temp_f:
        # Read the lines
        lines = temp_f.readlines()

        # Read the label from the first cell (row 0, column 0)
        label = lines[1].split(data_file_delimiter)[1]
        
        # Count the column count for the current line
        column_count = len(lines[0].split(data_file_delimiter))
        
        # Generate column names (will be 0, 1, 2, ..., column_count - 1)
        column_names = [i for i in range(0, column_count)]

        # Read csv
        df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
            
    value = df.iloc[7, 1]  # Indexing starts from 0, so row 8 would be at index 7, column 2 would be at index 1. This is where you'd change location if needed
    return float(value), label

def build_bar_chart(data, labels):
    # Create a bar chart using matplotlib
    plt.figure(figsize=(12, 6))
    x_pos = range(len(labels))  # Create positions for the bars on the x-axis
    plt.bar(x_pos, data)
    plt.title('Actual Residual Difference')
    plt.xlabel('Universities')
    plt.ylabel('Complexity')
    plt.xticks(x_pos, labels, rotation=45, ha='right')  # Set the x-axis positions and labels
    plt.tight_layout()  # Ensure labels fit within the figure area
    plt.show()

def main(folder_path):
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
    data = []
    labels = []
    
    for file_path in file_paths:
        modified_path = add_commas_to_15_fields(file_path)
        value, label = get_data_and_label_from_file(modified_path)
        data.append(value)
        labels.append(label)
    
    # Sort the data and labels from highest to lowest values
    data, labels = zip(*sorted(zip(data, labels), reverse=True))
    
    build_bar_chart(data, labels)

if __name__ == "__main__":
    main(folder_path)







