"""
process_data.py
---------------
Lee el CSV de despidos tech 2026 y genera archivos JSON en public/data/
con todos los textos ya traducidos al español.

Uso:
    python3 scripts/process_data.py

Compatible con Python 3.9+, solo usa la librería estándar.
"""

import csv
import json
from collections import defaultdict
from pathlib import Path

BASE_DIR   = Path(__file__).parent.parent
CSV_PATH   = BASE_DIR / "tech_layoffs_2026_tracker.csv"
OUTPUT_DIR = BASE_DIR / "public" / "data"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MESES = {
    # Formato completo (registros originales)
    "January 2026":   "Enero 2026",
    "February 2026":  "Febrero 2026",
    "March 2026":     "Marzo 2026",
    "April 2026":     "Abril 2026",
    "May 2026":       "Mayo 2026",
    "June 2026":      "Junio 2026",
    "July 2026":      "Julio 2026",
    "August 2026":    "Agosto 2026",
    "September 2026": "Septiembre 2026",
    "October 2026":   "Octubre 2026",
    "November 2026":  "Noviembre 2026",
    "December 2026":  "Diciembre 2026",
    # Formato corto (registros de layoffs.fyi)
    "January":   "Enero 2026",
    "February":  "Febrero 2026",
    "March":     "Marzo 2026",
    "April":     "Abril 2026",
    "May":       "Mayo 2026",
    "June":      "Junio 2026",
    "July":      "Julio 2026",
    "August":    "Agosto 2026",
    "September": "Septiembre 2026",
    "October":   "Octubre 2026",
    "November":  "Noviembre 2026",
    "December":  "Diciembre 2026",
}

MES_CORTO = {
    # Formato completo
    "January 2026":   "Ene",
    "February 2026":  "Feb",
    "March 2026":     "Mar",
    "April 2026":     "Abr",
    "May 2026":       "May",
    "June 2026":      "Jun",
    "July 2026":      "Jul",
    "August 2026":    "Ago",
    "September 2026": "Sep",
    "October 2026":   "Oct",
    "November 2026":  "Nov",
    "December 2026":  "Dic",
    # Formato corto
    "January":   "Ene",
    "February":  "Feb",
    "March":     "Mar",
    "April":     "Abr",
    "May":       "May",
    "June":      "Jun",
    "July":      "Jul",
    "August":    "Ago",
    "September": "Sep",
    "October":   "Oct",
    "November":  "Nov",
    "December":  "Dic",
}

TRIMESTRES = {
    "Q1 2026": "T1 2026",
    "Q2 2026": "T2 2026",
    "Q3 2026": "T3 2026",
    "Q4 2026": "T4 2026",
}

REGIONES = {
    "North America": "Norteamérica",
    "Europe":        "Europa",
    "Asia-Pacific":  "Asia-Pacífico",
    "Latin America": "Latinoamérica",
    "Middle East":   "Medio Oriente",
    "Africa":        "África",
}

PAISES = {
    "USA":         "EE.UU.",
    "UK":          "Reino Unido",
    "Germany":     "Alemania",
    "Canada":      "Canadá",
    "Australia":   "Australia",
    "India":       "India",
    "Spain":       "España",
    "Sweden":      "Suecia",
    "Netherlands":   "Países Bajos",
    "Austria":       "Austria",
    "Israel":        "Israel",
    "Brazil":        "Brasil",
    "Czech Republic":"República Checa",
}

SECTORES = {
    "AI Research":              "Investigación en IA",
    "Automotive Tech":          "Tecnología Automotriz",
    "CRM/SaaS":                 "CRM/SaaS",
    "Cybersecurity":            "Ciberseguridad",
    "Design Software":          "Software de Diseño",
    "E-Commerce":               "Comercio Electrónico",
    "E-Commerce/Cloud":         "Comercio Electrónico/Nube",
    "EV Batteries":             "Baterías para VE",
    "Enterprise SaaS":          "SaaS Empresarial",
    "Enterprise Software":      "Software Empresarial",
    "Fintech":                  "Fintech",
    "Grocery Tech":             "Tecnología de Supermercados",
    "Insurance":                "Seguros",
    "Interior Design Tech":     "Tecnología de Diseño de Interiores",
    "Logistics Software":       "Software de Logística",
    "Manufacturing":            "Manufactura",
    "Networking/Cybersecurity": "Redes/Ciberseguridad",
    "Retail Pharmacy":          "Farmacia Minorista",
    "Semiconductors":           "Semiconductores",
    "Social Media":             "Redes Sociales",
    "Social Media/AI":          "Redes Sociales/IA",
    "Social Media/VR":          "Redes Sociales/RV",
    "Telecommunications":       "Telecomunicaciones",
}

REACCIONES_BOLSA = {
    "Positive": "Positiva",
    "Negative": "Negativa",
    "Neutral":  "Neutral",
}

TAMAÑOS = {
    "Mega (5K+)":     "Mega (5K+)",
    "Large (2K-5K)":  "Grande (2K–5K)",
    "Medium (500-2K)":"Mediana (500–2K)",
    "Small (<500)":   "Pequeña (<500)",
}

ROLES = {
    "customer support":                     "Atención al cliente",
    "Overlapping roles from merger":         "Roles duplicados por fusión",
    "Content moderation":                   "Moderación de contenido",
    "admin roles":                          "Roles administrativos",
    "Middle management":                    "Mandos intermedios",
    "program managers":                     "Gerentes de programa",
    "QA testers":                           "Testers de QA",
    "content":                              "Creación de contenido",
    "VR/AR engineers":                      "Ingenieros de RV/RA",
    "metaverse designers":                  "Diseñadores de metaverso",
    "R&D engineers":                        "Ingenieros de I+D",
    "R&D staff":                            "Personal de I+D",
    "QA":                                   "Control de calidad (QA)",
    "IT ops":                               "Operaciones de TI",
    "IT operations":                        "Operaciones de TI",
    "database admins":                      "Administradores de base de datos",
    "support":                              "Soporte técnico",
    "Sales support":                        "Soporte de ventas",
    "Tier-1 customer service":              "Atención al cliente nivel 1",
    "marketing roles":                      "Roles de marketing",
    "Network engineers":                    "Ingenieros de redes",
    "software engineers":                   "Ingenieros de software",
    "data analysts":                        "Analistas de datos",
    "product managers":                     "Gerentes de producto",
    "HR":                                   "Recursos humanos",
    "finance":                              "Finanzas",
    "legal":                                "Legal",
    "operations":                           "Operaciones",
    "recruiters":                           "Reclutadores",
    "sales":                                "Ventas",
    "designers":                            "Diseñadores",
}

RAZONES = {
    "AI automates insurance tasks":                  "La IA automatiza tareas de seguros",
    "AI automation in warehouse operations":         "Automatización con IA en operaciones de almacén",
    "AI data centres replace human ops":             "Centros de datos con IA reemplazan operaciones humanas",
    "AI design tools replace human designers":       "Herramientas de IA reemplazan diseñadores",
    "AI investment and office space reduction":      "Inversión en IA y reducción de espacio de oficinas",
    "AI replaces QA and testing teams":              "La IA reemplaza equipos de QA y pruebas",
    "AI tools replace roles enabling smaller teams": "Herramientas de IA permiten equipos más pequeños",
    "AI-driven efficiency and restructuring":        "Eficiencia impulsada por IA y reestructuración",
    "AI-forward content and marketing strategy":     "Estrategia de contenido y marketing centrada en IA",
    "AI-forward strategy in customer ops":           "Estrategia centrada en IA para operaciones con clientes",
    "Blast furnace closure":                         "Cierre de alto horno",
    "Blast furnace closure effective":               "Cierre efectivo de alto horno",
    "Chip market slowdown":                          "Desaceleración del mercado de chips",
    "Cost restructuring and portfolio focus":        "Reestructuración de costos y enfoque de portafolio",
    "Cost restructuring with compensation":          "Reestructuración de costos con compensaciones",
    "Declining 5G demand and cost reduction":        "Caída en demanda 5G y reducción de costos",
    "Internal reorganization":                       "Reorganización interna",
    "Offset AI infrastructure costs":                "Compensar costos de infraestructura de IA",
    "Pivot from metaverse to AI research":           "Pivote del metaverso a investigación en IA",
    "Pivot to AI-first company strategy":            "Pivote hacia estrategia de empresa centrada en IA",
    "Post-Ansys acquisition restructuring":          "Reestructuración post-adquisición de Ansys",
    "Post-CyberArk acquisition overlap":             "Solapamiento post-adquisición de CyberArk",
    "Reduce bureaucracy and management layers":      "Reducir burocracia y capas de gestión",
    "Restructuring after Splunk acquisition":        "Reestructuración tras adquisición de Splunk",
    "Restructuring sales teams":                     "Reestructuración de equipos de ventas",
    "Rethinking digital transformation":             "Replantear la transformación digital",
    "Slowing EV demand":                             "Desaceleración en demanda de vehículos eléctricos",
    "Store closures and cost restructuring":         "Cierre de tiendas y reestructuración de costos",
}

def t(d, val):
    """Traduce un valor usando el diccionario dado; devuelve el original si no existe."""
    return d.get(val, val) if val else val


def to_int(val, default=0):
    try:
        return int(float(val)) if val not in ("", None) else default
    except (ValueError, TypeError):
        return default


def save_json(data, filename):
    path = OUTPUT_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✔ {filename}")


rows = []
with open(CSV_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        row["jobs_cut"]       = to_int(row.get("jobs_cut"))
        row["month_es"]       = t(MESES,            row.get("month", ""))
        row["month_short"]    = t(MES_CORTO,         row.get("month", ""))
        row["quarter_es"]     = t(TRIMESTRES,        row.get("quarter", ""))
        row["region_es"]      = t(REGIONES,          row.get("region", ""))
        row["country_es"]     = t(PAISES,            row.get("country", ""))
        row["sector_es"]      = t(SECTORES,          row.get("sector", ""))
        row["stock_es"]       = t(REACCIONES_BOLSA,  row.get("stock_reaction", ""))
        row["size_es"]        = t(TAMAÑOS,            row.get("layoff_size_category", ""))
        row["reason_es"]      = t(RAZONES,            row.get("reason_stated", ""))
        row["ai_cited_bool"]  = str(row.get("ai_cited", "")).lower() == "true"
        rows.append(row)

print(f"\n📂 CSV cargado: {len(rows)} registros\n")

total_jobs      = sum(r["jobs_cut"] for r in rows)
total_companies = len(rows)
ai_cited_count  = sum(1 for r in rows if r["ai_cited_bool"])
ai_cited_pct    = round(ai_cited_count / total_companies * 100, 1) if total_companies else 0

quarter_totals = defaultdict(int)
for r in rows:
    quarter_totals[r["quarter_es"]] += r["jobs_cut"]
top_quarter = max(quarter_totals, key=quarter_totals.get) if quarter_totals else "N/D"

# Calcular fecha automáticamente desde el registro más reciente del CSV
from datetime import datetime
layoff_dates = [r.get("layoff_date", "") for r in rows if r.get("layoff_date", "").strip()]
if layoff_dates:
    latest = max(layoff_dates)
    dt = datetime.strptime(latest, "%Y-%m-%d")
    MESES_ES = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
                "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]
    data_as_of = f"{dt.day} de {MESES_ES[dt.month - 1]} de {dt.year}"
else:
    data_as_of = "N/D"

save_json({
    "total_jobs_cut":   total_jobs,
    "total_companies":  total_companies,
    "ai_cited_pct":     ai_cited_pct,
    "top_quarter":      top_quarter,
    "data_as_of":       data_as_of,
}, "summary.json")

MES_ORDER = ["Enero","Febrero","Marzo","Abril","Mayo","Junio",
             "Julio","Agosto","Septiembre","Octubre","Noviembre","Diciembre"]

month_data = defaultdict(lambda: {"full": "", "jobs_cut": 0})
for r in rows:
    key = r["month_short"]
    month_data[key]["full"]     = r["month_es"]
    month_data[key]["jobs_cut"] += r["jobs_cut"]

# Ordenar por mes natural
by_month = sorted(
    [{"month": v["full"], "month_short": k, "jobs_cut": v["jobs_cut"]}
     for k, v in month_data.items()],
    key=lambda x: next((i for i, m in enumerate(MES_ORDER) if m in x["month"]), 99)
)
save_json(by_month, "by_month.json")

# ── Acumulado mensual ─────────────────────────────────────────────────────
cumulative = 0
cumulative_data = []
for entry in by_month:
    cumulative += entry["jobs_cut"]
    cumulative_data.append({
        "month":       entry["month"],
        "month_short": entry["month_short"],
        "jobs_cut":    entry["jobs_cut"],
        "cumulative":  cumulative,
    })
save_json(cumulative_data, "cumulative.json")

sector_data = defaultdict(int)
for r in rows:
    sector_data[r["sector_es"]] += r["jobs_cut"]

save_json(sorted(
    [{"sector": k, "jobs_cut": v} for k, v in sector_data.items()],
    key=lambda x: x["jobs_cut"], reverse=True
), "by_sector.json")

region_data = defaultdict(int)
for r in rows:
    region_data[r["region_es"]] += r["jobs_cut"]

save_json(sorted(
    [{"region": k, "jobs_cut": v} for k, v in region_data.items()],
    key=lambda x: x["jobs_cut"], reverse=True
), "by_region.json")

company_data = defaultdict(int)
for r in rows:
    company_data[r.get("company", "N/D")] += r["jobs_cut"]

save_json(sorted(
    [{"company": k, "jobs_cut": v} for k, v in company_data.items()],
    key=lambda x: x["jobs_cut"], reverse=True
)[:10], "top_companies.json")

save_json(sorted(
    [{"quarter": k, "jobs_cut": v} for k, v in quarter_totals.items()],
    key=lambda x: x["quarter"]
), "by_quarter.json")

TIPOS_EMPRESA = {
    "Public":  "Pública",
    "Private": "Privada",
}

save_json([
    {
        "company":      r.get("company"),
        "layoff_date":  r.get("layoff_date"),
        "jobs_cut":     r["jobs_cut"],
        "sector":       r["sector_es"],
        "region":       r["region_es"],
        "country":      r["country_es"],
        "ai_cited":     r["ai_cited_bool"],
        "reason":       r["reason_es"],
        "month":        r["month_es"],
        "quarter":      r["quarter_es"],
        "size":         r["size_es"],
        "stock":        r["stock_es"],
        "source":       r.get("verified_source"),
        "company_type": t(TIPOS_EMPRESA, r.get("company_type", "")),
    }
    for r in rows
], "detail.json")

role_count = defaultdict(int)
for r in rows:
    for role in r.get("roles_most_affected", "").split(","):
        role = role.strip()
        if role:
            role_es = t(ROLES, role)
            role_count[role_es] += 1

save_json(sorted(
    [{"role": k, "count": v} for k, v in role_count.items()],
    key=lambda x: x["count"], reverse=True
)[:20], "top_roles.json")

print(f"\n✅ Datos procesados correctamente en {OUTPUT_DIR}\n")
