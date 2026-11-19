"""Genera la hoja del Kit de marca (herramienta 4): comprueba que tus datos son iguales en todos los canales.

  python crear_marca.py   -> plantillas/marca-canales.xlsx (vacía) y ejemplo/marca-canales-ejemplo.xlsx

La hoja de ejemplo usa DATOS INVENTADOS de un restaurante que no existe.
Necesita: pip install openpyxl
"""
import os

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATOS = ["Nombre del local", "Dirección", "Teléfono", "Web", "Enlace de reservas", "Horario lunes", "Horario martes",
         "Horario miércoles", "Horario jueves", "Horario viernes", "Horario sábado", "Horario domingo", "Descripción corta"]
CANALES = ["Google", "Web", "Instagram", "Facebook", "TripAdvisor", "Reservas", "Reparto"]

CABECERA = PatternFill("solid", fgColor="2B2B2B")
BLANCO = Font(bold=True, color="FFFFFF")
AMARILLO = PatternFill("solid", fgColor="FFF4CC")
VERDE_F = PatternFill("solid", fgColor="D9F2D9")
ROJO = PatternFill("solid", fgColor="F8D7DA")
GRIS = PatternFill("solid", fgColor="F2F2F2")
NOTA = Font(italic=True, color="666666")


def crear(ruta, datos=None):
    wb = Workbook()
    fi = wb.active
    fi.title = "Canales"
    fi["A1"] = "LO QUE DICE CADA CANAL · copia aquí, tal cual, lo que aparece en cada sitio"
    fi["A1"].font = Font(bold=True, size=13)
    fi["A2"] = "Columna B: lo correcto, copiado de tu ficha de marca. Resto: lo que pone hoy en cada canal. Deja en blanco lo que no uses."
    fi["A2"].font = NOTA
    titulos = ["Dato", "Ficha de marca (lo correcto)"] + CANALES
    for i, t in enumerate(titulos, start=1):
        c = fi.cell(row=4, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        fi.column_dimensions[get_column_letter(i)].width = 22 if i == 1 else 34 if i == 2 else 26
    for r, dato in enumerate(DATOS, start=5):
        fi.cell(row=r, column=1, value=dato).font = Font(bold=True)
        for c in range(2, len(titulos) + 1):
            celda = fi.cell(row=r, column=c)
            celda.fill = AMARILLO
            celda.alignment = Alignment(wrap_text=True, vertical="top")
            if datos:
                celda.value = datos.get((dato, titulos[c - 1]))
    fi.freeze_panes = "C5"
    ultima = 4 + len(DATOS)

    co = wb.create_sheet("Comprobación", 0)
    co["A1"] = "COMPROBACIÓN · ¿dice lo mismo en todos los canales?"
    co["A1"].font = Font(bold=True, size=13)
    co["A2"] = "Se calcula sola. IGUAL = coincide con la ficha. DISTINTO = corrígelo en ese canal. Compara letra a letra: escribe siempre igual teléfonos y horarios."
    co["A2"].font = NOTA
    for i, t in enumerate(["Dato"] + CANALES + ["Canales distintos"], start=1):
        c = co.cell(row=4, column=i, value=t)
        c.font, c.fill = BLANCO, CABECERA
        co.column_dimensions[get_column_letter(i)].width = 24 if i == 1 else 15
    col_total = get_column_letter(len(CANALES) + 2)
    for r in range(5, ultima + 1):
        co.cell(row=r, column=1, value=f"=Canales!A{r}").font = Font(bold=True)
        for j in range(len(CANALES)):
            origen = get_column_letter(j + 3)
            co.cell(row=r, column=j + 2, value=(
                f'=IF(Canales!{origen}{r}="","sin revisar",IF(Canales!$B{r}="","falta la ficha",'
                f'IF(EXACT(TRIM(Canales!{origen}{r}),TRIM(Canales!$B{r})),"IGUAL","DISTINTO")))')).fill = GRIS
        co[f"{col_total}{r}"] = f'=COUNTIF(B{r}:{get_column_letter(len(CANALES) + 1)}{r},"DISTINTO")'
    fila_tot = ultima + 1
    co.cell(row=fila_tot, column=1, value="Datos distintos en este canal").font = Font(bold=True)
    for j in range(len(CANALES)):
        col = get_column_letter(j + 2)
        co[f"{col}{fila_tot}"] = f'=COUNTIF({col}5:{col}{ultima},"DISTINTO")'
    co[f"{col_total}{fila_tot}"] = f"=SUM({col_total}5:{col_total}{ultima})"
    co[f"A{fila_tot + 2}"] = f'=IF({col_total}{fila_tot}=0,"Todo lo revisado coincide con tu ficha.","Tienes "&{col_total}{fila_tot}&" datos que corregir. Empieza por Google.")'
    co[f"A{fila_tot + 2}"].font = Font(bold=True)
    zona = f"B5:{get_column_letter(len(CANALES) + 1)}{ultima}"
    co.conditional_formatting.add(zona, CellIsRule(operator="equal", formula=['"IGUAL"'], fill=VERDE_F))
    co.conditional_formatting.add(zona, CellIsRule(operator="equal", formula=['"DISTINTO"'], fill=ROJO))
    co.freeze_panes = "B5"

    os.makedirs(os.path.dirname(ruta), exist_ok=True)
    wb.save(ruta)
    return ruta


def datos_inventados():
    """Un restaurante que NO existe. Dirección, teléfono y enlaces son inventados."""
    ficha = {
        "Nombre del local": "Casa de Ejemplo", "Dirección": "Calle Inventada 12, 46000 Valencia", "Teléfono": "960 000 000",
        "Web": "casadeejemplo.example", "Enlace de reservas": "casadeejemplo.example/reservas",
        "Horario lunes": "Cerrado", "Horario martes": "13:00-16:00 y 20:00-23:30", "Horario miércoles": "13:00-16:00 y 20:00-23:30",
        "Horario jueves": "13:00-16:00 y 20:00-23:30", "Horario viernes": "13:00-16:00 y 20:00-00:00",
        "Horario sábado": "13:00-16:00 y 20:00-00:00", "Horario domingo": "13:00-16:30",
        "Descripción corta": "Cocina de brasa y arroces en el centro. Producto de temporada.",
    }
    d = {}
    for dato, valor in ficha.items():
        d[(dato, "Ficha de marca (lo correcto)")] = valor
        for canal in ("Google", "Web", "Instagram", "TripAdvisor"):
            d[(dato, canal)] = valor
    # Fallos puestos a propósito para ver cómo los marca
    d[("Teléfono", "TripAdvisor")] = "961 111 111"
    d[("Horario domingo", "Google")] = "13:00-16:00"
    d[("Nombre del local", "Instagram")] = "Restaurante Casa de Ejemplo"
    d[("Horario lunes", "TripAdvisor")] = "13:00-16:00"
    for dato in ("Horario lunes", "Horario martes", "Horario miércoles", "Horario jueves", "Horario viernes", "Horario sábado", "Horario domingo"):
        d[(dato, "Instagram")] = None   # Instagram no enseña el horario por días: sin revisar
    return d


if __name__ == "__main__":
    print(crear(os.path.join(BASE, "plantillas", "marca-canales.xlsx")))
    print(crear(os.path.join(BASE, "ejemplo", "marca-canales-ejemplo.xlsx"), datos_inventados()))
