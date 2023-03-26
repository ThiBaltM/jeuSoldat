import pygame
from classGame import Game

#initialisation valeurs plateau
largeurEcran, hauteurEcran = (1280, 720)
#paramétrage de l'affichage
screen = pygame.display.set_mode((largeurEcran,hauteurEcran))

clock = pygame.time.Clock()
FPS = 60

isRunning = True

game = Game(screen)

while isRunning:

    clock.tick(FPS)
    #gestion des touches
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.KEYDOWN:
            game.pressed[event.key] = True
        elif event.type == pygame.KEYUP:
            game.pressed[event.key] = False
        elif event.type == pygame.QUIT: #fermeture de la page
            game.saveScore()
            isRunning = False
        elif event.type == pygame.MOUSEMOTION:
            game.joueur.majAngle()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.pressed[event.button] = True
        elif event.type == pygame.MOUSEBUTTONUP:
            game.pressed[event.button] = False
    game.update()
    pygame.display.flip()

"""Je m'appelle Jules MEURIN j'ai 17ans, je suis en terminale au moment ou je code, soit en avril 2021.
V1: millieu avril - début mai
    -moteur de jeu

V2: 13 mai - 29 mai
    -refonte graphique
    -interface
    -munitions
    -items
    -visée multidirectionnel
    -collisions
    -nouvelles armes
    -suppressions des attaques au corp à corp

V3: 29 mai - ...
    - création et mise en place de maps définis
    - rotation du corp fluidifiée
    - attaques au corp a corp
    """

"""encore a faire:
- attaques au corp à corp
-faire en sorte que les tentes fassent spawn des ennemis
- ajouts des ennemis sur le tableau
"""         