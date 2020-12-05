import os
from datetime import datetime
# os.chdir('data')


def log_to_file(result_txt):
    now = datetime.now()
    # open a file to append
    outF = open("data/results.txt", "a")
    outF.write('\nNew analysis:' + "\n")
    outF.write(now.strftime("%d/%m/%Y %H:%M:%S") + "\n")

    for result in result_txt:
        outF.write(result)

