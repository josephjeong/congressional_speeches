'''
possible improvements:
- keep president from speakers, and combine with l_name: "president"
- deal with the gender generation

'house', 'month', 'day', 'year', 'speech', 'l_name', 'fname', 'datetime', 'bioname', 'state', 'party_name', 'congress', 'Begin Date', 'Adjourn Date'

to

figure out gender

speech_id speech date speaker party district f_name l_name chamber gender state stemmed
'''

from typing import Tuple
import pandas as pd
from datetime import datetime

def date_conversion(row : pd.Series) -> pd.DatetimeIndex:
    '''
    this function needs to catch weird edge cases from bad OCR
    printed dates out successively and inferred correct dates from 
    surrounding dates (intermediate value)
    '''
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

def gen_speakers() -> pd.DataFrame:
    # read in raw speakers file
    # members sourced from: https://voteview.com/articles/data_help_members
    speakers = pd.read_csv("data/HSall_members.csv")
    speakers["congress"] = speakers["congress"].astype(int)

    # get rid of presidents
    speakers = speakers [speakers["chamber"] != "President"]

    # create chambers 
    speakers.loc[speakers["chamber"] == "House", "house"] = "HOUSE OF REPRESENTATIVES"
    speakers.loc[speakers["chamber"] == "Senate", "house"] = "SENATE"

    # separate first name and last name
    speakers[["l_name", "f_name"]] = speakers["bioname"].str.split(",", n=1, expand=True)

    # merge with party names
    # parties sourced from: https://voteview.com/articles/data_help_parties
    parties = pd.read_csv("data/HSall_parties.csv")[["party_code", "party_name"]]
    speakers = pd.merge(speakers, parties, on="party_code")

    # combine session dates with speaker dat
    # get session dates from: https://github.com/shmcminn/congress-begin-end-dates/blob/master/congress-begin-end-dates.csv
    session_dates = pd.read_csv("data/congress_dates.csv")
    session_dates.rename(columns={"Congress": "congress"}, inplace=True)
    session_dates["Begin Date"] = pd.to_datetime(session_dates["Begin Date"], format="%b %d, %Y", errors="raise")
    session_dates["Adjourn Date"] = pd.to_datetime(session_dates["Adjourn Date"], format="%b %d, %Y", errors="raise")
    session_dates = session_dates.groupby(session_dates["congress"]).agg({'Begin Date': 'min', 'Adjourn Date': 'max'})
    speakers = pd.merge(speakers, session_dates, on="congress", how="left")

    # select columns and drop duplicates
    speakers.rename(columns={"state_abbrev": "state", "district_code": "district"}, inplace=True)
    speakers = speakers[["l_name", "f_name", "bioname", "state", "house", "party_name", "congress", "district", "chamber", 'Begin Date', 'Adjourn Date']]
    return speakers.drop_duplicates()

def gen_speeches() -> pd.DataFrame():
    # read in speech data
    df = pd.read_csv("data/speeches.csv", delimiter="|")
    df.rename(columns={"speeches": "speech"}, inplace=True)
    df["l_name"] = df["clean_names"].str.extract(r"\b(\w*?)$")

    # assume all men
    df["gender"] = "M"

    # conversion to datetime for speeches
    df["day"] = df["day"].fillna(1).astype(int) # only one date na (corrects it)
    df["year"] = df["year"].fillna(2011).astype(int) # an outlandish year to catch them
    df["datetime"] = df[['month','day','year']].apply(date_conversion, axis=1)

    # fillna and drop_dupes to make merge work
    df['l_name'] = df['l_name'].fillna(0)
    df['house'] = df['house'].fillna(0)
    return df.drop_duplicates()

def merge_speakers_speeches(speeches : pd.DataFrame, speakers : pd.DataFrame) -> Tuple[(pd.DataFrame, pd.DataFrame)]:
    # copy to df_original to detect duplicate matches
    speeches_og = speeches.copy()

    # merging attaches all speakers that match onto left
    # duplciate matches are created (to be filtered later)
    speeches = pd.merge(speeches, speakers, on=["l_name", "house"], how="left") # it gets much bigger here

    # filter out all speakers who's congressional dates don't match the speech date
    speeches_na = speeches[speeches.isna().any(axis=1)] # na speakers will cause next line to error
    speeches = speeches[(speeches["datetime"] >= speeches["Begin Date"]) & (speeches["datetime"] <= speeches["Adjourn Date"])]
    speeches = pd.concat([speeches, speeches_na])

    # detect duplicate values as seen from df_original
    speeches_small = speeches[["house", "month", "day", "year", "speech", "l_name", "datetime"]]
    df_og_values_not_in_df_small = speeches_og[~speeches_og.astype(str).apply(tuple, 1).isin(
        speeches_small.astype(str).apply(tuple, 1))]
    speeches = pd.concat([speeches, df_og_values_not_in_df_small])
    speeches_duplicates = speeches[speeches.duplicated(subset=["house", "month", "day", "year", "speech", "l_name", "datetime"], keep=False)]

    # drop duplicates (keeps first match, but deletes the rest)
    speeches.drop_duplicates(subset=["house", "month", "day", "year", "speech", "l_name", "datetime"], inplace=True)
    speeches.sort_index(inplace=True)
    speeches.reset_index(inplace=True, drop=True)

    # create date field
    speeches["date"] = speeches["datetime"].dt.strftime("%d %b %Y")
    speeches.rename(columns={"bioname": "speaker", "party_name": "party"}, inplace=True)

    # create correct column names to match corpus.gzip
    speeches = speeches[["speech", "date", "speaker", "party", "district", "f_name", "l_name", "chamber", "gender", "state"]]

    return speeches, speeches_duplicates

def main():
    speakers = gen_speakers()
    speeches = gen_speeches()
    df, df_duplicates = merge_speakers_speeches(speeches, speakers)
    print(df)
    df.to_csv("speakermap.csv", sep="|", index=False, header=True)
    df_duplicates.to_csv("speakermap_duplicates.csv", sep="|", index=False, header=True)

main()