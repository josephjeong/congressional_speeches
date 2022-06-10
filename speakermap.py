import pandas as pd
from datetime import datetime

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
speakers = speakers[["lastname", "bioname", "state_abbrev", "house", "party_name"]]
# s = df["bioname"].str.split(",", n=1, expand=True)
# print(s)

# print(speakers)

session_dates = pd.read_csv("data/congress_dates.csv")
session_dates["Begin Date"] = pd.to_datetime(session_dates["Begin Date"], format="%b %d, %Y", errors="raise")
session_dates["Adjourn Date"] = pd.to_datetime(session_dates["Adjourn Date"], format="%b %d, %Y", errors="raise")

# dataset_begin = datetime(1833)
# dataset_end = datetime(1875)
# session_dates = session_dates[session_dates["Begin Date"]]
# print(session_dates)

df = pd.read_csv("data/speeches.csv", delimiter="|")
df["lastname"] = df["clean_names"].str.extract(r"\b(\w*?)$")
df.drop(columns=["clean_names"], inplace=True)

def date_conversion(row):
    # this function needs to catch weird edge cases from bad OCR
    month = row[0]
    day = row[1]
    year = row[2]
    date = f"{row[0]} {row[1]} {row[2]}"
    if (date == "February 28 18335"): year = 1835
    elif (date == "December 21 1"): year = 1835
    elif (date == "February 1 183"): year = 1836
    elif (date == "February 2 1826"): year = 1836
    elif (date == "February 13 136"): year = 1836
    elif (date == "April 12 136"): year = 1836
    elif (date == "June 15 1"): year = 1836
    elif (date == "May 8 180"): year = 1840
    elif (date == "July 10 184"): year = 1840
    elif (date == "February 15 164"): year = 1842
    elif (date == "June 2 1"): year = 1846
    elif (date == "July 3 185"): year = 1852
    elif (date == "February 4 185"): year = 1858
    elif (date == "January 30 182"): year = 1862
    elif (date == "February 11 186"): year = 1862
    elif (date == "January 80 1866"): day = 30
    elif (date == "January 27 18"): year = 1868
    elif (date == "June 27 1"): year = 1868
    elif (date == "January 80 1871"): day = 30
    elif (date == "April 1 2011"): year = 1836
    elif (date == "February 27 2011"): year = 1838
    elif (date == "July 9 2011"): year = 1841
    elif (date == "December 29 2011"): year = 1848
    elif (date == "January 11 2011"): year = 1853
    elif (date == "December 17 2011"): year = 1856
    return datetime.strptime(f"{month} {day} {year}", '%B %d %Y')

# conversion to datetime for speeches
df["day"] = df["day"].fillna(1).astype(int) # generally this seems to work
df["year"] = df["year"].fillna(2011).astype(int) # an outlandish year
df["datetime"] = df[['month','day','year']].apply(date_conversion, axis=1)

df['lastname'] = df['lastname'].fillna(0)
df['house'] = df['house'].fillna(0)

print(df.shape, speakers.shape)
df.drop_duplicates(inplace=True)
speakers.drop_duplicates(inplace=True)
print(df.shape, speakers.shape)

df= pd.merge(df, speakers, on=["lastname", "house"], how="left")
print(df)
# df.to_csv("speakermap.csv", sep="|", index=False, header=True)
