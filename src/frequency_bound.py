from datetime import datetime
from typing import Optional
import pandas as pd

def frequency_bound(df : pd.DataFrame , word: Optional[str], start_year: Optional[datetime], end_year: Optional[datetime]) -> pd.DataFrame:
    print("processing frequency within constraints")
    if start_year: df = df.loc[(df["date"] >= start_year) & (df["date"] < end_year)]
    if word: df = df.loc[df["speech"].str.contains(word)]
    return df

