# WW2 Game Prototype

Un jeu de stratégie militaire WW2 en temps réel développé avec Pygame.

## Fonctionnalités

- 🎮 Contrôle de troupes à la souris
- ⚔️ Système d'attaque contre d'autres pays
- 👥 Mode multijoueur (détection des joueurs connectés)
- 🤖 Mode solo contre des IA/bots
- 📊 Gestion des ressources et des troupes
- 🌍 Carte stratégique avec territoires

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/roblox-pixel/ww2_game.git
cd ww2_game

# Installer les dépendances
pip install -r requirements.txt
```

## Démarrage

```bash
python main.py
```

## Structure du Projet

```
ww2_game/
├── main.py              # Point d'entrée
├── game.py              # Boucle de jeu principale
├── player.py            # Classe Joueur
├── troop.py             # Classe Troupes
├── ai_bot.py            # Système d'IA
├── map.py               # Gestion de la carte
├── requirements.txt     # Dépendances
└── README.md            # Documentation
```

## Contrôles

- **Clic gauche** : Sélectionner une troupe
- **Clic droit** : Attaquer ou se déplacer
- **ESC** : Quitter

## Architecture

### Mode de Jeu
- Si des joueurs sont connectés → Mode multijoueur PvP
- Sinon → Mode solo avec bots contrôlés par l'IA

### Système de Troupes
- Chaque joueur peut créer et contrôler plusieurs unités militaires
- Les troupes peuvent attaquer, se défendre ou se déplacer

### Système d'IA
- Les bots prennent des décisions d'attaque/défense automatiquement
- Stratégie adaptée aux ressources disponibles

## Développement

Ce projet est en phase de prototype. Les fonctionnalités principales sont :
- [ ] Interface graphique de base
- [ ] Système de troupes
- [ ] Mécanique d'attaque
- [ ] Système d'IA
- [ ] Multijoueur

## Licence

MIT
