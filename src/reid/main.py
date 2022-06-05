from encoder import OsNetEncoder
from utils import uncompress_string_image
import pandas as pd
import csv
import os
import cv2

"""
# Load pandas dataframe
df = pd.read_csv("./dataset/input_dataset.csv")

# Uncompress cropped image
df["uncompressed_feature_vector"] = df.apply(lambda x: uncompress_string_image(
    compresed_cropped_image=x["feature_vector"]),
    axis=1)
"""

# Declare an encoder object
encoder = OsNetEncoder(
    input_width=704,
    input_height=480,
    weight_filepath="../../models/osnet_ibn_ms_d_c.pth.tar",
    batch_size=32,
    num_classes=2022,
    patch_height=256,
    patch_width=128,
    norm_mean=[0.485, 0.456, 0.406],
    norm_std=[0.229, 0.224, 0.225],
    GPU=True)
im_lst = []
test_folder = "../../test"
for f in os.listdir(test_folder):
    fp = os.path.join(test_folder, f)
    img = cv2.imread(fp)
    print(fp)
    im_lst.append(img)    
encoder.get_features(im_lst)
exit()
# Add the new column
df["feature_vector"] = encoder.get_features(list(df["uncompressed_feature_vector"]))

# Clean the dataframe
df.drop("uncompressed_feature_vector", axis=1, inplace=True)

# Write the dataframe to a .csv
df.to_csv("./output_files/output_dataset.csv",
          index=False,
          quoting=csv.QUOTE_NONNUMERIC
          )
