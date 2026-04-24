#!/usr/bin/env python3
"""
Gestion de la carte du jeu WW2
"""

import pygame


class GameMap:
    """
    Classe représentant la carte du jeu
    """
    
    def __init__(self, width, height):
        """
        Initialiser la carte
        
        Args:
            width: Largeur de la carte
            height: Hauteur de la carte
        """
        self.width = width
        self.height = height
        self.territories = self.create_territories()
    
    def create_territories(self):
        """
        Créer les territoires de la carte
        
        Returns:
            Liste des territoires
        """
        territories = [
            {"name": "Base Nord-Ouest", "pos": (100, 100), "size": 80, "color": (50, 50, 100)},
            {"name": "Base Nord-Est", "pos": (1100, 100), "size": 80, "color": (50, 50, 100)},
            {"name": "Base Sud-Ouest", "pos": (100, 700), "size": 80, "color": (50, 50, 100)},
            {"name": "Base Sud-Est", "pos": (1100, 700), "size": 80, "color": (50, 50, 100)},
            {"name": "Zone centrale", "pos": (600, 400), "size": 150, "color": (30, 60, 30)},
        ]
        return territories
    
    def draw(self, screen):
        """
        Dessiner la carte
        
        Args:
            screen: Surface Pygame
        """
        # Dessiner les territoires
        for territory in self.territories:
            pygame.draw.circle(
                screen,
                territory["color"],
                territory["pos"],
                territory["size"],
                1
            )
            
            # Dessiner le nom du territoire
            font = pygame.font.Font(None, 14)
            text = font.render(territory["name"], True, (200, 200, 200))
            screen.blit(text, (territory["pos"][0] - 40, territory["pos"][1] - 10))
        
        # Dessiner la grille
        self.draw_grid(screen)
    
    def draw_grid(self, screen):
        """
        Dessiner une grille de référence
        
        Args:
            screen: Surface Pygame
        """
        grid_size = 100
        light_grey = (40, 40, 40)
        
        # Lignes verticales
        for x in range(0, self.width, grid_size):
            pygame.draw.line(screen, light_grey, (x, 0), (x, self.height), 1)
        
        # Lignes horizontales
        for y in range(0, self.height, grid_size):
            pygame.draw.line(screen, light_grey, (0, y), (self.width, y), 1)
