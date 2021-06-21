from models import Tournois, Joueur, Match, Ronde
#from views import View
#import views
from views import View
from tinydb import TinyDB, Query


db = TinyDB('db.json')

class Controller:
    """Classe controlleur"""
    #def __init__(self, nom, date, lieu):
    def __init__(self):
        tournois = View()
        # Créer le tournois
        tournois_info = tournois.input_data_tournois()
        tournois_model = Tournois(tournois_info["nom"], tournois_info["lieu"], tournois_info["date"])
        #print(tournois_model.lieu)
        print(tournois_model.__dict__)
        db.insert(tournois_model.__dict__)
        #joueur_info = tournois.innut_data_joueurs()

        # Créer les 8 joueurs
        joueur_info = tournois.input_data_joueurs()
        joueur_model = Joueur(joueur_info["nom"], joueur_info["prenom"], joueur_info["naissance"], joueur_info["sexe"])
        db.insert(joueur_model.__dict__)
        joueur_get = Query()
        joueur_get = db.get(joueur_get.nom == joueur_info["nom"])
        print(joueur_get)
        tournois_get = db.get(doc_id=1)
        print(tournois_get)
        print(tournois_get["joueurs"])
        print(joueur_get.doc_id)
        tournois_append_player = tournois_get["joueurs"]
        tournois_append_player.append(joueur_get.doc_id)
        print(tournois_append_player)
        #db.get(doc_id=1)["joueurs"].append(joueur_get.doc_id)
        #db.update({"joueurs": tournois_append_player}, tournois_get)
        tournois_get = Query()
        db.update({"joueurs": tournois_append_player}, tournois_get.nom == "tournois1")


    def creation_tournois(self, nom, lieu, date):
        titre = nom
        titre = Tournois(nom, lieu, date)
        #db.insert(titre)
        views.menu_principal()

