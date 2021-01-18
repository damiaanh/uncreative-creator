from scraper import *
from editor import *
from datetime import date
import os
#import shutil

def printBanner():
    banner ="""
     _    _                           _   _
    | |  | |                         | | (_)
    | |  | |_ __   ___ _ __ ___  __ _| |_ ___   _____
    | |  | | '_ \ / __| '__/ _ \/ _` | __| \ \ / / _ \\
    | |__| | | | | (__| | |  __/ (_| | |_| |\ V /  __/
     \____/|_| |_|\___|_|  \___|\__,_|\__|_| \_/ \___|
    / ____|               | |
    | |     _ __ ___  __ _| |_ ___  _ __
    | |    | '__/ _ \/ _` | __/ _ \| '__|
    | |____| | |  __/ (_| | || (_) | |
     \_____|_|  \___|\__,_|\__\___/|_|

    """
    print(banner)

if __name__ == "__main__":
    printBanner()
    date = date.today().strftime("%b-%d-%Y")
    print("Today is {i}. starting new cycle...\n".format(i=date))
    path = os.getcwd()+"/files/" + date
    os.mkdir(path)
    Scraper(path)
    Editor(path)
