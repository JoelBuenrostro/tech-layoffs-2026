/**
 * main.ts
 * Entry point del dashboard. Orquesta la inicialización de filtros y gráficas.
 * Lee los datos serializados por Astro desde el tag #chart-data y carga
 * Chart.js desde CDN antes de inicializar las gráficas.
 */

import { initCharts, type ChartData } from './charts';
import { initFilters } from './filters';

// Inicializar filtros de tabla (no depende de Chart.js)
initFilters();

// Leer datos del servidor embebidos por Astro en el DOM
const raw  = document.getElementById('chart-data')?.textContent ?? '{}';
const data = JSON.parse(raw) as ChartData;

// Cargar Chart.js desde CDN e inicializar gráficas al terminar
const s  = document.createElement('script');
s.src    = 'https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js';
s.onload = () => initCharts(data);
document.head.appendChild(s);
