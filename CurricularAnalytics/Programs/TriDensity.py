#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug  8 10:32:39 2023

@author: christalehr
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import csv
import seaborn as sns

folder_path_1 = sys.argv[1] 
folder_path_2 = sys.argv[2]

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

    with open(file_path, 'r') as temp_f:
        lines = temp_f.readlines()
        label = lines[1].split(data_file_delimiter)[1]
        
        column_count = len(lines[0].split(data_file_delimiter))
        column_names = [i for i in range(0, column_count)]
        df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
            
    value1 = df.iloc[6, 1]
    value2 = df.iloc[5, 1]
    return float(value1), float(value2), label

def build_density_chart(data1, data2, data3, labels):
    plt.figure(figsize=(12, 6))
    sns.kdeplot(data1, fill=True, label='Graduation Complexity')
    sns.kdeplot(data2, fill=True, label='Actual Residual Complexity')
    sns.kdeplot(data3, fill=True, label='Ideal Residual Complexity')
    plt.title('Density Chart of Complexity According to Curricular Analytics')
    plt.xlabel('Complexity', fontsize=13)
    plt.ylabel('Density', fontsize = 13)
    
    # Increase y-axis label font size
    plt.gca().yaxis.set_tick_params(labelsize=16)
   
    plt.xticks(rotation=45, ha='right', fontsize =16)
    plt.tight_layout()
    
    # Increase the legend font size
    legend = plt.legend()
    legend.set_title(None)  # Remove the default legend title
    for text in legend.get_texts():
        text.set_fontsize(16)  # Set the desired font size for legend text
        
    plt.show()

def main(folder_path_1, folder_path_2):
    file_paths_1 = [os.path.join(folder_path_1, file_name) for file_name in os.listdir(folder_path_1) if file_name.endswith('.csv')]
    data1 = []
    data2 = []
    labels = []
    
    for file_path in file_paths_1:
        modified_path = add_commas_to_15_fields(file_path)
        value1, value2, label = get_data_from_file(modified_path)
        data1.append(value1)
        data2.append(value2)
        labels.append(label)
    
    file_paths_2 = [os.path.join(folder_path_2, file_name) for file_name in os.listdir(folder_path_2) if file_name.endswith('.csv')]
    data3 = []
    
    for file_path in file_paths_2:
        modified_path = add_commas_to_15_fields(file_path)
        _, value3, _ = get_data_from_file(modified_path)
        data3.append(value3)
    
    build_density_chart(data1, data2, data3, labels)

if __name__ == "__main__":
    main(folder_path_1, folder_path_2)
