import requests
import csv
from bs4 import BeautifulSoup as BS
import os
from tqdm import tqdm



def recup_url_cat(url_site):
    reponse = requests.get(url_site)
    print(f"Status code pour {url_site}: {reponse.status_code}")
    page = reponse.content
    soup = BS(page, "html.parser")
    
    urls_categories = []
    
    categorie_container = soup.find("div", {"class": "side_categories"})
    liens_categories = categorie_container.find("ul").find("ul").find_all("a")
    
    for lien in liens_categories:
        url_categorie = f"http://books.toscrape.com/{lien.get('href')}"
        urls_categories.append(url_categorie)
    
    return urls_categories
    
def recup_url_livre(url_categorie):
    urls_livres = []
    page_suivante = True
    url_courante = url_categorie
    
    while page_suivante:
        reponse = requests.get(url_courante)
        soup = BS(reponse.content, "html.parser")
        
        livres = soup.find_all("article", {"class": "product_pod"})
        
        for livre in livres:
            href = livre.find('h3').find('a').get('href')
            url_livre = "http://books.toscrape.com/catalogue/" + href.split("/")[-2] + "/" + href.split("/")[-1]
            print(f"URL livre trouvée: {url_livre}")  # Debug
            urls_livres.append(url_livre)
            
        next_button = soup.find("li", {"class": "next"})
        if next_button:
            next_page = next_button.find("a").get("href")
            url_courante = "/".join(url_categorie.split("/")[:-1]) + "/" + next_page
        else:
            page_suivante = False
    
    return urls_livres
    

def ecriture_data(en_tete, info_book, categorie):
    if not os.path.exists("data"):
        os.mkdir("data")
        
    dossier_categorie = os.path.join("data", categorie)
    if not os.path.exists(dossier_categorie):
        os.mkdir(dossier_categorie)
        
    chemin_fichier = os.path.join(dossier_categorie, f"{categorie}.csv")
    
    fichier_existe = os.path.exists(chemin_fichier)
    
    with open(chemin_fichier, 'a', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',', lineterminator='\n')
        if not fichier_existe:
            writer.writerow(en_tete)
        writer.writerow(info_book)
    
    


def data_book(urls_livres):
    reponse = requests.get(urls_livres)
    print(f"Status code pour {urls_livres}: {reponse.status_code}")
    page = reponse.content
    soup = BS(page, "html.parser")
    
    url_book = urls_livres
    titre_book = soup.find("h1").get_text()
    upc = soup.find("table", {"class": "table table-striped"}).find_all("td")[0].get_text()
    prix_ht = soup.find("table", {"class": "table table-striped"}).find_all("td")[2].get_text()
    prix_ttc = soup.find("table", {"class": "table table-striped"}).find_all("td")[3].get_text()
    nb_dispo = soup.find("table", {"class": "table table-striped"}).find_all("td")[5].get_text()
    description = soup.find("h2").find_next("p").get_text()
    review_rating = soup.find("table", {"class": "table table-striped"}).find_all("td")[6].get_text()
    categorie = soup.find("ul", {"class":"breadcrumb"}).find_all("a")[-1].get_text()
    image_url = soup.find("div", {"class": "item active"}).find("img").get("src")
    image_url_complete = f"http://books.toscrape.com/{image_url}" 
      
    en_tete = ["Url livre ", "Titre ", "UPC ", "Prix HT ", "Prix TTC ", "Nb dispo ", "Description ", "Note ", "Catégorie ", "Url image "]
    info_book = [url_book, titre_book, upc, prix_ht, prix_ttc, nb_dispo, description, review_rating, categorie, image_url_complete]
    
    ecriture_data(en_tete, info_book, categorie)

    




urls_categories = recup_url_cat("http://books.toscrape.com/")
general_progress_bar = tqdm(total=len(urls_categories), desc="Running program") 

for url_categorie in urls_categories:
    urls_livres = recup_url_livre(url_categorie)
    general_progress_bar.update(1)
    for url_livre in urls_livres:
        data_book(url_livre)
    general_progress_bar.update(1)

general_progress_bar.close()