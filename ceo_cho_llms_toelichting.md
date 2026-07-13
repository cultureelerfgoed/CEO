# AI-ready erfgoeddata: toelichting in gewone taal

*Leeswijzer bij `ceo_cho_llms.txt` en de bijbehorende bestanden en hulpmiddelen.
Bedoeld voor collega's zonder linked-data-achtergrond.*

## Waar gaat dit over?

De RCE publiceert erfgoedgegevens als linked open data: informatie over
rijksmonumenten, beschermde gezichten, werelderfgoed en archeologie, afkomstig
uit Archis en het Monumentenregister. Die gegevens zijn technisch op orde,
maar AI-systemen (zoals taalmodellen en chatassistenten) hebben extra hulp
nodig om ze goed te kunnen gebruiken. Zonder die hulp stelt een AI verkeerde
vragen aan de data, of trekt het conclusies uit onvolledige informatie.

"AI-ready maken" betekent hier: het bestaande beter uitlegbaar en bevraagbaar
maken voor AI. Er wordt niets aan de gegevens zelf veranderd of toegevoegd —
de bronnen blijven leidend.

## Wat een AI moet weten, in vier vragen

Alles wat gemaakt is beantwoordt een van deze vier vragen die een AI stelt:

1. **Hoe zit de data in elkaar?** Welke soorten dingen bestaan er
   (rijksmonumenten, complexen, vondstlocaties) en hoe hangen ze samen?
2. **Wat zit er feitelijk in?** Het model beschrijft wat er *kan* bestaan;
   een AI moet ook weten wat er *echt* in de database zit, en hoeveel.
3. **Hoe stel je er goede vragen aan?** Voorbeelden van vragen in gewone
   taal met de bijbehorende correcte opvraging.
4. **Waar kan ik het zelf proberen?** Een manier voor de AI om live in de
   actuele data te kijken in plaats van op beschrijvingen te vertrouwen.

Het bestand `ceo_cho_llms.txt` is de wegwijzer die een AI langs deze vier
vragen leidt. De naam volgt een internationale afspraak (vergelijkbaar met
hoe websites een vast bestand hebben voor zoekmachines), zodat AI-hulpmiddelen
het vanzelf vinden.

## De onderdelen: vastgelegd versus actueel

Het belangrijkste onderscheid om te begrijpen is dat tussen **vastgelegde**
en **actuele (dynamische)** onderdelen.

### Vastgelegd (eenmalig gemaakt, wijzigt met het model mee)

**Het datamodel met uitleg en verwijzingen** (`CEO_RCE.ttl`). De formele
beschrijving van alle begrippen, in het Nederlands en Engels toegelicht.
Nieuw toegevoegd zijn verwijzingen naar internationale standaarden die
AI-systemen al kennen uit hun training — zo begrijpt een AI bijvoorbeeld
dat een "rijksmonument" verwant is aan wat internationaal een historisch
gebouw of landmark heet.

**Voorbeeldvragen** (`ceo-queryvoorbeelden.ttl`). Achttien vragen in gewone
taal ("welke monumenten waren oorspronkelijk een kerk?") met de technisch
correcte opvraging erbij, verdeeld over alle tien de hoofdsoorten objecten.
AI-systemen gebruiken zulke paren als voorbeeldmateriaal: zien hoe het hoort,
en dat patroon toepassen op nieuwe vragen.

### Actueel/dynamisch (haalt de situatie van dít moment op)

Dit is het onderscheidende deel van de aanpak: de AI hoeft niet te vertrouwen
op beschrijvingen die verouderd kunnen zijn, maar kan de werkelijke, actuele
situatie raadplegen. De databank wordt dagelijks ververst; deze hulpmiddelen
verversen mee.

**De live-verbinding voor AI** (interne MCP-server). Een koppelstuk volgens de
MCP-standaard — de opkomende industriestandaard waarmee AI-assistenten
veilig met databronnen praten. Hiermee kan een AI-assistent, met
toestemming van de gebruiker, rechtstreeks in de actuele erfgoeddata
kijken. Het koppelstuk kan uitsluitend *lezen* (wijzigen is technisch
geblokkeerd) en biedt zeven functies, waaronder:

- *Actuele aantallen opvragen* — hoeveel rijksmonumenten zijn er nú, hoe
  goed is een gegeven ingevuld? De AI baseert zich op de stand van vandaag.
- *De data verkennen* — de AI kan zelf ontdekken hoe gegevens samenhangen,
  vooruit én achteruit redenerend, ook voor vragen die niemand had voorzien.
- *Begrippen opzoeken in de terminologiebronnen* — zoekt een gebruiker op
  "kerk", dan raadpleegt de AI live de RCE-begrippenlijsten (het
  referentienetwerk en de Cultuurhistorische Thesaurus) en vindt zo ook
  verwante termen als "kapel". Daardoor zoekt de AI met de vaktermen van
  de RCE in plaats van met losse trefwoorden.
- *Vrij vragen stellen* — voor alles wat de andere functies niet dekken.

Dit koppelstuk kan lokaal draaien (op één werkplek) of centraal gehost
worden, zodat álle medewerkers en AI-toepassingen er gebruik van maken. Het
wordt om veiligheidsredenen apart en niet-openbaar beheerd, los van de
openbare beschrijvingen van de data.

**Twee "verversbare foto's" van de databank.** Sommige overzichten zijn te
zwaar om bij elke vraag live te berekenen. Daarvoor zijn twee hulpprogramma's
die op elk gewenst moment een actueel overzicht genereren:

- *De inhoudsopgave* (`genereer_void.py` maakt `ceo-void.ttl`): telt wat er
  feitelijk in de databank zit — hoeveel objecten van elke soort, hoe vaak
  elk gegeven voorkomt, en hoeveel verwijzingen er zijn naar externe bronnen
  zoals het Kadaster (BAG/BRK), de gemeente-registers en de begrippenlijsten.
  Zo weet een AI ook wat er *niet* in zit, en trekt het geen stellige
  conclusies uit ontbrekende gegevens.
- *De padenkaart* (`genereer_padenkaart.py` maakt `ceo-padenkaart.ttl`):
  brengt in kaart welke routes door de data daadwerkelijk bestaan en hoe
  goed ze gevuld zijn, verkend vanaf de tien hoofdsoorten objecten.

Deze twee zijn "dynamisch op afroep": het genereren kan handmatig, maar ook
automatisch worden ingepland (bijvoorbeeld wekelijks), zodat de gepubliceerde
overzichten altijd de actuele databank weerspiegelen.

## Wat dit nadrukkelijk níet is

Er wordt **niets toegevoegd aan of veranderd in de gegevens zelf**. Geen
verrijking, geen correcties, geen nieuwe feiten. De bronnen (Archis,
Monumentenregister, Werelderfgoed, Gezichten) blijven de enige plek waar
inhoudelijke wijzigingen thuishoren. Alles hier maakt het bestaande alleen
beter vindbaar, begrijpelijk en bevraagbaar voor AI — en via AI voor mensen.

## Beheer in het kort

| Onderdeel | Type | Bijwerken wanneer |
|---|---|---|
| Datamodel + uitleg | vastgelegd | bij modelwijzigingen (versiebeheer) |
| Voorbeeldvragen | vastgelegd | bij modelwijzigingen of nieuwe behoeften |
| Wegwijzer (`ceo_cho_llms.txt`) | vastgelegd | als onderdelen wijzigen |
| Inhoudsopgave (VoID) | dynamisch op afroep | periodiek, bij voorkeur automatisch |
| Padenkaart | dynamisch op afroep | periodiek, bij voorkeur automatisch |
| Live-verbinding (MCP) | dynamisch, continu | software-onderhoud; data altijd actueel |

## Vragen?

Neem contact op met het team Thesauri & Linked data (afdeling IV, cluster
Erfgoeddata & Datamanagement) via thesauri@cultureelerfgoed.nl.
