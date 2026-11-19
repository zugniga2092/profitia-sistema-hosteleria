"""Comprueba las hojas de Kit de marca (4) y Biblioteca de reseñas (5): calcula las fórmulas de los ejemplos
con un motor de hojas de cálculo y las compara con la misma cuenta hecha aparte en Python.

Necesita: pip install openpyxl formulas
"""
import datetime as dt
import os
import sys

import formulas

import crear_marca as M
import crear_resenas as RS

fallos = 0


def modelo(ruta):
    sol = formulas.ExcelModel().loads(ruta).finish().calculate()
    libro = os.path.basename(ruta)
    return lambda hoja, ref: sol[f"'[{libro}]{hoja}'!{ref}"].value[0, 0]


def mira(nombre, hoja, exp):
    global fallos
    if isinstance(exp, str):
        ok = str(hoja) == exp
    else:
        ok = abs(float(hoja) - exp) < 0.005
    fallos += not ok
    print(f"  {'OK ' if ok else 'MAL'} {nombre:34} hoja={hoja!s:>14}  cuenta aparte={exp!s:>14}")


# ---------- Kit de marca ----------
print("KIT DE MARCA")
d = M.datos_inventados()
val = modelo(os.path.join(M.BASE, "ejemplo", "marca-canales-ejemplo.xlsx"))
total = 0
for j, canal in enumerate(M.CANALES):
    col = chr(ord("B") + j)
    distintos = 0
    for r, dato in enumerate(M.DATOS, start=5):
        ficha, v = d.get((dato, "Ficha de marca (lo correcto)")), d.get((dato, canal))
        exp = "sin revisar" if not v else "IGUAL" if v.strip() == ficha.strip() else "DISTINTO"
        distintos += exp == "DISTINTO"
        if str(val("COMPROBACIÓN", f"{col}{r}")) != exp:
            mira(f"{canal} · {dato}", val("COMPROBACIÓN", f"{col}{r}"), exp)
    mira(f"Distintos en {canal}", val("COMPROBACIÓN", f"{col}{5 + len(M.DATOS)}"), distintos)
    total += distintos
mira("Total de datos que corregir", val("COMPROBACIÓN", f"I{5 + len(M.DATOS)}"), total)

# ---------- Biblioteca de reseñas ----------
print("BIBLIOTECA DE RESEÑAS")
d = RS.datos_inventados()
f = d["resenas"]
val = modelo(os.path.join(RS.BASE, "ejemplo", "resenas-ejemplo.xlsx"))
corte = d["hoy"] - dt.timedelta(days=90)
prob = lambda x: x[6] in ("negativa", "mixta")
mira("Reseñas en total", val("RESUMEN", "B4"), len(f))
mira("Media de estrellas", val("RESUMEN", "B5"), sum(x[2] for x in f) / len(f))
mira("Sin responder", val("RESUMEN", "B6"), sum(x[7] != "sí" for x in f))
mira("Con algún problema", val("RESUMEN", "B7"), sum(prob(x) for x in f))
mira("Recientes", val("RESUMEN", "B8"), sum(x[0] >= corte for x in f))
rec_tot = sum(prob(x) and x[0] >= corte for x in f)
ant_tot = sum(prob(x) and x[0] < corte for x in f)
cuenta = {t: sum(prob(x) and x[4] == t for x in f) for t in RS.TEMAS}
for i, tema in enumerate(RS.TEMAS, start=12):
    n = sum(x[4] == tema for x in f)
    c = cuenta[tema]
    rec = sum(prob(x) and x[4] == tema and x[0] >= corte for x in f)
    mira(f"{tema}: reseñas", val("RESUMEN", f"B{i}"), n)
    mira(f"{tema}: con problema", val("RESUMEN", f"C{i}"), c)
    mira(f"{tema}: problemas recientes", val("RESUMEN", f"E{i}"), rec)
    if c:
        mira(f"{tema}: puesto", val("RESUMEN", f"G{i}"), sum(v > c for v in cuenta.values()) + 1)
        a, b = rec / rec_tot, (c - rec) / ant_tot
        mira(f"{tema}: tendencia", val("RESUMEN", f"H{i}"), "Va a más" if a > b else "Va a menos" if a < b else "Igual")
p0 = 12 + len(RS.TEMAS) - 1 + 5
for i, plat in enumerate(RS.PLATAFORMAS, start=p0):
    de = [x for x in f if x[1] == plat]
    mira(f"{plat}: reseñas", val("RESUMEN", f"B{i}"), len(de))
    if de:
        mira(f"{plat}: media", val("RESUMEN", f"C{i}"), sum(x[2] for x in de) / len(de))
    mira(f"{plat}: sin responder", val("RESUMEN", f"D{i}"), sum(x[7] != "sí" for x in de))

print(f"\n{'TODO CUADRA' if not fallos else str(fallos) + ' DIFERENCIAS'}")
sys.exit(1 if fallos else 0)
