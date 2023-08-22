#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 22 09:42:48 2023

@author: christalehr
"""

# Import necessary libraries/modules
import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys

# Function to ensure that each row in the CSV file has exactly 15 fields (columns)
def add_commas_to_15_fields(input_file):
    # Open the input file for reading
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)
        modified_data = []

        # Loop through each row in the CSV file
        for row in reader:
            num_fields = len(row)
            # If the row has less than 15 fields, add empty fields to make it 15
            if num_fields < 15:
                row += [''] * (15 - num_fields)
            # If the row has more than 15 fields, truncate it to 15 fields
            elif num_fields > 15:
                row = row[:15]
            modified_data.append(row)

    # Write the modified data back to the same input file
    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_data)

    return input_file

# Function to extract specific data and a label from a file
def get_data_and_label_from_file(file_path):
    data_file_delimiter = ","
    with open(file_path, 'r') as temp_f:
        lines = temp_f.readlines()
        label = lines[1].split(data_file_delimiter)[1]
        column_count = len(lines[0].split(data_file_delimiter))
        column_names = [i for i in range(0, column_count)]
        df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
        
    value1 = df.iloc[6, 1]
    value2 = df.iloc[5, 1]
    return float(value1), float(value2), label

# Function to extract specific data from another file
def get_data_from_file_2(file_path):
    data_file_delimiter = ","
    with open(file_path, 'r') as temp_f:
        lines = temp_f.readlines()
        column_count = len(lines[0].split(data_file_delimiter))
        column_names = [i for i in range(0, column_count)]
        df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
        
    value3 = df.iloc[5, 1]
    return float(value3)

# Function to build and display a bar chart
def build_bar_chart(data1, data2, data3, labels):
    plt.figure(figsize=(12, 6))
    x_pos = range(len(labels))
    bar_width = 0.2
    group_offset = 0.3
    
    # Create three sets of bars with different data and labels
    plt.bar([pos + group_offset for pos in x_pos], data1, width=bar_width, align='center', label='Graduation')
    plt.bar([pos + bar_width + group_offset for pos in x_pos], data2, width=bar_width, align='center', label='Existing Residual')
    plt.bar([pos + bar_width * 2 + group_offset for pos in x_pos], data3, width=bar_width, align='center', label='Ideal Residual')

    # Set chart title and axis labels
    plt.title('Grad, Existing Residual, and Ideal Residual Complexity Comparison According to Curricular Analytics', fontsize=15)
    plt.xlabel('Universities', fontsize=16)
    plt.ylabel('Complexity', fontsize=16)

    # Set x-axis ticks and labels
    plt.xticks([pos + group_offset + bar_width for pos in x_pos], labels, rotation=45, ha='right')

    # Customize tick labels for specific conditions
    for i, label in enumerate(labels):
        if label.startswith('UC'):
            plt.gca().get_xticklabels()[i].set_color('green')
            plt.gca().get_xticklabels()[i].set_fontsize(13)
        else:
            plt.gca().get_xticklabels()[i].set_color('black')
            plt.gca().get_xticklabels()[i].set_fontsize(13)

    # Set tick label size for y-axis
    plt.gca().yaxis.set_tick_params(labelsize=16)

    # Remove bottom ticks on x-axis
    plt.tick_params(axis='x', which='both', bottom=False)
    plt.tight_layout()
    
    # Display the legend with custom font size
    legend = plt.legend()
    legend.set_title(None)
    for text in legend.get_texts():
        text.set_fontsize(16)

    # Show the chart
    plt.show()

# Main function
def main(folder_path, folder_path_2):
    # Get a list of file paths in the specified folders that end with '.csv'
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
    data1 = []
    data2 = []
    labels = []
    
    file_paths2 = [os.path.join(folder_path_2, file_name) for file_name in os.listdir(folder_path_2) if file_name.endswith('.csv')]
    data3 = []
        
    # Process the first set of files
    for file_path in file_paths:
        # Add commas to ensure each row has 15 fields
        modified_path = add_commas_to_15_fields(file_path)
        # Extract data and label from the modified file
        value1, value2, label = get_data_and_label_from_file(modified_path)
        data1.append(value1)
        data2.append(value2)
        labels.append(label)
    
    # Process the second set of files
    for file_path in file_paths2:
        # Add commas to ensure each row has 15 fields
        modified_path = add_commas_to_15_fields(file_path)
        # Extract data from the modified file
        value3 = get_data_from_file_2(modified_path)
        data3.append(value3)
    
    # Combine the data from both sets
    combined_data = list(zip(data1, data2, data3, labels))
    # Sort the combined data based on the first value (data1)
    sorted_combined_data = sorted(combined_data, key=lambda x: x[0])
    sorted_data1, sorted_data2, sorted_data3, sorted_labels = zip(*sorted_combined_data)

    # Generate and display the bar chart
    build_bar_chart(sorted_data1, sorted_data2, sorted_data3, sorted_labels)

# Entry point of the script
if __name__ == "__main__":
    # Get folder paths from command line arguments
    folder_path = sys.argv[1]
    folder_path_2 = sys.argv[2]
    # Call the main function with the specified folder paths
    main(folder_path, folder_path_2)
