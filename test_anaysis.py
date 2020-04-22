#!/usr/bin/env python3

import sys
import time
import os
import pandas as pd
from pathlib import Path

import image_analyzer
from analysis import analysis

def test_main_csv():
    testing_input_csv_path = Path().cwd() / 'testing' / 'testing_data.csv'
    testing_output_csv_path = Path().cwd() / 'testing' / 'testing_data_output.csv'
    testing_output_template_csv_path = Path().cwd() / 'testing' / 'testing_data_complete.csv'
    analysis(testing_input_csv_path, testing_output_csv_path)
    fields = ['image1', 'image2', 'similar']
    analysis_output_df = pd.read_csv(testing_output_csv_path, names=fields, usecols=fields, header=0)
    analysis_template_df = pd.read_csv(testing_output_template_csv_path, names=fields, usecols=fields, header=0)
    
    # Run the analysis program
    assert analysis_output_df.equals(analysis_template_df), "Output csv: <" + str(testing_output_csv_path) + "> does not match template csv: <" + str(testing_output_template_csv_path) + ">"

if __name__ == "__main__":
    test_main_csv()
    print("--- Everything passed ---")