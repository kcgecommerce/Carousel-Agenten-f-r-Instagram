#!/usr/bin/env python3
"""Laedt die von Canva exportierten Slides herunter und prueft sie.

Canvas Export liefert eine signierte URL je Seite. Die Signaturen laufen ab,
deshalb wird direkt nach dem Export geladen.

Aufruf:
    hole_slides.py <ziel-ordner> <urls.json>
    hole_slides.py <ziel-ordner> <url1> <url2> ...

urls.json ist entweder eine Liste von URLs oder die Antwort von export-design
(dann wird job.urls gelesen).

Geprueft wird, dass die Datei ein PNG ist und die erwarteten Masse hat.
Ein abgebrochener Download faellt so auf, statt spaeter beim Posten.
"""

import json
import os
import ssl
import struct
import subprocess
import sys
import urllib.error
import urllib.request

ERWARTET = (1080, 1350)


def png_masse(pfad):
    """Liest Breite und Hoehe aus dem IHDR-Block. Kein Pillow noetig."""
    with open(pfad, "rb") as f:
        kopf = f.read(24)
    if len(kopf) < 24 or kopf[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    breite, hoehe = struct.unpack(">II", kopf[16:24])
    return breite, hoehe


def urls_aus(quelle):
    if isinstance(quelle, dict):
        return quelle.get("job", {}).get("urls") or quelle.get("urls") or []
    return list(quelle)


def hole(url, ziel):
    """Laedt eine Datei. Faellt bei SSL-Problemen auf curl zurueck.

    Das Python von macOS bringt haeufig kein CA-Bundle mit, urllib scheitert
    dann mit CERTIFICATE_VERIFY_FAILED. curl liegt auf macOS und Linux bei und
    hat seinen eigenen Zertifikatsspeicher — das ist der verlaesslichere Weg,
    ohne eine Abhaengigkeit zu erzwingen.
    """
    try:
        kontext = ssl.create_default_context()
        try:
            import certifi

            kontext = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            pass

        with urllib.request.urlopen(url, timeout=120, context=kontext) as antwort:
            daten = antwort.read()
        with open(ziel, "wb") as f:
            f.write(daten)
        return len(daten)

    except (ssl.SSLError, urllib.error.URLError) as fehler:
        if "CERTIFICATE_VERIFY_FAILED" not in str(fehler):
            raise
        ergebnis = subprocess.run(
            ["curl", "-sSL", "--fail", "-o", ziel, url],
            capture_output=True,
            text=True,
        )
        if ergebnis.returncode != 0:
            raise RuntimeError(
                f"curl fehlgeschlagen: {ergebnis.stderr.strip() or ergebnis.returncode}"
            ) from fehler
        return os.path.getsize(ziel)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2

    ordner = sys.argv[1]
    rest = sys.argv[2:]

    if len(rest) == 1 and rest[0].endswith(".json"):
        with open(rest[0], encoding="utf-8") as f:
            urls = urls_aus(json.load(f))
    else:
        urls = rest

    if not urls:
        print("Keine URLs gefunden.")
        return 1

    os.makedirs(ordner, exist_ok=True)
    fehler = []

    for nr, url in enumerate(urls, start=1):
        ziel = os.path.join(ordner, f"slide-{nr}.png")
        try:
            groesse = hole(url, ziel)
        except Exception as e:
            fehler.append(f"slide-{nr}: Download fehlgeschlagen — {e}")
            continue

        masse = png_masse(ziel)
        if masse is None:
            fehler.append(f"slide-{nr}: keine gueltige PNG-Datei")
        elif masse != ERWARTET:
            fehler.append(
                f"slide-{nr}: Masse {masse[0]}x{masse[1]}, "
                f"erwartet {ERWARTET[0]}x{ERWARTET[1]}"
            )
        else:
            print(f"  slide-{nr}.png  {masse[0]}x{masse[1]}  {groesse // 1024} KB")

    if fehler:
        print(f"\n{len(fehler)} Probleme:")
        for f_ in fehler:
            print(f"  - {f_}")
        return 1

    print(f"\n{len(urls)} Slides in {ordner}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
