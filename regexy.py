import re
import sys
from typing import Dict, List
from pandas import DataFrame
from pprint import pprint

def first_string(l : List[str]):
    for s in l:
        if s: return re.sub("[^a-zA-Z\s]+", "", s).lstrip()

def speech_dataframes(data: List) -> List[List]:
    # find all the names involved in the speech
    txt = data[4]
    matches = re.findall(r'^\s(?:Mr\.((?:\s[A-Z].{1}[A-Z]*?)+)\W|(The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, re.MULTILINE)
    clean_names = list(map(first_string, matches))
    clean_names.insert(0, "") # no name at the starting portion of text

    # find all the speeches split by same criteria
    speeches = re.split(r'^\s(?:Mr\.(?:(?:\s[A-Z].{1}[A-Z]*?)+)\W|(?:The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, flags=re.MULTILINE)
    speeches = list(map(lambda s: s.replace("\n", " ") if s else "", speeches))

    # print(len(clean_names) - len(speeches))
    
    labelled_speeches = zip(clean_names, speeches)
    return [[data[0], data[1], data[2], data[3], l[0], l[1]] for l in labelled_speeches]

    # return {"names": clean_names, "speeches": speeches}

    # # create dataframe with speeches categorised by name
    # df = DataFrame({"names": clean_names, "speeches": speeches})
    # return df

def read_text() -> str:
    with open("output.txt", "r", encoding="utf-8") as f:
        return f.read()


txt = read_text()

segment = re.split(r"^\s(HOUSE\sOF\sREPRESENTATIVES|SENATE).\n\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\W\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d*?),\s(\d*)", txt, flags=re.MULTILINE | re.IGNORECASE)
segment.pop(0)
data = [[house, month, day, year, speech] for house, month, day, year, speech in zip(segment[0::5], segment[1::5], segment[2::5], segment[3::5], segment[4::5])]
data = list(map(speech_dataframes, data))
data = [item for sublist in data for item in sublist]
df = DataFrame(data)
df.columns = ["house", "month", "day", "year", "clean_names", "speeches"]
df.to_csv("speeches.csv", sep="|", index=False, header=True)
# df[:3000].to_csv("smaller.csv", sep="|")
# for row in data:
#     new_rows = []
#     for key in row[4]:
#         new_rows.append([row[0], row[1], row[2], row[3], row[4][key]])
#     print(new_rows)
#     import sys
#     sys.exit()

# df = DataFrame(data, columns=["chamber", "month", "day", "year", "speech", "speaker"])
# print(df)

# dates = re.findall(r"^\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\W\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d*?),\s(\d*)", txt, flags=re.MULTILINE | re.IGNORECASE)
# print(len(dates))
# dates = re.split(r"^\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\W\s(?:january|february|march|april|may|june|july|august|september|october|november|december)\s\d*?,\s\d*", txt, flags=re.MULTILINE | re.IGNORECASE)
# print(len(dates))

# houses = re.split(r"^\s(HOUSE OF REPRESENTATIVES|SENATE)", txt, flags=re.MULTILINE)
# print(houses.pop(0))
# data = [[house, speech] for house, speech in zip(houses[0::2], houses[1::2])]
# df = DataFrame(data)
# df.to_csv("speeches.csv")
# print(len(houses))


# with open("out.log", "w", encoding="utf-8") as log:
#     log.truncate()
#     pprint(houses, stream=log)

# df = speech_dataframes(txt)
# print(df)
