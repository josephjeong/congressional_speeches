import requests
from seleniumwire import webdriver
import pprint
import time
from urllib.parse import urlencode
from os import getcwd
import re

PATH = getcwd() + "/chromedriver"
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
time.sleep(30)
pp = pprint.PrettyPrinter(indent=4)
print(driver.title)
print(driver.get_cookies())
pp.pprint(driver.requests)

reqs = driver.requests

driver.quit()

text_req = list(filter(lambda req: "TextGenerator" in req.url , reqs))[-1]
req_headers = dict(text_req.headers)

pp.pprint(req_headers)

req_params = list(map(lambda file_num: {
    "handle": "hein.congrec/conglob" + str(file_num).zfill(4),
    "collection": "congrec",
    "print": "section",
    "ext": ".txt"
}, range(1, 128)))

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

from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

with ThreadPoolExecutor(max_workers=len(req_params)) as executor:
    all_transcript = list(tqdm(executor.map(
        send_req, req_params
    ), total=len(req_params)))
    concat_list = [j for i in all_transcript for j in i]
    print("concatenated all lists!")
    all_transcript = list(map(format_text, concat_list))
    concat_transcripts = "\n".join(all_transcript)
    concat_transcripts = concat_transcripts.replace("\n", "")
    
    print("concatenated all lists!")
    with open("output.txt", "w", encoding="utf-8") as f:
        f.truncate()
        f.write(concat_transcripts)

concat_transcripts.lower()