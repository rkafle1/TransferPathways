#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:34:15 2023

@author: christalehr
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv

#program creates a dual bar chart from a folder of input. Designed with complexity files in mind

folder_path = sys.argv[1]

#evens fields
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
            
    value1 = df.iloc[6, 1]  # Indexing starts from 0, so row 8 would be at index 7, column 2 would be at index 1.
                            # change this if you want to change where graduation complexity comes from
    value2 = df.iloc[5, 1]  # Assuming the second value is in column 2
                            # change this if you want to change where residual complexity comes from
    return float(value1), float(value2), label

def build_bar_chart(data1, data2, labels):
    # Create a bar chart using matplotlib
    plt.figure(figsize=(12, 6))
    x_pos = range(len(labels))  # Create positions for the bars on the x-axis
    
    # Set the width of each bar to make the bars overlap
    bar_width = 0.4

    plt.bar(x_pos, data1, width=bar_width, align='center', label='Graduation Complexity')
    plt.bar([pos + bar_width for pos in x_pos], data2, width=bar_width, align='center', label='Residual Complexity')

    plt.title('Graduation Complexity and Residual Complexity According to Curricular Analytics')
    plt.xlabel('Universities')
    plt.ylabel('Complexity')
    plt.xticks([pos + bar_width / 2 for pos in x_pos], labels, rotation=45, ha='right')  # Set the x-axis positions and labels
    plt.tight_layout()  # Ensure labels fit within the figure area
    plt.legend()  # Add legend to differentiate between Value 1 and Value 2
    plt.show()

def main(folder_path):
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
    data1 = []
    data2 = []
    labels = []
    
    for file_path in file_paths:
        modified_path = add_commas_to_15_fields(file_path)
        value1, value2, label = get_data_and_label_from_file(modified_path)
        data1.append(value1)
        data2.append(value2)
        labels.append(label)
    
    # Sort the data and labels from highest to lowest values
    data1, data2, labels = zip(*sorted(zip(data1, data2, labels), reverse=True))
    
    build_bar_chart(data1, data2, labels)

if __name__ == "__main__":
    main(folder_path)

