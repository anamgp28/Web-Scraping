import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

from icecream import ic

url = 'https://www.freepatentsonline.com'
url_page = 'https://www.freepatentsonline.com/result.html?p='
url_search = '&srch=xprtsrch&query_txt=ALL%28health+services%29+AND+%28ALL%28customer+servicies%29+OR+%28omnicanal%29+OR+ALL%28analitics%29%29&uspat=on&usapp=on&eupat=on&jp=on&pct=on&depat=on&date_range=last20&stemming=on&sort=relevance'

#pages = 15

def extract_links(pages):
    links = []
    for page in range(1,pages+1):
        r = requests.get(url_page + str(page) + url_search)
        soup = BeautifulSoup(r.content,"lxml")
        rows = soup.find_all('tr')
        rows = rows[2:-2]
        for row in rows:
            links.append(row.find('a')['href'])
    return links

def extract_patents(pages):
    links = extract_links(pages)
    table = []
    for link in links:
        r = requests.get(url + link)
        soup = BeautifulSoup(r.content,"lxml")
        
        dict = {}
        containers = soup.find_all('div', attrs={'class':'disp_doc2'})
        ic(containers)
        for container in containers:
            title = container.find('div', attrs={'class':'disp_elm_title'})
            value = container.find('div', attrs={'class':'disp_elm_text'})
            
            try:
                dict[title.getText().strip().replace(':', '')] = re.sub(' +', ' ', value.getText().strip())
                if 'International Classes' in dict.keys():
                    dict['International Classes'] = dict['International Classes'].replace(';', '\n')
            except:
                continue
        #ic(bool(dict))
        del dict['']
        table.append(dict)
    df = pd.DataFrame(table)
    ic(df)
    
          
extract_patents(2)