#Bonjour ! 
#J'espère que vous pourrez m'aider à créer un système de surveillance des prix. Pour élaborer une version bêta du système limitée à un seul revendeur, 
#Books to Scrape, le mieux est probablement de suivre les étapes que j'ai définies dans le fichier des exigences ci-joint.
#Lorsque vous aurez terminé, envoyez-moi un lien vers votre repository GitHub et un fichier compressé des données qu'il génère. Avec le code, 
#le repo doit inclure un requirements.txt et un README.md complété afin que j’exécute le code avec succès et produise des données ! 
#Le repo ne doit pas inclure les données et images extraites.
#Après avoir terminé le code, envoyez-moi un fichier ZIP des données générées. 
#Assurez-vous d'organiser toutes les données et images que vous avez extraites de manière simple.
#Pouvez-vous également m'envoyer un mail décrivant comment nous pourrions utiliser le code pour établir un pipeline ETL 
#(de l'anglais Extract, Transform, Load, signifiant extraire, transformer, charger) ? Cela sera utile pour le montrer à mon responsable.
#Cordialement,
#Sam
#Responsable d'équipe
#Books Online 

import requests

from bs4 import BeautifulSoup as BS


url = "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"
page = requests.get(url)
soup = BS(page.content, "html.parser")
titre_h1 = soup.find("h1")


print(titre_h1)

