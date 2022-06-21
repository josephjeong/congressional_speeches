import nltk
from nltk.stem import PorterStemmer
import concurrent.futures
from tqdm import tqdm

STEMMER = PorterStemmer()
def clean(raw):
    tokenized_text = nltk.word_tokenize(raw)
    stemmed = list(map(lambda w: STEMMER.stem(w), tokenized_text))
    return " ".join(stemmed)

def stem_words(df):
    # stem words
    print("Creating Stemmed Speeches")

    # read metadata for future reference
    with concurrent.futures.ProcessPoolExecutor() as executor:
        df["stemmed"] = list(tqdm(
                executor.map(clean, df["speech"], chunksize=1000),
                total = df.shape[0],
                desc= "Creating Stemmed Speeches"
            )
        )

    # df["stemmed"] = df["speech"].apply(clean)
    return df
