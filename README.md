# Carousel-Agent — Instagram-Carousels aus einer Canva-Vorlage

> SKAILE Building Challenge #2 — Abgabe 2026-07-26

Ein Agent, der aus einem Thema ein komplettes Instagram-Carousel baut: Slides im
Look der Marke, Caption und Hashtags dazu. Er arbeitet gegen eine bestehende
Canva-Vorlage, statt Designs neu zu erfinden — deshalb sieht das Ergebnis aus
wie das, was vorher schon von Hand gepostet wurde.

Der Agent ist markenneutral. Alles Kundenspezifische — Farben, Tonfall, Adresse,
Themen, fertige Posts — liegt in lokalen Konfigurationsdateien und nicht in
diesem Repo.

## Das Problem

Wer Social Media für einen Kunden macht, verbringt pro Carousel 60–90 Minuten:
Thema finden, Texte formulieren, Slides im Marken-Look bauen, Caption und
Hashtags schreiben, exportieren. Der Grund für zu seltenes Posten ist selten
Ideenmangel — es ist der Aufwand pro Post.

## Was der Agent macht

Thema rein — oder gar nichts, dann schlägt er selbst welche vor. Er schreibt
daraus ein vollständiges Carousel entlang eines festen Slide-Skeletts:
Hook, Inhalt, Ablauf, Wege, Call-to-Action. Die Texte gehen in eine Kopie der
Canva-Vorlage, die als PNG-Serie exportiert wird. Caption und Hashtags entstehen
im selben Durchlauf. Raus kommt ein Ordner, der nur noch hochgeladen werden muss.

Der Agent postet nicht selbst. Er bereitet vor, die Freigabe bleibt beim Menschen.

## Stack

- [x] Claude Code (Agent / Skills)
- [ ] n8n
- [x] Sonstiges: Canva über MCP (Design-Kopie, Textersetzung, PNG-Export)

## Aufbau

```
skill/            Der Agent — Ablauf und Regeln
skripte/          Export und Budget-Pruefung
vorlagen/         Beispiel-Konfiguration zum Nachbauen
docs/             Wie die Canva-Pipeline funktioniert und warum so

konfig/           Deine Marke. Lokal, nicht im Repo.
themen/           Backlog und Kalender. Lokal.
posts/            Fertige Posts. Lokal.
```

## Setup

[Folgt — INSTALL.md, an Claude adressiert.]

## Was während der Challenge entstanden ist

[Folgt.]

## Learnings

[Folgt.]

---

**Demo-Video:** [Folgt]

*SKAILE Academy Building Challenge — Juli 2026*
