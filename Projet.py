from collections import Counter
import re
import csv
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests

#Compte les mots d'un test
def nb_occurrence(texte):
    mots = re.findall(r'\b\w+\b', texte.lower())
    occurrences = Counter(mots)
    return occurrences.most_common()


#Test fonction
text = "Bonjour le monsieur, bonjour la madame."
print("Test fonction 1 : ", nb_occurrence(text))

#Déclaration des listes :
listeOccurence = [('un', 2), ('exemple', 2), ('pour', 2), ('la', 2), ('fonction', 2), ('ceci', 1), ('est', 1), ('de', 1), ('texte', 1), ('simple', 1), ('illustrer', 1)]
listeParasite = ['le', 'la', 'les', 'de', 'des', 'un', 'une', "l'", "d'", 'mes', 'ma', 'son', 'sa', "c'est", "s'est", 'ses', 'ces', 'sont', 'ça', 'ceci', 'est', 'pour']


#Compte le nombre de mots sans les mots parasites.
def filtrer_mots_parasites(UnelisteOccurence, UnelisteParasite):
    if UnelisteOccurence is None or UnelisteParasite is None:
        return "Les listes ne peuvent pas être vides"
    # Filtrer les mots parasites de la liste d'occurrences
    else:
        return [(mot, occ) for mot, occ in UnelisteOccurence if mot not in UnelisteParasite]

#Test fonction
print("Test fonction 2 : ", filtrer_mots_parasites(listeOccurence, listeParasite))

#Fichier parasite
def lire_mots_parasites(fichier_parasite):
    with open(fichier_parasite, 'r', encoding='utf-8') as file:
        reader = csv.reader(file, delimiter=';')
        [mot[0] for mot in reader]
        list = ['le', 'la', 'les', 'de', 'des', 'un', 'une', "l'", "d'", 'mes', 'ma', 'son', 'sa', "c'est", "s'est", 'ses', 'ces', 'sont', 'ça', 'ceci', 'est', 'pour']
        return list

#Test fonction
print("Test fonction 3 : ", lire_mots_parasites("mots_parasites.csv"))

#text est dans une variable 'text'
resultats_etape1 = nb_occurrence(text)

#fichier mots_parasites.cs est présent dans le même répertoire
mots_parasites = lire_mots_parasites('mots_parasites.csv')

resultats_etape2 = filtrer_mots_parasites(resultats_etape1, mots_parasites)
print(resultats_etape2[:3])

#Retire les balises HTML
def supprimer_balises_html(texte_html):
    soup = BeautifulSoup(texte_html, 'html.parser')
    return soup.get_text()

#Test fonction
html = "<h1>L'ennui mortel</h1> <p>par Chris Mills</p> <h2>Chapitre I : La nuit noire</h2> <p> Il faisait nuit noire. </p>"
print("Test fonction 5 : ", supprimer_balises_html(html))

#Retourne la liste des valeurs associées aux balises
def valeurs_attribut_balise(texte, balise, attribut):
    soup = BeautifulSoup(texte, 'html.parser')
    balises = soup.find_all(balise)
    return [tag.get(attribut) for tag in balises if tag.has_attr(attribut)]

html2 = """
<html>
    <body>
        <img src="image1.jpg" alt="Image 1">
        <img src="image2.jpg" alt="Image 2">
        <img src="image3.jpg" alt="Image 3">
    </body>
</html>
"""

#Test fonction
print("Test fonction 6 : ",valeurs_attribut_balise(html2, 'img', 'alt'))


#Pour récupérer les valeurs des attributs alt des balises img
print(valeurs_attribut_balise(html2, 'img', 'alt'))

html3 = """
<a href="https://example.com">Website</a></li>
  <li><a href="mailto:m.bluth@example.com">Email</a></li>
  <li><a href="tel:+123456789">Phone</a>
"""

#Pour récupérer tous les href des balises a
print(valeurs_attribut_balise(html3, 'a', 'href'))


#Extrait nom de domaine
def extraire_nom_domaine(url):
    return urlparse(url).netloc

url = "https://esiee-it.blackboard.com/ultra/courses/_101859_1/outline/edit/document/_1173113_1?courseId=_101859_1&view=content"

#Test fonction
print("Test fonction 8 : ", extraire_nom_domaine(url))

#Fonction 9
def filtrer_urls_par_domaine(domaine, urls):
    urls_domaine = [url for url in urls if extraire_nom_domaine(url) == domaine]
    urls_autres = [url for url in urls if extraire_nom_domaine(url) != domaine]
    return urls_domaine, urls_autres

# Exemple d'utilisation avec des URLs fictives
domaine_cible = "example.com"
liste_urls = [
    "http://example.com/page1",
    "http://example.com/page2",
    "http://subdomain.example.com/page3",
    "http://otherdomain.com/page4"
]

#Test fonction
print("Test fonction 9 : ", filtrer_urls_par_domaine(domaine_cible, liste_urls))


#Fonction 10
def obtenir_texte_html(url):
    response = requests.get(url)
    return response.text

# Exemple d'utilisation avec une URL fictive
url_test = "https://www.example.com"

# Appel de la fonction pour récupérer le texte HTML depuis l'URL
html_page = obtenir_texte_html(url_test)

# Affichage du texte HTML (les premiers 500 caractères pour éviter un affichage trop long)
if html_page:
    print("Texte HTML de la page (les premiers 500 caractères) :\n", html_page[:500])
else:
    print("Échec de la récupération du texte HTML.")


#URL test : https://www.example.com


# Assume que l'URL est fournie par l'utilisateur
url_auditer = input("Veuillez entrer l'URL à auditer : ")

texte_html_auditer = obtenir_texte_html(url_auditer)

# Effectuer l'analyse
resultats_etape1_auditer = nb_occurrence(texte_html_auditer)
resultats_etape2_auditer = filtrer_mots_parasites(resultats_etape1_auditer, mots_parasites)
nombre_liens_entrants = len(valeurs_attribut_balise(texte_html_auditer, 'a', 'href'))
nombre_liens_sortants = len(valeurs_attribut_balise(texte_html_auditer, 'a', 'href'))
presence_balises_alt = len(valeurs_attribut_balise(texte_html_auditer, 'img', 'alt')) > 0

# Afficher les résultats
print("Mots-clés avec les 3 premières occurrences:", resultats_etape2_auditer[:3])
print("Nombre de liens entrants:", nombre_liens_entrants)
print("Nombre de liens sortants:", nombre_liens_sortants)
print("Présence de balises alt:", presence_balises_alt)
