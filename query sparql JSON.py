#Python versie 3
import os, time

from SPARQLWrapper import SPARQLWrapper, JSON


# dit is de URL van het endpoint
sparql = SPARQLWrapper("https://linkeddata.cultureelerfgoed.nl/sparql")
sparql.setReturnFormat(JSON)

sparql.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX ceo: <https://linkeddata.cultureelerfgoed.nl/vocab/def/ceo#>
         SELECT * where {
        ?rm a <https://linkeddata.cultureelerfgoed.nl/def/ceo#Rijksmonument> .
 ?rm <https://linkeddata.cultureelerfgoed.nl/def/ceo#cultuurhistorischObjectnummer> ?nr
           
        }
        LIMIT 10
        """)
try:
        results = sparql.query().convert()

# Een result in JSON is een Python dictionary.
# De namen van de variabelen moeten letterlijk worden opgegeven 
        Ret=[]
        for result in results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    Ret.append(
                        (result["rm"]    ["value"]
                         ,  result["nr"]["value"]
                         )
                    )
                print(Ret) 
    
except Exception as e:
    if hasattr(e, 'message'):
        print(e.message)
    else:
        print(e)
