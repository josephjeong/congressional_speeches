import re
from typing import List
from pandas import DataFrame
from pprint import pprint

def first_string(l : List[str]):
    for s in l:
        if s: return re.sub("[^a-zA-Z\s]+", "", s).lstrip()


with open("output.txt", "r", encoding="utf-8") as f:
    txt = f.read()
    matches = re.findall(r'^\s(?:Mr\.((?:\s[A-Z].{1}[A-Z]*?)+)\W|(The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, re.MULTILINE)
    clean_names = list(map(first_string, matches))

    speeches = re.split(r'^\s(?:Mr\.(?:\s[A-Z].{1}[A-Z]*?)+)\W|The\s(?:SPEAKER|VICE\sPRESIDENT)', txt, flags=re.MULTILINE)
    speeches = list(map(lambda s: s.replace("\n", " ") if s else "", speeches))
    clean_names.insert(0, "")
    print(len(clean_names), len(speeches), len(clean_names) - len(speeches))
    l = [clean_names, speeches]
    d = list(map(list, zip(*l)))
    # print(d)
    with open("out.log", "w", encoding="utf-8") as fa:
        pprint(d, stream=fa)
        # fa.write(str(d))=
    # for speech in speeches:
    #     print("new line", speech.encode("utf-8"))
    # df = DataFrame({"names": clean_names, "speeches": speeches})
    # print(df)