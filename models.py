import os

'''Docstring'''


class Tournois:
    """Classe des tournois"""
    def __init__(self, nom, lieu, date, nb_tours=4, description="", joueurs=[]):
        self.nom = nom
        self.lieu = lieu
        self.date = date
        self.nb_tours = nb_tours
        #self.tourne = tourne
        #self.joueurs = joueurs
        #self.controle_du_temps = controle_du_temps
        self.description = description
        self.joueurs = joueurs

    #def __str__(self):
    #    return f"{self.nom} - {self.lieu} - {self.date} - {self.sexe}"


class Joueur:
    """Classe des joueurs"""
    def __init__(self, nom, prenom, naissance, sexe, classement=0, point=0):
        self.nom = nom
        self.prenom = prenom
        self.naissance = naissance
        self.sexe = sexe
        self.classement = classement
        self.point = point

    #def complete(self):
    #    return format(self.nom, self.prenom, self.naissance, self.naissance, self.sexe, self.classement)

    def __str__(self):
        """Retourne le nom, prénom, date de naissance et sexe de la classe sous forme de string,"""
        return f"{self.nom} - {self.prenom} - {self.naissance} - {self.sexe}"


class Match:
    """Classe des matchs"""
    def __init__(self, joueur1, joueur2, resultat):
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.resultat = resultat


"""Classe des rondes"""
class Ronde:
    def __init__(self):
        pass