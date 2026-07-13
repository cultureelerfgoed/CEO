#!/usr/bin/env python3
"""
Genereert een padenkaart (ceo-padenkaart.ttl) van de CHO-dataset:
data-gedreven SHACL-shapes die per klasse tonen welke predicaten eruit
vertrekken, waar ze heen leiden en hoe goed ze gevuld zijn.

Werkwijze: start bij de tien kernklassen (de echte CHO-objectklassen),
verken per klasse de uitgaande paden op basis van een steekproef, en
volg gevonden doelklassen transitief door tot de kaart compleet is
(breadth-first met bezocht-administratie).

Gebruik:
    pip install SPARQLWrapper rdflib
    python genereer_padenkaart.py [endpoint-url]
"""

import sys
from collections import deque
from datetime import date

from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import RDF, XSD
from SPARQLWrapper import JSON, SPARQLWrapper

DEFAULT_ENDPOINT = (
    "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql"
)
CEO = "https://linkeddata.cultureelerfgoed.nl/def/ceo#"
SH = Namespace("http://www.w3.org/ns/shacl#")
DCTERMS = Namespace("http://purl.org/dc/terms/")

STEEKPROEF = 1000          # instanties per klasse
MAX_KLASSEN = 60           # veiligheidsrem op de transitieve verkenning
MIN_AANDEEL = 0.005        # paden onder 0,5% van de steekproef weglaten (ruis)

KERNKLASSEN = [
    CEO + "Rijksmonument",
    CEO + "Gezicht",
    CEO + "Werelderfgoed",
    CEO + "Complex",
    CEO + "Vondstlocatie",
    CEO + "Vondsten",
    CEO + "Grondsporen",
    CEO + "ArcheologischTerrein",
    CEO + "ArcheologischComplex",
    CEO + "ArcheologischOnderzoeksgebied",
]


def verken(sparql: SPARQLWrapper, klasse: str) -> list[dict]:
    """Uitgaande paden van een klasse op basis van een steekproef."""
    sparql.setQuery(f"""
    SELECT ?p ?doel ?soort (COUNT(*) AS ?n) WHERE {{
      {{ SELECT ?s WHERE {{ ?s a <{klasse}> }} LIMIT {STEEKPROEF} }}
      ?s ?p ?o .
      OPTIONAL {{ ?o a ?otype }}
      BIND(IF(BOUND(?otype), STR(?otype),
           IF(isLiteral(?o), STR(DATATYPE(?o)), "iri")) AS ?doel)
      BIND(IF(BOUND(?otype), "klasse",
           IF(isLiteral(?o), "datatype", "iri")) AS ?soort)
    }}
    GROUP BY ?p ?doel ?soort ORDER BY DESC(?n)
    """)
    try:
        bindings = sparql.query().convert()["results"]["bindings"]
    except Exception as e:
        print(f"  WAARSCHUWING: verkenning mislukt ({type(e).__name__}); overslaan")
        return []
    return [{k: v["value"] for k, v in rij.items()} for rij in bindings]


def main() -> None:
    endpoint = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ENDPOINT
    print(f"Endpoint: {endpoint}")
    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    g = Graph()
    g.bind("sh", SH)
    g.bind("ceo", CEO)
    g.bind("dcterms", DCTERMS)

    kaart = URIRef("https://linkeddata.cultureelerfgoed.nl/id/padenkaart/cho")
    g.add((kaart, DCTERMS.title, Literal("Padenkaart CHO-dataset", lang="nl")))
    g.add((kaart, DCTERMS.description, Literal(
        f"Data-gedreven SHACL-shapes, afgeleid uit steekproeven van "
        f"{STEEKPROEF} instanties per klasse, transitief verkend vanaf "
        f"de tien CHO-kernklassen.", lang="nl")))
    g.add((kaart, DCTERMS.created, Literal(date.today().isoformat(), datatype=XSD.date)))

    wachtrij = deque(KERNKLASSEN)
    bezocht: set[str] = set()

    while wachtrij and len(bezocht) < MAX_KLASSEN:
        klasse = wachtrij.popleft()
        if klasse in bezocht:
            continue
        bezocht.add(klasse)
        naam = klasse.split("#")[-1]
        print(f"Verkennen: {naam} ...")
        paden = verken(sparql, klasse)
        if not paden:
            print(f"  (geen instanties of paden gevonden)")
            continue

        shape = URIRef(klasse + "Shape") if "#" in klasse else BNode()
        g.add((shape, RDF.type, SH.NodeShape))
        g.add((shape, SH.targetClass, URIRef(klasse)))

        for pad in paden:
            if "p" not in pad or "n" not in pad:
                continue
            try:
                n = int(pad["n"])
            except (ValueError, TypeError):
                continue
            if n < STEEKPROEF * MIN_AANDEEL:
                continue
            ps = BNode()
            g.add((shape, SH.property, ps))
            g.add((ps, SH.path, URIRef(pad["p"])))
            soort = pad.get("soort", "")
            doel = pad.get("doel", "")
            if soort == "klasse" and doel:
                g.add((ps, SH["class"], URIRef(doel)))
                if doel.startswith(CEO):
                    wachtrij.append(doel)  # transitief doorlopen
            elif soort == "datatype" and doel:
                g.add((ps, SH.datatype, URIRef(doel)))
            g.add((ps, SH.description, Literal(
                f"Gevuld bij {n}/{STEEKPROEF} instanties in de steekproef",
                lang="nl")))

    out = "ceo-padenkaart.ttl"
    g.serialize(out, format="turtle")
    print(f"\nKlaar: {out} — {len(bezocht)} klassen verkend, {len(g)} triples")


if __name__ == "__main__":
    main()
