import re
from typing import List

from pandas import DataFrame

def find_clean_name(l : List[str]):
    for s in l:
        if s: return re.sub("[^a-zA-Z\s]+", "", s).lstrip()

def speech_dataframes(data: List) -> List[List]:
    # find all the names involved in the speech
    txt = data[4]
    matches = re.findall(r'^\s(?:Mr\.((?:\s[A-Z].{1}[A-Z]*?)+)\W|(The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, re.MULTILINE)
    clean_names = list(map(find_clean_name, matches))
    clean_names.insert(0, "") # no name at the starting portion of text

    # find all the speeches split by same criteria
    speeches = re.split(r'^\s(?:Mr\.(?:(?:\s[A-Z].{1}[A-Z]*?)+)\W|(?:The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, flags=re.MULTILINE)
    speeches = list(map(lambda s: s.replace("\n", " ") if s else "", speeches))

    labelled_speeches = zip(clean_names, speeches)
    return [[data[0], data[1], data[2], data[3], l[0], l[1]] for l in labelled_speeches]

def read_text() -> str:
    with open("output.txt", "r", encoding="utf-8") as f:
        return f.read()

def chamber_and_dates(txt: str):
    # split based on chamber and dates
    segment = re.split(
        r"^\s(HOUSE\sOF\sREPRESENTATIVES|SENATE).\n\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\W\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d*?),\s(\d*)", 
        txt, flags=re.MULTILINE | re.IGNORECASE)
    segment.pop(0)
    return [[house, month, day, year, speech] for house, month, day, year, speech in zip(segment[0::5], segment[1::5], segment[2::5], segment[3::5], segment[4::5])]

def process_raw_text():
    txt = read_text()
    data = chamber_and_dates(txt)
    data = list(map(speech_dataframes, data))
    data = [item for sublist in data for item in sublist] # flatten speech characteristics
    df = DataFrame(data)
    df.columns = ["house", "month", "day", "year", "clean_names", "speeches"]
    # df.to_csv("speeches.csv", sep="|", index=False, header=True)
    return df
