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

from PIL import Image, UnidentifiedImageError
import numpy
from pathlib import Path
from subprocess import Popen

### invullen
JAAR = "2024"
THEMA = ""

### derivaten
DEST = Path("_posts")
SRC = Path("assets")
POSTNAAM = f"{JAAR}-05-10-weekend"
BRONPAD = SRC / f"w{JAAR}"
UITVOERBESTAND = (DEST / POSTNAAM).with_suffix(".markdown")
header = f"""\
---
layout: multiphotopage_thumb
title: "Ulenpas {JAAR}{(f': {THEMA}' if THEMA else '')}"
external-url:
categories: Weekenden
visible: 1
segments: SEG_NAMES
content_file: CONTENT_FILE
images:"""


def img_block(filepath: Path, **kwargs) -> bytearray:
    """
    Create element for in the images array in the front matter

    Parameters
    ----------
    filepath
        Path to the image file to be added

    Returns
    -------
        Multiline element to be added to the YAML array
    """
    kwargs["image_path"] = filepath
    kwargs["thumb_path"] = Path(*filepath.parts[:-1]) / "thumbs" / filepath.name
    kwargs["title"] = filepath.stem
    kwargs["description"] = ("" if any(filepath.stem.startswith(x) for x in ("WhatsApp Image", "NOCAP", "DSC", "IMG")) else filepath.stem)
    if getar(filepath) != 100:
        Popen(["convert", kwargs['image_path'], "-resize", "640x", kwargs['thumb_path']])
    else:
        kwargs["is_video"] = "true"

    s = ""
    for key, value in kwargs.items():
        sll = "/" if isinstance(value, Path) else ""
        s += f"\n    {key}: \"{sll}{value}\""

    s =  "  - " + s.lstrip() + "\n"
    return s.encode("UTF-8")


def getar(filepath: Path) -> float:
    try:
        img = Image.open(filepath)
        return img.height/img.width
    except UnidentifiedImageError:
        return 100.


# Scan input markdown file for image and text segments
with open(BRONPAD / "tekst.markdown", "r") as f:
    tekstje = f.read()
segments = []
in_imgs = False
text = ""
imgs = []
all_mentioned_imgs = []
for line in tekstje.splitlines():
    if line.startswith("![](") and line.endswith(")"):
        if not in_imgs:
            in_imgs = True
        img_file =  Path(line.split("![](")[1][1:-1].replace("%20", " "))
        imgs.append(img_file)
        all_mentioned_imgs.append(img_file)
    else:
        if in_imgs:
            segments.append({"text": text, "imgs": imgs})
            text = ""
            imgs = []
            in_imgs = False
        text += f"{line}\n"
segments.append({"text": text, "imgs": imgs})

# Gather and sort remaining images, to be placed at the bottom of the page
bestanden = list(filter(lambda x: x not in all_mentioned_imgs and x.name not in ("thumbs", "tekst.markdown"), BRONPAD.glob("*")))
beeldverhoudingen = [getar(bestand) for bestand in bestanden]
inds = numpy.argsort(beeldverhoudingen)  # Rangschik afbeelding naar beeldverhouding, ziet er beter uit.
bestanden = [bestanden[i] for i in inds]
segments.append({"text": "", "imgs": bestanden})


for seg in segments:
    print("SEGMENT SEGMENT")
    print(seg["text"])
    print(seg["imgs"])
    print()

# Add text segments
st, et = "{%", "%}"
cf = UITVOERBESTAND.with_stem("_" + UITVOERBESTAND.stem + "-content")
header = header.replace("CONTENT_FILE", cf.name)
with open(cf, "wb") as fuit:
    for i, seg in enumerate(segments):
        fuit.write(f'{st} if include.content == "{i}" {et}\n<wbr>\n\n'.encode("UTF-8"))  # HACK: <wbr> because if a heading is not preceded by something (in the text fragment included via liquid), a large vspace is present under the heading.
        fuit.write(seg["text"].encode("UTF-8"))
        fuit.write(f"\n{st} endif {et}\n".encode("UTF-8"))

# Front matter (YAML) incl. images
with open(UITVOERBESTAND, "wb") as fuit:
    header = header.replace("SEG_NAMES", str([str(i) for i in range(len(segments)-1)] + ["unsorted"]))
    fuit.write((header + "\n").encode("UTF-8"))
    for i, seg in enumerate(segments):
        for bestand in seg["imgs"]:
            fuit.write(img_block(bestand, segment=("unsorted" if i == len(segments)-1 else i)))
    fuit.write("---\n\n".encode("UTF-8"))

