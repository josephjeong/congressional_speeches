import pandas as pd

df = pd.read_csv("correct_output.txt", encoding="utf16")
df.drop_duplicates(inplace=True)
df.to_csv("output_no_dupe.txt", index=False)