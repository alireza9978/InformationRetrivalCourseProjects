from pathlib import Path

import pandas as pd
import swifter

from TextCleaning import *

a = swifter.config


def read_file():
    dataset_path = Path("../../data/HW1/plot_summaries.txt")
    with open(dataset_path) as f:
        lines = f.readlines()

    dataset = pd.DataFrame(lines, columns=["raw_data"])
    dataset["raw_data"] = dataset["raw_data"].swifter.apply(lambda row: row.split("\t"))
    dataset = pd.DataFrame(dataset['raw_data'].to_list(), columns=['id', 'plot'])
    return dataset


def clean_text(temp_text: str):
    # todo remove "{{plot}}" from start of texts
    temp_text = remove_punctuation(temp_text)
    temp_text = clean_url(temp_text)
    temp_text = make_lower(temp_text)
    temp_text_tokens = tokenize(temp_text)
    temp_text_tokens = remove_short_tokens(temp_text_tokens)
    temp_text_tokens = remove_stopwords(temp_text_tokens)
    temp_text_tokens = stemming(temp_text_tokens)
    temp_text_tokens = lemmatize(temp_text_tokens)
    return temp_text_tokens


if __name__ == '__main__':
    df = read_file()
    print("file loaded")
    # df["tokens"] = df["plot"].swifter.apply(clean_text)
    df["tokens"] = df["plot"].apply(clean_text)
    print(df)
