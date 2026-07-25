# Steuerpult im Obsidian-Vault

Der Agent baut Carousels. Gesteuert und überblickt wird er im Vault — nicht
in einem externen Sheet. Grund: der Vault ist ohnehin der Arbeitsort. Ein
zweiter Ort driftet auseinander, und niemand pflegt zwei Listen.

## Was der Agent im Vault anlegt

**Eine Notiz pro Post**, in einem eigenen Ordner. Frontmatter trägt die Daten,
die das Dashboard auswertet:

```yaml
---
typ: notiz
tags: [carousel, social]
status: zur-freigabe        # offen | gebaut | zur-freigabe | gepostet
thema: Führerschein mit 17
marke: Beispielmarke
kanal: Instagram
slides: 5
erstellt: 2026-07-25
gepostet:                    # wird beim Posten gefüllt
canva: https://www.canva.com/d/...
ordner: ~/…/posts/2026-07-25-fuehrerschein-mit-17
aktualisiert: 2026-07-25
---
```

Im Fließtext: die fünf Slides in Stichworten, das Ergebnis der Prüfungen und
was noch offen ist.

## Das Dashboard

Eine `.base`-Datei im Vault-Wurzelverzeichnis. Sie sammelt alle Post-Notizen
und zeigt sie in vier Ansichten:

| Ansicht | Zweck |
|---|---|
| Wartet auf mich | alles, was nicht `gepostet` ist — die tägliche Arbeitsliste |
| Alle Posts | nach Status gruppiert, Summe der Slides |
| Gepostet | Rückschau |
| Galerie | Kartenansicht |

Zwei berechnete Spalten: eine Ampel aus dem Status und das Alter in Tagen.
Liegt etwas lange auf `zur-freigabe`, sieht man es sofort.

## Arbeitsablauf

1. Dashboard öffnen, „Wartet auf mich" durchsehen
2. Claude Code im Agent-Ordner starten, Thema nennen — oder nach Vorschlägen fragen
3. Agent baut, legt ab, schreibt die Notiz
4. Nach dem Posten: `status: gepostet` und `gepostet:` setzen

Schritt 4 bleibt Handarbeit. Das ist Absicht — der Agent postet nicht, also
weiß er auch nicht, wann etwas online ging.

## Status-Werte

`offen` → `gebaut` → `zur-freigabe` → `gepostet`

Genau diese vier. Das Dashboard und die Ampel-Formel setzen sie voraus.
