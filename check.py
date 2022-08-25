import pandas as pd

df = pd.read_csv("temp/speakermap.csv", sep="|")
print(df.shape)

df = pd.read_csv("temp/speakermap_duplicates.csv", sep="|")
print(df.shape)
