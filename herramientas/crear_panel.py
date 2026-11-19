"""Genera la hoja del Panel del restaurante (herramienta 1) con la Revisión de los lunes (herramienta 3).

  python crear_panel.py            -> plantillas/panel.xlsx (vacía) y ejemplo/panel-ejemplo.xlsx

La hoja de ejemplo usa DATOS INVENTADOS de un restaurante que no existe, solo para ver el panel funcionando.
Necesita: pip install openpyxl
"""
import datetime as dt
import os
import random

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILAS = 3000  # filas que leen las fórmulas en cada pestaña de datos

NEGRITA = Font(bold=True)
CABECERA = PatternFill("solid", fgColor="2B2B2B")
BLANCO = Font(bold=True, color="FFFFFF")
GRIS = PatternFill("solid", fgColor="F2F2F2")
AMARILLO = PatternFill("solid", fgColor="FFF4CC")
VERDE = PatternFill("solid", fgColor="D9F2D9")
ROJO = PatternFill("solid", fgColor="F8D7DA")
EUROS = '#,##0.00 "€"'
PCT = "0.0%"
FECHA = "DD/MM/YYYY"


def cabecera(ws, titulos, anchos):
    for i, (t, a) in enumerate(zip(titulos, anchos), start=1):
        c = ws.cell(row=1, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        ws.column_dimensions[c.column_letter].width = a
    ws.freeze_panes = "A2"


def rango(hoja, col):
    return f"{hoja}!${col}$2:${col}${FILAS}"


def suma(hoja, col_valor, desde, hasta, extra=""):
    """SUMIFS entre dos fechas (columna A de la hoja), con un criterio extra opcional."""
    return (f"SUMIFS({rango(hoja, col_valor)},{rango(hoja, 'A')},\">=\"&{desde},"
            f"{rango(hoja, 'A')},\"<=\"&{hasta}{extra})")


def crear(ruta, datos=None):
    wb = Workbook()

    # ---------- Ajustes ----------
    aj = wb.active
    aj.title = "Ajustes"
    aj.column_dimensions["A"].width = 44
    aj.column_dimensions["B"].width = 22
    aj.column_dimensions["C"].width = 70
    aj["A1"] = "AJUSTES · rellena las celdas amarillas"
    aj["A1"].font = Font(bold=True, size=13)
    filas = [
        ("Nombre del local", datos["nombre"] if datos else "", None, "Como quieras que salga en el panel."),
        ("Plazas del local", datos["plazas"] if datos else "", "0", "Número de sillas."),
        ("Objetivo de coste de producto", datos["obj_producto"] if datos else "", PCT, "Lo fijas tú con tus últimos 3 meses. Mira REFERENCIAS.md."),
        ("Objetivo de coste de personal", datos["obj_personal"] if datos else "", PCT, "Igual: tu cifra, no la de otro."),
        ("Objetivo de ticket medio", datos["obj_ticket"] if datos else "", EUROS, "Sin IVA."),
        ("Semana a revisar: su lunes", datos["lunes"] if datos else "", FECHA, "Escribe la fecha del lunes. El panel coge de lunes a domingo."),
        ("Mes a revisar: su día 1", datos["mes_fecha"] if datos else "", FECHA, "Escribe el día 1 del mes. Ejemplo: 01/10/2026."),
    ]
    for i, (etq, val, fmt, nota) in enumerate(filas, start=2):
        aj.cell(row=i, column=1, value=etq).font = NEGRITA
        c = aj.cell(row=i, column=2, value=val if val != "" else None)
        c.fill = AMARILLO
        if fmt:
            c.number_format = fmt
        aj.cell(row=i, column=3, value=nota).font = Font(italic=True, color="666666")
    aj["A10"] = "Todos los importes de todas las pestañas van SIN IVA."
    aj["A10"].font = Font(bold=True, color="B00020")

    # ---------- Ventas ----------
    ve = wb.create_sheet("Ventas")
    cabecera(ve, ["Fecha", "Turno", "Ventas sin IVA", "Comensales", "Tickets", "Notas"], [13, 12, 16, 13, 10, 40])
    # ---------- Compras ----------
    co = wb.create_sheet("Compras")
    cabecera(co, ["Fecha de factura", "Proveedor", "Categoría", "Importe sin IVA", "Nº de factura", "Notas"], [16, 28, 14, 16, 16, 40])
    dv = DataValidation(type="list", formula1='"comida,bebida,otros"', allow_blank=True)
    co.add_data_validation(dv)
    dv.add(f"C2:C{FILAS}")
    # ---------- Mes ----------
    me = wb.create_sheet("Mes")
    cabecera(me, ["Mes (día 1)", "Concepto", "Tipo", "Importe sin IVA", "Notas"], [14, 44, 18, 16, 40])
    dv2 = DataValidation(type="list", formula1='"personal,gasto general"', allow_blank=True)
    me.add_data_validation(dv2)
    dv2.add(f"C2:C{FILAS}")

    if datos:
        for f in datos["ventas"]:
            ve.append(f)
        for f in datos["compras"]:
            co.append(f)
        for f in datos["mes_filas"]:
            me.append(f)
    for ws, col_fecha, col_eur in ((ve, "A", "C"), (co, "A", "D"), (me, "A", "D")):
        for r in range(2, ws.max_row + 1):
            ws[f"{col_fecha}{r}"].number_format = FECHA
            ws[f"{col_eur}{r}"].number_format = EUROS

    # ---------- Panel ----------
    pa = wb.create_sheet("Panel", 0)
    for col, ancho in zip("ABCDEFG", [40, 17, 17, 17, 14, 13, 58]):
        pa.column_dimensions[col].width = ancho
    pa["A1"] = '="PANEL · "&Ajustes!B2'
    pa["A1"].font = Font(bold=True, size=15)
    pa["A2"] = "Importes sin IVA. No escribas en esta pestaña: se calcula sola."
    pa["A2"].font = Font(italic=True, color="666666")
    for i, t in enumerate(["", "Semana", "Semana anterior", "Mes", "Objetivo", "Estado (mes)", "Cómo se calcula"], start=1):
        c = pa.cell(row=4, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        c.alignment = Alignment(horizontal="center")

    pa["A5"], pa["B5"], pa["C5"], pa["D5"] = "Desde", "=Ajustes!B7", "=B5-7", "=Ajustes!B8"
    pa["A6"], pa["B6"], pa["C6"], pa["D6"] = "Hasta", "=B5+6", "=C5+6", "=EOMONTH(D5,0)"
    for celda in ("B5", "C5", "D5", "B6", "C6", "D6"):
        pa[celda].number_format = FECHA

    def personal(desde, mensual):
        mes1 = f"DATE(YEAR({desde}),MONTH({desde}),1)"
        base = f"SUMIFS({rango('Mes', 'D')},{rango('Mes', 'A')},{mes1},{rango('Mes', 'C')},\"personal\")"
        return f"={base}" if mensual else f"={base}*7/DAY(EOMONTH({desde},0))"

    filas_panel = {
        8: ("Ventas", lambda c: f"={suma('Ventas', 'C', c + '5', c + '6')}", EUROS, "Suma de la pestaña Ventas entre las dos fechas."),
        9: ("Comensales", lambda c: f"={suma('Ventas', 'D', c + '5', c + '6')}", "#,##0", "Suma de comensales."),
        10: ("Ticket medio", lambda c: f'=IF({c}9=0,"",{c}8/{c}9)', EUROS, "Ventas ÷ comensales."),
        11: ("Compras de género (comida y bebida)", lambda c: "=" + suma("Compras", "D", c + "5", c + "6", f",{rango('Compras', 'C')},\"comida\"") + "+" + suma("Compras", "D", c + "5", c + "6", f",{rango('Compras', 'C')},\"bebida\""), EUROS, "Facturas de comida y bebida del periodo. Método sencillo: fiable en el mes, orientativo en la semana."),
        12: ("Coste de producto %", lambda c: f'=IF({c}8=0,"",{c}11/{c}8)', PCT, "Compras de género ÷ ventas."),
        13: ("Coste de personal", lambda c: personal(c + "5", c == "D"), EUROS, "Mes: suma de «personal» en la pestaña Mes. Semana: estimación = coste del mes × 7 ÷ días del mes."),
        14: ("Coste de personal %", lambda c: f'=IF({c}8=0,"",{c}13/{c}8)', PCT, "Coste de personal ÷ ventas."),
        15: ("Margen bruto", lambda c: f"={c}8-{c}11", EUROS, "Ventas − compras de género."),
        16: ("Coste principal % (producto + personal)", lambda c: f'=IF({c}8=0,"",({c}11+{c}13)/{c}8)', PCT, "Los dos gastos grandes juntos."),
    }
    for fila, (etq, formula, fmt, nota) in filas_panel.items():
        pa.cell(row=fila, column=1, value=etq).font = NEGRITA
        for col in "BCD":
            pa[f"{col}{fila}"] = formula(col)
            pa[f"{col}{fila}"].number_format = fmt
        pa.cell(row=fila, column=7, value=nota).font = Font(italic=True, color="666666")

    pa["A17"] = "Gastos generales"
    pa["D17"] = f"=SUMIFS({rango('Mes', 'D')},{rango('Mes', 'A')},D5,{rango('Mes', 'C')},\"gasto general\")"
    pa["G17"] = "Suma de «gasto general» en la pestaña Mes. Solo se calcula por mes."
    pa["A18"] = "Resultado de explotación (EBITDA)"
    pa["D18"] = "=D8-D11-D13-D17"
    pa["G18"] = "Ventas − género − personal − gastos generales."
    pa["A19"] = "Resultado sobre ventas %"
    pa["D19"] = '=IF(D8=0,"",D18/D8)'
    pa["G19"] = "Resultado ÷ ventas."
    for f in (17, 18, 19):
        pa[f"A{f}"].font = NEGRITA
        pa[f"D{f}"].number_format = PCT if f == 19 else EUROS
        pa[f"G{f}"].font = Font(italic=True, color="666666")
        for col in "BC":
            pa[f"{col}{f}"].fill = GRIS

    # Objetivos y estado (del mes)
    pa["E10"], pa["E12"], pa["E14"] = "=Ajustes!B6", "=Ajustes!B4", "=Ajustes!B5"
    pa["E10"].number_format, pa["E12"].number_format, pa["E14"].number_format = EUROS, PCT, PCT
    pa["F10"] = '=IF(OR(D10="",E10=""),"",IF(D10>=E10,"BIEN","REVISAR"))'
    pa["F12"] = '=IF(OR(D12="",E12=""),"",IF(D12<=E12,"BIEN","REVISAR"))'
    pa["F14"] = '=IF(OR(D14="",E14=""),"",IF(D14<=E14,"BIEN","REVISAR"))'
    pa.conditional_formatting.add("F8:F19", CellIsRule(operator="equal", formula=['"BIEN"'], fill=VERDE))
    pa.conditional_formatting.add("F8:F19", CellIsRule(operator="equal", formula=['"REVISAR"'], fill=ROJO))
    for f in range(8, 20):
        for col in "BCDEF":
            pa[f"{col}{f}"].alignment = Alignment(horizontal="right")

    pa["A21"] = "Avisos"
    pa["A21"].font = NEGRITA
    pa["A22"] = '=IF(D8=0,"No hay ventas en el mes elegido: revisa la fecha en Ajustes o la pestaña Ventas.","")'
    pa["A23"] = '=IF(AND(D8>0,D13=0),"Falta el coste de personal del mes en la pestaña Mes: el resultado sale mejor de lo que es.","")'
    pa["A24"] = '=IF(AND(D8>0,D11=0),"No hay compras de comida ni bebida en el mes: faltan facturas en la pestaña Compras.","")'
    for f in (22, 23, 24):
        pa[f"A{f}"].font = Font(color="B00020")
    pa.freeze_panes = "B5"

    # ---------- Lunes (herramienta 3: revisión semanal) ----------
    lu = wb.create_sheet("Lunes", 1)
    for col, ancho in zip("ABCDEFG", [40, 16, 16, 12, 13, 16, 44]):
        lu.column_dimensions[col].width = ancho
    lu["A1"] = '="REVISIÓN DE LOS LUNES · "&Ajustes!B2'
    lu["A1"].font = Font(bold=True, size=15)
    lu["A2"] = "Se calcula sola con la semana elegida en Ajustes. Copia la tabla entera y pégala en tu asistente de IA."
    lu["A2"].font = Font(italic=True, color="666666")
    for i, t in enumerate(["", "Esta semana", "Semana anterior", "Cambio", "Objetivo", "Diferencia en €", "Lectura"], start=1):
        c = lu.cell(row=4, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        c.alignment = Alignment(horizontal="center")
    lu["A5"], lu["B5"], lu["C5"] = "Desde", "=Panel!B5", "=Panel!C5"
    lu["A6"], lu["B6"], lu["C6"] = "Hasta", "=Panel!B6", "=Panel!C6"
    for celda in ("B5", "C5", "B6", "C6"):
        lu[celda].number_format = FECHA
    filas_lunes = [(8, "Ventas", 8, EUROS), (9, "Comensales", 9, "#,##0"), (10, "Ticket medio", 10, EUROS),
                   (11, "Coste de producto % (orientativo)", 12, PCT), (12, "Coste de personal % (estimación)", 14, PCT),
                   (13, "Coste principal %", 16, PCT)]
    for fila, etq, fila_panel, fmt in filas_lunes:
        lu.cell(row=fila, column=1, value=etq).font = NEGRITA
        lu[f"B{fila}"], lu[f"C{fila}"] = f"=Panel!B{fila_panel}", f"=Panel!C{fila_panel}"
        lu[f"B{fila}"].number_format = lu[f"C{fila}"].number_format = fmt
        if fila <= 10:
            lu[f"D{fila}"] = f'=IF(OR(B{fila}="",C{fila}="",C{fila}=0),"",B{fila}/C{fila}-1)'
            lu[f"D{fila}"].number_format = "+0.0%;-0.0%"
    lu["A14"] = "Servicios abiertos"
    lu["A15"] = "Rotación (comensales por plaza y servicio)"
    for col in "BC":
        lu[f"{col}14"] = (f'=COUNTIFS({rango("Ventas", "A")},">="&{col}5,{rango("Ventas", "A")},"<="&{col}6,'
                          f'{rango("Ventas", "C")},">0")')
        lu[f"{col}15"] = f'=IF(OR({col}14=0,Ajustes!$B$3="",Ajustes!$B$3=0),"",{col}9/({col}14*Ajustes!$B$3))'
        lu[f"{col}15"].number_format = "0.00"
    lu["A14"].font = lu["A15"].font = NEGRITA
    # Objetivos y diferencia en euros (positivo en costes = dinero gastado de más)
    lu["E10"], lu["E11"], lu["E12"] = "=Ajustes!B6", "=Ajustes!B4", "=Ajustes!B5"
    lu["E10"].number_format, lu["E11"].number_format, lu["E12"].number_format = EUROS, PCT, PCT
    lu["F10"] = '=IF(OR(B10="",E10=""),"",(B10-E10)*B9)'
    lu["F11"] = '=IF(OR(B11="",E11=""),"",(B11-E11)*B8)'
    lu["F12"] = '=IF(OR(B12="",E12=""),"",(B12-E12)*B8)'
    for f in (10, 11, 12):
        lu[f"F{f}"].number_format = '+#,##0.00 "€";-#,##0.00 "€"'
    lu["G10"] = '=IF(F10="","",IF(F10>=0,"Ticket por encima del objetivo","Ingresas menos de lo que marca tu objetivo"))'
    lu["G11"] = '=IF(F11="","",IF(F11>0,"Gastado de más en género","Género dentro del objetivo"))'
    lu["G12"] = '=IF(F12="","",IF(F12>0,"Gastado de más en personal","Personal dentro del objetivo"))'
    lu.conditional_formatting.add("G10:G12", FormulaRule(formula=['OR(LEFT(G10,7)="Gastado",LEFT(G10,8)="Ingresas")'], fill=ROJO))
    lu.conditional_formatting.add("G10:G12", FormulaRule(formula=['OR(ISNUMBER(SEARCH("dentro",G10)),ISNUMBER(SEARCH("encima",G10)))'], fill=VERDE))

    lu["A18"] = "Tendencia de las últimas 4 semanas"
    lu["A18"].font = Font(bold=True, size=12)
    for i, t in enumerate(["Semana (su lunes)", "Ventas", "Comensales", "Ticket medio", "Coste de producto %"], start=1):
        c = lu.cell(row=19, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
    for k, fila in zip((3, 2, 1, 0), (20, 21, 22, 23)):
        lu[f"A{fila}"] = f"=$B$5-{7 * k}"
        lu[f"A{fila}"].number_format = FECHA
        d, h = f"$A{fila}", f"($A{fila}+6)"
        lu[f"B{fila}"] = "=" + suma("Ventas", "C", d, h)
        lu[f"C{fila}"] = "=" + suma("Ventas", "D", d, h)
        lu[f"D{fila}"] = f'=IF(C{fila}=0,"",B{fila}/C{fila})'
        lu[f"E{fila}"] = (f'=IF(B{fila}=0,"",(' + suma("Compras", "D", d, h, f",{rango('Compras', 'C')},\"comida\"") + "+"
                          + suma("Compras", "D", d, h, f",{rango('Compras', 'C')},\"bebida\"") + f")/B{fila})")
        lu[f"B{fila}"].number_format = lu[f"D{fila}"].number_format = EUROS
        lu[f"C{fila}"].number_format, lu[f"E{fila}"].number_format = "#,##0", PCT
    lu["A25"] = "El coste de producto de una semana suelta baila con las compras grandes: mira la tendencia, no un solo dato."
    lu["A26"] = "El coste de personal semanal reparte el coste del mes por días. Para decidir, usa la columna Mes del Panel."
    lu["A25"].font = lu["A26"].font = Font(italic=True, color="666666")

    # ---------- Decisiones ----------
    de = wb.create_sheet("Decisiones")
    cabecera(de, ["Fecha", "Qué vimos", "Qué decidimos", "Responsable", "Para cuándo", "Qué pasó después"], [13, 40, 40, 18, 14, 44])
    if datos and datos.get("decisiones"):
        for f in datos["decisiones"]:
            de.append(f)
        for r in range(2, de.max_row + 1):
            de[f"A{r}"].number_format = de[f"E{r}"].number_format = FECHA

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    wb.save(ruta)
    return ruta


def datos_inventados():
    """Tres meses de un restaurante que NO existe. Cifras al azar con semilla fija."""
    r = random.Random(2026)
    ventas, compras, mes = [], [], []
    d = dt.date(2026, 8, 1)
    while d <= dt.date(2026, 10, 31):
        if d.weekday() != 0:  # cierra los lunes
            fuerte = d.weekday() >= 4
            for turno, base in (("comida", 30), ("cena", 22)):
                comensales = int(base * (1.5 if fuerte else 1) * r.uniform(0.75, 1.2))
                ticket = r.uniform(24, 31) if turno == "cena" else r.uniform(17, 23)
                ventas.append([d, turno, round(comensales * ticket, 2), comensales, max(1, round(comensales / 2.3)), "DATO INVENTADO"])
            if d.weekday() in (1, 3, 5):
                compras.append([d, "Proveedor de comida (ejemplo)", "comida", round(r.uniform(520, 900), 2), f"C-{d:%m%d}", "DATO INVENTADO"])
            if d.weekday() == 2:
                compras.append([d, "Distribuidor de bebidas (ejemplo)", "bebida", round(r.uniform(380, 620), 2), f"B-{d:%m%d}", "DATO INVENTADO"])
            if d.weekday() == 4 and d.day <= 7:
                compras.append([d, "Limpieza y menaje (ejemplo)", "otros", round(r.uniform(120, 220), 2), f"O-{d:%m%d}", "DATO INVENTADO"])
        d += dt.timedelta(days=1)
    for m in (8, 9, 10):
        m1 = dt.date(2026, m, 1)
        mes += [
            [m1, "Sueldos brutos", "personal", 9800.00, "DATO INVENTADO"],
            [m1, "Seguridad social a cargo de la empresa", "personal", 3100.00, "DATO INVENTADO"],
            [m1, "Sueldo del dueño", "personal", 2000.00, "DATO INVENTADO"],
            [m1, "Alquiler", "gasto general", 2400.00, "DATO INVENTADO"],
            [m1, "Luz, gas y agua", "gasto general", round(r.uniform(1100, 1400), 2), "DATO INVENTADO"],
            [m1, "Seguros", "gasto general", 180.00, "DATO INVENTADO"],
            [m1, "Gestoría", "gasto general", 220.00, "DATO INVENTADO"],
            [m1, "Comisiones de tarjetas", "gasto general", round(r.uniform(280, 380), 2), "DATO INVENTADO"],
            [m1, "Mantenimiento y otros", "gasto general", round(r.uniform(200, 600), 2), "DATO INVENTADO"],
        ]
    return {
        "nombre": "Restaurante de Ejemplo (datos inventados)", "plazas": 48,
        "obj_producto": 0.30, "obj_personal": 0.34, "obj_ticket": 23.0,
        "lunes": dt.date(2026, 10, 19), "mes_fecha": dt.date(2026, 10, 1),
        "ventas": ventas, "compras": compras, "mes_filas": mes,
        "decisiones": [[dt.date(2026, 10, 19), "Coste de producto por encima del objetivo dos semanas seguidas",
                        "Pesar la ración del plato más vendido en cada servicio", "Jefe de cocina", dt.date(2026, 10, 25),
                        "DATO INVENTADO · se rellena el lunes siguiente"]],
    }


if __name__ == "__main__":
    print(crear(os.path.join(BASE, "plantillas", "panel.xlsx")))
    print(crear(os.path.join(BASE, "ejemplo", "panel-ejemplo.xlsx"), datos_inventados()))
