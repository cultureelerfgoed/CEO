De ZAAK ontologieën





# Inhoudsopgave


# Inleiding

Het RCE zaakmodel is gebaseerd op het RGBZ versie 1.1 en aangepast voor het gebruik bij de RCE (Objectencatalogus RCE-Zaken versie 0.3). 


Het uitgebreidere model, dat overigens niet door RCE wordt gebruikt, zijn de verbindingen met de ruimere betekenis van “Betrokkene” weergegeven. 

De zaaktype catalogus (ZTCO) en de zaaktype eigenschappen (ZTCEO) zijn allebei in een aparte ontologie opgenomen conform de beschrijving in het document Objectencatalogus RCE-Zaken. Onderstaande afbeelding is het UML model van de ZTCO.

De zaaktype catalogus ontologie (ZTCO) wordt geïmporteerd in de ZAAK ontologie (ZO) om de koppeling tussen beide te realiseren. De zaaktype eigenschappen ontologie (ZTCEO) wordt in de ZTCO geïmporteerd. 

# Ontwerpbesluiten

1. Het RGBZ staat verschillende soorten objecten toe. Bij de RCE is in de implementatie van het zaakmodel een (zaak)object altijd een CultuurhistorischObject.
2. De zaakontologie (ZAAK) is in principe volledig in overeenstemming met het conceptuele model ZAAK. Echter:
3.  In het ZAAK-model hebben niet alle relaties een ‘naam’ die de specifieke semantische betekenis weergeeft. Bv ‘betreft’. Hebben daarom de Objectproperties een naam gegeven waar de range aan het einde is opgenomen. Hierdoor worden de objectproperties specifiek tussen twee resources. Bijvoorbeeld: zo:betreft wordt zo:betreftRol  (in het UML model staat er alleen “betreft”) en property zo:isOnderwerpVan wordt zo:isOnderwerpVanZaak. 
4. Daarnaast zijn ook inverse properties gemodelleerd.
5. We werken Betrokkene voorlopig niet uit want de informatie kan niet naar de linked data voorziening vanwege AVG.
6. We hebben wel de relatie naar Betrokkene gemodelleerd, maar niet de eigenschappen!
7. Wanneer er sprake is van relatie tussen CEO en ZO, dan kiezen we voor de ontologie waar de data zit. Voorbeeld zo:heeftDocument en ceo:heeftKennisregistratie.
8. De property documentid (domein Document) uit het DMS, is nu nog een DatatypeProperty. Maar wordt straks in de DMS ontologie gemodelleerd als ObjectProperty.
9. De ontologieën CEO en ZAAK verwijzen naar elkaar met de objectproperties: zo:betreftZaakObject inverse zo:betreftCultuurhistortischObject.

# Metadata informatie

### De ZAAK Ontologie (ZO)

Base URI: [https://data.cultureelerfgoed.nl/def/zo](https://data.cultureelerfgoed.nl/vocab/def/zo)

### De Zaak Type Catalogus Ontologie (ZTCO)

Base URI: https://data.cultureelerfgoed.nl/def/ztco



| **prefix** | **Namespace URI**                                |
| ---------- | ------------------------------------------------ |
| ceo        | https://linkeddata.cultureelerfgoed.nl/def/ceo#  |
| dcterms    | http://purl.org/dc/terms/                        |
| foaf       | http://xmlns.com/foaf/0.1/                       |
| owl        | http://www.w3.org/2002/07/owl#                   |
| rdf        | http://www.w3.org/1999/02/22-rdf-syntax-ns#      |
| rdfs       | http://www.w3.org/2000/01/rdf-schema#            |
| skos       | http://www.w3.org/2004/02/skos/core#             |
| xsd        | http://www.w3.org/2001/XMLSchema#                |
| zo         | https://linkeddata.cultureelerfgoed.nl/def/zo#   |
| ztco       | https://linkeddata.cultureelerfgoed.nl/def/ztco# |


### De Zaak Type Catalogus Eigenschappen Ontologie (ZTCEO)

Base URI:[ https://data.cultureelerfgoed.nl/def/ztceo](https://data.cultureelerfgoed.nl/vocab/def/ztceo)



| **prefix** | **Namespace URI**                                 |
| ---------- | ------------------------------------------------- |
| ceo        | https://linkeddata.cultureelerfgoed.nl/def/ceo#   |
| dcterms    | http://purl.org/dc/terms/                         |
| foaf       | http://xmlns.com/foaf/0.1/                        |
| owl        | http://www.w3.org/2002/07/owl#                    |
| rdf        | http://www.w3.org/1999/02/22-rdf-syntax-ns#       |
| rdfs       | http://www.w3.org/2000/01/rdf-schema#             |
| skos       | http://www.w3.org/2004/02/skos/core#              |
| xsd        | http://www.w3.org/2001/XMLSchema#                 |
| ztceo      | https://linkeddata.cultureelerfgoed.nl/def/ztceo# |



N.B. De ZTCEO ontologie bevat uitsluitend instanties van de ZTCO eigenschapstypen die specifiek zijn voor de RCE.