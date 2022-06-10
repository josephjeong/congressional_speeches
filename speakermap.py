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
speakers = speakers[["lastname", "bioname", "state_abbrev", "house", "party_name", "congress"]]
speakers.drop_duplicates(inplace=True)

session_dates = pd.read_csv("data/congress_dates.csv")
session_dates["congress"] = session_dates["Congress"]
session_dates.drop(columns=["Congress", "Session"], axis=1, inplace=True)
session_dates["Begin Date"] = pd.to_datetime(session_dates["Begin Date"], format="%b %d, %Y", errors="raise")
session_dates["Adjourn Date"] = pd.to_datetime(session_dates["Adjourn Date"], format="%b %d, %Y", errors="raise")
aggregation_functions = {'Begin Date': 'min', 'Adjourn Date': 'max'}
session_dates = session_dates.groupby(session_dates["congress"]).aggregate(aggregation_functions)
speakers = pd.merge(speakers, session_dates, on="congress", how="left")

df = pd.read_csv("data/speeches.csv", delimiter="|")
df["lastname"] = df["clean_names"].str.extract(r"\b(\w*?)$")
df.drop(columns=["clean_names"], inplace=True)

def date_conversion(row):
    # this function needs to catch weird edge cases from bad OCR
    # printed dates out successively and inferred correct dates from 
    # surrounding dates (intermediate value)
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
    elif (date == "April 19 2011"): year = 1836
    elif (date == "February 25 1637"): year = 1837
    elif (date == "May 1 1640"): year = 1840
    elif (date == "July 28 1641"): year = 1841
    elif (date == "August 7 1811"): year = 1841
    elif (date == "March 19 1812"): year = 1842
    elif (date == "April 21 1812"): year = 1842
    elif (date == "May 25 1944"): year = 1844
    elif (date == "February 10 1745"): year = 1845
    elif (date == "April 16 3850"): year = 1850
    elif (date == "February 5 3862"): year = 1862
    elif (date == "April 4 1806"): year = 1866
    elif (date == "January 19 1887"): year = 1867
    elif (date == "July 5 1887"): year = 1867
    # return datetime.strptime(f"{month} {day} {year}", '%B %d %Y')
    try:
        if (year < 1833 or year > 1875): print(f"{month} {day} {year}")
        return pd.to_datetime(f"{month} {day} {year}", format='%B %d %Y')
    except:
        print(f"{month} {day} {year}")
        return pd.to_datetime(datetime.now())

# conversion to datetime for speeches
df["day"] = df["day"].fillna(1).astype(int) # generally this seems to work
df["year"] = df["year"].fillna(2011).astype(int) # an outlandish year
df["datetime"] = df[['month','day','year']].apply(date_conversion, axis=1)

df['year'] = df['datetime'].dt.year
df['month'] = df['datetime'].dt.month
df['day'] = df['datetime'].dt.day

df['lastname'] = df['lastname'].fillna(0)
df['house'] = df['house'].fillna(0)

df.drop_duplicates(inplace=True)
speakers.drop_duplicates(inplace=True)

df_original = df.copy()

df = pd.merge(df, speakers, on=["lastname", "house"], how="left") # it gets much bigger here

df_na = df[df.isna().any(axis=1)]
df = df[(df["datetime"] >= df["Begin Date"]) & (df["datetime"] <= df["Adjourn Date"])]
df = pd.concat([df, df_na])
df1 = df_original
df2 = df[["house", "month", "day", "year", "speeches", "lastname", "datetime"]]
df1_values_not_in_df2 = df1[~df1.astype(str).apply(tuple, 1).isin(df2.astype(str).apply(tuple, 1))]
df = pd.concat([df, df1_values_not_in_df2])
df_duplicates = df[df.duplicated(subset=["house", "month", "day", "year", "speeches", "lastname", "datetime"], keep=False)]
# drop duplicates (keeps first match, but deletes the rest)
df.drop_duplicates(subset=["house", "month", "day", "year", "speeches", "lastname", "datetime"], inplace=True)
df.sort_index(inplace=True)
df.reset_index(inplace=True, drop=True)

"""
'house', 'month', 'day', 'year', 'speeches', 'lastname', 'datetime', 'bioname', 'state_abbrev', 'party_name', 'congress', 'Begin Date', 'Adjourn Date'
"""
# df.to_csv("speakermap.csv", sep="|", index=False, header=True)
# df_duplicates.to_csv("speakermap_duplicates.csv", sep="|", index=False, header=True)
