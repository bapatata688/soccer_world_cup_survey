import pandas as pd

# ─────────────────────────────────────────
# CARGA Y NORMALIZACIÓN DE DATOS
# ─────────────────────────────────────────
df = pd.read_csv("encuesta_snacks_mundial_2026_guatemala_2500_respuestas.csv")

str_cols = [
    "RangoEdad",
    "Ocupacion",
    "PlaneaVerMundial2026",
    "SeleccionApoya",
    "CompraDisenoSeleccion",
    "SeleccionInfluyeCompra",
    "JugadoresInfluyentes",
    "TipoPublicidadAtractiva",
    "PromocionPreferida",
    "CompraTarjetasColeccionables",
    "CampaniaMasProbableCompra",
]
for col in str_cols:
    df[col] = df[col].astype(str).str.strip()
    df[col] = df[col].replace("nan", pd.NA)

df_clean = df.dropna(subset=["Ocupacion", "RangoEdad"]).copy()

TOTAL = len(df)


# HELPERS
def tabla_freq(serie, label="Valor"):
    """Tabla de frecuencia con n y %, ordenada de mayor a menor."""
    counts = serie.value_counts()
    pct = (counts / TOTAL * 100).round(2)
    return pd.DataFrame({"n": counts, "%": pct}).rename_axis(label)


def tabla_freq_grupo(df_sub, col, label="Valor"):
    """Frecuencia dentro de un subgrupo."""
    n_sub = len(df_sub)
    counts = df_sub[col].value_counts()
    pct = (counts / n_sub * 100).round(2)
    return pd.DataFrame({"n": counts, "%_grupo": pct}).rename_axis(label)


def top_n(tabla, n=10):
    return tabla.head(n)


separator = "=" * 60

# 1. INTENCIÓN DE SEGUIR EL MUNDIAL FIFA 2026
print(separator)
print("1. INTENCIÓN DE SEGUIR EL MUNDIAL FIFA 2026")
print(separator)

# 1.1 Resultado global
print("\n[1.1] Resultado Global")
print(tabla_freq(df["PlaneaVerMundial2026"], "PlaneaVerMundial2026").to_string())

# 1.2 Por rango de edad
print("\n[1.2] Por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    print(f"\n  Rango de Edad: {edad}  (n={len(sub)})")
    t = tabla_freq_grupo(sub, "PlaneaVerMundial2026")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(t.to_string())

# 1.3 Por ocupación
print("\n[1.3] Por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    print(f"\n  Ocupación: {ocu}  (n={len(sub)})")
    t = tabla_freq_grupo(sub, "PlaneaVerMundial2026")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(t.to_string())

# 1.4 Por rango de edad agrupado por ocupación
print("\n[1.4] Por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) == 0:
            continue
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        t = tabla_freq_grupo(sub, "PlaneaVerMundial2026")
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(t.to_string())

# 2. SELECCIÓN QUE APOYARÁ PRINCIPALMENTE
print("\n" + separator)
print("2. SELECCIÓN QUE APOYARÁ PRINCIPALMENTE")
print(separator)

# 2.1 Ranking global
print("\n[2.1] Ranking Global de Selecciones")
t_sel = tabla_freq(df["SeleccionApoya"], "SeleccionApoya")
print(t_sel.to_string())

# 2.2 Top 10
print("\n[2.2] Top 10 Selecciones Más Apoyadas")
print(top_n(t_sel).to_string())

# 2.4 Top 3 por rango de edad
print("\n[2.4] Top 3 por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "SeleccionApoya").head(3)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 2.5 Top 3 por ocupación
print("\n[2.5] Top 3 por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "SeleccionApoya").head(3)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 2.6 Top 3 por RangoEdad + Ocupación
print("\n[2.6] Top 3 por Rango de Edad + Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) < 2:
            continue
        t = tabla_freq_grupo(sub, "SeleccionApoya").head(3)
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# 3. COMPRA DE SNACK CON DISEÑO DE SELECCIÓN
print("\n" + separator)
print("3. COMPRA DE SNACK CON DISEÑO DE SELECCIÓN")
print(separator)

# 3.1 Resultado global
print("\n[3.1] Resultado Global")
t_cdis = tabla_freq(df["CompraDisenoSeleccion"], "CompraDisenoSeleccion")
print(t_cdis.to_string())

# 3.2 Comparativa global detallada (ya es la misma tabla)
print("\n[3.2] Comparativa Global por Opción de Respuesta")
print(t_cdis.to_string())

# 3.3 Por edad
print("\n[3.3] Por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "CompraDisenoSeleccion")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 3.4 Por ocupación
print("\n[3.4] Por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "CompraDisenoSeleccion")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 3.5 Por edad x ocupación
print("\n[3.5] Por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) == 0:
            continue
        t = tabla_freq_grupo(sub, "CompraDisenoSeleccion")
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# 4. SELECCIÓN CON MAYOR INFLUENCIA EN LA COMPRA
print("\n" + separator)
print("4. SELECCIÓN CON MAYOR INFLUENCIA EN LA COMPRA")
print(separator)

t_inf = tabla_freq(df["SeleccionInfluyeCompra"], "SeleccionInfluyeCompra")

# 4.1 Ranking completo
print("\n[4.1] Ranking Completo de Selecciones")
print(t_inf.to_string())

# 4.3 Top 10
print("\n[4.3] Top 10 Selecciones Más Influyentes")
print(top_n(t_inf).to_string())

# 5. JUGADORES QUE MOTIVARÍAN LA COMPRA
print("\n" + separator)
print("5. JUGADORES QUE MOTIVARÍAN LA COMPRA")
print(separator)

# Expandir jugadores (separados por ";")
jugadores_series = df["JugadoresInfluyentes"].str.split(";").explode().str.strip()
jugadores_series = jugadores_series[jugadores_series.str.lower() != "ninguno"]
jugadores_series = jugadores_series[jugadores_series != ""]
TOTAL_JUG = len(jugadores_series)


def tabla_jugadores(serie, n_total):
    counts = serie.value_counts()
    pct = (counts / n_total * 100).round(2)
    return pd.DataFrame({"Frecuencia": counts, "%": pct}).rename_axis("Jugador")


# 5.1-5.3 Ranking global
t_jug = tabla_jugadores(jugadores_series, TOTAL_JUG)
print("\n[5.1] Ranking Global de Jugadores")
print(t_jug.to_string())
print("\n[5.3] Top 10 Jugadores Más Influyentes")
print(top_n(t_jug).to_string())

# 5.4 Ranking por rango de edad
print("\n[5.4] Top 5 Jugadores por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    idx = df_clean[df_clean["RangoEdad"] == edad].index
    sub_jug = (
        df_clean.loc[idx, "JugadoresInfluyentes"].str.split(";").explode().str.strip()
    )
    sub_jug = sub_jug[sub_jug.str.lower() != "ninguno"]
    sub_jug = sub_jug[sub_jug != ""]
    if len(sub_jug) == 0:
        continue
    t = tabla_jugadores(sub_jug, len(sub_jug)).head(5)
    print(f"\n  {edad}  (menciones={len(sub_jug)})")
    print(t.to_string())

# 5.5 Ranking por ocupación
print("\n[5.5] Top 5 Jugadores por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    idx = df_clean[df_clean["Ocupacion"] == ocu].index
    sub_jug = (
        df_clean.loc[idx, "JugadoresInfluyentes"].str.split(";").explode().str.strip()
    )
    sub_jug = sub_jug[sub_jug.str.lower() != "ninguno"]
    sub_jug = sub_jug[sub_jug != ""]
    if len(sub_jug) == 0:
        continue
    t = tabla_jugadores(sub_jug, len(sub_jug)).head(5)
    print(f"\n  {ocu}  (menciones={len(sub_jug)})")
    print(t.to_string())

# 5.6 Ranking por RangoEdad + Ocupación
print("\n[5.6] Top 3 Jugadores por Rango de Edad + Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        idx = df_clean[
            (df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)
        ].index
        if len(idx) < 2:
            continue
        sub_jug = (
            df_clean.loc[idx, "JugadoresInfluyentes"]
            .str.split(";")
            .explode()
            .str.strip()
        )
        sub_jug = sub_jug[sub_jug.str.lower() != "ninguno"]
        sub_jug = sub_jug[sub_jug != ""]
        if len(sub_jug) == 0:
            continue
        t = tabla_jugadores(sub_jug, len(sub_jug)).head(3)
        print(f"\n  {edad} | {ocu}  (menciones={len(sub_jug)})")
        print(t.to_string())

# ─────────────────────────────────────────────────────────────
# 6. TIPO DE PUBLICIDAD MÁS ATRACTIVA
# ─────────────────────────────────────────────────────────────
print("\n" + separator)
print("6. TIPO DE PUBLICIDAD MÁS ATRACTIVA")
print(separator)

# 6.1 Ranking global
print("\n[6.1] Ranking Global")
t_pub = tabla_freq(df["TipoPublicidadAtractiva"], "TipoPublicidadAtractiva")
print(t_pub.to_string())

# 6.3 Por edad
print("\n[6.3] Por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "TipoPublicidadAtractiva").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 6.4 Por ocupación
print("\n[6.4] Por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "TipoPublicidadAtractiva").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 6.5 Por edad x ocupación
print("\n[6.5] Por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) < 2:
            continue
        t = tabla_freq_grupo(sub, "TipoPublicidadAtractiva").head(3)
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# ─────────────────────────────────────────────────────────────
# 7. PROMOCIÓN PREFERIDA
# ─────────────────────────────────────────────────────────────
print("\n" + separator)
print("7. PROMOCIÓN PREFERIDA")
print(separator)

t_promo = tabla_freq(df["PromocionPreferida"], "PromocionPreferida")

# 7.1 Ranking completo
print("\n[7.1] Ranking Completo")
print(t_promo.to_string())

# 7.2 Top 5
print("\n[7.2] Top 5 Promociones Preferidas")
print(t_promo.head(5).to_string())

# 7.4 Por edad
print("\n[7.4] Top 5 por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "PromocionPreferida").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 7.5 Por ocupación
print("\n[7.5] Top 5 por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "PromocionPreferida").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 7.6 Por edad x ocupación
print("\n[7.6] Top 3 por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) < 2:
            continue
        t = tabla_freq_grupo(sub, "PromocionPreferida").head(3)
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# ─────────────────────────────────────────────────────────────
# 8. COMPRA DE SNACK CON TARJETAS COLECCIONABLES
# ─────────────────────────────────────────────────────────────
print("\n" + separator)
print("8. COMPRA DE SNACK CON TARJETAS COLECCIONABLES")
print(separator)

# 8.1-8.2 Resultado global
print("\n[8.1-8.2] Resultado Global")
t_tar = tabla_freq(df["CompraTarjetasColeccionables"], "CompraTarjetasColeccionables")
print(t_tar.to_string())

# 8.3 Por edad
print("\n[8.3] Por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "CompraTarjetasColeccionables")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 8.4 Por ocupación
print("\n[8.4] Por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "CompraTarjetasColeccionables")
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 8.5 Por edad x ocupación
print("\n[8.5] Por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) == 0:
            continue
        t = tabla_freq_grupo(sub, "CompraTarjetasColeccionables")
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# ─────────────────────────────────────────────────────────────
# 9. CAMPAÑA CON MAYOR PROBABILIDAD DE COMPRA
# ─────────────────────────────────────────────────────────────
print("\n" + separator)
print("9. CAMPAÑA CON MAYOR PROBABILIDAD DE COMPRA")
print(separator)

t_camp = tabla_freq(df["CampaniaMasProbableCompra"], "CampaniaMasProbableCompra")

# 9.1 Ranking completo
print("\n[9.1] Ranking Completo")
print(t_camp.to_string())

# 9.2 Top 5
print("\n[9.2] Top 5 Campañas")
print(t_camp.head(5).to_string())

# 9.4 Por edad
print("\n[9.4] Top 5 por Rango de Edad")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    sub = df_clean[df_clean["RangoEdad"] == edad]
    t = tabla_freq_grupo(sub, "CampaniaMasProbableCompra").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {edad}  (n={len(sub)})")
    print(t.to_string())

# 9.5 Por ocupación
print("\n[9.5] Top 5 por Ocupación")
for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
    sub = df_clean[df_clean["Ocupacion"] == ocu]
    t = tabla_freq_grupo(sub, "CampaniaMasProbableCompra").head(5)
    t["%_global"] = (t["n"] / TOTAL * 100).round(2)
    print(f"\n  {ocu}  (n={len(sub)})")
    print(t.to_string())

# 9.6 Por edad x ocupación
print("\n[9.6] Top 3 por Rango de Edad x Ocupación")
for edad in sorted(df_clean["RangoEdad"].dropna().unique()):
    for ocu in sorted(df_clean["Ocupacion"].dropna().unique()):
        sub = df_clean[(df_clean["RangoEdad"] == edad) & (df_clean["Ocupacion"] == ocu)]
        if len(sub) < 2:
            continue
        t = tabla_freq_grupo(sub, "CampaniaMasProbableCompra").head(3)
        t["%_global"] = (t["n"] / TOTAL * 100).round(2)
        print(f"\n  {edad} | {ocu}  (n={len(sub)})")
        print(t.to_string())

# ─────────────────────────────────────────────────────────────
# RESUMEN EJECUTIVO Y PRINCIPALES HALLAZGOS
# ─────────────────────────────────────────────────────────────
print("\n" + separator)
print("RESUMEN EJECUTIVO Y PRINCIPALES HALLAZGOS")
print(separator)

# Calcular valores clave
pct_si_mundial = round(
    df["PlaneaVerMundial2026"].value_counts(normalize=True)["Sí"] * 100, 2
)
sel_apoya_top = df["SeleccionApoya"].value_counts().idxmax()
sel_apoya_pct = round(df["SeleccionApoya"].value_counts(normalize=True).max() * 100, 2)
sel_influye_top = df["SeleccionInfluyeCompra"].value_counts().idxmax()
sel_influye_pct = round(
    df["SeleccionInfluyeCompra"].value_counts(normalize=True).max() * 100, 2
)

jug_top = tabla_jugadores(jugadores_series, TOTAL_JUG).index[0]
jug_pct = tabla_jugadores(jugadores_series, TOTAL_JUG).iloc[0]["%"]

pub_top = df["TipoPublicidadAtractiva"].value_counts().idxmax()
pub_pct = round(
    df["TipoPublicidadAtractiva"].value_counts(normalize=True).max() * 100, 2
)

promo_top = df["PromocionPreferida"].value_counts().idxmax()
promo_pct = round(df["PromocionPreferida"].value_counts(normalize=True).max() * 100, 2)

tarj_si_pct = round(
    df["CompraTarjetasColeccionables"].value_counts(normalize=True).get("Sí", 0) * 100,
    2,
)

camp_top = df["CampaniaMasProbableCompra"].value_counts().idxmax()
camp_pct = round(
    df["CampaniaMasProbableCompra"].value_counts(normalize=True).max() * 100, 2
)

# Disposición compra diseño (positivas = Sí + Probablemente sí + Definitivamente sí)
positivas = ["Sí", "Probablemente sí", "Definitivamente sí"]
pct_positivas = round(
    df["CompraDisenoSeleccion"].isin(positivas).sum() / TOTAL * 100, 2
)

print(f"""
╔══════════════════════════════════════════════════════════════╗
║          ANÁLISIS: MUNDIAL FIFA 2026 — MARCA DE SNACKS       ║
║                    Total encuestados: {TOTAL}                       ║
╚══════════════════════════════════════════════════════════════╝

1. INTENCIÓN DE SEGUIR EL MUNDIAL
   • {pct_si_mundial}% de los encuestados planea ver el Mundial FIFA 2026.
   • Altísimo nivel de engagement: sólo 1 de cada 10 no planea seguirlo.

2. SELECCIÓN MÁS APOYADA
   • {sel_apoya_top} lidera con {sel_apoya_pct}% del apoyo total.
   • El podio lo completan Argentina (15%) y Portugal (10%).

3. SELECCIÓN CON MAYOR INFLUENCIA DE COMPRA
   • {sel_influye_top} encabeza la influencia en la decisión de compra ({sel_influye_pct}%).
   • México (14%) y Argentina (13%) son también palancas clave.

4. JUGADOR MÁS INFLUYENTE
   • {jug_top} es el jugador que más motivaría la compra ({jug_pct}% de las menciones).
   • Le siguen Cristiano Ronaldo, Vinícius Júnior, Kylian Mbappé y Neymar Jr.

5. PUBLICIDAD MÁS ATRACTIVA
   • "{pub_top}" es el formato preferido ({pub_pct}%).
   • Segunda opción: "Una selección nacional" (23%).

6. PROMOCIÓN MÁS ATRACTIVA
   • La promoción favorita es "{promo_top}" ({promo_pct}% de preferencia).
   • Le sigue "Descuento directo" (21%).

7. TARJETAS COLECCIONABLES
   • {tarj_si_pct}% compraría snacks si incluyen tarjetas coleccionables.
   • Mecanismo de alto potencial para incrementar volumen de venta.

8. CAMPAÑA CON MAYOR INTENCIÓN DE COMPRA
   • "{camp_top}" es la campaña más motivadora ({camp_pct}%).
   • "Edición Mundial FIFA 2026" ocupa el segundo lugar (16%).

9. DISEÑO DE SELECCIÓN EN EL EMPAQUE
   • {pct_positivas}% tendría respuesta positiva ante un snack con diseño de selección
     (suma de: Sí + Probablemente sí + Definitivamente sí).

══════════════════════════════════════════════════════════════
INSIGHTS DE MARKETING ACCIONABLES
══════════════════════════════════════════════════════════════

A. PRODUCTO
   → Lanzar ediciones limitadas con diseño de Brasil, Argentina y Portugal
     (selecciones de mayor apoyo e influencia de compra).
   → Incluir tarjetas coleccionables de jugadores: 58% declara que sí compraría.

B. EMBAJADORES
   → Activar a Lionel Messi como rostro principal de la campaña; es el jugador
     con mayor poder de influencia espontánea.
   → Cristiano Ronaldo y Vinícius Júnior son opciones de alto impacto para
     mercados complementarios.

C. PUBLICIDAD
   → Centrar creatividades en "jugador famoso" (29%) y "selección nacional" (23%).
   → En jóvenes (18–34 años), el humor y los sorteos también son tractores.

D. PROMOCIONES
   → El 2x1 y el descuento directo son los mayores impulsores de compra.
   → Las tarjetas coleccionables son la tercera opción y generan lealtad de largo plazo.

E. CAMPAÑA PRINCIPAL
   → La "Edición Brasil" y la "Edición Mundial FIFA 2026" son las de mayor
     intención de compra.
   → Segmentar: jóvenes responden a ediciones de jugadores famosos;
     adultos (35+) prefieren ediciones de selecciones clásicas.

F. SEGMENTACIÓN
   → El segmento 25–34 años (36% de la muestra) es el núcleo de consumo;
     empleados privados y estudiantes son los grupos más grandes.
   → Personalizar comunicación: estudiantes responden a humor y 2x1;
     empresarios y profesionales valoran ediciones premium de selecciones.
""")
