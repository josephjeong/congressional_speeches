from re import L
import numpy as np
import pandas as pd

from src.corpus.process_hein_dataset import process_hein
from src.corpus.scrape import scrape_transcripts
from src.corpus.speakermap import map_speakers
from src.corpus.structure_text import structure_raw_text
from src.stem import stem_words

def generate_speech_id(df):
    return df

def create_corpus():
    # scrape_transcripts()
    structured_text = structure_raw_text()
    scrape_df = map_speakers(structured_text)
    # scrape_df = map_speakers(0)
    print("wow!")
    scrape_df['speech_id'] = scrape_df.index
    hein_df = process_hein()
    df = pd.concat([scrape_df, hein_df])
    # df = stem_words(df)
    df["district"].replace({".": 0}, inplace=True)
    df["district"].fillna(0, inplace=True)
    df["district"] = df["district"].astype(float)
    df = df.astype({
        "speech":"string",
        "date": "string",
        "speaker": "string",
        "party": "string",
        "district": "int",
        "f_name": "string",
        "l_name": "string",
        "chamber": "string",
        "gender": "string",
        "state": "string",
        "speech_id": "int",
        # "stem": "string"
    })
    # print(df)
    df.sample(n=100).to_csv("temp/corpus_sample.csv", index=False, sep="|")
    df.to_parquet("temp/corpus.gzip", index=False, compression="gzip", engine="pyarrow")
    return df

    import sys
    sys.exit(1)

def read_corpus():
    """
    speech_id speech date speaker party district f_name l_name chamber gender state stemmed
    """
    print("Loading Corpus")
    return pd.read_parquet("temp/corpus.gzip", engine="pyarrow")
