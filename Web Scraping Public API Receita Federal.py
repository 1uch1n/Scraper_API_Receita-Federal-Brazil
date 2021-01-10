# Author: Louis Leclerc
# Creation date: 26/05/2020
# Last update: 02/10/2020
# Description:
    # scraper of Brazilian companies data (name, activity, directors, address...)
    # input = tax registration number (CNPJ)
    # from the Federal Tax Registry's API (Receita Federal Web Services)
    # more info on https://www.receitaws.com.br/api

import requests
import json
import datetime
import time
import os

# defining file path
# os.chdir("/FILE/PATH")

# defining input file (has to be a one-column list of names in csv format)
# my_file = "FILE_NAME.csv"

url_receita = "https://www.receitaws.com.br/v1/cnpj/"
error_message = "Invalid CNPJ"

# token only necessary if using the paying services of the API (> 3 requests/s)
# token = {"Authorization":"token 607035d8e2dbd7e6b6b57234b3c905b44d6e73fd470e8d183993f0448c294dc2"}

# set d_day to today if using the paying API
# d_day = datetime.date.today()-datetime.date(YEAR, MONTH, DAY)

# function returning a valid API request URL from any CNPJ
def correct_url(cnpj):
    if cnpj.isalnum()==False:
        new_cnpj= ""
        for i in cnpj:
            if i.isalnum() == True:
                new_cnpj += i
            else:
                pass
        if len(new_cnpj)==14:
            return url_receita + new_cnpj # + "/days/" + d_day for the paying API
        else:
            return False
    elif cnpj.isalnum()==True and len(cnpj)==14:
        return url_receita + cnpj # + "/days/" + + d_day for the paying API
    else:
        return False

# function returning a list of the company's data from its CNPJ
def scraping_page(url):
    if url == False:
        return error_message
    else:
        response = requests.get(url) #requests.get(url, headers=token) for the paying API
        page_content = response.text
        dct = json.loads(page_content)
        clefs= dct.keys()
        valeurs = dct.values()
        corpo_id = zip(clefs, valeurs)
        corpo_id = list(corpo_id)
        return corpo_id

# function returning a CSV of CNPJs (without any other information) and returns a list of those CNPJs
def file_cnpj(file):
    with open(file, encoding="utf-8") as f:
        res = f.read().splitlines()
    return res

# general function scrapping data from a list of CNPJs
# respects the 3 request/sec limit of the free API
def scrap_list(cnpj_list):
    request_nb = 0
    res=[]
    for i in cnpj_list:
        if request_nb<3: #change max number of requests if using the paying API
            res.append(scraping_page(correct_url(i)))
            request_nb+=1
        else:
            time.sleep(60)
            res.append(scraping_page(correct_url(i)))
            requetes = 1
    return res

print(scrap_list(file_cnpj(my_file)))
