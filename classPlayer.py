import pygame
from classBullet import Bullet
from classSang import Sang
from math import atan2, pi, sqrt, cos , sin, degrees
from classItem import Arme
pygame.font.init()

class Player:
    def __init__(self, game):
        self.game = game
        armes = ["ar","pistolet","uzi", "fusilAPompe", "sniper"]
        self.tableau = self.game.tableau
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        #import des images et retournement si nécéssaire
        #haut du corp
        self.imagesHaut = {}
        #       self.imageHaut[arme + direction] [étape dans l'animation ssi arme == "" or arme == "contact"]
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            self.imagesHaut["sniperSemiReload" + direction] = []
            for k in range(1,4):
                self.imagesHaut["sniperSemiReload" + direction].append(pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/snipersemiReload{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
        #images pour chaque armes et chaque directions
        for arme in armes:
            for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
                self.imagesHaut[arme + direction] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/joueur/"+ arme + ".png"), angle),(self.largeurCase, self.hauteurCase))
            for direction, angle in [("HautDroite", 0), ("HautGauche", 90), ("BasGauche", 180), ("BasDroite", -90)]:
                self.imagesHaut[arme + direction] = pygame.transform.scale(pygame.transform.rotate(pygame.image.load("assets/joueur/"+ arme + "_45.png"), angle),(self.largeurCase, self.hauteurCase))

        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            #corp à corp
            self.imagesHaut["contact" + direction] = []
            for k in range(1,3):
                self.imagesHaut["contact" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/contact{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #mort
            self.imagesHaut["meurt" + direction] = []
            for k in range(1,5):
                self.imagesHaut["meurt" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/meurt{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #courir sans arme
            self.imagesHaut[direction] = []
            for k in range(1,5):
                self.imagesHaut[direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/marche{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #rechergement
            for arme in armes:
                self.imagesHaut["reload" + arme + direction] = []
                for k in range(1,5):
                    self.imagesHaut["reload" + arme + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/{arme}Reload{k}.png"), angle),(self.largeurCase, self.hauteurCase)))


        self.imageHautActuelle = self.imagesHaut["Droite"][0]
        #partie jambes
        self.imagesBas = {}
        for direction, angle in [("Haut", 90), ("Bas", -90), ("Gauche", 180), ("Droite", 0)]:
            #statique
            self.imagesBas["statique" + direction] =  pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/statique.png"), angle),(self.largeurCase, self.hauteurCase))
            #marche avant
            self.imagesBas["avant" + direction] = []
            for k in range(1,5):
                self.imagesBas["avant" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/avant{k}.png"), angle),(self.largeurCase, self.hauteurCase)))
            #pas chassés
            self.imagesBas["cote" + direction] = []
            for k in range(1,4):
                self.imagesBas["cote" + direction].append( pygame.transform.scale(pygame.transform.rotate(pygame.image.load(f"assets/joueur/cote{k}.png"), angle + 90),(self.largeurCase, self.hauteurCase)))

        self.imageBasActuelle = self.imagesBas["statiqueDroite"]
        self.largeurCase, self.hauteurCase = int(self.game.largeurCase), int(self.game.hauteurCase)
        self.direction = "Droite"
        self.position = (3,17)
        self.coords = self.position[0] * self.largeurCase, self.position[1] * self.hauteurCase
        #self.tableau[self.position[1]][self.position[0]].append(self)
        self.isMooving = False
        self.busy = 0
        self.hand = ""
        self.maxBusy = 10   #à modifier pour changer vitesse du joueur (nbr d'étape pour l'animation)
        self.slot = ["ar","fusilAPompe",""]
        self.slotActif = 2
        self.compteurFire = 0
        self.traversable = False
        self.traversableB = True
        #gestion bar de vie
        self.max_health = 100
        self.health = self.max_health
        self.dead = False
        self.pixel = self.largeurCase/20, self.hauteurCase/20
        self.rect = self.imageHautActuelle.get_rect()
        #visée a la souris
        self.directionVision = "Droite"
        self.dx = 1
        self.dy = 0
        self.rads = 0
        self.compteurContact = 0
        #gestion munitions
        self.maxAmmo = {"uzi" : 25, "ar" : 30, "pistolet" : 6, "fusilAPompe" : 2, "" : 0, "sniper" : 6 }
        self.magazine = self.maxAmmo.copy()
        self.ammo = {"uzi" : 75, "ar" : 90, "pistolet" : 18, "fusilAPompe" : 6, "" : 0, "sniper" : 18}
        self.changed = False #si changement d'arme
        self.reloading = -1
        self.semiReloading = -1
        #affichage de l'interface des armes
        self.imageArme = {}
        for arme in armes + ["poing", "cadre"]:
            self.imageArme[arme] = pygame.transform.scale(pygame.image.load(f"assets/{arme}.png"),(round(1.4 * self.largeurCase),round(1.4 * self.hauteurCase)))

    def __str__(self):
        return "🔫"

    def verifDirection(self, direction):
        """Cette fonction renvoie un booléen si le déplacement est possible ou non"""
        if direction == "Droite":
            if self.game.tableau[self.position[1]][self.position[0] + 1].passable():
                return True
        elif direction == "Gauche":
            if self.game.tableau[self.position[1]][self.position[0] - 1].passable():
                return True
        elif direction == "Haut":
            if self.game.tableau[self.position[1] - 1][self.position[0]].passable():
                return True
        elif direction == "Bas":
            if self.game.tableau[self.position[1] + 1][self.position[0]].passable():
                return True
        return False

    def affichage(self):
        """Cette fonction affiche l'image du joueur, et permet l'affichage des munitions"""
        if self.dead:
            self.health = 0
        self.compteurFire -= 1

        #application du changement de vitesse par l'arme
        if self.changed != False and self.busy <= 0:
           self.maxBusy = self.changed
           self.changed = False 

        #affichage du corp
        self.game.screen.blit(self.imageBasActuelle, ((self.game.largeurPlateau - 1) /2 * self.largeurCase, (self.game.hauteurPlateau - 1) /2 * self.hauteurCase))
        self.game.screen.blit(self.imageHautActuelle, ((self.game.largeurPlateau - 1) /2 * self.largeurCase, (self.game.hauteurPlateau - 1) /2 * self.hauteurCase))
        #gestion de la vie
        if self.health <= 0 and not self.busy:
            self.dead = True
            self.busy = 120
            print("you loose !")
        if self.game.compteur % 15 == 0 and self.health < self.max_health and not self.dead:
            self.health += 0.125
            if self.health > self.max_health:
                self.health = self.max_health
        #affichage de la barre de vie
        pygame.draw.rect(self.game.screen, (203, 150, 150), pygame.Rect(self.pixel[0] * 130, 10.5* self.hauteurCase, self.pixel[0] * 120, 6 * self.pixel[1]))
        pourcentageVie = (self.health / self.max_health) * 120 * self.pixel[0]
        pygame.draw.rect(self.game.screen, (5, 135, 0), pygame.Rect(self.pixel[0] * 130, 10.5* self.hauteurCase,  pourcentageVie, 6 * self.pixel[1]))
        #items au sol
        for elmt in self.game.loot:
            if elmt.position == self.position:
                if type(elmt) is Arme :
                    if self.game.pressed[pygame.K_e]:
                        elmt.picked()
                else:
                    elmt.picked()
        #rechargement
        self.reloading -= 1
        if self.reloading >= 0:
            self.animReload()
        if self.compteurFire >= 0 and self.hand == "sniper":
            self.animSemiReload()

    def afficheArmes(self):
        """Cette fonction affiche les armes dans l'interface"""
        for decalage, arme in [(1, self.slot[0]), (2, self.slot[1]), (3, "poing")]:
            #affichage du cadre gris à ajouter
            self.game.screen.blit(self.imageArme[arme],( decalage * 1.65 * self.largeurCase, 9.6 *self.game.hauteurCase))
        self.game.screen.blit(self.imageArme["cadre"],((self.slotActif + 1) * 1.65 * self.largeurCase,  9.6 *self.game.hauteurCase,))

    def afficheAmmo(self):
        """Cette fonction affiche les munitions du joueur"""
        myfont = pygame.font.SysFont('Impact', self.game.screen.get_width() // 45)
        textsurface = myfont.render(f"{self.magazine[self.hand]} / {self.ammo[self.hand]}", False, (255, 255, 255))
        self.game.screen.blit(textsurface,(self.largeurCase * 0.1, 10* self.hauteurCase,))
    
    def reload(self):
        """Cette fonction fait recharger le joueur et change les variable en question"""
        if self.reloading <= 0:
            if self.ammo[self.hand] < self.maxAmmo[self.hand]:
                self.magazine[self.hand] = self.ammo[self.hand]
                self.ammo[self.hand] = 0
            else:
                self.ammo[self.hand] +=  self.magazine[self.hand]
                self.ammo[self.hand] -= self.maxAmmo[self.hand]
                self.magazine[self.hand] = self.maxAmmo[self.hand]
                self.reloading = {"fusilAPompe":30, "ar":40, "pistolet":35, "uzi":30, "sniper" : 120}[self.hand]
       
    def animReload(self):
        """Cette fonction anime le rechergement de l'arme"""
        reloadingTime = {"fusilAPompe":30, "ar":40, "pistolet":35, "uzi":30, "sniper" : 120}[self.hand]
        if self.reloading <= 1:
            self.imageHautActuelle = self.imagesHaut[self.hand + self.directionVision]
        elif self.reloading < reloadingTime / 4:
            self.imageHautActuelle = self.imagesHaut["reload" + self.hand + self.directionVision][3]
        elif self.reloading < reloadingTime / 2:
            self.imageHautActuelle = self.imagesHaut["reload" + self.hand + self.directionVision][2]
        elif self.reloading < reloadingTime * 3 / 4:
            self.imageHautActuelle = self.imagesHaut["reload" + self.hand + self.directionVision][1]
        else:
            self.imageHautActuelle = self.imagesHaut["reload" + self.hand + self.directionVision][0]

    def animSemiReload(self):
        """Cette fonction anime le sniper entre les tirs"""
        reloadingTime = 55
        if self.compteurFire <= 1:
            self.imageHautActuelle = self.imagesHaut[self.hand + self.directionVision]
        elif self.compteurFire < reloadingTime / 3:
            self.imageHautActuelle = self.imagesHaut["sniperSemiReload" + self.direction][2]
        elif self.compteurFire < reloadingTime / 1.5:
            self.imageHautActuelle = self.imagesHaut["sniperSemiReload" + self.direction][1]
        else:
            self.imageHautActuelle = self.imagesHaut["sniperSemiReload" + self.direction][0]

    def droite(self):
        """Cette fonction définis les variables pour un déplacement a droite"""
        if self.verifDirection("Droite"):
            self.tableau[self.position[1]][self.position[0]].supprVal(self)
            self.position = self.position[0] + 1, self.position[1]
            self.tableau[self.position[1]][self.position[0]].append(self)
            self.busy = self.maxBusy
            self.direction = "Droite"
            if self.hand == "":
                self.directionVision = "Droite"

    def gauche(self):
        """Cette fonction définis les variables pour un déplacement a gauche"""
        if self.verifDirection("Gauche"):
            self.tableau[self.position[1]][self.position[0]].supprVal(self)
            self.position = self.position[0] - 1, self.position[1]
            self.tableau[self.position[1]][self.position[0]].append(self)
            self.busy = self.maxBusy
            self.direction = "Gauche"
            if self.hand == "":
                self.directionVision = "Gauche"

    def haut(self):
        """Cette fonction définis les variables pour un déplacement en haut"""
        if self.verifDirection("Haut"):
            self.tableau[self.position[1]][self.position[0]].supprVal(self)
            self.position = self.position[0], self.position[1] - 1
            self.tableau[self.position[1]][self.position[0]].append(self)
            self.busy = self.maxBusy
            self.direction = "Haut"
            if self.hand == "":
                self.directionVision = "Haut"

    def bas(self):
        """Cette fonction définis les variables pour un déplacement en bas"""
        if self.verifDirection("Bas"):
            self.tableau[self.position[1]][self.position[0]].supprVal(self)
            self.position = self.position[0], self.position[1] + 1
            self.tableau[self.position[1]][self.position[0]].append(self)
            self.busy = self.maxBusy
            self.direction = "Bas"
            if self.hand == "":
                self.directionVision = "Bas"
    
    def mouvement(self):
        """Cette fonction continue le mouvement du personnage pour qu'il se déplace "brique par brique" """
        #si le joueur à perdu (animation)
        if self.dead:
            if self.busy <= 30:
                self.imageHautActuelle = self.imagesHaut["meurt" + self.directionVision][3]
            elif self.busy <= 60:
                self.imageHautActuelle = self.imagesHaut["meurt" + self.directionVision][2]
            elif self.busy <= 90:
                self.imageHautActuelle = self.imagesHaut["meurt" + self.directionVision][1]
            else:
                self.imageHautActuelle = self.imagesHaut["meurt" + self.directionVision][0]
            if self.busy != 3:
                self.busy -= 1
            else:
                self. busy = 10

        #si le joueur est au contact
        elif self.compteurContact > 0 :
            if self.compteurContact <= 15:
                self.imageHautActuelle = self.imagesHaut["contact" + self.direction][0]
            else:
                self.imageHautActuelle = self.imagesHaut["contact" + self.direction][1]
            self.compteurContact -= 1

            
        else:
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


            #gestion des pas
            if self.busy <= self.maxBusy/6:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][0]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][0]
            elif self.busy <= self.maxBusy/3:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][1]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][1]
            elif self.busy <= self.maxBusy/2:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][0]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][0]
            elif self.busy <= self.maxBusy/6 * 4:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][2]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][2]
            elif self.busy <= self.maxBusy/6 * 5:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][3]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][3]
            elif self.busy <= self.maxBusy:
                self.imageBasActuelle = self.imagesBas["avant" + self.direction][2]
                if self.hand == "":
                    self.imageHautActuelle = self.imagesHaut[self.direction][2]
            self.busy -= 1
     
    def statique(self):
        """Cette fonction met a jour l'image du joueur quand il ne bouge pas ou plus en fonction de son arme"""
        self.imageBasActuelle = self.imagesBas["statique" + self.direction]
        self.direction = self.directionVision

    def changeArme(self, n):
        """cette fonction fait changer l'arme acutelle du joueur sur celle dans le "slot" n°1
        n - int - le numéro du slot (entre 0 et 1) """
        if self.reloading <= 0:
            self.hand = self.slot[n]
            self.changed = {"ar": 18 , "fusilAPompe":15 , "uzi":14 , "pistolet":12 , "":10, "sniper" : 28}[self.hand] #vitesse selon l'arme
            if self.hand == "":
                self.directionVision = self.direction
                self.imageHautActuelle = self.imagesHaut[self.direction][0]
            else:
                self.imageHautActuelle = self.imagesHaut[self.hand + self.directionVision]
            self.slotActif = n

    def majAngle(self):
        """Cette fonction met a jour l'angle de tire et éventuellement le regard du joueur si besoin"""
        """
        if self.hand =="" or self.dead or self.reloading >= 0:
            return
        else:
            #gestion pour si le joueur tire
            pos = pygame.mouse.get_pos() 
            self.dx = pos[0] - (self.game.largeurPlateau - 1) /2 * self.largeurCase - 10*self.pixel[0]
            self.dy = pos[1] - (self.game.hauteurPlateau - 1) /2 * self.hauteurCase - 10*self.pixel[1]
            if self.dx == 0 and self.dy == 0:
                self.dx = 1
            #gestion de l'image du haut du corp
            self.rads = atan2(-self.dy,self.dx)
            self.rads %= 2*pi
            if self.rads <= pi/6:
                self.imageHautActuelle = self.imagesHaut[self.hand + "Droite"]
            elif self.rads <= pi/3:
                self.imageHautActuelle = self.imagesHaut[self.hand + "HautDroite"]
            elif self.rads <= 2*pi/3:
                self.imageHautActuelle = self.imagesHaut[self.hand + "Haut"]
            elif self.rads <= 5*pi/6:
                self.imageHautActuelle = self.imagesHaut[self.hand + "HautGauche"]
            elif self.rads <= 7*pi/6:
                self.imageHautActuelle = self.imagesHaut[self.hand + "Gauche"]
            elif self.rads <= 4*pi/3:
                self.imageHautActuelle = self.imagesHaut[self.hand + "BasGauche"]
            elif self.rads <= 5*pi/3:
                self.imageHautActuelle = self.imagesHaut[self.hand + "Bas"]
            elif self.rads <= 11*pi/6:
                self.imageHautActuelle = self.imagesHaut[self.hand + "BasDroite"]
            else:
                self.imageHautActuelle = self.imagesHaut[self.hand + "Droite"]"""
        if self.hand =="" or self.dead or self.reloading >= 0:
            return
        else:
            #gestion pour si le joueur tire
            pos = pygame.mouse.get_pos() 
            self.dx = pos[0] - (self.game.largeurPlateau - 1) /2 * self.largeurCase - 10*self.pixel[0]
            self.dy = pos[1] - (self.game.hauteurPlateau - 1) /2 * self.hauteurCase - 10*self.pixel[1]
            if self.dx == 0 and self.dy == 0:
                self.dx = 1
            #gestion de l'image du haut du corp
            self.rads = atan2(-self.dy,self.dx)
            self.rads %= 2*pi
            self.imageHautActuelle = pygame.transform.rotate(self.imagesHaut[self.hand + "Droite"], degrees(self.rads))

    def touched(self, dmg):
        """Cette fonction modifie la vie quand il est touché par une balle"""
        self.health -= dmg
        if self.health < 0:
            self.health = 0
        self.game.tabSang.append(Sang(self))

    def contact(self):
            if self.compteurContact <= 0:
                self.health -= 45
                self.compteurContact = 30

    def feu(self):
        """Cette fonction fait tirer le joueur selon l'arme qu'il utilise"""
        if self.hand == "sniper" and self.compteurFire >= 0:
            return
            
        self.majAngle()
        if self.compteurFire <= 0 and self.reloading <= 0:
            if self.magazine[self.hand] <= 0:
                if self.ammo[self.hand] > 0:
                    self.reload()
                else:
                    return #bruit de plus de balles
            else:
                #calcul hypoténuse avec souris
                l = sqrt(self.dx**2 + self.dy**2)
                if self.hand == "pistolet":
                    self.compteurFire = 48
                    speedH = self.dx * 14 / l  #ici 14 correspond à la vitesse du projectile
                    speedV = self.dy * 14 / l  
                    self.game.projectiles.append(Bullet(10, self, 25, speedH, speedV, True))
                elif self.hand == "ar":
                    self.compteurFire = 12
                    speedH = self.dx * 15 / l  #ici 10 correspond à la vitesse du projectile
                    speedV = self.dy * 15 / l  
                    self.game.projectiles.append(Bullet(15, self, 20, speedH, speedV, True))
                elif self.hand == "uzi":
                    self.compteurFire = 3
                    speedH = self.dx * 12 / l  #ici 12 correspond à la vitesse du projectile
                    speedV = self.dy * 12 / l 
                    self.game.projectiles.append(Bullet(6, self, 8, speedH, speedV, True))
                elif self.hand == "fusilAPompe":
                    for rads in [-self.rads + (pi/2), -self.rads + (pi/2) + pi/12, -self.rads + (pi/2) - pi/12]:
                        self.game.projectiles.append(Bullet(5,self,25, 8*sin(rads), -8*cos(rads), True))
                        self.compteurFire = 40
                elif self.hand == "sniper":
                    self.compteurFire = 55
                    speedH = self.dy * 30 / l  #ici 22 correspond à la vitesse du projectile
                    speedV = self.dx * 30 / l 
                    self.game.projectiles.append(Bullet(32, self, 100, speedH, speedV, True))
                self.magazine[self.hand] -= 1


                