/**
 * filters.ts
 * Lógica de filtrado interactivo de la tabla de empresas.
 * Se inicializa en DOMContentLoaded desde index.astro.
 */

function applyFilters(): void {
  const searchInput  = document.getElementById('searchInput')  as HTMLInputElement | null;
  const sectorSelect = document.getElementById('filterSector') as HTMLSelectElement | null;
  const regionSelect = document.getElementById('filterRegion') as HTMLSelectElement | null;
  const aiSelect     = document.getElementById('filterAI')     as HTMLSelectElement | null;
  const typeSelect   = document.getElementById('filterType')   as HTMLSelectElement | null;
  const countLabel   = document.getElementById('tableCount')   as HTMLElement | null;

  if (!searchInput || !sectorSelect || !regionSelect || !aiSelect) return;

  const search = searchInput.value.toLowerCase();
  const sector = sectorSelect.value;
  const region = regionSelect.value;
  const ai     = aiSelect.value;
  const type   = typeSelect?.value ?? '';

  const rows = document.querySelectorAll<HTMLTableRowElement>('#mainTable tbody tr');
  let visible = 0;

  rows.forEach(row => {
    const ok = (!search || (row.dataset.company ?? '').includes(search))
            && (!sector || row.dataset.sector === sector)
            && (!region || row.dataset.region === region)
            && (!ai     || row.dataset.ai     === ai)
            && (!type   || row.dataset.type   === type);

    row.style.display = ok ? '' : 'none';
    if (ok) visible++;
  });

  if (countLabel) {
    countLabel.textContent = `${visible} / ${rows.length} empresas`;
  }
}

export function initFilters(): void {
  document.addEventListener('DOMContentLoaded', () => {
    applyFilters();

    const ids = ['searchInput', 'filterSector', 'filterRegion', 'filterAI', 'filterType'];
    ids.forEach(id => {
      const el = document.getElementById(id);
      el?.addEventListener('input',  applyFilters);
      el?.addEventListener('change', applyFilters);
    });
  });
}
