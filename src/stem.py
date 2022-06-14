import nltk
from nltk.stem import PorterStemmer

STEMMER = PorterStemmer()
def clean(raw):
    tokenized_text = nltk.word_tokenize(raw)
    stemmed = list(map(lambda w: STEMMER.stem(w), tokenized_text))
    return " ".join(stemmed)

def stem_words(df):
    # stem words
    print("Creating Stemmed Speeches")
    df["stemmed"] = df["speech"].apply(clean)
    return df
