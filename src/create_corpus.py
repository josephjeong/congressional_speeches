import pandas as pd

from src.corpus.process_hein_dataset import process_hein
from src.corpus.scrape import scrape_transcripts
from src.corpus.speakermap import map_speakers
from src.corpus.structure_text import structure_raw_text

def generate_speech_id(df):
    return df

def create_corpus():
    scrape_transcripts()
    structured_text = structure_raw_text()
    scrape_df = map_speakers(structured_text)
    print("wow!")
    scrape_df['speech_id'] = scrape_df.index
    hein_df = process_hein()
    df = pd.concat([scrape_df, hein_df])
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
