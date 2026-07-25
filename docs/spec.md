# Spec — Carousel-Agent

Stand 2026-07-25. Beschreibt, was gebaut wird und warum so.

## Zweck

Aus einem Thema entsteht ein vollständiges Instagram-Carousel: Slides im Look
der Marke, Caption, Hashtags. Der Agent bereitet vor; das Posten bleibt beim
Menschen.

Das Problem, das er löst: 60–90 Minuten Handarbeit pro Post. Nicht das Finden
von Ideen ist der Engpass, sondern die Umsetzung.

## Trennung von Agent und Marke

Der Agent ist markenneutral und liegt öffentlich im Repo. Alles Kundenspezifische
liegt lokal und ist per `.gitignore` ausgeschlossen.

| Ort | Inhalt | Öffentlich |
|---|---|---|
| `skill/`, `skripte/`, `vorlagen/`, `docs/` | Der Agent | ja |
| `konfig/` | Marke: Farben, Tonfall, Adresse, Slot-Karte | nein |
| `posts/` | Fertige PNGs, Captions | nein |
| `~/zweites-gehirn/` | Steuerpult: Backlog, Kalender, Dashboard | nein |

Ein Dritter, der das Repo klont, legt sein eigenes `konfig/` an und hat einen
funktionierenden Agenten für seine Marke.

## Das Steuerpult liegt im Vault

Bedient wird über Obsidian, nicht über ein externes Sheet. Grund: der Vault ist
ohnehin der Ort, an dem gearbeitet wird; ein zweiter Ort driftet auseinander.

- `themen-backlog.md` — Themenpool, von Hand ergänzbar
- `content-kalender.md` — datierter Plan
- `posts/<datum>-<thema>.md` — pro Post eine Notiz mit Frontmatter:
  `thema`, `datum`, `status`, `canva_link`, `ordner`
- `carousel-dashboard.base` — Tabellenansicht über diese Notizen: was offen,
  was geplant, was gepostet, wie viele im Monat

Ablauf: Dashboard öffnen, sehen was ansteht, Agent in Claude Code starten,
Ergebnis erscheint als Notiz im Dashboard.

## Der Canva-Weg

Festgelegt durch den Machbarkeits-Check in `canva-pipeline.md`:

```
copy-design → read-design (Transaktion) → edit-design (replace_text)
→ commit → export-design (png) → herunterladen
```

Voraussetzung: eine fertige Vorlage liegt in Canva. Sie wurde einmal von Hand
gebaut und wird pro Post kopiert und befüllt.

## Slide-Skelett

Fünf Seiten, je 1080×1350:

1. **Cover** — Kategorie, Claim, Unterzeile, Badge, Wisch-Hinweis
2. **Warum** — Kategorie, Titel, Fließtext, drei Belege, Footer, Zähler
3. **Ablauf** — Kategorie, Titel, drei nummerierte Schritte mit Unterzeile
4. **Wege** — drei Kontaktwege
5. **CTA** — Claim, Unterzeile, URL, Adresse

Das Skelett ist Teil der Vorlage, nicht des Agenten. Eine andere Vorlage mit
anderer Struktur wird über ihre Slot-Karte beschrieben.

## Slot-Karte

Pro Textfeld hält `konfig/slots.json` fest:

| Feld | Bedeutung |
|---|---|
| `id` | Canva-`locator_id` |
| `rolle` | wofür der Text steht, z.B. `cover_headline` |
| `breite` | Boxbreite in Pixel |
| `groesse` | Schriftgröße |
| `zeilen` | erlaubte Zeilenzahl |
| `budget` | maximale Zeichen je Zeile |

`budget` wird aus Breite und Schriftgröße geschätzt und an den Originaltexten
der Vorlage kalibriert.

## Zwei Prüfungen gegen kaputte Slides

Canva-Textboxen haben feste Breite und schrumpfen nicht. Zu langer Text bricht
um und überlappt das nächste Element — ohne dass ein Aufruf fehlschlägt.

1. **Budget-Prüfung vor dem Schreiben.** Jeder Text gegen sein Zeichenbudget.
   Zu lang wird gekürzt und erneut geprüft.
2. **Sichtprüfung nach dem Schreiben.** `edit-design` liefert ein Vorschaubild
   zurück. Der Agent sieht es an und erkennt, was durchs Budget gerutscht ist.

Zeichenzählen allein reicht nachweislich nicht: im Test brach eine Headline mit
derselben Zeichenzahl wie das Original um, weil ihre Glyphen breiter sind.

## Ablauf eines Durchlaufs

1. **Thema** — aus dem Aufruf, sonst Vorschlag aus Backlog und Kalender
2. **Texten** — die fünf Slides entlang des Skeletts füllen
3. **Budget-Prüfung** — Slot für Slot, kürzen bis es passt
4. **Canva** — kopieren, Texte setzen, je Seite Vorschaubild prüfen, committen
5. **Export** — PNGs in `posts/<datum>-<thema>/`
6. **Caption** — Text und Hashtags in `caption.md`
7. **Vault** — Notiz schreiben, Backlog-Status nachziehen

## Was der Agent nicht tut

- Nicht posten. Keine Instagram-Anbindung.
- Keine Gesichter oder Personenfotos einsetzen.
- Keine Termine erfinden. Datumsangaben kommen aus der Konfiguration oder vom
  Menschen.

## Bau-Reihenfolge

Der Kern zuerst, damit auch bei knapper Zeit etwas Vollständiges dasteht.

1. Slot-Karte und Marken-Konfiguration
2. Durchlauf von Thema bis PNG plus Caption
3. Backlog und Kalender
4. Vault-Notizen und Dashboard
5. INSTALL.md für Fremdnutzung
