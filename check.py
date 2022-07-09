import pandas as pd

# df = pd.read_csv("temp/speeches.csv", sep="|")
# print(df.loc[117192])

df = pd.read_parquet("temp/corpus.gzip", engine="pyarrow")
print(df[(df["l_name"] == "TIPTON") & (df["speech_id"] < 150000)])