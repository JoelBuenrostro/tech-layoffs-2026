/**
 * charts.ts
 * Inicializa todas las gráficas del dashboard usando Chart.js (vía CDN).
 * Se invoca desde index.astro una vez que Chart.js ha cargado.
 */

// Chart.js se carga desde CDN como global — declaramos el tipo mínimo necesario
declare const Chart: any;

interface MonthRow       { month_short: string; jobs_cut: number }
interface SectorRow      { sector:      string; jobs_cut: number }
interface RegionRow      { region:      string; jobs_cut: number }
interface CompanyRow     { company:     string; jobs_cut: number }
interface CumulativeRow  { month_short: string; jobs_cut: number; cumulative: number }

export interface ChartData {
  byMonth:      MonthRow[];
  bySector:     SectorRow[];
  byRegion:     RegionRow[];
  topCompanies: CompanyRow[];
  cumulative:   CumulativeRow[];
}

// Paleta de colores — azul profesional sobre fondo claro
const PALETTE = [
  '#4f6ef7', // Blue
  '#06b6d4', // Cyan
  '#f59e0b', // Amber
  '#10b981', // Emerald
  '#f43f5e', // Rose
  '#8b5cf6', // Purple
  '#0ea5e9', // Sky
  '#84cc16', // Lime
  '#fb923c', // Orange
  '#ec4899', // Pink
];

const GRID_COLOR   = 'rgba(0,0,0,0.06)';
const TICK_COLOR   = '#718096';
const LEGEND_COLOR = '#4a5568';

const baseScales = {
  x: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
  y: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
};

export function initCharts(data: ChartData): void {
  const { byMonth, bySector, byRegion, topCompanies, cumulative } = data;

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
          g.addColorStop(0, 'rgba(79,110,247,0.80)');
          g.addColorStop(1, 'rgba(79,110,247,0.10)');
          return g;
        },
        borderColor: '#4f6ef7',
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
          g.addColorStop(0, 'rgba(6,182,212,0.80)');
          g.addColorStop(1, 'rgba(6,182,212,0.10)');
          return g;
        },
        borderColor: '#06b6d4',
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

  // ── Despidos acumulados (línea con área) ───────────────────────────────────
  if (cumulative?.length) {
    new Chart(document.getElementById('chartCumulative'), {
      type: 'line',
      data: {
        labels: cumulative.map(d => d.month_short),
        datasets: [
          {
            label: 'Acumulado',
            data: cumulative.map(d => d.cumulative),
            borderColor: '#4f6ef7',
            borderWidth: 2.5,
            pointBackgroundColor: '#4f6ef7',
            pointRadius: 5,
            pointHoverRadius: 7,
            tension: 0.4,
            fill: true,
            backgroundColor: (ctx: any) => {
              const g = ctx.chart.ctx.createLinearGradient(0, 0, 0, 260);
              g.addColorStop(0, 'rgba(79,110,247,0.18)');
              g.addColorStop(1, 'rgba(79,110,247,0.01)');
              return g;
            },
          },
          {
            label: 'Mensual',
            data: cumulative.map(d => d.jobs_cut),
            borderColor: '#06b6d4',
            borderWidth: 1.5,
            borderDash: [5, 4],
            pointBackgroundColor: '#06b6d4',
            pointRadius: 4,
            pointHoverRadius: 6,
            tension: 0.4,
            fill: false,
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: true,
            position: 'top',
            labels: { color: LEGEND_COLOR, boxWidth: 12, boxHeight: 2, padding: 16, font: { size: 11 } },
          },
          tooltip: {
            callbacks: {
              label: (ctx: any) => ` ${ctx.dataset.label}: ${ctx.parsed.y.toLocaleString('es-MX')} empleos`,
            },
          },
        },
        scales: {
          x: { ticks: { color: TICK_COLOR, font: { size: 11 } }, grid: { color: GRID_COLOR } },
          y: {
            ticks: {
              color: TICK_COLOR,
              font: { size: 11 },
              callback: (v: any) => v >= 1000 ? `${(v / 1000).toFixed(0)}k` : v,
            },
            grid: { color: GRID_COLOR },
          },
        },
      },
    });
  }
}
