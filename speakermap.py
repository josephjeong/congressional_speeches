from doctest import Example
import pandas as pd

speakers = pd.read_csv("data/HSall_members.csv")
speakers = speakers.dropna(subset=["died", "born"])
speakers = speakers[["congress", "chamber", "state_abbrev", "bioname", "party_code", "born", "died"]]
speakers["born"] = speakers["born"].astype(int)
speakers["died"] = speakers["died"].astype(int)
speakers["congress"] = speakers["congress"].astype(int)
speakers = speakers[(speakers["congress"] >= 23) & (speakers["congress"] <= 45)]
speakers = speakers [speakers["chamber"] != "President"]

# parties sourced from: https://voteview.com/articles/data_help_parties
parties = pd.read_csv("data/HSall_parties.csv")[["party_code", "party_name"]]
speakers = pd.merge(speakers, parties, on="party_code")

speakers[["lastname", "firstname"]] = speakers["bioname"].str.split(",", n=1, expand=True)
speakers.loc[speakers["chamber"] == "House", "house"] = "HOUSE OF REPRESENTATIVES"
speakers.loc[speakers["chamber"] == "Senate", "house"] = "SENATE"
speakers = speakers[["lastname", "state_abbrev", "house", "party_name"]]
# s = df["bioname"].str.split(",", n=1, expand=True)
# print(s)

print(speakers)

df = pd.read_csv("speeches.csv", delimiter="|")
df["lastname"] = df["clean_names"].str.extract(r"\b(\w*?)$")
# df.drop(columns=["clean_names", "speeches"], inplace=True)
print(df)

df['lastname'] = df['lastname'].fillna(0)
df['house'] = df['house'].fillna(0)
df= pd.merge(df, speakers, on=["lastname", "house"], how="left")
print(df)

"""
1196714
1,412,423,881
"""