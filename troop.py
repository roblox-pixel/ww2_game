#!/usr/bin/env python3
"""
Classe Troupe pour le jeu WW2
"""

import pygame
import math


class Troop:
    """
    Classe représentant une unité militaire
    """
    
    def __init__(self, pos, color):
        """
        Initialiser une troupe
        
        Args:
            pos: Position initiale (x, y)
            color: Couleur de la troupe (R, G, B)
        """
        self.x, self.y = pos
        self.color = color
        self.radius = 10
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)
        
        # Propriétés de combat
        self.health = 100
        self.max_health = 100
        self.damage = 10
        self.speed = 2
        self.range = 100
        
        # État
        self.is_attacking = False
        self.target = None
        self.target_pos = None
        
    def move_to(self, pos):
        """
        Se déplacer vers une position
        
        Args:
            pos: Position cible (x, y)
        """
        self.target_pos = pos
        self.target = None
        self.is_attacking = False
    
    def attack(self, target_troop):
        """
        Attaquer une troupe ennemie
        
        Args:
            target_troop: Troupe à attaquer
        """
        self.target = target_troop
        self.is_attacking = True
    
    def take_damage(self, damage):
        """
        Subir des dégâts
        
        Args:
            damage: Montant des dégâts
        """
        self.health = max(0, self.health - damage)
    
    def update(self):
        """
        Mettre à jour la troupe
        """
        if self.target and self.target.health > 0:
            # Si une cible existe, aller vers elle
            self.move_towards(self.target.x, self.target.y)
        elif self.target_pos:
            # Sinon, aller vers la position cible
            self.move_towards(self.target_pos[0], self.target_pos[1])
        
        # Mettre à jour le rect
        self.rect.x = self.x - self.radius
        self.rect.y = self.y - self.radius
    
    def move_towards(self, target_x, target_y):
        """
        Se déplacer vers une position cible
        
        Args:
            target_x: Coordonnée X cible
            target_y: Coordonnée Y cible
        """
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > self.speed:
            # Se déplacer vers la cible
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
        else:
            # Arrêté à la cible
            self.target_pos = None
    
    def draw(self, screen):
        """
        Dessiner la troupe
        
        Args:
            screen: Surface Pygame
        """
        # Dessiner le cercle de la troupe
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Dessiner la barre de santé au-dessus
        health_bar_width = 20
        health_bar_height = 4
        health_bar_x = self.x - health_bar_width / 2
        health_bar_y = self.y - self.radius - 10
        
        # Barre de fond (rouge)
        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
        
        # Barre de santé (vert)
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))
        
        # Dessiner un contour si en train d'attaquer
        if self.is_attacking:
            pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), self.radius + 3, 1)
