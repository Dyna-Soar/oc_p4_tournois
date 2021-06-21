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
        #joueur_info = tournois.input_data_joueurs()
        #joueur_model = Joueur(joueur_info["nom"], joueur_info["prenom"], joueur_info["naissance"], joueur_info["sexe"])
        #db.insert(joueur_model.__dict__)
        #joueur_get = Query()
        #joueur_get = db.get(joueur_get.nom == joueur_info["nom"])
        #tournois_get = db.get(doc_id=1)
        #tournois_append_player = tournois_get["joueurs"]
        #tournois_append_player.append(joueur_get.doc_id)
        #tournois_get = Query()
        #db.update({"joueurs": tournois_append_player}, tournois_get.nom == tournois_info["nom"])
        Controller.creation_joueurs(self, tournois, tournois_info)

    def creation_joueurs(self, tournois, tournois_info):
        # Prompt the user for player input via a function in the views.py
        joueur_info = tournois.input_data_joueurs()
        # Create an instance of player, called joueur_model, with the return value of joueur_info
        joueur_model = Joueur(joueur_info["nom"], joueur_info["prenom"], joueur_info["naissance"], joueur_info["sexe"])
        # Store the instance created, called joueur_model, in the db
        db.insert(joueur_model.__dict__)
        # Call the query() default function, in joueur_get, in order to form queries
        joueur_get = Query()
        # Query the current player by its name, which is an attribute stored in joueur_info
        joueur_get = db.get(joueur_get.nom == joueur_info["nom"])
        # Get the current tournois info by id, which now is arbitrary 1
        tournois_get = db.get(doc_id=1)
        # Store the list of players from the current tournois, in the variable tournois_append_player
        tournois_append_player = tournois_get["joueurs"]
        # Append the id indice of the current player in the tournois_append_player list
        tournois_append_player.append(joueur_get.doc_id)
        # Call the query() default function, in tournois_get, in order to form queries
        tournois_get = Query()
        # Update the db, in the current tournois, with the updated list of player indice that include the current appended player id
        db.update({"joueurs": tournois_append_player}, tournois_get.nom == tournois_info["nom"])






