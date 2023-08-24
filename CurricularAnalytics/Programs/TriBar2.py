#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 13 20:08:38 2023

@author: christalehr
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import csv
import sys

def add_commas_to_15_fields(input_file):
    with open(input_file, 'r', newline='') as infile:
        reader = csv.reader(infile)

        modified_data = []
        for row in reader:
            num_fields = len(row)
            if num_fields < 15:
                row += [''] * (15 - num_fields)
            elif num_fields > 15:
                row = row[:15]
            
            modified_data.append(row)

    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(modified_data)

    return input_file

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

def get_data_from_file_2(file_path):
    data_file_delimiter = ","

    with open(file_path, 'r') as temp_f:
        lines = temp_f.readlines()
        column_count = len(lines[0].split(data_file_delimiter))
        column_names = [i for i in range(0, column_count)]
        df = pd.read_csv(file_path, header=None, delimiter=data_file_delimiter, names=column_names)
            
    value3 = df.iloc[5, 1]
    return float(value3)

def build_bar_chart(data1, data2, data3, labels):
    plt.figure(figsize=(12, 6))
    x_pos = range(len(labels))
    bar_width = 0.2
    group_offset = 0.3
    
    plt.bar([pos + group_offset for pos in x_pos], data1, width=bar_width, align='center', label='Graduation')
    plt.bar([pos + bar_width + group_offset for pos in x_pos], data2, width=bar_width, align='center', label='Existing Residual')
    plt.bar([pos + bar_width * 2 + group_offset for pos in x_pos], data3, width=bar_width, align='center', label='Ideal Residual')

    plt.title('Grad, Existing Residual, and Ideal Residual Complexity Comparison According to Curricular Analytics', fontsize=15)
    plt.xlabel('Universities', fontsize=16)
    plt.ylabel('Complexity', fontsize=16)

    plt.xticks([pos + group_offset + bar_width for pos in x_pos], labels, rotation=45, ha='right')

    for i, label in enumerate(labels):
        if label.startswith('UC'):
            plt.gca().get_xticklabels()[i].set_color('green')
            plt.gca().get_xticklabels()[i].set_fontsize(13)
        else:
            plt.gca().get_xticklabels()[i].set_color('black')
            plt.gca().get_xticklabels()[i].set_fontsize(13)

    plt.gca().yaxis.set_tick_params(labelsize=16)

    plt.tick_params(axis='x', which='both', bottom=False)
    plt.tight_layout()
    
    legend = plt.legend()
    legend.set_title(None)
    for text in legend.get_texts():
        text.set_fontsize(16)

    plt.show()

def main(folder_path, folder_path_2):
    file_paths = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path) if file_name.endswith('.csv')]
    data1 = []
    data2 = []
    labels = []
    
    file_paths2 = [os.path.join(folder_path_2, file_name) for file_name in os.listdir(folder_path_2) if file_name.endswith('.csv')]
    data3 = []
        
    for file_path in file_paths:
        modified_path = add_commas_to_15_fields(file_path)
        value1, value2, label = get_data_and_label_from_file(modified_path)
        data1.append(value1)
        data2.append(value2)
        labels.append(label)
        
    for file_path in file_paths2:
        modified_path = add_commas_to_15_fields(file_path)
        value3 = get_data_from_file_2(modified_path)
        data3.append(value3)
        
    combined_data = list(zip(data1, data2, data3, labels))
    sorted_combined_data = sorted(combined_data, key=lambda x: x[0])
    sorted_data1, sorted_data2, sorted_data3, sorted_labels = zip(*sorted_combined_data)

    build_bar_chart(sorted_data1, sorted_data2, sorted_data3, sorted_labels)

if __name__ == "__main__":
    folder_path = sys.argv[1]
    folder_path_2 = sys.argv[2]
    main(folder_path, folder_path_2)
