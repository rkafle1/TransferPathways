#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 11:20:53 2023

@author: christalehr and YayaJiang
"""

import pandas as pd
import sys

file1 = sys.argv[1]  # admission
file2 = sys.argv[2]  # graduation
file3 = sys.argv[3]  # residual

# Read the CSV files and convert columns 'E', 'F', and 'G' to string data type to work with pd.NA
df1 = pd.read_csv(file1, header=0)
df2 = pd.read_csv(file2, header=0)
df2.iloc[:, 4] = df2.iloc[:, 4].astype('string')
df2.iloc[:, 5] = df2.iloc[:, 5].astype('string')
df2.iloc[:, 6] = df2.iloc[:, 6].astype('string')

starting_row_index = 6

def remove_matching_value(x, value_to_remove):
    if pd.notna(x):
        values_list = [item.strip() for item in str(x).split(';') if item.strip() != value_to_remove]
        return ';'.join(values_list)
    return x

# Keep the classes in graduation that are not in admission
for index, row in df1.iloc[starting_row_index:].iterrows():
    c_value = row[2]
    d_value = row[3]

    matched_rows_df2 = df2[(df2.iloc[:, 2] == c_value) & (df2.iloc[:, 3] == d_value)]

    for _, matched_row_df2 in matched_rows_df2.iterrows():
        target_row_index = int(matched_row_df2.name)
        value_in_column_a = df2.iat[target_row_index, 0]

        # Remove the data from all rows in df2 except row 'a'
        for col in df2.columns[1:]:
            df2.at[target_row_index, col] = pd.NA

        # Apply the remove_matching_value function to each cell in columns 'E', 'F', and 'G'
        df2.iloc[:, 4] = df2.iloc[:, 4].apply(remove_matching_value, value_to_remove=value_in_column_a)
        df2.iloc[:, 5] = df2.iloc[:, 5].apply(remove_matching_value, value_to_remove=value_in_column_a)
        df2.iloc[:, 6] = df2.iloc[:, 6].apply(remove_matching_value, value_to_remove=value_in_column_a)

# Save the updated DataFrame to a new CSV file without printing NaN or <NA> values
df2.to_csv(file3, index=False, na_rep='', float_format='%.0f')
