import requests
import csv
from bs4 import BeautifulSoup as BS
import os
from tqdm import tqdm
from datetime import datetime


#fonction pour récupérer les urls des catégories
def recup_url_cat(url_site):
    reponse = requests.get(url_site)
    page = reponse.content
    soup = BS(page, "html.parser")
    
    urls_categories = []
    
    categorie_container = soup.find("div", {"class": "side_categories"})
    liens_categories = categorie_container.find("ul").find("ul").find_all("a")
    #boucle pour récupérer les urls des catégories  
    for lien in liens_categories:
        url_categorie = f"http://books.toscrape.com/{lien.get('href')}"
        urls_categories.append(url_categorie)
    
    return urls_categories
 
#fonction pour récupérer les urls des livres    
def recup_url_livre(url_categorie):
    urls_livres = []
    page_suivante = True
    url_courante = url_categorie
    
    while page_suivante:
        reponse = requests.get(url_courante)
        soup = BS(reponse.content, "html.parser")
        
        livres = soup.find_all("article", {"class": "product_pod"})
        #boucle pour récupérer les urls des livres
        for livre in livres:
            href = livre.find('h3').find('a').get('href')
            url_livre = "http://books.toscrape.com/catalogue/" + href.split("/")[-2] + "/" + href.split("/")[-1] #ajout du chemin pour les urls des livres
            urls_livres.append(url_livre)
        #récupération de la page suivante, si elle existe
        next_button = soup.find("li", {"class": "next"})
        if next_button:
            next_page = next_button.find("a").get("href")
            url_courante = "/".join(url_categorie.split("/")[:-1]) + "/" + next_page
        else:
            page_suivante = False
    
    return urls_livres
    
#fonction pour écrire les données dans un fichier csv, et créer les dossiers et fichiers si nécessaire    
def ecriture_data(en_tete, info_book, categorie):
    if not os.path.exists("data"):
        os.mkdir("data")
        
    dossier_categorie = os.path.join("data", categorie)
    if not os.path.exists(dossier_categorie):
        os.mkdir(dossier_categorie)
    
    date_str = datetime.now().strftime("%d-%m-%Y")   #option pour ajouter la date dans le nom du fichier csv
    chemin_fichier = os.path.join(dossier_categorie, f"{categorie}_{date_str}.csv") #convention de nommage du fichier csv, catégorie + date
    
    fichier_existe = os.path.exists(chemin_fichier)
    #ouverture du fichier csv en mode append, si le fichier n'existe pas, il sera créé
    with open(chemin_fichier, 'a', newline='', encoding='utf-8') as fichier_csv:
        writer = csv.writer(fichier_csv, delimiter=',', lineterminator='\n')
        if not fichier_existe:
            writer.writerow(en_tete)
        writer.writerow(info_book)
    
    

#fonction pour récupérer les données des livres 
def data_book(urls_livres):
    reponse = requests.get(urls_livres)
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
    
    if not os.path.exists("data/images_data"):
        os.makedirs("data/images_data")
    #récupération de l'url de l'image et du nom de l'image
    image = image_url_complete
    nom_image = upc #nom de l'image = UPC du livre car il est unique
    chemin_image = os.path.join("data/images_data", f"{nom_image}.jpg")
    #téléchargement de l'image si elle n'existe pas déjà
    if not os.path.exists(chemin_image):
        image_data = requests.get(image).content
        with open(chemin_image, "wb") as fichier_image:
            fichier_image.write(image_data)
        print(f"Image {nom_image}.jpg téléchargée") #affichage de la progression du téléchargement
    
    
    #en-tête du fichier csv     
    en_tete = ["Url livre ", "Titre ", "UPC ", "Prix HT ", "Prix TTC ", "Nb dispo ", "Description ", "Note ", "Catégorie ", "Url image "]
    #données à écrire dans le fichier csv
    info_book = [url_book, titre_book, upc, prix_ht, prix_ttc, nb_dispo, description, review_rating, categorie, image_url_complete]
    
    #appel de la fonction pour écrire les données dans le fichier csv
    ecriture_data(en_tete, info_book, categorie)


        
#programme principal

#récupération des urls des catégories   
urls_categories = recup_url_cat("http://books.toscrape.com/")
#appel de la barre de progression
general_progress_bar = tqdm(total=len(urls_categories), desc="Running program") 
#boucle pour récupérer les urls des livres pour chaque catégorie    
for url_categorie in urls_categories:
    urls_livres = recup_url_livre(url_categorie)
    general_progress_bar.update(1) #mise à jour de la barre de progression
    #boucle pour récupérer les données des livres pour chaque url
    for url_livre in urls_livres:
        data_book(url_livre)
    

general_progress_bar.close() #fermeture de la barre de progression  