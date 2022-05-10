import re

with open("output.txt", "r", encoding="utf-8") as f:
    txt = f.read()
    print(re.findall('^\s(?:Mr\.((?:\s[A-Z].{1}[A-Z]*?)+)\W|(The\s(?:SPEAKER|VICE\sPRESIDENT)))', txt, re.MULTILINE))