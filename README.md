# Publieke blogfeed van Orly Vlot

[![Dagelijkse verversing](https://github.com/JourneyConsultancy/post-feed/actions/workflows/update.yml/badge.svg)](https://github.com/JourneyConsultancy/post-feed/actions/workflows/update.yml)

Deze feed levert de openbare blog-URL’s van [orlyvlot.nl](https://orlyvlot.nl/), bijvoorbeeld voor het controleren van interne links.

**Feed:** [posts.json](https://journeyconsultancy.github.io/post-feed/posts.json)

```json
{"urls": ["https://orlyvlot.nl/voorbeeld/"]}
```

De bestaande workflow leest de openbare WordPress API dagelijks rond **02:00 UTC**. Hij maakt alleen een commit als de URL-lijst verandert. Een handmatige uitvoering kan via Actions. De statusbadge toont het resultaat van de workflow, geen onafhankelijk bewijs dat alle bloginhoud actueel is.

De actuele GitHub Pages-host is `journeyconsultancy.github.io`. Gebruik die host ook in bestaande API-clients; de oude host van het persoonlijke account levert voor deze feed geen werkende redirect.

Onderdeel van [Journey Consultancy](https://journeyconsultancy.nl/).
