# Auteur : Louis Leclerc
# Date : 26/05/2020
# Description :
    # programme d'extraction des données d'entreprises brésiliennes (nom, activité, dirigeants, adresse...)
    # à partir de leur numéro d'enregistrement (le CNPJ)
    # et de l'API du registre fiscal fédéral (Receita Federal Web Services)
    # plus d'info sur https://www.receitaws.com.br/api

# A faire:
    # Retravailler la présentation des résultats dans la fonction finale
    # Ou faire un CSV en sortie

# Importation des modules requests, json, datetime et time, et localisation du fichier de CNPJ
import requests
import json
import datetime
import time
import os
os.chdir("/home/luchin/Documents/AmIntel/Communication/Blog/BDD Lava Jato")

# définition des valeurs invariables
my_file = "dados_amostra_CNPJ.csv"
url_receita = "https://www.receitaws.com.br/v1/cnpj/"
error_message = "Invalid CNPJ"
# token = {"Authorization":"token 607035d8e2dbd7e6b6b57234b3c905b44d6e73fd470e8d183993f0448c294dc2"}
    # nécessaire uniquement pour la connexion payante à l'API
# jour_j = datetime.date.today()-datetime.date(2020, 5, 26)
    # nécessaire uniquement pour la connexion payante à l'API
    # A retravailler pour avoir un nombre intégral de jours

# fonction qui retourne une URL valide quelque soit la composition du CNPJ
def correct_url(cnpj):
    if cnpj.isalnum()==False:
        new_cnpj= ""
        for i in cnpj:
            if i.isalnum() == True:
                new_cnpj += i
            else:
                pass
        if len(new_cnpj)==14:
            return url_receita + new_cnpj # + "/days/" + jour_j pour l'API commerciale
        else:
            return False
    elif cnpj.isalnum()==True and len(cnpj)==14:
        return url_receita + cnpj # + "/days/" + jour_j pour l'API commerciale
    else:
        return False

# fonction qui retourne une liste des données d'une entreprise à partir de son CNPJ
def scraping_page(url):
    if url == False:
        return error_message
    else:
        response = requests.get(url) #requests.get(url, headers=token) pour l'API commerciale
        page_content = response.text
        dct = json.loads(page_content)
        clefs= dct.keys()
        valeurs = dct.values()
        corpo_id = zip(clefs, valeurs)
        corpo_id = list(corpo_id)
        return corpo_id

# fonction qui ouvre un CSV de CNPJ (sans autre info) et retourne une liste de ces CNPJ
def file_cnpj(file):
    with open(file, encoding="utf-8") as f:
        res = f.read().splitlines()
    return res

# fonction générale qui scrap les infos à partir d'une liste de CNPJ
# en respectant la limite de 3 requêtes par minute de l'API publique
def scrap_list(cnpj_list):
    request_nb = 0
    res=[]
    for i in cnpj_list:
        if request_nb<3:
            res.append(scraping_page(correct_url(i)))
            request_nb+=1
        else:
            time.sleep(60)
            res.append(scraping_page(correct_url(i)))
            requetes = 1
    return res

print(scrap_list(file_cnpj(my_file)))