# PAM-DB-Crawler

## Intro

This repository contains a simple, stupid meta-programming based crawler-genrator for the _API Pflanzenschutz DB_ provided at: https://psm-api.bvl.bund.de/

> Das Bundesamt für Verbraucherschutz und Lebensmittelsicherheit stellt monatlich die in Deutschland geltenden Pflanzenschutzmittelzulassungen in einer Datenbank (PSM-DB) bereit. Dies ist die Dokumentation dieser PSM-DB über das Tool Swagger im OpenAPI-Standard. Die PSM-DB stellt dieselben Daten wie der über das BVL zu beziehende monatliche Access-Dumb [sic] in selber Aktualität bereit.

## Working with this script.

If you want to run this script:  
```python
python main.py
```
This must be run from the directory the `main.py` script is in! The script will generate the models and store them in the `models` package. A SQLite DB will be created.

If you want to use additional API endpoints and models, have a look at `definitions.py`. In here, basic information is provided which is used to generate crawler for these.

If you want to extend the generated model-crawler, have a look at `generator.py`. In this script the information of API endpoints and models is used to generate python code which is able to crawl them.

## Footnotes: 
Meta-Programming 101 - This project is to 80% a python code generator. The generated code is a stupid, write-only DB model which is able to pull data from an endpoint provided.

Python-specific information: Well.. actually there are something called "Metaclasses" in Python which could be used instead of the direct code-generation I have been using here. Would be nice to translate this code to a Metaclass based generator in the near future.
