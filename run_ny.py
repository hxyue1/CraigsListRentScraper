import RentScraper as RS
import pandas as pd
from datetime import datetime

today = datetime.today()
if today.weekday() == 0:
    try:
        old_df = pd.read_csv('NYRent.csv')
        old_data = True
    except:
        old_data = False
        print('No old data')
    result_df = RS.CraigsListToDF('https://newyork.craigslist.org/d/apts-housing-for-rent/search/apa', 120)
    if old_data == True:
        new_df = pd.concat([old_df, result_df])
        new_df.to_csv('NYRent.csv')
    elif old_data == False:
        result_df.to_csv('NYRent.csv')
