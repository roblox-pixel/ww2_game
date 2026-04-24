#!/usr/bin/env python3
"""
WW2 Game Prototype - Point d'entrée principal
"""

import pygame
import sys
from game import Game


def main():
    """
    Fonction principale pour démarrer le jeu
    """
    # Initialiser Pygame
    pygame.init()
    
    # Créer l'instance du jeu
    game = Game()
    
    # Lancer la boucle principale
    game.run()
    
    # Quitter proprement
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
