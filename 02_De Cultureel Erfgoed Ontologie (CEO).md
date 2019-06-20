<span id="anchor"></span>De Cultureel Erfgoed Ontologie (CEO)

[*https://docs.google.com/document/d/1-AMp7VcOO6axMYTSxwU6imv42dgiX2P-\_LLaCJfnqS8/edit?usp=sharing*](https://docs.google.com/document/d/19y00TWb-fYBQrIIyanY8kBBIYRsrTOaZ4ZB8lo3N0IU/edit?usp=sharing)

<span id="anchor-1"></span>Inhoudsopgave

<span id="anchor-2"></span>

<span id="anchor-3"></span>Inleiding

In de CEO wordt brondata die overeenkomen met de logische modellen CHOI en KENNIS gemodelleerd.

(En RCE ZAAK data in de ZAAK Ontologie (ZO) en de ZAAKTYPECATALOGUS Ontologie (ZTC))

<span id="anchor-4"></span>Cultureel Erfgoed Ontologie (CEO)

Base URI: [*https://linkeddata.cultureelerfgoed.nl/def/ceo*](https://linkeddata.cultureelerfgoed.nl/def/ceo)

<span id="anchor-5"></span>Imports

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

<span id="anchor-6"></span>Afwijkingen in de ontologie t.o.v. de logische modellen

De modellering van de entiteiten Thesaurusterm en Woordsysteem wijkt af van het logische model, omdat we dicht tegen het gebruik van SKOS willen zitten. Dit geeft ook een eenvoudiger model en heeft een grotere herkenbaarheid. Door deze afwijking gaat er geen informatie uit het logische model verloren.

De volgende elementen zijn nog niet opgenomen: want (nog) geen data beschikbaar.

**CHOI**

De CHO.GBKN/GBT en CHO.BRT

CHO.identificatieIMKICH

De CHO.Gezicht en CHO.Werelderfgoed

**KENNIS**

<span id="anchor-7"></span>Afwijkingen in de ontologie t.o.v. de technische implementatie

In de Kimomo database zijn niet alle tabellen voorzien van een attribuut voor nummers. In de ontologie zijn deze wel opgenomen. Voor de vulling wordt dan gebruik gemaakt van de primary key van de betreffende tabel.

<span id="anchor-8"></span>Ontwerpbeslissingen (CEO)

1.  We gebruiken voor geometrie een eigen ceo:class daarom gebruiken we ook een eigen ceo-property om aan te geven dat de geometrie volgens het RD-stelsel is, indien gewenst kunnen we op deze wijze ook andere stelsels modelleren. ([*testquery*](https://docs.google.com/document/d/1n9xO50E7O2W0wviyLbIcbo4yF2ZNeAkRh_G0zeqaIW8/edit#bookmark=id.fc3xdarxvkpn))
2.  We modelleren locatienaam, kaartbladcode, locatieOmschrijving als een “string” ([*testquery*](https://docs.google.com/document/d/1n9xO50E7O2W0wviyLbIcbo4yF2ZNeAkRh_G0zeqaIW8/edit#bookmark=id.fc3xdarxvkpn))en niet als class, omdat er sprake is van maar één attribuut van het soort “string” in de betreffende entiteit.
3.  We modelleren voorlopig geen land, maar doen dit pas als andere landen in data gaan voorkomen.
4.  Binnen de class ceo:Datering geldt de constrain: ceo:heeftTijdvak en ceo:heeftPeriode kunnen niet gelijktijdig worden gebruikt bij dezelfde instance uit ceo:Datering.
5.  In toekomstige situatie vervangen we instance Actor en Rol door een SKOS-concept.

Als er in de data geen Actor of Rol is voorkomt dan wordt als waarde voor de String “Onbekend” gebruikt. Property wordt dan ceo:heeftActor, ceo:heeftRol.

1.  Op basis van de lengte hebben we de de naam van de property tussen classes CEO en BasisregistratieRelatie ingekort (basisregistratieobjectrelatie).
2.  De vier properties: heeftHoofdadres, heeftSitueringTegenoverAdres, heeftSitueringBijAdres, heeftRegisteradres zijn alleen van toepassing op de class Rijksmonument.([*testquery*](https://docs.google.com/document/d/1n9xO50E7O2W0wviyLbIcbo4yF2ZNeAkRh_G0zeqaIW8/edit#bookmark=id.fc3xdarxvkpn))
3.  De property heeftKennisregistratie kan gebruikt worden om alle kennisregistraties bij een CHO in een query te aggregeren. ([*testquery*](https://docs.google.com/document/d/1n9xO50E7O2W0wviyLbIcbo4yF2ZNeAkRh_G0zeqaIW8/edit#bookmark=id.fc3xdarxvkpn))
4.  We modelleren CHO niet als geo:Feature omdat niet ieder Cultuurhistorisch object een geometrie heeft.
5.  We gebruiken de pdok property om aan te geven dat geometrie volgens het RD-stelsel is, indien gewenst kunnen we op deze wijze ook andere stelsels modelleren.
6.  Kennisregistratiepatroon: Om aan een CHO een subclass van de class Kennisregistratie te koppelen gebruiken we een property met als naam heeftX, waarbij X vervangen door de naam van de subclass bijvoorbeeld heeftFunctie. Om nu de bijvoorbeeld de “naam” van deze functie uit de thesaurus te halen gebruiken we het patroon heeftXnaam, bv heeft FunctieNaam.([*testquery*](https://docs.google.com/document/d/1n9xO50E7O2W0wviyLbIcbo4yF2ZNeAkRh_G0zeqaIW8/edit#bookmark=id.fc3xdarxvkpn))
7.  In verband met de lengte is de naam van de property ingekort tot ceo:heeftBasisregistratieRelatie in plaats van ceo:heeftBasisregistratieObjectRelatie.
8.  De property ceo:naam zou volgens het consequent volgen van de impliciete conventie ceo:cultuurhistorischobjectNaam moeten luiden.
9.  De entiteit ‘woordsysteem’ uit het kennismodel wordt niet opgenomen in de ceo omdat:

<!-- -->

1.  het technische model afwijkt van het logisch model;

2.  de informatie uit het logische model ook te herleiden is uit en met behulp van de URI van de term.

Afwezigheid van data in de datalaag

Sommige attributen hebben geen data in het technische model. Hiervoor kunnen twee oorzaken worden aangewezen:

1. Er is geanticipeerd op gebruik dat nog niet is gerealiseerd.

2. De data is in de migratie van ODB/ARCHIS2 naar CHO, KENNIS en ZAAK is (nog) niet (goed) overgekomen.

In de ETL is hiervoor dan ook geen (nooit?) een script geschreven.

N.B. Het risico is nu dat verbetering in de datalaag niet automatisch worden doorgevoerd naar de LD-voorziening.

De volgende drie properties zijn *alleen *van toepassing op de class Rijksmonument, en lopen naar LocatieAanduiding, zodat hier ook de locatieaanduiding properties gebruikt kunnen worden.

-   ceo:heeftHoofdadres
-   ceo:heeftSitueringTegenoverAdres
-   ceo:heeftSitueringBijAdres

De properties:

-   locatienaam,
-   kaartbladcode,
-   locatieOmschrijving

zijn gemodelleerd als string en niet als class omdat er sprake is van maar één attribuut van het soort string in de betreffende entiteit.

<span id="anchor-9"></span>CEO classes en properties

[*https://docs.google.com/spreadsheets/d/e/2PACX-1vQkwbsC\_MsF1v--m5r7J8vEnYWPHuCQrjrzKbYiLm\_1Opi1EuLqBsPvs-LaTjnFdCiGdKgbQVxEfF6k/pubhtml*](https://docs.google.com/spreadsheets/d/e/2PACX-1vQkwbsC_MsF1v--m5r7J8vEnYWPHuCQrjrzKbYiLm_1Opi1EuLqBsPvs-LaTjnFdCiGdKgbQVxEfF6k/pubhtml)
