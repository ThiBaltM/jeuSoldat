import pygame
from classPlayer import Player
from classEnnemis import *
from listeChainee import Liste
from classItem import *
from random import choice
from classDecor import *
from maps import tabMap0


class Test:
    def __init__(self):
        self.traversable = False        


class Game:
    def __init__(self, screen, difficulty = "easy"):
        
        self.largeurPlateau, self.hauteurPlateau = 19, 11 
        self.tableau = tabMap0
        #autre variables
        self.screen = screen
        self.largeurCase, self.hauteurCase = int(self.screen.get_width()/ self.largeurPlateau), int(self.screen.get_height()/ (self.hauteurPlateau))
        self.difficulty = difficulty
        self.imageFond = pygame.transform.scale(pygame.image.load("assets/textureBoue.png"),(int(self.largeurPlateau*self.largeurCase),int(self.hauteurCase * 2)))
        self.pressed = {pygame.K_e : False,1: False, pygame.K_z:False, pygame.K_s:False, pygame.K_q:False, pygame.K_d:False, 49 : False, 50 : False, 51 : False, pygame.K_SPACE: False}
        self.joueur = Player(self)
        self.compteur = 0
        self.ennemis = Liste()
        self.projectiles = Liste()
        self.tabSang = Liste()
        self.hauteurScreen, self.largeurScreen = (self.screen.get_height() - 2* self.hauteurCase,self.screen.get_width())
        self.loot = Liste()
        self.score = 0
        self.nameJoueur = "ThiBalt"
        source = open("highScore.txt", "r")
        self.highScore = source.read()
        source.close()
        self.rewardKill = 10
        self.lvl = 0
        self.decor = Decor(self)
                  
    def update(self):
        """Cette fonction met a jour les evenement divers pouvant avoir lieux"""
        #tableau de recherche des tentes et ennemis
        """
        pos = self.joueur.position
        x0, x1 = pos[0] - 9, pos[0] + 9
        if x1 >= 31:
            x1 = 31
        if x0 <= 0:
            x0 = 0
        y0, y1 = pos[1] - 5, pos[1] + 5
        if y0 <= 0:
            y0 = 0
        if y1 >= 20:
            y1 = 20
        newT = self.tableau[x0:x1][y0:y1]
        """
        if self.compteur % (120 * 4) == 0:
            self.ennemis.append(choice([EnnemiAR(self,(11,12)), EnnemiPompe(self,(3,7)),EnnemiUzi(self,(23,12))]))
        self.decor.majAffichage()
        #affichage loot
        for k in self.loot:
            k.affichage()
        #affichage joueur
        self.joueur.affichage()
        #affichage des ennemis
        for k in self.ennemis:
            k.affichageMaj()
        #affichage des projectiles
        for k in self.projectiles:
            k.majTire()
        #affichage du sang
        for k in self.tabSang:
            k.majAnim()
        #affichage de la barre inférieur
        self.joueur.afficheAmmo()
        self.joueur.afficheArmes()
        myfont = pygame.font.SysFont('Impact', self.screen.get_width() // 74)
        textScoreSurface = myfont.render(f"your score :{self.score}", False, (255, 255, 255))
        textHighScoreSurface = myfont.render(f"high score :{self.highScore}", False, (255, 255, 255))
        self.screen.blit(textScoreSurface,(self.joueur.pixel[0] * 340,self.joueur.pixel[1]))
        self.screen.blit(textHighScoreSurface,(self.joueur.pixel[0] * 340, 9 * self.joueur.pixel[1]))
        #gestion joueur
        if self.joueur.reloading >= 1:
            self.joueur.animReload()
        if self.joueur.busy >= 1:
            self.joueur.mouvement()
        else:
            if self.pressed[pygame.K_z]:
                self.joueur.haut()
            elif self.pressed[pygame.K_s]:
                self.joueur.bas()
            elif self.pressed[pygame.K_q]:
                self.joueur.gauche()
            elif self.pressed[pygame.K_d]:
                self.joueur.droite()
            else:
                self.joueur.statique()
        if self.pressed[49]:
            self.joueur.changeArme(0)
        elif self.pressed[50]:
            self.joueur.changeArme(1)
        elif self.pressed[51]:
            self.joueur.changeArme(2)
        elif self.pressed[1] and not self.joueur.dead:
            self.joueur.feu()
        
        self.compteur += 1
        
        #ajout d'un ennemis toutes les 3 secondes
        
        """if self.compteur % 180 == 0 and not self.joueur.dead:
            self.score += 1
            self.ennemis.append(EnnemiAR(self))"""
            #self.ennemis.append(choice([EnnemiAR(self), EnnemiPompe(self), EnnemiUzi(self)]))

        

    def drop(self, entite):
        """Cette fonction créer un nouveau loot"""
        obj = choice([KitSoin(entite)] * 3 + [Pansement(entite)] *15 + [Munitions(entite)] * 15 + [None] * 20 + [BoiteMunitions(entite)] + [Arme(entite)] * 10)
        if obj != None:
            self.loot.append(obj)
    
    def saveScore(self):
        """Cette fonction doit être activé"e lorsque le jeu est fermé, elle sauvegerde le score si il est meilleur que le meilleur score"""
        if self.score > int(self.highScore):
            source = open("highScore.txt", "w")
            source.write(str(self.score))
            source.close()





        
        