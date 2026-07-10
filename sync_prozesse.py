#!/usr/bin/env python3
"""Sync Prozesse/ -> portal/docs/ mit Sperrliste.

Quelle der Wahrheit bleibt der Ordner Prozesse/ im Projekt-Root.
Dieses Skript kopiert die schuelertauglichen Prozessdateien in die
Website-Struktur. Vor jedem Publish ausfuehren.

Aufruf:  python3 sync_prozesse.py [Projekt-Root]
         (ohne Argument: eine Ebene ueber Kommunikation/)
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


def main() -> int:
    warnings: list[str] = []
    for src_name, (dst_name, title) in MAPPING.items():
        src = ROOT / "Prozesse" / src_name
        dst = DOCS / dst_name
        if not src.is_dir():
            print(f"FEHLER: Quelle fehlt: {src}")
            return 1
        dst.mkdir(parents=True, exist_ok=True)
        # Hinweis: Dateien werden ueberschrieben, aber nicht geloescht.
        # Wird eine Prozessdatei in Prozesse/ umbenannt/entfernt, die alte
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
