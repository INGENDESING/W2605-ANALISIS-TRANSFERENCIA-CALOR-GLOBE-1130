# -*- coding: utf-8 -*-
"""
Script de limpieza masiva:
1. Elimina toda referencia a 6, 7 u 5 descargas/cargas/carrotanques diarios
   en los informes LaTeX activos, limitando la capacidad maxima a 5 descargas/dia.
2. Reemplaza el codigo de proyecto W2605 por W2605 en archivos de texto.

Uso:
    python src/fix_descargas_w2605.py
"""
from pathlib import Path

ROOT = Path(".")

# Archivos LaTeX activos a depurar
LATEX_FILES = [
    ROOT / "docs/report/W2605-PR-INF-001.tex",
    ROOT / "docs/report/W2605-PR-INF-002.tex",
    ROOT / "docs/report/W2605-PR-INF-003.tex",
    ROOT / "docs/report/ResumenEjecutivoGerencial_W2605.tex",
    ROOT / "docs/report/sections/01_frontmatter.tex",
    ROOT / "docs/report/sections/02_resumen.tex",
    ROOT / "docs/report/sections/04_introduccion.tex",
    ROOT / "docs/report/sections/05_balance_materia_energia.tex",
    ROOT / "docs/report/sections/05_objetivos.tex",
    ROOT / "docs/report/sections/06_alcance.tex",
    ROOT / "docs/report/sections/07_bases_disenio.tex",
    ROOT / "docs/report/sections/08_metodologia.tex",
    ROOT / "docs/report/sections/09_resultados.tex",
    ROOT / "docs/report/sections/10_analisis.tex",
    ROOT / "docs/report/sections/11_conclusiones.tex",
    ROOT / "docs/report/sections/13_anexos.tex",
    ROOT / "docs/report/config/datos_proyecto.tex",
    ROOT / "docs/report/config/datos_proyecto_001.tex",
    ROOT / "docs/report/config/datos_proyecto_002.tex",
    ROOT / "docs/report/config/datos_proyecto_003.tex",
    ROOT / "docs/report/config/header.tex",
    ROOT / "docs/report/config/membrete_config.yaml",
    ROOT / "docs/report/config/preamble.tex",
    ROOT / "docs/report/references/bibliografia.bib",
]


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def write_text(path: Path, text: str):
    path.write_text(text, encoding="utf-8")


def replace_exact(text: str, old: str, new: str) -> str:
    """Reemplazo literal de subcadenas."""
    return text.replace(old, new)


def clean_descargas_latex(text: str) -> str:
    # --- Resumen Ejecutivo Gerencial ---
    text = replace_exact(
        text,
        "El area de 13~m$^2$ cubre el requerimiento de 5 descargas diarias en el Caso~A (100~%) y lo supera en el Caso~B (140~%, 5 descargas/dia). Manteniendo la glucosa almacenada a $\\geq$55$^\\circ$C (Caso~B), se alcanzan 5 descargas/dia.",
        "El area de 13~m$^2$ cubre el requerimiento de 5 descargas diarias en ambos casos. Manteniendo la glucosa almacenada a $\\geq$55$^\\circ$C (Caso~B), se reduce el tiempo por descarga y se aumenta el margen termico, siempre dentro del limite maximo de 5 descargas/dia.",
    )

    text = replace_exact(
        text,
        "Con el area de 13~m$^2$ se alcanzan 5--5 descargas/dia segun condiciones termicas, versus 5 descargas requeridas.",
        "Con el area de 13~m$^2$ se cumple el requerimiento de 5 descargas/dia en condiciones realistas, con mayor margen termico cuando la glucosa se mantiene $\\geq$55$^\\circ$C.",
    )

    text = replace_exact(
        text,
        "Incremento de capacidad de 5 a 5 descargas/dia (+40%)",
        "Mayor margen termico y menor tiempo por descarga manteniendo el limite de 5 descargas/dia",
    )

    text = replace_exact(
        text,
        "El tanque Tag 53A-90A-0056 con el sistema de media cana del fondo construido (13~m$^2$) alcanza una capacidad de 5--5 descargas diarias segun las condiciones termicas de operacion. El requerimiento actual es de 5 descargas diarias (120~ton/dia), que se cumple al 100~% en el Caso~A y se supera al 140~% en el Caso~B (5 descargas/dia, 168~ton/dia). Para alcanzar la condicion superior es mandatorio mantener la glucosa almacenada a temperaturas $\\geq$55$^\\circ$C mediante optimizacion del aislamiento termico.",
        "El tanque Tag 53A-90A-0056 con el sistema de media cana del fondo construido (13~m$^2$) cumple el requerimiento actual de 5 descargas diarias (120~ton/dia). En condiciones realistas (Caso~A) se alcanza el 100~% del requerimiento. Manteniendo la glucosa almacenada a temperaturas $\\geq$55$^\\circ$C (Caso~B) se incrementa el margen termico y se reduce el tiempo por descarga, siempre dentro del limite maximo de 5 descargas/dia.",
    )

    # --- sections/02_resumen.tex ---
    text = replace_exact(
        text,
        "El \\textbf{Caso B (55$\\rightarrow$57\\°C)} corresponde a una estrategia de mantenimiento termico proactivo. Al mantener la glucosa almacenada a minimo 55\\°C, el flujo maximo aumenta a 7.5~ton/h, permitiendo completar 5 descargas por dia (168~toneladas), equivalente al 140\\% del requerimiento operativo.",
        "El \\textbf{Caso B (55$\\rightarrow$57\\°C)} corresponde a una estrategia de mantenimiento termico proactivo. Al mantener la glucosa almacenada a minimo 55\\°C, el flujo maximo aumenta a 7.5~ton/h, reduciendo el tiempo por descarga y aumentando el margen termico, siempre dentro del limite maximo de 5 descargas/dia (120~toneladas).",
    )

    text = replace_exact(
        text,
        "El area de 13~m$^2$ cumple con el requerimiento de 5 descargas diarias en el Caso~A (100~%) y lo supera en el Caso~B (140~%, 5 descargas/dia). Se recomienda optimizar el aislamiento termico del tanque con el fin de mantener la glucosa almacenada a temperaturas $\\geq$ 55\\°C, condicion necesaria para garantizar una operacion robusta con el area disponible.",
        "El area de 13~m$^2$ cumple con el requerimiento de 5 descargas diarias en ambos casos. Se recomienda optimizar el aislamiento termico del tanque con el fin de mantener la glucosa almacenada a temperaturas $\\geq$ 55\\°C, condicion que aumenta el margen termico y robustece la operacion dentro del limite maximo de 5 descargas/dia.",
    )

    text = replace_exact(
        text,
        "La condicion ideal con aislamiento optimizado (55\\°C a 57\\°C) permitiria hasta 7.5~ton/h, equivalente a 5 descargas diarias.",
        "La condicion ideal con aislamiento optimizado (55\\°C a 57\\°C) permitiria hasta 7.5~ton/h, aunque la operacion se mantendra dentro del limite maximo de 5 descargas diarias.",
    )

    text = replace_exact(
        text,
        "Con area 13~m$^2$, en condicion realista (54\\°C$\\rightarrow$57\\°C, considerando perdidas por aislamiento degradado tras 20 anos), se alcanzan 5 descargas diarias (120~ton/dia, 100% del requerimiento). Con aislamiento termico optimizado (55\\°C$\\rightarrow$57\\°C), se alcanzan 5 descargas (168~ton/dia, 140%).",
        "Con area 13~m$^2$, en condicion realista (54\\°C$\\rightarrow$57\\°C, considerando perdidas por aislamiento degradado tras 20 anos), se alcanzan 5 descargas diarias (120~ton/dia, 100% del requerimiento). Con aislamiento termico optimizado (55\\°C$\\rightarrow$57\\°C), se mantiene la capacidad de 5 descargas diarias con mayor margen termico.",
    )

    text = replace_exact(
        text,
        "Mantener glucosa almacenada $\\geq$ 55\\°C & Alta & Incremento de capacidad de 5 a 5 descargas/dia (+40%). Eleva el cumplimiento del requerimiento de 100% a 140%.",
        "Mantener glucosa almacenada $\\geq$ 55\\°C & Alta & Mayor margen termico y menor tiempo por descarga, manteniendo el limite maximo de 5 descargas/dia.",
    )

    text = replace_exact(
        text,
        "El tanque de almacenamiento de glucosa Tag 53A-90A-0056 con el sistema de media cana del fondo construido (13~m$^2$ en fondo toriesferico) opera en condiciones realistas (54\\°C$\\rightarrow$57\\°C, considerando perdidas termicas por aislamiento degradado tras 20 anos de servicio) con una capacidad de 5 descargas diarias (120~ton/dia, 100% del requerimiento de 5 descargas). La condicion de 5 descargas diarias (168~ton/dia, 140% del requerimiento) requiere mantener la glucosa almacenada a $\\geq$55\\°C mediante optimizacion del aislamiento termico.",
        "El tanque de almacenamiento de glucosa Tag 53A-90A-0056 con el sistema de media cana del fondo construido (13~m$^2$ en fondo toriesferico) opera en condiciones realistas (54\\°C$\\rightarrow$57\\°C, considerando perdidas termicas por aislamiento degradado tras 20 anos de servicio) con una capacidad de 5 descargas diarias (120~ton/dia, 100% del requerimiento de 5 descargas). Manteniendo la glucosa almacenada a $\\geq$55\\°C mediante optimizacion del aislamiento termico se incrementa el margen termico y se reduce el tiempo por descarga, siempre dentro del limite maximo de 5 descargas/dia.",
    )

    # --- sections/09_resultados.tex ---
    text = replace_exact(
        text,
        "\\textbf{Descargas/dia} & \\textbf{5} & \\textbf{7} & +2 \\\\",
        "\\textbf{Descargas/dia} & \\textbf{5} & \\textbf{5} & limite operativo \\\\",
    )
    text = replace_exact(
        text,
        "Capacidad diaria & 120 ton & 168 ton & +48 ton \\\\",
        "Capacidad diaria & 120 ton & 120 ton & dentro del limite \\\\",
    )
    text = replace_exact(
        text,
        "Cumplimiento req. (120 ton) & 100% & 140% & +40% \\\\",
        "Cumplimiento req. (120 ton) & 100% & 100% & cumple limite \\\\",
    )

    text = replace_exact(
        text,
        "\\textbf{Caso B (55\\°C$\\rightarrow$57\\°C):} Manteniendo la glucosa almacenada a 55\\°C, el flujo maximo aumenta a 7.5~ton/h. Esto permite completar \\textbf{5 descargas por dia} (168~toneladas), alcanzando el 140\\% del requerimiento de 5 descargas diarias.",
        "\\textbf{Caso B (55\\°C$\\rightarrow$57\\°C):} Manteniendo la glucosa almacenada a 55\\°C, el flujo maximo aumenta a 7.5~ton/h. Si bien el flujo tecnico permite tiempos de descarga mas cortos, la operacion se mantiene dentro del limite maximo de \\textbf{5 descargas por dia} (120~toneladas), cumpliendo el 100% del requerimiento.",
    )

    text = replace_exact(
        text,
        "\\textbf{Conclusion operativa:} Con el requerimiento actualizado de 5 descargas diarias, el area de 13~m\\textsuperscript{2} \\textbf{cumple} el objetivo en el Caso~A (5 descargas/dia) y \\textbf{lo supera} en el Caso~B (5 descargas/dia). Manteniendo la glucosa a minimo 55\\°C (Caso~B), se alcanza una capacidad de 5 descargas/dia, equivalente al 140\\% del requerimiento.",
        "\\textbf{Conclusion operativa:} Con el requerimiento actualizado de 5 descargas diarias, el area de 13~m\\textsuperscript{2} \\textbf{cumple} el objetivo en ambos casos. Manteniendo la glucosa a minimo 55\\°C (Caso~B), se reduce el tiempo por descarga y se aumenta el margen termico, siempre dentro del limite maximo de 5 descargas/dia.",
    )

    # Genéricos
    text = replace_exact(text, "5--5 descargas", "5 descargas")
    text = replace_exact(text, "5 a 5 descargas", "5 descargas")
    text = replace_exact(text, "5 descargas/dia", "5 descargas/dia")
    text = replace_exact(text, "5~descargas/dia", "5~descargas/dia")
    text = replace_exact(text, "5 descargas", "5 descargas")
    text = replace_exact(text, "5~descargas", "5~descargas")
    text = replace_exact(text, "5 carrotanques", "5 carrotanques")
    text = replace_exact(text, "5~carrotanques", "5~carrotanques")
    text = replace_exact(text, "5 cargas", "5 cargas")
    text = replace_exact(text, "5~cargas", "5~cargas")

    text = replace_exact(text, "5 descargas/dia", "5 descargas/dia")
    text = replace_exact(text, "5~descargas/dia", "5~descargas/dia")
    text = replace_exact(text, "5 descargas", "5 descargas")
    text = replace_exact(text, "5~descargas", "5~descargas")
    text = replace_exact(text, "5 carrotanques", "5 carrotanques")
    text = replace_exact(text, "5~carrotanques", "5~carrotanques")
    text = replace_exact(text, "5 cargas", "5 cargas")
    text = replace_exact(text, "5~cargas", "5~cargas")
    text = replace_exact(text, "cinco descargas", "cinco descargas")
    text = replace_exact(text, "cinco cargas", "cinco cargas")
    text = replace_exact(text, "cinco carrotanques", "cinco carrotanques")

    text = replace_exact(text, "5 descargas/dia", "5 descargas/dia")
    text = replace_exact(text, "5~descargas/dia", "5~descargas/dia")
    text = replace_exact(text, "5 descargas", "5 descargas")
    text = replace_exact(text, "5~descargas", "5~descargas")
    text = replace_exact(text, "5 carrotanques", "5 carrotanques")
    text = replace_exact(text, "5~carrotanques", "5~carrotanques")
    text = replace_exact(text, "5 cargas", "5 cargas")
    text = replace_exact(text, "5~cargas", "5~cargas")
    text = replace_exact(text, "cinco descargas", "cinco descargas")

    # Porcentajes 140% que ya no aplican
    text = replace_exact(text, "140%", "100%")

    return text


def replace_w2605(text: str) -> str:
    text = text.replace("W2605", "W2605")
    text = text.replace("w2605", "w2605")
    return text


def process_file(path: Path):
    if not path.exists():
        print(f"[SKIP] No existe: {path}")
        return
    text = read_text(path)
    original = text
    text = clean_descargas_latex(text)
    text = replace_w2605(text)
    if text != original:
        write_text(path, text)
        print(f"[OK] {path}")
    else:
        print(f"[NO_CHANGE] {path}")


def main():
    for p in LATEX_FILES:
        process_file(p)


if __name__ == "__main__":
    main()
