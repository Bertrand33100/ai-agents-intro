"""Client FastMCP de vérification en mémoire du serveur local."""

import asyncio
import json
from fastmcp import Client
from server.learning_server import mcp


CHAMPS_SUJET = {
    "id",
    "title",
    "summary",
    "prerequisites",
    "key_concepts",
    "common_mistakes",
    "practice_idea",
}


async def main() -> None:
    """Vérifie la découverte et l'utilisation des capacités du serveur MCP."""
    async with Client(mcp) as client:
        outils = await client.list_tools()
        noms_outils = {outil.name for outil in outils}
        assert {"search_topics", "get_topic_details"} <= noms_outils
        print("Outils visibles :", ", ".join(sorted(noms_outils)))

        ressources = await client.list_resources()
        assert any(str(ressource.uri) == "topics://catalog" for ressource in ressources)
        print("Ressource visible : topics://catalog")

        recherche = await client.call_tool(
            "search_topics", {"query": "décorateurs"}
        )
        assert recherche.data
        assert recherche.data[0]["id"] == "python-decorators"
        print("Recherche « décorateurs » :", recherche.data[0]["title"])

        details = await client.call_tool(
            "get_topic_details", {"topic_id": "python-decorators"}
        )
        assert CHAMPS_SUJET == set(details.data)
        print(
            "Détails « python-decorators » :",
            f"{len(details.data)} champs reçus.",
        )

        inconnu = await client.call_tool(
            "get_topic_details", {"topic_id": "sujet-inexistant"}
        )
        assert inconnu.data.get("error")
        print("Identifiant inconnu :", inconnu.data["error"])

        vide = await client.call_tool("get_topic_details", {"topic_id": "   "})
        assert vide.data.get("error")
        print("Identifiant vide :", vide.data["error"])

        contenu = await client.read_resource("topics://catalog")
        catalogue = json.loads(contenu[0].text)
        assert catalogue
        assert all(set(sujet) == {"id", "title"} for sujet in catalogue)
        print(f"Catalogue lu : {len(catalogue)} sujets (identifiant et titre).")


if __name__ == "__main__":
    asyncio.run(main())
