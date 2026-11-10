# Générateur d'agents IA en Python

## Description

**AI Agents in Python** est un projet Python qui permet de générer automatiquement des fiches de révision sur des sujets informatiques grâce à plusieurs agents d'intelligence artificielle.

L'utilisateur fournit un sujet, par exemple `Python decorators`, et l'application génère une fiche de révision structurée au format Markdown.

Le projet utilise trois agents spécialisés qui travaillent successivement :

1. **Explainer Agent** : explique le sujet de manière pédagogique.
2. **Practice Designer Agent** : crée un exercice pratique.
3. **Reviewer Agent** : relit le brouillon et propose des améliorations.

Un programme Python orchestre les agents, assemble leurs réponses, vérifie la structure du document et enregistre la fiche finale.

Le modèle d'intelligence artificielle fonctionne localement avec Ollama.

## Prérequis

Pour installer et exécuter le projet, il faut disposer de :

- Python 3.10 ou supérieur.
- pip.
- Ollama.
- Google Agent Development Kit (ADK).
- LiteLLM.
- python-dotenv.
- Le modèle Qwen3 1.7B installé dans Ollama.
- Un environnement Linux ou WSL recommandé.

### Technologies utilisées

| Technologie  | Utilisation                          |
| ------------ | ------------------------------------ |
| Python       | Langage de programmation             |
| Google ADK   | Création et orchestration des agents |
| LiteLLM      | Communication avec le modèle IA      |
| Ollama       | Exécution locale du modèle           |
| Qwen3 1.7B   | Modèle de langage                    |
| Markdown     | Format des fiches de révision        |
| Git / GitHub | Gestion du code source               |

## Installation

### 1. Accéder au projet

```bash
cd ~/projects/ai-agents-intro
```

### 2. Créer un environnement virtuel

```bash
python3 -m venv venv
```

### 3. Activer l'environnement virtuel

Sous Linux / WSL :

```bash
source venv/bin/activate
```

### 4. Mettre à jour pip

```bash
python -m pip install --upgrade pip
```

### 5. Installer les dépendances

```bash
pip install -r requirements.txt
```

Les principales dépendances utilisées sont :

- `google-adk`
- `litellm`
- `python-dotenv`

## Configuration

### 1. Installer et vérifier Ollama

Vérifier qu'Ollama est installé :

```bash
ollama --version
```

### 2. Télécharger le modèle

```bash
ollama pull qwen3:1.7b
```

### 3. Vérifier le modèle installé

```bash
ollama list
```

Le modèle utilisé dans ce projet est :

**Qwen3 1.7B – Quantification Q4_K_M**

### 4. Configurer les variables d'environnement

Créer le fichier `.env` à partir du fichier d'exemple :

```bash
cp .env.example .env
```

Configuration du fichier `.env` :

```dotenv
MODEL_NAME=ollama_chat/qwen3:1.7b
OLLAMA_API_BASE=http://localhost:11434
```

Le fichier `.env` contient la configuration locale de l'application.

Il ne doit jamais être publié sur GitHub.

Le fichier `.env.example` peut être partagé, car il ne doit contenir aucune information secrète.

### 5. Démarrer Ollama

Si le serveur Ollama n'est pas déjà actif :

```bash
ollama serve
```

Si Ollama fonctionne déjà, il n'est pas nécessaire de démarrer une seconde instance.

## Exécution du projet

Après l'installation des dépendances et la configuration d'Ollama, lancer le programme avec un sujet entre guillemets :

```bash
python main.py "Python decorators"
```

Le programme exécute les différentes étapes du workflow :

1. Génération de l'explication.
2. Création de l'exercice pratique.
3. Assemblage du brouillon.
4. Relecture par le Reviewer Agent.
5. Assemblage du document final.
6. Vérification des sections obligatoires.
7. Enregistrement de la fiche Markdown.

Le fichier généré est enregistré dans :

```text
output/study_guide.md
```

## Exemple d'entrée

Sujet transmis à l'application :

```text
Python decorators
```

Commande utilisée :

```bash
python main.py "Python decorators"
```

## Exemple de sortie

Le programme génère une fiche de révision organisée autour des huit sections suivantes :

```markdown
# Topic

Python decorators

## Simple Explanation

Explication simple du sujet.

## Key Concepts

Présentation des concepts importants.

## Example

Exemple de code Python.

## Practice Exercise

Exercice pratique.

## Common Mistakes

Présentation des erreurs fréquentes.

## Review Comments

Commentaires de relecture.

## Final Summary

Résumé final.
```

Après la génération, le programme affiche notamment :

```text
Validation réussie : toutes les sections sont présentes.

Fichier enregistré avec succès : output/study_guide.md
```

## Structure du projet

```text
ai-agents-intro/
│
├── agents/
│   ├── __init__.py
│   ├── model_config.py
│   ├── explainer_agent.py
│   ├── practice_designer_agent.py
│   └── reviewer_agent.py
│
├── tools/
│   ├── __init__.py
│   ├── file_writer.py
│   └── validation.py
│
├── output/
│   └── study_guide.md
│
├── data/
│   └── topic_examples.json
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── main.py
```

### Organisation des dossiers

- `agents/` : contient les trois agents d'intelligence artificielle.
- `tools/` : contient les outils Python déterministes.
- `output/` : accueille les fiches de révision générées.
- `data/` : contient les données et exemples de sujets.
- `main.py` : point d'entrée de l'application.
- `requirements.txt` : liste les dépendances Python.
- `.env.example` : présente les variables de configuration.
- `.gitignore` : définit les fichiers ignorés par Git.
- `README.md` : documentation du projet.

## Les agents IA

### 1. Explainer Agent

Son rôle est d'expliquer le sujet demandé de manière simple et pédagogique.

Il génère :

- Une explication générale.
- Les concepts importants.
- Un exemple de code.
- Les erreurs fréquentes.
- Un résumé final.

### 2. Practice Designer Agent

Son rôle est de concevoir un exercice pratique adapté au sujet étudié.

Il génère :

- Un énoncé.
- Un objectif pédagogique.
- Les entrées et sorties attendues si nécessaire.
- Des indices pour aider l'utilisateur.

Son objectif est de faire réfléchir l'apprenant sans lui fournir directement la solution complète.

### 3. Reviewer Agent

Son rôle est de relire le brouillon produit par les deux premiers agents.

Il doit :

- Identifier les informations manquantes.
- Repérer les explications ambiguës.
- Proposer des améliorations.
- Donner une recommandation finale : `APPROVED` ou `REVISION REQUIRED`.

## Les outils Python

### 1. file_writer.py

Cet outil permet d'enregistrer la fiche de révision au format Markdown.

Ses responsabilités :

- Créer le dossier de destination s'il n'existe pas.
- Écrire le contenu dans un fichier.
- Utiliser l'encodage UTF-8.
- Intercepter les erreurs d'écriture.
- Retourner un message indiquant le résultat de l'enregistrement.

### 2. validation.py

Cet outil vérifie automatiquement la présence des huit sections obligatoires dans la fiche générée.

Les sections contrôlées sont :

1. Topic
2. Simple Explanation
3. Key Concepts
4. Example
5. Practice Exercise
6. Common Mistakes
7. Review Comments
8. Final Summary

L'outil retourne un résultat de validation ainsi que la liste des sections manquantes.

Cette validation vérifie uniquement la structure du document. Elle ne garantit pas l'exactitude technique du contenu généré.

## Liste d'auto-validation

### Structure du projet

- [x] Création des dossiers du projet.
- [x] Création des modules des trois agents.
- [x] Création des modules des deux outils.
- [x] Création du README.
- [x] Création de requirements.txt.
- [x] Création de .env.example.
- [x] Configuration de .gitignore.

### Environnement et configuration

- [x] Création de l'environnement virtuel Python.
- [x] Installation des dépendances.
- [x] Installation d'Ollama.
- [x] Téléchargement du modèle Qwen3 1.7B.
- [x] Configuration des variables d'environnement.
- [x] Vérification du fonctionnement du modèle local.
- [x] Protection du fichier .env.

### Agents et workflow

- [x] Création de l'Explainer Agent.
- [x] Création du Practice Designer Agent.
- [x] Création du Reviewer Agent.
- [x] Configuration de Google ADK avec LiteLLM.
- [x] Mise en place du workflow séquentiel.
- [x] Assemblage des réponses des agents.
- [x] Génération des fiches Markdown.

### Gestion des erreurs et validation

- [x] Détection des variables d'environnement manquantes.
- [x] Détection d'un serveur Ollama indisponible.
- [x] Détection d'un modèle indisponible.
- [x] Gestion des erreurs d'écriture.
- [x] Vérification des sections obligatoires.
- [x] Gestion d'un sujet vide.

### Documentation

- [x] Présentation du projet.
- [x] Instructions d'installation.
- [x] Configuration du modèle.
- [x] Instructions d'exécution.
- [x] Exemple d'entrée.
- [x] Exemple de sortie.
- [x] Présentation des agents.
- [x] Présentation des outils.
- [x] Réflexion personnelle.
- [x] Limites connues.

## Réflexion personnelle

### 1. Quelle est la différence entre un appel direct à un LLM et un agent IA ?

Un appel direct à un LLM consiste à envoyer une instruction à un modèle de langage et à recevoir une réponse.

Un agent IA va plus loin. Il possède un objectif, des instructions et éventuellement des outils qui lui permettent d'accomplir une tâche précise.

Dans mon projet, les agents ne se contentent pas de répondre à une question. Ils travaillent ensemble dans un workflow organisé pour produire une fiche de révision complète.

### 2. Quel est le rôle de chaque agent dans mon système ?

Chaque agent possède une responsabilité spécifique.

- L'Explainer Agent explique le sujet.
- Le Practice Designer Agent crée un exercice pratique.
- Le Reviewer Agent relit le brouillon et propose des améliorations.

Cette séparation des responsabilités permet de mieux organiser le programme et de rendre son fonctionnement plus compréhensible.

### 3. Quel est le rôle de chaque outil dans mon système ?

Le projet utilise deux outils Python déterministes.

- `file_writer.py` enregistre la fiche finale dans un fichier Markdown.
- `validation.py` vérifie la présence des sections obligatoires.

Contrairement aux agents IA, ces outils exécutent des opérations programmées à l'avance et ne génèrent pas de réponses à l'aide d'un modèle de langage.

### 4. Quelle a été la partie la plus difficile du projet ?

La partie la plus difficile a été de comprendre comment faire communiquer les différents composants et les intégrer dans un workflow fonctionnel.

J'ai notamment dû apprendre à configurer Google ADK, connecter LiteLLM à Ollama, organiser les responsabilités des agents et assembler leurs réponses dans un document unique.

La gestion des erreurs a également été une étape importante. J'ai appris à tester les variables d'environnement, l'indisponibilité du serveur Ollama, l'absence d'un modèle et les problèmes de permissions lors de l'écriture d'un fichier.

Ce projet m'a permis de mieux comprendre l'importance de la séparation des responsabilités, de la validation et des tests.

### 5. Quelle limite ai-je observée avec le modèle utilisé ?

J'ai utilisé Qwen3 1.7B avec une quantification Q4_K_M, exécuté localement avec Ollama.

Pendant les essais, j'ai observé plusieurs limites :

- Des expressions parfois mélangées entre le français et l'anglais.
- Des erreurs grammaticales.
- Des espaces manquants dans certaines phrases.
- Des réponses qui ne respectent pas toujours toutes les instructions.
- Des propositions de révision qui ne garantissent pas la correction du document final.

J'ai également constaté qu'un modèle local de petite taille nécessite une vérification humaine de ses réponses.

Les performances dépendent des ressources matérielles disponibles, notamment de la mémoire et de la puissance de calcul. Les besoins matériels exacts de mon installation n'ont pas encore été mesurés.

## Limites connues

Le projet présente plusieurs limites :

- La qualité des fiches dépend du modèle d'intelligence artificielle utilisé.
- Un modèle de petite taille peut produire des explications incorrectes ou imprécises.
- Les agents ne respectent pas toujours toutes les instructions.
- Le Reviewer Agent ne garantit pas la correction de tous les problèmes identifiés.
- La validation automatique contrôle uniquement la structure du document.
- Le code Python généré n'est pas automatiquement garanti comme correct ou exécutable.
- Ollama doit être disponible pour exécuter l'application.
- Le modèle configuré doit être installé localement.
- Les performances dépendent du matériel utilisé.

Une vérification humaine reste donc nécessaire avant d'utiliser les fiches générées comme support d'apprentissage.

---

**Projet réalisé dans le cadre de mon apprentissage du développement logiciel et de l'intelligence artificielle.**
