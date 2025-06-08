# Puissance X

**Puissance X** est une version évoluée du célèbre jeu Puissance 4. Elle propose des fonctionnalités enrichies comme des dimensions de plateau personnalisables, une IA adaptative selon le niveau de difficulté, et même un mode tournoi entre intelligences artificielles.

---

## 🎮 Description

Puissance X permet à un joueur humain d’affronter une IA sur un plateau par défaut de **6 lignes et 7 colonnes**, avec un objectif par défaut de **4 jetons alignés**. Ces paramètres peuvent être ajustés :

- **Taille du plateau :** de 5x5 à 10x10
- **Condition de victoire :** aligner 3 à 7 jetons

L’IA utilise l’algorithme **Minimax** avec **élagage alpha-bêta**, avec trois niveaux de difficulté :
- 🟢 *Facile*
- 🟠 *Moyen*
- 🔴 *Difficile*

---

## 🚀 Fonctionnalités principales

- 👤 **Mode solo** : un joueur contre l’IA
- 🎯 **Trois niveaux d’IA** : facile, moyen, difficile
- 🧠 **IA basée sur Minimax + alpha-bêta pruning**
- 🖼️ **Interface graphique** intuitive via `pygame`
- 📊 **Tournoi automatisé IA vs IA** avec sauvegarde des statistiques en JSON
- 🧩 **Grille personnalisable** (dimensions et condition de victoire)

---

## 🧪 Mode tournoi IA (IA vs IA)

Le fichier `ai_match_tester.py` simule automatiquement des séries de matchs entre IA de différents niveaux.

**Fonctionnalités du tournoi :**
- Lancement automatique de 50 matchs par duel (`easy vs medium`, `medium vs hard`, etc.)
- Alternance du joueur qui commence pour équilibrer les résultats
- Historique des coups et résultats sauvegardés dans un fichier `match_results.json`
- Statistiques détaillées par IA :
  - Nombre de victoires
  - Nombre de défaites
  - Nombre de matchs nuls

💡 Idéal pour évaluer la performance de l'algorithme en fonction du niveau de difficulté.

---

## 🗂️ Architecture du projet


```
Puissance_X/
├── ai.py # Algorithmes Minimax, heuristiques d'évaluation
├── ai_match_tester.py # Simulation de tournois entre IA
├── constants.py # Paramètres globaux (couleurs, tailles, etc.)
├── credits_screen.py # Écran des crédits
├── evaluation.py # Évaluation IA vs IA (autre implémentation)
├── game.py # Logique du jeu joueur vs IA
├── game_logic.py # Fonctions de base (vérification de victoire, placement, etc.)
├── game_screen.py # Rendu graphique du plateau
├── interface.py # Logique de l'interface Pygame
├── main.py # Point d’entrée de l’application
├── main_menu.py # Menu principal (jouer, options, quitter)
├── match_results.json # Résultats des matchs IA vs IA (généré automatiquement)
├── settings_screen.py # Menu de configuration des paramètres du jeu
└── README.md # Ce fichier
```
## Installation et lancement

1. Clonez le dépôt :


git clone https://github.com/fayssalzakaria/puissance4.git
cd Puissance_X

2. Accédez au dossier du projet :

cd puissance4


3. Assurez-vous d'avoir installé les dépendances nécessaires avec les commande suivantes :


  pip install numpy
  pip install pygame
  
4. Lancer le jeu
python main.py

5. Lancez le tournoi IA vs IA pour analyser les performances :

python ai_match_tester.py

## Screenshots

Voici quelques captures d'écran du projet :

![Menu principal](Screen_1.PNG)
![Difficulte](Screen_2.PNG)
![Fin jeu](Screen_3.PNG)
##  Auteurs  
**Fayssal**  
- Email : fayssal.132004@gmail.com
  
**Nicolas**  
