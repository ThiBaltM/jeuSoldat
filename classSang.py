import pygame
from random import choice

class Sang():
    def __init__(self,joueur):
        self.joueur = joueur
        self.lenAnim = 20
        self.compteur = self.lenAnim
        self.game = joueur.game
        self.images = [pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/sang1.png"), choice([0, 90, 180, -90])),(int(joueur.largeurCase), int(joueur.hauteurCase))),
        pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/sang2.png"), choice([0, 90, 180, -90])),(int(joueur.largeurCase), int(joueur.hauteurCase)))]
        self.imageActuelle = self.images[0]
        self.position = joueur.position[0], joueur.position[1]

    def majAnim(self):
        """cette fonction met a jour l'animation du sang"""
        self.game.screen.blit(self.imageActuelle,(self.game.decor.coordsFond[0] + self.position[0] * self.game.largeurCase, self.game.decor.coordsFond[1] + self.position[1] * self.game.hauteurCase, self.game.largeurCase, self.game.hauteurCase))
        if self.compteur < self.lenAnim/2:
            self.imageActuelle = self.images[1]
        self.compteur -= 1
        if self.compteur <= 0:
            self.game.tabSang.supprVal(self)


