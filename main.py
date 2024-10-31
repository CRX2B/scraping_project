import requests
import csv
from bs4 import BeautifulSoup as BS

"""
product_page_url =
upc =
book_title =
price_including_tax =
price_excluding_tax =
number_available =
product_description =
category =
review_rating =
image_url =
"""


def extraction_data(elements):
    resultat = []
    for element in elements:
        resultat.append(element.string)
    return resultat
    



def ecriture_data(data, en_tete, table_info):
    with open(data, 'w') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(en_tete)
        writer.writerow(table_info)


def etl():
    url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
    reponse = requests.get(url)
    page = reponse.content
    soup = BS(page, "html.parser")
    
    table_info = soup.find_all("td")
    
    en_tete = ["Universal Product code", "Type", "Prix ttc", "Prix ht", "Qt dispo", "Nb d'avis"]
    table_info = extraction_data(table_info)
    
    ecriture_data("data/data.csv", en_tete, table_info)
    
    
etl()