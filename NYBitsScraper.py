"""
@Author: Demerak
@Date: 05/05/2021
@Description: This is a short script that scrapes the nybits.com 
              website and gather information about apartments 
              for rent in NYC neighborhoods.
"""

## Core Pkgs
import time
import random 

## EDA Pkgs
import pandas as pd

## Web Scraping Pkgs
import requests
from bs4 import BeautifulSoup

## url_dict is a dictionary that contains all the main_urls
url_dict = {
   "Downtown Manhattan": "https://www.nybits.com/apartments/downtown_manhattan_apartment_buildings.html",
   "Midtown Manhattan" : "https://www.nybits.com/apartments/midtown_manhattan_apartment_buildings.html",
   "Uptown Manhattan" : "https://www.nybits.com/apartments/uptown_manhattan_apartment_buildings.html",
   "Upper Manhattan" : "https://www.nybits.com/apartments/upper_manhattan_apartment_buildings.html",
   #"Brooklyn" : "https://www.nybits.com/apartments/brooklyn_rental_buildings.html",
   #"Queens" : "https://www.nybits.com/apartments/queens_rental_buildings.html",
   #"Bronx" : "https://www.nybits.com/apartments/bronx_rental_buildings.html",
   "New Jersey" : "https://www.nybits.com/apartments/new_jersey_rental_buildings.html"
}

for neighberhood in url_dict:
    ## List of all the dataframes (each dataframe represent all the information about one apartment)
    dataframes_list = []

    ## Request the url from each NYC neighborhood 
    main_url = url_dict[neighberhood]
    page = requests.get(main_url)
    soup = BeautifulSoup(page.content, 'lxml')

    ## Find the list of all the apartment and iterate over all of them
    url_list = soup.find('ul', {'class': 'spacyul buildingul'})
    for litag in url_list.find_all('li'):
        ## dataframe_data --> data inside the dataframe, 
        ## dataframe_column --> names of all the columns 
        dataframe_data = [[]] 
        dataframe_column = []

        ## Not the best practice but wait a random amount of 
        ## seconds between those two numbers before extracting the
        ## data. This is necessary without it the server will detect the script
        time.sleep(random.randint(26,35))

        ## Get the apartment name and store it in both lists
        apt_name = litag.find('a').text
        dataframe_data[0].append(apt_name) 
        dataframe_column.append("Name")

        ## Get the link of the apartment webpage
        link = litag.find('a', href=True)
        print(link['href'])

        apt_page = requests.get(link['href'], timeout=(5,10))

        ## Get the html of the apartment webpage and find the summary table
        apt_soup = BeautifulSoup(apt_page.content, 'lxml')
        
        ## Find the apartment description and append data and column name to both list
        details = apt_soup.find("div", attrs={"class": "contentleft"})
        description = details.findAll('p')
        description = description[0].text.replace("\n", " ").strip()
        dataframe_data[0].append(description)
        dataframe_column.append("Description")

        ## The summary table contains essential most of the data available
        summary_data = apt_soup.find("table", attrs={"id": "summarytable"})
        for tr in summary_data.find_all("tr"):
            data_list = [] # Store that data into another list
            for td in tr.find_all("td"):
                data_list.append(td.text)  

            ## Append that data inside both 
            dataframe_data[0].append(data_list[1].replace("\n", " ").strip())
            dataframe_column.append(data_list[0])

        ## Putting all the data in a dataframe 
        df = pd.DataFrame(dataframe_data, columns = dataframe_column)
        ## Adding this dataframe of a single apartment to the dataframe of all the apartments
        dataframes_list.append(df)

        print(df)

        total_df = pd.concat(dataframes_list, axis=0, ignore_index=True)

        csv_name = neighberhood + ".csv"

        total_df.to_csv(csv_name)


   







        
