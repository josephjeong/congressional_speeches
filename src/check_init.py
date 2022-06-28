import os
import sys

def check_init() -> None:
    folders_to_create = [
        "data/hein_dataset/hein_bound",
        "data/HSall_dataset/",
        "output/",
        "temp/"
    ]
    for folder in folders_to_create:
        if not os.path.exists(folder):
            print(f"Creating path: {folder}")
            os.makedirs(folder)

    files_to_exist = {
        "data/hein_dataset/hein-bound/043_SpeakerMap.txt": "https://primoa.library.unsw.edu.au/primo-explore/fulldisplay?docid=UNSW_ALMA61158502230001731&vid=UNSWS&lang=en_US&context=L",
        "data/HSall_dataset/congress_dates.csv": "https://github.com/shmcminn/congress-begin-end-dates/blob/master/congress-begin-end-dates.csv\nAnd please remove all rows where the date format is not: %b %d, %Y",
        "data/HSall_dataset/HSall_members.csv": "https://voteview.com/articles/data_help_members",
        "data/HSall_dataset/HSall_parties.csv": "https://voteview.com/articles/data_help_parties",
        "chromedriver": "Please download the relevant chromedriver here: https://chromedriver.chromium.org/downloads"
    }

    all_exist = True
    for file, website in files_to_exist.items():
        if not os.path.exists(file):
            print(f"Data file required does not exist at {file}\n Please source it here: {website}")
            all_exist = False
    if not all_exist:
        sys.exit(1)
