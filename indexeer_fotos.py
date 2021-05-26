#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 13:38:42 2021

@author: ostheer
"""

import os

#%%
bron_pad = "/home/ostheer/Documents/git/snepperswebsite.github.io/assets/w2009"
jaar = "2009"
output_bestand = "output.txt"

#%%
template = """  - image_path: /assets/wJAAR/BESTANDSNAAM
    title: TITEL
    description: "BESCHRIJVING"
"""
template = template[:-1]

bestanden = os.listdir(bron_pad)

print("images:\n", file=open(output_bestand, "w"))

i = 1
for bestand in bestanden:
    bestandsnaam_geenExtensie = bestand.split(".")[:-1]
    bestandsnaam_geenExtensie = "".join(bestandsnaam_geenExtensie)
    
    beschrijving = bestandsnaam_geenExtensie.replace("_", " ").replace("-", " ")
    beschrijving = beschrijving.lower().capitalize()# + "."
    
    foto = template.replace("JAAR", jaar).replace("BESTANDSNAAM", bestand).replace("TITEL", bestandsnaam_geenExtensie).replace("BESCHRIJVING", beschrijving)
    
    print(foto, file=open(output_bestand, "a"))
    
    
    if i == 3:
        print("\n", file=open(output_bestand, "a"))
        i = 0
    
    i += 1