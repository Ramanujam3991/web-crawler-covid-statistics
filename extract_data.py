from html.parser import HTMLParser
from urllib import parse
import pandas as pd
import requests
import re
import json
from pymongo_integration import *



def crawl_data_from_link(url):
    #skip population data?
    is_skip_population = True
    if is_skip_population and 'coronavirus' not in url:
        return
    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    #url = 'https://www.worldometers.info/coronavirus/#countries'
    try:
        html_source = requests.get(url).text
        html_source = re.sub(r'<.*?>', lambda g: g.group(0).upper(), html_source)
    except:
        print('invalid page schema',url)
        return
    print('url:::',url)
    try:
        dataframe = pd.read_html(html_source)
    except:
        print('no tables in this page',url)
        return
    print(dataframe)
    dictArr=list(dataframe[0].T.to_dict().values())
    print(':::',dictArr)
    #insert the data
    if '#countries' in url:
        # insert the main data
        insertIntoDb(dictArr)
        print('Found countries:::')
    elif '/country/' in url:
        #insert the trivial contry level data
        table_name = url[url.find('country/')+8:len(url)-1]
        print('table_name**',table_name)
        insertIntoDb(dictArr, table_name)

    #file.close()



