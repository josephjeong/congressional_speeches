def read_text():
    with open("output.txt", "r", encoding="utf-8") as f:
        return f.read()

# import enchant
# print(enchant.list_languages())

from enchant.checker import SpellChecker

chkr = SpellChecker()
chkr.set_text(read_text())
for err in chkr:
    sug = err.suggest()
    print(err.word, sug)
    err.replace(sug)

import enchant
help(enchant)