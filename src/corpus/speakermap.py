'''
possible improvements:
- keep president from speakers, and combine with l_name: "president"
- deal with the gender generation
'''
from datetime import datetime
from mimetypes import init
from typing import Tuple

import pandas as pd

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
    elif (date == "April 1 1"): year = 1836
    elif (date == "April 19 1"): year = 1836
    elif (date == "February 27 1"): year = 1838
    elif (date == "July 9 1"): year = 1841
    elif (date == "December 29 1"): year = 1848
    elif (date == "January 11 1"): year = 1853
    elif (date == "December 17 1"): year = 1856
    # return datetime.strptime(f"{month} {day} {year}", '%B %d %Y')
    try:
        if (year < 1833 or year > 1875): print(f"Incorrect date: {month} {day} {year}")
        return pd.to_datetime(f"{month} {day} {year}", format='%B %d %Y')
    except:
        print(f"Incorrect date: {month} {day} {year}")
        return pd.to_datetime(datetime.now())

# def gen_speakers(speakers: str) -> pd.DataFrame:
def gen_speakers() -> pd.DataFrame:
    # read in raw speakers file
    # members sourced from: https://voteview.com/articles/data_help_members
    speakers = pd.read_csv("data/HSall_dataset/HSall_members.csv")
    speakers["congress"] = speakers["congress"].astype(int)

    # get rid of presidents
    speakers = speakers [speakers["chamber"] != "President"]

    # create chambers 
    speakers.loc[speakers["chamber"] == "House", "house"] = "HOUSE OF REPRESENTATIVES"
    speakers.loc[speakers["chamber"] == "Senate", "house"] = "SENATE"

    # separate first name and last name
    speakers[["l_name", "f_name"]] = speakers["bioname"].str.split(",", n=1, expand=True)

    # remove obviously wrong congress dates
    speakers = speakers[speakers["congress"] <= 55]

    # merge with party names
    # parties sourced from: https://voteview.com/articles/data_help_parties
    parties = pd.read_csv("data/HSall_dataset/HSall_parties.csv")[["party_code", "party_name"]]
    speakers = pd.merge(speakers, parties, on="party_code")

    # combine session dates with speaker data
    # get session dates from: https://github.com/shmcminn/congress-begin-end-dates/blob/master/congress-begin-end-dates.csv
    session_dates = pd.read_csv("data/HSall_dataset/congress_dates.csv")
    session_dates.rename(columns={"Congress": "congress"}, inplace=True)
    session_dates["Begin Date"] = pd.to_datetime(session_dates["Begin Date"], format="%b %d, %Y", errors="raise")
    session_dates["Adjourn Date"] = pd.to_datetime(session_dates["Adjourn Date"], format="%b %d, %Y", errors="raise")
    session_dates = session_dates.groupby(session_dates["congress"]).agg({'Begin Date': 'min', 'Adjourn Date': 'max'})
    speakers = pd.merge(speakers, session_dates, on="congress", how="left")

    # select columns and drop duplicates
    speakers.rename(columns={"state_abbrev": "state", "district_code": "district"}, inplace=True)
    speakers = speakers[["l_name", "f_name", "bioname", "state", "house", "party_name", "congress", "district", "chamber", 'Begin Date', 'Adjourn Date']]
    return speakers.drop_duplicates()

def process_speeches(df):
    df.rename(columns={"speeches": "speech"}, inplace=True)
    df["l_name"] = df["clean_names"].str.extract(r"\b(\w*?)$")

    # assume all men
    df["gender"] = "M"

    # lots of empty strings
    df = df.replace(r'^\s*$', 1, regex=True)

    # conversion to datetime for speeches
    df["day"] = df["day"].fillna(1).astype(int) # only one date na (corrects it)
    df["year"] = df["year"].fillna(2011).astype(int) # an outlandish year to catch them
    df["datetime"] = df[['month','day','year']].apply(date_conversion, axis=1)

    # fillna and drop_dupes to make merge work
    df['l_name'] = df['l_name'].fillna(0)
    df['house'] = df['house'].fillna(0)
    return df.drop_duplicates()

def lower_and_split(s : str):
    s = s.lower()
    s = s.split()
    try: 
        return s[0]
    except:
        print(s)
        return ""

def initials_apply(s : str):
    s = lower_and_split(s)
    s = s[0]
    return s

def reconcile_duplicates(df : pd.DataFrame):
    # check how many have a first name
    first_names = df[df["clean_names"].str.contains(" ")]
    not_first_names = df[~df["clean_names"].str.contains(" ")]
    # one_space = "^[a-zA-Z0-9]+\s[a-zA-Z0-9]+$"
    one_space = first_names["clean_names"].str.contains("^[a-zA-Z0-9]{2,}\s[a-zA-Z0-9]{2,}$")
    first_names_only = first_names[one_space]
    initials = first_names[~one_space]

    # find the ones with first names
    first_name_match_subset = first_names_only["clean_names"].apply(lower_and_split) == first_names_only["f_name"].apply(lower_and_split)
    first_name_match = first_names_only[first_name_match_subset]
    # print(first_name_match)

    # take the remaining values 
    first_name_no_match = first_names_only.merge(first_name_match.drop_duplicates(), on=["speech", "clean_names"], how="left", indicator=True)
    first_name_no_match = first_name_no_match[first_name_no_match["_merge"] == "left_only"]

    # process the initials
    initials_match_subset = initials["clean_names"].apply(initials_apply) == initials["f_name"].apply(initials_apply)
    initials_match = initials[initials_match_subset]
    initials_no_match = initials.merge(initials_match.drop_duplicates(), on=["speech", "clean_names"], how="left", indicator=True)
    initials_no_match = initials_no_match[initials_no_match["_merge"] == "left_only"]

    match = pd.concat([first_name_match, initials_match])
    no_match = pd.concat([first_name_no_match, initials_no_match])

    no_match = no_match[['house_x', 'month_x', 'day_x', 'year_x', 'clean_names', 'speech',    
        'l_name_x', 'gender_x', 'datetime_x', 'f_name_x', 'bioname_x',
        'state_x', 'party_name_x', 'congress_x', 'district_x', 'chamber_x',    
        'Begin Date_x', 'Adjourn Date_x']]
    no_match = no_match.rename(columns={
        'house_x' : 'house', 
        'month_x' : 'month', 
        'day_x' : 'day', 
        'year_x' : 'year', 
        'l_name_x' : 'l_name', 
        'gender_x' : 'gender', 
        'datetime_x' : 'datetime', 
        'f_name_x' : 'f_name', 
        'bioname_x' : 'bioname',
        'state_x' : 'state', 
        'party_name_x' : 'party_name', 
        'congress_x' : 'congress', 
        'district_x' : 'district', 
        'chamber_x' : 'chamber',    
        'Begin Date_x' : 'Begin Date', 
        'Adjourn Date_x' : 'Adjourn Date'
    })

    no_match = pd.concat([no_match, not_first_names])

    return match, no_match

def merge_speakers_speeches(speeches : pd.DataFrame, speakers : pd.DataFrame) -> Tuple[(pd.DataFrame, pd.DataFrame)]:
    num_speeches = speeches.shape[0]
    # merging attaches all speakers that match onto left
    # duplciate matches are created (to be filtered later)
    speeches = pd.merge(speeches, speakers, on=["l_name", "house"], how="left") # it gets much bigger here

    # find all na values and filter them out
    na_mask = speeches.isna().any(axis=1)
    speeches_na = speeches[na_mask] # no duplicates in speeches_na
    speeches = speeches[~na_mask]

    # find speeches who fit within the correct time
    time_mask = (speeches["datetime"] >= speeches["Begin Date"]) & (speeches["datetime"] <= speeches["Adjourn Date"])
    speeches_matched  = speeches[time_mask]
    speeches_unmatched = speeches[~time_mask] # some of these are incorrectly unmatched
    # we need to remove these duplicates, and add them to speeches_na

    subset = ["house", "month", "day", "year", "speech", "l_name", "datetime"]

    # for matched speeches, remove duplicates
    duplicate_mask = speeches_matched.duplicated(subset=subset, keep=False)
    speeches_duplicate = speeches_matched[duplicate_mask]
    speeches_not_duplicate = speeches_matched[~duplicate_mask]

    # find the number of incorrectly unmatched speeches
    speeches_matched_no_dupes = pd.concat(
        [speeches_na, 
        speeches_duplicate.drop_duplicates(subset=subset, keep="first"), 
        speeches_not_duplicate]
    )

    # find common values between unmatched speeches, and matched speeches to put back into na
    common = speeches_unmatched.merge(speeches_matched_no_dupes, on=subset, how="left", indicator=True)
    speeches_unmatched_na = common[common['_merge'] == "left_only"].drop_duplicates(subset=subset)
    speeches_na_final = pd.concat([speeches_na, speeches_unmatched_na])

    # resolve duplicates
    duplicates_match, duplicates_no_match = reconcile_duplicates(speeches_duplicate)

    # add na speeches back to final matched
    speeches_matched_final = pd.concat([speeches_not_duplicate, speeches_na_final, duplicates_match]).drop(labels=["_merge"], axis=1)
    speeches_duplicate_final = duplicates_no_match

    print(f"""
    Final Stats for speech matching:
    - Input Speeches: {num_speeches}
    - One Match: {speeches_not_duplicate.shape[0] + duplicates_match.shape[0]}
    - No Match: {speeches_na_final.shape[0]}
    - Duplicate Matches: {speeches_duplicate_final.drop_duplicates(subset=["speech", "clean_names"]).shape[0]}
    - Total Output Speeches: {speeches_not_duplicate.shape[0] + speeches_na_final.shape[0] + speeches_duplicate.drop_duplicates(subset=subset).shape[0]}
    - Missing Speeches: {num_speeches - (speeches_not_duplicate.shape[0] + speeches_na_final.shape[0] + speeches_duplicate.drop_duplicates(subset=subset).shape[0])}
    """)

    # create date field
    speeches_matched_final["date"] = speeches_matched_final["datetime"].dt.strftime("%Y%m%d")
    speeches_matched_final.rename(columns={"bioname": "speaker", "party_name": "party"}, inplace=True)

    # create correct column names to match corpus.gzip
    speeches_matched_final = speeches_matched_final[["speech", "date", "speaker", "party", "district", "f_name", "l_name", "chamber", "gender", "state"]]

    return speeches_matched_final, speeches_duplicate_final

def map_speakers(speeches):
    print("Mapping Speakers")
    speakers = gen_speakers()
    speeches = process_speeches(speeches)
    df, df_duplicates = merge_speakers_speeches(speeches, speakers)
    df_duplicates.to_csv("temp/speakermap_duplicates.csv", sep="|", index=False, header=True)
    df.to_csv("temp/speakermap.csv", sep="|", index=False, header=True)
    return df
