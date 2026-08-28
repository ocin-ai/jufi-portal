#!/usr/bin/env python3
"""Sync <Abteilung>/_Prozesse/ -> Portal/docs/ mit Sperrliste.

Quelle der Wahrheit bleiben die Ordner `_Prozesse/` in den Abteilungsordnern.
Dieses Skript kopiert die schuelertauglichen Prozessdateien in die
Website-Struktur. Vor jedem Publish ausfuehren.

Aufruf:  python3 sync_prozesse.py [Projekt-Root]
         (ohne Argument: der Projektordner BK2J-Jufi, zwei Ebenen ueber Portal/)
"""
import re
import shutil
import sys
from pathlib import Path

PORTAL = Path(__file__).resolve().parent
DOCS = PORTAL / "docs"
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else PORTAL.parent.parent

# Abteilungs-Ordner: Quelle -> (Ziel in docs/, Nav-Titel)
MAPPING = {
    "1_Sekretariat-Personal": ("abteilung-1", "Abteilung 1 – Sekretariat / Personal"),
    "2.1_Wareneinkauf-Lager": ("abteilung-2-1", "Abteilung 2.1 – Wareneinkauf / Lager"),
}

# MATERIAL: Master-PDF (relativ zum Projekt-Root) -> Dateiname in docs/dateien/
# Nur Lesematerial. Arbeitsdateien (Excel/Word zum Ausfuellen) gehoeren NICHT ins
# oeffentliche Portal - sie liegen auf dem Schullaufwerk.
MATERIAL = {
    "00_Firmenorga/_Vorlagen/2627_00_Regeln_Handout-A4_v1.pdf": "Regeln-Handout.pdf",
    "1_Sekretariat-Personal/_Vorlagen/2627_08_Arbeitszeugnis-Infoblatt_v1.pdf": "Infoblatt-Arbeitszeugnis.pdf",
    "1_Sekretariat-Personal/_Vorlagen/2627_10_Betriebsrat-Infoblatt_v1.pdf": "Infoblatt-Betriebsrat.pdf",
}

# SPERRLISTE: diese Dateien werden NIEMALS veroeffentlicht (Regex, case-insensitive)
BLOCKLIST = [
    r"^00_Logins",              # Zugangsdaten
    r"^00_Bildungsplan-Mapping",  # didaktisches Internum
    r"^00_Offene-Punkte",       # Arbeitsstand
    r"Startprompt",             # Chat-Interna
    r"^\.",                     # versteckte Dateien (.DS_Store etc.)
]

# WARNLISTE: bei Treffern im Inhalt Warnung ausgeben (manuell pruefen)
CONTENT_WARN = [
    (r"(?i)passwort|kennwort", "Passwort erwaehnt"),
    (r"(?i)00_Logins", "Verweis auf Logins-Datei"),
    (r"\b(GL|Sekretariat)\s*\(\s*[A-ZÄÖÜ]{2}", "moegliche SuS-Kuerzel (XX)"),
]


def blocked(name: str) -> bool:
    return any(re.search(p, name, re.IGNORECASE) for p in BLOCKLIST)


def sync_regeln(warnings: list[str]) -> None:
    """00_Firmenorga/00_Regeln-Mitarbeitende.md -> docs/regeln.md (SuS-Regelwerk)."""
    src = ROOT / "00_Firmenorga" / "00_Regeln-Mitarbeitende.md"
    if not src.is_file():
        warnings.append("00_Regeln-Mitarbeitende.md fehlt in 00_Firmenorga/ – docs/regeln.md nicht aktualisiert")
        return
    text = src.read_text(encoding="utf-8")
    # Entwurfs-/Status-Zeile nicht veroeffentlichen
    text = re.sub(r"^> Status: .*\n", "", text, flags=re.MULTILINE)
    for pattern, label in CONTENT_WARN:
        if re.search(pattern, text):
            warnings.append(f"00_Regeln-Mitarbeitende.md: {label}")
    # Hinweis auf die Druckfassung nur in der Portalfassung ergaenzen
    text = text.replace(
        "> Gilt verbindlich für **alle Abteilungen**.",
        "> Gilt verbindlich für **alle Abteilungen**. Zum Ausdrucken gibt es dieselben Regeln\n"
        "> als [Handout (PDF)](dateien/Regeln-Handout.pdf) — siehe [Material](material.md).\n>\n> ",
        1,
    )
    (DOCS / "regeln.md").write_text(text, encoding="utf-8")
    print("  kopiert:   00_Regeln-Mitarbeitende.md -> regeln.md")


def sync_material(warnings: list[str]) -> None:
    """Lesematerial (PDF) aus den _Vorlagen-Ordnern -> docs/dateien/."""
    ziel = DOCS / "dateien"
    ziel.mkdir(parents=True, exist_ok=True)
    erlaubt = set()
    for quelle, name in MATERIAL.items():
        src = ROOT / quelle
        erlaubt.add(name)
        if not src.is_file():
            warnings.append(f"Material fehlt: {quelle} - {name} nicht aktualisiert")
            continue
        shutil.copy2(src, ziel / name)
        print(f"  kopiert:   {name}")
    for alt in ziel.glob("*"):
        if alt.is_file() and alt.name not in erlaubt:
            warnings.append(f"dateien/{alt.name}: nicht mehr in MATERIAL - manuell loeschen")


def main() -> int:
    warnings: list[str] = []
    sync_regeln(warnings)
    sync_material(warnings)
    for src_name, (dst_name, title) in MAPPING.items():
        src = ROOT / src_name / "_Prozesse"
        dst = DOCS / dst_name
        if not src.is_dir():
            print(f"FEHLER: Quelle fehlt: {src}")
            return 1
        dst.mkdir(parents=True, exist_ok=True)
        # Hinweis: Dateien werden ueberschrieben, aber nicht geloescht.
        # Wird eine Prozessdatei in _Prozesse/ umbenannt/entfernt, die alte
        # Kopie in docs/ manuell loeschen (Warnung unten).
        src_names = {f.name for f in src.glob("*.md") if not blocked(f.name)}
        for old in dst.glob("*.md"):
            if old.name not in src_names:
                warnings.append(f"{dst_name}/{old.name}: verwaist (Quelle fehlt) – manuell loeschen")
        (dst / ".pages").write_text(f"title: {title}\n", encoding="utf-8")
        for f in sorted(src.glob("*.md")):
            if blocked(f.name):
                print(f"  gesperrt:  {src_name}/{f.name}")
                continue
            text = f.read_text(encoding="utf-8")
            # Links auf gesperrte Dateien -> neutraler Text (kein toter Link im Portal)
            text = re.sub(
                r"\[([^\]]*)\]\((?:\.\./|\./)*(?:00_Logins|00_Bildungsplan-Mapping|00_Offene-Punkte)[^)]*\.md\)",
                r"\1 *(interne Datei, nicht im Portal)*",
                text,
            )
            # Verweis auf das zentrale Regelwerk -> Portalseite regeln.md
            text = text.replace("../00_Regeln-Mitarbeitende.md", "../regeln.md")
            for pattern, label in CONTENT_WARN:
                if re.search(pattern, text):
                    warnings.append(f"{src_name}/{f.name}: {label}")
            (dst / f.name).write_text(text, encoding="utf-8")
            print(f"  kopiert:   {src_name}/{f.name}")
    if warnings:
        print("\nWARNUNGEN (manuell pruefen, Datei wurde trotzdem kopiert):")
        for w in warnings:
            print(f"  ! {w}")
    print("\nSync abgeschlossen.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
