
from typing import List, Tuple
from pytest import param
import requests

# res = requests.get("https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?handle=hein.congrec/conglob0127&collection=congrec&section=0&id=1&print=15&sectioncount=2&ext=.txt")
# print(res.text)

from seleniumwire import webdriver
import pprint
import time
from os import getcwd

PATH = getcwd() + "/chromedriver"
driver = webdriver.Chrome(PATH)

# headers={'Host': 'heinonline-org.wwwproxy1.library.unsw.edu.au', 'Connection': 'keep-alive', 'Cache-Control': 'max-age=0', 'Upgrade-Insecure-Requests': "1", 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'Sec-Fetch-Site': 'cross-site', 'Sec-Fetch-Mode': 'navigate', 'Sec-Fetch-Dest': 'document', 'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"', 'sec-ch-ua-mobile': '?0', 'sec-ch-ua-platform': '"macOS"', 'Referer': 'https://login.microsoftonline.com/', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8', 'Cookie': 'ezproxy=BeJpzPYalmpafyo; ezproxyl=BeJpzPYalmpafyo; ezproxyn=BeJpzPYalmpafyo'}
# req = requests.get(url='https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?handle=hein.congrec/conglob0127&collection=congrec&section=0&id=1&print=15&sectioncount=2&ext=.txt', headers=headers)
# print(req.text)

from urllib.parse import urlencode
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

# for i in range(0, 1000):
#     req = requests.get(url='https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?handle=hein.congrec/conglob0127&collection=congrec&section=0&id=16&print=30&sectioncount=2&ext=.txt', headers=req_headers)
#     if req.status_code != 200:
#         print("this failed")
#         import sys
#         sys.exit()
#     print("another one", i, len(req.text))
# print("yay it works!\n", req.text)

from concurrent.futures import ThreadPoolExecutor

def send_req(starts: Tuple[int, int]) -> str:
    params = {
        "handle": "hein.congrec/conglob0127",
        "collection": "congrec",
        "section": 0,
        "id": starts[0],
        "print": starts[1],
        "sectioncount": 2,
        "ext": ".txt"
    }
    # https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?handle=hein.congrec/conglob0127&collection=congrec&section=0&id=956&print=21&sectioncount=1&ext=.txt
    print(params)
    req = requests.get(url="https://heinonline-org.wwwproxy1.library.unsw.edu.au/HOL/TextGenerator?" + urlencode(params), headers=req_headers)
    return req.text

starts = list(map(lambda x: (x, x+15), range(0, 200, 15)))
print(starts)

with ThreadPoolExecutor() as executor:
    all_transcript = list(executor.map(
        send_req, starts
    ))
    pp.pprint(all_transcript)