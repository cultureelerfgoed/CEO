# ldv-tools — AI-toegang tot de RCE Linked Data Voorziening

Hulpmiddelen om de CHO-dataset in de LDV bevraagbaar te maken voor
AI-systemen. Hoort bij de AI-ready onderdelen in de ceo-repository:
https://github.com/cultureelerfgoed/ceo

## Inhoud

- `ldv_mcp.py` — MCP-server (Model Context Protocol) met 7 lezende tools:
  vrije SPARQL-queries, datasettotalen, klasse- en propertypartities,
  padverkenning (vooruit en achteruit) en conceptzoeken in de waardenlijsten
  (rn/2 via PoolParty, CHT via het NDE Termennetwerk).
  Draait lokaal (stdio) of centraal (streamable HTTP); zie de docstring.
- `Dockerfile` — voor centrale hosting van de MCP-server.
- `genereer_void.py` — genereert ceo-void.ttl (VoID incl. linksets).
- `genereer_padenkaart.py` — genereert ceo-padenkaart.ttl (SHACL-shapes).
- `tel_ceo_klassen.py` — snelle telling per CEO-klasse, zonder dependencies.

## Installatie

    pip install "mcp[cli]" httpx SPARQLWrapper rdflib   # Python 3.10+

`tel_ceo_klassen.py` werkt zonder installatie (alleen standaardbibliotheek).

## Configuratie (omgevingsvariabelen)

- `LDV_ENDPOINT` — SPARQL-endpoint van de CHO-dataset
- `POOLPARTY_BASE`, `POOLPARTY_PROJECT_ID`, `POOLPARTY_AUTH` — rn/2-zoeken
- `TERMENNETWERK_ENDPOINT`, `TERMENNETWERK_BRONNEN` — thesaurus-zoeken
- `MCP_TRANSPORT=http`, `MCP_PORT` — voor de remote variant

Alle tools zijn uitsluitend lezend; schrijfoperaties worden geblokkeerd.

Contact: team Thesauri & Linked data (afdeling IV, cluster Erfgoeddata &
Datamanagement), thesauri@cultureelerfgoed.nl
