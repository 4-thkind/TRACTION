let DATA = null;

const SYS_COLOR = {
  engine:'#ef4444', fuel:'#f59e0b', tyres:'#22c55e', aero:'#3b82f6', oil:'#ea580c'
};

const SYS_LABELS = {
  engine: 'COOLANT TEMP',
  oil:    'OIL QUALITY',
  aero:   'EFFICIENCY',
  fuel:   'E20 LEVEL',
  tyres:  'AVG PRESSURE'
};

async function fetchVehicleData() {
  try {
    const res = await fetch('/api/status');
    DATA = await res.json();
    updateDashboardSummary();
    if (activeKey && document.getElementById('detailPanel').style.display !== 'none') {
      showDetail(activeKey);
    }
  } catch(e) {
    console.error("Failed to fetch vehicle data:", e);
  }
}

function updateDashboardSummary() {
  if (!DATA) return;

  // Update chip labels — now with F1-style header + badge + label + value
  const chipMap = {
    engine: ['#ef4444', DATA.engine.metrics[0].v, 'COOLANT TEMP'],
    oil:    ['#ea580c', DATA.oil.metrics[0].v, 'OIL QUALITY'],
    aero:   ['#3b82f6', DATA.aero.metrics[0].v.split('/')[0], 'EFFICIENCY'],
    fuel:   ['#f59e0b', DATA.fuel.metrics[0].v, 'E20 LEVEL'],
    tyres:  ['#22c55e', DATA.tyres.metrics[0].v.split(' / ')[0] + ' PSI', 'AVG PRESSURE'],
  };

  Object.entries(chipMap).forEach(([k,[col,val,label]]) => {
    const el = document.getElementById('chip-' + k);
    if (!el) return;

    const code = k === 'tyres' ? 'TYR' : k.toUpperCase();
    const d = DATA[k];
    const badgeTxt = d.badgeTxt || '';
    const bt = badgeTxt.toLowerCase();

    let badgeClass = 'ok';
    let badgeLabel = 'OK';
    if (bt.includes('urgent') || bt.includes('overheat') || bt.includes('low') || bt.includes('aged') || bt.includes('replace')) {
      badgeClass = 'alert';
      badgeLabel = '!';
    } else if (bt.includes('soon') || bt.includes('watch') || bt.includes('warm') || bt.includes('rotation')) {
      badgeClass = 'warn';
      badgeLabel = '!';
    } else {
      badgeLabel = 'OK';
    }

    el.innerHTML = `
      <div class="chip-header">
        <span class="chip-code" style="color:${col}">${code}</span>
        <span class="chip-badge ${badgeClass}">${badgeLabel}</span>
      </div>
      <span class="chip-label">${label}</span>
      <span class="chip-val">${val}</span>
    `;
  });

  // Update left panel cards
  ['engine','oil','fuel','tyres'].forEach(key => {
    const d = DATA[key];
    const badgeEl = document.getElementById(`card-${key}-badge`);
    const valEl   = document.getElementById(`card-${key}-val`);
    if (valEl) valEl.textContent = d.metrics[0].v;
    if (badgeEl) {
      badgeEl.textContent = d.badgeTxt.toUpperCase();
      badgeEl.className = 'sys-badge';
      const t = d.badgeTxt.toLowerCase();
      if (t.includes('normal')||t.includes('good')||t.includes('all four')||t.includes('healthy')||t.match(/score \d/))
        badgeEl.classList.add('ok');
      else if (t.includes('urgent')||t.includes('overheat')||t.includes('low')||t.includes('aged')||t.includes('replace'))
        badgeEl.classList.add('alert');
      else if (t.includes('soon')||t.includes('watch')||t.includes('warm')||t.includes('rotation'))
        badgeEl.classList.add('warn');
    }
  });
}

window.addEventListener('DOMContentLoaded', () => { fetchVehicleData(); });

let activeKey = null;

function selectCard(el, key) {
  document.querySelectorAll('.sys-row').forEach(c => c.classList.remove('active-card'));
  el.classList.add('active-card');
  activateChip(key);
  showDetail(key);
}

function selectChip(key) {
  activateChip(key);
  document.querySelectorAll('.sys-row').forEach(c => {
    c.classList.toggle('active-card', c.dataset.key === key);
  });
  showDetail(key);
}

function activateChip(key) {
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  const el = document.getElementById('chip-' + key);
  if (el) el.classList.add('active');
  activeKey = key;
  drawConnectors(key);
}

function showDetail(key) {
  const d = DATA && DATA[key]; if (!d) return;
  document.getElementById('defaultPanel').style.display = 'none';
  document.getElementById('detailPanel').style.display = 'block';
  document.getElementById('d-nav-code').textContent = key.toUpperCase();
  document.getElementById('d-name').textContent = d.name.toUpperCase();
  document.getElementById('d-tagline').textContent = d.tagline.toUpperCase();

  const badge = document.getElementById('d-badge');
  badge.textContent = d.badgeTxt.toUpperCase();
  const col = SYS_COLOR[key] || '#00E5FF';
  badge.style.cssText = `background:${col}18;color:${col};border:1px solid ${col}35`;

  document.getElementById('d-metrics').innerHTML = d.metrics.map(m =>
    `<div class="metric-cell-f1">
      <div class="metric-lbl-f1">${m.l.toUpperCase()}</div>
      <div class="metric-val-f1" style="color:${m.c}">${m.v}</div>
    </div>`
  ).join('');

  document.getElementById('d-insight').innerHTML = d.insight;
  document.getElementById('d-body').textContent = d.body;
  document.getElementById('d-actions').innerHTML = d.actions.map(a =>
    `<button class="action-btn-f1 ${a.p?'primary':'secondary'}">${a.l.toUpperCase()}</button>`
  ).join('');
}

function showDefault() {
  document.getElementById('defaultPanel').style.display = 'block';
  document.getElementById('detailPanel').style.display = 'none';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.sys-row').forEach(c => c.classList.remove('active-card'));
  clearConnectors();
  activeKey = null;
}

/* ── Connector lines (solid, thin cyan with glow — F1-style) ── */
const CHIP_HS = {
  engine: { chipId:'chip-engine', hsIds:['hs-engine'],                          anchor:'right'  },
  oil:    { chipId:'chip-oil',    hsIds:['hs-oil'],                             anchor:'left'   },
  fuel:   { chipId:'chip-fuel',   hsIds:['hs-fuel'],                            anchor:'right'  },
  aero:   { chipId:'chip-aero',   hsIds:['hs-aero'],                            anchor:'left'   },
  tyres:  { chipId:'chip-tyres',  hsIds:['hs-tfl','hs-tfr','hs-trl','hs-trr'], anchor:'top'    },
};

function ptInScene(el) {
  const sr = document.getElementById('carScene').getBoundingClientRect();
  const r  = el.getBoundingClientRect();
  return { x: r.left + r.width/2 - sr.left, y: r.top + r.height/2 - sr.top };
}
function chipAnchorPt(el, anchor) {
  const sr = document.getElementById('carScene').getBoundingClientRect();
  const r  = el.getBoundingClientRect();
  switch(anchor) {
    case 'bottom': return { x: r.left+r.width/2-sr.left, y: r.bottom-sr.top };
    case 'top':    return { x: r.left+r.width/2-sr.left, y: r.top-sr.top };
    case 'left':   return { x: r.left-sr.left,           y: r.top+r.height/2-sr.top };
    case 'right':  return { x: r.right-sr.left,          y: r.top+r.height/2-sr.top };
  }
}
function drawConnectors(key) {
  const svg = document.getElementById('connSvg'); svg.innerHTML = '';
  const map = CHIP_HS[key]; if (!map) return;
  const chipEl = document.getElementById(map.chipId); if (!chipEl) return;
  const cp  = chipAnchorPt(chipEl, map.anchor);
  const col = SYS_COLOR[key] || '#00E5FF';

  map.hsIds.forEach(id => {
    const hsel = document.getElementById(id); if (!hsel) return;
    const hp = ptInScene(hsel);
    const dx = hp.x-cp.x, dy = hp.y-cp.y;
    const c1x = cp.x+dx*.42, c1y = cp.y;
    const c2x = cp.x+dx*.58, c2y = hp.y;

    // Glow path (fat, blurred)
    const glow = document.createElementNS('http://www.w3.org/2000/svg','path');
    glow.setAttribute('d',`M${cp.x},${cp.y} C${c1x},${c1y} ${c2x},${c2y} ${hp.x},${hp.y}`);
    glow.setAttribute('stroke',col); glow.setAttribute('stroke-width','3.5');
    glow.setAttribute('fill','none'); glow.setAttribute('opacity','0.08');
    glow.setAttribute('stroke-linecap','round');
    svg.appendChild(glow);

    // Main solid line (F1-style — thin, solid, not dashed)
    const path = document.createElementNS('http://www.w3.org/2000/svg','path');
    path.setAttribute('d',`M${cp.x},${cp.y} C${c1x},${c1y} ${c2x},${c2y} ${hp.x},${hp.y}`);
    path.setAttribute('stroke',col); path.setAttribute('stroke-width','0.8');
    path.setAttribute('fill','none');
    path.setAttribute('opacity','0.4'); path.setAttribute('stroke-linecap','round');
    svg.appendChild(path);

    // Small endpoint dot at the hotspot
    const dot = document.createElementNS('http://www.w3.org/2000/svg','circle');
    dot.setAttribute('cx', hp.x); dot.setAttribute('cy', hp.y);
    dot.setAttribute('r', '2.5');
    dot.setAttribute('fill', col); dot.setAttribute('opacity', '0.35');
    svg.appendChild(dot);
  });
}
function clearConnectors() { document.getElementById('connSvg').innerHTML=''; }

function toggleBtn(btn) {
  btn.classList.toggle('on');
  btn.querySelector('span').textContent = btn.classList.contains('on') ? 'ON' : 'OFF';
}
function setMode(btn) {
  document.querySelectorAll('.drive-chip').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}
document.querySelectorAll('.mode-btn').forEach(b => {
  b.addEventListener('click', () => {
    document.querySelectorAll('.mode-btn').forEach(x => x.classList.remove('active'));
    b.classList.add('active');
  });
});
