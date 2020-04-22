#!/usr/bin/env python3

import sys
import time
import os
from pathlib import Path
import argparse

import image_analyzer

def analysis(filename, output_csv_filepath):

    print("Start of ImageAnalysis program...")

    # Initialize the class
    analyzer = image_analyzer.ImageAnalyzer(filename)

    # Read the csv
    analyzer.read_csv()

    # Run the comparison
    start = time.time()
    analyzer.compare_images()
    stop = time.time()
    print("Total execution time of comparison operation = " + str(stop-start) + " sec.")

    # Normalize the similarity column
    # analyzer.similarity_normalizer()

    # Print dataset
    print(analyzer)

    # Write the csv
    analyzer.create_csv(output_csv_filepath)

# analysis()
if __name__ == "__main__":
    # Command line argument
    parser = argparse.ArgumentParser()
    parser.add_argument("input_csv_path", help="The path to the csv containging the image dataset.", type=str)
    parser.add_argument('-o', '--output', action='store_true', help="The filename for the output csv.")
    args = parser.parse_args()
    
    # Argument check - for CSV file path
    if not args.input_csv_path:
        print("Error: Please specify the path to the dataset csv.")
        sys.exit(1)
    
    input_file_path = Path(args.input_csv_path)

    if not args.output:
        new_output_filename = input_file_path.stem + "_output.csv"
        output_file_path = input_file_path.parents[0] / new_output_filename
    else:
        output_file_path = args.output
    


    # Path Validity Check    
    if not input_file_path.exists():
        print("Error: CSV file not found, please provide valid path to csv.")
        sys.exit(1)
    
    analysis(input_file_path, output_file_path)