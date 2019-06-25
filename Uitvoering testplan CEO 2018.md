<span id="anchor"></span>Testplan

Voer de test uit via de testmethode in de testomgeving met de testscripts

<span id="anchor-1"></span>Testmethode

*ontologie*

Visuele inspectie ontologie in Visio (compleetheid, naamgeving, patronen)

Visuele inspectie ontologie in Composer (compleetheid, naamgeving, patronen)

Het runnen van ontologie test scripts in Composer (voor valideren ontologie)

Het runnen van een reasoner in Composer op testdata

*data*

Runnen van testscripts in GraphDB

API

Runnen van testscripts in Postman

<span id="anchor-2"></span>Testomgeving

Topbraid Composer (visuele inspectie, reasoner)

GraphDB (test met scripts)

Postman (test met scripts)

<span id="anchor-3"></span>Testscripts (D= data, O=ontologie)

*D: query lege ceo properties*

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns\#&gt;

PREFIX owl: &lt;http://www.w3.org/2002/07/owl\#&gt;

select ?ceo\_property where {

?ceo\_property a ?type . FILTER (?type in (owl:ObjectProperty, owl:DatatypeProperty)). FILTER (regex(str(?ceo\_property), "def")) . FILTER not EXISTS {?inst ?ceo\_property ?waarde}

} order by asc (?ceo\_property)

*D: query lege ceo classes*

PREFIX owl: &lt;http://www.w3.org/2002/07/owl\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select distinct ?class ?inst where {

?class ?a owl:Class . FILTER NOT EXISTS { ?inst rdfs:domain ?class }

}

\*\*\*\*\*\*\*\*

*O: welke ontologieën worden hergebruikt:*

SELECT \*

WHERE

{?ontologie owl:imports ?import

}

\*\*\*\*\*\*\*\*

*O: wat is van alle properties de range?*

select ?p ?range

WHERE

{

?p rdfs:range ?range

FILTER (strstarts(str(?p),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*

*O: wat is van alle properties het domein?*

select ?p ?domain

WHERE

{

?p rdfs:domain ?domain

FILTER (strstarts(str(?p),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*

*O: welke properties hebben meer dan 1 domein:*

SELECT distinct ?s ?domain

WHERE

{?s ?p ?o

 { SELECT ?s WHERE { ?s rdfs:domain ?domain }

GROUP BY ?s HAVING (COUNT(?domain) &gt; 1) }

?s rdfs:domain ?domain

}

\*\*\*\*\*\*\*\*

*O: wat is de lijst van ceo classes:*

select ?class

WHERE

{

?class a owl:Class

FILTER (strstarts(str(?class),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*

*O: hoeveel classes zijn er?*

select (count(?class) as ?count)

WHERE

{

?class a owl:Class

FILTER (strstarts(str(?class),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*

*O: welke elementen die niet de ceo prefix hebben zijn aanwezig in de ontologie:*

select distinct ?s

WHERE

{

?s ?p ?o

FILTER (!strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*

select distinct ?p

WHERE

{

?s ?p ?o

FILTER (!strstarts(str(?p),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*

select distinct ?o

WHERE

{

?s ?p ?o .

FILTER (isuri(?o))

FILTER (!strstarts(str(?o),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*

*D: hoeveel instanties van elke class *

select ?class (count(?instantie) as ?aantal\_instanties)

WHERE {

?instantie a ?class

}

GROUP BY ?class

ORDER BY desc (?aantal\_instanties)

\*\*\*\*\*\*\*\*\*

*O: *<span id="anchor-4"></span>*O: zitten er blank nodes in de ontologie?*

select ?s

WHERE

{

?s ?p ?o

FILTER (isblank(?s))

}

\*\*\*\*\*\*\*\*\*

*D: welke instances hebben een NL taal* (uitgevoerd)

select ?p ?lang

WHERE

{?s ?p ?o

filter (!isuri(?o))

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

BIND (lang(?o) as ?lang)

FILTER (?lang != "nl")

}

\*\*\*\*\*\*\*\*\*\*\*

*D: welke instances hebben een taal anders dan NL (uitgevoerd)*

select ?s ?o ?lang

WHERE

{?s ?p ?o

filter (!isuri(?o))

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

BIND (lang(?o) as ?lang)

FILTER((?lang != "nl")&&(?lang!=""))

}

\*\*\*\*\*\*\*\*\*\*\*\*

*D: *<span id="anchor-5"></span>*D: welke instances met een string property hebben geen language tag?*

select \*

WHERE

{?s ?p ?o .

filter (!isuri(?o))

?p rdfs:range xsd:string .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

BIND (lang(?o) as ?lang)

FILTER((?lang=""))

}

\*\*\*\*\*\*\*\*\*\*\*

*O: *<span id="anchor-6"></span>*O: welke ceo classes zijn een subclass van een class uit een andere ontologie?*

select \*

WHERE

{?class a owl:Class .

?sub rdfs:subClassOf ?class .

FILTER (!strstarts(str(?class),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER (strstarts(str(?sub),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*\*\*\*

*O: *<span id="anchor-7"></span>*O: welke ceo objectproperty is een subproperty van een property uit een andere ontologie?*

select \*

WHERE

{?objp a owl:ObjectProperty .

?subp rdfs:subPropertyOf ?objp .

FILTER (!strstarts(str(?objp),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER (strstarts(str(?subp),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke ceo datatypeproperty is een subproperty van een property uit een andere ontologie?*

select \*

WHERE

{?datap a owl:DatatypeProperty .

?subp rdfs:subPropertyOf ?datap .

FILTER (!strstarts(str(?datap),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER (strstarts(str(?subp),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

select \*

WHERE

{?datap a rdf:Property .

?subp rdfs:subPropertyOf ?datap .

FILTER (!strstarts(str(?datap),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER (strstarts(str(?subp),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

<span id="anchor-8"></span>

*O: welke zijn boolean properties?*

SELECT distinct ?p

WHERE

{?p a owl:DatatypeProperty ;

rdfs:range xsd:boolean

 }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-9"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: classes en properties hebben geen rdfs:label*

select distinct ?s

WHERE {?s ?p ?o .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER NOT EXISTS { ?s rdfs:label ?label }

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-10"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: juiste string bij rdfs:comment van een Class*

select distinct ?s

WHERE {?s rdfs:comment ?comment .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

?s a owl:Class .

FILTER (!contains(?comment, "De class") ||(!contains(?comment, "is de representatie van")))

}

<span id="anchor-11"></span>

*O: juiste string bij rdfs:comment van een ObjectProperty*

select distinct ?s

WHERE {?s rdfs:comment ?comment .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

?s a owl:ObjectProperty .

FILTER (!contains(?comment, "De property") ||(!contains(?comment, "legt de relatie tussen")))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-12"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: juiste string bij rdfs:comment van een DatatypeProperty*

select distinct ?s

WHERE {?s rdfs:comment ?comment .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

?s a owl:DatatypeProperty .

FILTER (!contains(?comment, "De property") ||(!contains(?comment, "wordt gebruikt om aan te geven")))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-13"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: qname van property of class bestaat uit alleen letters*

select distinct ?s

WHERE {?s ?p ?o ;

 a ?type .

FILTER (?type in (owl:Class, owl:ObjectProperty, owl:DatatypeProperty))

BIND ("https://linkeddata.cultureelerfgoed.nl/def/ceo\#" as ?prefix)

FILTER (strstarts(str(?s),?prefix))

BIND (strafter(str(?s),"\#") as ?qname)

FILTER regex(?qname, "\[^a-zA-Z\]")

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-14"></span>*D: welke cultuurhistorische objecten hebben geen cultuurhistorisch objectnummer (uitgevoerd)*

select distinct ?s

WHERE {?s ?p ?o ; rdfs:subClassOf ceo:CultuurhistorischObject .

FILTER NOT EXISTS {?s ceo:cultuurhistorischObjectnummer ?nummer }

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-15"></span>*D: welke kennis objecten hebben (g)een kennisregistratienummer (uitgevoerd)*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \*

where {?s ceo:kennisregistratienummer ?kennisregistratienummer } limit 100

select distinct ?s

WHERE {?s ?p ?o ; rdfs:subClassOf ceo:Kennisregistratie.

FILTER NOT EXISTS {?s ceo:kennisregistratienummer ?nummer }

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-16"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke classes hebben een nummer-property*

select distinct ?o ?s

WHERE {?s rdfs:domain ?o .

FILTER (strstarts(str(?o),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#")) .

FILTER (strends(str(?s),"nummer"))

 }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-17"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke (hoeveel) classes hebben geen rdfs:comment*

select distinct ?s

\# (count(?s) as ?aantal)

WHERE { ?s ?p ?o .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER NOT EXISTS {?s rdfs:comment ?comment } }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-18"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke (hoeveel) properties hebben geen rdfs:comment*

select distinct ?s

\# (count(?s) as ?aantal)

WHERE { ?s rdfs:domain ?o

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER NOT EXISTS {?s rdfs:comment ?comment } }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-19"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke notaties staan erbij de CEO classes en properties*

select ?s ?note

WHERE { ?s skos:editorialNote ?note

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-20"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke (hoeveel) classes hebben geen *dcterms:created

select distinct ?s

\# (count(?s) as ?aantal)

WHERE { ?s ?p ?o .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER NOT EXISTS {?s dcterms:created ?created } }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-21"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke (hoeveel) properties hebben geen *dcterms:created

select distinct ?s

\# (count(?s) as ?aantal)

WHERE { ?s rdfs:domain ?o

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

FILTER NOT EXISTS {?s dcterms:created ?created } }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-22"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke object properties voldoen niet aan de voorwaarden prefix die begint met ‘heeft’ of ‘is’*

select distinct ?s

WHERE {?s a owl:ObjectProperty .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

.

FILTER (!regex(str(?s), "heeft")&& (!regex(str(?s), "is")))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-23"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke data type properties heeft een prefix die begint met ‘heeft’ of ‘is’*

select distinct ?s

WHERE {?s a owl:DatatypeProperty .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

.

FILTER (regex(str(?s), "heeft")&& (regex(str(?s), "is")))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-24"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke class wordt niet geschreven in UpperCamelCase*

select distinct ?s

WHERE {?s ?p ?o ; a owl:Class

FILTER regex(str(?s), "ceo\#\[a-z\]")

}

<span id="anchor-25"></span>

*O: welke datatype property wordt begint niet met een kleine letter*

select distinct ?s

WHERE {?s ?p ?o ; a owl:DatatypeProperty

FILTER regex(str(?s), "ceo\#\[A-Z\]")

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-26"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: welke ceo properties verwijzen naar een thesaurusterm*

select distinct ?s

WHERE {

 ?s ?p skos:Concept .

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O*<span id="anchor-27"></span>*O: *controleer of ceo:heeftGeometrie een subproperty is van gsp:hasGeometry (nog uitvoeren)

ASK { ceo:heeftGeometrie rdfs:subPropertyOf gsp:hasGeometry ; rdfs:range ceo:Geometrie }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O*<span id="anchor-28"></span>*O: *controleer of locatienaam, kaartbladcode en locatieomschrijving een string is (nog uitvoeren)

ASK { ceo:locatienaam rdfs:range xsd:string }

ASK { ceo:kaartbladcode rdfs:range xsd:string }

ASK { ceo:locatieomschrijving rdfs:range xsd:string }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-29"></span>*D: *controleer of heeftHoofdadres, heeftSitueringTegenoverAdres, heeftSitueringBijAdres als domain hebben rijksmonument (uitgevoerd)

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select ?s

where {

?s ceo:heeftHoofdadres ?o . ?s a ceo:Rijksmonument }

LIMIT 100

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select ?s

where {

?s ceo:heeftSitueringTegenoverAdres ?o . ?s a ceo:Rijksmonument }

LIMIT 100

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select ?s

where {

?s ceo:heeftSitueringBijAdres ?o . ?s a ceo:Rijksmonument }

LIMIT 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-30"></span>*D: *controleer of de instance bij heeftSitueringTegenoverAdres en heeftSitueringBijAdres hetzelfde zijn (uitgevoerd)

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select ?s

where {

?s ceo:heeftSitueringTegenoverAdres ?o ; ceo:heeftSitueringBijAdres ?o2 . FILTER (sameTerm(?o, ?o2))

 }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-31"></span>*D: *welke properties hangen aan rijksmonument 5

select \*

where {

?s ceo:rijksmonumentnummer "5"^^xsd:int ; ?p ?o

}

\#welke properties hangen aan rijksmonument 5

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns\#&gt;

PREFIX xsd: &lt;http://www.w3.org/2001/XMLSchema\#&gt;

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-32"></span>*D: *welke properties hebben ‘register’ in hun naam

PREFIX ceo: &lt;https://data.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX rdf: &lt;http://www.w3.org/1999/02/22-rdf-syntax-ns\#&gt;

select distinct ?p

where {

?s ?p ?o . FILTER regex(str(?p), "register", "i") }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*<span id="anchor-33"></span>\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O: *welke properties vallen onder het kennisregistratiepatroon

select distinct ?s ?s2

WHERE {?s ?p ?o . ?s2 ?p ?o

FILTER regex(str(?s2), "^https://linkeddata.cultureelerfgoed.nl/def/ceo\#heeft.\*Naam$")

BIND (uri(concat(str(?s), "Naam")) as ?s3)

FILTER (sameTerm(?s2, ?s3))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-34"></span>*D: *welke instances hebben meer dan een waarde (werkt niet vanwege class)

select ?s

WHERE

{

?s a owl:Class

FILTER (strstarts(str(?s),"https://linkeddata.cultureelerfgoed.nl/def/ceo\#"))

?inst a ?s

}

group by ?s HAVING (COUNT(?inst) &gt; 1)

{

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-35"></span>*D: *hoe ziet de data er in de ETL uit (niet uitvoerbaar)

select \*

WHERE {

?s ?p ?o . FILTER regex(str(?p), "vocab", "i")

} LIMIT 1000

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-36"></span>*D: *hoeveel (welke) instanties zitten er in een bepaalde class, bijvoorbeeld ceo:JuridischeStatus

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select ?class (count(?instantie) as ?aantal\_instanties)

WHERE {

?instantie a ceo:JuridischeStatus

}

GROUP BY ?class

ORDER BY desc (?aantal\_instanties)

\#werkt niet, instances en classes niet geinferreerd!

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-37"></span>*D: *aantal cultuurhistorische objecten met juridische status aanduiding

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select (count(?instantie) as ?aantal\_instanties)

WHERE {

 ?s ceo:heeftJuridischeStatus ?instantie

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*O*<span id="anchor-38"></span>*O: *controleer of ceo:locatienaam een subproperty is van locn:addressArea (Nog uitvoeren)

ASK { ceo:locatienaam rdfs:subPropertyOf locn:addressArea }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-39"></span>*D: *welke cultuurhistorische objecten horen bij een complex en vise versa (uitgevoerd)

select ?cho ?complex

WHERE {

 ?rm ceo:isOnderdeelVanComplex ?complex .

\#?complex ceo:heeftRijksmonument ?rm

}

\#LIMIT 100

\#Resultaat slechts 1?

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-40"></span>*D: *controleer of alle rijksmonumenten in de ETL zit (met Monumentenregister) (uitgevoerd)

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select (count(?rijksmonument) as ?aantal\_rijksmonumenten)

WHERE { ?rijksmonument a ceo:Rijksmonument }

*D*<span id="anchor-41"></span>*D: *controleer of locn:addressArea en ceo:locatienaam dezelfde waarde heeft (Inferred triple)

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX locn: &lt;http://www.w3.org/ns/locn\#&gt;

ASK

{

?ceo ceo:heeftLocatieAanduiding ?locatieAanduiding

 . ?locatieAanduiding locn:addressArea ?addressArea

. ?locatieAanduiding ceo:locatienaam ?locatienaam . FILTER (sameTerm(?addressArea, ?locatienaam))

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-42"></span>*D: *controleer of het property-pad naar woonplaats klopt

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX xsd: &lt;http://www.w3.org/2001/XMLSchema\#&gt;

select \*

WHERE {

 ?object ceo:heeftLocatieAanduiding/ceo:heeftLocatieAdres/ceo:woonplaatsnaam ?woomplaats .

} LIMIT 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-43"></span>*D: T*oon een bepaald pad met alle bijbehorende instanties

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \*

WHERE {

 ?s ceo:heeftGebeurtenis ?gebeurtenis . ?gebeurtenis ceo:heeftDatering ?datering . ?datering ceo:heeftTijdvak ?tijdvak . ?tijdvak ceo:startdatum ?startdatum ; ceo:einddatum ?einddatum

} LIMIT 100

*D*<span id="anchor-44"></span>*D: c*ontroleer of ceo:basisregistratie, ceo:datumInschrijvingInMonumentenregister respectievelijk een uri en een literal is

ASK {?s ceo:heeftBasisregistratie ?basisregistratie . FILTER (isURI(?basisregistratie)) }

ASK {?s ceo:datumInschrijvingInMonumentenregister ?inschrijfdatum . FILTER (isLITERAL(?inschrijfdatum)) }

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-45"></span>*D: c*ontroleer percentage rijksmonumenten behorende bij een complex

select (SUM(?aantal2 / (?aantal1 / 100)) AS ?percentage)

WHERE {

select

(count(?rm1) AS ?aantal1) (count(?rm2) AS ?aantal2)

WHERE { { ?rm1

&lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#rijksmonumentnummer&gt; ?rijksmonumentnummer }

UNION

{ ?rm2 &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#complexnummer&gt;

?complexnummer . }

}}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-46"></span>*D: c*ontroleer aantal rijksmonumenten en aantal behorende bij een complex

select

(count(?rm1) AS ?aantalRM) (count(?rm2) AS ?aantalRMbehorendBijCompex)

WHERE{ { ?rm1

&lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#rijksmonumentnummer&gt; ?rijksnummernummer }

UNION

{ ?rm2 &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#complexnummer&gt;

?complexnummer . }

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-47"></span>*D: c*ontroleer aanwezige RD-coordinaten, check in monumentenregister of dit klopt

\#ceo:asWKT-RD

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX gsp: &lt;http://www.opengis.net/ont/geosparql\#&gt;

select \*

WHERE {?ceo ceo:heeftGeometrie?geometrie . ?geometrie ceo:asWKT-RD ?RD }

LIMIT 100

\#pdok:asWKT-RD

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX gsp: &lt;http://www.opengis.net/ont/geosparql\#&gt;

PREFIX pdok: &lt;http://data.pdok.nl/def/pdok\#&gt;

select \*

WHERE {?ceo ceo:heeftGeometrie ?geometrie . ?geometrie pdok:asWKT-RD ?RD}

LIMIT 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-48"></span>*D: c*ontroleer of gemeente gekoppeld aan rijksmonument uit owms lijst komt

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select ?s

\#(count(?s) AS ?aantal)

WHERE { ?s a ceo:Rijksmonument .

 ?s ceo:heeftLocatieAanduiding/ceo:heeftLocatieAdres/ceo:heeftGemeente ?gemeente .

FILTER (strstarts(str(?gemeente),"http://standaarden.overheid.nl/owms/terms/"))

}

*D*<span id="anchor-49"></span>*D: *Een constrain is: ceo:heeftTijdvak en ceo:heeftPeriode kunnen niet gelijktijdig worden gebruikt bij dezelfde instance ceo:Datering.

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX : &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftTijdvak ?tijdvak ; ceo:heeftPeriode ?periode

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-50"></span>*D: datering*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftDatering ?datering . ?datering ?p ?o

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-51"></span>*D: ceo:heeftHoofdobject*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftHoofdobject ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-52"></span>*D: ceo:heeftGebeurtenis*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftGebeurtenis ?gebeurtenis . ?gebeurtenis ?p ?o

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-53"></span>*D: ceo:heeftGebeurtenisNaam*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftGebeurtenis/ceo:heeftGebeurtenisNaam ?gebeurtenis .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-54"></span>*D: ceo:heeftFunctie*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftFunctie ?functie . ?functie ?p ?o

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-55"></span>*D: ceo:heeftMateriaal*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftMateriaal ?materiaal . ?materiaal ?p ?o

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-56"></span>*D: ceo:archis2Waarnemingsnummer*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:archis2Waarnemingsnummer ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-57"></span>*D: ceo:archis2Monumentnummer*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:archis2Monumentnummer ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-58"></span>*D: ceo:archis2Vondstnummer*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:archis2Vondstnummer ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-59"></span>*D: ceo:archis2Complexnummer*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:archis2Complexnummer ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-60"></span>*D: ceo:heeftNaam*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftNaam ?naam . ?s a ceo:Rijksmonument . ?naam ?p ?o

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-61"></span>*D: ceo:heeftBouwkundigeKwaliteit*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftBouwkundigeKwaliteit ?kwaliteit . ?kwaliteit ?p ?o .

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-62"></span>*D: welke kennis objecten hebben geen kennisregistratienummer*

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select distinct ?s

WHERE {?s ?p ?o ; rdfs:subClassOf ceo:Kennisregistratie.

FILTER NOT EXISTS {?s ceo:kennisregistratienummer ?nummer }

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-63"></span>*D:rijksmonument prov/gemeente*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select ?s

where {

 ?s a ceo:Rijksmonument ; ceo:heeftProvincie ?provincie ; ceo:heeftGemeente ?gemeente

} \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-64"></span>*D: constrain tijdvak en periode niet tegelijk voorkomend*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

PREFIX : &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 ?s ceo:heeftTijdvak ?tijdvak ; ceo:heeftEindPeriode ?periode

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-65"></span>*D: boolean 'false'*

select \* where {

?s ?p ?o . FILTER (regex(str(?o), "false"))

} limit 100

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-66"></span>*D: property meer dan 1 domein*

*PREFIX owl: &lt;http://www.w3.org/2002/07/owl\#&gt;*

*PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;*

*select ?s (count(?domain) as ?aantal)*

*where {*

* ?s rdfs:domain ?domain*

*} group by ?s*

*having (?aantal &gt; 1)*

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-67"></span>*D: property meer dan 1 range*

PREFIX owl: &lt;http://www.w3.org/2002/07/owl\#&gt;

PREFIX rdfs: &lt;http://www.w3.org/2000/01/rdf-schema\#&gt;

select ?s (count(?range) as ?aantal)

where {

 ?s rdfs:range ?range

} group by ?s

having (?aantal &gt; 1)

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-68"></span>*D: Check geometrie niet meegenomen in LD*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select \* where {

 \#?s a ceo:Vondsten .

\#?s a ceo:Vondstlocatie .

\#?s a ceo:ArcheologischTerrein .

?s a ceo:ArcheologischComplex .

 ?s ceo:heeftGeometrie ?g

}

\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

*D*<span id="anchor-69"></span>*D: Check op aantal*

PREFIX ceo: &lt;https://linkeddata.cultureelerfgoed.nl/def/ceo\#&gt;

select (count(?s) as ?aantal)

where {

 \#klopt

\#?s a ceo:ArcheologischComplex .

\# klopt

?s a ceo:ArcheologischTerrein

}

<span id="anchor-70"></span>Issues naar aanleiding van de testresultaten

Test uitgevoerd op dataset 20181106 (versie 1.1)

1.  Als developer wil ik in de LD data aanpassen de prefix ceo, zodat deze klopt volgens de Uri-strategie. (LIN 167)
2.  **Als developer wil ik in de LD data toevoegen bij iedere datatype string de taal ’{@nl}, zodat in de toekomst het onderscheidt is te maken in taal. (zie Issue 17)**
3.  Als ontoloog wil ik in de ontologie aanpassen de schrijfwijze creatie- en mutatiedatum, zodat hier consequent op gezocht kan worden. (LIN 168)
4.  Als ontoloog wil ik in de ontologie zorgen dat de prefix van geosparql wordt meegenomen in de export, zodat het zoeken op geosparql classes en predicaten mogelijk is. (LIN 169)
5.  **Als developer wil ik in de LD data zorgen dat iedere literal is voorzien van een xsd datatype, zodat het zoeken op datatype volledige en juiste resultaten geeft.**
6.  **Als developer wil ik in de LD data verwijderen de waarde false, zodat er geen ambivalentie ontstaat over de betekenis van data.**
7.  **Als developer wil ik in de LD data aanpassen xsd:long i.p.v. xd:integer, zodat ze voldoet aan de vastgestelde datatypes in de ontologie, zie bijvoorbeeld ceo:basisregistratieRelatienummer "6012922"^^xsd:long **
8.  **Als developer wil ik in de LD data verwijderen ceo:heeftBeginPeriode en ceo:heeftEindPeriode en deze aanpassen aan de ontologie, zodat de data voldoet aan de ontologie, zie predicaten ceo:heeftTemporeleRelatie en ceo:heeftPeriode in class ceo:Datering)**
9.  Als ontoloog wil ik in de ontologie opheffen de discrepantie tussen ceo:startdatum en ceo:einddatum zijnde een dateTime in de Kimomo database i.p.v. date in de ontologie, zodat de database en LD data in sync zijn. (LIN 170)
10. Als developer wil ik in de LD data de ontbrekende triples provincie en gemeente toevoegen aan de rijksmonumenten, zodat deze gegevens uit de Kimomo database ook in de LD data zitten. (LIN-166)
11. Als ontoloog wil ik onderzoeken en aanpassen (indien fout) waarom Iedere samenhang-instantie maar 1 object heeft, zodat dit klopt met de ontologie. (LIN 171)
12. Als developer wil ik in de LD data de ontbrekende BAGRelatie triples toevoegen, zodat deze gegevens uit de Kimomo database ook in de LD data zitten.(ceo:BAGRelatienummer, ceo:verblijfsobjectIdentificatie, ceo:pandIdentificatie) (LIN 172)
13. Als developer wil ik in de LD data de ontbrekende BRKRelatie triples toevoegen, zodat deze gegevens uit de Kimomo database ook in de LD data zitten. (ceo:BRKRelatienummer, ceo:appartementAanduiding, ceo:deelperceelnummer, ceo:kadastraleGemeentecode, ceo:perceelnummer, ceo:sectie) (LIN 173)
14. Als ontoloog wil ik onderzoeken waarom er geen ceo:archis2Waarnemingsnummer data is opgenomen in de ETL data, zodat de data in de LD data volledig is. (LIN 174)
15. Als developer wil ik in de LD data aanpassen ceo:archis2Monumentnummer van skos:Concept naar xd:integer, zodat het klopt met de ontologie. (LIN 175)
16. Als ontoloog wil ik onderzoeken waarom niet alle cho’s bij ceo:heeftKennisregistratie een inverse ceo:heeftBetrekkingOp hebben, zodat de juistheid en volledigheid van de triple store klopt. (totaal bij 2241) (LIN 176)
17. **Als ontoloog wil ik onderzoeken waarom ceo:Voorganger niet in data zit, zodat de juistheid en volledigheid van de LD data klopt.**
18. **Als ontoloog wil ik onderzoeken of qua semantiek ceo:aantal en co:toelichting met meer dan 1 domein verder gespecificeerd moeten worden, zodat de helderheid en toepasbaarheid van de LD data wordt verbeterd.**
19. **Als ontoloog wil ik in de ontologie kijken naar gebruik van de importeerde standaard vocabulaires, zodat er een redundantie wordt opgenomen in de ontologie. (zie Issue 22)**
20. Als ontoloog wil ik in de ontologie verwijderen het datatype xsd:string van ceo:perceelnummer omdat deze nu twee types heeft, zodat de ontologie en LD data juist is. (LIN 177)
21. **Als ontoloog wil ik in de ontologie alle de rdfs:comment aanpassen aan het afgesproken patroon.**
22. **Als developer wil ik onderzoeken waarom er in de class ArcheologischeTerrein bij het predikaat ceo:omschrijving verkeerde data is opgenomen, zodat de kwaliteit van de data kan worden verbeterd, zie uri:&lt;**[***https://linkeddata.cultureelerfgoed.nl/cho-kennis/id/omschrijving/6055466***](https://linkeddata.cultureelerfgoed.nl/cho-kennis/id/omschrijving/6055466)**&gt;**
