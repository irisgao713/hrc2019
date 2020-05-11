import pandas as pd
from email import notify

def check_rows(filename):
    '''
    Check if the CSV file contains more than 100 rows
    '''

    fold = "../results/parsed_raw/"

    apa = pd.read_csv(fold + "apa/" + filename)
    roo = pd.read_csv(fold + "roo/" + filename)
    if apa.shape[0] < 100 or roo.shape[0] < 100:
        notify("contamination")