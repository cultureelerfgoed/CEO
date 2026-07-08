"""Telt per CEO-klasse het aantal instanties in de LDV (CHO-dataset).
Geen pakketten nodig — alleen de Python-standaardbibliotheek.
Gewoon runnen in PyCharm; resultaat verschijnt in de console.
"""
import json
import urllib.request

ENDPOINT = "https://api.linkeddata.cultureelerfgoed.nl/datasets/rce/cho/services/cho/sparql"
CEO = "https://linkeddata.cultureelerfgoed.nl/def/ceo#"

QUERY = """
SELECT ?klasse (COUNT(?s) AS ?aantal)
WHERE { ?s a ?klasse . FILTER(STRSTARTS(STR(?klasse), "%s")) }
GROUP BY ?klasse ORDER BY DESC(?aantal)
""" % CEO


def sparql(query):
    req = urllib.request.Request(
        ENDPOINT,
        data=query.encode("utf-8"),
        headers={
            "Content-Type": "application/sparql-query",
            "Accept": "application/sparql-results+json",
        },
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read())


def main():
    print(f"Bevragen van: {ENDPOINT}\n")
    rijen = sparql(QUERY)["results"]["bindings"]
    print(f"{'Instanties':>12}  CEO-klasse")
    print("-" * 60)
    totaal = 0
    for rij in rijen:
        klasse = rij["klasse"]["value"].replace(CEO, "ceo:")
        aantal = int(rij["aantal"]["value"])
        totaal += aantal
        print(f"{aantal:>12,}  {klasse}")
    print("-" * 60)
    print(f"{totaal:>12,}  totaal ({len(rijen)} klassen met instanties)")


if __name__ == "__main__":
    main()
