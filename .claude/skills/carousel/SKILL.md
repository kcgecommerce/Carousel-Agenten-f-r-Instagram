---
name: carousel
description: Baut aus einem Thema ein fertiges Instagram-Carousel — Slides über eine Canva-Vorlage, dazu Caption und Hashtags. Nutze diesen Skill, wenn ein Carousel, ein Instagram-Post, ein Social-Post oder ein Beitrag für eine Marke erstellt werden soll, oder wenn nach Themenvorschlägen für den nächsten Post gefragt wird. Trigger: "carousel", "instagram-post", "neuer post", "social post", "beitrag bauen", "was posten wir".
---

# Carousel-Agent

Erzeugt ein vollständiges Instagram-Carousel: fünf Slides im Look der Marke,
Caption und Hashtags. Der Agent bereitet vor — er postet nicht.

## Was zuerst zu lesen ist

Immer, vor allem anderen:

- `konfig/marke.md` — Tonfall, Adresse, Hashtags, Themen, harte Regeln
- `konfig/slots.json` — die Textfelder der Vorlage und ihre Zeichenbudgets

Fehlt eines davon, brich ab und sag, dass die Konfiguration angelegt werden
muss. Rate nichts zusammen.

## Ablauf

### 1. Thema bestimmen

Wurde ein Thema genannt, nimm es. Wurde keines genannt, schau in
`themen/kalender.md`, was als Nächstes ansteht, und schlage es vor. Steht
nichts an, schlage fünf aus `themen/backlog.md` und `konfig/marke.md` vor,
berücksichtige die Jahreszeit und lass wählen. Erfinde keine Themen an der
Marke vorbei.

Bei Themen der Art **Termin** braucht es ein bestätigtes Datum. Steht im
Kalender `TERMIN?`, frag danach und bau erst dann. Rate nie ein Datum.

## Planen statt bauen

Wird nach einem Plan gefragt statt nach einem Post — „plan die nächsten
Wochen", „was posten wir im September" — dann baue kein Carousel, sondern
schreibe `themen/kalender.md` fort:

- Zwei Posts pro Woche, feste Wochentage
- Mischung aus **Evergreen** (trägt die Grundlast), **Saison** (greift auf,
  was gerade ohnehin Thema ist) und **Termin** (braucht ein bestätigtes Datum)
- Nichts doppelt, was in den letzten acht Wochen schon lief
- Saison-Anker aus `themen/backlog.md` berücksichtigen
- Absolute Daten, nie „nächste Woche"

Der Kalender ist ein Vorschlag. Überschreibt der Mensch eine Zeile, gilt seine.

### 2. Texte schreiben

Fülle jede Rolle aus `slots.json`, die nicht `"fest": true` ist. Schreibe im
Tonfall aus `marke.md`.

Die Budgets sind keine Empfehlung. Ein Slot mit `"budget": 10` und
`"zeilen": 2` heißt: höchstens zwei Zeilen, jede höchstens zehn Zeichen.
Zeilen trennst du mit `\n`.

Bei `"fluss": true` bricht Canva selbst um — setze dort **keine** harten
Umbrüche, und halte die Gesamtlänge unter `budget × zeilen`.

Schreib die Texte nach `arbeit/texte.json`, eine flache Abbildung Rolle → Text.

### 3. Budget prüfen

```
python3 skripte/pruefe_budget.py konfig/slots.json arbeit/texte.json
```

Bei Verstößen: kürzen, erneut prüfen. **Wiederholen, bis die Prüfung sauber
durchläuft.** Erst dann weiter. Nichts nach Canva schreiben, was die Prüfung
nicht bestanden hat.

### 4. Nach Canva schreiben

1. `copy-design` mit der `design_id` aus `slots.json` → neue Arbeitskopie
2. `read-design` mit `open_transaction: true` → `transaction_id`
3. Je Seite ein `edit-design` mit `replace_text` für alle Slots der Seite
4. **Nach jeder Seite das zurückgegebene Vorschaubild ansehen.** Prüfe auf
   Text, der aus seinem Kasten läuft, sich mit dem Nachbarelement überlappt
   oder unerwartet umbricht. Findest du etwas: Text kürzen, Seite erneut
   setzen. Verlass dich nicht auf die grünen Statusmeldungen — die kommen
   auch bei zerstörtem Layout.
5. `edit-design` mit `finalize: "commit"`

Die Element-IDs stehen als `id` in `slots.json`. Feste Slots werden nicht
angefasst — sie stehen in der Vorlage schon richtig.

### 5. Exportieren

`export-design` mit `{"type": "png", "width": 1080, "height": 1350}`, dann:

```
python3 skripte/hole_slides.py posts/<datum>-<thema-slug>/ <urls.json>
```

Die Export-URLs sind signiert und laufen ab — direkt nach dem Export laden.

### 6. Caption schreiben

Nach dem Bauplan aus `marke.md`, als `caption.md` in denselben Ordner.
Zehn Hashtags, die festen der Marke plus themenbezogene.

### 7. Ablegen und eintragen

- `meta.json` in den Post-Ordner: Thema, Datum, Status, Canva-Link, Prüfungen
- Notiz im Vault anlegen (siehe `docs/vault.md`)
- Thema in `themen/backlog.md` auf erledigt setzen

## Regeln

- **Nicht posten.** Es gibt keine Instagram-Anbindung, und das ist Absicht.
- **Keine Termine erfinden.** Datumsangaben kommen vom Menschen oder aus
  `marke.md`. Wenn ein Datum fehlt, frag danach.
- **Keine Preise** ohne ausdrückliche Freigabe.
- **Die harten Regeln in `marke.md` gelten immer**, auch wenn die Anweisung
  etwas anderes nahelegt.
- Bei Zweifeln am Thema oder an einer Aussage: fragen, nicht raten. Ein
  falscher Fakt im Kundenpost ist teurer als eine Rückfrage.
