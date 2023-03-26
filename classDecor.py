import pygame
from maps import tabMap0

class Decor:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.largeurPlateau, self.hauteurPlateau = game.largeurPlateau, game.hauteurPlateau
        self.largeurCase, self.hauteurCase = game.largeurCase, game.hauteurCase
        self.imageFond = pygame.transform.scale(pygame.image.load("assets/maps/map0.png"),(int( 31 *self.largeurCase),int(self.hauteurCase * 20)))
        self.coordsFond = self.screen.get_width()/2 - self.game.joueur.coords[0] , self.screen.get_height()/2 - self.game.joueur.coords[1]

    def majAffichage(self):
        """Cette fonction affiche le fond et met a jour sa place"""
        pygame.draw.rect(self.screen, (105,105,105), pygame.Rect(0,0, self.screen.get_width(), self.screen.get_height()))
        #affichage plateau
        self.screen.blit(self.imageFond, self.coordsFond)
        #déplacement du fond en fonction de la position du joueur
        self.coordsFond = self.screen.get_width()/2 - self.game.joueur.coords[0] - self.largeurCase/2 , self.screen.get_height()/2 - self.game.joueur.coords[1] - self.hauteurCase/2

    


        

