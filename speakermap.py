import pandas as pd
import numpy as np

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

# print(speakers)

df = pd.read_csv("data/speeches.csv", delimiter="|")
df["lastname"] = df["clean_names"].str.extract(r"\b(\w*?)$")
# df.drop(columns=["clean_names", "speeches"], inplace=True)
# print(df)

df['lastname'] = df['lastname'].fillna(0)
df['house'] = df['house'].fillna(0)

# df.to_csv("")

# n = 50000
# list_df = [df[i:i+n] for i in range(0,df.shape[0],n)]
# print(len(list_df))

# result_dfs = []
# for i, small_df in enumerate(list_df):
#     result_dfs.append(pd.merge(small_df, speakers, on=["lastname", "house"], how="left"))
#     print("another one", i)
# df = pd.concat(result_dfs)


# # df= pd.merge(df, speakers, on=["lastname", "house"], how="left")
# df.to_csv("speakermap.csv", sep="|", index=False, header=True)
# print(df)

speakers.to_csv("yourdata.csv", sep="|")
df.to_csv("yourdata2.csv", sep="|")

del(speakers)
del(df)

df1 = pd.read_csv("yourdata.csv", delimiter="|")
df2 = pd.read_csv("yourdata2.csv", delimiter="|")

# creating a empty bucket to save result
df_result = pd.DataFrame(columns=(df1.columns.append(df2.columns)).unique())
df_result.to_csv("df3.csv",index_label=False, sep="|")

# save data which only appear in df1 # sorry I was doing left join here. no need to run below two line.
# df_result = df1[df1.Colname1.isin(df2.Colname2)!=True]
# df_result.to_csv("df3.csv",index_label=False, mode="a")

# deleting df2 to save memory
del(df2)

def preprocess(x):
    print("preprocessing!")
    df2=pd.merge(df1,x, on=["lastname", "house"], how="left")
    df2.to_csv("df3.csv", mode="a", header=False, index=False, sep="|")

reader = pd.read_csv("yourdata2.csv", chunksize=10000, delimiter="|") # chunksize depends with you colsize

[preprocess(r) for r in reader]

"""
1196714
1,412,423,881
"""