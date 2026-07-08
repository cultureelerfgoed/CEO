"""
ldv_mcp — MCP-server voor de RCE Linked Data Voorziening (LDV).

Ontsluit het SPARQL-endpoint van de CHO-dataset zodat een LLM (bijv. Claude
Desktop) zelf de dataset kan bevragen en o.a. een VoID-beschrijving kan
samenstellen. De server levert bewust bouwstenen (tellingen, vrije queries);
het samenstellen van de VoID-Turtle laat je aan het model over.

Installatie:
    pip install "mcp[cli]" httpx

Starten:
    Lokaal (stdio, voor Claude Desktop op dezelfde machine):
        python ldv_mcp.py
    Remote (streamable HTTP, voor centrale hosting):
        MCP_TRANSPORT=http MCP_PORT=8000 python ldv_mcp.py
        -> MCP-endpoint: http://<host>:8000/mcp

Aansluiten van clients op de remote variant:
    - claude.ai: Instellingen -> Connectors -> Custom connector -> URL invullen
    - Claude Desktop: idem via Settings -> Connectors
    - Andere MCP-clients: streamable-http transport naar dezelfde URL

Beveiliging remote variant:
    De tools zijn uitsluitend lezend en de LDV is open data, dus het risico
    is beperkt. Zet de server voor productie desondanks achter een reverse
    proxy met TLS (en eventueel een API-key of IP-filtering) op eigen infra.

Registratie in Claude Desktop (claude_desktop_config.json):
    {
      "mcpServers": {
        "ldv": {
          "command": "/usr/local/bin/python3.9",
          "args": ["/pad/naar/ldv_mcp.py"],
          "env": { "LDV_ENDPOINT": "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql" }
        }
      }
    }

Voorbeeldopdracht aan Claude daarna:
    "Genereer een VoID-beschrijving van de CHO-dataset: haal de totalen,
     klassepartities en propertypartities op via de ldv-tools en schrijf
     het resultaat als Turtle."
"""

import json
import os
import re

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, ConfigDict, Field

ENDPOINT = os.environ.get(
    "LDV_ENDPOINT",
    "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql",
)
CEO_NS = "https://linkeddata.cultureelerfgoed.nl/def/ceo#"
TIMEOUT = 120.0

mcp = FastMCP("ldv_mcp")

# Alleen lezende queryvormen toestaan.
_VERBODEN = re.compile(
    r"\b(INSERT|DELETE|LOAD|CLEAR|CREATE|DROP|COPY|MOVE|ADD)\b", re.IGNORECASE
)


async def _sparql(query: str) -> dict:
    """Voert een SPARQL-query uit tegen de LDV en geeft de JSON-resultaten."""
    if _VERBODEN.search(query):
        raise ValueError(
            "Alleen lezende queries (SELECT/ASK/CONSTRUCT/DESCRIBE) zijn "
            "toegestaan; UPDATE-operaties zijn geblokkeerd."
        )
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(
            ENDPOINT,
            content=query,
            headers={
                "Content-Type": "application/sparql-query",
                "Accept": "application/sparql-results+json",
            },
        )
        resp.raise_for_status()
        return resp.json()


def _rijen(resultaat: dict) -> list[dict]:
    """Vereenvoudigt SPARQL-JSON naar een lijst van platte dicts."""
    return [
        {var: cel["value"] for var, cel in rij.items()}
        for rij in resultaat.get("results", {}).get("bindings", [])
    ]


class SparqlSelectInput(BaseModel):
    """Invoer voor een vrije SPARQL-query."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    query: str = Field(
        ...,
        description=(
            "Een lezende SPARQL-query (SELECT/ASK). Gebruik waar mogelijk "
            "LIMIT om resultaten beperkt te houden. Prefix voor de ontologie: "
            f"PREFIX ceo: <{CEO_NS}>"
        ),
        min_length=10,
    )
    max_rijen: int = Field(
        default=100,
        description="Maximum aantal teruggegeven rijen (1-1000).",
        ge=1,
        le=1000,
    )


class PartitieInput(BaseModel):
    """Invoer voor partitie-tellingen."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    alleen_ceo: bool = Field(
        default=True,
        description=(
            "Indien true: beperk tot URI's in de CEO-namespace "
            "(compactere, relevantere VoID). Indien false: alle namespaces."
        ),
    )


@mcp.tool(
    name="ldv_sparql_select",
    annotations={
        "title": "SPARQL-query op de LDV",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_sparql_select(params: SparqlSelectInput) -> str:
    """Voert een vrije, lezende SPARQL-query uit op de LDV (CHO-dataset).

    Gebruik dit voor alles wat de gespecialiseerde teltools niet dekken,
    zoals steekproeven van instanties, het verkennen van waardepatronen
    of het controleren of een property daadwerkelijk gevuld is.

    Returns:
        str: JSON met de resultaatrijen (variabele -> waarde), afgekapt
        op max_rijen. Bevat 'aantal_rijen' en 'afgekapt' als metadata.
    """
    try:
        resultaat = await _sparql(params.query)
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "fout": f"Endpoint gaf HTTP {e.response.status_code}.",
            "suggestie": "Controleer de querysyntax; test eventueel eerst "
                         "met een LIMIT 10.",
        }, ensure_ascii=False)
    rijen = _rijen(resultaat)
    return json.dumps({
        "aantal_rijen": min(len(rijen), params.max_rijen),
        "afgekapt": len(rijen) > params.max_rijen,
        "rijen": rijen[: params.max_rijen],
    }, ensure_ascii=False)


@mcp.tool(
    name="ldv_dataset_totalen",
    annotations={
        "title": "Datasettotalen (voor VoID)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_dataset_totalen() -> str:
    """Haalt de kerncijfers van de dataset op voor een VoID-beschrijving.

    Levert de waarden voor void:triples, void:entities, void:classes en
    void:properties, plus de endpoint-URL voor void:sparqlEndpoint.

    Returns:
        str: JSON met triples, entiteiten, klassen, properties en endpoint.
    """
    queries = {
        "triples": "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }",
        "entiteiten": "SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a [] }",
        "klassen": "SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { [] a ?c }",
        "properties": "SELECT (COUNT(DISTINCT ?p) AS ?n) WHERE { [] ?p [] }",
    }
    totalen = {}
    for naam, q in queries.items():
        rijen = _rijen(await _sparql(q))
        totalen[naam] = int(rijen[0]["n"]) if rijen else 0
    totalen["endpoint"] = ENDPOINT
    return json.dumps(totalen, ensure_ascii=False)


@mcp.tool(
    name="ldv_klasse_partities",
    annotations={
        "title": "Klassepartities (void:classPartition)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_klasse_partities(params: PartitieInput) -> str:
    """Telt per klasse het aantal instanties in de dataset.

    Dit zijn de waarden voor void:classPartition / void:entities in een
    VoID-beschrijving. Toont ook welke ontologieklassen NIET in de data
    voorkomen — belangrijke informatie voor querygeneratie.

    Returns:
        str: JSON-lijst van {klasse, aantal}, aflopend gesorteerd.
    """
    rijen = _rijen(await _sparql(
        "SELECT ?c (COUNT(?s) AS ?n) WHERE { ?s a ?c } "
        "GROUP BY ?c ORDER BY DESC(?n)"
    ))
    partities = [
        {"klasse": r["c"], "aantal": int(r["n"])}
        for r in rijen
        if not params.alleen_ceo or r["c"].startswith(CEO_NS)
    ]
    return json.dumps(partities, ensure_ascii=False)


@mcp.tool(
    name="ldv_property_partities",
    annotations={
        "title": "Propertypartities (void:propertyPartition)",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_property_partities(params: PartitieInput) -> str:
    """Telt per property het aantal triples in de dataset.

    Dit zijn de waarden voor void:propertyPartition / void:triples in een
    VoID-beschrijving. Properties met lage aantallen zijn dun gevuld —
    relevant voor het inschatten van querykansrijkheid.

    Returns:
        str: JSON-lijst van {property, aantal}, aflopend gesorteerd.
    """
    rijen = _rijen(await _sparql(
        "SELECT ?p (COUNT(*) AS ?n) WHERE { ?s ?p ?o } "
        "GROUP BY ?p ORDER BY DESC(?n)"
    ))
    partities = [
        {"property": r["p"], "aantal": int(r["n"])}
        for r in rijen
        if not params.alleen_ceo or r["p"].startswith(CEO_NS)
    ]
    return json.dumps(partities, ensure_ascii=False)




class VerkenKlasseInput(BaseModel):
    """Invoer voor padverkenning vanaf een klasse."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    klasse: str = Field(
        ...,
        description=(
            "Volledige URI van de te verkennen klasse, bijv. "
            f"{CEO_NS}Rijksmonument"
        ),
        min_length=10,
    )
    steekproef: int = Field(
        default=1000,
        description=(
            "Aantal instanties in de steekproef (100-10000). Groter = "
            "vollediger beeld, maar zwaarder voor het endpoint."
        ),
        ge=100,
        le=10000,
    )


@mcp.tool(
    name="ldv_verken_klasse",
    annotations={
        "title": "Verken uitgaande paden van een klasse",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_verken_klasse(params: VerkenKlasseInput) -> str:
    """Ontdekt welke predicaten vanaf een klasse vertrekken en waar ze
    naartoe leiden (doelklasse of datatype), op basis van een steekproef
    van instanties.

    Gebruik dit om iteratief door de graaf te navigeren bij het opbouwen
    van een querypad: start bij de klasse van de vraag, volg het relevante
    predicaat naar de doelklasse, en verken die opnieuw tot je bij de
    gewenste waarde (literal) bent. De aantallen tonen ook hoe goed een
    pad gevuld is binnen de steekproef.

    Returns:
        str: JSON-lijst van {predicaat, doel, soort, aantal}, waarbij
        soort 'klasse', 'datatype' of 'iri-zonder-type' is, aflopend
        gesorteerd op aantal binnen de steekproef.
    """
    q = f"""
    SELECT ?p ?doel ?soort (COUNT(*) AS ?n) WHERE {{
      {{ SELECT ?s WHERE {{ ?s a <{params.klasse}> }} LIMIT {params.steekproef} }}
      ?s ?p ?o .
      OPTIONAL {{ ?o a ?otype }}
      BIND(
        IF(BOUND(?otype), STR(?otype),
          IF(isLiteral(?o), STR(DATATYPE(?o)), "iri-zonder-type")
        ) AS ?doel)
      BIND(
        IF(BOUND(?otype), "klasse",
          IF(isLiteral(?o), "datatype", "iri-zonder-type")
        ) AS ?soort)
    }}
    GROUP BY ?p ?doel ?soort
    ORDER BY DESC(?n)
    """
    try:
        rijen = _rijen(await _sparql(q))
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "fout": f"Endpoint gaf HTTP {e.response.status_code}.",
            "suggestie": "Verklein de steekproef of controleer de klasse-URI.",
        }, ensure_ascii=False)
    paden = [
        {
            "predicaat": r.get("p", ""),
            "doel": r.get("doel", ""),
            "soort": r.get("soort", ""),
            "aantal": int(r.get("n", 0)),
        }
        for r in rijen
    ]
    return json.dumps({
        "klasse": params.klasse,
        "steekproef": params.steekproef,
        "paden": paden,
    }, ensure_ascii=False)




@mcp.tool(
    name="ldv_verken_inkomend",
    annotations={
        "title": "Verken inkomende paden naar een klasse",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_verken_inkomend(params: VerkenKlasseInput) -> str:
    """Ontdekt vanuit welke klassen en via welke predicaten er naar
    instanties van deze klasse wordt verwezen (achteruit navigeren).

    Gebruik dit voor vragen waarbij het pad omgekeerd loopt, zoals
    "bij welk complex hoort dit rijksmonument": verken inkomend op
    Rijksmonument en je vindt Complex -> heeftRijksmonument.

    Returns:
        str: JSON-lijst van {bronklasse, predicaat, aantal}, aflopend
        gesorteerd op aantal binnen de steekproef.
    """
    q = f"""
    SELECT ?bron ?p (COUNT(*) AS ?n) WHERE {{
      {{ SELECT ?o WHERE {{ ?o a <{params.klasse}> }} LIMIT {params.steekproef} }}
      ?s ?p ?o .
      OPTIONAL {{ ?s a ?bron }}
    }}
    GROUP BY ?bron ?p
    ORDER BY DESC(?n)
    """
    try:
        rijen = _rijen(await _sparql(q))
    except httpx.HTTPStatusError as e:
        return json.dumps({
            "fout": f"Endpoint gaf HTTP {e.response.status_code}.",
            "suggestie": "Verklein de steekproef of controleer de klasse-URI.",
        }, ensure_ascii=False)
    paden = [
        {
            "bronklasse": r.get("bron", "onbekend"),
            "predicaat": r.get("p", ""),
            "aantal": int(r.get("n", 0)),
        }
        for r in rijen
    ]
    return json.dumps({
        "klasse": params.klasse,
        "steekproef": params.steekproef,
        "inkomende_paden": paden,
    }, ensure_ascii=False)




class ZoekConceptInput(BaseModel):
    """Invoer voor conceptzoeken in de waardenlijsten."""
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    term: str = Field(
        ...,
        description="Zoekterm in natuurlijke taal, bijv. 'kerk' of 'baksteen'.",
        min_length=2,
    )
    bron: str = Field(
        default="alle",
        description=(
            "Waar te zoeken: 'termennetwerk' (CHT en andere gepubliceerde "
            "thesauri via het NDE Termennetwerk), 'rn' (referentienetwerk "
            "rn/2 via PoolParty-SPARQL) of 'alle' (beide)."
        ),
        pattern="^(termennetwerk|rn|alle)$",
    )
    max_resultaten: int = Field(
        default=25, description="Maximum aantal concepten per bron (1-100).",
        ge=1, le=100,
    )
    klasse_filter: str = Field(
        default="",
        description=(
            "Optioneel, alleen voor bron 'rn': filter op concepttype via een "
            "rnce-klasse-URI, bijv. "
            "https://data.cultureelerfgoed.nl/id/rnce#Function voor functies."
        ),
    )


TERMENNETWERK_ENDPOINT = os.environ.get(
    "TERMENNETWERK_ENDPOINT",
    "https://termennetwerk-api.netwerkdigitaalerfgoed.nl/graphql",
)
TERMENNETWERK_BRONNEN = os.environ.get(
    "TERMENNETWERK_BRONNEN",
    "https://data.cultureelerfgoed.nl/term/id/cht",
).split(",")
# PoolParty (referentienetwerk rn/2, incl. ABR) — REST-API met Basic-auth.
POOLPARTY_BASE = os.environ.get(
    "POOLPARTY_BASE", "https://digitaalerfgoed.poolparty.biz"
)
POOLPARTY_PROJECT_ID = os.environ.get(
    "POOLPARTY_PROJECT_ID", "1DF17ED7-1ED6-0001-11B0-1350116C3790"
)
# Zet als "gebruikersnaam:wachtwoord" in de omgeving; nooit in code of chat.
POOLPARTY_AUTH = os.environ.get("POOLPARTY_AUTH", "")


async def _zoek_termennetwerk(term: str, maxr: int) -> list[dict]:
    """Zoekt via de GraphQL-API van het NDE Termennetwerk."""
    bronnen = ", ".join(f'"{b.strip()}"' for b in TERMENNETWERK_BRONNEN)
    graphql = {
        "query": f"""query {{
          terms(sources: [{bronnen}], query: "{term.replace('"', '')}") {{
            source {{ name uri }}
            result {{
              __typename
              ... on Terms {{
                terms {{ uri prefLabel altLabel }}
              }}
            }}
          }}
        }}"""
    }
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        resp = await client.post(TERMENNETWERK_ENDPOINT, json=graphql)
        resp.raise_for_status()
        data = resp.json()
    concepten = []
    for bron in data.get("data", {}).get("terms", []):
        bron_naam = bron.get("source", {}).get("name", "")
        for c in (bron.get("result", {}) or {}).get("terms", [])[:maxr]:
            concepten.append({
                "uri": c.get("uri", ""),
                "prefLabel": "; ".join(c.get("prefLabel") or []),
                "altLabel": "; ".join(c.get("altLabel") or []) or None,
                "bron": bron_naam or "Termennetwerk",
            })
    return concepten


async def _zoek_rn(term: str, maxr: int, klasse_filter: str = "") -> list[dict]:
    """Zoekt in het referentienetwerk (rn/2, incl. ABR) via de PoolParty
    Suggest API (/extractor/api/suggest), met Basic-authenticatie."""
    if not POOLPARTY_AUTH or ":" not in POOLPARTY_AUTH:
        raise RuntimeError(
            "POOLPARTY_AUTH is niet geconfigureerd. Zet de omgevings-"
            "variabele als 'gebruikersnaam:wachtwoord' voor de PoolParty-"
            "omgeving; de rn/2-lijsten zijn alleen met authenticatie "
            "bevraagbaar."
        )
    gebruiker, _, wachtwoord = POOLPARTY_AUTH.partition(":")
    params = {
        "projectId": POOLPARTY_PROJECT_ID,
        "language": "nl",
        "searchString": term,
    }
    if klasse_filter:
        params["customClassFilters"] = klasse_filter
    async with httpx.AsyncClient(
        timeout=TIMEOUT, auth=(gebruiker, wachtwoord)
    ) as client:
        resp = await client.get(
            f"{POOLPARTY_BASE}/extractor/api/suggest", params=params
        )
        resp.raise_for_status()
        data = resp.json()

    # Responsvorm verschilt per PoolParty-versie; defensief parsen.
    kandidaten = (
        data.get("suggestedConcepts")
        or data.get("results")
        or data.get("concepts")
        or (data if isinstance(data, list) else [])
    )
    concepten = []
    for c in kandidaten[:maxr]:
        pref = c.get("prefLabel") or c.get("prefLabels") or ""
        if isinstance(pref, list):
            pref = "; ".join(
                p.get("label", p) if isinstance(p, dict) else str(p)
                for p in pref
            )
        elif isinstance(pref, dict):
            pref = pref.get("label", "")
        concepten.append({
            "uri": c.get("uri") or c.get("id", ""),
            "prefLabel": pref,
            "altLabel": None,
            "bron": "Referentienetwerk rn/2 incl. ABR (PoolParty Suggest)",
        })
    if not concepten and kandidaten == []:
        # Geef de structuur terug zodat parsing bijgesteld kan worden.
        concepten.append({
            "uri": "",
            "prefLabel": f"(onverwachte responsvorm: {str(data)[:200]})",
            "altLabel": None,
            "bron": "PoolParty Suggest — parsing controleren",
        })
    return concepten


@mcp.tool(
    name="ldv_zoek_concept",
    annotations={
        "title": "Zoek concepten in de waardenlijsten",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    },
)
async def ldv_zoek_concept(params: ZoekConceptInput) -> str:
    """Zoekt SKOS-concepten in de waardenlijsten op basis van een term.

    De waardenlijsten leven NIET in de LDV zelf: het referentienetwerk
    (rn/2, inclusief de ABR-begrippen) is bevraagbaar via de PoolParty\n    Suggest API (met authenticatie), de gepubliceerde thesauri
    (zoals de CHT) via het NDE Termennetwerk. Deze tool bevraagt beide.

    Gebruik dit ALTIJD voordat je op conceptwaarden filtert: resolve eerst
    de natuurlijke-taalterm naar concept-URI's (vindt ook synoniemen via
    altLabel), en filter daarna in de CHO-query exact op die URI's met
    VALUES, in plaats van met CONTAINS op labels.

    Returns:
        str: JSON met per gevonden concept: uri, prefLabel, altLabel en bron.
    """
    concepten, fouten = [], []
    if params.bron in ("termennetwerk", "alle"):
        try:
            concepten += await _zoek_termennetwerk(params.term, params.max_resultaten)
        except Exception as e:
            fouten.append(f"Termennetwerk: {e}")
    if params.bron in ("rn", "alle"):
        try:
            concepten += await _zoek_rn(params.term, params.max_resultaten, params.klasse_filter)
        except Exception as e:
            fouten.append(f"rn/PoolParty: {e}")
    antwoord = {
        "term": params.term,
        "aantal": len(concepten),
        "concepten": concepten,
        "tip": "Filter in vervolgqueries op de CHO-dataset met "
               "VALUES ?concept { <uri1> <uri2> } in plaats van CONTAINS.",
    }
    if fouten:
        antwoord["waarschuwingen"] = fouten
    return json.dumps(antwoord, ensure_ascii=False)


if __name__ == "__main__":
    if os.environ.get("MCP_TRANSPORT", "stdio").lower() in ("http", "streamable-http"):
        mcp.settings.host = os.environ.get("MCP_HOST", "0.0.0.0")
        mcp.settings.port = int(os.environ.get("MCP_PORT", "8000"))
        mcp.settings.stateless_http = True
        mcp.run(transport="streamable-http")
    else:
        mcp.run()
