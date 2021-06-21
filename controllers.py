from models import Tournois, Joueur, Match, Ronde
#from views import View
#import views
from views import View
from tinydb import TinyDB, Query


db = TinyDB('db.json')
db_tournois = db.table('table_tournois')
db_joueurs = db.table('table_joueurs')

class Controller:
    """Classe controlleur"""
    def __init__(self):
        # Create an instance of the View class in views, called tournois
        tournois = View()
        # Créer le tournois
        # Store the user input of tournois info (nom, lieu, date) in the variable tournois_info
        tournois_info = tournois.input_data_tournois()
        # Create an instance of tournois calss in models.py, called tournois_model with the return user input,
        tournois_model = Tournois(tournois_info["nom"], tournois_info["lieu"], tournois_info["date"])
        print(tournois_model.__dict__)
        # Insert the current tournois_model instance of Tournois class inside the db
        db_tournois.insert(tournois_model.__dict__)

        # Créer les 8 joueurs

        # Call the creation_joueurs function
        tournois_id = db.table('table_tournois')
        #tournois_id = tournois_id.get(doc_id=len(tournois_id))
        tournois_id = len(tournois_id)
        print(tournois_id)
        Controller.creation_joueurs(self, tournois, tournois_info, tournois_id)

    def creation_joueurs(self, tournois, tournois_info, tournois_id):
        for i in range(8):
            print(tournois_id)
            # Prompt the user for player input via a function in the views.py
            joueur_info = tournois.input_data_joueurs()
            # Create an instance of player, called joueur_model, with the return value of joueur_info
            joueur_model = Joueur(joueur_info["nom"], joueur_info["prenom"], joueur_info["naissance"], joueur_info["sexe"])
            # Store the instance created, called joueur_model, in the db
            db_joueurs.insert(joueur_model.__dict__)
            # Call the query() default function, in joueur_get, in order to form queries
            joueur_get = Query()
            joueur_id = Query()
            # Query the current player by its name, which is an attribute stored in joueur_info
            #joueur_get = db_joueurs.get(joueur_get.nom == joueur_info["nom"])
            #print(joueur_get)
            joueur_id = db.table('table_joueurs')
            joueur_id = len(joueur_id)
            # Get the current tournois info by id, which is now the argument tournois_id passed in the current function
            tournois_get = db_tournois.get(doc_id=tournois_id)
            print(tournois_get)
            # Store the list of players from the current tournois, in the variable tournois_append_player
            tournois_append_player = tournois_get["joueurs"]
            # Append the id indice of the current player in the tournois_append_player list
            #tournois_append_player.append(joueur_get.doc_id)
            tournois_append_player.append(joueur_id)
            # Call the query() default function, in tournois_get, in order to form queries
            tournois_get = Query()
            # Update the db, in the current tournois, with the updated list of player indice that include the current appended player id
            db_tournois.update({"joueurs": tournois_append_player}, tournois_get.nom == tournois_info["nom"])






