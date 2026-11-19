"""Genera la hoja del Cerebro de costes (herramienta 2).

  python crear_costes.py   -> plantillas/costes.xlsx (vacía) y ejemplo/costes-ejemplo.xlsx

La hoja de ejemplo usa DATOS INVENTADOS (precios, mermas, raciones y ventas de un restaurante que no existe).
Necesita: pip install openpyxl
"""
import datetime as dt
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N_ING, N_ESC, N_PLA = 300, 1500, 200   # filas preparadas en cada pestaña

NEGRITA = Font(bold=True)
CABECERA = PatternFill("solid", fgColor="2B2B2B")
BLANCO = Font(bold=True, color="FFFFFF")
AMARILLO = PatternFill("solid", fgColor="FFF4CC")
GRIS = PatternFill("solid", fgColor="F2F2F2")
VERDE = PatternFill("solid", fgColor="D9F2D9")
ROJO = PatternFill("solid", fgColor="F8D7DA")
NARANJA = PatternFill("solid", fgColor="FFE5B4")
NOTA = Font(italic=True, color="666666")
EUROS, EUROS3, PCT, FECHA = '#,##0.00 "€"', '#,##0.000 "€"', "0.0%", "DD/MM/YYYY"


def cabecera(ws, titulos, anchos, calculadas=()):
    for i, (t, a) in enumerate(zip(titulos, anchos), start=1):
        c = ws.cell(row=1, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        c.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[c.column_letter].width = a
    ws.row_dimensions[1].height = 32
    ws.freeze_panes = "B2"


def crear(ruta, datos=None):
    wb = Workbook()

    # ---------- Ajustes ----------
    aj = wb.active
    aj.title = "Ajustes"
    for col, a in zip("ABC", (46, 20, 74)):
        aj.column_dimensions[col].width = a
    aj["A1"] = "AJUSTES · rellena las celdas amarillas"
    aj["A1"].font = Font(bold=True, size=13)
    filas = [
        ("Nombre del local", datos["nombre"] if datos else None, None, "Como quieras que salga."),
        ("IVA de tus precios de carta", 0.10, PCT, "En restauración suele ser el 10 %. Confírmalo con tu gestor."),
        ("Objetivo de coste de producto por plato", datos["objetivo"] if datos else None, PCT, "El mismo que fijaste en el Panel, o uno por tipo de plato si lo prefieres."),
        ("Avisar si un precio tiene más de (días)", 60, "0", "Los precios más viejos que esto salen marcados como «Precio antiguo»."),
        ("Fecha de hoy", datos["hoy"] if datos else None, FECHA, "Escríbela cada vez que revises la hoja. Sirve para detectar precios antiguos."),
    ]
    for i, (etq, val, fmt, nota) in enumerate(filas, start=2):
        aj.cell(row=i, column=1, value=etq).font = NEGRITA
        c = aj.cell(row=i, column=2, value=val)
        c.fill = AMARILLO
        if fmt:
            c.number_format = fmt
        aj.cell(row=i, column=3, value=nota).font = NOTA
    aj["A8"] = "Los precios de proveedor van SIN IVA. Los precios de carta van CON IVA: la hoja se lo quita sola."
    aj["A8"].font = Font(bold=True, color="B00020")
    aj["A10"] = "Celdas amarillas: las rellenas tú. Celdas grises: se calculan solas, no las toques."
    aj["A10"].font = NOTA

    # ---------- Ingredientes ----------
    ing = wb.create_sheet("Ingredientes")
    cabecera(ing, ["Ingrediente", "Proveedor", "Formato de compra", "Precio del formato (sin IVA)", "Cantidad del formato",
                   "Unidad de uso", "Precio por unidad", "Merma %", "Precio real por unidad", "Fecha del precio", "Aviso", "Notas"],
             [28, 24, 22, 16, 13, 11, 14, 10, 15, 13, 24, 30])
    dv = DataValidation(type="list", formula1='"kg,litro,unidad"', allow_blank=True)
    ing.add_data_validation(dv)
    dv.add(f"F2:F{N_ING}")
    for r in range(2, N_ING + 1):
        ing[f"G{r}"] = f'=IF(OR(D{r}="",E{r}="",E{r}=0),"",D{r}/E{r})'
        ing[f"I{r}"] = f'=IF(G{r}="","",G{r}/(1-H{r}))'
        ing[f"K{r}"] = (f'=IF(A{r}="","",IF(G{r}="","Falta precio o cantidad",IF(H{r}="","Falta medir la merma",'
                        f'IF(J{r}="","Falta la fecha",IF(Ajustes!$B$6-J{r}>Ajustes!$B$5,"Precio antiguo","")))))')
        ing[f"D{r}"].number_format = EUROS
        ing[f"G{r}"].number_format = ing[f"I{r}"].number_format = EUROS
        ing[f"H{r}"].number_format = PCT
        ing[f"J{r}"].number_format = FECHA
        for col in "GIK":
            ing[f"{col}{r}"].fill = GRIS
    ing.conditional_formatting.add(f"K2:K{N_ING}", FormulaRule(formula=['LEN(K2)>0'], fill=NARANJA))

    # ---------- Escandallos ----------
    esc = wb.create_sheet("Escandallos")
    cabecera(esc, ["Plato", "Ingrediente", "Cantidad por ración (ya limpia)", "Unidad", "Precio real por unidad", "Coste", "Notas"],
             [30, 28, 16, 10, 16, 12, 34])
    dv2 = DataValidation(type="list", formula1=f"=Ingredientes!$A$2:$A${N_ING}", allow_blank=True)
    dv2.error, dv2.showErrorMessage = "Ese ingrediente no está en la pestaña Ingredientes. Añádelo allí primero.", True
    esc.add_data_validation(dv2)
    dv2.add(f"B2:B{N_ESC}")
    tabla = f"Ingredientes!$A$2:$I${N_ING}"
    for r in range(2, N_ESC + 1):
        esc[f"D{r}"] = f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{tabla},6,FALSE),""))'
        esc[f"E{r}"] = f'=IF(B{r}="","",IFERROR(VLOOKUP(B{r},{tabla},9,FALSE),"SIN PRECIO"))'
        esc[f"F{r}"] = f'=IF(OR(C{r}="",NOT(ISNUMBER(E{r}))),"",C{r}*E{r})'
        esc[f"C{r}"].number_format = "0.000"
        esc[f"E{r}"].number_format = EUROS
        esc[f"F{r}"].number_format = EUROS3
        for col in "DEF":
            esc[f"{col}{r}"].fill = GRIS
    esc.conditional_formatting.add(f"E2:E{N_ESC}", CellIsRule(operator="equal", formula=['"SIN PRECIO"'], fill=ROJO))

    # ---------- Platos ----------
    pla = wb.create_sheet("Platos", 0)
    cabecera(pla, ["Plato (igual que en Escandallos)", "Precio de carta (con IVA)", "Raciones vendidas al mes", "Precio sin IVA",
                   "Coste de la ración", "Margen por ración", "Coste de producto %", "Estado", "Margen al mes", "Aviso"],
             [34, 14, 14, 13, 13, 13, 13, 11, 14, 34])
    e_plato, e_coste, e_precio = f"Escandallos!$A$2:$A${N_ESC}", f"Escandallos!$F$2:$F${N_ESC}", f"Escandallos!$E$2:$E${N_ESC}"
    for r in range(2, N_PLA + 1):
        pla[f"D{r}"] = f'=IF(B{r}="","",B{r}/(1+Ajustes!$B$3))'
        pla[f"E{r}"] = f'=IF(A{r}="","",SUMIFS({e_coste},{e_plato},A{r}))'
        pla[f"F{r}"] = f'=IF(OR(D{r}="",E{r}=""),"",D{r}-E{r})'
        pla[f"G{r}"] = f'=IF(OR(D{r}="",E{r}=""),"",E{r}/D{r})'
        pla[f"H{r}"] = f'=IF(OR(G{r}="",Ajustes!$B$4=""),"",IF(G{r}<=Ajustes!$B$4,"BIEN","REVISAR"))'
        pla[f"I{r}"] = f'=IF(OR(F{r}="",C{r}=""),"",F{r}*C{r})'
        pla[f"J{r}"] = (f'=IF(A{r}="","",IF(COUNTIFS({e_plato},A{r})=0,"Sin escandallo: revisa que el nombre sea igual",'
                        f'IF(COUNTIFS({e_plato},A{r},{e_precio},"SIN PRECIO")>0,"Hay ingredientes sin precio",'
                        f'IF(B{r}="","Falta el precio de carta",""))))')
        for col, fmt in (("B", EUROS), ("D", EUROS), ("E", EUROS), ("F", EUROS), ("G", PCT), ("I", EUROS), ("C", "#,##0")):
            pla[f"{col}{r}"].number_format = fmt
        for col in "DEFGHIJ":
            pla[f"{col}{r}"].fill = GRIS
    pla.conditional_formatting.add(f"H2:H{N_PLA}", CellIsRule(operator="equal", formula=['"BIEN"'], fill=VERDE))
    pla.conditional_formatting.add(f"H2:H{N_PLA}", CellIsRule(operator="equal", formula=['"REVISAR"'], fill=ROJO))
    pla.conditional_formatting.add(f"J2:J{N_PLA}", FormulaRule(formula=['LEN(J2)>0'], fill=NARANJA))

    if datos:
        for i, f in enumerate(datos["ingredientes"], start=2):
            nombre, prov, formato, precio, cantidad, unidad, merma, fecha, nota = f
            ing[f"A{i}"], ing[f"B{i}"], ing[f"C{i}"], ing[f"D{i}"], ing[f"E{i}"], ing[f"F{i}"] = nombre, prov, formato, precio, cantidad, unidad
            ing[f"H{i}"], ing[f"J{i}"], ing[f"L{i}"] = merma, fecha, nota
        for i, (plato, ingrediente, cantidad) in enumerate(datos["escandallos"], start=2):
            esc[f"A{i}"], esc[f"B{i}"], esc[f"C{i}"] = plato, ingrediente, cantidad
        for i, (plato, precio, raciones) in enumerate(datos["platos"], start=2):
            pla[f"A{i}"], pla[f"B{i}"], pla[f"C{i}"] = plato, precio, raciones

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    wb.save(ruta)
    return ruta


def datos_inventados():
    """Un restaurante que NO existe. Todos los precios, mermas, raciones y ventas son inventados."""
    d = dt.date
    inv = "DATO INVENTADO"
    ingredientes = [
        # nombre, proveedor, formato, precio formato, cantidad, unidad, merma, fecha precio, nota
        ("Lomo de ternera", "Carnes (ejemplo)", "Pieza de 4 kg", 72.00, 4, "kg", 0.20, d(2026, 11, 12), inv),
        ("Secreto ibérico", "Carnes (ejemplo)", "Bandeja de 2 kg", 31.00, 2, "kg", 0.10, d(2026, 11, 12), inv),
        ("Pollo de corral", "Carnes (ejemplo)", "Caja de 6 kg", 39.00, 6, "kg", 0.30, d(2026, 8, 20), inv + " · precio antiguo a propósito"),
        ("Merluza", "Pescados (ejemplo)", "Pieza de 3 kg", 42.00, 3, "kg", 0.45, d(2026, 11, 14), inv),
        ("Gamba roja", "Pescados (ejemplo)", "Caja de 1 kg", 58.00, 1, "kg", 0.50, d(2026, 11, 14), inv),
        ("Arroz bomba", "Distribuidor (ejemplo)", "Saco de 5 kg", 17.50, 5, "kg", 0.00, d(2026, 10, 30), inv),
        ("Patata", "Frutas y verduras (ejemplo)", "Saco de 25 kg", 18.75, 25, "kg", 0.20, d(2026, 11, 10), inv),
        ("Tomate", "Frutas y verduras (ejemplo)", "Caja de 6 kg", 10.80, 6, "kg", 0.10, d(2026, 11, 10), inv),
        ("Lechuga", "Frutas y verduras (ejemplo)", "Caja de 12 unidades", 9.60, 12, "unidad", 0.25, d(2026, 11, 10), inv),
        ("Cebolla", "Frutas y verduras (ejemplo)", "Saco de 10 kg", 9.00, 10, "kg", 0.15, d(2026, 11, 10), inv),
        ("Huevo", "Distribuidor (ejemplo)", "Caja de 180 unidades", 36.00, 180, "unidad", 0.02, d(2026, 11, 5), inv),
        ("Aceite de oliva", "Distribuidor (ejemplo)", "Garrafa de 5 l", 40.00, 5, "litro", 0.00, d(2026, 11, 5), inv),
        ("Nata", "Distribuidor (ejemplo)", "Brik de 1 l", 3.90, 1, "litro", 0.00, d(2026, 11, 5), inv),
        ("Queso curado", "Distribuidor (ejemplo)", "Cuña de 1 kg", 16.00, 1, "kg", 0.08, d(2026, 11, 5), inv),
        ("Chocolate", "Distribuidor (ejemplo)", "Tableta de 1 kg", 11.00, 1, "kg", 0.00, d(2026, 10, 28), inv),
        ("Pan", "Panadería (ejemplo)", "Barra", 0.60, 1, "unidad", 0.00, d(2026, 11, 16), inv),
        ("Caldo de pescado", "Elaboración propia", "Olla de 10 l", 9.00, 10, "litro", None, d(2026, 11, 1), inv + " · merma sin medir a propósito"),
    ]
    escandallos = [
        ("Entrecot a la brasa", "Lomo de ternera", 0.300), ("Entrecot a la brasa", "Patata", 0.200), ("Entrecot a la brasa", "Aceite de oliva", 0.020), ("Entrecot a la brasa", "Pan", 0.25),
        ("Secreto con patatas", "Secreto ibérico", 0.220), ("Secreto con patatas", "Patata", 0.200), ("Secreto con patatas", "Aceite de oliva", 0.020), ("Secreto con patatas", "Pan", 0.25),
        ("Pollo asado", "Pollo de corral", 0.280), ("Pollo asado", "Patata", 0.180), ("Pollo asado", "Cebolla", 0.050), ("Pollo asado", "Aceite de oliva", 0.015), ("Pollo asado", "Pan", 0.25),
        ("Merluza a la plancha", "Merluza", 0.200), ("Merluza a la plancha", "Tomate", 0.080), ("Merluza a la plancha", "Aceite de oliva", 0.020), ("Merluza a la plancha", "Pan", 0.25),
        ("Arroz de gamba roja", "Arroz bomba", 0.100), ("Arroz de gamba roja", "Gamba roja", 0.090), ("Arroz de gamba roja", "Caldo de pescado", 0.350), ("Arroz de gamba roja", "Tomate", 0.050), ("Arroz de gamba roja", "Aceite de oliva", 0.025),
        ("Ensalada de la casa", "Lechuga", 0.50), ("Ensalada de la casa", "Tomate", 0.150), ("Ensalada de la casa", "Cebolla", 0.030), ("Ensalada de la casa", "Queso curado", 0.040), ("Ensalada de la casa", "Aceite de oliva", 0.020),
        ("Tortilla de patata", "Patata", 0.250), ("Tortilla de patata", "Huevo", 3), ("Tortilla de patata", "Cebolla", 0.060), ("Tortilla de patata", "Aceite de oliva", 0.040),
        ("Tarta de chocolate", "Chocolate", 0.060), ("Tarta de chocolate", "Nata", 0.050), ("Tarta de chocolate", "Huevo", 1),
    ]
    platos = [
        ("Entrecot a la brasa", 24.00, 310), ("Secreto con patatas", 17.50, 240), ("Pollo asado", 13.50, 280),
        ("Merluza a la plancha", 18.00, 190), ("Arroz de gamba roja", 19.50, 260), ("Ensalada de la casa", 9.50, 330),
        ("Tortilla de patata", 8.00, 420), ("Tarta de chocolate", 6.50, 300),
    ]
    return {"nombre": "Restaurante de Ejemplo (datos inventados)", "objetivo": 0.30, "hoy": d(2026, 11, 19),
            "ingredientes": ingredientes, "escandallos": escandallos, "platos": platos}


if __name__ == "__main__":
    print(crear(os.path.join(BASE, "plantillas", "costes.xlsx")))
    print(crear(os.path.join(BASE, "ejemplo", "costes-ejemplo.xlsx"), datos_inventados()))
