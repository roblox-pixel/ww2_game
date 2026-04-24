#!/usr/bin/env python3
"""
Système d'IA pour les bots du jeu WW2
"""

from player import Player
import random
import math


class AIBot(Player):
    """
    Classe représentant un bot contrôlé par l'IA
    """
    
    def __init__(self, name, start_pos, color):
        """
        Initialiser un bot IA
        
        Args:
            name: Nom du bot
            start_pos: Position de départ
            color: Couleur du bot
        """
        super().__init__(name, start_pos, color)
        self.update_counter = 0
        self.decision_interval = 30  # Prendre une décision tous les 30 frames
        self.aggressiveness = random.uniform(0.5, 1.5)  # Niveau d'agressivité
        
    def update(self, player, other_bots):
        """
        Mettre à jour le bot et son IA
        
        Args:
            player: Instance du joueur principal
            other_bots: Liste des autres bots
        """
        # Mettre à jour les troupes
        super().update()
        
        self.update_counter += 1
        
        # Prendre une décision tous les X frames
        if self.update_counter >= self.decision_interval:
            self.update_counter = 0
            self.make_decision(player, other_bots)
    
    def make_decision(self, player, other_bots):
        """
        Prendre une décision d'attaque ou de création de troupe
        
        Args:
            player: Instance du joueur principal
            other_bots: Liste des autres bots
        """
        # Créer une nouvelle troupe si ressources suffisantes
        if random.random() < 0.3 and self.resources >= 100:
            self.create_troop()
        
        # Attaquer les ennemis proches
        self.attack_nearby_enemies(player, other_bots)
    
    def attack_nearby_enemies(self, player, other_bots):
        """
        Attaquer les ennemis proches
        
        Args:
            player: Instance du joueur principal
            other_bots: Liste des autres bots
        """
        for troop in self.troops:
            # Si la troupe ne cible personne
            if not troop.is_attacking or not troop.target or troop.target.health <= 0:
                # Chercher une cible à proximité
                target = self.find_closest_enemy(troop, player, other_bots)
                if target:
                    troop.attack(target)
    
    def find_closest_enemy(self, troop, player, other_bots):
        """
        Trouver l'ennemi le plus proche
        
        Args:
            troop: Troupe qui cherche une cible
            player: Instance du joueur principal
            other_bots: Liste des autres bots
            
        Returns:
            La troupe ennemie la plus proche ou None
        """
        closest_enemy = None
        closest_distance = float('inf')
        
        # Vérifier les troupes du joueur
        for enemy_troop in player.troops:
            distance = math.sqrt((troop.x - enemy_troop.x)**2 + (troop.y - enemy_troop.y)**2)
            if distance < closest_distance and distance < troop.range * self.aggressiveness:
                closest_enemy = enemy_troop
                closest_distance = distance
        
        # Vérifier les troupes des autres bots
        for bot in other_bots:
            if bot == self:
                continue
            for enemy_troop in bot.troops:
                distance = math.sqrt((troop.x - enemy_troop.x)**2 + (troop.y - enemy_troop.y)**2)
                if distance < closest_distance and distance < troop.range * self.aggressiveness:
                    closest_enemy = enemy_troop
                    closest_distance = distance
        
        return closest_enemy
