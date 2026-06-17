# -*- coding: utf-8 -*-
"""
Reemplaza W2605 -> W2605 y elimina referencias a 6/7/5 descargas/cargas/carrotanques
en archivos de texto de src, webapp, results y archivos sueltos del proyecto.
No toca RECICLAJE ni binarios.
"""
from pathlib import Path
import mimetypes

ROOT = Path(".")

TARGET_DIRS = [
    ROOT / "src",
    ROOT / "webapp",
    ROOT / "results",
    ROOT / "Data/Estudio espesores",
]

TARGET_FILES = [
    ROOT / "README.md",
    ROOT / "CONTEXT.md",
    ROOT / "README_ESTRUCTURA.md",
    ROOT / "render.yaml",
    ROOT / "requirements.txt",
    ROOT / "AGENTS.md",
    ROOT / "LICENSE",
]

SKIP_DIRS = {ROOT / "RECICLAJE", ROOT / ".git", ROOT / "venv", ROOT / ".vs", ROOT / ".vscode"}

# Extensiones de texto a procesar
TEXT_EXTENSIONS = {
    ".py", ".js", ".html", ".css", ".md", ".txt", ".tex", ".bib", ".csv",
    ".yaml", ".yml", ".json", ".svg", ".xml", ".ini", ".cfg", ".toml",
    ".rst", ".log", ".aux", ".out", ".spl", ".bbl", ".blg", ".lof", ".lot",
    ".toc", ".synctex.gz",
}


def is_text_file(path: Path) -> bool:
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    mime, _ = mimetypes.guess_type(str(path))
    if mime and mime.startswith("text/"):
        return True
    return False


def read_text(path: Path) -> str:
    encodings = ["utf-8", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            return path.read_text(encoding=enc)
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"No se pudo decodificar {path}")


def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def clean_descargas(text: str) -> str:
    # 5 descargas/cargas/carrotanques
    text = text.replace("5 descargas/dia", "5 descargas/dia")
    text = text.replace("5~descargas/dia", "5~descargas/dia")
    text = text.replace("5 descargas", "5 descargas")
    text = text.replace("5~descargas", "5~descargas")
    text = text.replace("5 carrotanques", "5 carrotanques")
    text = text.replace("5~carrotanques", "5~carrotanques")
    text = text.replace("5 cargas", "5 cargas")
    text = text.replace("5~cargas", "5~cargas")

    # 5 descargas/cargas/carrotanques
    text = text.replace("5 descargas/dia", "5 descargas/dia")
    text = text.replace("5~descargas/dia", "5~descargas/dia")
    text = text.replace("5 descargas", "5 descargas")
    text = text.replace("5~descargas", "5~descargas")
    text = text.replace("5 carrotanques", "5 carrotanques")
    text = text.replace("5~carrotanques", "5~carrotanques")
    text = text.replace("5 cargas", "5 cargas")
    text = text.replace("5~cargas", "5~cargas")
    text = text.replace("cinco descargas", "cinco descargas")
    text = text.replace("cinco cargas", "cinco cargas")
    text = text.replace("cinco carrotanques", "cinco carrotanques")

    # 5 descargas/cargas/carrotanques
    text = text.replace("5 descargas/dia", "5 descargas/dia")
    text = text.replace("5~descargas/dia", "5~descargas/dia")
    text = text.replace("5 descargas", "5 descargas")
    text = text.replace("5~descargas", "5~descargas")
    text = text.replace("5 carrotanques", "5 carrotanques")
    text = text.replace("5~carrotanques", "5~carrotanques")
    text = text.replace("5 cargas", "5 cargas")
    text = text.replace("5~cargas", "5~cargas")
    text = text.replace("cinco descargas", "cinco descargas")

    # Rango 5-7 / 5--7
    text = text.replace("5--5 descargas", "5 descargas")
    text = text.replace("5-5 descargas", "5 descargas")
    text = text.replace("5 a 5 descargas", "5 descargas")
    text = text.replace("5--5 descargas/dia", "5 descargas/dia")

    # Porcentajes 140% derivados de 5 descargas (solo cuando acompañan a 5 descargas previamente)
    # Se deja como estaba en textos genericos; se corrige manualmente si es necesario.
    return text


def replace_w2605(text: str) -> str:
    text = text.replace("W2605", "W2605")
    text = text.replace("w2605", "w2605")
    return text


def process_file(path: Path) -> bool:
    if not path.is_file():
        return False
    if not is_text_file(path):
        return False
    try:
        text = read_text(path)
    except Exception as e:
        print(f"[ERROR_LEER] {path}: {e}")
        return False
    original = text
    text = clean_descargas(text)
    text = replace_w2605(text)
    if text != original:
        try:
            write_text(path, text)
            print(f"[OK] {path}")
            return True
        except Exception as e:
            print(f"[ERROR_ESCRIBIR] {path}: {e}")
            return False
    return False


def collect_files():
    files = set()
    for d in TARGET_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if any(part in SKIP_DIRS for part in p.parents):
                continue
            if p.is_file():
                files.add(p)
    for f in TARGET_FILES:
        if f.exists():
            files.add(f)
    return sorted(files)


def main():
    files = collect_files()
    changed = 0
    for f in files:
        if process_file(f):
            changed += 1
    print(f"\nTotal archivos procesados: {len(files)}")
    print(f"Archivos modificados: {changed}")


if __name__ == "__main__":
    main()
