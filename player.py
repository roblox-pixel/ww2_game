#!/usr/bin/env python3
"""
Classe Joueur pour le jeu WW2
"""

from troop import Troop
import random


class Player:
    """
    Classe représentant un joueur
    """
    
    def __init__(self, name, start_pos, color):
        """
        Initialiser un joueur
        
        Args:
            name: Nom du joueur
            start_pos: Position de départ (x, y)
            color: Couleur du joueur (R, G, B)
        """
        self.name = name
        self.start_pos = start_pos
        self.color = color
        self.troops = []
        self.resources = 1000  # Ressources pour créer des troupes
        self.max_troops = 10
        
    def create_troop(self):
        """
        Créer une nouvelle troupe
        """
        if len(self.troops) < self.max_troops and self.resources >= 100:
            # Créer la troupe à proximité de la base
            offset_x = random.randint(-50, 50)
            offset_y = random.randint(-50, 50)
            pos = (self.start_pos[0] + offset_x, self.start_pos[1] + offset_y)
            
            troop = Troop(pos, self.color)
            self.troops.append(troop)
            self.resources -= 100
            return troop
        return None
    
    def update(self):
        """
        Mettre à jour le joueur et ses troupes
        """
        for troop in self.troops:
            troop.update()
        
        # Régénérer les ressources lentement
        self.resources = min(self.resources + 0.5, 2000)
    
    def get_total_strength(self):
        """
        Calculer la force totale du joueur
        """
        return sum(t.health for t in self.troops)
