import pygame
from classBullet import Bullet
from random import choice
from listeChainee import Liste
from classSang import Sang
from math import pi, sqrt, atan2, cos ,sin, degrees

class EnnemiAR:
    def __init__(self, game, pos):
        """
        game - game object - la classe qui fait tourner le jeu
        pos - tuple - position (largeur , hauteur) de l'ennemi sur le plateau"""
        self.game = game
        self.tableau = self.game.tableau
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.imagesHaut = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            self.imagesHaut[direction] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/ennemi/AR/ar.png"), angle),(self.largeurCase, self.hauteurCase))
            #corp à corp
            self.imagesHaut["contact" + direction] = []
            for k in range(1,3):
                self.imagesHaut["contact" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/AR/arContact{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #mort
            self.imagesHaut["meurt" + direction] = []
            for k in range(1,4):
                self.imagesHaut["meurt" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/AR/arMeurt{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #rechargement
            self.imagesHaut["reload" + direction] = []
            for k in range(1,5):
                self.imagesHaut["reload" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/AR/arReload{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
        self.imagesBas = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            #statique
            self.imagesBas["statique" + direction] =  pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/AR/statique.png"), angle),(self.largeurCase, self.hauteurCase))
            #marche avant
            self.imagesBas["avant" + direction] = []
            for k in range(1,5):
                self.imagesBas["avant" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/AR/avant{k}.png"), angle),(self.largeurCase, self.hauteurCase)))

        self.largeurCase, self.hauteurCase = self.game.largeurCase, self.game.hauteurCase
        self.direction = "Gauche"
        self.compteurFire = 0
        self.imageHautActuelle = self.imagesHaut["Gauche"]
        self.imageBasActuelle = self.imagesBas["statiqueGauche"]
        self.position = pos
        self.coords = self.position[0] * self.largeurCase, self.position[1] * self.hauteurCase
        self.enJoue = False
        self.vision = 10
        self.portee = 7
        self.joueur = self.game.joueur
        self.health = 50
        self.maxBusy = 28
        self.busy = 0
        self.projectiles = Liste()
        self.hand = "ar"
        self.rect = self.imageHautActuelle.get_rect()
        self.dead = False
        self.contact = False
        self.pixel = self.joueur.pixel
        self.reloading = -1
        self.ammo = 30
        self.maxAmmo = 30
        self.dx = 0
        self.dy = 0
        self.traversable = False
        self.traversableB = True
        self.mooving = False
        self.screen = game.screen

    def __str__(self):
        return "🖓"

    def affichageMaj(self):
        """Cette fonction affiche et met a jour les variables qsui doivent l'être"""
        x = (self.game.largeurPlateau - 1) /2 * self.hauteurCase - self.game.joueur.coords[0] + self.coords[0] +4 * self.pixel[0]
        y = (self.game.hauteurPlateau - 1) /2 * self.largeurCase - self.game.joueur.coords[1] + self.coords[1] -5 * self.pixel[1]
        self.iA()
        #pygame.draw.rect(self.screen, "red", pygame.Rect(self.game.decor.coordsFond[0] + self.position[0] * self.largeurCase, self.game.decor.coordsFond[1] + self.position[1] * self.hauteurCase, self.largeurCase, self.hauteurCase))
        self.screen.blit(self.imageBasActuelle,(x, y))
        self.screen.blit(self.imageHautActuelle,(x, y))
        #gestion pour si le joueur tire
        if self.dx == 0 and self.dy == 0:
            self.dx = 1
        print(self.position)
    
    def majAngle(self):
        """Cette fonction met a jour l'affichage du haut du corp en fonction de la position du joueur"""
        pos = self.joueur.position[0], self.joueur.position[1]
        self.dx =  pos[0] - self.position[0]
        self.dy = pos[1] - self.position[1]
        if self.reloading <= 0:
            #gestion de l'image du haut du corp
            self.rads = atan2(-self.dy,self.dx)
            self.rads %= 2*pi
            self.imageHautActuelle = pygame.transform.rotate(self.imagesHaut["Droite"], degrees(self.rads))
        else:
            self.reloading -= 1
            self.animReload()

    def iA(self):
        """Fait se déplacer l'ennemi si nécéssaire et tire si c'est bon"""
        if self.contact and not self.dead:
            if self.busy <= 40/2:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][0]
            else:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][1]
            self.busy -= 1
            if self.busy <= 0:
                self.contact = False
                self.joueur.contact()
                self.health = 0

        elif self.dead:
            #animation de mort
            if self.busy <= 40/3:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][2]
            elif self.busy <= (40/3) * 2:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][1]
            else:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][0]
            self.busy -= 1
            #fin de l'animation de mort
            if self.busy <= 0:
                self.tableau[self.position[1]][self.position[0]].supprVal(self)
                self.game.drop(self)
                self.game.score += self.game.rewardKill
                self.game.ennemis.supprVal(self)
        else:
            self.compteurFire -=1
            if self.health <= 0:
                self.dead = True
                self.busy = 40
                self.imageBasActuelle = self.imagesBas["statique" + self.direction]
            if self.enJoue and self.compteurFire <= 0:
                self.imagesBasActuelle = self.imagesBas["statique"+self.direction]
                self.feu()
                self.enJoue = False
            posJoueur = self.joueur.position
            posEnnemi = self.position
            difLargeur, difHauteur = posJoueur[0] - posEnnemi[0], posJoueur[1] - posEnnemi[1]
            if self.busy <= 0:
                #si il est a portée
                if sqrt(difHauteur**2 + difLargeur**2) < self.portee:
                    self.majAngle()
                    self.enJoue = True

                #si il est juste dans le champ de vision
                elif self.vision * -1 <= difHauteur <= self.vision and self.vision * -1 <= difLargeur <= self.vision:
                    self.majAngle()
                    if difHauteur <= 0:
                        if difLargeur <= 0:
                            self.direction = choice(["Haut", "Gauche"])
                        else:
                            self.direction = choice(["Haut", "Droite"])
                    else:
                        if difLargeur <= 0:
                            self.direction = choice(["Bas", "Gauche"])
                        else:
                            self.direction = choice(["Bas", "Droite"])
                    self.mooving = True
                #si l'ennemi ne sais pas ou est le joueur
                else:
                    if 0 < self.position[0] < self.game.largeurPlateau - 1:
                        direction = ["Gauche", "Droite"]
                    elif self.position[0] == 0:
                        direction = ["Droite"]
                    else:
                        direction = ["Gauche"]
                    if 0 < self.position[1] < self.game.hauteurPlateau - 1:
                        direction.append("Haut")
                        direction.append("Bas")
                    elif self.position[1] == 0:
                        direction.append("Bas")
                    else:
                        direction.append("Haut")
                    self.direction = choice(direction)
                    self.imageHautActuelle = self.imagesHaut[self.direction]
                    self.mooving = True
                   
                if self.verifDirection() and self.mooving:
                    if self.direction  == "Bas":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self) #met a jour le tableau
                        self.position = self.position[0], self.position[1] + 1             #met a jour les positions
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Haut":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0], self.position[1] - 1
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Gauche":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] - 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    else:
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] + 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    self.busy = self.maxBusy
                    self.mooving = False
                            
            else:
                self.mouvement()

    def verifDirection(self):
        """Cette fonction renvoie un booléen si le déplacement est possible ou non"""
        if self.direction == "Droite":
            if self.position[0] + 1 < self.game.largeurPlateau and self.game.tableau[self.position[1]][self.position[0] + 1].passable():
                return True
        elif self.direction == "Gauche":
            if self.position[0] > 0 and self.game.tableau[self.position[1]][self.position[0] - 1].passable():
                return True
        elif self.direction == "Haut":
            if self.position[1] > 0 and self.game.tableau[self.position[1] - 1][self.position[0]].passable():
                return True
        elif self.direction == "Bas":
            if self.position[1] + 1 < self.game.hauteurPlateau and self.game.tableau[self.position[1] + 1][self.position[0]].passable():
                return True
        return False

    def mouvement(self):
        """Cette fonction fait bouger l'ennemi"""
        deplLargeur = self.largeurCase/self.maxBusy
        deplHauteur = self.hauteurCase/self.maxBusy
        if self.direction == "Gauche":
            self.coords = self.coords[0] - deplLargeur, self.coords[1] 
        elif self.direction == "Droite":
            self.coords = self.coords[0] + deplLargeur, self.coords[1] 
        elif self.direction == "Haut":
            self.coords = self.coords[0], self.coords[1] - deplHauteur 
        else:
            self.coords = self.coords[0], self.coords[1] + deplHauteur
        
        if self.busy <= self.maxBusy/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= self.maxBusy/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][1]
        elif self.busy <= self.maxBusy/2:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= (self.maxBusy*2)/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        elif self.busy <= (self.maxBusy*5)/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][3]
        elif self.busy <= self.maxBusy:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        self.busy -= 1

    def touched(self, dmg):
        """Cette fonction modifie la vie quand il est touché par une balle"""
        self.health -= dmg
        if self.health < 0:
            self.health = 0
        self.game.tabSang.append(Sang(self))

    def feu(self):
        """Cette fonction fait tirer l'ennemi dans sa direction"""
        if self.compteurFire <= 0 and self.reloading <= 0:
            l = sqrt(self.dx**2 + self.dy**2)
            speedH = self.dx * 12 / l  #ici 12 correspond à la vitesse du projectile
            speedV = self.dy * 12 / l  
            self.game.projectiles.append(Bullet(15, self,5, speedH, speedV, False))
            self.compteurFire = 12
            self.ammo -= 1
            if self.ammo <= 0:
                self.reload()

    def reload(self):
        """redonne des munitions et active l'animation"""
        self.reloading = 50
        self.ammo = self.maxAmmo

    def animReload(self):
        """Cette fonction anime le rechergement de l'arme"""
        reloadingTime = 40
        if self.reloading <= 1:
            self.imageHautActuelle = self.imagesHaut[self.direction]
        elif self.reloading < reloadingTime / 4:
            self.imageHautActuelle = self.imagesHaut["reload"+ self.direction][3]
        elif self.reloading < reloadingTime / 2:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][2]
        elif self.reloading < reloadingTime * 3 / 4:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][1]
        else:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][0]


#####################################################################################################################
"""Ennemi au fusil a pompe"""
#####################################################################################################################

class EnnemiPompe:
    def __init__(self, game, pos):
        """
        game - game object - la classe qui fait tourner le jeu
        pos - tuple - position (largeur , hauteur) de l'ennemi sur le plateau"""
        self.game = game
        self.tableau = self.game.tableau
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.imagesHaut = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            self.imagesHaut[direction] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/ennemi/fusilAPompe/fusilAPompe.png"), angle),(self.largeurCase, self.hauteurCase))
            #corp à corp
            self.imagesHaut["contact" + direction] = []
            for k in range(1,3):
                self.imagesHaut["contact" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/fusilAPompe/fusilAPompeContact{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #mort
            self.imagesHaut["meurt" + direction] = []
            for k in range(1,4):
                self.imagesHaut["meurt" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/fusilAPompe/fusilAPompeMeurt{k}.png"), angle),(self.largeurCase, self.hauteurCase)))

        self.imagesBas = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            #statique
            self.imagesBas["statique" + direction] =  pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/fusilAPompe/statique.png"), angle),(self.largeurCase, self.hauteurCase))
            #marche avant
            self.imagesBas["avant" + direction] = []
            for k in range(1,5):
                self.imagesBas["avant" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/fusilAPompe/avant{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #rechargement
            self.imagesHaut["reload" + direction] = []
            for k in range(1,5):
                self.imagesHaut["reload" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/fusilAPompe/fusilAPompeReload{k}.png"), angle),(self.largeurCase, self.hauteurCase)))

        self.largeurCase, self.hauteurCase = self.game.largeurCase, self.game.hauteurCase
        self.direction = "Gauche"
        self.compteurFire = 0
        self.imageHautActuelle = self.imagesHaut["Gauche"]
        self.imageBasActuelle = self.imagesBas["statiqueGauche"]
        self.position = pos
        self.coords = self.position[0] * self.largeurCase, self.position[1] * self.hauteurCase
        self.enJoue = False
        self.vision = 15
        self.portee = 5
        self.joueur = self.game.joueur
        self.health = 60
        self.maxBusy = 40
        self.busy = 0
        self.projectiles = Liste()
        self.hand = "fusilAPompe"
        self.rect = self.imageHautActuelle.get_rect()
        self.dead = False
        self.contact = False
        self.pixel = self.joueur.pixel
        self.reloading = -1
        self.ammo = 2
        self.maxAmmo = 2
        self.dx = 0
        self.dy = 0
        self.traversable = False
        self.traversableB = True
        self.mooving = False
        self.screen = game.screen

    def __str__(self):
        return "🖓"

    def affichageMaj(self):
        """Cette fonction affiche et met a jour les variables qsui doivent l'être"""
        x = (self.game.largeurPlateau - 1) /2 * self.hauteurCase - self.game.joueur.coords[0] + self.coords[0] +4 * self.pixel[0]
        y = (self.game.hauteurPlateau - 1) /2 * self.largeurCase - self.game.joueur.coords[1] + self.coords[1] -5 * self.pixel[1]
        self.iA()
        #pygame.draw.rect(self.screen, "red", pygame.Rect(self.game.decor.coordsFond[0] + self.position[0] * self.largeurCase, self.game.decor.coordsFond[1] + self.position[1] * self.hauteurCase, self.largeurCase, self.hauteurCase))
        self.screen.blit(self.imageBasActuelle,(x, y))
        self.screen.blit(self.imageHautActuelle,(x, y))
        #gestion pour si le joueur tire
        if self.dx == 0 and self.dy == 0:
            self.dx = 1
    
    def majAngle(self):
        """Cette fonction met a jour l'affichage du haut du corp en fonction de la position du joueur"""
        pos = self.joueur.position[0], self.joueur.position[1]
        self.dx =  pos[0] - self.position[0]
        self.dy = pos[1] - self.position[1]
        if self.reloading <= 0:
            #gestion de l'image du haut du corp
            self.rads = atan2(-self.dy,self.dx)
            self.rads %= 2*pi
            self.imageHautActuelle = pygame.transform.rotate(self.imagesHaut["Droite"], degrees(self.rads))
        else:
            self.reloading -= 1
            self.animReload()

    def iA(self):
        """Fait se déplacer l'ennemi si nécéssaire et tire si c'est bon"""
        if self.contact and not self.dead:
            if self.busy <= 40/2:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][0]
            else:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][1]
            self.busy -= 1
            if self.busy <= 0:
                self.contact = False
                self.joueur.contact()
                self.health = 0

        elif self.dead:
            #animation de mort
            if self.busy <= 40/3:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][2]
            elif self.busy <= (40/3) * 2:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][1]
            else:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][0]
            self.busy -= 1
            #fin de l'animation de mort
            if self.busy <= 0:
                self.tableau[self.position[1]][self.position[0]].supprVal(self)
                self.game.drop(self)
                self.game.score += self.game.rewardKill
                self.game.ennemis.supprVal(self)
        else:
            self.compteurFire -=1
            if self.health <= 0:
                self.dead = True
                self.busy = 40
                self.imageBasActuelle = self.imagesBas["statique" + self.direction]
            if self.enJoue and self.compteurFire <= 0:
                self.imagesBasActuelle = self.imagesBas["statique"+self.direction]
                self.feu()
                self.enJoue = False
            posJoueur = self.joueur.position
            posEnnemi = self.position
            difLargeur, difHauteur = posJoueur[0] - posEnnemi[0], posJoueur[1] - posEnnemi[1]
            if self.busy <= 0:
                #si il est a portée
                if sqrt(difHauteur**2 + difLargeur**2) < self.portee:
                    self.majAngle()
                    self.enJoue = True

                #si il est juste dans le champ de vision
                elif self.vision * -1 <= difHauteur <= self.vision and self.vision * -1 <= difLargeur <= self.vision:
                    self.majAngle()
                    if difHauteur <= 0:
                        if difLargeur <= 0:
                            self.direction = choice(["Haut", "Gauche"])
                        else:
                            self.direction = choice(["Haut", "Droite"])
                    else:
                        if difLargeur <= 0:
                            self.direction = choice(["Bas", "Gauche"])
                        else:
                            self.direction = choice(["Bas", "Droite"])
                    self.mooving = True
                #si l'ennemi ne sais pas ou est le joueur
                else:
                    if 0 < self.position[0] < self.game.largeurPlateau - 1:
                        direction = ["Gauche", "Droite"]
                    elif self.position[0] == 0:
                        direction = ["Droite"]
                    else:
                        direction = ["Gauche"]
                    if 0 < self.position[1] < self.game.hauteurPlateau - 1:
                        direction.append("Haut")
                        direction.append("Bas")
                    elif self.position[1] == 0:
                        direction.append("Bas")
                    else:
                        direction.append("Haut")
                    self.direction = choice(direction)
                    self.imageHautActuelle = self.imagesHaut[self.direction]
                    self.mooving = True
                   
                if self.verifDirection() and self.mooving:
                    if self.direction  == "Bas":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self) #met a jour le tableau
                        self.position = self.position[0], self.position[1] + 1             #met a jour les positions
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Haut":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0], self.position[1] - 1
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Gauche":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] - 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    else:
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] + 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    self.busy = self.maxBusy
                    self.mooving = False
                            
            else:
                self.mouvement()

    def verifDirection(self):
        """Cette fonction renvoie un booléen si le déplacement est possible ou non"""
        if self.direction == "Droite":
            if self.position[0] + 1 < self.game.largeurPlateau and self.game.tableau[self.position[1]][self.position[0] + 1].passable():
                return True
        elif self.direction == "Gauche":
            if self.position[0] > 0 and self.game.tableau[self.position[1]][self.position[0] - 1].passable():
                return True
        elif self.direction == "Haut":
            if self.position[1] > 0 and self.game.tableau[self.position[1] - 1][self.position[0]].passable():
                return True
        elif self.direction == "Bas":
            if self.position[1] + 1 < self.game.hauteurPlateau and self.game.tableau[self.position[1] + 1][self.position[0]].passable():
                return True
        return False

    def mouvement(self):
        """Cette fonction fait bouger l'ennemi"""
        deplLargeur = self.largeurCase/self.maxBusy
        deplHauteur = self.hauteurCase/self.maxBusy
        if self.direction == "Gauche":
            self.coords = self.coords[0] - deplLargeur, self.coords[1] 
        elif self.direction == "Droite":
            self.coords = self.coords[0] + deplLargeur, self.coords[1] 
        elif self.direction == "Haut":
            self.coords = self.coords[0], self.coords[1] - deplHauteur 
        else:
            self.coords = self.coords[0], self.coords[1] + deplHauteur
        
        if self.busy <= self.maxBusy/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= self.maxBusy/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][1]
        elif self.busy <= self.maxBusy/2:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= (self.maxBusy*2)/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        elif self.busy <= (self.maxBusy*5)/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][3]
        elif self.busy <= self.maxBusy:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        self.busy -= 1

    def touched(self, dmg):
        """Cette fonction modifie la vie quand il est touché par une balle"""
        self.health -= dmg
        if self.health < 0:
            self.health = 0
        self.game.tabSang.append(Sang(self))

    def feu(self):
            """Cette fonction fait tirer l'ennemi dans sa direction"""
            if self.reloading <= 0:
                for rads in [self.rads, self.rads + pi/12, self.rads - pi/12]:
                    self.game.projectiles.append(Bullet(5,self,8, 8*cos(rads), -8*sin(rads), False))
                    self.compteurFire = 40
                self.ammo -= 1
                if self.ammo <= 0:
                    self.reload()

    def reload(self):
        """redonne des munitions et active l'animation"""
        self.reloading = 35
        self.ammo = self.maxAmmo

    def animReload(self):
        """Cette fonction anime le rechergement de l'arme"""
        reloadingTime = 40
        if self.reloading <= 1:
            self.imageHautActuelle = self.imagesHaut[self.direction]
        elif self.reloading < reloadingTime / 4:
            self.imageHautActuelle = self.imagesHaut["reload"+ self.direction][3]
        elif self.reloading < reloadingTime / 2:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][2]
        elif self.reloading < reloadingTime * 3 / 4:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][1]
        else:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][0]

########################################################################################################
""" Ennemi Uzi"""
#######################################################################################################
class EnnemiUzi:
    def __init__(self, game, pos):
        """
        game - game object - la classe qui fait tourner le jeu
        pos - tuple - position (largeur , hauteur) de l'ennemi sur le plateau"""
        self.game = game
        self.tableau = self.game.tableau
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.sang = [pygame.transform.scale(pygame.image.load("assets/sang1.png"),(self.largeurCase, self.hauteurCase)),pygame.transform.scale(pygame.image.load("assets/sang2.png"),(self.largeurCase, self.hauteurCase))]
        self.imagesHaut = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            self.imagesHaut[direction] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/ennemi/Uzi/uzi.png"), angle),(self.largeurCase, self.hauteurCase))
            #corp à corp
            self.imagesHaut["contact" + direction] = []
            for k in range(1,3):
                self.imagesHaut["contact" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/Uzi/uziContact{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #mort
            self.imagesHaut["meurt" + direction] = []
            for k in range(1,4):
                self.imagesHaut["meurt" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/Uzi/uziMeurt{k}.png"), angle),(self.largeurCase, self.hauteurCase)))

        self.imagesBas = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            #statique
            self.imagesBas["statique" + direction] =  pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/Uzi/statique.png"), angle),(self.largeurCase, self.hauteurCase))
            #marche avant
            self.imagesBas["avant" + direction] = []
            for k in range(1,5):
                self.imagesBas["avant" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/Uzi/avant{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #rechargement
            self.imagesHaut["reload" + direction] = []
            for k in range(1,5):
                self.imagesHaut["reload" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/ennemi/Uzi/uziReload{k}.png"), angle),(self.largeurCase, self.hauteurCase)))

        self.largeurCase, self.hauteurCase = self.game.largeurCase, self.game.hauteurCase
        self.direction = "Gauche"
        self.compteurFire = 0
        self.imageHautActuelle = self.imagesHaut["Gauche"]
        self.imageBasActuelle = self.imagesBas["statiqueGauche"]
        self.position = pos
        self.coords = self.position[0] * self.largeurCase, self.position[1] * self.hauteurCase
        self.enJoue = False
        self.vision = 15
        self.portee = 5
        self.joueur = self.game.joueur
        self.health = 30
        self.maxBusy = 35
        self.busy = 0
        self.projectiles = Liste()
        self.hand = "uzi"
        self.rect = self.imageHautActuelle.get_rect()
        self.dead = False
        self.contact = False
        self.pixel = self.joueur.pixel
        self.reloading = -1
        self.ammo = 25
        self.maxAmmo = 25
        self.dx = 0
        self.dy = 0
        self.traversable = False
        self.traversableB = True
        self.mooving = False
        self.screen = game.screen

    def __str__(self):
        return "🖓"

    def affichageMaj(self):
        """Cette fonction affiche et met a jour les variables qsui doivent l'être"""
        x = (self.game.largeurPlateau - 1) /2 * self.hauteurCase - self.game.joueur.coords[0] + self.coords[0] + 4*self.pixel[0]
        y = (self.game.hauteurPlateau - 1) /2 * self.largeurCase - self.game.joueur.coords[1] + self.coords[1] - 5*self.pixel[1]
        self.iA()
        #pygame.draw.rect(self.screen, "red", pygame.Rect(self.game.decor.coordsFond[0] + self.position[0] * self.largeurCase, self.game.decor.coordsFond[1] + self.position[1] * self.hauteurCase, self.largeurCase, self.hauteurCase))
        self.screen.blit(self.imageBasActuelle,(x, y))
        self.screen.blit(self.imageHautActuelle,(x, y))
        #gestion pour si le joueur tire
        if self.dx == 0 and self.dy == 0:
            self.dx = 1
    
    def majAngle(self):
        """Cette fonction met a jour l'affichage du haut du corp en fonction de la position du joueur"""
        pos = self.joueur.position[0], self.joueur.position[1]
        self.dx =  pos[0] - self.position[0]
        self.dy = pos[1] - self.position[1]
        if self.reloading <= 0:
            #gestion de l'image du haut du corp
            self.rads = atan2(-self.dy,self.dx)
            self.rads %= 2*pi
            self.imageHautActuelle = pygame.transform.rotate(self.imagesHaut["Droite"], degrees(self.rads))
        else:
            self.reloading -= 1
            self.animReload()

    def iA(self):
        """Fait se déplacer l'ennemi si nécéssaire et tire si c'est bon"""
        if self.contact and not self.dead:
            if self.busy <= 40/2:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][0]
            else:
                self.imageHautActuelle = self.imagesHaut["contact"+self.direction][1]
            self.busy -= 1
            if self.busy <= 0:
                self.contact = False
                self.joueur.contact()
                self.health = 0

        elif self.dead:
            #animation de mort
            if self.busy <= 40/3:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][2]
            elif self.busy <= (40/3) * 2:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][1]
            else:
                self.imageActuelle = self.imagesHaut["meurt"+self.direction][0]
            self.busy -= 1
            #fin de l'animation de mort
            if self.busy <= 0:
                self.tableau[self.position[1]][self.position[0]].supprVal(self)
                self.game.drop(self)
                self.game.score += self.game.rewardKill
                self.game.ennemis.supprVal(self)
        else:
            self.compteurFire -=1
            if self.health <= 0:
                self.dead = True
                self.busy = 40
                self.imageBasActuelle = self.imagesBas["statique" + self.direction]
            if self.enJoue and self.compteurFire <= 0:
                self.imagesBasActuelle = self.imagesBas["statique"+self.direction]
                self.feu()
                self.enJoue = False
            posJoueur = self.joueur.position
            posEnnemi = self.position
            difLargeur, difHauteur = posJoueur[0] - posEnnemi[0], posJoueur[1] - posEnnemi[1]
            if self.busy <= 0:
                #si il est a portée
                if sqrt(difHauteur**2 + difLargeur**2) < self.portee:
                    self.majAngle()
                    self.enJoue = True

                #si il est juste dans le champ de vision
                elif self.vision * -1 <= difHauteur <= self.vision and self.vision * -1 <= difLargeur <= self.vision:
                    self.majAngle()
                    if difHauteur <= 0:
                        if difLargeur <= 0:
                            self.direction = choice(["Haut", "Gauche"])
                        else:
                            self.direction = choice(["Haut", "Droite"])
                    else:
                        if difLargeur <= 0:
                            self.direction = choice(["Bas", "Gauche"])
                        else:
                            self.direction = choice(["Bas", "Droite"])
                    self.mooving = True
                #si l'ennemi ne sais pas ou est le joueur
                else:
                    if 0 < self.position[0] < self.game.largeurPlateau - 1:
                        direction = ["Gauche", "Droite"]
                    elif self.position[0] == 0:
                        direction = ["Droite"]
                    else:
                        direction = ["Gauche"]
                    if 0 < self.position[1] < self.game.hauteurPlateau - 1:
                        direction.append("Haut")
                        direction.append("Bas")
                    elif self.position[1] == 0:
                        direction.append("Bas")
                    else:
                        direction.append("Haut")
                    self.direction = choice(direction)
                    self.imageHautActuelle = self.imagesHaut[self.direction]
                    self.mooving = True
                   
                if self.verifDirection() and self.mooving:
                    if self.direction  == "Bas":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self) #met a jour le tableau
                        self.position = self.position[0], self.position[1] + 1             #met a jour les positions
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Haut":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0], self.position[1] - 1
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    elif self.direction == "Gauche":
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] - 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    else:
                        self.tableau[self.position[1]][self.position[0]].supprVal(self)
                        self.position = self.position[0] + 1, self.position[1]
                        self.tableau[self.position[1]][self.position[0]].append(self)
                    self.busy = self.maxBusy
                    self.mooving = False
                            
            else:
                self.mouvement()

    def verifDirection(self):
        """Cette fonction renvoie un booléen si le déplacement est possible ou non"""
        if self.direction == "Droite":
            if self.position[0] + 1 < self.game.largeurPlateau and self.game.tableau[self.position[1]][self.position[0] + 1].passable():
                return True
        elif self.direction == "Gauche":
            if self.position[0] > 0 and self.game.tableau[self.position[1]][self.position[0] - 1].passable():
                return True
        elif self.direction == "Haut":
            if self.position[1] > 0 and self.game.tableau[self.position[1] - 1][self.position[0]].passable():
                return True
        elif self.direction == "Bas":
            if self.position[1] + 1 < self.game.hauteurPlateau and self.game.tableau[self.position[1] + 1][self.position[0]].passable():
                return True
        return False

    def mouvement(self):
        """Cette fonction fait bouger l'ennemi"""
        deplLargeur = self.largeurCase/self.maxBusy
        deplHauteur = self.hauteurCase/self.maxBusy
        if self.direction == "Gauche":
            self.coords = self.coords[0] - deplLargeur, self.coords[1] 
        elif self.direction == "Droite":
            self.coords = self.coords[0] + deplLargeur, self.coords[1] 
        elif self.direction == "Haut":
            self.coords = self.coords[0], self.coords[1] - deplHauteur 
        else:
            self.coords = self.coords[0], self.coords[1] + deplHauteur
        
        if self.busy <= self.maxBusy/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= self.maxBusy/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][1]
        elif self.busy <= self.maxBusy/2:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][0]
        elif self.busy <= (self.maxBusy*2)/3:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        elif self.busy <= (self.maxBusy*5)/6:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][3]
        elif self.busy <= self.maxBusy:
            self.imageBasActuelle = self.imagesBas["avant"+self.direction][2]
        self.busy -= 1

    def touched(self, dmg):
        """Cette fonction modifie la vie quand il est touché par une balle"""
        self.health -= dmg
        if self.health < 0:
            self.health = 0
        self.game.tabSang.append(Sang(self))

    def feu(self):
        """Cette fonction fait tirer l'ennemi dans sa direction"""
        if self.compteurFire <= 0 and self.reloading <= 0:
            l = sqrt(self.dx**2 + self.dy**2)
            speedH = self.dx * 11 / l  #ici 12 correspond à la vitesse du projectile
            speedV = self.dy * 11 / l  
            self.game.projectiles.append(Bullet(25, self,1, speedH, speedV, False))
            self.compteurFire = 3
            self.ammo -= 1
            if self.ammo <= 0:
                self.reload()

    def reload(self):
        """redonne des munitions et active l'animation"""
        self.reloading = 40
        self.ammo = self.maxAmmo

    def animReload(self):
        """Cette fonction anime le rechergement de l'arme"""
        reloadingTime = 40
        if self.reloading <= 1:
            self.imageHautActuelle = self.imagesHaut[self.direction]
        elif self.reloading < reloadingTime / 4:
            self.imageHautActuelle = self.imagesHaut["reload"+ self.direction][3]
        elif self.reloading < reloadingTime / 2:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][2]
        elif self.reloading < reloadingTime * 3 / 4:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][1]
        else:
            self.imageHautActuelle = self.imagesHaut["reload" + self.direction][0]


