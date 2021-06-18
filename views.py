from models import Tournois, Joueur, Match, Ronde
from tinydb import TinyDB, Query
from controllers import *
#from controllers import Controller

"""type your views here"""

db = TinyDB('db.json')
list_joueurs = []
list_tournois = []

# Dictionnaires à sérialiser et à entrer dans la db, permettant de prendre les informations relatives au tournois
dict_tournois = {}
dict_joueurs = {}
tuple_match = ()


class View:
    def input_data_tournois(self):
        """Prend les données des tournois et les envoie au controleur"""
        nom = input("entrez le nom du tournois: ")
        lieu = input("entrez le lieu du tournois: ")
        date = input("entrez la date du tournois: ")
        return (nom, lieu, date)


def menu_principal():
    """Génère le menu principal"""
    print("Voici le menu principal:")
    print("- Taper \"tournois\" pour créer un tournois")
    print("- Taper \"joueur\" pour créer un joueur")
    print("- Taper \"lancer\" pour lancer le tournois")
    print("- Taper \"liste joueurs\" pour consulter la liste des joueurs")
    print("- Taper \"info tournois\" pour consulter les informations du tournois")
    selection = input("selection: ")
    if selection == "tournois":
        creer_tournois()
    elif selection == "joueur":
        creer_joueur()
    elif selection == "lancer":
        pass
    elif selection == "liste joueurs":
        liste_joueurs()
    # Relance une séléction de menus à l'utilisateur
    elif selection == "info tournois":
        info_tournois()
    else:
        menu_principal()



def creer_tournois():
    """DEPRECIE -- Génère les tournois"""
    nom = input("entrez le nom du tournois: ")
    lieu = input("entrez le lieu du tournois: ")
    date = input("entrez la date du tournois: ")
    tournoisN = Tournois(nom, lieu, date)
    #list_tournois.append(tournoisN)
    db.insert(tournoisN)
    menu_principal()


def creer_joueur():
    """Créer le profil d'un joueur"""
    nom = input("entrez le nom de famille: ")
    prenom = input("entrez le prénom: ")
    naissance = input("entrez la date de naissance: ")
    sexe = input("entrez le sexe: ")
    joueur1 = Joueur(nom, prenom, naissance, sexe)
    #joueur1 = Joueur("bodin", "tiago", "02/10/1996", "homme", 0)
    print(joueur1)
    list_joueurs.append(joueur1)
    print("\n")
    menu_principal()


def liste_joueurs():
    """Affiche la liste des joueurs"""
    for i in list_joueurs:
        print(f"{i.nom} - {i.prenom} - {i.naissance} - {i.sexe} - {i.classement} - {i.point}")
    print("\n")
    menu_principal()


def creer_match():
    """Création de match"""
    Match()
    pass


def attribue_point(nom, issue_match):
    """Attribue les points après un match"""
    if issue_match == "match_win":
        Joueur.point += 1
    if issue_match == "match_nul":
        Joueur.point += 0.5


def generation_paires():
    """Génère les paires selon le système de tournois suisse"""
    #for i in list_joueurs:
        #i.points
    pass


def rapport():
    """Affiche le rapport final"""
    pass

def info_tournois():
    """Retourne les informations relatives au tournois"""
    print(f"{list_tournois[0].nom} - {list_tournois[0].lieu} - {list_tournois[0].date} - {list_tournois[0].nb_tours}")
    menu_principal()

#menu_principal()
