# Canva-Pipeline — Machbarkeits-Check

Geprüft am 2026-07-25, bevor gebaut wurde, damit der Bau-Weg nicht auf einer
Annahme steht. Alle Aussagen sind gegen die Canva-MCP-Tools getestet, nicht
aus der Dokumentation abgeschrieben.

## Was nicht geht

| Weg | Warum nicht |
|---|---|
| Brand-Template + Autofill | `search-brand-templates` lieferte leer — mit und ohne Dataset-Filter. Brand-Templates setzen einen entsprechenden Canva-Plan voraus. Ohne sie fällt Autofill aus. |
| `generate-design-structured` | Kann nur `presentation`, und verlangt zwingend ein Widget, in dem ein Mensch den Outline freigibt. Für einen Agenten, der durchläuft, unbrauchbar. |
| `generate-design` | Kann zwar `instagram_post` (1080×1350), erzeugt aber einseitige, KI-gewürfelte Designs. Nicht mehrseitig, nicht reproduzierbar, nicht im Marken-Look. |

## Was geht — der gewählte Weg

```
copy-design (Vorlage)
  → read-design (open_transaction: true)   # liefert locator_ids je Element
  → edit-design (replace_text je Slot)     # ein Aufruf pro Seite
  → edit-design (finalize: commit)
  → export-design (png, 1080x1350)         # eine URL pro Seite
  → herunterladen
```

Am 2026-07-25 komplett durchgetestet: 5 PNGs, je 1080×1350, 8-bit RGB.

Der Weg setzt voraus, dass in Canva **eine fertige Vorlage liegt**, die einmal
von Hand gebaut wurde. Das ist keine Schwäche, sondern der Grund, warum das
Ergebnis nach der Marke aussieht statt nach Stock-Design.

## Der Fallstrick — und warum er den Agenten prägt

Canva-Textboxen haben **feste Breite und passen die Schriftgröße nicht an**.
Zu langer Text bricht um, wächst nach unten und **überlappt das nächste
Element**. Das Layout ist dann zerstört, ohne dass irgendein Aufruf fehlschlägt
— alle Statusmeldungen bleiben grün.

Beobachtet im Test: eine Headline mit 12 Zeichen wurde gegen eine andere
Headline mit ebenfalls 12 Zeichen getauscht. Die neue brach trotzdem um und
schob sich über die Unterzeile, weil ihre Glyphen breiter sind. Zeichenzählen
allein reicht also nicht.

Daraus folgen zwei Schutzschichten:

1. **Zeichenbudget je Slot**, abgeleitet aus Boxbreite, Schriftgröße und
   erlaubter Zeilenzahl. Greift vor dem Canva-Aufruf und fängt die groben Fälle.
2. **Sichtprüfung des Thumbnails.** `edit-design` gibt nach jedem Edit ein
   gerendertes Vorschaubild zurück. Der Agent schaut es an und erkennt
   Überlappungen, die durch das Budget gerutscht sind.

Ein Agent ohne diese Prüfungen produziert zuverlässig kaputte Slides und meldet
dabei Erfolg.

## Was der Agent über die Vorlage wissen muss

Pro Textfeld: `locator_id`, welche Rolle es im Slide spielt, Boxbreite,
Schriftgröße, erlaubte Zeilenzahl, daraus das Zeichenbudget. Diese Abbildung
wird einmal je Vorlage erstellt und liegt in der lokalen Konfiguration —
sie beschreibt eine konkrete Marke und gehört deshalb nicht ins Repo.
