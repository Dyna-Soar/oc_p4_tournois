from models import Tournois, Joueur, Match, Ronde
from views import View
from tinydb import TinyDB, Query
import random


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
        # Insert the current tournois_model instance of Tournois class inside the db
        ## db_tournois.insert(tournois_model.__dict__)
        tournois_model.insert_db_tournois()

        # Create th 8 players of the tournament by Calling the creation_joueurs function
        # Get id of latest tournament created
        tournois_id = len(db_tournois)
        Controller.creation_joueurs(self, tournois, tournois_info, tournois_id, tournois_model)

        Controller.update_classement(self, tournois)
        Controller.creation_paires_classement(self, tournois)
        # Met les joueurs ensemble pour un premier tour (creation_paires_default())
        while tournois_model.nb_tours > 0:
            Controller.creation_paires_default(self, tournois)
            Controller.tour_suivant(self, tournois_model, tournois_id)



    def creation_joueurs(self, tournois, tournois_info, tournois_id, tournois_model):
        """Créer 8 joueurs pour le tournois"""
        for i in range(4):
            # Prompt the user for player input via a function in the views.py
            joueur_info = tournois.input_data_joueurs()
            # Create an instance of player, called joueur_model, with the return value of joueur_info
            joueur_model = Joueur(joueur_info["nom"], joueur_info["prenom"], joueur_info["naissance"], joueur_info["sexe"])
            # Store the instance created, called joueur_model, in the db
            db_joueurs.insert(joueur_model.__dict__)
            # Get the id of the latest player created and store the value in joueur_id
            joueur_id = len(db_joueurs)
            # Get the current tournois info by id, which is now the argument tournois_id passed in the current function
            tournois_get = db_tournois.get(doc_id=tournois_id)
            # Store the list of players from the current tournois, in the variable tournois_append_player
            tournois_append_player = tournois_get["joueurs"]
            # Append the id indice of the current player in the tournois_append_player list
            #tournois_append_player.append(joueur_get.doc_id)
            tournois_append_player.append(joueur_id)
            # Call the query() default function, in tournois_get, in order to form queries
            tournois_get = Query()
            # Update the db, in the current tournois, with the updated list of player indice that include the current appended player id
            ## db_tournois.update({"joueurs": tournois_append_player}, tournois_get.nom == tournois_info["nom"])
            tournois_model.joueurs = tournois_append_player
            tournois_model.update_db_tournois_joueurs()
            print(tournois_model.__dict__)

    def creation_paires_default(self, tournois):
        """Met les joueurs ensemble pour un premier tour"""
        list_id_joueurs = []
        for i in range(len(db_joueurs)):
            list_id_joueurs.append(i + 1)
        print(list_id_joueurs)
        while len(list_id_joueurs) > 0:
            joueur1 = random.choice(list_id_joueurs)
            list_id_joueurs.remove(joueur1)
            joueur2 = random.choice(list_id_joueurs)
            list_id_joueurs.remove(joueur2)
            print(f"{joueur1} vs {joueur2}")
            # Get match result
            resultat = Controller.resultat_match(self, tournois, joueur1, joueur2)
            # Add points into de the db
            Controller.attribution_points(tournois, joueur1, joueur2, resultat)

    def creation_paires_classement(self, tournois):
        list_classement_joueurs = []
        for player_id in range(len(db_joueurs)):
            player_id = player_id + 1
            infos_joueur = db_joueurs.get(doc_id=player_id)
            dict_classement_joueurs = {}
            dict_classement_joueurs["id"] = player_id
            dict_classement_joueurs["classement"] = int(infos_joueur["classement"])
            list_classement_joueurs.append(dict_classement_joueurs)
        classement_sup = []
        classement_inf = []
        number_of_players = len(list_classement_joueurs)
        while len(list_classement_joueurs) != 0:
            highest_rank = 10
            for i in range(len(list_classement_joueurs)):
                if list_classement_joueurs[i]["classement"] < highest_rank:
                    highest_rank = list_classement_joueurs[i]["classement"]
            for i in range(len(list_classement_joueurs)):
                if list_classement_joueurs[i]["classement"] == highest_rank:
                    if len(list_classement_joueurs) <= number_of_players/2:
                        classement_inf.append(list_classement_joueurs[i])
                    else:
                        classement_sup.append(list_classement_joueurs[i])
                    list_classement_joueurs.remove(list_classement_joueurs[i])
                    break
        print(classement_sup)
        print(classement_inf)

    def creation_paires_points(self, tournois):
        pass

    def resultat_match(self, tournois, joueur1, joueur2):
        """Retourne le résultat d'un match"""
        infos_joueur1 = db_joueurs.get(doc_id=joueur1)
        infos_joueur1 = infos_joueur1["nom"] + " " + infos_joueur1["prenom"]
        infos_joueur2 = db_joueurs.get(doc_id=joueur2)
        infos_joueur2 = infos_joueur2["nom"] + " " + infos_joueur2["prenom"]
        resultat = tournois.input_resultat_match(infos_joueur1, infos_joueur2)
        if resultat == "1":
            print(f"le joueur {infos_joueur1} a gagné")
            return 1
        elif resultat == "2":
            print(f"le joueur {infos_joueur2} a gagné")
            return 2
        else:
            print("Match Nul")
            return 0

    def attribution_points(self, joueur1, joueur2, resultat):
        """Update les points des joueurs dans la db"""
        joueur1_get = db_joueurs.get(doc_id=joueur1)
        joueur2_get = db_joueurs.get(doc_id=joueur2)
        if resultat == 1:
            add_point = joueur1_get["point"] + 1
            db_joueurs.update({"point": add_point}, Query().nom == joueur1_get["nom"])
        elif resultat == 2:
            add_point = joueur2_get["point"] + 1
            db_joueurs.update({"point": add_point}, Query().nom == joueur2_get["nom"])
        else:
            add_point_j1 = joueur1_get["point"] + 0.5
            add_point_j2 = joueur2_get["point"] + 0.5
            db_joueurs.update({"point": add_point_j1}, Query().nom == joueur1_get["nom"])
            db_joueurs.update({"point": add_point_j2}, Query().nom == joueur2_get["nom"])
        return 1

    def tour_suivant(self, tournois_model, tournois_id):
        """Update de moins 1 le nombre de tours du tournois"""
        print("next tour sucess")
        tournois_get = db_tournois.get(doc_id=tournois_id)
        nb_tours_diminue = tournois_get["nb_tours"] - 1
        tournois_model.nb_tours = nb_tours_diminue
        db_tournois.update({"nb_tours": nb_tours_diminue}, Query().nom == tournois_get["nom"])
        return 1

    def update_classement(self, tournois):
        all_players = db_joueurs.all()
        print(all_players)
        list_classement = tournois.input_classement(all_players)
        print(list_classement)
        for i in list_classement:
            db_joueurs.update({"classement": i["ranking"]}, Query().nom == i["name"])

