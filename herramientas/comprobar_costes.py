"""Comprueba el Cerebro de costes: calcula las fórmulas de la hoja de ejemplo con un motor de hojas
de cálculo y las compara con la misma cuenta hecha aparte en Python.

Necesita: pip install openpyxl formulas
"""
import os
import sys

import formulas

from crear_costes import BASE, datos_inventados

RUTA = os.path.join(BASE, "ejemplo", "costes-ejemplo.xlsx")
d = datos_inventados()
IVA, OBJ, DIAS = 0.10, d["objetivo"], 60

# 1) La cuenta aparte
real, aviso_ing = {}, {}
for nombre, _p, _f, precio, cantidad, _u, merma, fecha, _n in d["ingredientes"]:
    real[nombre] = precio / cantidad / (1 - (merma or 0))
    aviso_ing[nombre] = ("Falta medir la merma" if merma is None else
                         "Precio antiguo" if (d["hoy"] - fecha).days > DIAS else "")
esperado = {}
for plato, carta, raciones in d["platos"]:
    coste = sum(c * real[i] for p, i, c in d["escandallos"] if p == plato)
    sin_iva = carta / (1 + IVA)
    esperado[plato] = {"D": sin_iva, "E": coste, "F": sin_iva - coste, "G": coste / sin_iva,
                       "H": "BIEN" if coste / sin_iva <= OBJ else "REVISAR", "I": (sin_iva - coste) * raciones}

# 2) Lo que calcula la hoja
sol = formulas.ExcelModel().loads(RUTA).finish().calculate()
libro = os.path.basename(RUTA)
val = lambda hoja, ref: sol[f"'[{libro}]{hoja}'!{ref}"].value[0, 0]

fallos = 0
print("PLATOS")
for i, (plato, _c, _r) in enumerate(d["platos"], start=2):
    e = esperado[plato]
    ok = all(abs(float(val("PLATOS", f"{c}{i}")) - e[c]) < 0.005 for c in "DEFGI") and val("PLATOS", f"H{i}") == e["H"] \
        and str(val("PLATOS", f"J{i}")) == ""
    fallos += not ok
    print(f"  {'OK ' if ok else 'MAL'} {plato:24} coste={e['E']:6.2f}  margen={e['F']:6.2f}  coste%={e['G'] * 100:5.1f}  {e['H']:8} margen/mes={e['I']:9.2f}")
print("AVISOS DE INGREDIENTES")
for i, f in enumerate(d["ingredientes"], start=2):
    hoja = str(val("INGREDIENTES", f"K{i}"))
    ok = hoja == aviso_ing[f[0]]
    fallos += not ok
    if hoja or not ok:
        print(f"  {'OK ' if ok else 'MAL'} {f[0]:24} hoja=«{hoja}»  esperado=«{aviso_ing[f[0]]}»")
print("CARTA (ingeniería de carta por sección)")
grupos = {}
for plato, _c, raciones in d["platos"]:
    grupos.setdefault(d["secciones"].get(plato) or "Toda la carta", []).append((plato, raciones, esperado[plato]["F"]))
grupo_esperado = {}
for seccion, items in grupos.items():
    total, n = sum(r for _p, r, _m in items), len(items)
    medio = sum(r * m for _p, r, m in items) / total
    for plato, r, m in items:
        if n < 2:
            grupo_esperado[plato] = "Sección con un solo plato"
            continue
        vendido, deja = r / total >= 0.7 / n, m >= medio
        grupo_esperado[plato] = ("Estrella" if vendido and deja else "Muy vendido, deja poco" if vendido else
                                 "Deja mucho, se vende poco" if deja else "Se vende poco y deja poco")
for i, (plato, _c, _r) in enumerate(d["platos"], start=2):
    hoja = str(val("CARTA", f"K{i}"))
    ok = hoja == grupo_esperado[plato]
    fallos += not ok
    print(f"  {'OK ' if ok else 'MAL'} {plato:24} {(d['secciones'].get(plato) or ''):12} hoja=«{hoja}»  esperado=«{grupo_esperado[plato]}»")
print(f"\n{'TODO CUADRA' if not fallos else str(fallos) + ' DIFERENCIAS'}")
sys.exit(1 if fallos else 0)
