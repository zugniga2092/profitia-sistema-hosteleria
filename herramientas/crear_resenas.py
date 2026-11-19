"""Genera la hoja de la Biblioteca de reseñas (herramienta 5).

  python crear_resenas.py   -> plantillas/resenas.xlsx (vacía) y ejemplo/resenas-ejemplo.xlsx

La hoja de ejemplo usa RESEÑAS INVENTADAS de un restaurante que no existe.
Necesita: pip install openpyxl
"""
import datetime as dt
import os
import random

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 3000
TEMAS = ["comida", "servicio", "tiempo de espera", "precio", "ambiente y ruido", "limpieza", "reservas", "reparto", "otros"]
PLATAFORMAS = ["Google", "TripAdvisor", "Reservas", "Reparto", "Redes", "Otras"]

CABECERA = PatternFill("solid", fgColor="2B2B2B")
BLANCO = Font(bold=True, color="FFFFFF")
AMARILLO = PatternFill("solid", fgColor="FFF4CC")
ROJO = PatternFill("solid", fgColor="F8D7DA")
VERDE = PatternFill("solid", fgColor="D9F2D9")
NOTA = Font(italic=True, color="666666")
NEGRITA = Font(bold=True)
FECHA, PCT = "DD/MM/YYYY", "0%"
R = lambda col: f"Reseñas!${col}$2:${col}${N}"


def cabecera(ws, fila, titulos, anchos=None):
    for i, t in enumerate(titulos, start=1):
        c = ws.cell(row=fila, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        c.alignment = Alignment(wrap_text=True, vertical="center")
        if anchos:
            ws.column_dimensions[c.column_letter].width = anchos[i - 1]


def crear(ruta, datos=None):
    wb = Workbook()
    aj = wb.active
    aj.title = "Ajustes"
    for col, a in zip("ABC", (44, 18, 70)):
        aj.column_dimensions[col].width = a
    aj["A1"] = "AJUSTES · rellena las celdas amarillas"
    aj["A1"].font = Font(bold=True, size=13)
    for i, (etq, val, fmt, nota) in enumerate([
        ("Nombre del local", datos["nombre"] if datos else None, None, ""),
        ("Fecha de hoy", datos["hoy"] if datos else None, FECHA, "Escríbela cada vez que revises la hoja."),
        ("«Reciente» significa los últimos (días)", 90, "0", "Sirve para ver si un problema va a más."),
    ], start=2):
        aj.cell(row=i, column=1, value=etq).font = NEGRITA
        c = aj.cell(row=i, column=2, value=val)
        c.fill = AMARILLO
        if fmt:
            c.number_format = fmt
        aj.cell(row=i, column=3, value=nota).font = NOTA
    aj["A6"] = "No copies el nombre de quien escribe la reseña: no hace falta."
    aj["A6"].font = Font(bold=True, color="B00020")

    re = wb.create_sheet("Reseñas")
    cabecera(re, 1, ["Fecha", "Plataforma", "Estrellas", "Texto (copiado tal cual)", "Tema principal", "Tema secundario",
                     "Sentimiento", "Respondida", "Acción"], [13, 14, 10, 70, 18, 18, 13, 12, 36])
    re.freeze_panes = "A2"
    for lista, cols in ((",".join(PLATAFORMAS), "B"), (",".join(TEMAS), "EF"), ("positiva,negativa,mixta", "G"), ("sí,no", "H"),
                        ("1,2,3,4,5", "C")):
        dv = DataValidation(type="list", formula1=f'"{lista}"', allow_blank=True)
        re.add_data_validation(dv)
        for col in cols:
            dv.add(f"{col}2:{col}{N}")
    if datos:
        for f in datos["resenas"]:
            re.append(f)
        for r in range(2, re.max_row + 1):
            re[f"A{r}"].number_format = FECHA
            re[f"D{r}"].alignment = Alignment(wrap_text=True, vertical="top")

    rs = wb.create_sheet("Resumen", 0)
    for col, a in zip("ABCDEFGH", (30, 13, 16, 14, 16, 16, 12, 22)):
        rs.column_dimensions[col].width = a
    rs["A1"] = '="BIBLIOTECA DE RESEÑAS · "&Ajustes!B2'
    rs["A1"].font = Font(bold=True, size=15)
    rs["A2"] = "Se calcula sola con la pestaña Reseñas."
    rs["A2"].font = NOTA
    generales = [
        ("Reseñas en total", f'=COUNTA({R("A")})', "#,##0"),
        ("Media de estrellas", f'=IF(COUNT({R("C")})=0,"",SUM({R("C")})/COUNT({R("C")}))', "0.00"),
        ("Sin responder", f'=B4-COUNTIFS({R("H")},"sí")', "#,##0"),
        ("Con algún problema (negativas o mixtas)", f'=COUNTIFS({R("G")},"negativa")+COUNTIFS({R("G")},"mixta")', "#,##0"),
        ("Recientes (desde la fecha de corte)", f'=COUNTIFS({R("A")},">="&B9)', "#,##0"),
        ("Fecha de corte de «reciente»", "=Ajustes!B3-Ajustes!B4", FECHA),
    ]
    for i, (etq, formula, fmt) in enumerate(generales, start=4):
        rs.cell(row=i, column=1, value=etq).font = NEGRITA
        rs[f"B{i}"] = formula
        rs[f"B{i}"].number_format = fmt

    cabecera(rs, 11, ["Tema", "Reseñas", "Con problema", "% con problema", "Problemas recientes", "Problemas anteriores", "Puesto", "Tendencia"])
    f0, f1 = 12, 12 + len(TEMAS) - 1
    for i, tema in enumerate(TEMAS, start=f0):
        rs.cell(row=i, column=1, value=tema).font = NEGRITA
        prob = lambda extra="": (f'COUNTIFS({R("E")},$A{i},{R("G")},"negativa"{extra})+COUNTIFS({R("E")},$A{i},{R("G")},"mixta"{extra})')
        rs[f"B{i}"] = f'=COUNTIFS({R("E")},$A{i})'
        rs[f"C{i}"] = "=" + prob()
        rs[f"D{i}"] = f'=IF(B{i}=0,"",C{i}/B{i})'
        rs[f"E{i}"] = "=" + prob(f',{R("A")},">="&$B$9')
        rs[f"F{i}"] = f"=C{i}-E{i}"
        rs[f"G{i}"] = f'=IF(C{i}=0,"",COUNTIF($C${f0}:$C${f1},">"&C{i})+1)'
        rs[f"H{i}"] = (f'=IF(C{i}=0,"",IF(OR($E${f1 + 1}=0,$F${f1 + 1}=0),"faltan datos",'
                       f'IF(E{i}/$E${f1 + 1}>F{i}/$F${f1 + 1},"Va a más",IF(E{i}/$E${f1 + 1}<F{i}/$F${f1 + 1},"Va a menos","Igual"))))')
        rs[f"D{i}"].number_format = PCT
    rs.cell(row=f1 + 1, column=1, value="Total").font = NEGRITA
    for col in "BCEF":
        rs[f"{col}{f1 + 1}"] = f"=SUM({col}{f0}:{col}{f1})"
    rs.conditional_formatting.add(f"H{f0}:H{f1}", CellIsRule(operator="equal", formula=['"Va a más"'], fill=ROJO))
    rs.conditional_formatting.add(f"H{f0}:H{f1}", CellIsRule(operator="equal", formula=['"Va a menos"'], fill=VERDE))
    rs.conditional_formatting.add(f"G{f0}:G{f1}", CellIsRule(operator="lessThanOrEqual", formula=["3"], fill=ROJO))
    rs[f"A{f1 + 2}"] = "Puesto 1, 2 y 3 = tus tres problemas principales. «Va a más» = pesa más en los problemas recientes que en los anteriores."
    rs[f"A{f1 + 2}"].font = NOTA

    p0 = f1 + 5
    cabecera(rs, p0 - 1, ["Plataforma", "Reseñas", "Media de estrellas", "Sin responder"])
    for i, plat in enumerate(PLATAFORMAS, start=p0):
        rs.cell(row=i, column=1, value=plat).font = NEGRITA
        rs[f"B{i}"] = f'=COUNTIFS({R("B")},$A{i})'
        rs[f"C{i}"] = f'=IF(B{i}=0,"",SUMIFS({R("C")},{R("B")},$A{i})/B{i})'
        rs[f"D{i}"] = f'=B{i}-COUNTIFS({R("B")},$A{i},{R("H")},"sí")'
        rs[f"C{i}"].number_format = "0.00"

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    wb.save(ruta)
    return ruta


def datos_inventados():
    """Reseñas INVENTADAS de un restaurante que no existe (semilla fija)."""
    r = random.Random(11)
    textos = {
        ("comida", "positiva"): ["El arroz estaba en su punto y la carne muy tierna.", "Producto muy bueno, se nota la brasa.", "La tarta de chocolate, de lo mejor de la noche."],
        ("comida", "negativa"): ["El pescado llegó frío a la mesa.", "La ración de carne nos pareció escasa para el precio."],
        ("servicio", "positiva"): ["Nos atendieron con mucha amabilidad y nos aconsejaron bien.", "El camarero estuvo muy atento toda la cena."],
        ("servicio", "negativa"): ["Tuvimos que pedir la carta tres veces.", "Nadie nos preguntó si queríamos postre."],
        ("tiempo de espera", "negativa"): ["Esperamos 40 minutos entre el primero y el segundo.", "Con reserva y aun así tardaron media hora en sentarnos.", "La comida estaba buena pero tardó muchísimo en salir.", "Un sábado por la noche la espera se hace eterna."],
        ("tiempo de espera", "mixta"): ["Todo rico, aunque tardaron bastante en servirnos.", "Buen sitio, pero ve con tiempo porque van lentos."],
        ("precio", "negativa"): ["Algo caro para lo que es.", "La cuenta subió más de lo esperado por las bebidas."],
        ("precio", "positiva"): ["Buena relación entre calidad y precio."],
        ("ambiente y ruido", "mixta"): ["Local bonito, pero con mucho ruido cuando se llena.", "Se come bien, aunque cuesta hablar por el ruido."],
        ("ambiente y ruido", "positiva"): ["El local es acogedor y la terraza muy agradable."],
        ("limpieza", "positiva"): ["Todo muy limpio, incluidos los baños."],
        ("reservas", "negativa"): ["Llamé dos veces para reservar y no cogieron el teléfono."],
        ("reparto", "negativa"): ["El pedido llegó incompleto, faltaba la guarnición."],
        ("otros", "positiva"): ["Fuimos por un cumpleaños y salimos encantados."],
    }
    estrellas = {"positiva": (4, 5), "mixta": (3, 4), "negativa": (1, 2)}
    filas = []
    hoy = dt.date(2026, 11, 19)
    for i in range(46):
        dias = r.randint(2, 280)
        reciente = dias <= 90
        claves = list(textos)
        pesos = [(4 if k[0] == "tiempo de espera" and reciente else 1.5 if k[1] == "positiva" else 1) for k in claves]
        tema, sent = r.choices(claves, weights=pesos)[0]
        plat = r.choices(PLATAFORMAS[:5], weights=[10, 4, 3, 2, 1])[0] if tema != "reparto" else "Reparto"
        secundario = "servicio" if tema == "tiempo de espera" and r.random() < 0.4 else None
        respondida = "sí" if dias > 60 and r.random() < 0.7 else "no"
        filas.append([hoy - dt.timedelta(days=dias), plat, r.randint(*estrellas[sent]), "RESEÑA INVENTADA · " + r.choice(textos[(tema, sent)]),
                      tema, secundario, sent, respondida, None])
    filas.sort(key=lambda f: f[0], reverse=True)
    return {"nombre": "Restaurante de Ejemplo (datos inventados)", "hoy": hoy, "resenas": filas}


if __name__ == "__main__":
    print(crear(os.path.join(BASE, "plantillas", "resenas.xlsx")))
    print(crear(os.path.join(BASE, "ejemplo", "resenas-ejemplo.xlsx"), datos_inventados()))
