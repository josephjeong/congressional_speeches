import nltk
import pandas as pd
from nltk.stem import PorterStemmer
import concurrent.futures
from tqdm import tqdm

STEMMER = PorterStemmer()
def clean(raw):
    try:
        tokenized_text = nltk.word_tokenize(raw)
        stemmed = list(map(lambda w: STEMMER.stem(w), tokenized_text))
        return " ".join(stemmed)
    except:
        # some are 1 integers
        # print(raw)
        return ""

def stem_words(df : pd.DataFrame):
    # stem words
    with concurrent.futures.ProcessPoolExecutor() as executor:
        stemmed = list(tqdm(
                executor.map(clean, df["speech"], chunksize=1000),
                total = df.shape[0],
                desc= "Creating Stemmed Speeches"
            )
        )
        df["stemmed"] = stemmed
    return df
