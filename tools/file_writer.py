
"""Outils pour enregistrer des fichiers Markdown."""

from pathlib import Path


def save_markdown_file(file_path: str, content: str) -> str:
    """Enregistre du contenu Markdown dans un fichier."""

    path = Path(file_path)

    try:
        # Créer le dossier parent s'il n'existe pas
        path.parent.mkdir(parents=True, exist_ok=True)

        # Écrire le contenu dans le fichier
        path.write_text(content, encoding="utf-8")

        return f"Fichier enregistré avec succès : {path}"

    except OSError as error:
        return f"Impossible d'enregistrer le fichier {path} : {error}"
