#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 08:50:42 2023

@author: christalehr
"""

import os
import re
from collections import Counter
import csv
import sys

folder_path = sys.argv[1]  # input folder containing CSV files

def get_all_words_from_file(file_path):
    encodings = ["utf-8", "latin-1"]  # List of encodings to try

    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                content = file.read().lower()
                words = re.findall(r'\b[a-zA-Z]+\b', content)  # Only match alphabetic words
                return words
        except UnicodeDecodeError:
            pass

    print(f"Unable to read file: {file_path}")
    return []

def get_all_words_from_folder(folder_path):
    all_words = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            file_words = get_all_words_from_file(file_path)
            all_words.extend(file_words)

    return all_words

def write_word_counts_to_csv(file_path, word_counts):
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['Word', 'Count'])
        for word, count in word_counts.items():
            csv_writer.writerow([word, count])

if __name__ == "__main__":

    all_words = get_all_words_from_folder(folder_path)
    word_counts = Counter(all_words)

    num_most_common = 10  # Change this number to display more or fewer words
    most_common_words = word_counts.most_common(num_most_common)

    print("\nMost Common Words:")
    for word, count in most_common_words:
        print(f"{word}: {count}")

    csv_output_file = "word_counts.csv"
    write_word_counts_to_csv(csv_output_file, word_counts)

    print(f"\nWord counts have been saved to '{csv_output_file}'.")

