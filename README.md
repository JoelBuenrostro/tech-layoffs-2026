# Tech Layoffs 2026 · Dashboard

Dashboard interactivo que analiza y visualiza los despidos masivos en la industria tecnológica durante 2026. Publicado como sitio estático en GitHub Pages y actualizado mensualmente.

🔗 **[Ver dashboard en vivo](https://joelbuenrostro.github.io/tech-layoffs-2026)**

---

## Stack tecnológico

| Capa | Tecnología |
|---|---|
| Frontend | [Astro](https://astro.build) (generación estática) |
| Gráficas | [Chart.js 4](https://www.chartjs.org) vía CDN |
| Datos | Python 3 + pandas |
| Deploy | GitHub Actions → GitHub Pages |
| Tipado | TypeScript |

---

## Estructura del proyecto

```
tech-layoffs-2026/
├── scripts/
│   └── process_data.py        # Pipeline de datos: CSV → JSON
├── src/
│   ├── layouts/
│   │   └── Layout.astro       # Shell HTML + fuentes
│   ├── pages/
│   │   └── index.astro        # Página principal del dashboard
│   ├── scripts/
│   │   ├── main.ts            # Entry point del cliente
│   │   ├── charts.ts          # Inicialización de gráficas
│   │   └── filters.ts         # Lógica de filtros de tabla
│   └── styles/
│       ├── global.css         # Design tokens y reset
│       └── dashboard.css      # Estilos del dashboard
├── public/
│   └── data/                  # JSONs generados por process_data.py
│       ├── summary.json
│       ├── by_month.json
│       ├── by_sector.json
│       ├── by_region.json
│       ├── by_quarter.json
│       ├── top_companies.json
│       ├── top_roles.json
│       └── detail.json
├── tech_layoffs_2026_tracker.csv  # Fuente de datos principal
└── .github/
    └── workflows/
        └── deploy.yml         # CI/CD: build + deploy a GitHub Pages
```

---

## Requisitos

- Node.js 18+
- Python 3.9+

---

## Desarrollo local

**1. Instalar dependencias:**

```bash
npm install
```

**2. Procesar los datos del CSV:**

```bash
python3 scripts/process_data.py
```

Esto genera todos los JSONs en `public/data/`.

**3. Levantar el servidor de desarrollo:**

```bash
npm run dev
```

El dashboard estará disponible en `http://localhost:4321`.

---

## Actualización mensual de datos

El flujo de actualización es:

1. Abrir `tech_layoffs_2026_tracker.csv` y agregar las nuevas filas del mes.
2. Ejecutar `python3 scripts/process_data.py` para regenerar los JSONs.
3. Hacer commit y push a `main`. GitHub Actions construye y publica automáticamente.

> Si una empresa o rol aparece en inglés en el dashboard, es señal de que falta su entrada en los diccionarios de traducción de `process_data.py`.

---

## Columnas del CSV

| Columna | Descripción |
|---|---|
| `company` | Nombre de la empresa |
| `date` | Fecha del anuncio (YYYY-MM-DD) |
| `jobs_cut` | Número de empleos eliminados |
| `sector` | Sector de la industria |
| `country` | País de origen |
| `region` | Región geográfica |
| `ai_cited` | Si la IA fue citada como causa (Yes/No) |
| `reason_stated` | Razón declarada por la empresa |
| `stock_reaction` | Reacción de la bolsa (Positive/Negative/Neutral) |
| `layoff_size_category` | Categoría por tamaño del despido |
| `roles_most_affected` | Roles más afectados (separados por coma) |
| `verified_source` | URL de la fuente verificada |

---

## JSONs generados

| Archivo | Contenido |
|---|---|
| `summary.json` | KPIs globales: total empleos, empresas, % IA, trimestre líder |
| `by_month.json` | Empleos perdidos agrupados por mes |
| `by_sector.json` | Distribución por sector |
| `by_region.json` | Distribución por región |
| `by_quarter.json` | Distribución por trimestre |
| `top_companies.json` | Top 10 empresas por empleos eliminados |
| `top_roles.json` | Top 20 roles más afectados |
| `detail.json` | Registro completo para la tabla interactiva |

---

## Deploy

El deploy es automático vía GitHub Actions al hacer push a `main`. El workflow en `.github/workflows/deploy.yml`:

1. Instala dependencias de Node y Python
2. Ejecuta `process_data.py` para regenerar los datos
3. Ejecuta `astro build`
4. Publica el contenido de `dist/` en GitHub Pages

---

## Autor

**Joel Buenrostro** · [LinkedIn](https://www.linkedin.com/in/joelbuenrostro)
