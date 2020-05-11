import pandas as pd
from email import notify

def check_rows(filename):
    '''
    Check if the CSV file contains more than 100 rows
    '''
    df = pd.read_csv(filename)
    if df.shape[0] < 100:
        notify("contamination")