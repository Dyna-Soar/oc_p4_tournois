from models import Tournois, Joueur, Match, Ronde
#from views import View
import views
from tinydb import TinyDB, Query


class Controller:
    """Classe controlleur"""
    def __init__(self):
        #menu = views.menu_principal()
        self.tournois = Tournois(views.View.input_data_tournois(self))
        print("hi")

    def creation_tournois(self, nom, lieu, date):
        titre = nom
        titre = Tournois(nom, lieu, date)
        #db.insert(titre)
        views.menu_principal()

