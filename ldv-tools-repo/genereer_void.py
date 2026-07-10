#!/usr/bin/env python3
"""
Genereert een VoID-beschrijving (ceo-void.ttl) van de CHO-dataset in de RCE LDV.

Bevraagt het SPARQL-endpoint voor:
  - totaal aantal triples, entiteiten, klassen en properties
  - void:classPartition per klasse (aantal instanties)
  - void:propertyPartition per property (aantal triples)

Gebruik:
  pip install SPARQLWrapper rdflib
  python genereer_void.py [endpoint-url]

Zonder argument wordt de standaard LDV-endpoint-URL gebruikt (controleer deze!).
Output: ceo-void.ttl in de huidige map.
"""

import sys
from datetime import date

from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, XSD
from SPARQLWrapper import JSON, SPARQLWrapper

# --- Configuratie -----------------------------------------------------------

DEFAULT_ENDPOINT = (
    "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql"
)
DATASET_URI = URIRef("https://linkeddata.cultureelerfgoed.nl/id/dataset/cho")
CEO_NS = "https://linkeddata.cultureelerfgoed.nl/def/ceo#"

VOID = Namespace("http://rdfs.org/ns/void#")
FORMATS = Namespace("http://www.w3.org/ns/formats/")

# Beperk partities tot CEO-namespace zodat de VoID compact en relevant blijft.
ONLY_CEO_PARTITIONS = True

# Externe doeldatasets voor void:Linkset-detectie: namespace-prefix -> naam.
EXTERNE_DATASETS = {
    "https://data.cultureelerfgoed.nl/term/id/rn/": "RCE-referentienetwerk (rn)",
    "https://data.cultureelerfgoed.nl/term/id/cht/": "Cultuurhistorische Thesaurus (CHT)",
    "https://data.cultureelerfgoed.nl/term/id/abr/": "Archeologisch Basisregister (ABR)",
    "http://standaarden.overheid.nl/owms/terms/": "OWMS (gemeenten/provincies)",
    "https://identifier.overheid.nl/tooi/": "TOOI",
    "https://bag.basisregistraties.overheid.nl/": "BAG (Kadaster)",
    "https://brk.basisregistraties.overheid.nl/": "BRK (Kadaster)",
}


def query(sparql: SPARQLWrapper, q: str) -> list[dict]:
    sparql.setQuery(q)
    return sparql.query().convert()["results"]["bindings"]


def scalar(sparql: SPARQLWrapper, q: str, var: str) -> int:
    rows = query(sparql, q)
    return int(rows[0][var]["value"]) if rows else 0


def main() -> None:
    endpoint = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_ENDPOINT
    print(f"Endpoint: {endpoint}")

    sparql = SPARQLWrapper(endpoint)
    sparql.setReturnFormat(JSON)

    print("Totalen ophalen...")
    triples = scalar(sparql, "SELECT (COUNT(*) AS ?n) WHERE { ?s ?p ?o }", "n")
    entities = scalar(
        sparql, "SELECT (COUNT(DISTINCT ?s) AS ?n) WHERE { ?s a [] }", "n"
    )
    n_classes = scalar(
        sparql, "SELECT (COUNT(DISTINCT ?c) AS ?n) WHERE { [] a ?c }", "n"
    )
    n_props = scalar(
        sparql, "SELECT (COUNT(DISTINCT ?p) AS ?n) WHERE { [] ?p [] }", "n"
    )
    print(f"  {triples:,} triples, {entities:,} entiteiten, "
          f"{n_classes} klassen, {n_props} properties")

    print("Klassepartities ophalen...")
    class_rows = query(sparql, """
        SELECT ?c (COUNT(?s) AS ?n)
        WHERE { ?s a ?c }
        GROUP BY ?c ORDER BY DESC(?n)
    """)

    print("Linksets detecteren (objectnamespaces per property)...")
    linkset_rows = query(sparql, """
        SELECT ?p ?ns (COUNT(*) AS ?n) WHERE {
          ?s ?p ?o .
          FILTER(isIRI(?o))
          BIND(REPLACE(STR(?o), "(#|/)[^#/]*$", "$1") AS ?ns)
        }
        GROUP BY ?p ?ns ORDER BY DESC(?n)
    """)

    print("Propertypartities ophalen...")
    prop_rows = query(sparql, """
        SELECT ?p (COUNT(*) AS ?n)
        WHERE { ?s ?p ?o }
        GROUP BY ?p ORDER BY DESC(?n)
    """)

    # --- VoID-graaf opbouwen -------------------------------------------------
    g = Graph()
    g.bind("void", VOID)
    g.bind("dcterms", DCTERMS)

    d = DATASET_URI
    g.add((d, RDF.type, VOID.Dataset))
    g.add((d, DCTERMS.title, Literal("CHO-dataset (Cultuurhistorische Objecten)", lang="nl")))
    g.add((d, DCTERMS.description, Literal(
        "Linked-data-publicatie van cultuurhistorische objecten van de RCE, "
        "beschreven volgens de Cultureel Erfgoed Ontologie (CEO).", lang="nl")))
    g.add((d, DCTERMS.publisher, URIRef(
        "http://standaarden.overheid.nl/owms/terms/Rijksdienst_voor_het_Cultureel_Erfgoed")))
    g.add((d, DCTERMS.license, URIRef("https://creativecommons.org/licenses/by/4.0/")))
    g.add((d, DCTERMS.modified, Literal(date.today().isoformat(), datatype=XSD.date)))
    g.add((d, VOID.sparqlEndpoint, URIRef(endpoint)))
    g.add((d, VOID.uriSpace, Literal("https://linkeddata.cultureelerfgoed.nl/")))
    g.add((d, VOID.vocabulary, URIRef(CEO_NS.rstrip("#"))))
    g.add((d, VOID.vocabulary, URIRef("http://www.w3.org/2004/02/skos/core")))
    g.add((d, VOID.vocabulary, URIRef("http://www.opengis.net/ont/geosparql")))
    g.add((d, VOID.feature, FORMATS.Turtle))

    g.add((d, VOID.triples, Literal(triples, datatype=XSD.integer)))
    g.add((d, VOID.entities, Literal(entities, datatype=XSD.integer)))
    g.add((d, VOID.classes, Literal(n_classes, datatype=XSD.integer)))
    g.add((d, VOID.properties, Literal(n_props, datatype=XSD.integer)))

    for row in class_rows:
        cls = row["c"]["value"]
        if ONLY_CEO_PARTITIONS and not cls.startswith(CEO_NS):
            continue
        part = URIRef(f"{DATASET_URI}/klasse/{cls.split('#')[-1]}")
        g.add((d, VOID.classPartition, part))
        g.add((part, VOID["class"], URIRef(cls)))
        g.add((part, VOID.entities, Literal(int(row["n"]["value"]), datatype=XSD.integer)))

    for row in prop_rows:
        prop = row["p"]["value"]
        if ONLY_CEO_PARTITIONS and not prop.startswith(CEO_NS):
            continue
        part = URIRef(f"{DATASET_URI}/property/{prop.split('#')[-1]}")
        g.add((d, VOID.propertyPartition, part))
        g.add((part, VOID.property, URIRef(prop)))
        g.add((part, VOID.triples, Literal(int(row["n"]["value"]), datatype=XSD.integer)))

    # void:Linkset per (property, externe dataset)
    ls_nr = 0
    for row in linkset_rows:
        if "ns" not in row or "p" not in row or "n" not in row:
            continue
        ns = row["ns"]["value"]
        doel = next((naam for prefix, naam in EXTERNE_DATASETS.items()
                     if ns.startswith(prefix)), None)
        if doel is None:
            continue
        prefix = next(p for p in EXTERNE_DATASETS if ns.startswith(p))
        ls_nr += 1
        ls = URIRef(f"{DATASET_URI}/linkset/{ls_nr}")
        g.add((ls, RDF.type, VOID.Linkset))
        g.add((ls, VOID.subjectsTarget, d))
        g.add((ls, VOID.objectsTarget, URIRef(prefix)))
        g.add((ls, VOID.linkPredicate, URIRef(row["p"]["value"])))
        g.add((ls, VOID.triples, Literal(int(row["n"]["value"]), datatype=XSD.integer)))
        g.add((ls, DCTERMS.description, Literal(f"Links naar {doel}", lang="nl")))
    print(f"  {ls_nr} linksets naar externe datasets gevonden")

    out = "ceo-void.ttl"
    g.serialize(out, format="turtle")
    print(f"Klaar: {out} ({len(g)} triples)")


if __name__ == "__main__":
    main()
