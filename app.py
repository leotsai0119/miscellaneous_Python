# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:40:49 2020

@author: Cai, Yun-Ting
"""
# %% import
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from random import randint
from tqdm import tqdm
from datetime import datetime
import time
import csv
import re

# %% set options for webdirver
options = Options()
options.add_argument("--disable-notifications")

# %% execute webdriver
print("Enter search string: ")
srch = input()
time.sleep(5)
# driverPath = "./geckodriver"
# driverPath = "~/anaconda3/envs/U/geckodriver"
firefox = webdriver.Firefox(options = options)
# open udndata
firefox.get("https://udndata.com/library")
time.sleep(5)

# find search string
search = firefox.find_element_by_id("SearchString")
search.send_keys(srch)
time.sleep(2)

# select drop down menu
drop = Select(firefox.find_element_by_id("s1"))
drop.select_by_value("-1")
time.sleep(3)

# click submit button
click_submit = firefox.find_element_by_class_name("btn")
click_submit.click()
time.sleep(5)

# select sorting
sort = Select(firefox.find_element_by_id("select"))
sort.select_by_value("0")
time.sleep(5)

# select sharepage
page = Select(firefox.find_element_by_id("sharepage"))
page.select_by_value("50")
time.sleep(5)

# %% parse number of pages and urls

# parse html
bs = BeautifulSoup(firefox.page_source, "html.parser")

# parse n page and define how many pages to parse
n = int(bs.select("div[class='message'] span")[1].text)
if n % 50 == 0:
    n_page = n // 50
elif n % 50 > 0:
    n_page = n // 50 + 1

# urls
u = bs.select("div[class='page-number page-number-web'] a")
links = [i.get("href") for i in u]
h = "https://udndata.com" + links[3].split("&", 2)[0] + "&"
t = "&" + links[3].split("&", 2)[2]
links = [h + "page=" + str(i) + t for i in range(2, n_page + 1)]

# %% processing

# make lists
date = []
paper =[]
page = []
classification = []
author = []

# =============================================================================
# first page
# =============================================================================

# parse html
bs = BeautifulSoup(firefox.page_source, "html.parser")

# titles
ttl = bs.select("h2[class='control-pic'] a")
# extract text and replace '\n'
t = [ttl[j].text.replace("\n", "") for j in range(len(ttl))]
title = [i.split(".")[1] for i in t]

# extract summary by CSS selector
smry = bs.select("p.summary")
summary = [smry[j].text for j in range(len(smry))]
# replace with re.sub
summary = [re.sub("\n|\t", " ", i) for i in summary]

# source
src = bs.select("span.source")
source = [j.text for j in src]
# date, paper, page, classification, and author
date = [j.split('．')[0] for j in source]
paper = [j.split('．')[1] for j in source]
page = [j.split('．')[2] for j in source]
classification = [j.split('．')[3] for j in source]
author = [j.split('．')[4] for j in source]

# sleep
time.sleep(randint(10, 60))

# =============================================================================
# # loop from page 2
# =============================================================================
for i in tqdm(range(n_page - 1), 
                      desc = "downloading", 
                      ncols = 80):
    firefox.get(links[i])
    time.sleep(randint(15, 30))
    # parse html
    bs = BeautifulSoup(firefox.page_source, "html.parser")
    # titles
    ttl = bs.select("h2[class='control-pic'] a")
    # extract text and replace '\n'
    t = [ttl[j].text.replace("\n", "") for j in range(len(ttl))]
    t = [j.split(".")[1] for j in t]
    for j in range(len(t)):
        title.append(t[j])
    # summary
    smry = bs.select("p.summary")
    smry = [smry[j].text for j in range(len(smry))]
    smry = [re.sub("\n|\t", " ", i) for i in smry]
    for j in range(len(smry)):
        summary.append(smry[j])
    # parse source
    src = bs.select("span.source")
    source = [j.text for j in src]
    for j in source:
        date.append(j.split('．')[0])
        paper.append(j.split('．')[1])
        page.append(j.split('．')[2])
        classification.append(j.split('．')[3])
        author.append(j.split('．')[4])
    # sleep for 3 mins after parsing 5 pages
    if i != 0 and (i - 1) != 0 and (i - 1) % 5 == 0:
        print("\npausing for 3 mins")
        time.sleep(180)
# result
result = []
dtime = datetime.strftime(datetime.now(), "%Y-%b-%d %H:%M:%S")

for j in range(len(title)):
    result.append([dtime, srch, title[j], date[j], 
                   summary[j], paper[j], page[j], 
                   classification[j], author[j]])
# header
header = ['timestamp', 'keyword', 'title', 'date', 
          'summary', 'paper', 'page', 
          'classification', 'author']
# write to csv
with open("./U.csv", 'w', newline='', encoding="utf-8-sig") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(result)        
print("Done! Check your folder for U.csv file.")
print("You may close the app.")
