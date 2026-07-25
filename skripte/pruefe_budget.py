#!/usr/bin/env python3
"""Prueft Carousel-Texte gegen die Zeichenbudgets der Slot-Karte.

Canva-Textboxen haben feste Breite und passen die Schriftgroesse nicht an.
Zu langer Text bricht um, waechst nach unten und ueberlappt das naechste
Element — ohne dass ein API-Aufruf fehlschlaegt. Diese Pruefung laeuft
deshalb VOR dem Schreiben nach Canva.

Aufruf:
    pruefe_budget.py <slots.json> <texte.json>

texte.json bildet Rollen auf Texte ab:
    {"cover_headline": "FÜHRERSCHEIN\\nMIT 17", "cover_unterzeile": "..."}

Rueckgabe: 0 wenn alles passt, 1 bei Verstoessen. Verstoesse gehen nach stdout.
"""

import json
import sys


def lade(pfad):
    with open(pfad, encoding="utf-8") as f:
        return json.load(f)


def slots_nach_rolle(karte):
    """Flacht die Seitenstruktur zu einer Abbildung Rolle -> Slot ab.

    Rollennamen muessen ueber alle Seiten eindeutig sein. Sind sie es nicht,
    ueberschreiben sich Slots stillschweigend und der Agent laesst Seiten leer,
    ohne dass es auffaellt.
    """
    gefunden = {}
    for seite in karte["seiten"]:
        for slot in seite["slots"]:
            rolle = slot["rolle"]
            if rolle in gefunden:
                raise ValueError(
                    f"Rolle {rolle!r} kommt mehrfach vor "
                    f"(Seite {gefunden[rolle]['seite']} und {seite['nummer']}). "
                    f"Rollennamen muessen eindeutig sein."
                )
            gefunden[rolle] = dict(slot, seite=seite["nummer"])
    return gefunden


def pruefe(slot, text):
    """Gibt die Liste der Verstoesse fuer einen einzelnen Slot zurueck."""
    verstoesse = []
    rolle = slot["rolle"]

    if slot.get("fest"):
        verstoesse.append(
            f"{rolle}: ist ein fester Slot und darf nicht getextet werden "
            f"(vorgesehen: {slot.get('wert')!r})"
        )
        return verstoesse

    max_zeilen = slot["zeilen"]
    budget = slot["budget"]

    # Fliesstext bricht Canva selbst um. Dort zaehlt die Gesamtlaenge gegen
    # das Budget aller Zeilen, nicht jede Zeile einzeln — sonst meldet die
    # Pruefung einen Verstoss, den es gar nicht gibt.
    if slot.get("fluss"):
        gesamt = budget * max_zeilen
        if "\n" in text:
            verstoesse.append(
                f"{rolle}: enthaelt einen harten Umbruch. Fliesstext wird von "
                f"Canva umgebrochen, hier gehoert keiner hinein."
            )
        laenge = len(text)
        if laenge > gesamt:
            verstoesse.append(
                f"{rolle}: {laenge} Zeichen, erlaubt sind {gesamt} "
                f"({max_zeilen} Zeilen à {budget}) — {laenge - gesamt} zu viel"
            )
        return verstoesse

    zeilen = text.split("\n")

    if len(zeilen) > max_zeilen:
        verstoesse.append(
            f"{rolle}: {len(zeilen)} Zeilen, erlaubt sind {max_zeilen}"
        )

    for nr, zeile in enumerate(zeilen, start=1):
        laenge = len(zeile)
        if laenge > budget:
            verstoesse.append(
                f"{rolle}, Zeile {nr}: {laenge} Zeichen, erlaubt sind {budget} "
                f"— {laenge - budget} zu viel: {zeile!r}"
            )

    return verstoesse


def pruefe_alle(karte, texte):
    slots = slots_nach_rolle(karte)
    verstoesse = []

    for rolle, text in texte.items():
        slot = slots.get(rolle)
        if slot is None:
            verstoesse.append(f"{rolle}: gibt es in der Vorlage nicht")
            continue
        verstoesse.extend(pruefe(slot, text))

    offen = [
        rolle
        for rolle, slot in slots.items()
        if not slot.get("fest") and rolle not in texte
    ]
    for rolle in sorted(offen):
        verstoesse.append(f"{rolle}: kein Text geliefert")

    return verstoesse


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2

    karte = lade(sys.argv[1])
    texte = lade(sys.argv[2])
    verstoesse = pruefe_alle(karte, texte)

    if not verstoesse:
        anzahl = len([t for t in texte])
        print(f"OK — {anzahl} Texte passen in ihre Slots.")
        return 0

    print(f"{len(verstoesse)} Verstoesse:\n")
    for v in verstoesse:
        print(f"  - {v}")
    print("\nTexte kuerzen und erneut pruefen. Nicht nach Canva schreiben.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
