/**
 * charts.ts
 * Inicializa todas las gráficas del dashboard usando Chart.js (vía CDN).
 * Se invoca desde index.astro una vez que Chart.js ha cargado.
 */

// Chart.js se carga desde CDN como global — declaramos el tipo mínimo necesario
declare const Chart: any;

interface MonthRow    { month_short: string; jobs_cut: number }
interface SectorRow   { sector:   string; jobs_cut: number }
interface RegionRow   { region:   string; jobs_cut: number }
interface CompanyRow  { company:  string; jobs_cut: number }

export interface ChartData {
  byMonth:      MonthRow[];
  bySector:     SectorRow[];
  byRegion:     RegionRow[];
  topCompanies: CompanyRow[];
}

// Paleta de colores — perceptualmente distintos sobre fondo oscuro
const PALETTE = [
  '#6366f1', '#06b6d4', '#f59e0b', '#10b981', '#f43f5e',
  '#a855f7', '#0ea5e9', '#84cc16', '#fb923c', '#ec4899',
];

const GRID_COLOR   = 'rgba(255,255,255,0.05)';
const TICK_COLOR   = '#4a5a7a';
const LEGEND_COLOR = '#8899bb';

const baseScales = {
  x: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
  y: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
};

export function initCharts(data: ChartData): void {
  const { byMonth, bySector, byRegion, topCompanies } = data;

  Chart.defaults.font.family = "'Inter', sans-serif";

  // ── Empleos perdidos por mes ────────────────────────────────────────────────
  new Chart(document.getElementById('chartMonth'), {
    type: 'bar',
    data: {
      labels: byMonth.map(d => d.month_short),
      datasets: [{
        label: 'Empleos perdidos',
        data: byMonth.map(d => d.jobs_cut),
        backgroundColor: (ctx: any) => {
          const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, 260);
          g.addColorStop(0, 'rgba(99,102,241,0.85)');
          g.addColorStop(1, 'rgba(99,102,241,0.2)');
          return g;
        },
        borderColor: '#6366f1',
        borderWidth: 1,
        borderRadius: 5,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx: any) => ` ${ctx.parsed.y.toLocaleString('es-MX')} empleos` } },
      },
      scales: baseScales,
    },
  });

  // ── Distribución por sector (anillo) ────────────────────────────────────────
  new Chart(document.getElementById('chartSector'), {
    type: 'doughnut',
    data: {
      labels: bySector.map(d => d.sector),
      datasets: [{ data: bySector.map(d => d.jobs_cut), backgroundColor: PALETTE, borderWidth: 0, hoverOffset: 6 }],
    },
    options: {
      responsive: true,
      cutout: '62%',
      plugins: {
        legend: { position: 'right', labels: { color: LEGEND_COLOR, boxWidth: 10, boxHeight: 10, borderRadius: 3, padding: 10, font: { size: 11 } } },
        tooltip: { callbacks: { label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed.toLocaleString('es-MX')}` } },
      },
    },
  });

  // ── Distribución por región (circular) ─────────────────────────────────────
  new Chart(document.getElementById('chartRegion'), {
    type: 'doughnut',
    data: {
      labels: byRegion.map(d => d.region),
      datasets: [{ data: byRegion.map(d => d.jobs_cut), backgroundColor: PALETTE.slice(2), borderWidth: 0, hoverOffset: 6 }],
    },
    options: {
      responsive: true,
      cutout: '50%',
      plugins: {
        legend: { position: 'right', labels: { color: LEGEND_COLOR, boxWidth: 10, boxHeight: 10, borderRadius: 3, padding: 10, font: { size: 11 } } },
        tooltip: { callbacks: { label: (ctx: any) => ` ${ctx.label}: ${ctx.parsed.toLocaleString('es-MX')}` } },
      },
    },
  });

  // ── Top 10 empresas (barras horizontales) ───────────────────────────────────
  new Chart(document.getElementById('chartCompanies'), {
    type: 'bar',
    data: {
      labels: topCompanies.map(d => d.company),
      datasets: [{
        label: 'Empleos perdidos',
        data: topCompanies.map(d => d.jobs_cut),
        backgroundColor: (ctx: any) => {
          const g = ctx.chart.ctx.createLinearGradient(300, 0, 0, 0);
          g.addColorStop(0, 'rgba(245,158,11,0.85)');
          g.addColorStop(1, 'rgba(245,158,11,0.2)');
          return g;
        },
        borderColor: '#f59e0b',
        borderWidth: 1,
        borderRadius: 4,
        borderSkipped: false,
      }],
    },
    options: {
      indexAxis: 'y',
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: { callbacks: { label: (ctx: any) => ` ${ctx.parsed.x.toLocaleString('es-MX')} empleos` } },
      },
      scales: {
        x: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
        y: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { display: false } },
      },
    },
  });
}
