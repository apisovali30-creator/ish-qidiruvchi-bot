// ========================================================
// OQILA GOOGLE ADMIN PANEL JAVASCRIPT
// ========================================================

const state = {
  token: localStorage.getItem('oqila_admin_token') || '',
  adminInfo: null,
  activeTab: 'tabStats',
  resumes: [],
  vacancies: [],
  reviews: [],
  config: null,
  lastStats: null,
  pollTimer: null
};

// DOM Elements
const loginOverlay = document.getElementById('loginOverlay');
const adminApp = document.getElementById('adminApp');
const quickLoginForm = document.getElementById('quickLoginForm');
const adminKeyInput = document.getElementById('adminKeyInput');
const loginErrorMsg = document.getElementById('loginErrorMsg');
const btnLogout = document.getElementById('btnLogout');
const adminToast = document.getElementById('adminToast');
const adminUserName = document.getElementById('adminUserName');
const adminUserEmail = document.getElementById('adminUserEmail');
const adminAvatarImg = document.getElementById('adminAvatarImg');

// Init
document.addEventListener('DOMContentLoaded', async () => {
  setupTabs();
  setupFilterListeners();
  await loadServerConfig();

  if (state.token) {
    const ok = await verifySession();
    if (ok) {
      showDashboard();
      return;
    }
  }

  showLogin();
  setupGoogleAuth();
});

// Toast Helper
function showToast(message, type = 'success') {
  adminToast.textContent = message;
  adminToast.className = `admin-toast ${type}`;
  adminToast.style.display = 'block';
  setTimeout(() => {
    adminToast.style.display = 'none';
  }, 3500);
}

// 1. Config Loader
async function loadServerConfig() {
  try {
    const res = await fetch('/api/admin/config');
    if (res.ok) {
      state.config = await res.json();
    }
  } catch (e) {
    console.error('Config yuklashda xatolik:', e);
  }
}

// 2. Google Identity Services Setup
function setupGoogleAuth() {
  if (window.google && window.google.accounts && state.config && state.config.google_client_id) {
    google.accounts.id.initialize({
      client_id: state.config.google_client_id,
      callback: handleGoogleLoginResponse
    });

    const btnWrapper = document.getElementById('googleBtnContainer');
    if (btnWrapper) {
      btnWrapper.innerHTML = '';
      google.accounts.id.renderButton(btnWrapper, {
        theme: 'outline',
        size: 'large',
        text: 'signin_with',
        shape: 'rectangular',
        width: 320
      });
    }
  }
}

async function handleGoogleLoginResponse(response) {
  if (!response.credential) return;
  loginErrorMsg.style.display = 'none';

  try {
    const res = await fetch('/api/admin/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: response.credential })
    });

    const data = await res.json();
    if (res.ok && data.status === 'ok') {
      state.token = data.token;
      state.adminInfo = data.admin;
      localStorage.setItem('oqila_admin_token', data.token);
      showDashboard();
      showToast("Google orqali tizimga muvaffaqiyatli kirildi! ✨");
    } else {
      loginErrorMsg.textContent = data.detail || "Kirishda xatolik yuz berdi";
      loginErrorMsg.style.display = 'block';
    }
  } catch (err) {
    loginErrorMsg.textContent = "Server bilan bog'lanishda xatolik!";
    loginErrorMsg.style.display = 'block';
  }
}

// Quick Login (Email + Secret Key)
if (quickLoginForm) {
  quickLoginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    loginErrorMsg.style.display = 'none';

    const secretKey = adminKeyInput.value.trim();
    if (!secretKey) return;

    try {
      const res = await fetch('/api/admin/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: 'aliapisov11@gmail.com',
          secret_key: secretKey
        })
      });

      const data = await res.json();
      if (res.ok && data.status === 'ok') {
        state.token = data.token;
        state.adminInfo = data.admin;
        localStorage.setItem('oqila_admin_token', data.token);
        showDashboard();
        showToast("Xavfsiz tizimga muvaffaqiyatli kirildi! 👑");
      } else {
        loginErrorMsg.textContent = data.detail || "Noto'g'ri kalit kiritildi!";
        loginErrorMsg.style.display = 'block';
      }
    } catch (err) {
      loginErrorMsg.textContent = "Server bilan aloqa uzildi!";
      loginErrorMsg.style.display = 'block';
    }
  });
}

// Verify Session
async function verifySession() {
  try {
    const res = await fetch('/api/admin/me', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      const data = await res.json();
      state.adminInfo = data.admin;
      return true;
    }
  } catch (e) {
    console.warn('Sessiya xatosi:', e);
  }
  return false;
}

// UI Mode Switches
function showLogin() {
  stopLiveAutoRefresh();
  loginOverlay.style.display = 'flex';
  adminApp.style.display = 'none';
}

function showDashboard() {
  loginOverlay.style.display = 'none';
  adminApp.style.display = 'flex';

  if (state.adminInfo) {
    adminUserName.textContent = state.adminInfo.name || 'Ali (Admin)';
    adminUserEmail.textContent = state.adminInfo.email || 'aliapisov11@gmail.com';
    if (state.adminInfo.picture) {
      adminAvatarImg.src = state.adminInfo.picture;
    }
  }

  // Load all initial data
  loadStats();
  loadResumes();
  loadVacancies();
  loadReviews();

  // Start Real-Time Auto-Refresh
  startLiveAutoRefresh();
}

// Logout
if (btnLogout) {
  btnLogout.addEventListener('click', async () => {
    stopLiveAutoRefresh();
    try {
      await fetch('/api/admin/logout', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${state.token}` }
      });
    } catch (e) {}
    localStorage.removeItem('oqila_admin_token');
    state.token = '';
    state.adminInfo = null;
    showLogin();
    showToast("Tizimdan chiqildi");
  });
}

// Navigation Tabs
function setupTabs() {
  const navBtns = document.querySelectorAll('.admin-nav-btn');
  navBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      navBtns.forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.admin-tab-section').forEach(sec => sec.classList.remove('active'));

      btn.classList.add('active');
      const tabId = btn.getAttribute('data-tab');
      const targetSec = document.getElementById(tabId);
      if (targetSec) targetSec.classList.add('active');
      state.activeTab = tabId;
    });
  });

  const btnRefreshStats = document.getElementById('btnRefreshStats');
  if (btnRefreshStats) {
    btnRefreshStats.addEventListener('click', () => {
      loadStats();
      showToast("Statistika yangilandi 🔄");
    });
  }
}

// ==================== REAL-TIME LIVE AUTO-REFRESH & AUDIO CHIME ====================

function playNotificationChime() {
  try {
    const AudioCtx = window.AudioContext || window.webkitAudioContext;
    if (!AudioCtx) return;
    const ctx = new AudioCtx();
    if (ctx.state === 'suspended') {
      ctx.resume();
    }
    const osc = ctx.createOscillator();
    const gain = ctx.createGain();
    osc.connect(gain);
    gain.connect(ctx.destination);

    osc.type = 'sine';
    const t = ctx.currentTime;
    osc.frequency.setValueAtTime(587.33, t);        // D5
    osc.frequency.setValueAtTime(880.00, t + 0.12); // A5

    gain.gain.setValueAtTime(0, t);
    gain.gain.linearRampToValueAtTime(0.22, t + 0.04);
    gain.gain.exponentialRampToValueAtTime(0.001, t + 0.45);

    osc.start(t);
    osc.stop(t + 0.46);
  } catch (e) {
    console.debug("Audio chime skipped:", e);
  }
}

function startLiveAutoRefresh() {
  stopLiveAutoRefresh();
  state.pollTimer = setInterval(runLiveSync, 3500);
}

function stopLiveAutoRefresh() {
  if (state.pollTimer) {
    clearInterval(state.pollTimer);
    state.pollTimer = null;
  }
}

function renderStatsDisplay(s) {
  if (!s) return;
  const fEl = document.getElementById('statFarroshCount');
  const eEl = document.getElementById('statEnagaCount');
  const vEl = document.getElementById('statVacanciesCount');
  const rEl = document.getElementById('statAvgRating');
  const revEl = document.getElementById('statReviewsCount');

  if (fEl) fEl.textContent = s.farrosh_count || 0;
  if (eEl) eEl.textContent = s.enaga_count || 0;
  if (vEl) vEl.textContent = s.total_vacancies || 0;
  if (rEl) rEl.textContent = (s.avg_rating || 5.0).toFixed(1) + ' ⭐';
  if (revEl) revEl.textContent = `${s.total_reviews || 0} ta haqiqiy mijoz izohlari`;

  const br = document.getElementById('badgeResumesCount');
  const bv = document.getElementById('badgeVacanciesCount');
  const bw = document.getElementById('badgeReviewsCount');
  if (br) br.textContent = s.total_resumes || 0;
  if (bv) bv.textContent = s.total_vacancies || 0;
  if (bw) bw.textContent = s.total_reviews || 0;
}

async function runLiveSync() {
  if (!state.token || loginOverlay.style.display !== 'none') return;
  try {
    const res = await fetch('/api/admin/stats', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    const current = data.stats;
    const prev = state.lastStats;

    if (prev) {
      const newResumes = (current.total_resumes || 0) - (prev.total_resumes || 0);
      const newVacancies = (current.total_vacancies || 0) - (prev.total_vacancies || 0);
      const newReviews = (current.total_reviews || 0) - (prev.total_reviews || 0);

      if (newResumes > 0) {
        playNotificationChime();
        showToast(`🔔 Yangi nomzod anketasi keldi (+${newResumes})!`, 'success');
        if (state.activeTab === 'tabResumes') loadResumes(true);
      }
      if (newVacancies > 0) {
        playNotificationChime();
        showToast(`🔔 Yangi buyurtma keldi (+${newVacancies})!`, 'success');
        if (state.activeTab === 'tabVacancies') loadVacancies(true);
      }
      if (newReviews > 0) {
        playNotificationChime();
        showToast(`⭐ Yangi mijoz sharhi keldi (+${newReviews})!`, 'success');
        if (state.activeTab === 'tabReviews') loadReviews();
      }
    }

    state.lastStats = current;
    renderStatsDisplay(current);

    // Quiet sync of active table data
    const activeEl = document.activeElement;
    const isTyping = activeEl && (activeEl.id === 'resumeSearchInput' || activeEl.id === 'vacancySearchInput');
    if (!isTyping) {
      if (state.activeTab === 'tabResumes') {
        silentSyncResumes();
      } else if (state.activeTab === 'tabVacancies') {
        silentSyncVacancies();
      }
    }
  } catch (err) {
    console.debug('Live sync error:', err);
  }
}

async function silentSyncResumes() {
  const search = document.getElementById('resumeSearchInput')?.value.trim() || '';
  const profession = document.getElementById('resumeProfessionFilter')?.value || '';
  const is_busy = document.getElementById('resumeBusyFilter')?.value ?? '';
  const is_active = document.getElementById('resumeStatusFilter')?.value ?? '';

  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (profession) params.append('profession', profession);
  if (is_busy !== '') params.append('is_busy', is_busy);
  if (is_active !== '') params.append('is_active', is_active);

  try {
    const res = await fetch(`/api/admin/resumes?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    const newItems = data.data || [];
    const oldSig = JSON.stringify((state.resumes || []).map(r => ({ id: r.id, busy: r.is_busy, active: r.is_active })));
    const newSig = JSON.stringify(newItems.map(r => ({ id: r.id, busy: r.is_busy, active: r.is_active })));
    if (oldSig !== newSig) {
      state.resumes = newItems;
      renderResumesTable(state.resumes);
    }
  } catch (e) {
    console.debug('silentSyncResumes error:', e);
  }
}

async function silentSyncVacancies() {
  const search = document.getElementById('vacancySearchInput')?.value.trim() || '';
  const is_active = document.getElementById('vacancyStatusFilter')?.value ?? '';

  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (is_active !== '') params.append('is_active', is_active);

  try {
    const res = await fetch(`/api/admin/vacancies?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    const newItems = data.data || [];
    const oldSig = JSON.stringify((state.vacancies || []).map(v => ({ id: v.id, active: v.is_active })));
    const newSig = JSON.stringify(newItems.map(v => ({ id: v.id, active: v.is_active })));
    if (oldSig !== newSig) {
      state.vacancies = newItems;
      renderVacanciesTable(state.vacancies);
    }
  } catch (e) {
    console.debug('silentSyncVacancies error:', e);
  }
}

// ==================== DATA LOADERS ====================

// 1. STATS
async function loadStats() {
  try {
    const res = await fetch('/api/admin/stats', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    state.lastStats = data.stats;
    renderStatsDisplay(data.stats);
  } catch (e) {
    console.error('Stats xatosi:', e);
  }
}

// 2. RESUMES (NOMZODLAR)
async function loadResumes(highlightNew = false) {
  const search = document.getElementById('resumeSearchInput')?.value.trim() || '';
  const profession = document.getElementById('resumeProfessionFilter')?.value || '';
  const is_busy = document.getElementById('resumeBusyFilter')?.value ?? '';
  const is_active = document.getElementById('resumeStatusFilter')?.value ?? '';

  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (profession) params.append('profession', profession);
  if (is_busy !== '') params.append('is_busy', is_busy);
  if (is_active !== '') params.append('is_active', is_active);

  try {
    const res = await fetch(`/api/admin/resumes?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    state.resumes = data.data || [];
    renderResumesTable(state.resumes, highlightNew);
  } catch (e) {
    console.error('Resumes xatosi:', e);
  }
}

function renderResumesTable(list, highlightNew = false) {
  const tbody = document.getElementById('resumesTableBody');
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="9" class="empty-cell">Hech qanday nomzod anketasi topilmadi</td></tr>`;
    return;
  }

  tbody.innerHTML = list.map((item, idx) => {
    const profClass = item.profession.includes('Enaga') ? 'badge-enaga' : 'badge-farrosh';
    const profIcon = item.profession.includes('Enaga') ? '👶' : '🧹';
    const statusClass = item.is_active === 1 ? 'badge-active' : 'badge-inactive';
    const statusText = item.is_active === 1 ? '🟢 Faol' : '⚪️ Yashirilgan';
    const isBusy = Number(item.is_busy) === 1;
    const busyBadge = isBusy 
      ? '<span class="badge-pill badge-busy-admin">🔴 Band</span>' 
      : '<span class="badge-pill badge-available-admin">🟢 Bo\'sh</span>';
    const avatar = item.photo_url || (item.profession.includes('Enaga') 
      ? 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80'
      : 'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=120&q=80');

    const rowClass = (highlightNew && idx === 0) ? 'row-highlight-new' : '';

    return `
      <tr class="${rowClass}">
        <td>
          <div class="user-cell">
            <img src="${avatar}" alt="" class="user-cell-img">
            <div>
              <div class="user-cell-name">${escapeHtml(item.full_name)}</div>
              <div class="user-cell-id">ID: #${item.id}</div>
            </div>
          </div>
        </td>
        <td><span class="badge-pill ${profClass}">${profIcon} ${escapeHtml(item.profession)}</span></td>
        <td>
          <b>🎂 ${item.age || 35} yosh</b><br>
          <span style="color:var(--text-secondary);font-size:12px;">📍 ${escapeHtml(item.district || '')}</span>
        </td>
        <td>
          <b>${escapeHtml(item.expected_salary || "Kelishilgan")}</b><br>
          <span style="color:var(--text-muted);font-size:11px;">⏰ ${escapeHtml(item.work_type || 'Kunlik')}</span>
        </td>
        <td>
          <a href="tel:${item.phone}" style="color:var(--accent-orange);text-decoration:none;font-weight:600;">${escapeHtml(item.phone)}</a>
          ${item.telegram ? `<br><small style="color:var(--text-secondary);">@${escapeHtml(item.telegram.replace('@',''))}</small>` : ''}
        </td>
        <td>
          <b style="color:#F59E0B;">⭐ ${(item.avg_rating || 5.0).toFixed(1)}</b>
          <span style="font-size:11px;color:var(--text-muted);">(${item.reviews_count || 0})</span>
        </td>
        <td>${busyBadge}</td>
        <td><span class="badge-pill ${statusClass}">${statusText}</span></td>
        <td>
          <div class="action-btns">
            <button class="btn-action-icon btn-action-busy ${isBusy ? 'is-busy' : 'is-available'}" onclick="toggleResumeBusy(${item.id})" title="Bandlik holatini o'zgartirish">
              ${isBusy ? '🟢 Bo\'sh qilish' : '🔴 Band qilish'}
            </button>
            <button class="btn-action-icon btn-action-toggle" onclick="toggleResume(${item.id})" title="Holatini o'zgartirish">
              ${item.is_active === 1 ? '👁 Yashirish' : '🟢 Ko\'rsatish'}
            </button>
            <button class="btn-action-icon btn-action-delete" onclick="deleteResume(${item.id})" title="O'chirish">
              🗑
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

async function toggleResumeBusy(id) {
  try {
    const res = await fetch(`/api/admin/resumes/${id}/busy`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    const data = await res.json();
    if (res.ok) {
      showToast(data.message || `Anketa #${id} bandlik holati yangilandi!`);
      loadResumes();
    } else {
      showToast(data.detail || "Xatolik yuz berdi", "error");
    }
  } catch (e) {
    showToast("Xatolik yuz berdi", "error");
  }
}

async function toggleResume(id) {
  try {
    const res = await fetch(`/api/admin/resumes/${id}/toggle`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      showToast(`Anketa #${id} holati yangilandi!`);
      loadResumes();
      loadStats();
    }
  } catch (e) {
    showToast("Xatolik yuz berdi", "error");
  }
}

async function deleteResume(id) {
  if (!confirm(`Haqiqatdan ham #${id}-sonli anketani va unga tegishli barcha sharhlarni butunlay o'chirmoqchimisiz?`)) return;

  try {
    const res = await fetch(`/api/admin/resumes/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      showToast(`Anketa #${id} o'chirildi! 🗑`);
      loadResumes();
      loadStats();
    }
  } catch (e) {
    showToast("O'chirishda xatolik", "error");
  }
}

// 3. VACANCIES (BUYURTMALAR)
async function loadVacancies() {
  const search = document.getElementById('vacancySearchInput').value.trim();
  const is_active = document.getElementById('vacancyStatusFilter').value;

  const params = new URLSearchParams();
  if (search) params.append('search', search);
  if (is_active !== '') params.append('is_active', is_active);

  try {
    const res = await fetch(`/api/admin/vacancies?${params.toString()}`, {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    state.vacancies = data.data || [];
    renderVacanciesTable(state.vacancies);
  } catch (e) {
    console.error('Vacancies xatosi:', e);
  }
}

function renderVacanciesTable(list) {
  const tbody = document.getElementById('vacanciesTableBody');
  if (!list.length) {
    tbody.innerHTML = `<tr><td colspan="7" class="empty-cell">Hech qanday buyurtma topilmadi</td></tr>`;
    return;
  }

  tbody.innerHTML = list.map(item => {
    const statusClass = item.is_active === 1 ? 'badge-active' : 'badge-inactive';
    const statusText = item.is_active === 1 ? '🟢 Ochiq' : '⚪️ Yopilgan';

    return `
      <tr>
        <td>
          <div class="user-cell-name">${escapeHtml(item.title)}</div>
          <div class="user-cell-id">ID: #${item.id} | Sana: ${item.created_at ? item.created_at.substring(0, 10) : ''}</div>
        </td>
        <td><b>${escapeHtml(item.profession || 'Farrosh')}</b></td>
        <td>📍 ${escapeHtml(item.district || '')}</td>
        <td><b style="color:var(--accent-orange);">${escapeHtml(item.salary || '')}</b></td>
        <td>
          <a href="tel:${item.phone}" style="color:var(--text-main);font-weight:600;">${escapeHtml(item.phone)}</a>
          ${item.telegram ? `<br><small style="color:var(--text-secondary);">@${escapeHtml(item.telegram.replace('@',''))}</small>` : ''}
        </td>
        <td><span class="badge-pill ${statusClass}">${statusText}</span></td>
        <td>
          <div class="action-btns">
            <button class="btn-action-icon btn-action-toggle" onclick="toggleVacancy(${item.id})">
              ${item.is_active === 1 ? 'Yopish' : 'Ochish'}
            </button>
            <button class="btn-action-icon btn-action-delete" onclick="deleteVacancy(${item.id})">
              🗑
            </button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

async function toggleVacancy(id) {
  try {
    const res = await fetch(`/api/admin/vacancies/${id}/toggle`, {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      showToast(`Buyurtma #${id} holati o'zgartirildi!`);
      loadVacancies();
      loadStats();
    }
  } catch (e) {
    showToast("Xatolik", "error");
  }
}

async function deleteVacancy(id) {
  if (!confirm(`Haqiqatdan ham #${id}-sonli buyurtmani o'chirmoqchimisiz?`)) return;

  try {
    const res = await fetch(`/api/admin/vacancies/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      showToast(`Buyurtma #${id} o'chirildi! 🗑`);
      loadVacancies();
      loadStats();
    }
  } catch (e) {
    showToast("O'chirishda xatolik", "error");
  }
}

// 4. REVIEWS (SHARHLAR)
async function loadReviews() {
  try {
    const res = await fetch('/api/admin/reviews', {
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (!res.ok) return;
    const data = await res.json();
    state.reviews = data.data || [];
    renderReviewsGrid(state.reviews);
  } catch (e) {
    console.error('Reviews xatosi:', e);
  }
}

function renderReviewsGrid(list) {
  const container = document.getElementById('reviewsListGrid');
  if (!list.length) {
    container.innerHTML = `<div class="empty-placeholder" style="grid-column: 1/-1;text-align:center;padding:40px;color:var(--text-muted);">Mijozlar tomonidan qoldirilgan sharhlar mavjud emas</div>`;
    return;
  }

  container.innerHTML = list.map(rev => {
    const stars = '⭐'.repeat(rev.rating);
    return `
      <div class="review-admin-card">
        <div class="rev-header">
          <div>
            <div class="rev-target-worker">👩 ${escapeHtml(rev.worker_name || 'Ishchi')} <small style="color:var(--text-muted);font-weight:normal;">(${escapeHtml(rev.worker_profession || 'Xodim')})</small></div>
            <div style="font-size:11px;color:var(--text-muted);">ID: #${rev.id} | Ishchi ID: #${rev.worker_id}</div>
          </div>
          <div class="rev-stars">${stars} (${rev.rating}/5)</div>
        </div>

        <div class="rev-comment-text">"${escapeHtml(rev.comment)}"</div>

        <div class="rev-footer">
          <div class="rev-author">✍️ ${escapeHtml(rev.author_name || 'Mijoz')}</div>
          <button class="btn-action-icon btn-action-delete" onclick="deleteReview(${rev.id})">
            🗑 Sharhni o'chirish
          </button>
        </div>
      </div>
    `;
  }).join('');
}

async function deleteReview(id) {
  if (!confirm(`Haqiqatdan ham ushbu sharhni o'chirmoqchimisiz? Nomzodning umumiy yulduzchali reytingi avtomatik qayta hisoblanadi.`)) return;

  try {
    const res = await fetch(`/api/admin/reviews/${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${state.token}` }
    });
    if (res.ok) {
      showToast(`Sharh #${id} o'chirildi va reyting qayta hisoblandi! ⭐`);
      loadReviews();
      loadStats();
      loadResumes();
    }
  } catch (e) {
    showToast("Sharhni o'chirishda xatolik", "error");
  }
}

// Helpers
function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

function setupFilterListeners() {
  const resumeSearch = document.getElementById('resumeSearchInput');
  const resumeProf = document.getElementById('resumeProfessionFilter');
  const resumeBusy = document.getElementById('resumeBusyFilter');
  const resumeStatus = document.getElementById('resumeStatusFilter');

  if (resumeSearch) resumeSearch.addEventListener('input', debounce(loadResumes, 300));
  if (resumeProf) resumeProf.addEventListener('change', loadResumes);
  if (resumeBusy) resumeBusy.addEventListener('change', loadResumes);
  if (resumeStatus) resumeStatus.addEventListener('change', loadResumes);

  const vacSearch = document.getElementById('vacancySearchInput');
  const vacStatus = document.getElementById('vacancyStatusFilter');

  if (vacSearch) vacSearch.addEventListener('input', debounce(loadVacancies, 300));
  if (vacStatus) vacStatus.addEventListener('change', loadVacancies);
}

function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Expose globals for inline onclick
window.toggleResume = toggleResume;
window.toggleResumeBusy = toggleResumeBusy;
window.deleteResume = deleteResume;
window.toggleVacancy = toggleVacancy;
window.deleteVacancy = deleteVacancy;
window.deleteReview = deleteReview;
