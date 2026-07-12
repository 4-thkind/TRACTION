let DATA = null;

async function fetchVehicleData() {
  try {
    const res = await fetch('/api/status');
    DATA = await res.json();
    console.log("Loaded dynamic vehicle data:", DATA);
    updateDashboardSummary();
    // If a detail panel is open, refresh it with new data
    if (activeKey && document.getElementById('detailPanel').style.display !== 'none') {
      showDetail(activeKey);
    }
  } catch(e) {
    console.error("Failed to fetch vehicle data:", e);
  }
}

function updateDashboardSummary() {
  if (!DATA) return;
  // Update Chips
  const elEngine = document.getElementById('chip-engine');
  if (elEngine) elEngine.innerHTML = `<span class="chip-dot" style="background:${DATA.engine.metrics[0].c}"></span>Engine ${DATA.engine.metrics[0].v}`;
  const elOil = document.getElementById('chip-oil');
  if (elOil) elOil.innerHTML = `<span class="chip-dot" style="background:${DATA.oil.metrics[0].c}"></span>Oil ${DATA.oil.metrics[0].v}`;
  const elAero = document.getElementById('chip-aero');
  if (elAero) elAero.innerHTML = `<span class="chip-dot" style="background:${DATA.aero.metrics[0].c}"></span>Aero ${DATA.aero.metrics[0].v.split('/')[0]}`;
  const elFuel = document.getElementById('chip-fuel');
  if (elFuel) elFuel.innerHTML = `<span class="chip-dot" style="background:${DATA.fuel.metrics[0].c}"></span>E20 · ${DATA.fuel.metrics[0].v}`;
  const elTyres = document.getElementById('chip-tyres');
  if (elTyres) elTyres.innerHTML = `<span class="chip-dot" style="background:${DATA.tyres.metrics[0].c}"></span>Tyres ${DATA.tyres.metrics[0].v.split(' / ')[0]} PSI`;

  // Update bottom cards
  ['engine', 'oil', 'fuel', 'tyres'].forEach(key => {
    const d = DATA[key];
    const cardBadge = document.getElementById(`card-${key}-badge`);
    const cardVal = document.getElementById(`card-${key}-val`);
    if (cardBadge) cardBadge.textContent = d.badgeTxt;
    if (cardVal) cardVal.textContent = d.metrics[0].v;
  });
}

// Fetch once on load
window.addEventListener('DOMContentLoaded', () => {
  fetchVehicleData();
  // We could also set an interval here for live updates: setInterval(fetchVehicleData, 5000);
});

let activeKey = null;

function selectCard(el, key) {
  document.querySelectorAll('.cond-card').forEach(c => c.classList.remove('active-card'));
  el.classList.add('active-card');
  activateChip(key);
  showDetail(key);
}

function selectChip(key) {
  activateChip(key);
  document.querySelectorAll('.cond-card').forEach(c => {
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
  const d = DATA[key]; if (!d) return;
  document.getElementById('defaultPanel').style.display = 'none';
  document.getElementById('detailPanel').style.display = 'block';
  document.getElementById('d-icon').textContent = d.icon;
  document.getElementById('d-name').textContent = d.name;
  document.getElementById('d-tagline').textContent = d.tagline;
  document.getElementById('d-hero').style.background = d.heroBg;
  const badge = document.getElementById('d-badge');
  badge.textContent = d.badgeTxt; badge.style.background = d.badgeBg; badge.style.color = d.badgeCol;
  document.getElementById('d-metrics').innerHTML = d.metrics.map(m =>
    `<div class="metric-cell"><div class="metric-lbl">${m.l}</div><div class="metric-val" style="color:${m.c}">${m.v}</div></div>`
  ).join('');
  document.getElementById('d-insight').innerHTML = d.insight;
  document.getElementById('d-body').textContent = d.body;
  document.getElementById('d-actions').innerHTML = d.actions.map(a =>
    `<button class="action-btn ${a.p?'primary':'secondary'}">${a.l}</button>`
  ).join('');
}

function showDefault() {
  document.getElementById('defaultPanel').style.display = 'block';
  document.getElementById('detailPanel').style.display = 'none';
  document.querySelectorAll('.chip').forEach(c => c.classList.remove('active'));
  document.querySelectorAll('.cond-card').forEach(c => c.classList.remove('active-card'));
  clearConnectors(); activeKey = null;
}

/* ── Bezier connector lines ── */
const CHIP_HS = {
  engine: { chipId:'chip-engine', hsIds:['hs-engine'],                          anchor:'bottom' },
  oil:    { chipId:'chip-oil',    hsIds:['hs-oil'],                             anchor:'left'   },
  fuel:   { chipId:'chip-fuel',   hsIds:['hs-fuel'],                            anchor:'right'  },
  aero:   { chipId:'chip-aero',   hsIds:['hs-aero'],                            anchor:'left'   },
  tyres:  { chipId:'chip-tyres',  hsIds:['hs-tfl','hs-tfr','hs-trl','hs-trr'], anchor:'top'    },
};
const COL = {engine:'#ef4444',fuel:'#f59e0b',tyres:'#22c55e',aero:'#3b82f6',oil:'#ea580c'};

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
  const cp = chipAnchorPt(chipEl, map.anchor);
  const col = COL[key] || '#999';
  map.hsIds.forEach(id => {
    const hsel = document.getElementById(id); if (!hsel) return;
    const hp = ptInScene(hsel);
    const dx = hp.x-cp.x, dy = hp.y-cp.y;
    const c1x = cp.x+dx*.4, c1y = cp.y;
    const c2x = cp.x+dx*.6, c2y = hp.y;
    const path = document.createElementNS('http://www.w3.org/2000/svg','path');
    path.setAttribute('d',`M${cp.x},${cp.y} C${c1x},${c1y} ${c2x},${c2y} ${hp.x},${hp.y}`);
    path.setAttribute('stroke',col); path.setAttribute('stroke-width','1.5');
    path.setAttribute('stroke-dasharray','5 3'); path.setAttribute('fill','none');
    path.setAttribute('opacity','0.55'); path.setAttribute('stroke-linecap','round');
    svg.appendChild(path);
  });
}
function clearConnectors() { document.getElementById('connSvg').innerHTML=''; }

function toggleBtn(btn){ btn.classList.toggle('on'); }
function setMode(btn){
  document.querySelectorAll('.drive-chip').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
}
document.querySelectorAll('.mode-btn').forEach(b=>{
  b.addEventListener('click',()=>{
    document.querySelectorAll('.mode-btn').forEach(x=>x.classList.remove('active'));
    b.classList.add('active');
  });
});