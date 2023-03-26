from classEnnemis import *
from random import choice

class Tente:
    def __init__(self,pos):
        """pos - tupple - x,y position de la tente sur quadrillage"""
        self.pos = pos
        self.compteur = 0
    
    def update(self):
        """cette fonction met a jour, et fait apparaittre si besoin un ennemis aléatoire entre les 3"""
        self.compteur += 1
        if self.compteur % 60 * 8:
            choice([EnnemiAR(self.pos), EnnemiPompe(self.pos), EnnemiUzi(self.pos)])
        