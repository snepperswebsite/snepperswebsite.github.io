#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instructies:
  1. Maak map aan onder /assets met naam /wJAAR
  2. In die map, maak een bestand genaamd 'tekst.markdown', en schrijf daar de beschrijving.
  3. Plaats alle foto's in die map, met als bestandsnaam de bijschriften
  4. Wijzig in dit script de het JAAR en eventueel wat andere zaken in de header of zo
  5. Voer dit script uit. 
"""

###
JAAR = "2010"
THEMA = "Sneppers de Musical"
POSTNAAM = f"{JAAR}-05-10-weekend"
BRONPAD = f"assets/w{JAAR}"
UITVOERBESTAND = f"_posts/{POSTNAAM}.markdown"


###
import os
import subprocess
from PIL import Image, UnidentifiedImageError
import numpy

def getar(filepath):
    try:
        img = Image.open(filepath)
        return img.height/img.width
    except UnidentifiedImageError:
        return 100


###
header = f"""\
---
layout: photopage_thumb
title: "Ulenpas {JAAR}{(f': {THEMA}' if THEMA else '')}"
external-url:
categories: Weekenden
visible: 1
images:"""

template = f"""  - image_path: /assets/w{JAAR}/BESTANDSNAAM
    thumb_path: /assets/w{JAAR}/thumbs/BESTANDSNAAM
    title: TITEL
    description: "BESCHRIJVING"
"""
template = template[:-1]


###
with open(f"{BRONPAD}/tekst.markdown", "r") as f:
    tekstje = f.read()
bestanden = list(filter(lambda x: x not in ("thumbs", "tekst.markdown"), os.listdir(BRONPAD)))
beeldverhoudingen = [getar(f"{BRONPAD}/{bestand}") for bestand in bestanden]
inds = numpy.argsort(beeldverhoudingen)  # Rangschik afbeelding naar beeldverhouding, ziet er beter uit.

print(header, file=open(UITVOERBESTAND, "w"))
for ib in inds:
    bestand = bestanden[ib]

    bestandsnaam_geenExtensie = bestand.split(".")[:-1]
    bestandsnaam_geenExtensie = "".join(bestandsnaam_geenExtensie)
    
    beschrijving = bestandsnaam_geenExtensie.replace("_", " ").replace("-", " ")
    if beeldverhoudingen[ib] != 100:
        os.system(f"convert '{BRONPAD}/{bestand}' -resize 640x '{BRONPAD}/thumbs/{bestand}'")
    else:
        template += "\n    is_video: true"
    foto = template.replace("BESTANDSNAAM", bestand).replace("TITEL", bestandsnaam_geenExtensie).replace("BESCHRIJVING", beschrijving)
    
    print(foto, file=open(UITVOERBESTAND, "a"))    

print(f"---\n\n{tekstje}", file=open(UITVOERBESTAND, "a"))