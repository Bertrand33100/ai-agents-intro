"""Serveur MCP des sujets d'apprentissage en programmation."""

import json
import unicodedata
from pathlib import Path
from typing import Any

from fastmcp import FastMCP


mcp = FastMCP("Programming Learning Server")
TOPICS_FILE = Path(__file__).resolve().parents[1] / "data" / "topics.json"


def _normaliser(texte: str) -> str:
    """Normalise la casse et les accents pour faciliter la recherche."""
    decomposed = unicodedata.normalize("NFKD", texte.casefold())
    return "".join(
        caractere
        for caractere in decomposed
        if not unicodedata.combining(caractere)
    )


def _charger_sujets() -> list[dict[str, Any]]:
    """Charge le catalogue local des sujets de programmation."""
    return json.loads(TOPICS_FILE.read_text(encoding="utf-8"))


@mcp.tool(run_in_thread=False)
def search_topics(query: str) -> list[dict[str, Any]]:
    """Recherche les sujets par titre, résumé ou concept clé.

    La recherche ignore la casse et les accents. Une requête vide ou sans résultat
    renvoie une liste vide. Chaque résultat fournit un résumé et des indices utiles
    pour aider un agent à choisir le sujet pertinent.
    """
    if not isinstance(query, str):
        return []

    termes = [_normaliser(terme) for terme in query.split() if terme.strip()]
    if not termes:
        return []

    sujets = _charger_sujets()
    resultats = []

    for sujet in sujets:
        champs_recherchables = [
            sujet.get("id", ""),
            sujet.get("title", ""),
            sujet.get("summary", ""),
            *sujet.get("key_concepts", []),
        ]
        texte_recherchable = _normaliser(" ".join(champs_recherchables))

        if all(terme in texte_recherchable for terme in termes):
            resultats.append(
                {
                    "id": sujet["id"],
                    "title": sujet["title"],
                    "summary": sujet["summary"],
                    "prerequisites": sujet["prerequisites"],
                    "key_concepts": sujet["key_concepts"],
                }
            )

    return resultats


@mcp.tool(run_in_thread=False)
def get_topic_details(topic_id: str) -> dict[str, Any]:
    """Renvoie toutes les informations d'un sujet identifié par son identifiant.

    L'identifiant doit correspondre exactement à un identifiant du catalogue.
    Une valeur vide, invalide ou inconnue renvoie un objet contenant une erreur.
    """
    if not isinstance(topic_id, str) or not topic_id.strip():
        return {"error": "L'identifiant du sujet doit être une chaîne non vide."}

    identifiant = topic_id.strip()
    for sujet in _charger_sujets():
        if sujet.get("id") == identifiant:
            return sujet

    return {
        "error": f"Aucun sujet ne correspond à l'identifiant « {identifiant} »."
    }


@mcp.resource("topics://catalog", mime_type="application/json")
async def get_topic_catalog() -> str:
    """Fournit en lecture seule les identifiants et titres des sujets disponibles."""
    catalogue = [
        {"id": sujet["id"], "title": sujet["title"]}
        for sujet in _charger_sujets()
    ]
    return json.dumps(catalogue, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run(show_banner=False, log_level="ERROR")
