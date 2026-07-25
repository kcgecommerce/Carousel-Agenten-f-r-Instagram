# Canva-Pipeline — Machbarkeits-Check

Datum: 2026-07-25. Geprüft, bevor gebaut wurde, damit der Bau-Weg nicht auf
einer Annahme steht.

## Was nicht geht

| Weg | Warum nicht |
|---|---|
| Brand-Template + Autofill | Konto hat **0 Brand-Templates** (`search-brand-templates` liefert leer, mit und ohne Dataset-Filter). Autofill fällt damit aus. |
| `generate-design-structured` | Kann nur `presentation`, und verlangt zwingend ein Widget, in dem ein Mensch den Outline freigibt. Nicht automatisierbar. |
| `generate-design` | Kann zwar `instagram_post` (1080×1350), erzeugt aber einseitige, KI-gewürfelte Designs. Nicht reproduzierbar, nicht mehrseitig. |

## Was geht — der gewählte Weg

```
copy-design (Vorlage)
  → read-design (open_transaction: true)   # liefert locator_ids je Element
  → edit-design (replace_text je Slot)     # pro Seite ein Aufruf
  → edit-design (finalize: commit)
  → export-design (png, 1080x1350)         # liefert eine URL pro Seite
  → curl                                    # PNGs auf Platte
```

Am 2026-07-25 komplett durchgetestet. Ergebnis: 5 PNGs, je 1080×1350, 8-bit RGB.

## Die Vorlage

`<VORLAGEN-ID>` — „Carousel-Vorlage", 5 Seiten, je 1080×1350.
Struktur, die sich für beliebige Themen wiederverwenden lässt:

1. **Cover** — Kategorie-Badge, Haupt-Claim, Unterzeile, Datums-Badge, „Wische für alle Infos"
2. **Warum** — Titel, Fließtext, 3 Bullets, Footer, Seitenzähler
3. **Ablauf** — 3 nummerierte Schritte mit Über- und Unterzeile
4. **Wege** — 3 Kanäle (Online / Telefon / Vor Ort)
5. **CTA** — Claim, Unterzeile, URL, Adresse

## Brand — aus dem Design ausgelesen, nicht geraten

- Rot: `<MARKENFARBE>`
- Hintergrund: `<HINTERGRUNDFARBE>`
- Text: `<TEXTFARBE>`
- Weiß auf Rot: `#ffffff`
- Schriftschnitte: `heavy` (Headlines), `semibold` (Rest)

Anmerkung: die HTML-Flyer im Ordner `beitraege/` nutzen `<FLYERFARBE>`. Maßgeblich
ist die Canva-Datei, weil daraus die Posts entstehen.

## Der Fallstrick — und warum er den Agenten prägt

Canva-Textboxen haben **feste Breite und passen die Schriftgröße nicht an**.
Zu langer Text bricht um, wächst nach unten und **überlappt das nächste Element**.

Im Test ersetzt: „ERSTE-HILFE-KURS" → „FÜHRERSCHEIN MIT 17". Ergebnis: die
Headline brach zu „FÜHRERSCHE / IN", schob sich über die Unterzeile, und
„BEGLEITETES FAHREN" überlappte das Badge „BF17". Layout zerstört.

Konsequenz für den Bau: jeder Text-Slot braucht ein **hartes Zeichenbudget**,
das aus Boxbreite, Schriftgröße und Zeilenzahl abgeleitet ist. Der Agent muss
beim Texten innerhalb dieses Budgets bleiben und vor dem Export prüfen, ob
er es eingehalten hat. Ein Agent, der einfach drauflos textet, produziert
kaputte Slides.

## Test-Artefakte

Wegwerf-Kopie `<TESTKOPIE-ID>` in Canva — kann gelöscht werden.
