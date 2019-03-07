# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 19:56:38 2019

@author: try94
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from bs4 import BeautifulSoup 
import pandas as pd
import time


vol = 65
issue = 1

start = time.time()
url = "https://pubsonline.informs.org/toc/mnsc/%s/%s"%(vol,issue)
r = requests.get(url)
soup = BeautifulSoup(r.text,"html.parser")
soup_abstact_list = soup.find_all('span',class_='hlFld-Abstract')
soup_title_list = soup.find_all('h5',class_='issue-item__title')
paper_info=[]
for i in range(len(soup_title_list)):
    paper = soup_title_list[i]
    paper_title = paper.text
    paper_url = paper.a['href']
    url = 'https://pubsonline.informs.org'+paper_url
    time.sleep(5)
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    abstract = soup.find('div',class_='hlFld-Abstract')
    abstract_text = abstract.find('p').text
    try:
        depart = abstract.text.split()[-1]
    except:
        depart = 'None'    
    paper_abstract = soup_abstact_list[i-1].text
    paper_info.append([depart,paper_title,paper_url,abstract_text])

labels=['department','title','url','abstract']
df = pd.DataFrame.from_records(paper_info, columns=labels)
now = time.time()
print('Finished, and %.2f s elapse'%(now-start))
df.to_csv('mnsc_%s_%s.csv'%(vol,issue),encoding('utf-8'))