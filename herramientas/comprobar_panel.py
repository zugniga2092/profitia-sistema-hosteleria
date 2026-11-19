"""Comprueba el Panel: calcula las fórmulas de la hoja de ejemplo con un motor de hojas de cálculo
y las compara con la misma cuenta hecha aparte en Python.

Necesita: pip install openpyxl formulas
"""
import calendar
import datetime as dt
import os
import sys

import formulas
from openpyxl import load_workbook

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA = os.path.join(BASE, "ejemplo", "panel-ejemplo.xlsx")

# 1) La cuenta aparte, leyendo los datos tal cual
wb = load_workbook(RUTA)
aj = wb["Ajustes"]
lunes, mes1 = aj["B7"].value.date(), aj["B8"].value.date()
fecha = lambda v: v.date() if isinstance(v, dt.datetime) else v
ventas = [(fecha(r[0]), r[2], r[3]) for r in wb["Ventas"].iter_rows(min_row=2, values_only=True) if r[0]]
compras = [(fecha(r[0]), r[2], r[3]) for r in wb["Compras"].iter_rows(min_row=2, values_only=True) if r[0]]
mes = [(fecha(r[0]), r[2], r[3]) for r in wb["Mes"].iter_rows(min_row=2, values_only=True) if r[0]]


def periodo(desde, hasta, mensual):
    v = sum(x[1] for x in ventas if desde <= x[0] <= hasta)
    c = sum(x[2] for x in ventas if desde <= x[0] <= hasta)
    g = sum(x[2] for x in compras if desde <= x[0] <= hasta and x[1] in ("comida", "bebida"))
    m1 = desde.replace(day=1)
    p = sum(x[2] for x in mes if x[0] == m1 and x[1] == "personal")
    if not mensual:
        p = p * 7 / calendar.monthrange(desde.year, desde.month)[1]
    return {8: v, 9: c, 10: v / c, 11: g, 12: g / v, 13: p, 14: p / v, 15: v - g, 16: (g + p) / v}


fin_mes = mes1.replace(day=calendar.monthrange(mes1.year, mes1.month)[1])
esperado = {
    "B": periodo(lunes, lunes + dt.timedelta(days=6), False),
    "C": periodo(lunes - dt.timedelta(days=7), lunes - dt.timedelta(days=1), False),
    "D": periodo(mes1, fin_mes, True),
}
gastos = sum(x[2] for x in mes if x[0] == mes1 and x[1] == "gasto general")
d = esperado["D"]
esperado["D"].update({17: gastos, 18: d[8] - d[11] - d[13] - gastos})
esperado["D"][19] = esperado["D"][18] / d[8]

# 2) Lo que calcula la hoja
modelo = formulas.ExcelModel().loads(RUTA).finish()
sol = modelo.calculate()
libro = os.path.basename(RUTA)


def celda(ref):
    v = sol[f"'[{libro}]PANEL'!{ref}"].value[0, 0]
    return float(v)


fallos = 0
nombres = {8: "Ventas", 9: "Comensales", 10: "Ticket medio", 11: "Compras de género", 12: "Coste de producto %",
           13: "Coste de personal", 14: "Coste de personal %", 15: "Margen bruto", 16: "Coste principal %",
           17: "Gastos generales", 18: "Resultado de explotación", 19: "Resultado sobre ventas %"}
for col, titulo in (("B", "Semana"), ("C", "Semana anterior"), ("D", "Mes")):
    print(f"\n{titulo}")
    for fila, exp in esperado[col].items():
        hoja = celda(f"{col}{fila}")
        ok = abs(hoja - exp) < 0.005
        fallos += not ok
        print(f"  {'OK ' if ok else 'MAL'} {nombres[fila]:28} hoja={hoja:>12.4f}  cuenta aparte={exp:>12.4f}")
# 3) Pestaña Lunes
plazas, obj_prod, obj_pers, obj_ticket = aj["B3"].value, aj["B4"].value, aj["B5"].value, aj["B6"].value
turnos = [(fecha(r[0]), r[2]) for r in wb["Ventas"].iter_rows(min_row=2, values_only=True) if r[0]]


def lunes_val(ref):
    return float(sol[f"'[{libro}]LUNES'!{ref}"].value[0, 0])


b = esperado["B"]
servicios = sum(1 for f, v in turnos if lunes <= f <= lunes + dt.timedelta(days=6) and v > 0)
esperado_lunes = {
    "B14": servicios, "B15": b[9] / (servicios * plazas),
    "D8": b[8] / esperado["C"][8] - 1, "D10": b[10] / esperado["C"][10] - 1,
    "F10": (b[10] - obj_ticket) * b[9], "F11": (b[12] - obj_prod) * b[8], "F12": (b[14] - obj_pers) * b[8],
    "B13": b[16],
}
for k, fila in zip((3, 2, 1, 0), (20, 21, 22, 23)):
    ini = lunes - dt.timedelta(days=7 * k)
    pk = periodo(ini, ini + dt.timedelta(days=6), False)
    esperado_lunes.update({f"B{fila}": pk[8], f"C{fila}": pk[9], f"D{fila}": pk[10], f"E{fila}": pk[12]})
print("\nLunes")
for ref, exp in esperado_lunes.items():
    hoja = lunes_val(ref)
    ok = abs(hoja - exp) < 0.005
    fallos += not ok
    print(f"  {'OK ' if ok else 'MAL'} {ref:5} hoja={hoja:>12.4f}  cuenta aparte={exp:>12.4f}")
print(f"\n{'TODO CUADRA' if not fallos else str(fallos) + ' DIFERENCIAS'}")
sys.exit(1 if fallos else 0)
