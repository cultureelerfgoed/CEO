<span id="anchor"></span>Rest materiaal ontologie modelleering

[*https://docs.google.com/document/d/1WBiK0ZJD0NdGi8z5sJwc8SzuVUfmTYJMf0uj3DZdo7E/edit?usp=sharing*](https://docs.google.com/document/d/1WBiK0ZJD0NdGi8z5sJwc8SzuVUfmTYJMf0uj3DZdo7E/edit?usp=sharing)

<span id="anchor-1"></span>Vraagstukken, referentiemateriaal, voorbeelden, oude modelleringen, etc.

<span id="anchor-2"></span>

<span id="anchor-3"></span>Vraagstukken

**Gebruik van qualificatie ‘register’ in een property**

Huidige (4-9) voorkomens:

Objectproperties (let op: camelCase)

-   -   heeftRegisterAdres

    -   heeftRegisterNaam

    -   heeftRegisterOmschrijving

    -   heeftRegisterPerceel

Dataproperties

-   registerComplexNaam

-   registerNaam

-   registerDatum

Binnen een property wordt de qualificatie ‘register’ toegepast, wanneer de property voldoet aan twee voorwaarden:

- is aangemerkt als registergegeven zie: Memo ‘Registergegevens onder de

 Erfgoedwet’, d.d. 20 juli 2017 ; (filenaam; memo borging registerfunctie v01a.docx) n

- er sprake is van gelijksoortige data, die niet onder het register valt. Daarmee wordt onderscheid gemaakt tussen register en niet-register data.

Als aan deze voorwaarden wordt voldaan, worden er twee properties aangemaakt de ene met de voorloper

‘register’ en de andere zonder.

-   owl:objectProperty: ceo:heeftRegisterX en ceo:heeftX

> Voorbeeld: ceo:heeftRegisterPerceel en ceo:heeftPerceel

-   owl:datatypeProperty: ceo:registerX en ceo:x

> Voorbeeld: ceo:registerNaam en ceo:naam

**Hoe om te gaan met redundante documentdata in ZAAK?**

Lijkt voorlopig geen probleem omdat we nog geen ontologie voor REC gaan opstellen. Tot Nader order kunnen we de document info uit he zaakmodel halen.

**Owl full/DL/Lite of rdfs+ ?**

Ziie:[*https://ragrawal.wordpress.com/2007/02/20/difference-between-owl-lite-dl-and-full/*](https://ragrawal.wordpress.com/2007/02/20/difference-between-owl-lite-dl-and-full/)

**Moeten we restricties modelleren? **

Denk aan bijvoorbeeld heeftMonumentAard. Zo ja, dan :Gebruiken we shacl en/of OWL constrains zoals bijvoorbeeld: AllValuesOff oid?

**Hoe verhoud SKOS:Concept modellering zich tot OWL:class modellering.**

Onderdeel hiervan is bijvoorbeeld de koppeling naar wetteksten

**Hergebruik van een waarde als instance in meerdere lijstjes**

Denk bijvoorbeeld aan lijstje als onvolledig, compleet etc. ( nb er was een concreet voorbeeld.)

**Het gebruik van vann**

De vann CV lijkt niet te werken.

**Modellering**

Modellering tussen van de relaties tussen ontologie, datamodel en thesaurusconcepten. (en wat er in de erfgoedwet staat)

**Hergebruik van een waarde**

Hergebruik van een waarde, waarbij er sprake is van een verschil in betekenis, als instance in meerdere lijstjes

-    Bv onbekend, niet van toepassing, ja/nee, onbepaald

 Twee mogelijkheden:

-   1 onbekend of
-   Voor ieder lijsje een onbekend. Bv “juridischStatusTypeOnbekend”.

**Modelleren volgens volledige en/of beperkte semantiek?**

*Casus*

Bij een rijksmonument is in de brondata vaak de/een architect bekend. De impliciete semantiek hiervan is: “dat op een bepaald moment (datering) er een gebeurtenis (event) van een bepaald type bv ‘ontwerp’ heeft plaatsgevonden, waarbij een persoon (actor) als architect (rol) heeft gefunctioneerd”.

Dit is in het conceptuele model KENNIS expliciet gemodelleerd.

Een bijbehorende ontologie zou er zo uit kunnen zien.

Het is ook mogelijk de architect van een rijksmonument - zei het met verlies van betekenis - als volgt weer te geven:

De volledige ontologie heeft de volgende voordelen:

-   Dichter bij de bron modellen
-   Vergelijkbare constructen elders vermoedelijk onontkoombaar, daarom is dit consequent
-   Meer betekenis en informatie
-   Terug naar beperkte modellering is relatief eenvoudig
-   Complexer query’s zijn mogelijk

En de volgende nadelen:

-   Minder direct leesbaar (voor wie?)
-   Complexer query’s zijn nodig

De beperkte ontologie heeft de volgende voordelen:

-   Eenvoud

En de volgende nadelen:

Vragen

Kunnen beide manieren naast elkaar bestaan?

Is een groeipad denkbaar zonder belemmeringen voor volledige semantiek?

Door bijvoorbeeld geen “Range” te geven aan dataproperties?

Of is het slimmer om een aparte ontologie te maken: de simple ceo -&gt; sceo?

N.b. In de eerste versie van de CEO is uitgegaan van ‘beperkte semantiek’, omdat dit aansloot bij het doel van de kerker-POC.

Analyse teksten en (tijdelijke) voorbeelden

Vergelijking t.b.v. het gebruik van SKOS en/of VANN voor het annoteren van ontologieën.

Kiezen welke we gaan gebruiken

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
||
||
||

<span id="anchor-4"></span>**Plan van aanpak**

1.  Bestaande modellering controleren, documenteren en omschrijven en kijken naar aanwezige tweetaligheid

    1.  ~~Hernoemen na ar versie 0.3 cleanversie~~

    2.  ~~In de volgende volgorde doorlopen van de CV’s~~: ~~CEO~~, ~~LOCN, BRK~~, ~~OVERHEID~~, ~~SKOS ~~

    3.  ~~rdfs:comments bij CEO bestaandeconstructen uit conceptuele datamodel halen en in sync brengen met thesaurus.~~

    4.  ~~Nalopen CEO op ‘oude’ constructen (Eerst de Classes doorlopen, daarna Properties)~~

    5.  ~~Nog weghalen aanwijzingsreden uit CEO~~

2. ~~File hernoemen in ME edition~~

~~Weggelaten property isJuridischeStatusTypeVan~~

1.  LOCN, SKOS
2.  Relatie en betekenis tussen de concepten zoals ze voorkomen in ontologie (comment/label) architectuur, thesaurus en de (erfgoed)wet is vastgelegd en beschreven.
3.  Volgende vraagstukken behandelen (volgorde nog nader bepalen)
4.  Bottom-up volledig maken.
5.  Tweetalig maken.

<span id="anchor-5"></span>LOG

**14042017**

-   Creatie versie02

    -   Verwijderd

-   CEO:Denominatie en ceo:heeftDenominatie, moet onderdeel zijn van KPO!
-   RDFS:heeftType, want dubbel en onjuiste prefix.

    -   

        -   ceo:heeftLocatieOpmerking

**21042017**

-   -   Opgenomen

        -   ceo:heeftSitueringBij
        -   ceo:heeftSitueringTegenover
        -   ceo:plaatsCode
        -   Import BRK model als file.
        -   cho:Complex
        -   cho:heeftComplexnummer

**26042017**

-   -   Opgenomen

        -   ceo:heeftRijksmonument en de inverse behoortTotComplex

**14112017**

-   -   Algemeen

        -   Start door modellering voor Kadaster PoC

**28112017**

-   -   Opgenomen

-   -   Verwijderd

        -   ceo:Aanwijzingsreden en ceo:heeftAanwijzingsreden en ceo:heeftRedengevendeOmschrijving: ceo:heeftRegisterInschrijfdatum want was specifiek opgenomen voor Kerken PoC.
        -   De oude ceo:aardMonument verwijdert ivm ook bestaan ceo:heeftMonumentAard.
    -   Wijzigingen

        -   Hernoemen ceo:Status en ceo:heeftStatus naar ceo:JuridischeStatus ceo:heeftJuridischeStatus

**12122017**

-   -   Opgenomen

        -   Import DC en VANN
    -   Verwijderd

    -   Wijzigingen

**20122017**

-   -   Opgenomen nieuwe versie

        -   DC, DCTERMS en VANN
    -   Wijziging versie benaming van 03 naar 01

**01092018**

-   -   Opgenomen

        -   Prefix voor locn
    -   Verwijderd

    -   Wijzigingen

<span id="anchor-6"></span>

<span id="anchor-7"></span>

<span id="anchor-8"></span>Provenance

[*https://docs.google.com/presentation/d/13fqPcupeOq11N7APeCLA\_HzkEUZUmtNToyy9LkLSpFU/edit\#slide=id.g19c6e93abb\_0\_48*](https://docs.google.com/presentation/d/13fqPcupeOq11N7APeCLA_HzkEUZUmtNToyy9LkLSpFU/edit#slide=id.g19c6e93abb_0_48)

||
||
||
||
||

**Oplossing 1 (zonder provenance)**

123 naam St. Jan

123 naam Sint Jan

**Oplossing 2 (provenance in property) Voorlopig: 27-03-2017**

123 naam St. Jan -&gt; mrs modellering

123 AdminBnaam Sint Jan -&gt; PoC modellering temp

AdminBnaam subPropertyOf naam -&gt; PoC modellering temp

**Oplossing 3 (Graph)**

Graph Admin A

123 naam St. Jan

Graph Admin B

123 naam Sint Jan

Mergen naar een nieuwe Graph Admin AB

**Oplossing 4 (m.b.v. prov ontologie)**

123 naam St. Jan prov Admin A

St. Jan hasName St. Jan

123 naam Sint Jan prov Admin B

 Sint Jan hasName Sint Jan

**Oplossing 5**

123adminA naam St. Jan

123adminA dataset AdminA

123adminA sameAs 123

123 naam Sint Jan

123 dataset AdminB

<span id="anchor-9"></span>

<span id="anchor-10"></span>Samenhang CHO

<span id="anchor-11"></span>

<span id="anchor-12"></span>
