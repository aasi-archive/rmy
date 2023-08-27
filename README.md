# The Ramayana (Online)

The modernization and digitization of the Ramayana, along with the English translation. This repository hosts the Python scripts used to create HTML pages along with the search indexer deployed on the aasi-flask-server. We use Jinja2 for templating, json, and re for most of the parsing of the source text. The website uses Bootstrap, Font-Awesome, and jQuery. 

## Building

Simply run:

```bash
python rmy2html.py
python rmy2html-skt.py
```

This should generate the HTMLs for both the English and Sanskrit versions in `./build/`. The build directory can then be hosted anywhere.

