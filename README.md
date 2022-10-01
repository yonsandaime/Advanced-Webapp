# Voorbeeld Flask gebaseerde webapplicatie

## Downloaden / Updaten van dit project:
Git project eerste keer downloaden (via een terminal): 
```
git clone https://gitlab.com/steffen.thielemans/flask-webapp-example.git
```

Nadien updaten via ```git pull``` binnen dit git project (=deze map)

## Installeren van de Python dependencies:

```
pip install -r requirements.txt
```

## Uitvoeren van de Flask webapplicatie:

```
python webapp.py
```

De Flask webserver wordt opgestart op http://localhost:8080


# CoAP communicatie met de K4.04 telecomlab lampen:

[Constrained Application Protocol](https://en.wikipedia.org/wiki/Constrained_Application_Protocol) (CoAP) is een vaakgebruikt protocol voor communicatie binnen Internet of Things (IoT) systemen. Het is gelijkaardig aan Hypertext Transfer Protocol (HTTP) maar heeft minder overhead en werkt over UDP in plaats van UDP.

We maken gebruik van de ```aiocoap``` Python bibliotheek om via het CoAP protocol data uit te wisselen met de lampen. [Documentatie van deze bibliotheek is hier beschikbaar](https://aiocoap.readthedocs.io/en/latest/index.html).

De ```aiocoap``` bibliotheek is geimplementeerd aan de hand van asynchrone I/O operaties door middel van Python's ```asyncio``` bibliotheek. CoAP verzoeken maken daarmee gebruik van async/await. Meer informatie rond asyncio en de async/await syntax is te vinden op [Python's officiele documentatie](https://docs.python.org/3/library/asyncio.html). 

## IPv6 connectiviteit:

De lampen zelf beschikken elk over een ARM-gebaseerde IoT microprocessor met IEEE 802.15.4 2.4 GHz 'ZigBee' radio. Door gebruik te maken van het [Contiki-NG](https://github.com/contiki-ng/contiki-ng) besturingsysteem wordt [IPv6](https://nl.wikipedia.org/wiki/Internet_Protocol_versie_6) connectiviteit mogelijk. Deze connectiviteit is onderling tussen de toestellen binnen het IPv6 IoT netwerk, maar ook met toestellen buiten het IoT netwerk zoals computers en een eventuele webserver.

De huidige VUB computernetwerken bieden nog geen IPv6 aan, al wordt er wel aan gewerkt. In tussentijd moet een [IP tunnel](https://en.wikipedia.org/wiki/IP_tunnel) opgezet worden waarmee IPv6 connectiviteit via encapsulatie bovenop de bestaande klassieke IPv4 netwerken mogelijk wordt. Meer info in het hoe & wat door de assistent tijdens de WPOs.