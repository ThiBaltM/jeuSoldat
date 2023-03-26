import pygame
from random import randint

class KitSoin:
    def __init__(self, entite):
        self.game = entite.game
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.img = pygame.transform.scale(pygame.image.load(f"assets/kitSoin.png"),(self.largeurCase, self.hauteurCase))
        self.entite = entite
        self.position = entite.position
        self.coords = self.position[0] * self.hauteurCase, self.position[1] * self.largeurCase
        self.timer = 600
        self.traversable = True
        self.pixel = entite.pixel

    def affichage(self):
        """Cette fonction affiche l'item au sol"""
        if self.timer <= 0:
            self.game.loot.supprVal(self)
            return
        self.game.screen.blit(self.img, (self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase))
        self.timer -= 1

    def picked(self):
        """Cette fonction rend la vie au joueur"""
        self.game.joueur.health = self.game.joueur.max_health
        self.game.loot.supprVal(self) 

class Pansement:
    def __init__(self, entite):
        self.soin = 20
        self.traversable = True
        self.game = entite.game
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.img = pygame.transform.scale(pygame.image.load(f"assets/pansement.png"),(self.largeurCase, self.hauteurCase))
        self.entite = entite
        self.position = entite.position
        self.coords = self.position[0] * self.hauteurCase, self.position[1] * self.largeurCase
        self.timer = 600
        self.pixel = entite.pixel

    def affichage(self):
        """Cette fonction affiche l'item au sol"""
        if self.timer <= 0:
            self.game.loot.supprVal(self)
            return
        self.game.screen.blit(self.img, (self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase))
        self.timer -=1
    
    def picked(self):
        """Cette fonction redonne un peu de vie au joueur"""
        if self.game.joueur.health + self.soin <= self.game.joueur.max_health:
            self.game.joueur.health += self.soin
        else:
            self.game.joueur.health = self.game.joueur.max_health
        self.game.loot.supprVal(self)

class Munitions:
    def __init__(self, entite, n = randint(15,25)): #je met 15 et 25 mais après je divise par 10 cvar randint ne prend que les nbr entiers
        self.game = entite.game
        self.traversable = True
        self.entite = entite
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.img = pygame.transform.scale(pygame.image.load(f"assets/munitions.png"),(self.largeurCase, self.hauteurCase))
        self.n = round((n/10) * self.game.joueur.maxAmmo[self.game.joueur.hand])
        self.game = entite.game
        self.position = entite.position
        self.coords = self.position[0] * self.game.hauteurCase, self.position[1] * self.game.largeurCase
        self.timer = 600
        self.pixel = entite.pixel

    def affichage(self):
        """Cette fonction affiche l'item au sol"""
        if self.timer <= 0:
            self.game.loot.supprVal(self)
            return
        self.game.screen.blit(self.img, (self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase))
        self.timer -=1
    
    def picked(self):
        """Cette fonction redonne des munitions au joueur"""
        self.game.joueur.ammo[self.game.joueur.hand] += self.n
        self.game.loot.supprVal(self)

class BoiteMunitions:
    def __init__(self, entite, n = randint(50,80)):
        self.game = entite.game
        self.traversable = True
        self.entite = entite
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.img = pygame.transform.scale(pygame.image.load(f"assets/boiteMunitions.png"),(self.largeurCase, self.hauteurCase))
        self.n = round((n/10) * self.game.joueur.maxAmmo[self.game.joueur.hand])
        self.game = entite.game
        self.position = entite.position
        self.coords = self.position[0] * self.game.hauteurCase, self.position[1] * self.game.largeurCase
        self.timer = 600
        self.pixel = entite.pixel

    def affichage(self):
        """Cette fonction affiche l'item au sol"""
        if self.timer <= 0:
            self.game.loot.supprVal(self)
            return
        self.game.screen.blit(self.img, (self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase))
        self.timer -=1
    
    def picked(self):
        """Cette fonction redonne des munitions au joueur"""
        self.game.joueur.ammo[self.game.joueur.hand] += self.n
        self.game.loot.supprVal(self)

class Arme:
    def __init__(self, entite):
        self.traversable = True
        self.game = entite.game
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.img = pygame.transform.scale(pygame.image.load(f"assets/{entite.hand}.png"),(self.largeurCase, self.hauteurCase))
        self.game = entite.game
        self.entite = entite
        self.position = entite.position
        self.coords = self.position[0] * self.game.hauteurCase, self.position[1] * self.game.largeurCase
        self.timer = 600
        self.pixel = entite.pixel

    def affichage(self):
        """Cette fonction affiche l'item au sol"""
        if self.timer <= 0:
            self.game.loot.supprVal(self)
            return
        self.game.screen.blit(self.img, (self.game.largeurPlateau //2 * self.largeurCase - self.game.joueur.coords[0] + self.position[0] * self.largeurCase, self.game.hauteurPlateau //2 * self.hauteurCase- self.game.joueur.coords[1] + self.position[1] * self.hauteurCase))
        self.timer -=1
    
    def picked(self):
        """Cette fonction donne l'arme et des munitions de cette arme au joueur si il ne l'a pas sur lui"""
        if not self.entite.hand in self.game.joueur.slot:
            self.game.joueur.slot[self.game.joueur.slotActif ] = self.entite.hand
            self.game.joueur.changeArme(self.game.joueur.slotActif)
        self.game.joueur.ammo[self.entite.hand] += self.game.joueur.maxAmmo[self.entite.hand]
        self.game.loot.supprVal(self)