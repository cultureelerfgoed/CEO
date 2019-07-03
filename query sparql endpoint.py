# Python versie 3
# Dit script runt achter elkaar de queries die in een bestand in een folder staan.
# Resultaten worden achtereenvolgend in een logfile geplaatst.
# Een timer houdt bij hoe lang het duurde voordat de query de resultaten heeft teruggegeven 

import os, time
from SPARQLWrapper import SPARQLWrapper, XML

querydir = "C:\\Users\\YOUR NAME HERE\\Code\\Python\\RDF\\queries\\"
logfile = "C:\\Users\\YOUR NAME HERE\\Code\\Python\\RDF\\logs\\logfile.txt"

# dit is de URL van het endpoint
sparql = SPARQLWrapper("https://linkeddata.cultureelerfgoed.nl/sparql")

#returnformaat is SPARQL XML omdat dit onafhankelijk is van de queryparameters
sparql.setReturnFormat(XML)
if not os.path.exists(logfile):
    with open(logfile, 'a', encoding="UTF-8") as f:
        for file in os.listdir(querydir):
            print("running query " + file)
            queryfile = open(os.path.join(querydir, file), "r", encoding="UTF-8")
            sparql.setQuery(queryfile.read())
            print("*************OUTPUT VAN QUERY " + file + "**************", file=f)
            start = time.time()
            results = sparql.query().convert()
            end = time.time()
            print(results.toxml(), file=f)
            print("*************QUERY " + file + "   duurde " + str(end - start) + "  seconden****", file=f)
    f.close()
else:
# oude logfile weghalen, anders wordt de nieuwe run bij de vorige opgeteld
    os.remove(logfile)
    print("oude logfile verwijderd, opnieuw runnen svp")
