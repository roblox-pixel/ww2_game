#!/usr/bin/env python3
"""
Boucle principale du jeu WW2
"""

import pygame
import sys
from player import Player
from map import GameMap
from ai_bot import AIBot
import random

# Constantes d'écran
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Game:
    """
    Classe principale du jeu
    """
    
    def __init__(self):
        """
        Initialiser le jeu
        """
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("WW2 Game - Prototype")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 24)
        self.font_large = pygame.font.Font(None, 36)
        
        # Initialiser la carte
        self.map = GameMap(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Créer le joueur
        self.player = Player("Player1", (100, 100), BLUE)
        
        # Créer les bots/IA
        self.bots = [
            AIBot("Bot1", (900, 100), RED),
            AIBot("Bot2", (900, 700), YELLOW),
            AIBot("Bot3", (100, 700), GREEN),
        ]
        
        # État du jeu
        self.selected_troop = None
        self.game_state = "playing"  # playing, paused, game_over
        self.players_connected = False  # À intégrer avec multijoueur
        
    def handle_events(self):
        """
        Gérer les événements de l'utilisateur
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # Créer une nouvelle troupe pour le joueur
                    self.player.create_troop()
                    
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic gauche
                    self.handle_left_click(event.pos)
                elif event.button == 3:  # Clic droit
                    self.handle_right_click(event.pos)
    
    def handle_left_click(self, pos):
        """
        Gérer le clic gauche (sélection)
        """
        # Chercher une troupe à sélectionner
        for troop in self.player.troops:
            if troop.rect.collidepoint(pos):
                self.selected_troop = troop
                return
    
    def handle_right_click(self, pos):
        """
        Gérer le clic droit (action)
        """
        if not self.selected_troop:
            return
        
        # Vérifier les collisions avec les troupes ennemies
        target_found = False
        
        # Vérifier les bots
        for bot in self.bots:
            for bot_troop in bot.troops:
                if bot_troop.rect.collidepoint(pos):
                    # Attaquer la troupe ennemie
                    self.selected_troop.attack(bot_troop)
                    target_found = True
                    break
            if target_found:
                break
        
        # Si pas de cible, se déplacer
        if not target_found:
            self.selected_troop.move_to(pos)
    
    def update(self):
        """
        Mettre à jour la logique du jeu
        """
        # Mettre à jour le joueur
        self.player.update()
        
        # Mettre à jour les bots
        for bot in self.bots:
            bot.update(self.player, self.bots)
        
        # Vérifier les collisions d'attaque
        self.check_attacks()
        
        # Supprimer les troupes mortes
        self.clean_dead_troops()
        
        # Vérifier l'état du jeu
        self.check_game_state()
    
    def check_attacks(self):
        """
        Vérifier si les attaques touchent leurs cibles
        """
        # Attaques du joueur
        for troop in self.player.troops:
            if troop.is_attacking and troop.target:
                if troop.rect.colliderect(troop.target.rect):
                    troop.target.take_damage(troop.damage)
                    troop.is_attacking = False
        
        # Attaques des bots
        for bot in self.bots:
            for troop in bot.troops:
                if troop.is_attacking and troop.target:
                    if troop.rect.colliderect(troop.target.rect):
                        troop.target.take_damage(troop.damage)
                        troop.is_attacking = False
    
    def clean_dead_troops(self):
        """
        Supprimer les troupes avec 0 PV
        """
        self.player.troops = [t for t in self.player.troops if t.health > 0]
        for bot in self.bots:
            bot.troops = [t for t in bot.troops if t.health > 0]
    
    def check_game_state(self):
        """
        Vérifier l'état du jeu
        """
        # Si le joueur n'a plus de troupes, game over
        if len(self.player.troops) == 0:
            self.game_state = "game_over"
    
    def draw(self):
        """
        Dessiner tous les éléments du jeu
        """
        self.screen.fill(BLACK)
        
        # Dessiner la carte
        self.map.draw(self.screen)
        
        # Dessiner les troupes du joueur
        for troop in self.player.troops:
            troop.draw(self.screen)
            # Mettre en évidence la troupe sélectionnée
            if troop == self.selected_troop:
                pygame.draw.circle(self.screen, WHITE, troop.rect.center, troop.radius + 5, 2)
        
        # Dessiner les troupes des bots
        for bot in self.bots:
            for troop in bot.troops:
                troop.draw(self.screen)
        
        # Dessiner l'UI
        self.draw_ui()
        
        pygame.display.flip()
    
    def draw_ui(self):
        """
        Dessiner l'interface utilisateur
        """
        # Informations du joueur
        player_text = self.font.render(f"Joueur: {len(self.player.troops)} troupes", True, BLUE)
        self.screen.blit(player_text, (10, 10))
        
        # Informations des bots
        y_offset = 40
        for bot in self.bots:
            bot_text = self.font.render(f"{bot.name}: {len(bot.troops)} troupes", True, bot.color)
            self.screen.blit(bot_text, (10, y_offset))
            y_offset += 30
        
        # Contrôles
        controls_text = self.font.render("ESPACE: Créer troupe | Clic G: Sélectionner | Clic D: Attaquer/Déplacer", True, WHITE)
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))
        
        # État de la troupe sélectionnée
        if self.selected_troop:
            health_bar_x = 10
            health_bar_y = SCREEN_HEIGHT - 60
            health_bar_width = 200
            health_bar_height = 20
            
            # Barre de fond
            pygame.draw.rect(self.screen, RED, (health_bar_x, health_bar_y, health_bar_width, health_bar_height))
            
            # Barre de santé
            health_percentage = self.selected_troop.health / self.selected_troop.max_health
            pygame.draw.rect(self.screen, GREEN, (health_bar_x, health_bar_y, health_bar_width * health_percentage, health_bar_height))
            
            # Texte de santé
            health_text = self.font.render(f"PV: {self.selected_troop.health}/{self.selected_troop.max_health}", True, WHITE)
            self.screen.blit(health_text, (health_bar_x + 210, health_bar_y))
    
    def run(self):
        """
        Boucle principale du jeu
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
