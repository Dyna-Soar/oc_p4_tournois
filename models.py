from tinydb import TinyDB, Query

'''Fichier des models'''

db = TinyDB('db.json')
db_tournois = db.table('table_tournois')
db_joueurs = db.table('table_joueurs')


class Tournois:
    """Classe des tournois"""
    def __init__(
            self, nom, lieu, date, nb_tours=4, description="", joueurs=[]
    ):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nb_tours = nb_tours
        # self.controle_du_temps = controle_du_temps
        self.description = description
        self.joueurs = joueurs

    def insert_db_tournois(self):
        db_tournois.insert(self.__dict__)

    def update_db_tournois_joueurs(self):
        tournois_get = Query()
        db_tournois.update(
            {"joueurs": self.joueurs}, tournois_get.nom == self.nom
        )

    def update_db_tournois_nb_tours(self):
        tournois_get = Query()
        db_tournois.update(
            {"nb_tours": self.nb_tours}, tournois_get.nom == self.nom
        )


class Joueur:
    """Classe des joueurs"""
    def __init__(self, nom, prenom, naissance, sexe, classement=0, point=0):
        self.nom = nom
        self.prenom = prenom
        self.naissance = naissance
        self.sexe = sexe
        self.classement = classement
        self.point = point

    def insert_db_joueur(self):
        db_joueurs.insert(self.__dict__)

    def update_db_joueur_point(self, id):
        db_joueurs.update({"point": self.point}, db_joueurs.get(doc_id=id))

    def __str__(self):
        """Retourne le nom, prénom, date de naissance
        et sexe de la classe sous forme de string,"""
        return f"{self.nom} - {self.prenom} - {self.naissance} - {self.sexe}"


class Match:
    """Classe des matchs"""
    def __init__(self, joueur1, joueur2, resultat):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = resultat


class Ronde:
    """Classe des rondes"""
    def __init__(self):
        pass
