import pandas as pd
from regex import D

df = pd.read_csv("speakermap.csv", delimiter="|")
df = df.groupby("year").size().to_frame('count')
df["percent"] = df["count"] / df["count"].sum() * 100
df["cumulative"] = df["percent"].cumsum().round(decimals=2)
df["percent"] = df["percent"].round(decimals=2)
# df["percent"] = df['num'] / df.groupby('year')['num'].transform('sum')
df.to_csv("stats.csv")