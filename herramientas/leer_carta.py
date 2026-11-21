"""Lee una hoja de costes (plantilla o tuya) y saca, plato a plato, el margen y el grupo de la carta.

  python herramientas/leer_carta.py "ruta/a/Costes - mi local.xlsx"

Hace las mismas cuentas que las fórmulas de la hoja, a partir de lo que has escrito (ingredientes,
escandallos, platos y secciones). Así funciona aunque la hoja no se haya abierto nunca en Excel.
Necesita: pip install openpyxl
"""
import sys

from openpyxl import load_workbook


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def leer(ruta):
    wb = load_workbook(ruta, data_only=False)
    iva = num(wb["Ajustes"]["B3"].value) or 0.10
    real = {}
    for fila in wb["Ingredientes"].iter_rows(min_row=2, values_only=True):
        nombre, precio, cantidad, merma = fila[0], num(fila[3]), num(fila[4]), num(fila[7])
        if nombre and precio is not None and cantidad:
            real[str(nombre).strip()] = precio / cantidad / (1 - (merma or 0))
    coste, sin_precio = {}, set()
    for fila in wb["Escandallos"].iter_rows(min_row=2, values_only=True):
        plato, ing, cant = fila[0], fila[1], num(fila[2])
        if not plato or not ing:
            continue
        plato, ing = str(plato).strip(), str(ing).strip()
        if ing not in real:
            sin_precio.add(plato)
            continue
        coste[plato] = coste.get(plato, 0) + (cant or 0) * real[ing]
    secciones = {}
    if "Carta" in wb.sheetnames:
        for r in range(2, wb["Carta"].max_row + 1):
            plato, sec = wb["Platos"][f"A{r}"].value, wb["Carta"][f"B{r}"].value
            if plato:
                secciones[str(plato).strip()] = (str(sec).strip() if sec else "Toda la carta")
    platos = []
    for fila in wb["Platos"].iter_rows(min_row=2, values_only=True):
        nombre, carta, raciones = fila[0], num(fila[1]), num(fila[2])
        if not nombre:
            continue
        nombre = str(nombre).strip()
        sin_iva = carta / (1 + iva) if carta else None
        c = coste.get(nombre)
        margen = sin_iva - c if (sin_iva is not None and c is not None) else None
        aviso = ("Sin escandallo" if c is None and nombre not in sin_precio else
                 "Hay ingredientes sin precio" if nombre in sin_precio else
                 "Falta el precio de carta" if carta is None else "")
        platos.append({"plato": nombre, "seccion": secciones.get(nombre, "Toda la carta"), "precio_carta": carta,
                       "raciones": raciones, "coste": c, "margen": margen,
                       "coste_pct": (c / sin_iva) if (c is not None and sin_iva) else None, "aviso": aviso})
    # Ingeniería de carta (Kasavana y Smith, 1982), por sección
    por_seccion = {}
    for p in platos:
        if p["raciones"] is not None and p["margen"] is not None:
            por_seccion.setdefault(p["seccion"], []).append(p)
    for p in platos:
        grupo = por_seccion.get(p["seccion"], [])
        if p not in grupo:
            p["grupo"] = "Faltan datos"
            continue
        if len(grupo) < 2:
            p["grupo"] = "Sección con un solo plato"
            continue
        total = sum(x["raciones"] for x in grupo)
        medio = sum(x["raciones"] * x["margen"] for x in grupo) / total
        vendido, deja = p["raciones"] / total >= 0.7 / len(grupo), p["margen"] >= medio
        p["grupo"] = ("Estrella" if vendido and deja else "Muy vendido, deja poco" if vendido else
                      "Deja mucho, se vende poco" if deja else "Se vende poco y deja poco")
    return platos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    e = lambda v, f: "" if v is None else f.format(v)
    print("Plato | Sección | Precio carta | Raciones/mes | Coste ración | Margen ración | Coste % | Grupo | Aviso")
    for p in leer(sys.argv[1]):
        print(" | ".join([p["plato"], p["seccion"], e(p["precio_carta"], "{:.2f} €"), e(p["raciones"], "{:.0f}"),
                          e(p["coste"], "{:.2f} €"), e(p["margen"], "{:.2f} €"), e(p["coste_pct"] and p["coste_pct"] * 100, "{:.1f} %"),
                          p["grupo"], p["aviso"]]))
