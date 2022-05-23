from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import requests
from seleniumwire import webdriver
import pprint
import time
from os import getcwd
import re
from typing import Dict, List
from pandas import DataFrame
from pprint import pprint
import pandas as pd

def format_text(txt: str):
    txt = txt.replace("\n", "")
    txt = txt.replace("-", "")
    return txt

def send_req(params):
    i = 2
    text = ""
    output = []
    while text != "\n":
        params["section"] = i
        i += 1
        try:
            req = requests.get(url="https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?" + urlencode(params), headers=req_headers, timeout=30)
            try:
                text = re.findall("<pre>([\s\S]*)<\/pre>", req.text)[0]
                # replace newline with space to eliminate reandom newlines in requests?
            except IndexError:
                text = "\n" # newlines are adding double newlines but it seems to break otherwise
        except requests.exceptions.Timeout:
            text = "\n"
        output.append(text)
        print(str(params["handle"]) + " " + str(i))
    return output

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

def scrape():
    # req_params = list(map(lambda file_num: {
    #     "handle": "hein.congrec/conglob" + str(file_num).zfill(4),
    #     "collection": "congrec",
    #     "print": "section",
    #     "ext": ".txt"
    # }, range(1, 128)))

    # PATH = getcwd() + "/chromedriver"
    # driver = webdriver.Chrome(PATH)

    # from urllib.parse import urlencode
    # params = {
    #     "handle": "hein.congrec/conglob0127",
    #     "collection": "congrec",
    #     "section": 0,
    #     "id": 1, # starting page?
    #     "print": 15, # ending page?
    #     "sectioncount": 2,
    #     "ext": ".txt"
    # }
    # driver.get("https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?" + urlencode(params))
    # time.sleep(30)
    # pp = pprint.PrettyPrinter(indent=4)
    # print(driver.title)
    # print(driver.get_cookies())
    # pp.pprint(driver.requests)

    # reqs = driver.requests

    # driver.quit()

    # text_req = list(filter(lambda req: "TextGenerator" in req.url , reqs))[-1]

    # with ThreadPoolExecutor(max_workers=len(req_params)) as executor:
    #     all_transcript = list(tqdm(executor.map(
    #         send_req, req_params
    #     ), total=len(req_params)))
    #     concat_list = [j for i in all_transcript for j in i]
    #     print("concatenated all lists!")
    #     all_transcript = list(map(format_text, concat_list))
    #     concat_transcripts = "\n".join(all_transcript)
    #     concat_transcripts = concat_transcripts.replace("\n", "")
    #     # concat_transcripts = concat_transcripts.lower()
        
    # print("concatenated all lists!")
    # with open("output.txt", "w", encoding="utf-8") as f:
    #     f.truncate()
    #     f.write(concat_transcripts)

    # txt = concat_transcripts

    # segment = re.split(r"^\s(HOUSE\sOF\sREPRESENTATIVES|SENATE).\n\s(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)\W\s(january|february|march|april|may|june|july|august|september|october|november|december)\s(\d*?),\s(\d*)", txt, flags=re.MULTILINE | re.IGNORECASE)
    # segment.pop(0)
    # data = [[house, month, day, year, speech] for house, month, day, year, speech in zip(segment[0::5], segment[1::5], segment[2::5], segment[3::5], segment[4::5])]
    # data = list(map(speech_dataframes, data))
    # data = [item for sublist in data for item in sublist]
    # df = DataFrame(data)
    # df.columns = ["house", "month", "day", "year", "clean_names", "speeches"]
    # df.to_csv("speeches.csv", sep="|", index=False, header=True)

    # speakers = pd.read_csv("data/HSall_members.csv")
    speakers = pd.read_csv("../data/HSall_members.csv")
    speakers = speakers.dropna(subset=["died", "born"])
    speakers = speakers[["congress", "chamber", "state_abbrev", "bioname", "party_code", "born", "died"]]
    speakers["born"] = speakers["born"].astype(int)
    speakers["died"] = speakers["died"].astype(int)
    speakers["congress"] = speakers["congress"].astype(int)
    speakers = speakers[(speakers["congress"] >= 23) & (speakers["congress"] <= 45)]
    speakers = speakers [speakers["chamber"] != "President"]

    # parties sourced from: https://voteview.com/articles/data_help_parties
    parties = pd.read_csv("../data/HSall_parties.csv")[["party_code", "party_name"]]
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
    df.to_csv("output.csv")