import pandas as pd
import re
import os 
import concurrent.futures
from tqdm import tqdm

def load_speeches(dir: str) -> pd.DataFrame:
    with open(dir, "r") as file:
        lines = "\n".join(list(map(lambda x: re.findall(r"^(.*?)\|", x)[0] +"|"+re.findall(r"^.*?\|(.*)", x)[0].replace("|", " "), file.readlines()[1:])))
    return pd.DataFrame([x.split("|") for x in lines.split("\n")])

def load_descriptions(dir: str) -> pd.DataFrame():
    return pd.read_csv(dir, sep="|", encoding="ansi")

def load_speakers(dir: str) -> pd.DataFrame():
    return pd.read_csv(dir, sep="|", encoding="ansi")

def create_corpus():
    DIR = "data/hein-bound/"
    files = os.listdir(DIR)
    
    speech_files = list(map(lambda x: DIR + x, filter(lambda x: "speeches" in x, files)))
    speeches = None # higher namespace
    with concurrent.futures.ProcessPoolExecutor() as executor:
        speeches = pd.concat(tqdm( # flatten and add progress bar
                executor.map(load_speeches, speech_files, chunksize=1), # read stories and create rows
                total=len(speech_files),
                desc= "Reading In Speeches"
            )
        ).dropna()
        speeches.columns = ["speech_id", "speech"]
        speeches["speech_id"] = speeches["speech_id"].astype(int)

    descr_files = list(map(lambda x: DIR + x, filter(lambda x: "descr" in x, files)))
    descriptions = None
    with concurrent.futures.ProcessPoolExecutor() as executor:
        descriptions = pd.concat(tqdm( # flatten and add progress bar
                executor.map(load_descriptions, descr_files, chunksize=1), # read stories and create rows
                total=len(descr_files),
                desc= "Reading In Descriptions"
            )
        ).dropna()
        descriptions["speech_id"] = descriptions["speech_id"].astype(int)
        descriptions.drop(columns=["number_within_file", "line_start", "line_end", "file", "char_count", "word_count"], inplace=True)

    speaker_files = list(map(lambda x: DIR + x, filter(lambda x: "SpeakerMap" in x, files)))
    speakers = None
    with concurrent.futures.ProcessPoolExecutor() as executor:
        speakers = pd.concat(tqdm( # flatten and add progress bar
                executor.map(load_speakers, speaker_files, chunksize=1), # read stories and create rows
                total=len(descr_files),
                desc= "Reading In Speakers"
            )
        ).dropna()
        speakers["speech_id"] = speakers["speech_id"].astype(int)
        # speakers.drop(columns=["number_within_file"])
    
    print("joining tables")
    df = pd.merge(speeches, descriptions, on="speech_id", how="left")
    df = pd.merge(df, speakers, on="speech_id", how="left")
    # df = pd.merge(speeches, descriptions, on="speech_id")
    # df = pd.merge(df, speakers, on="speech_id")

    print("deduping data")
    df.fillna('', inplace=True)
    df.loc[(df["first_name"] == "Unknown") & (df["firstname"] == ""), "f_name"] = " "
    df.loc[(df["first_name"] == "Unknown") & (df["firstname"] != ""), "f_name"] = df["firstname"]
    df.loc[(df["first_name"] != "Unknown") & (df["firstname"] != ""), "f_name"] = df["firstname"]
    df.loc[(df["first_name"] != "Unknown") & (df["firstname"] == ""), "f_name"] = df["first_name"]

    df.loc[(df["last_name"] == "Unknown") & (df["lastname"] == ""), "l_name"] = " "
    df.loc[(df["last_name"] == "Unknown") & (df["lastname"] != ""), "l_name"] = df["lastname"]
    df.loc[(df["last_name"] != "Unknown") & (df["lastname"] != ""), "l_name"] = df["lastname"]
    df.loc[(df["last_name"] != "Unknown") & (df["lastname"] == ""), "l_name"] = df["last_name"]

    df.loc[(df["chamber_x"] == "E") & (df["chamber_y"] == ""), "chamber"] = " "
    df.loc[(df["chamber_x"] == "E") & (df["chamber_y"] != ""), "chamber"] = df["chamber_y"]
    df.loc[(df["chamber_x"] != "E") & (df["chamber_y"] != ""), "chamber"] = df["chamber_y"]
    df.loc[(df["chamber_x"] != "E") & (df["chamber_y"] == ""), "chamber"] = df["chamber_x"]

    df.loc[(df["gender_x"] == "Special") & (df["gender_y"] == ""), "gender"] = " "
    df.loc[(df["gender_x"] == "Special") & (df["gender_y"] != ""), "gender"] = df["gender_y"]
    df.loc[(df["gender_x"] != "Special") & (df["gender_y"] != ""), "gender"] = df["gender_y"]
    df.loc[(df["gender_x"] != "Special") & (df["gender_y"] == ""), "gender"] = df["gender_x"]

    df.loc[(df["state_x"] == "Unknown") & (df["state_y"] == ""), "state"] = " "
    df.loc[(df["state_x"] == "Unknown") & (df["state_y"] != ""), "state"] = df["state_y"]
    df.loc[(df["state_x"] != "Unknown") & (df["state_y"] != ""), "state"] = df["state_y"]
    df.loc[(df["state_x"] != "Unknown") & (df["state_y"] == ""), "state"] = df["state_x"]

    df.drop(columns=["first_name", "firstname", "last_name", "lastname", "chamber_x", "chamber_y", "gender_x", "gender_y", "state_x", "state_y", "speakerid", "nonvoting"], inplace=True)

    # date, who said it, which party, which chamber, state, district
    return df