# INSTALL.md — Anleitung für Claude

> **An Claude:** Diese Datei ist an dich adressiert. Ein Mensch hat dieses Repo
> geklont und will den Carousel-Agenten für **seine** Marke einrichten. Führe ihn
> durch. Er kennt Canva, aber nicht unbedingt die technischen Begriffe hier.

## Was der Agent voraussetzt

Prüfe das zuerst und sag Bescheid, wenn etwas fehlt:

1. **Canva über MCP verbunden.** Teste mit `list-brand-kits`. Kommt ein Fehler
   wegen fehlender Scopes, muss der Connector neu verbunden werden.
2. **Eine fertige Carousel-Vorlage in Canva.** Mehrseitig, 1080×1350, im Look
   der Marke, von Hand gebaut. **Der Agent erfindet kein Design.** Gibt es
   noch keine, ist das der erste Schritt — und er passiert in Canva, nicht hier.
3. **Python 3.** Keine Pakete nötig.

Autofill über Brand-Templates ist **nicht** der Weg — siehe
`docs/canva-pipeline.md`, das wurde geprüft und verworfen.

## Schritt 1 — Vorlage finden

`search-designs` aufrufen und den Menschen die richtige Vorlage wählen lassen.
Notiere die `design_id` (beginnt mit `D`).

## Schritt 2 — Slot-Karte erzeugen

Das ist der Kern der Einrichtung. Für **jede** Seite der Vorlage:

```
read-design mit open_transaction: true, filter.page_indices: [n]
```

Die Antwort listet jedes Element mit `[locator_id]`, Position, Größe,
Schriftgröße und dem aktuellen Text.

Baue daraus `konfig/slots.json` nach dem Muster in
`vorlagen/slots.beispiel.json`. Für jedes Textfeld:

| Feld | Woher |
|---|---|
| `id` | die `locator_id` aus der Antwort |
| `rolle` | sprechender Name, **über alle Seiten eindeutig** |
| `zeilen` | wie viele Zeilen der Originaltext hat |
| `budget` | Zeichen je Zeile — siehe unten |
| `original` | der Text, der jetzt drinsteht |

**Budget bestimmen:** nimm die längste Zeile des Originaltexts. Bei Headlines
(`fontWeight` `heavy` oder `ultrabold`) ziehe 15 Prozent ab. Der Originaltext
wurde von Hand gesetzt und passt nachweislich — das ist die verlässlichste
Referenz. Eine Formel aus Boxbreite und Schriftgröße streut zu stark, weil
Groß-/Kleinschreibung, Buchstabenabstand und Glyphenbreite mitspielen.

**Fließtext** (ein Absatz, der über mehrere Zeilen läuft) bekommt
`"fluss": true`. Dort zählt die Gesamtlänge, nicht die einzelne Zeile.

**Unveränderliches** — Logo-Zeile, Adresse, Seitenzähler, Nummern — bekommt
`"fest": true` und den festen Wert. Der Agent fasst diese Felder nie an.

Danach prüfen:
```
python3 skripte/pruefe_budget.py konfig/slots.json vorlagen/texte.beispiel.json
```
Bricht das mit „Rolle kommt mehrfach vor" ab, sind die Namen nicht eindeutig.

## Schritt 3 — Marke beschreiben

`konfig/marke.md` nach dem Muster in `vorlagen/marke.beispiel.md` anlegen.
Frag den Menschen nach:

- Name, Ort, Adresse, Web-Adresse
- Tonfall: Du oder Sie? Zielgruppe? Wie klingen bestehende Posts?
- Hashtags: welche immer, welche themenbezogen
- Themen, die bespielt werden
- **Harte Regeln:** was darf nie in einem Post stehen? Personenfotos?
  Preise? Rechtliches? Frag ausdrücklich danach — das ist der Teil, bei dem
  ein Fehler teuer wird.

Farben liest du am besten aus der Canva-Antwort ab, statt zu fragen.

## Schritt 4 — Probelauf

Bau ein Carousel zu einem einfachen Thema. Achte darauf:

- Läuft die Budget-Prüfung sauber durch?
- Sieht **jedes** Vorschaubild gut aus — kein Text, der aus seinem Kasten
  läuft oder das Nachbarelement überlappt?
- Sind alle exportierten PNGs 1080×1350?

Bricht etwas um, obwohl das Budget eingehalten wurde: das Budget für diesen
Slot senken und in `konfig/slots.json` nachziehen. Das ist normal beim
Einrichten und wird nach ein, zwei Posts stabil.

## Schritt 5 — Vault anbinden, falls gewünscht

Siehe `docs/vault.md`. Braucht Obsidian mit Bases. Wer das nicht nutzt,
lässt es weg — der Agent funktioniert auch ohne.

## Was danach gilt

- `konfig/`, `posts/` und `themen/` sind per `.gitignore` ausgeschlossen.
  Marken- und Kundendaten gehören nicht in ein öffentliches Repo. Prüf das
  vor dem ersten Push mit `git status`.
- Der Agent postet nicht und soll es nicht. Die Freigabe bleibt beim Menschen.
