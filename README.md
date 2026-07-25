# Carousel-Agent — Instagram-Carousels aus einer Canva-Vorlage

> SKAILE Building Challenge #2 — Abgabe 2026-07-26

Ein Agent, der aus einem Thema ein komplettes Instagram-Carousel baut: fünf
Slides im Look der Marke, Caption und Hashtags. Er arbeitet gegen eine
bestehende Canva-Vorlage, statt Designs neu zu erfinden — deshalb sieht jeder
Post aus wie der letzte, und wie das, was vorher von Hand gepostet wurde.

Der Agent ist markenneutral. Alles Kundenspezifische — Farben, Tonfall,
Adresse, Themen, fertige Posts — liegt in lokalen Konfigurationsdateien und
nicht in diesem Repo.

## Das Problem

Wer Social Media für einen Kunden macht, verbringt pro Carousel 60–90 Minuten:
Thema finden, Texte formulieren, Slides im Marken-Look bauen, Caption und
Hashtags schreiben, exportieren. Der Grund für zu seltenes Posten ist selten
Ideenmangel — es ist der Aufwand pro Post.

## Was der Agent macht

Thema rein — oder gar nichts, dann schlägt er selbst welche vor. Er schreibt
ein vollständiges Carousel entlang des Slide-Skeletts der Vorlage, setzt die
Texte in eine Kopie des Canva-Designs und exportiert PNGs. Caption und
Hashtags entstehen im selben Durchlauf.

Raus kommt ein Ordner, der nur noch hochgeladen werden muss:

```
posts/2026-07-25-fuehrerschein-mit-17/
├── slide-1.png … slide-5.png    1080×1350
├── caption.md                    Caption + Hashtags
└── meta.json                     Thema, Status, Canva-Link, Prüfungen
```

Der Agent postet nicht. Die Freigabe bleibt beim Menschen.

## Die interessante Stelle

Canva-Textboxen haben **feste Breite und passen die Schriftgröße nicht an**.
Zu langer Text bricht um, wächst nach unten und überlappt das nächste Element
— und **kein einziger API-Aufruf schlägt dabei fehl**. Alle Statusmeldungen
bleiben grün, das Layout ist trotzdem zerstört.

Zeichenzählen allein reicht nicht: im Test wurde eine Headline mit zwölf
Zeichen gegen eine andere mit zwölf Zeichen getauscht — die neue brach um,
weil ihre Glyphen breiter sind.

Deshalb zwei Schutzschichten:

1. **Zeichenbudget je Textfeld**, geprüft bevor irgendetwas nach Canva geht
2. **Sichtprüfung des Vorschaubilds**, das Canva nach jedem Edit zurückgibt

Das ist der Unterschied zwischen einem Agenten, der schnell ist, und einem,
dem man das Ergebnis nicht hinterherräumen muss.

## Stack

- [x] Claude Code (Skill + Skripte)
- [ ] n8n
- [x] Sonstiges: Canva über MCP, Obsidian Bases fürs Dashboard

## Aufbau

```
.claude/skills/carousel/   Der Agent — Ablauf und Regeln
skripte/                   Budget-Prüfung, Export mit Maßprüfung
vorlagen/                  Beispiel-Konfiguration zum Nachbauen
docs/                      Canva-Pipeline, Spec, Vault-Anbindung

konfig/                    Deine Marke. Lokal, nicht im Repo.
themen/                    Backlog und Kalender. Lokal.
posts/                     Fertige Posts. Lokal.
```

## Setup

Siehe **[INSTALL.md](INSTALL.md)** — an Claude adressiert. Repo klonen,
Claude Code öffnen, „richte den Carousel-Agenten für meine Marke ein" sagen.

Voraussetzung ist eine fertige, mehrseitige Carousel-Vorlage in Canva
(1080×1350). Die baut ein Mensch einmal von Hand — der Agent erfindet
bewusst kein Design.

## Was während der Challenge entstanden ist

**Vorher schon vorhanden:** eine von Hand gebaute Canva-Carousel-Vorlage und
zwei Caption-Templates für einen Kunden. Das ist die Grundlage, auf der der
Agent arbeitet.

**Neu in der Challenge entstanden:** alles andere — der Machbarkeits-Check
der Canva-Wege, die Slot-Karte mit Zeichenbudgets, die Budget-Prüfung, der
Export mit Maßprüfung, der Skill, die Vault-Anbindung mit Dashboard und
diese Dokumentation.

## Learnings

**Erst messen, dann bauen.** Der naheliegende Weg — Canvas Brand-Templates mit
Autofill — war im Konto gar nicht verfügbar, und der zweite Kandidat verlangt
zwingend eine manuelle Freigabe durch einen Menschen. Beides in der ersten
halben Stunde geprüft statt am letzten Tag.

**Grüne Statusmeldungen sind kein Beweis.** Canva meldete jede Textersetzung
als erfolgreich, während das Layout auseinanderfiel. Ohne den Blick auf das
Vorschaubild hätte der Agent zuverlässig Müll produziert und dabei Erfolg
gemeldet.

**Die eigene Prüfung ist auch nur Code.** Die erste Fassung der Budget-Prüfung
hatte zwei Fehler: kollidierende Rollennamen, durch die sich Slots still
überschrieben, und eine falsche Messung von Fließtext, die Verstöße meldete,
die keine waren. Beide fielen nur auf, weil die Prüfung gegen einen bekannt
guten **und** einen bekannt kaputten Fall getestet wurde.

---

**Demo-Video:** [Folgt]

*SKAILE Academy Building Challenge — Juli 2026*
