Setup instructions:
1. add data into a folder labelled "data" in the root directory
    e.g. a file in your repo would be "data/hein-bound/descr_044.txt"
2. run python3 main.py --word "word" --years "start_year-end_year"

If you are missing any files, the code will alert you

The first time you run the code, it'll create a corpus.
Each subsequent run will load the corpus and output to freq.csv

# Issues:
- A weird encoding bug prevents the joining of strings in array in scrape.py
