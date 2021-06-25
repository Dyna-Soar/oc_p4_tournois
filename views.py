from models import Tournois, Joueur, Match, Ronde
from tinydb import TinyDB, Query
from controllers import *

"""type your views here"""

db = TinyDB('db.json')
db_tournois = db.table('table_tournois')
db_joueurs = db.table('table_joueurs')
db_matchs = db.table('table_matchs')

class View:
    def input_data_tournois(self):
        """Prend les données des tournois et les envoie au controleur"""
        nom = input("entrez le nom du tournois: ")
        lieu = input("entrez le lieu du tournois: ")
        date = input("entrez la date du tournois: ")
        data_tournois = {"nom": nom, "lieu": lieu, "date": date}
        return data_tournois

    def input_data_joueurs(self):
        """Prend les données des tournois et les envoie au controleur"""
        nom = input("entrez le nom du joueur: ")
        prenom = input("entrez le prénom du joueur: ")
        naissance = input("entrez la date de naissance du joueur: ")
        sexe = input("entrez le sexe du joueur: ")
        data_joueur = {"nom": nom, "prenom": prenom, "naissance": naissance, "sexe": sexe}
        return data_joueur

    def menu_principal(self):
        """Génère le menu principal"""
        print("- Taper \"1\" pour lancer le tournois")
        print("- Taper \"2\" pour passer au match suivant")
        print("- Taper \"3\" pour modifier le classement des joueurs")
        selection = input("selection: ")
        return selection

    def input_resultat_match(self, joueur1, joueur2):
        """Demande à l'utilisateur le résultat d'un match et retourne ce résultat"""
        print(f"joueur1: {joueur1}")
        print(f"joueur2: {joueur2}")
        resultat = None
        while resultat != "1" and resultat != "2" and resultat != "0":
            resultat = input("Tapez 1 si le joueur1 a gagné, 2 si le joueur 2 a gagné, ou 0 si match nul: ")
        return resultat

    def input_classement(self, all_players):
        list_classement = []
        for i in range(len(all_players)):
            dict_classement = {}
            name_player = all_players[i]["nom"]
            classement_player = input(f"Classement de {name_player}: ")
            dict_classement["name"] = name_player
            dict_classement["ranking"] = classement_player
            list_classement.append(dict_classement)
        return list_classement

    def rapport(self, tournois, joueurs, matchs):
        print("")
        print("RAPPORT DU TOURNOIS")
        print(f"Nom du tournois: {tournois[0]['nom']} - Lieu: {tournois[0]['lieu']} - Date: {tournois[0]['date']} - Description: {tournois[0]['description']}")
        print("")
        print("LISTE DES JOUEURS:")
        for i in range(len(joueurs)):
            print(f"{joueurs[i]['nom']} - {joueurs[i]['prenom']} - {joueurs[i]['naissance']} - Classement: {joueurs[i]['classement']} - Points: {joueurs[i]['point']}")
        for i in range(len(matchs)):
            View.round_display(self, i)
            joueur1 = db_joueurs.get(doc_id=matchs[i]['joueur1'])
            joueur1_nom = joueur1["nom"]
            joueur1_prenom = joueur1["prenom"]
            joueur2 = db_joueurs.get(doc_id=matchs[i]['joueur2'])
            joueur2_nom = joueur2["nom"]
            joueur2_prenom = joueur2["prenom"]
            if matchs[i]["resultat"] == "1":
                print(f"{joueur1_nom} {joueur1_prenom} a gagné contre {joueur2_nom} {joueur2_prenom}")
            elif matchs[i]["resultat"] == "2":
                print(f"{joueur2_nom} {joueur2_prenom} a gagné contre {joueur1_nom} {joueur1_prenom}")
            else:
                print(f"Match Nul entre {joueur1_nom} {joueur1_prenom} et {joueur2_nom} {joueur2_prenom}")

    def round_display(self, i):
        if i == 0:
            print("")
            print("ROUND 1")
        if i == 4:
            print("")
            print("ROUND 2")
        if i == 8:
            print("")
            print("ROUND 3")
        if i == 12:
            print("")
            print("ROUND 4")