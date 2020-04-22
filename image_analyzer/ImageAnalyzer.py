
import numpy as np
import pandas as pd
import os
import cv2
import time
from pathlib import Path

class ImageAnalyzer:

    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.image_df = None
    
    def __str__(self):
        csv_path_str = "\nCurrent CSV path = " + str(self.csv_path)
        image_df_str = "Image Dataframe (Preview): \n" + str(self.image_df.head())
        return csv_path_str + "\n" + image_df_str + "\n...\n"
    
    # CSV Reader
    def read_csv(self):
        try:
            # defined my own header names for standard use of header names throughout package
            temp_df = pd.read_csv(self.csv_path, names=['image1', 'image2',], header=0)
        except Exception as e:
            print("Error reading csv: " + str(e))
        else:
            # remove any rows with missing data
            # add empty rows for similar and elapsed for later use
            temp_df = temp_df.reindex(columns = ['image1', 'image2', 'similar', 'elapsed'], fill_value = "")
            self.image_df = temp_df

    # compare images
    # Uses DataFrame.apply() because it uses C extensions for Python in Cython, thereby making it faster
    #   than standard looping.
    def compare_images(self):
        self.image_df = self.image_df.apply(lambda row: self.lambda_row_replacer(row), axis=1)

    # Mean Squared Error - Used for comparison
    def mse(self, row):
        image1_path = Path(row['image1'])
        image2_path = Path(row['image2'])
        if not image1_path.exists() or not image2_path.exists():
            raise FileNotFoundError
        image1 = cv2.imread(row['image1'])
        image2 = cv2.imread(row['image2'])
        if image1.shape != image2.shape:
            image_sizes = "image1 = " + str(image1.shape) + "," + " image2 = " + str(image2.shape)
            raise Exception("Images must be the same size. " + image_sizes)
        err = np.sum((image1.astype("float") - image2.astype("float")) ** 2)
        err /= float(image1.shape[0] * image2.shape[1])
        return err
            
    # Row Replacer for use by the lambda function
    def lambda_row_replacer(self, row):
        try:
            start_time = time.time()
            row_mse = self.mse(row)
            stop_time = time.time()
            row['similar'] = row_mse
            row['elapsed'] = stop_time - start_time
        except FileNotFoundError as e:
            print("\nError - Following line contains invalid entry: ", "<", str(int(row.name) + 2), "\t", str(row['image1']), "\t", str(row['image2']), ">")
            if not Path(row['image1']).exists():
                print("\t The following file cannot be found: ", row['image1'])
            else:
                print("\t The following file cannot be found: ", row['image2'])
        except Exception as e:
            # The reason for the (+ 2) is due to the header row and 0 based indexing of the dataframe now aligning with the line numbers of the input CSV
            print("\nError - Following line contains invalid entry: ", "<", str(int(row.name) + 2), "\t", str(row['image1']), "\t", str(row['image2']), ">")
            print("\t", str(e), "\n")
        finally:
            return row
    
    # A function that normalizes the similarity score in order to allow easier comparison
    def similarity_normalizer(self):
        self.image_df["similar"] = ((self.image_df["similar"]-self.image_df["similar"].min())/(self.image_df["similar"].max()-self.image_df["similar"].min()))
        
    # Output CSV Creator
    def create_csv(self, filepath):
        try:
            self.image_df.to_csv(filepath, index=None, header=True)
        except Exception as e:
            print("Error writing to csv: ", str(e))
        else:
            print("CSV created at following location: ", filepath)
