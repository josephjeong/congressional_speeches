import argparse
from datetime import datetime
import re
import sys
from src.frequency_bound import frequency_bound
from src.create_corpus import create_corpus

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--word', type=str, default=None, help='The word to search for e.g. "Amalgamation"')
    parser.add_argument('--years', type=str, default=None, help='The timeframe in years to search within. (e.g. "1890-1920")')
    args = parser.parse_args()

    # parse the arguments given
    word = args.word
    years = args.years
    start_year = None
    end_year = None
    if years:
        s = r"^(\d{4})-(\d{4})$"
        years = re.findall(s, args.years)
        if not years:
            print("ERROR: Please submit the years in the format start_year-end_year e.g --year 1820-1900")
            sys.exit()
        start_year = datetime(min(list(map(lambda x: int(x), years[0]))), 1, 1)
        end_year = datetime(max(list(map(lambda x: int(x), years[0]))) + 1, 1, 1)

    # create unified corpus
    df = create_corpus()

    # df = frequency_bound(word, start_year, end_year)
    # df.to_csv("out.csv")
    print(df)

if __name__ == "__main__":
    main()