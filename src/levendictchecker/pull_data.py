import os
import urllib.request

import pandas as pd

DICTIONARY_URL = "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt"
DICTIONARY_FILE = "data/english_dictionary.txt"
PARQUET_FILE = "data/english_dictionary.parquet"


def download_dictionary():
    """
    Download an English dictionary file in text format.
    """
    print("Downloading dictionary...")
    urllib.request.urlretrieve(DICTIONARY_URL, DICTIONARY_FILE)
    print("Dictionary downloaded.")


def convert_to_parquet():
    """
    Convert the English dictionary file to a Parquet file and remove the definition column.
    """
    print("Converting to Parquet...")
    # read the dictionary file
    with open(DICTIONARY_FILE, "r") as f:
        lines = f.readlines()
        words = [line.strip() for line in lines]
    # create a dataframe
    df = pd.DataFrame({"word": words})
    # make a length col 
    df["length"] = df["word"].str.len()
    # save to parquet
    df.to_parquet(PARQUET_FILE)
   


def main():
    os.makedirs("data", exist_ok=True)
    download_dictionary()
    convert_to_parquet()


if __name__ == "__main__":
    main()
