# Dit script maakt het mogelijk om onderdelen van je Python routine mee te nemen in een SPARQL query. 
# De querystring wordt dynamish opgebouwd
#Python versie 3
import os, time, re

from SPARQLWrapper import SPARQLWrapper, JSON


# dit is de URL van het endpoint
sparql = SPARQLWrapper("https://linkeddata.cultureelerfgoed.nl/sparql")
sparql.setReturnFormat(JSON)
prefix = "PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> PREFIX ceo: <https://linkeddata.cultureelerfgoed.nl/vocab/def/ceo#>"
query_select = "SELECT"
query_where = "where {"
query_var = "?rm "
query_condition = "a <https://linkeddata.cultureelerfgoed.nl/def/ceo#Rijksmonument> .\
          ?rm <https://linkeddata.cultureelerfgoed.nl/def/ceo#cultuurhistorischObjectnummer> ?nr \
                } \
          LIMIT 10"


sparql.setQuery(prefix + query_select + "* "+ query_where + query_var + query_condition )
try:
        results = sparql.query().convert()

# Een result in JSON is een Python dictionary.
# De namen van de variabelen moeten letterlijk worden opgegeven 
        Ret=[]
        for result in results["results"]["bindings"]:
                for result in results["results"]["bindings"]:
                    Ret.append(
                        (result[re.sub("[? ]", "", query_var)]    ["value"]
                         ,  result["nr"]["value"]
                         )
                    )
                print(Ret) 
    
except Exception as e:
    if hasattr(e, 'message'):
        print(e.message)
    else:
        print(e)
