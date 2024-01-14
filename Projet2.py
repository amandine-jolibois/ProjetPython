import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from tkinter import filedialog


class AnalyseurReferencementIHM:
    def __init__(self, root):
        self.root = root
        self.root.title("Analyseur de Référencement")

        # Variables pour stocker les entrées de l'utilisateur
        self.url_entree = tk.StringVar()
        self.mots_clefs_entree = tk.StringVar()

        # Première Interface
        self.creer_premiere_interface()

    def creer_premiere_interface(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widgets
        label_url = ttk.Label(frame, text="URL de la première page :")
        entry_url = ttk.Entry(frame, textvariable=self.url_entree, width=40)

        label_mots_clefs = ttk.Label(frame, text="Mots-clés (séparés par des virgules) :")
        entry_mots_clefs = ttk.Entry(frame, textvariable=self.mots_clefs_entree, width=40)

        bouton_analyser = ttk.Button(frame, text="Lancer l'analyse", command=self.analyser_page)

        # Mise en page des widgets
        label_url.grid(column=0, row=0, sticky=tk.W, pady=5)
        entry_url.grid(column=0, row=1, padx=10, pady=5, sticky=(tk.W, tk.E))
        label_mots_clefs.grid(column=0, row=2, sticky=tk.W, pady=5)
        entry_mots_clefs.grid(column=0, row=3, padx=10, pady=5, sticky=(tk.W, tk.E))
        bouton_analyser.grid(column=0, row=4, pady=10)

    def analyser_page(self):
        # Récupérer les données de l'interface utilisateur
        url = self.url_entree.get()
        mots_clefs = [mot.strip() for mot in self.mots_clefs_entree.get().split(',')]

        # Créer une instance de l'AnalyseurReferencement
        analyseur = AnalyseurReferencement(url, mots_clefs)

        # Effectuer l'analyse et passer à la deuxième interface
        resultats = analyseur.analyser_referencement()

        if resultats:
            # Afficher la deuxième interface avec les résultats
            self.creer_deuxieme_interface(resultats)
        else:
            messagebox.showerror("Erreur", "Impossible d'analyser la page. Vérifiez l'URL et réessayez.")

    def creer_deuxieme_interface(self, resultats):
        # Effacer la première interface
        for widget in self.root.winfo_children():
            widget.destroy()

        # Deuxième Interface
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Widgets pour afficher les résultats
        label_resultats = ttk.Label(frame, text="Résultats de l'analyse :")
        label_resultats.grid(column=0, row=0, pady=10)

        # Afficher les résultats
        for index, url_info in enumerate(resultats['informations']):
            ttk.Label(frame, text=f"{index + 1}. URL : {url_info['url']}").grid(column=0, row=index + 1, sticky=tk.W,
                                                                                pady=5)
            ttk.Label(frame, text=f"Liens Sortants : {url_info['liens_sortants']}").grid(column=0, row=index + 2,
                                                                                         sticky=tk.W, pady=5)
            ttk.Label(frame, text=f"Liens Internes : {url_info['liens_internes']}").grid(column=0, row=index + 3,
                                                                                         sticky=tk.W, pady=5)
            ttk.Label(frame, text=f"% de Balises Alt : {url_info['pourcentage_alt']}").grid(column=0, row=index + 4,
                                                                                            sticky=tk.W, pady=5)
            ttk.Label(frame, text=f"3 Premières Valeurs des Mots Clés Pertinents : {url_info['mots_clefs'][:3]}").grid(
                column=0, row=index + 5, sticky=tk.W, pady=5)

            mots_clefs_utilisateur = set(self.mots_clefs_entree.get().split(','))
            mots_clefs_resultat = set(url_info['mots_clefs'][:3])
            ttk.Label(frame,
                      text=f"Mots Clés Utilisateur parmi les 3 Premiers : {'Oui' if mots_clefs_utilisateur.intersection(mots_clefs_resultat) else 'Non'}").grid(
                column=0, row=index + 6, sticky=tk.W, pady=5)

        # Menu pour sauvegarder le rapport de référencement et pour mettre a jour la liste des mots
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        menu_rapport = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Sauvegarder le Rapport", menu=menu_rapport)
        menu_rapport.add_command(label="Dans un Fichier Texte", command=lambda: self.sauvegarder_rapport_texte(resultats))
        menu_mots_clefs = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Mots Clefs Parasites", menu=menu_mots_clefs)
        menu_mots_clefs.add_command(label="Mettre à Jour", command=self.mettre_a_jour_mots_clefs_parasites)

    def sauvegarder_rapport_texte(self, resultats):
        # Ouvrir une boîte de dialogue pour choisir l'emplacement du fichier
        fichier = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Fichiers texte", "*.txt")])

        if fichier:
            # Sauvegarder le rapport dans le fichier texte
            with open(fichier, 'w') as f:
                for index, url_info in enumerate(resultats['informations']):
                    f.write(f"{index + 1}. URL : {url_info['url']}\n")
                    f.write(f"Liens Sortants : {url_info['liens_sortants']}\n")
                    f.write(f"Liens Internes : {url_info['liens_internes']}\n")
                    f.write(f"% de Balises Alt : {url_info['pourcentage_alt']}\n")
                    f.write(f"3 Premières Valeurs des Mots Clés Pertinents : {url_info['mots_clefs'][:3]}\n")

                    mots_clefs_utilisateur = set(self.mots_clefs_entree.get().split(','))
                    mots_clefs_resultat = set(url_info['mots_clefs'][:3])
                    f.write(
                        f"Mots Clés Utilisateur parmi les 3 Premiers : {'Oui' if mots_clefs_utilisateur.intersection(mots_clefs_resultat) else 'Non'}\n\n")
            print("\n")

    def lire_mots_parasites(fichier_parasite):
        with open(fichier_parasite, 'r', encoding='utf-8') as file:
            reader = csv.reader(file, delimiter=';')
            [mot[0] for mot in reader]
            list = ['le', 'la', 'les', 'de', 'des', 'un', 'une', "l'", "d'", 'mes', 'ma', 'son', 'sa', "c'est", "s'est",
                    'ses', 'ces', 'sont', 'ça', 'ceci', 'est', 'pour']
            return list

    def mettre_a_jour_mots_clefs_parasites(self):
        # Ouvrir une boîte de dialogue pour choisir le fichier CSV des mots clefs parasites
        fichier_parasites = filedialog.askopenfilename(filetypes=[("Fichiers CSV", "*.csv")])

        if fichier_parasites:
            # Mettre à jour la liste des mots clefs parasites
            nouveaux_parasites = lire_mots_parasites(fichier_parasites)

            if nouveaux_parasites:
                # Utiliser les nouveaux parasites dans le reste du programme
                print("Mots Clefs Parasites mis à jour avec succès !")
            else:
                messagebox.showerror("Erreur", "Impossible de lire le fichier des mots clefs parasites.")


class AnalyseurReferencement:
    def __init__(self, url, mots_clefs):
        self.url = url
        self.mots_clefs = mots_clefs

    def analyser_referencement(self):
        try:
            html = self.recuperer_html_depuis_url(self.url)
            if not html:
                return None

            # Utilisez les fonctions précédemment définies pour analyser la page
            soup = BeautifulSoup(html, 'html.parser')
            urls = [a['href'] for a in soup.find_all('a', href=True)]

            # Exemple de résultats fictifs
            resultats = {
                'urls': urls,
                'informations': []
            }

            for url in resultats['urls']:
                liens_sortants = self.obtenir_liens_sortants(url)
                liens_internes = self.obtenir_liens_internes(url)
                pourcentage_alt = self.calculer_pourcentage_balises_alt(url)
                mots_clefs_pertinents = self.obtenir_mots_clefs_pertinents(url)

                information_url = {
                    'url': url,
                    'liens_sortants': liens_sortants,
                    'liens_internes': liens_internes,
                    'pourcentage_alt': pourcentage_alt,
                    'mots_clefs': mots_clefs_pertinents
                }

                resultats['informations'].append(information_url)

            return resultats
        except Exception as e:
            print(f"Une erreur s'est produite lors de l'analyse : {e}")
            return None

    def recuperer_html_depuis_url(self, url):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Gère les erreurs HTTP
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Une erreur s'est produite lors de la récupération de la page : {e}")
            return None

    def obtenir_liens_sortants(self, url):
        # Fonction à implémenter pour obtenir le nombre de liens sortants
        # Simulation avec une valeur aléatoire entre 1 et 10
        return 5

    def obtenir_liens_internes(self, url):
        # Fonction à implémenter pour obtenir le nombre de liens internes
        # Simulation avec une valeur aléatoire entre 1 et 10
        return 3

    def calculer_pourcentage_balises_alt(self, url):
        # Fonction à implémenter pour calculer le pourcentage de balises alt
        # Simulation avec une valeur aléatoire entre 50 et 100
        return 80

    def obtenir_mots_clefs_pertinents(self, url):
        # Fonction à implémenter pour obtenir les mots clés pertinents
        # Simulation avec une liste fixe
        return ['web', 'analyse', 'site', 'python', 'referencement']


# Lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalyseurReferencementIHM(root)
    root.mainloop()
