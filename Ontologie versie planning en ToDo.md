<span id="anchor"></span>Ontologie ToDo, versie planning en beheer

[*https://docs.google.com/document/d/1C\_mD2-wuiICzTAkfVpf8739JOm7IZnSyaH7mPkqjirk/edit?usp=sharing*](https://docs.google.com/document/d/1C_mD2-wuiICzTAkfVpf8739JOm7IZnSyaH7mPkqjirk/edit?usp=sharing)

<span id="anchor-1"></span>Todo

Lijst checken op backlog-items.

Algemeen

1.  Hoe moet de base uri van ontologie eruit zien? Wat zijn de afwijkingen in het Excel van ‘Steven’ tov oorspronkelijk** RCE strategie/KOOP**, omgevingswet en de invulling die het kadaster daaraan geeft. Argumentatie voor verschillen documenteren. (Lieke/Patrick/Frans) **(done) **(BI 80)
2.  Op basis van visio modellering Rijksmonument aanpassen in de ceo definiëren wanneer de qualificatie ‘register’ wordt toegepast bij een property. Modellering soms niet consequent nl soms ook properties die niet rechtstreeks in de conceptuele modellen staan. Het betreft veelal monumentenregister informatie. Bijvoorbeeld het bestaan van de property registerComplexnaam heroverwegen** (Regel opgesteld, bepalen bij welke properties dat geldt, zie document)** Genereren overzicht met voorkomende properties en bepalen in welke varianten de register toevoeging wordt gebruikt.(Frans) (BI 81) (voorstel naar Joop hoe dit te modelleren, bijvoorbeeld als RO (Frans)) (Patrick18918: Oude versie TopBraid/Visio bewaren, nieuwe versie zonder register qualificatie/done)
3.  Besluit over ‘Inferred en inserted triples’ voorbereiden. (Patrick) **(going)** (nb als na reasoning ongewenste triples dan is de ontologie niet juist.) Voorlopig van afzien, na productie (na versie 1.0 Ontologie)
4.  Eigennamen lijsten bepalen die en die in PoolParty zetten c.q. Linken bv. Owms en RCE. (Patrick120918: lijsten overheid:KadastraleGemeente, overheid:Gemeente, overheid:Provincie. De vraag moet dit in PPT? Steven heeft owms uri’s voor gemeente en provincie staan in ETL, kadastrale gemeente is nu string geen owms uri) (Patrick) (voor versie 1.0 Ontologie)
5.  Bespreken nummers voor references met Gijs (Frans)(doen voor validatie)
6.  We moeten de modellering van JuridischeStatus en MonumentenAard herzien, want we doorzien nu dat hier geen instanties van gaan ontstaan het lijkt daarom consequent om toch te verwijzen naar een thesaurus-item. 4-9 besloten om range te vervangen door skos:concept en verwijderen instanties. Doorvoeren in TopBraid en ETL (Patrick120918: Steven heeft dit al verwerkt in de ETL, het daarnaast aangepast in Visio, TopBraid) (doen voor validatie) (Patrick18918: Verwerken in Visio en Top Braid. dONE
7.   Syncen gebruik functiesoort (huidige bestemming wordt huidige functie en oorspronkelijk functie) in ontologie, data en thesaurus. (doen voor validatie)
8.  Gehele ontologie doorlopen of strings geen integer moet zijn bv archis2monumentnummer. (Patrick120918: done)
9.  In de toekomst ook andere srs modelleren dan RD dit opnemen in de documentatie. (Patrick / Frans) (na versie 1.0 Ontologie)
10. Zie mail Steven over Visio tabblad C RM adresproperties (terugkoppelen, Patrick120918: Staat in lijst TODO ETL, na Steven’s vakantie bespreken) (voor versie 1.0 Ontologie)
11. In ETL heeft Steven twee properties gemodelleerd binnen Datering, heeftBeginPeriode en heeftEindPeriode deze staan niet in de ontologie. Frans/Patrick18918: Meenemen in checken volledigheid en consistentie tussen datamodel, visio en topbraid (voor versie 1.0 Ontologie)
12. Samenhang verwerken in TopBraid en door geven aan Steven, checken nog oude properties aangaande Samenhang. (Patrick) (voor versie 1.0 Ontologie)
13. Verwarring rond de term naam, zie: heeftNaam versus skos conceptnamen, zoals heeftMateriaalNaam (Bespreken met Lieke) (herzien in nieuwe versie, eventueel entiteitnaam van naam (zie heeftNaam) in het logisch model aanpassen)
14. Uri strategie betreft {reference} op welke wijze heeft Steven deze nummers (doen voor validatie)gegenereerd? Bespreken in een aparte sessie met Steven (Patrick/Frans) (doen voor validatie) (Afspraak 1 oktober)
15.  Een document maken welke data mee gaat in de ETL, accorderen door data-eigenaar. Opnemen in testplan.(Frans/Patrick)

    1.  De aanwezig of afwezigheid van data in de technisch model documenteren i.v.m. ETL (Frans) (voor versie 1.0 Ontologie)

16. Overzicht leveren van zaak properties die een reference nummer krijgen (Patrick)
17. In Visio en TopBraid modelleren nummers, zie mail Frans (Patrick) (done!)
18. Modellering label Thesaurusterm vaststellen (Frans/Patrick)
19. Verwerken opmerkingen uit Visio platen in TopBraid (Patrick) (voor versie 1.0 Ontologie)
20. Toevoegen bij alle kennis properties de relatie subProperty of heeftKennisregistratie (zie Visio plaat Kennisregistratiepatroon) (Patrick) (voor versie 1.0 Ontologie)
21. Nader beschrijven de keuze voor heeftXNaam alleen voor constructie naar range skos:Concept. (zie Visio plaat Kennisregistratiepatroon)
22. Query maken op constrain niet tegelijk voorkomen heeftTijdvak en heeftPeriode (Patrick) voor versie 1.0 Ontologie)

*Valideren en testen van de ontologie en data*

**Checken van de ontologie**

Voorbereiding:

1.  Selecteren en oplossen issues uit bovenstaande todo-lijst die noodzakelijk zijn voor validatie en testen. (27-8, gedaan)
2.  Gaandeweg richtlijn voor het voorkomen van ongewenste redundantie in de visio-visualisering opstellen. Om te voorkomen dat wijzigingen niet op alle plaatsen worden doorgevoerd.
3.  Consequente visualisering doorvoeren in visio: kleur, lettertype, uitlijning, harde return, schrijfwijze, lettergrootte, richting van de pijl, naamgeving tabbladen, etc
4.  Checken op juistheid, duidelijkheid en volledigheid van de specs: zijn alle uitgangspunten, ontwerpbeslissingen en documentatie (beschrijving) standaard waaraan de ontologie moet voldoen beschreven. RCE kwaliteitsstandaard ontologie (zie: 01\_RCE ontologieën versie 0.3 en 02\_CEO).

**Checken volledigheid en consistentie tussen datamodel, visio en topbraid: **(Issue 26)

-   Checken aanwezigheid constructen uit conceptueel datamodel als TopBraid-constructen (gedaan)
-   Checken op redundantie visio-constructen in visio (in samenhang met 2)
-   Checken aanwezigheid alle visio-constructen in TopBraid (gedaan tot tabblad geometrie)
-   Checken aanwezigheid alle TopBraid-constructen in Visio (zijn er constructen in Topbraid onterecht blijven staan?)
-   Dubbel check constructen uit logische datamodel als TopBraid-constructen

 **Het checken van de ontologie aan de hand van de uitgangspunten** (Issue 25)

-   Per uitgangspunt (handmatig) door de ontologie gaan.
-   Checken op het juiste gebruik van de documentatiestandaard.
-   Checken of er properties zijn in andere vocab’s die als domein of range een ceo:class hebben gekregen: (is ongewenste hermodellering van andere vocab).

**Checken van de data uit de ETL**

1.  Selecteren en oplossen issues uit bovenstaande todo-lijst die noodzakelijk om goede test te kunnen uitvoeren.

Checken of alle constructen aanwezig zijn in de data (niet in aantallen)

-   Wijze bepalen waarop dit (automatisch) vastgesteld kan worden.
-   Test uitvoeren

Zijn er triples in de data die we niet verwachten gezien de ontologie? (bv uit oude versie)

-   Bepalen hoe we dit te (automatisch) kunnen achterhalen.
-   Test uitvoeren

Checks

-   Is de reference uit de uri gebaseerd om het uniek cho-nummer?

**Checken van de ontologie met behulp van de data **(Zijn er inferenties die we niet verwachten.)

-   Hoe kunnen we dit (automatisch) doen?
-   Zoekvragen formuleren

**Checken bruikbaarheid van de ontologie met behulp van de interface (nieuw 4/9)**

<span id="anchor-2"></span>Versie planning

Voor iedere versie geldt dat van de constructen de:

-   relatie en betekenis tussen de concepten zoals ze voorkomen in ontologie zijn vastgelegd en beschreven m.b.v. rdfs:comment en rdfs:label. verschillende (modellerings) data zijn geannoteerd in de ontologie;
-   de constructen zijn gevisualiseerd m.b.v. VOWL;
-   de mapping met de datalaag is gedocumenteerd (in dit document).
-   het al of niet aanwezig zijn van domein en range is onderbouwd.

**Planning voor CEO**

||
||
||
||
||
||
||
||
||
||
||
||
||
||

**Planning voor ZO**

||
||
||
||
||
||
||
||
||

\*) N.B. Voorlopig geen land gemodelleerd pas in latere fase, als andere landen in data wordt gemodelleerd.

<span id="anchor-3"></span>Versiebeheer

Betreft de afspraken en vastlegging van het insync laten lopen van de inrichting ETL met de ontologie:

-   iedere wijziging in TopBraid (ontologie) krijgt versie 09xx;
-   wordt gepubliceerd op Github;
-   dit (Github) bestand wordt gebruikt om wijziging uit te voeren in de ETL;
-   bij iedere versie release van de ETL wordt een change list bijgehouden;
-   de change list wordt gepubliceerd in het document ‘Ontologie versie planning en Todo’.

ETL change list:

Versie: 12/06/2018

[*https://drive.google.com/open?id=1H-ieH5OKXy3ScfwOnlvgt3WI8FWG3xRZ*](https://drive.google.com/open?id=1H-ieH5OKXy3ScfwOnlvgt3WI8FWG3xRZ)

**DONE**

1.  Is RML/CARML (ETL) een oplossing voor RCE, want beter onderhoudbaar? Actie: opnemen op backlog (Patrick) (done)
2.  Afspraak maken en vastleggen over het beter in de pas laten lopen van de ETL met de ontwikkeling van de ontologie. (Patrick/Steven)** (done, Steven levert een change list die wordt opgenomen in Google document: Ontologie ToDo, versie planningen beheer)**
3.  Voor nu MF historie in de ontologie (zie visio) blijven we voorlopig dicht bij de data. Dit besluit opnemen in de ontwerpdocumentatie ook nog doorvoeren in TopBraid (Patrick) ** (done, zie document)**
4.  Welke modellering van enumeratie ‘relatietype’ in de CHOI is nodig: kijken naar wat voorkomt voor in de data. Ontvangen van Steven. (Patrick / Frans) Drie properties modelleren voor samenhang.relatietype conform voorkomens in de data.** (done)**
