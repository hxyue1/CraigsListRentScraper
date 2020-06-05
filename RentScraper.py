#Importing packages
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import re

#For graphing
import seaborn as sns
import matplotlib.pyplot as plt
sns.set(style="ticks", color_codes=True)

def ContentParser(content):
    """Parses results to obtain price, number of bedrooms, area and location information from html tags.
        
    Args:
        content (bs4.tag): The beautiful soup result from parsing the webpage.
    Returns:
        [[]].
    """

    results_list = []    
    #Looping through each listing
    for li_tag in content.find_all('li', {'class':'result-row'}):

        #Getting price
        price = li_tag.find('span', {'class':'result-price'}).getText()
        price = int(re.search('[0-9]+',price)[0])

        #Checking if num bedrooms and/or area is given
        try:
            #Getting number of bedrooms and area
            br_area= li_tag.find('span',{'class':'housing'}).getText()
            br_area_bool = True
        except:
            br_area = None
            br = np.nan
            area = np.nan

        #For cases where bedrooms and/or area are given
        if br_area:
            
            #For listings which do not have bedrooms
            try:
                br_area = br_area.replace('\n','').replace(' ','')
                br = re.findall('[\w\s]+', br_area)[0]
                br = int(br.replace('br', ''))
            except:
                br=np.nan
            
            #For listings which do not have area
            try:
                area = re.findall('[\w\s]+', br_area)[1]
                area = int(area.replace('ft2',''))
            except:
                area = np.nan


        #Not all postings have district tags          
        try:
            district = li_tag.find('span', {'class':'result-hood'}).getText()#Getting district
            district = district.replace('(','').replace(')','').strip()
        except:
            district = np.nan
        
        #Appending each result
        results_list.append([price, br, area, district])
        
    return(results_list)

def CraigsListToDF(urlpage, num_pages=120):
    """Takes input webpage and converts listing data to a dataframe
    
    Args:
        urlpage (str): The website CraigsList url to be scraped.
    Returns:
        pd.DataFrame: DataFrame of results.
    
    """
    request = Request(urlpage)
    webpage = urlopen(urlpage).read()
    soup = BeautifulSoup(webpage, 'lxml')

    #Calculating number of pages to loop through
    total_results = int(soup.find('span', {'class': 'totalcount'}).getText())
    num_results_per_page = num_pages#<--- Check this
    num_pages = int(np.floor(total_results/num_results_per_page))

    start_pos = 0
    results_list = []

    #Looping through each page
    for page_count in range(0,num_pages):

        #Updating URL
        start_string = '?s='+ str(start_pos)
        new_url= urlpage + start_string

        #Getting and parsing page
        request = Request(new_url)
        webpage = urlopen(new_url).read()
        soup = BeautifulSoup(webpage, 'lxml')
        content = soup.find('ul', {'class':'rows'})

        #Running content parser
        temp_results_list = ContentParser(content)
        results_list.extend(temp_results_list)

        #Updating position counter
        start_pos += num_results_per_page
        print(page_count)
        
    results_df = pd.DataFrame(results_list, columns = ['Price', 'Bedrooms', 'Area', 'Location'])
    
    return(results_df)