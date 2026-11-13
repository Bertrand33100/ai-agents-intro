# MCP Servers in Python

## Description

Ce projet pédagogique présente la création d'un serveur MCP (Model Context Protocol) en Python avec FastMCP.

Il expose un catalogue local de sujets de programmation enregistré dans `data/topics.json`. Un agent pédagogique peut rechercher un sujet, récupérer ses informations détaillées et générer une réponse adaptée à la question de l'étudiant.

Le serveur s'appelle **Programming Learning Server** et utilise le transport local `stdio` (Standard Input/Output).

L'objectif est de comprendre comment une application d'intelligence artificielle peut communiquer avec des capacités externes grâce au protocole MCP.

## MCP Architecture Summary

MCP (Model Context Protocol) est un protocole qui standardise la communication entre les applications d'intelligence artificielle et les programmes qui fournissent des capacités externes.

Son architecture repose notamment sur trois composants :

- **Host (hôte)** : application qui orchestre l'agent et ses interactions avec les serveurs MCP.
- **Client (client MCP)** : composant de l'hôte qui établit une connexion avec un serveur MCP précis, découvre ses capacités et les utilise.
- **Server (serveur MCP)** : programme qui expose des capacités accessibles au client, notamment des outils et des ressources.

Un hôte peut gérer plusieurs clients MCP, généralement un par serveur auquel il se connecte.

Deux types de capacités sont utilisés dans ce projet :

- **Tools (outils)** : opérations exécutables à la demande, comme rechercher un sujet ou récupérer ses détails.
- **Resources (ressources)** : données consultables par le client, comme le catalogue des sujets.

Dans ce projet, l'agent joue le rôle d'application hôte. Son client MCP démarre le serveur local, recherche les sujets pertinents avec un outil, puis récupère les détails d'un sujet sélectionné.

Le principe du moindre privilège consiste à limiter les permissions et les capacités accessibles à une application au strict nécessaire.

## Requirements

- Python 3.10 ou plus récent.
- `pip`, le gestionnaire de paquets Python.
- Le module Python `venv` pour créer un environnement virtuel.
- FastMCP, déclaré dans `requirements.txt` avec `fastmcp>=2.0`.

Version utilisée et testée pendant le développement : **FastMCP 4.1.8**.

Aucune clé API, aucun compte externe et aucun modèle d'intelligence artificielle externe ne sont nécessaires.

## Setup

Depuis le dossier du projet `mcp-intro/` :

Créer un environnement virtuel :

```bash
python3 -m venv .venv
```

Activer l'environnement virtuel sous Linux ou WSL :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
python -m pip install -r requirements.txt
```

Vérifier la version de FastMCP installée :

```bash
python -m pip show fastmcp
```

Sous Windows PowerShell, l'activation de l'environnement virtuel se fait avec :

```powershell
.venv\Scripts\Activate.ps1
```

## How to Run the Server

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
python server/learning_server.py
```

Le serveur démarre avec le transport `stdio`.

Il attend les communications d'un client MCP et ne démarre pas de service HTTP.

Pour arrêter le serveur lorsqu'il est lancé directement dans un terminal, utiliser `Ctrl+C`.

L'agent présenté dans ce projet démarre lui-même le serveur comme sous-processus. Il n'est donc pas nécessaire de lancer le serveur dans un terminal séparé pour utiliser l'agent.

## How to Test the Server

Le projet contient un client de vérification dans `client/mcp_client.py`.

Depuis la racine du projet :

```bash
python -m client.mcp_client
```

Ce client utilise `fastmcp.Client` avec l'instance du serveur importée directement dans Python.

Il vérifie les éléments suivants :

1. La découverte des deux outils MCP.
2. La découverte de la ressource `topics://catalog`.
3. La recherche du sujet « décorateurs ».
4. La récupération des détails de `python-decorators`.
5. Le traitement d'un identifiant inconnu.
6. Le traitement d'un identifiant vide.
7. La lecture du catalogue des sujets.

Ce test valide les échanges MCP avec une instance en mémoire. Il ne vérifie pas à lui seul le démarrage du serveur dans un sous-processus `stdio`.

Cette dernière partie est vérifiée par l'exécution réelle de l'agent.

Exemple de sortie observée :

```text
Outils visibles : get_topic_details, search_topics
Ressource visible : topics://catalog
Recherche « décorateurs » : Décorateurs Python
Détails « python-decorators » : 7 champs reçus.
Identifiant inconnu : Aucun sujet ne correspond à l'identifiant « sujet-inexistant ».
Identifiant vide : L'identifiant du sujet doit être une chaîne non vide.
Catalogue lu : 5 sujets (identifiant et titre).
```

## How to Run the Agent

L'agent pédagogique est disponible dans `client/agent.py`.

Depuis la racine du projet, avec l'environnement virtuel activé :

```bash
python -m client.agent "Je veux étudier les décorateurs Python. Que dois-je revoir d'abord ?"
```

L'agent utilise `PythonStdioTransport` pour démarrer `server/learning_server.py` comme sous-processus Python et communiquer avec lui via MCP.

Son fonctionnement est le suivant :

1. Il reçoit une question depuis le terminal.
2. Il extrait les mots utiles de la question.
3. Il appelle `search_topics` via MCP.
4. Il récupère l'identifiant du premier résultat.
5. Il appelle `get_topic_details` via MCP.
6. Il construit une réponse pédagogique à partir des informations reçues.
7. Il affiche la réponse dans le terminal.
8. Il enregistre la réponse dans `output/sample_agent_response.md`.

Si aucun sujet ne correspond à la recherche, l'agent indique clairement qu'il n'a trouvé aucune correspondance.

Sans question en argument, l'agent utilise une question d'exemple portant sur les décorateurs Python.

## Available Tools

Le serveur expose deux outils MCP.

### 1. `search_topics(query: str)`

Recherche des sujets dans le catalogue local.

La recherche porte sur les champs suivants :

- Identifiant du sujet.
- Titre.
- Résumé.
- Concepts clés.

Caractéristiques :

- Ignore la casse.
- Ignore les accents.
- Recherche tous les termes fournis dans les champs recherchables.
- Renvoie une liste vide si la requête est vide ou si aucun sujet ne correspond.

Chaque résultat contient :

- `id`
- `title`
- `summary`
- `prerequisites`
- `key_concepts`

### 2. `get_topic_details(topic_id: str)`

Récupère toutes les informations d'un sujet à partir de son identifiant.

Exemple :

```python
get_topic_details("python-decorators")
```

Les informations retournées comprennent :

- `id`
- `title`
- `summary`
- `prerequisites`
- `key_concepts`
- `common_mistakes`
- `practice_idea`

Un identifiant vide ou inconnu renvoie un objet contenant un champ `error`.

## Available Resources

Le serveur expose une ressource MCP en lecture seule.

### `topics://catalog`

Cette ressource fournit un aperçu du catalogue des sujets disponibles.

Elle retourne une chaîne JSON (JavaScript Object Notation) contenant uniquement :

- L'identifiant de chaque sujet.
- Son titre.

Exemple de contenu :

```json
[
  {
    "id": "python-functions",
    "title": "Fonctions Python"
  },
  {
    "id": "python-loops",
    "title": "Boucles Python"
  }
]
```

La ressource utilise le type MIME `application/json`.

Elle permet au client de consulter le catalogue sans modifier les données originales.

## Third-Party MCP Server Review

Le serveur tiers étudié est **Filesystem**, disponible dans le dépôt officiel :

https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem

Ce serveur permet à une application compatible MCP d'interagir avec des fichiers et des dossiers locaux.

### Type d'exécution

Filesystem est un serveur local lancé comme sous-processus Node.js avec le transport `stdio`.

La documentation consultée indique une dépendance à Node.js 24 ou une version ultérieure.

### Outils et ressources exposés

Les capacités documentées comprennent notamment :

- `read_text_file` : lire le contenu d'un fichier texte.
- `search_files` : rechercher des fichiers.
- `list_directory` : afficher le contenu d'un dossier.
- `write_file` : écrire un fichier.
- `edit_file` : modifier un fichier.
- `move_file` : déplacer un fichier.

Le serveur fournit également un modèle de ressource permettant d'accéder à des fichiers locaux avec des URI de type `file://`.

### Permissions et identifiants

Aucune clé API ni aucun compte distant ne sont nécessaires dans la configuration locale de base.

Le serveur doit recevoir les chemins des dossiers auxquels il est autorisé à accéder.

Le processus s'exécute avec les permissions du compte système qui le lance.

### Risques identifiés

Les outils d'écriture peuvent modifier, écraser ou déplacer des fichiers.

Un serveur compromis pourrait également exploiter les permissions du compte système pour accéder à d'autres fichiers accessibles à ce processus.

Le transport `stdio` ne constitue pas une sandbox (environnement d'exécution isolé).

### Mesures de sécurité recommandées

Avant d'utiliser ce serveur :

- Lire sa documentation et examiner son code source.
- Limiter l'accès à un dossier temporaire dédié.
- Utiliser le mode `--read-only` lorsque les opérations d'écriture ne sont pas nécessaires.
- Isoler le processus dans un conteneur ne montant que les dossiers indispensables.
- Éviter de donner accès au dossier personnel ou aux fichiers contenant des secrets.

Documentation complémentaire :

https://github.com/modelcontextprotocol/modelcontextprotocol/blob/main/docs/docs/2026-07-28/tutorials/security/local-server-security.mdx

Cette analyse repose sur la documentation consultée. Le serveur tiers n'a pas été installé ni exécuté dans ce projet.

## Example Output

Exemple réel obtenu en exécutant l'agent avec la question :

```bash
python -m client.agent "Je veux étudier les décorateurs Python. Que dois-je revoir d'abord ?"
```

Réponse générée et enregistrée dans `output/sample_agent_response.md` :

```markdown
# Réponse de l'assistant d'étude

**Ta demande :** Je veux étudier les décorateurs Python. Que dois-je revoir d'abord ?

## Sujet recommandé : Décorateurs Python

### Pourquoi ce sujet est pertinent
Un décorateur reçoit une fonction et renvoie une fonction qui ajoute ou modifie son comportement.

### Prérequis
- fonctions
- fonctions imbriquées
- fonctions d'ordre supérieur

### Concepts clés
- fonction de première classe
- fermeture
- fonction enveloppe
- syntaxe @

### Idée de pratique
Créer un décorateur qui affiche le nom d'une fonction avant de l'appeler.

### Erreurs courantes à éviter
- Oublier de renvoyer la fonction enveloppe
- Appeler la fonction au lieu de la renvoyer
```

## Known Limitations

- Le catalogue est petit, local et statique. Le serveur n'utilise ni base de données ni API externe.
- La recherche repose sur la présence de mots dans les champs des sujets.
- Elle ne comprend pas les synonymes et ne réalise pas de véritable analyse sémantique de l'intention de l'utilisateur.
- L'agent est déterministe : il ne fait appel à aucun modèle de langage externe.
- L'agent ne possède pas de mémoire de conversation.
- Lorsqu'une recherche renvoie plusieurs résultats, l'agent sélectionne le premier. Une question ambiguë peut donc conduire à une recommandation inadaptée.
- Le serveur utilise le transport local `stdio` et n'expose pas d'URL HTTP.
- Les tests du client `mcp_client.py` utilisent une instance en mémoire ; ils ne remplacent pas les tests du démarrage réel du serveur en sous-processus.

## Reflection

### 1. What problem does MCP solve?

MCP résout le problème de communication entre les applications d'intelligence artificielle et les programmes externes.

Il fournit une interface commune permettant à une application de découvrir et d'utiliser des capacités externes sans devoir intégrer directement la logique de chaque programme.

### 2. What is the difference between an MCP tool and an MCP resource?

Un outil MCP exécute une opération à la demande du client.

Par exemple, `search_topics` recherche un sujet dans le catalogue.

Une ressource MCP fournit des données consultables par le client.

Par exemple, `topics://catalog` permet de lire les identifiants et les titres des sujets disponibles.

### 3. What does your MCP server expose?

Mon serveur expose :

- Deux outils : `search_topics` et `get_topic_details`.
- Une ressource en lecture seule : `topics://catalog`.

Ces capacités utilisent les données du fichier local `data/topics.json`.

### 4. How does your agent use the MCP server?

Mon agent joue le rôle d'application hôte.

Il démarre le serveur local avec le transport `stdio`, établit une connexion avec un client FastMCP, puis utilise les outils disponibles.

Il commence par rechercher un sujet avec `search_topics`, récupère ensuite ses informations détaillées avec `get_topic_details`, puis construit une réponse pédagogique à partir des données reçues.

Il enregistre enfin le résultat dans `output/sample_agent_response.md`.

### 5. What should you check before using a third-party MCP server?

Avant d'utiliser un serveur MCP tiers, il faut vérifier :

- L'identité de son éditeur et la provenance du code.
- La documentation et les dépendances.
- Les outils et les ressources qu'il expose.
- Les permissions et les accès qu'il demande.
- Les identifiants ou secrets auxquels il pourrait accéder.
- Les données qu'il peut lire, modifier ou transmettre.
- Les possibilités de limiter ses permissions et de l'isoler.

Il est important de ne jamais accorder des permissions excessives à un serveur sans avoir compris ses conséquences.

### 6. What limitation did you observe in your implementation?

La principale limite observée est la recherche par mots-clés.

L'agent extrait les termes utiles de la question et recherche leur présence dans le catalogue. Il ne comprend pas réellement les synonymes ni l'intention de l'utilisateur.

De plus, lorsqu'il reçoit plusieurs résultats, il sélectionne uniquement le premier.

Une amélioration possible serait d'intégrer ultérieurement un système de classement des résultats ou un modèle de langage capable de mieux interpréter les questions.
