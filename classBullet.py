from os import error
import pygame
from classSang import Sang
from math import inf, sqrt, ceil

class Bullet:
    def __init__(self, dmgFallOff, entite, dmg, speedH, speedV, ally = True):
        """
        param : 
                dmgFallOff - int - la distance au bout de laquel le projectile perd la moitié de ses dégats
                joueur - ? - l'entité qui tire
                dmg - les dégats que la balle doit infliger
                speedh - int - la vitesse de la balle a l'horizontale en cases par seconde
                speedV - int la vitesse de la balle varticale en cases par seconde
                ally - bool - si c'est le joueur qui tire ou non
        """
        self.dmgFallOff = 0.5 ** (1/dmgFallOff)
        self.entite = entite
        self.ally = ally
        self.tableau = self.entite.tableau
        self.game = self.entite.game
        self.hauteurScreen, self.largeurScreen = self.game.hauteurScreen, self.game.largeurScreen
        self.image = pygame.transform.scale(pygame.image.load("assets/balle.png"),(int(self.entite.largeurCase//5),int(self.entite.hauteurCase//5)))
        self.pixel = self.entite.largeurCase/20, self.entite.hauteurCase/20
        self.tableau = self.entite.tableau
        self.largeurCase, self.hauteurCase = self.entite.largeurCase, self.entite.hauteurCase
        self.position = self.entite.position[0], self.entite.position[1]
        self.coords = self.position[0] * self.largeurCase , self.position[1] * self.hauteurCase
        self.originCoords = self.coords[0], self.coords[1]
        self.screen = self.entite.game.screen
        self.dmg = dmg
        self.unitSpeedHorizontal = speedH * self.largeurCase / 60
        self.unitSpeedVertical = speedV * self.hauteurCase / 60
        if speedH == 0:
            self.checkH = inf
        else:
            self.checkH = 60 / speedH
        if speedV == 0:
            self.checkV = inf
        else:
            self.checkV = 60 / speedV
        self.compteur = 0
        self.axeY = 0
        self.axeX = 0
        if self.unitSpeedVertical < 0:
            self.axeY = -1
        elif self.unitSpeedVertical > 0:
            self.axeY = 1
        if self.unitSpeedHorizontal < 0:
            self.axeX = -1
        elif self.unitSpeedHorizontal > 0:
            self.axeX = 1
        self.distance = 0
    

    def majTire(self):
        """Cette fonction met a jour la position de la balle"""
        x = self.game.screen.get_width() /2 - self.game.joueur.coords[0] + self.coords[0]
        y = self.game.screen.get_height() /2 - self.game.joueur.coords[1] + self.coords[1]
        self.position = round(self.coords[0]/ self.largeurCase), round(self.coords[1] / self.hauteurCase)
        #vérifie si ça touche quelque chose
        if 0 <= self.coords[1] < self.game.decor.imageFond.get_height() and 0 <= self.coords[0] < self.game.decor.imageFond.get_width() and self.game.tableau[self.position[1]][self.position[0]].passableB():
            if self.ally:
                for ennemi in self.game.ennemis.tableau():
                    if self.position == ennemi.position:
                        self.game.tabSang.append(Sang(ennemi))
                        if not ennemi.dead:
                            ennemi.health -= self.dmg
                            if ennemi.health < 0:
                                self.dmg = ennemi.health * -1
                            else:
                                self.game.projectiles.supprVal(self)
            else:
                if self.position == self.game.joueur.position:
                    self.game.projectiles.supprVal(self)
                    self.game.joueur.touched(self.dmg)
        else:
            self.game.projectiles.supprVal(self)
        #affichage et mise ajour
        self.screen.blit(self.image,(x,y))
        #pygame.draw.rect(self.screen, "yellow", pygame.Rect(self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase, self.largeurCase, self.hauteurCase))

        dx, dy = self.coords[0] - self.originCoords[0] , self.coords[1] - self.originCoords[1]
        l = sqrt(dx**2 + dy**2) / sqrt(self.game.hauteurCase**2 + self.game.largeurCase**2)
        if self.distance < l // 1:
            self.distance += 1
            self.dmg *= self.dmgFallOff

        self.coords = self.coords[0] + self.unitSpeedHorizontal , self.coords[1] + self.unitSpeedVertical
        self.compteur += 1