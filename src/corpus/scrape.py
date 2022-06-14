import re
from concurrent.futures import ThreadPoolExecutor
from os import getcwd
from typing import Dict
from urllib.parse import urlencode

import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver
from tqdm import tqdm

PATH = getcwd() + "/chromedriver"

def get_user_permissions():
    driver = webdriver.Chrome(PATH)
    params = {
        "handle": "hein.congrec/conglob0127",
        "collection": "congrec",
        "section": 0,
        "id": 1, # starting page?
        "print": 15, # ending page?
        "sectioncount": 2,
        "ext": ".txt"
    }
    driver.get("https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?" + urlencode(params))
    WebDriverWait(driver, 120).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, "/html/body/pre"),
            "CONGRESS" # once congressional record loads
        ),
        'Authentication timed out'
    )
    reqs = driver.requests
    driver.quit()
    text_req = list(filter(lambda req: "TextGenerator" in req.url , reqs))[-1]
    return dict(text_req.headers)

def remove_dashes_and_newlines(txt: str):
    txt = txt.replace("\n", "")
    txt = txt.replace("-", "")
    return txt

def send_req(params : Dict):
    '''
    Scraps one congressional period of all the text as one cannot scrape all of it at once
    '''
    req_headers = params.pop("req_header")
    i = 2
    text = ""
    output = []
    while text != "\n":
        params["section"] = i
        i += 1
        try:
            resp = requests.get(url="https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?" + urlencode(params), headers=req_headers, timeout=30)
            try:
                text = re.findall("<pre>([\s\S]*)<\/pre>", resp.text)[0]
            except IndexError:
                text = "\n" # newlines are adding double newlines but it breaks otherwise
        except requests.exceptions.Timeout:
            text = "\n"
        output.append(text)
    return output

def scrape_pages(req_headers):
    # create parameters to find all text
    req_params = list(map(lambda file_num: {
        "handle": "hein.congrec/conglob" + str(file_num).zfill(4),
        "collection": "congrec",
        "print": "section",
        "ext": ".txt",
        "req_header": req_headers
    }, range(1, 128)))[:2]

    with ThreadPoolExecutor(max_workers=len(req_params)) as executor:
        # map preserves order of the transcripts
        all_transcript = list(tqdm(executor.map(send_req, req_params), 
            total=len(req_params),
            desc= "scraping all congressional speeches (each iteration takes a while)"
        ))
    concat_list = [j for i in all_transcript for j in i] # flatten transcripts
    transcript = list(map(remove_dashes_and_newlines, concat_list))
    concat_transcripts = "\n".join(transcript)
    new_concat_transcripts = concat_transcripts.replace("\n", "")
    return new_concat_transcripts

def save_transcript(transcript):
    with open("temp/scrape_output.txt", "w", encoding="utf-8") as f:
        f.truncate()
        f.write(transcript)

def scrape_transcripts():
    print("Scraping Websites")
    req_headers = get_user_permissions()
    complete_transcript = scrape_pages(req_headers)
    save_transcript(complete_transcript)
