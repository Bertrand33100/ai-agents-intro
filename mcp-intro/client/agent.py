"""Agent pédagogique déterministe consommant le serveur par MCP en stdio."""

import argparse
import asyncio
import re
import sys
from pathlib import Path
from typing import Any

from fastmcp import Client
from fastmcp.client.transports import PythonStdioTransport


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SERVER_FILE = PROJECT_ROOT / "server" / "learning_server.py"
SAMPLE_QUESTION = "Je veux étudier les décorateurs Python. Que dois-je revoir d'abord ?"
OUTPUT_FILE = PROJECT_ROOT / "output" / "sample_agent_response.md"

MOTS_DE_LIAISON = {
    "a", "abord", "about", "an", "and", "apprendre", "avec", "before", "can",
    "ce", "comment", "d", "dans", "de", "des", "dois", "du", "en", "est",
    "étudier", "first", "for", "help", "how", "i", "in", "is", "la", "le",
    "les", "l", "me", "mon", "moi", "of", "on", "or", "pour", "que", "quel",
    "quelle", "quels", "revoir", "review", "should", "study", "the", "to", "un",
    "une", "want", "what", "when", "which", "with", "would", "you", "je", "veux",
}


def _extraire_requete(question: str) -> str:
    """Garde les mots utiles d'une question pour interroger le catalogue."""
    mots = re.findall(r"[^\W_]+", question.casefold(), flags=re.UNICODE)
    termes = [mot for mot in mots if mot not in MOTS_DE_LIAISON]
    return " ".join(termes) or question.strip()


def _liste_markdown(titre: str, valeurs: Any) -> list[str]:
    """Formate une liste reçue du serveur, sans ajouter de détails."""
    lignes = [f"### {titre}"]
    if isinstance(valeurs, list) and valeurs:
        lignes.extend(f"- {valeur}" for valeur in valeurs)
    else:
        lignes.append("- Non renseigné dans le catalogue.")
    return lignes


def _formater_reponse(question: str, details: dict[str, Any] | None) -> str:
    """Construit une réponse courte uniquement à partir des données MCP."""
    if details is None:
        return (
            "# Réponse de l'assistant d'étude\n\n"
            f"**Ta demande :** {question}\n\n"
            "Je n'ai trouvé aucun sujet correspondant dans le catalogue. "
            "Essaie avec un titre ou un concept de programmation plus précis."
        )

    lignes = [
        "# Réponse de l'assistant d'étude",
        "",
        f"**Ta demande :** {question}",
        "",
        f"## Sujet recommandé : {details.get('title', 'Sujet sans titre')}",
        "",
        "### Pourquoi ce sujet est pertinent",
        str(details.get("summary", "Le catalogue ne fournit pas de résumé.")),
        "",
    ]
    lignes.extend(_liste_markdown("Prérequis", details.get("prerequisites")))
    lignes.append("")
    lignes.extend(_liste_markdown("Concepts clés", details.get("key_concepts")))
    lignes.extend(["", "### Idée de pratique"])
    lignes.append(str(details.get("practice_idea", "Non renseignée dans le catalogue.")))
    lignes.append("")
    lignes.extend(_liste_markdown("Erreurs courantes à éviter", details.get("common_mistakes")))
    return "\n".join(lignes)


async def generer_reponse(question: str) -> str:
    """Interroge les outils MCP et compose une réponse pour l'étudiant."""
    transport = PythonStdioTransport(
        SERVER_FILE,
        cwd=str(PROJECT_ROOT),
        python_cmd=sys.executable,
        keep_alive=False,
    )
    async with Client(transport) as client:
        recherche = await client.call_tool(
            "search_topics", {"query": _extraire_requete(question)}
        )
        correspondances = recherche.data

        if not correspondances:
            return _formater_reponse(question, None)

        topic_id = correspondances[0].get("id")
        if not isinstance(topic_id, str) or not topic_id:
            return _formater_reponse(question, None)

        resultat_details = await client.call_tool(
            "get_topic_details", {"topic_id": topic_id}
        )
        details = resultat_details.data
        if not isinstance(details, dict) or details.get("error"):
            return _formater_reponse(question, None)

        return _formater_reponse(question, details)


def enregistrer_reponse(reponse: str) -> None:
    """Enregistre l'exemple de réponse pour pouvoir le relire."""
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(reponse.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Répond à une question d'étude en utilisant les outils MCP."
    )
    parser.add_argument(
        "question",
        nargs="*",
        help="Question ou sujet à étudier (par défaut : une question sur les décorateurs).",
    )
    arguments = parser.parse_args()
    question = " ".join(arguments.question).strip() or SAMPLE_QUESTION

    reponse = asyncio.run(generer_reponse(question))
    enregistrer_reponse(reponse)
    print(reponse)
    print(f"\nRéponse enregistrée dans : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
