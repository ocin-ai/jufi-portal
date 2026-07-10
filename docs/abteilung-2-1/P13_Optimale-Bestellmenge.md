# Prozess 13: Ermittlung optimale Bestellmenge / Einkaufsmenge

> Abteilung 2.1 Wareneinkauf / Lager · Status: überarbeitet (fachlich ausgebaut) · zuletzt bearbeitet: 2026-07-07

## Steckbrief

| | |
| --- | --- |
| **Prozess-Nr.** | 13 |
| **Verantwortlich** | → [Übersicht](00_Uebersicht-Prozesse-Verantwortlichkeiten.md) |
| **Turnus** | regelmäßig (vor jedem Einkauf) |
| **Schnittstellen** | Team Einkaufsliste · Team SumUp · Team Inventur |

## Ziel / Kurzbeschreibung

Für jeden Artikel die passende Bestellmenge bestimmen, sodass der Kiosk bis zum nächsten Einkauf lieferfähig bleibt, ohne zu viel zu bestellen (Vermeidung von Überbeständen und Verderb). Grundlage sind die tatsächlichen Verkaufszahlen und der aktuelle Bestand.

## Relevante Dateien

| Datei | Dateiname | Dateipfad |
| --- | --- | --- |
| Bedarfsermittlung (Excel, optional) | 25-26_13_Bedarfsermittlung | Ablage_2.1_Wareneinkauf-Lager/13_Optimale-Bestellmenge/ |
| Verkaufsdaten (SumUp) | vgl. [P05](P05_Umsatzauswertung-SumUp.md) | vgl. P05 |
| Aktueller Bestand (Inventur) | vgl. [P07](P07_Inventur.md) | vgl. P07 |
| Konzept-Notiz (Aufbau der Excel; Datei folgt bei Bedarf) | 25-26_13_Bedarfsermittlung_Konzept.md | Ablage_2.1_Wareneinkauf-Lager/13_Optimale-Bestellmenge/ |

## Prozessschritte

- [ ] **Verkaufstempo ermitteln:** Für den Artikel den durchschnittlichen Absatz pro Woche aus SumUp bestimmen (Verkaufsbericht, z. B. Mittel der letzten 4 Wochen; vgl. [P05](P05_Umsatzauswertung-SumUp.md)).
- [ ] **Erwarteten Bedarf berechnen:** Bedarf bis zum nächsten Einkauf = durchschnittlicher Wochenabsatz × Anzahl Wochen bis zum nächsten Einkauf.
- [ ] **Aktuellen Bestand abziehen:** Ist-Bestand aus der Inventur berücksichtigen (vgl. [P07](P07_Inventur.md)).
- [ ] **Sicherheitsbestand einplanen:** Kleinen Puffer für Nachfrageschwankungen und ausgefallene Einkaufsfahrten aufschlagen (Faustregel; bei stark schwankenden Artikeln höher).
- [ ] **Bestellmenge festlegen:** Bestellmenge = erwarteter Bedarf + Sicherheitsbestand − aktueller Bestand.
- [ ] **Haltbarkeit prüfen:** Bei verderblichen Artikeln nicht mehr bestellen, als bis zum Mindesthaltbarkeitsdatum verkauft werden kann (vgl. [P17](P17_Pruefung-Haltbarkeit.md)).
- [ ] **Sonderfaktoren berücksichtigen:** Aktionen, Ferien/Feiertage, saisonale Effekte (z. B. Kaltgetränke bei Hitze) einplanen.
- [ ] **In die Einkaufsliste übertragen:** Ergebnis mit Menge an das Team Einkaufsliste geben (vgl. [P01](P01_Einkaufsliste-erstellen.md)).

## Offene Punkte / tbd.

- Bewusst praxisnah/bedarfsorientiert gehalten (Berufskolleg-tauglich). Die weitergehenden Bildungsplan-Kompetenzen (Lagerkennziffern, ABC-Analyse) sind im Bildungsplan-Mapping *(interne Datei, nicht im Portal)* als Ausbau-Kandidaten vermerkt und können später ein eigener Unterrichtsbaustein werden.
