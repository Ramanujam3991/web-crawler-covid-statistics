from html.parser import HTMLParser
from urllib import parse
import pandas as pd
import requests
import re
import json
from web_crawler.pymongo_integration import *


def crawl_data_from_link(url):
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = 'https://www.worldometers.info/coronavirus/#countries'
    html_source = requests.get(url).text
    html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), html_source)
    print('hi::::')
    dataframe = pd.read_html(html_source)
    print(dataframe)
    # file = open('covid/data.txt', 'w')
    dictArr = []
    val = 0
    countryLst= dataframe[0]['Country,Other'].to_dict().values()
    TotalCasesLst = dataframe[0]['TotalCases'].to_dict().values()
    NewCasesLst =  dataframe[0]['NewCases'].to_dict().values()
    TotalDeaths=dataframe[0]['TotalDeaths'].to_dict().values()
    NewDeaths=dataframe[0]['TotalDeaths'].to_dict().values()
    TotalRecovered = dataframe[0]['TotalRecovered'].to_dict().values()
    ActiveCases = dataframe[0]['ActiveCases'].to_dict().values()

    #print('countryLst::',dataframe[0].T.to_dict().values())
    print('ActiveCases::', ActiveCases)
    dictArr=list(dataframe[0].T.to_dict().values())
    print(':::',dictArr)
    insertIntoDb(dictArr)
    #file.close()



