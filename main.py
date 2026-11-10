"""Orchestre les agents et enregistre la fiche de révision finale."""

import argparse
import asyncio
import json
import re
from urllib.error import URLError
from urllib.request import urlopen

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agents.model_config import MODEL_NAME, OLLAMA_API_BASE
from agents.explainer_agent import explainer_agent
from agents.practice_designer_agent import practice_designer_agent
from agents.reviewer_agent import reviewer_agent
from tools.file_writer import save_markdown_file
from tools.validation import validate_required_sections


APP_NAME = "ai_study_guide"
USER_ID = "local_user"
MARKDOWN_HEADING_PATTERN = re.compile(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$")
EXPLAINER_SECTIONS = (
    "Simple Explanation",
    "Key Concepts",
    "Example",
    "Common Mistakes",
    "Final Summary",
)


def check_model_configuration() -> bool:
    """Vérifie la configuration et la disponibilité du modèle Ollama."""

    missing_variables = [
        name
        for name, value in (
            ("MODEL_NAME", MODEL_NAME),
            ("OLLAMA_API_BASE", OLLAMA_API_BASE),
        )
        if not value
    ]
    if missing_variables:
        missing = ", ".join(missing_variables)
        print(
            f"Configuration manquante : {missing}. "
            "Copie .env.example vers .env, puis vérifie ces variables."
        )
        return False

    if not MODEL_NAME.startswith("ollama_chat/"):
        print(
            "Configuration invalide : MODEL_NAME doit utiliser le format "
            "ollama_chat/nom-du-modèle, par exemple "
            "ollama_chat/qwen3:1.7b."
        )
        return False

    try:
        with urlopen(f"{OLLAMA_API_BASE}/api/tags", timeout=3) as response:
            payload = json.load(response)
    except (URLError, TimeoutError, OSError, ValueError) as error:
        print(
            "Impossible de joindre ou de lire Ollama. Vérifie "
            "OLLAMA_API_BASE et démarre le serveur avec `ollama serve`. "
            f"Détail : {type(error).__name__}."
        )
        return False

    available_models = payload.get("models") if isinstance(payload, dict) else None
    if not isinstance(available_models, list):
        print("Ollama a répondu, mais sa liste de modèles est invalide.")
        return False

    requested_model = MODEL_NAME.removeprefix("ollama_chat/")
    installed_models = {
        model_name
        for model in available_models
        if isinstance(model, dict)
        for model_name in (model.get("name"), model.get("model"))
        if isinstance(model_name, str)
    }
    if requested_model not in installed_models:
        print(
            f"Modèle Ollama introuvable : {requested_model}. "
            f"Télécharge-le avec `ollama pull {requested_model}`, "
            "ou corrige MODEL_NAME dans .env."
        )
        return False

    return True


def normalize_heading(title: str) -> str:
    """Normalise un titre Markdown pour comparer son libellé."""

    title = re.sub(r"^\d+[.)]\s*", "", title.strip())
    return " ".join(title.split()).casefold()


def extract_explainer_sections(markdown: str) -> dict[str, str]:
    """Extrait les sections attendues de la réponse de l'agent explicatif."""

    known_sections = {normalize_heading(title): title for title in EXPLAINER_SECTIONS}
    sections = {}
    active_section = None
    section_lines = []
    fence_marker = None

    for line in markdown.splitlines():
        fence_match = re.match(r"^\s*(`{3,}|~{3,})", line)
        if fence_match:
            if active_section:
                section_lines.append(line)
            marker = fence_match.group(1)[0]
            if fence_marker is None:
                fence_marker = marker
            elif fence_marker == marker:
                fence_marker = None
            continue

        heading_match = MARKDOWN_HEADING_PATTERN.match(line)
        if not fence_marker and heading_match:
            section_title = known_sections.get(
                normalize_heading(heading_match.group(2))
            )
            if section_title:
                if active_section:
                    sections[active_section] = "\n".join(section_lines).strip()
                active_section = section_title
                section_lines = []
                continue

        if active_section:
            section_lines.append(line)

    if active_section:
        sections[active_section] = "\n".join(section_lines).strip()

    return sections


def strip_leading_section_heading(content: str, title: str) -> str:
    """Retire le titre de section si un agent l'a inclus dans sa réponse."""

    lines = content.strip().splitlines()
    for index, line in enumerate(lines):
        if not line.strip():
            continue

        match = MARKDOWN_HEADING_PATTERN.match(line)
        if match and normalize_heading(match.group(2)) == normalize_heading(title):
            del lines[index]
        break

    return "\n".join(lines).strip()


def assemble_draft(topic: str, explanation: str, practice: str) -> str:
    """Assemble le brouillon destiné à l'agent de relecture."""

    sections = extract_explainer_sections(explanation)
    practice = strip_leading_section_heading(practice, "Practice Exercise")
    section_content = {
        **sections,
        "Practice Exercise": practice or "Aucun exercice n'a été généré.",
    }

    blocks = [f"# Topic\n\n{topic.strip()}"]
    for title in EXPLAINER_SECTIONS[:3]:
        content = section_content.get(title) or "Contenu non généré."
        blocks.append(f"## {title}\n\n{content}")

    practice_content = section_content["Practice Exercise"]
    blocks.append(f"## Practice Exercise\n\n{practice_content}")

    for title in EXPLAINER_SECTIONS[3:]:
        content = section_content.get(title) or "Contenu non généré."
        blocks.append(f"## {title}\n\n{content}")

    return "\n\n".join(blocks).strip() + "\n"


def replace_markdown_section(markdown: str, title: str, content: str) -> str:
    """Remplace une section Markdown existante ou l'insère à sa place logique."""

    lines = markdown.splitlines()
    section_index = None
    section_level = None

    for index, line in enumerate(lines):
        match = MARKDOWN_HEADING_PATTERN.match(line)
        if match and normalize_heading(match.group(2)) == normalize_heading(title):
            section_index = index
            section_level = len(match.group(1))
            break

    if section_index is None:
        insertion_index = len(lines)
        insertion_level = 2
        if normalize_heading(title) == "review comments":
            for index, line in enumerate(lines):
                match = MARKDOWN_HEADING_PATTERN.match(line)
                if match and normalize_heading(match.group(2)) == "final summary":
                    insertion_index = index
                    insertion_level = len(match.group(1))
                    break

        inserted_section = [
            f"{'#' * insertion_level} {title}",
            "",
            content.strip(),
            "",
        ]
        updated_lines = (
            lines[:insertion_index]
            + inserted_section
            + lines[insertion_index:]
        )
        return "\n".join(updated_lines).strip() + "\n"

    end_index = len(lines)
    for index in range(section_index + 1, len(lines)):
        match = MARKDOWN_HEADING_PATTERN.match(lines[index])
        if match and len(match.group(1)) <= section_level:
            end_index = index
            break

    replacement = [
        f"{'#' * section_level} {title}",
        "",
        content.strip(),
        "",
    ]
    updated_lines = lines[:section_index] + replacement + lines[end_index:]
    return "\n".join(updated_lines).strip() + "\n"


def assemble_final_markdown(draft: str, review: str) -> str:
    """Ajoute les commentaires du relecteur et retourne la fiche finale."""

    review = strip_leading_section_heading(review, "Review Comments")
    if not review:
        review = "Aucun commentaire de relecture n'a été généré."
    return replace_markdown_section(draft, "Review Comments", review)


async def generate_agent_response(agent, prompt: str, session_service) -> str:
    """Exécute un agent et retourne sa réponse finale."""

    runner = Runner(
        agent=agent,
        app_name=APP_NAME,
        session_service=session_service,
    )
    session = await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
    )
    message = types.Content(
        role="user",
        parts=[types.Part(text=prompt)],
    )

    response = ""
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content:
            for part in event.content.parts:
                if part.text:
                    response += part.text

    return response


async def run_explainer_agent(topic: str, session_service) -> str:
    """Génère les sections explicatives à partir du sujet."""

    return await generate_agent_response(explainer_agent, topic, session_service)


async def run_practice_designer_agent(
    topic: str,
    explanation: str,
    session_service,
) -> str:
    """Génère un exercice basé sur le sujet et l'explication obtenue."""

    prompt = (
        f"SUJET D'ORIGINE :\n{topic}\n\n"
        "EXPLICATION GÉNÉRÉE PAR L'AGENT EXPLICATIF :\n"
        "--- Début de l'explication ---\n"
        f"{explanation}\n"
        "--- Fin de l'explication ---"
    )
    return await generate_agent_response(
        practice_designer_agent,
        prompt,
        session_service,
    )


async def run_reviewer_agent(draft: str, session_service) -> str:
    """Demande au relecteur d'examiner le brouillon assemblé."""

    prompt = (
        "BROUILLON COMPLET DE LA FICHE À RELIRE :\n"
        "--- Début du brouillon ---\n"
        f"{draft}\n"
        "--- Fin du brouillon ---"
    )
    return await generate_agent_response(reviewer_agent, prompt, session_service)


async def run_agent(topic: str) -> None:
    """Orchestre les agents, valide la fiche finale et l'enregistre."""

    if not topic.strip():
        print("Le sujet ne peut pas être vide. Indique un sujet à expliquer.")
        return

    session_service = InMemorySessionService()

    print(f"\nSujet demandé : {topic}\n")
    print("Étape 1/3 : génération de l'explication...\n")
    explanation = await run_explainer_agent(topic, session_service)
    if not explanation.strip():
        print("Aucune explication n'a été générée ; arrêt du workflow.")
        return

    print("Étape 2/3 : création de l'exercice pratique...\n")
    practice = await run_practice_designer_agent(
        topic,
        explanation,
        session_service,
    )

    print("Assemblage du brouillon...\n")
    draft = assemble_draft(topic, explanation, practice)

    print("Étape 3/3 : relecture du brouillon...\n")
    review = await run_reviewer_agent(draft, session_service)

    print("Assemblage du Markdown final...\n")
    final_markdown = assemble_final_markdown(draft, review)
    print(final_markdown)

    validation = validate_required_sections(final_markdown)
    if validation["valid"]:
        print("\nValidation réussie : toutes les sections sont présentes.")
    else:
        missing = ", ".join(validation["missing_sections"])
        print(
            "\nÉchec de la validation. Sections manquantes : "
            f"{missing}. Le fichier sera enregistré pour inspection."
        )

    result = save_markdown_file("output/study_guide.md", final_markdown)
    print(f"\n{result}")


def main() -> None:
    """Récupère le sujet et lance le workflow séquentiel."""

    parser = argparse.ArgumentParser(
        description="Générateur de fiches de révision avec IA."
    )
    parser.add_argument(
        "topic",
        nargs="+",
        help="Sujet informatique à expliquer.",
    )

    args = parser.parse_args()
    topic = " ".join(args.topic)
    if not topic.strip():
        parser.error("Le sujet ne peut pas être vide.")

    if not check_model_configuration():
        return

    asyncio.run(run_agent(topic))


if __name__ == "__main__":
    main()
