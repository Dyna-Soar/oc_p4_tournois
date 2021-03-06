from models import Tournois, Joueur, Match
from views import View
from tinydb import TinyDB, Query

db = TinyDB('db.json')
db_tournois = db.table('table_tournois')
db_joueurs = db.table('table_joueurs')
db_matchs = db.table('table_matchs')


class Controller:
    """Classe controlleur"""
    def __init__(self):
        """Instanciation initiale du controlleur"""
        Controller.enchainement_processus(self)

    def enchainement_processus(self):
        # Create an instance of the View class in views, called tournois
        tournois = View()
        # Créer le tournois
        if len(db_tournois) == 0:
            tournois_model = Controller.creation_tournois(self, tournois)
        else:
            tournois_info = db_tournois.get(doc_id=1)
            tournois_model = Tournois(
                tournois_info["nom"],
                tournois_info["lieu"],
                tournois_info["date"]
            )
        # Get id of latest tournament created
        tournois_id = len(db_tournois)
        if len(db_joueurs) > 0:
            for i in range(len(db_joueurs)):
                tournois_append_player = tournois_model.joueurs
                tournois_append_player.append(i+1)
                tournois_model.joueurs = tournois_append_player
                Controller.creation_joueurs(
                    self, tournois, tournois_id,
                    tournois_model, nb_joueurs_restant=8-len(db_joueurs)
                )
        else:
            Controller.creation_joueurs(
                self, tournois, tournois_id, tournois_model
            )
        if len(db_matchs) >= 16:
            Controller.rapport(self, tournois)
        else:
            Controller.update_classement(self, tournois)
            Controller.creation_paires_classement(self, tournois)
            Controller.tour_suivant(self, tournois_model, tournois_id)
            # Créer les paires et matchs pour tours suivants
            while tournois_model.nb_tours > 0:
                Controller.creation_paires_points(self, tournois)
                Controller.tour_suivant(self, tournois_model, tournois_id)
            Controller.update_classement(self, tournois)
            Controller.rapport(self, tournois)

    def creation_tournois(self, tournois):
        """Créer le tournois"""
        # Get user input
        tournois_info = tournois.input_data_tournois()
        # Create an instance of tournois class
        tournois_model = Tournois(
            tournois_info["nom"], tournois_info["lieu"], tournois_info["date"]
        )
        # Insert tournament data in the db
        tournois_model.insert_db_tournois()
        return tournois_model

    def creation_joueurs(
            self, tournois, tournois_id, tournois_model, nb_joueurs_restant=8
    ):
        """Créer 8 joueurs pour le tournois"""
        for i in range(nb_joueurs_restant):
            # Prompt the user for player input via a function in the views.py
            joueur_info = tournois.input_data_joueurs()
            # Create an instance of player
            joueur_model = Joueur(
                joueur_info["nom"], joueur_info["prenom"],
                joueur_info["naissance"], joueur_info["sexe"]
            )
            # Store the instance created, called joueur_model, in the db
            db_joueurs.insert(joueur_model.__dict__)
            # Get the id of the latest player created
            joueur_id = len(db_joueurs)
            # Get tournament data by id
            tournois_get = db_tournois.get(doc_id=tournois_id)
            # Store the list of players in a list
            tournois_append_player = tournois_get["joueurs"]
            # Append the id of player to a list
            tournois_append_player.append(joueur_id)
            tournois_get = Query()
            # Update the db with list of players
            tournois_model.joueurs = tournois_append_player
            tournois_model.update_db_tournois_joueurs()

    def creation_paires_classement(self, tournois):
        """Met les joueurs ensemble pour un premier tour,
        en fonction du classement"""
        # joueur1_id = None
        # joueur2_id = None
        list_classement_joueurs = Controller.algo_classement_joueurs(self)
        number_of_players = len(list_classement_joueurs)
        # Algorithme créant 2 listes: une supérieure et une inférieure
        divided_classement = Controller.algo_paires_sup_inf(
            self, list_classement_joueurs, number_of_players
        )
        classement_sup = divided_classement["classement_sup"]
        classement_inf = divided_classement["classement_inf"]

        # Algorithme de génération des paires par classement
        Controller.algo_paires_classement(
            self, tournois, classement_sup, classement_inf
        )

    def algo_classement_joueurs(self):
        """Retourne une liste des joueurs"""
        list_classement_joueurs = []
        for player_id in range(len(db_joueurs)):
            player_id = player_id + 1
            infos_joueur = db_joueurs.get(doc_id=player_id)
            dict_classement_joueurs = {}
            dict_classement_joueurs["id"] = player_id
            dict_classement_joueurs["classement"] = int(
                infos_joueur["classement"]
            )
            list_classement_joueurs.append(dict_classement_joueurs)
        return list_classement_joueurs

    def algo_paires_sup_inf(self, list_classement_joueurs, number_of_players):
        '''Algorithme divisant la liste générale
         en 2 listes: une supérieure et une inférieure'''
        classement_sup = []
        classement_inf = []
        while len(list_classement_joueurs) != 0:
            highest_rank = 10
            for i in range(len(list_classement_joueurs)):
                if list_classement_joueurs[i]["classement"] < highest_rank:
                    highest_rank = list_classement_joueurs[i]["classement"]
            for i in range(len(list_classement_joueurs)):
                if list_classement_joueurs[i]["classement"] == highest_rank:
                    if len(list_classement_joueurs) <= number_of_players / 2:
                        classement_inf.append(list_classement_joueurs[i])
                    else:
                        classement_sup.append(list_classement_joueurs[i])
                    list_classement_joueurs.remove(list_classement_joueurs[i])
                    break
        divided_classement = {
            "classement_sup": classement_sup, "classement_inf": classement_inf
        }
        return divided_classement

    def algo_paires_classement(self, tournois, classement_sup, classement_inf):
        """Algorithme de génération des paires par classement"""
        joueur1_id = None
        joueur2_id = None
        while len(classement_sup) != 0:
            highest_rank_sup = 100
            highest_rank_inf = 100
            for i in range(len(classement_sup)):
                if classement_sup[i]["classement"] < highest_rank_sup:
                    highest_rank_sup = classement_sup[i]["classement"]
            for i in range(len(classement_inf)):
                if classement_inf[i]["classement"] < highest_rank_inf:
                    highest_rank_inf = classement_inf[i]["classement"]
            for i in range(len(classement_sup)):
                if classement_sup[i]["classement"] == highest_rank_sup:
                    joueur1_id = classement_sup[i]["id"]
                    classement_sup.remove(classement_sup[i])
                    break
            for i in range(len(classement_inf)):
                if classement_inf[i]["classement"] == highest_rank_inf:
                    joueur2_id = classement_inf[i]["id"]
                    classement_inf.remove(classement_inf[i])
                    break
            resultat = Controller.resultat_match(
                self, tournois, joueur1_id, joueur2_id
            )
            Controller.attribution_points(
                self, joueur1_id, joueur2_id, resultat
            )

    def creation_paires_points(self, tournois):
        """Creation de paires en fonction des points,
         et classement, sans répétition d'instances de matchs"""
        joueur1 = None
        joueur2 = None
        list_joueurs = Controller.algo_classement_joueurs_points(self)
        # Algorithme mettant les joueur ensemble en fonction des points
        while len(list_joueurs) > 0:
            # First part, find the highest ranking p1
            # First loop to find the highest number of points
            highest_points = 0
            for i in range(len(list_joueurs)):
                if list_joueurs[i]["point"] > highest_points:
                    highest_points = list_joueurs[i]["point"]
            duplicate_highest_point = 0
            list_duplicate_point = []
            # Check for players with the same highest points
            for i in range(len(list_joueurs)):
                if list_joueurs[i]["point"] == highest_points:
                    duplicate_highest_point += 1
                    list_duplicate_point.append(list_joueurs[i])
            # Path of Two or more players with the same nb of highest points
            if duplicate_highest_point > 1:
                highest_rank = 10
                for i in range(len(list_duplicate_point)):
                    if list_duplicate_point[i]["classement"] < highest_rank:
                        highest_rank = list_duplicate_point[i]["classement"]
                for i in range(len(list_duplicate_point)):
                    if list_duplicate_point[i]["classement"] == highest_rank:
                        joueur1 = list_duplicate_point[i]
                        list_joueurs.remove(joueur1)
                        break
            # Path of unique player with the highest point
            else:
                joueur1 = list_duplicate_point[0]
                list_joueurs.remove(joueur1)
            # Find potential joueur2 to pair with joueur1
            optimal_order_list_p2 = []
            # First, check if already paired
            for i in range(len(list_joueurs)):
                if Controller.check_duplicate_match(
                        self, joueur1, list_joueurs[i]
                ) == "never played":
                    optimal_order_list_p2.append(list_joueurs[i])
            # Second, order by points
            point_order_list_p2 = []
            highest_points = 0
            for i in range(len(optimal_order_list_p2)):
                if optimal_order_list_p2[i]["point"] > highest_points:
                    highest_points = optimal_order_list_p2[i]["point"]
            for i in range(len(optimal_order_list_p2)):
                if optimal_order_list_p2[i]["point"] == highest_points:
                    point_order_list_p2.append(optimal_order_list_p2[i])
            # Third, order by rank
            highest_rank = 10
            for i in range(len(point_order_list_p2)):
                if point_order_list_p2[i]["classement"] < highest_rank:
                    highest_rank = point_order_list_p2[i]["classement"]
            for i in range(len(point_order_list_p2)):
                if point_order_list_p2[i]["classement"] == highest_rank:
                    joueur2 = point_order_list_p2[i]
                    list_joueurs.remove(joueur2)
                    break
            resultat = Controller.resultat_match(
                self, tournois, joueur1["id"], joueur2["id"]
            )
            Controller.attribution_points(
                self, joueur1["id"], joueur2["id"], resultat
            )

    def algo_classement_joueurs_points(self):
        """Retourne le une liste de dictionnaires des joueurs"""
        list_joueurs = []
        for player_id in range(len(db_joueurs)):
            player_id = player_id + 1
            infos_joueur = db_joueurs.get(doc_id=player_id)
            dict_joueur = {}
            dict_joueur["id"] = player_id
            dict_joueur["point"] = infos_joueur["point"]
            dict_joueur["classement"] = int(infos_joueur["classement"])
            list_joueurs.append(dict_joueur)
        return list_joueurs

    def check_duplicate_match(self, joueur1, joueur2):
        """Check for duplicated matches"""
        # Query for both players as player1
        joueur1 = joueur1["id"]
        joueur2 = joueur2["id"]
        query_matchs_j1 = db_matchs.search(Query()["joueur1"] == joueur1)
        query_matchs_j2 = db_matchs.search(Query()["joueur1"] == joueur2)
        # Player 1 as P1 loop check
        for i in range(len(query_matchs_j1)):
            if query_matchs_j1[i]["joueur2"] == joueur2:
                return "already played"
        # Player 2 as P1 loop check
        for i in range(len(query_matchs_j2)):
            if query_matchs_j2[i]["joueur2"] == joueur1:
                return "already played"
        return "never played"

    def resultat_match(self, tournois, joueur1, joueur2):
        """Retourne le résultat d'un match"""
        infos_joueur1 = db_joueurs.get(doc_id=joueur1)
        infos_joueur1 = infos_joueur1["nom"] + " " + infos_joueur1["prenom"]
        infos_joueur2 = db_joueurs.get(doc_id=joueur2)
        infos_joueur2 = infos_joueur2["nom"] + " " + infos_joueur2["prenom"]
        resultat = tournois.input_resultat_match(infos_joueur1, infos_joueur2)
        match_model = Match(joueur1, joueur2, resultat)
        # Store the instance created, called match_model, in the db
        db_matchs.insert(match_model.__dict__)
        if resultat == "1":
            return 1
        elif resultat == "2":
            return 2
        else:
            return 0

    def attribution_points(self, joueur1, joueur2, resultat):
        """Update les points des joueurs dans la db"""
        joueur1_get = db_joueurs.get(doc_id=joueur1)
        joueur2_get = db_joueurs.get(doc_id=joueur2)
        if resultat == 1:
            add_point = joueur1_get["point"] + 1
            db_joueurs.update(
                {"point": add_point}, Query().nom == joueur1_get["nom"]
            )
        elif resultat == 2:
            add_point = joueur2_get["point"] + 1
            db_joueurs.update(
                {"point": add_point}, Query().nom == joueur2_get["nom"]
            )
        else:
            add_point_j1 = joueur1_get["point"] + 0.5
            add_point_j2 = joueur2_get["point"] + 0.5
            db_joueurs.update(
                {"point": add_point_j1}, Query().nom == joueur1_get["nom"]
            )
            db_joueurs.update(
                {"point": add_point_j2}, Query().nom == joueur2_get["nom"]
            )
        return 1

    def tour_suivant(self, tournois_model, tournois_id):
        """Update de moins 1 le nombre de tours du tournois"""
        tournois_get = db_tournois.get(doc_id=tournois_id)
        nb_tours_diminue = tournois_get["nb_tours"] - 1
        tournois_model.nb_tours = nb_tours_diminue
        db_tournois.update(
            {"nb_tours": nb_tours_diminue}, Query().nom == tournois_get["nom"]
        )
        return 1

    def update_classement(self, tournois):
        """Update le classement des joueurs"""
        all_players = db_joueurs.all()
        list_classement = tournois.input_classement(all_players)
        for i in list_classement:
            db_joueurs.update(
                {"classement": i["ranking"]}, Query().nom == i["name"]
            )

    def rapport(self, tournois):
        """Envoie le rapport dans la view"""
        tournois_all_data = db_tournois.all()
        joueurs_all_data = db_joueurs.all()
        matchs_all_data = db_matchs.all()
        tournois.rapport(
            tournois=tournois_all_data,
            joueurs=joueurs_all_data,
            matchs=matchs_all_data
        )
