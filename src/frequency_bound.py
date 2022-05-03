from datetime import datetime
from typing import Optional
import pandas as pd
from nltk.stem import PorterStemmer

def frequency_bound(df : pd.DataFrame , word: Optional[str], start_year: Optional[datetime], end_year: Optional[datetime]) -> pd.DataFrame:
    print("processing frequency within constraints")
    if start_year: df = df.loc[(df["date"] >= start_year) & (df["date"] < end_year)]
    if word: df = df.loc[df["speech"].str.contains(r"\b{}\b".format(word), regex=True)]
    return df

def frequency_bound_stem(df : pd.DataFrame , word: Optional[str], start_year: Optional[datetime], end_year: Optional[datetime]) -> pd.DataFrame:
    print("processing frequency within constraints")
    stemmer = PorterStemmer()
    stemmed_word = stemmer.stem(word)
    if start_year: df = df.loc[(df["date"] >= start_year) & (df["date"] < end_year)]
    if word: df = df.loc[df["stemmed"].str.contains(r"\b{}\b".format(stemmed_word), regex=True)]
    return df