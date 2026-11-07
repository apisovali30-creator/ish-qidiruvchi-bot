// ==========================================================================
// TELEGRAM MINI APP - CLIENT ENGINE (FARROSH VA ENAGA PLATFORMASI V9.0)
// Specialized Platform for Domestic Cleaners & Nannies with Ratings & Reviews
// ==========================================================================

document.addEventListener("DOMContentLoaded", () => {
  const tg = window.Telegram?.WebApp;
  if (tg) {
    try {
      tg.ready();
      tg.expand();
      tg.setHeaderColor?.("#f6f8f7");
      tg.setBackgroundColor?.("#f6f8f7");
    } catch (e) {
      console.log("Telegram init error:", e);
    }
  }

  // Telegram User or Fallback Demo User
  const tgUser = tg?.initDataUnsafe?.user || {
    id: 1001,
    first_name: "Ali",
    username: "aliapisov"
  };

  // High-Definition Photography Co-optimized for Cleaners & Nannies
  const categoryCovers = {
    "Farrosh": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80",
    "Enaga": "https://images.unsplash.com/photo-1544717305-2782549b5136?auto=format&fit=crop&w=600&q=80",
    "Buyurtmalar": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=600&q=80",
    "Default": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=600&q=80"
  };

  // Avatars for Social Proof
  const sampleAvatars = [
    "https://images.unsplash.com/photo-1534528741775-53994a69daeb?auto=format&fit=crop&w=120&q=80",
    "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=120&q=80",
    "https://images.unsplash.com/photo-1494790108377-be9c29b29330?auto=format&fit=crop&w=120&q=80",
    "https://images.unsplash.com/photo-1517841905240-472988babdf9?auto=format&fit=crop&w=120&q=80"
  ];

  // State Management
  const state = {
    currentTab: "home", // "home" | "explore" | "wizard" | "profile"
    exploreMode: "Farrosh", // "Farrosh" | "Enaga" | "vacancies"
    selectedDistrict: "Hammasi",
    selectedWorkType: "Hammasi",
    searchQuery: "",
    districts: [],
    workTypes: [],
    vacancies: [],
    resumes: [],
    myPosts: { vacancies: [], resumes: [] },
    
    // Review Modal State
    activeWorkerForReview: null,
    selectedRating: 5,

    // Wizard (Savol-Javob Anketa) State
    wizard: {
      currentStep: 1,
      totalSteps: 5,
      postType: "resume", // "resume" (xodim) | "vacancy" (mijoz)
      profession: "Farrosh", // "Farrosh" | "Enaga"
      title: "", // Ism yoki E'lon sarlavhasi
      age: 35,
      district: "",
      workType: "Kunlik (Bir martalik)",
      salary: "",
      phone: "",
      telegram: "",
      description: ""
    }
  };

  // DOM Elements - Navigation & Header
  const headerUserName = document.getElementById("headerUserName");
  const viewHome = document.getElementById("viewHome");
  const viewExplore = document.getElementById("viewExplore");
  const viewWizard = document.getElementById("viewWizard");
  const viewProfile = document.getElementById("viewProfile");
  const dockTabs = document.querySelectorAll(".dock-tab");

  // Screen 1 (Home) Controls
  const topIndustryCarousel = document.getElementById("topIndustryCarousel");
  const startWizardBtn = document.getElementById("startWizardBtn");
  const btnServicesViewAll = document.getElementById("btnServicesViewAll");
  const btnFeaturedViewAll = document.getElementById("btnFeaturedViewAll");
  const mainCardsGrid = document.getElementById("mainCardsGrid");

  // Screen 2 (Explore) Controls
  const exploreHeaderTitle = document.getElementById("exploreHeaderTitle");
  const exploreSegFarrosh = document.getElementById("exploreSegFarrosh");
  const exploreSegEnaga = document.getElementById("exploreSegEnaga");
  const exploreSegVacancies = document.getElementById("exploreSegVacancies");
  const exploreSearchInput = document.getElementById("exploreSearchInput");
  const exploreClearSearch = document.getElementById("exploreClearSearch");
  const exploreRegionSelect = document.getElementById("exploreRegionSelect");
  const exploreFilterChips = document.getElementById("exploreFilterChips");
  const exploreCardsGrid = document.getElementById("exploreCardsGrid");

  // Wizard Elements
  const stepBadgeNum = document.getElementById("stepBadgeNum");
  const stepBadgeTitle = document.getElementById("stepBadgeTitle");
  const stepFillBar = document.getElementById("stepFillBar");
  const tileResume = document.getElementById("tileResume");
  const tileVacancy = document.getElementById("tileVacancy");

  const wizProfSelector = document.getElementById("wizProfSelector");
  const wizQ2Title = document.getElementById("wizQ2Title");
  const wizQ2Desc = document.getElementById("wizQ2Desc");
  const wizLblJobTitle = document.getElementById("wizLblJobTitle");
  const inputWizTitle = document.getElementById("inputWizTitle");
  const wizAgeGroup = document.getElementById("wizAgeGroup");
  const inputWizAge = document.getElementById("inputWizAge");

  const inputWizRegion = document.getElementById("inputWizRegion");
  const wizWorkTypePills = document.getElementById("wizWorkTypePills");
  const wizLblSalary = document.getElementById("wizLblSalary");
  const inputWizSalary = document.getElementById("inputWizSalary");

  const inputWizPhone = document.getElementById("inputWizPhone");
  const inputWizTelegram = document.getElementById("inputWizTelegram");
  const wizLblDesc = document.getElementById("wizLblDesc");
  const inputWizDesc = document.getElementById("inputWizDesc");
  const wizPreviewCard = document.getElementById("wizPreviewCard");

  const btnWizBack = document.getElementById("btnWizBack");
  const btnWizNext = document.getElementById("btnWizNext");
  const btnWizSubmit = document.getElementById("btnWizSubmit");

  // Profile Elements
  const profileCardName = document.getElementById("profileCardName");
  const profileCardHandle = document.getElementById("profileCardHandle");
  const profVacCount = document.getElementById("profVacCount");
  const profResCount = document.getElementById("profResCount");
  const myAdsGrid = document.getElementById("myAdsGrid");

  // Detail Sheet Modal Elements
  const detailSheetModal = document.getElementById("detailSheetModal");
  const sheetDetailBody = document.getElementById("sheetDetailBody");
  const floatingToast = document.getElementById("floatingToast");

  // Review Modal Elements
  const reviewModal = document.getElementById("reviewModal");
  const closeReviewModalBtn = document.getElementById("closeReviewModalBtn");
  const modalWorkerNameText = document.getElementById("modalWorkerNameText");
  const starPickerRow = document.getElementById("starPickerRow");
  const reviewScoreLabel = document.getElementById("reviewScoreLabel");
  const inputReviewAuthor = document.getElementById("inputReviewAuthor");
  const inputReviewComment = document.getElementById("inputReviewComment");
  const btnSubmitReview = document.getElementById("btnSubmitReview");

  // User Profile Name & Handle
  const displayName = tgUser.first_name || "Mehmon";
  headerUserName.textContent = displayName;
  profileCardName.textContent = displayName;
  profileCardHandle.textContent = tgUser.username ? `@${tgUser.username}` : `ID: ${tgUser.id}`;
  if (tgUser.username) {
    inputWizTelegram.value = `@${tgUser.username}`;
    state.wizard.telegram = `@${tgUser.username}`;
  }
  inputReviewAuthor.value = displayName;

  // --- TELEGRAM PROFILE AVATAR MANAGEMENT ---
  function loadUserAvatar(user, name) {
    const headerImg = document.getElementById("userHeaderImg");
    const headerFallback = document.getElementById("userHeaderFallback");
    const profileImg = document.getElementById("profileUserAvatarImg");
    const profileFallback = document.getElementById("profileAvatarFallback");

    const initial = (name || "A").trim().charAt(0).toUpperCase();
    if (headerFallback) headerFallback.textContent = initial;
    if (profileFallback) profileFallback.textContent = initial;

    function applyAvatar(src) {
      if (headerImg) {
        headerImg.onload = () => {
          headerImg.style.display = "block";
          if (headerFallback) headerFallback.style.display = "none";
        };
        headerImg.src = src;
      }
      if (profileImg) {
        profileImg.onload = () => {
          profileImg.style.display = "block";
          if (profileFallback) profileFallback.style.display = "none";
        };
        profileImg.src = src;
      }
    }

    if (user && user.photo_url) {
      applyAvatar(user.photo_url);
      return;
    }

    if (user && user.id) {
      const avatarEndpoint = `/api/user-avatar/${user.id}`;
      const probe = new Image();
      probe.onload = () => applyAvatar(avatarEndpoint);
      probe.onerror = () => {
        if (headerImg) headerImg.style.display = "none";
        if (profileImg) profileImg.style.display = "none";
        if (headerFallback) headerFallback.style.display = "flex";
        if (profileFallback) profileFallback.style.display = "flex";
      };
      probe.src = avatarEndpoint;
    }
  }

  loadUserAvatar(tgUser, displayName);

  // --- INITIAL DATA FETCHING ---
  async function fetchInitData() {
    try {
      const [distRes, workRes] = await Promise.all([
        fetch("/api/districts"),
        fetch("/api/work-types")
      ]);
      state.districts = await distRes.json();
      state.workTypes = await workRes.json();

      renderExploreDistricts();
      renderWizardDropdowns();

      await Promise.all([loadFeaturedWorkers(), loadResumes(), loadVacancies(), loadMyPosts()]);
      handleHashRouting();
    } catch (err) {
      console.error("Initialization error:", err);
      showToast("Ma'lumotlarni yuklashda xatolik yuz berdi");
    }
  }

  function renderExploreDistricts() {
    exploreRegionSelect.innerHTML = '<option value="Hammasi">📍 Barcha tumanlar (Toshkent va viloyatlar)</option>';
    state.districts.forEach(dist => {
      const opt = document.createElement("option");
      opt.value = dist;
      opt.textContent = `📍 ${dist}`;
      exploreRegionSelect.appendChild(opt);
    });
  }

  function renderWizardDropdowns() {
    inputWizRegion.innerHTML = '<option value="" disabled selected>Tumanni tanlang</option>';
    state.districts.forEach(dist => {
      const opt = document.createElement("option");
      opt.value = dist;
      opt.textContent = dist;
      inputWizRegion.appendChild(opt);
    });
  }

  function formatDisplaySalary(raw) {
    if (!raw) return "Kelishilgan";
    let s = String(raw).trim();
    s = s.replace(/(\d+)\s+500\s+000\s+so'm/gi, "$1.5 mln so'm");
    s = s.replace(/(\d+)\s+500\s+000/g, "$1.5 mln so'm");
    s = s.replace(/(\d+)\s+000\s+000\s+so'm/gi, "$1 mln so'm");
    s = s.replace(/(\d+)\s+000\s+000/g, "$1 mln so'm");
    return s;
  }

  // --- CARD RENDERING (2-COLUMN GRID) ---
  function createCard(type, item) {
    const isWorker = type === "resume";
    const prof = item.profession || (isWorker ? "Farrosh" : "Buyurtma");
    const coverUrl = categoryCovers[prof] || categoryCovers["Farrosh"];
    const title = isWorker ? item.full_name : item.title;
    const districtText = (item.district || "Toshkent").replace(" tumani", "").replace(" shahri", "");
    const rawSalary = isWorker ? (item.expected_salary || "Kelishilgan") : item.salary;
    const salary = formatDisplaySalary(rawSalary);

    const card = document.createElement("div");
    card.className = "ref-job-card";

    let badgeHtml = "";
    let tagsHtml = "";

    if (isWorker) {
      const avgRating = Number(item.avg_rating || 5.0).toFixed(1);
      const revCount = item.reviews_count || 0;
      badgeHtml = `
        <span class="card-category-badge">${prof === 'Enaga' ? '👶 Enaga' : '🧹 Farrosh'}</span>
        <span class="card-rating-badge">⭐ ${avgRating} (${revCount})</span>
      `;
      tagsHtml = `
        <div class="card-tags-row">
          <span class="card-age-tag">🎂 ${item.age || 35} yosh</span>
          <span class="card-district-tag">📍 ${escapeHtml(districtText)}</span>
        </div>
      `;
    } else {
      badgeHtml = `
        <span class="card-category-badge">📋 Buyurtma</span>
      `;
      tagsHtml = `
        <div class="card-tags-row">
          <span class="card-district-tag">📍 ${escapeHtml(districtText)}</span>
          <span class="card-age-tag">⏰ ${escapeHtml((item.work_type || 'Kunlik').split(' ')[0])}</span>
        </div>
      `;
    }

    card.innerHTML = `
      <div class="card-cover-wrap">
        <img src="${coverUrl}" class="card-cover-img" alt="${escapeHtml(title)}" loading="lazy">
        ${badgeHtml}
      </div>
      <div class="card-body-wrap">
        <h4 class="card-title-text">${escapeHtml(title)}</h4>
        ${tagsHtml}
        <div class="card-footer-row" style="margin-top: 10px;">
          <span class="card-salary-bold" title="${escapeHtml(rawSalary)}">${escapeHtml(salary)}</span>
          <div class="avatar-cluster">
            <img src="${sampleAvatars[0]}" alt="User">
            <img src="${sampleAvatars[1]}" alt="User">
            <img src="${sampleAvatars[2]}" alt="User">
          </div>
        </div>
      </div>
    `;

    card.addEventListener("click", () => openDetailSheet(type, item));
    return card;
  }

  // --- DATA LOADING ---
  // --- DATA LOADING ---
  let allFeaturedWorkers = [];
  async function loadFeaturedWorkers() {
    try {
      const res = await fetch("/api/resumes");
      const data = await res.json();
      allFeaturedWorkers = data.data || [];
      renderMainFeaturedCards();
    } catch (err) {
      console.error("loadFeaturedWorkers error:", err);
    }
  }

  async function loadResumes() {
    try {
      const params = new URLSearchParams();
      if (state.exploreMode === "Farrosh") params.append("profession", "Farrosh");
      else if (state.exploreMode === "Enaga") params.append("profession", "Enaga");
      
      if (state.selectedDistrict !== "Hammasi") params.append("district", state.selectedDistrict);
      if (state.selectedWorkType !== "Hammasi") params.append("work_type", state.selectedWorkType);
      if (state.searchQuery) params.append("search", state.searchQuery);

      const res = await fetch(`/api/resumes?${params.toString()}`);
      const data = await res.json();
      state.resumes = data.data || [];
      if (state.exploreMode === "Farrosh" || state.exploreMode === "Enaga") {
        renderExploreCards();
      }
    } catch (err) {
      console.error("loadResumes error:", err);
    }
  }

  async function loadVacancies() {
    try {
      const params = new URLSearchParams();
      if (state.selectedDistrict !== "Hammasi") params.append("district", state.selectedDistrict);
      if (state.selectedWorkType !== "Hammasi") params.append("work_type", state.selectedWorkType);
      if (state.searchQuery) params.append("search", state.searchQuery);

      const res = await fetch(`/api/vacancies?${params.toString()}`);
      const data = await res.json();
      state.vacancies = data.data || [];
      if (state.exploreMode === "vacancies") {
        renderExploreCards();
      }
    } catch (err) {
      console.error("loadVacancies error:", err);
    }
  }

  function renderMainFeaturedCards() {
    mainCardsGrid.innerHTML = "";
    if (allFeaturedWorkers.length === 0) {
      mainCardsGrid.innerHTML = `
        <div class="empty-state-box">
          <span class="empty-icon">🧹</span>
          <h4>Xodimlar topilmadi</h4>
          <p>Birinchi bo'lib anketa qoldiring!</p>
        </div>
      `;
      return;
    }

    // Top rated workers on Home
    allFeaturedWorkers.slice(0, 8).forEach(r => {
      mainCardsGrid.appendChild(createCard("resume", r));
    });
  }

  function renderExploreCards() {
    exploreCardsGrid.innerHTML = "";
    let items = [];
    let type = "resume";

    if (state.exploreMode === "vacancies") {
      items = state.vacancies;
      type = "vacancy";
    } else {
      items = state.resumes;
      type = "resume";
    }

    if (items.length === 0) {
      const label = state.exploreMode === "vacancies" ? "Buyurtmalar" : (state.exploreMode === "Enaga" ? "Enagalar" : "Farroshlar");
      exploreCardsGrid.innerHTML = `
        <div class="empty-state-box">
          <span class="empty-icon">🔍</span>
          <h4>Mos ${label} topilmadi</h4>
          <p>Filtrlarni o'zgartirib ko'ring yoki birinchi bo'lib e'lon joylang!</p>
        </div>
      `;
      return;
    }

    items.forEach(item => {
      exploreCardsGrid.appendChild(createCard(type, item));
    });
  }

  async function loadMyPosts() {
    try {
      const res = await fetch(`/api/my-posts?user_id=${tgUser.id}`);
      const data = await res.json();
      state.myPosts = data.data || { vacancies: [], resumes: [] };
      profVacCount.textContent = state.myPosts.vacancies.length;
      profResCount.textContent = state.myPosts.resumes.length;
      renderMyPostsGrid();
    } catch (err) {
      console.error("loadMyPosts error:", err);
    }
  }

  function renderMyPostsGrid() {
    myAdsGrid.innerHTML = "";
    const allMy = [
      ...state.myPosts.resumes.map(r => ({ ...r, _type: 'resume' })),
      ...state.myPosts.vacancies.map(v => ({ ...v, _type: 'vacancy' }))
    ];

    if (allMy.length === 0) {
      myAdsGrid.innerHTML = `
        <div class="empty-state-box">
          <span class="empty-icon">📂</span>
          <p>Siz hali hech qanday anketa yoki e'lon joylashtirmagansiz.</p>
        </div>
      `;
      return;
    }

    allMy.forEach(item => {
      myAdsGrid.appendChild(createCard(item._type, item));
    });
  }

  // --- DETAIL SHEET MODAL (WITH RATINGS & REVIEWS) ---
  async function openDetailSheet(type, item) {
    hapticImpact();
    const isWorker = type === "resume";
    const prof = item.profession || (isWorker ? "Farrosh" : "Buyurtma");
    const coverUrl = categoryCovers[prof] || categoryCovers["Farrosh"];
    const title = isWorker ? item.full_name : item.title;
    const salary = isWorker ? (item.expected_salary || "Kelishilgan") : item.salary;
    const description = isWorker ? (item.bio || "Batafsil ma'lumot berilmagan") : (item.description || "Batafsil ma'lumot berilmagan");

    let workerMetaHtml = "";
    let reviewsSectionHtml = "";

    if (isWorker) {
      const avgRating = Number(item.avg_rating || 5.0).toFixed(1);
      const revCount = item.reviews_count || 0;

      workerMetaHtml = `
        <div class="sheet-meta-tags-row">
          <span class="sheet-meta-pill">
            <span>Yoshi:</span>
            <strong>🎂 ${item.age || 35} yosh</strong>
          </span>
          <span class="sheet-meta-pill">
            <span>Tuman:</span>
            <strong>📍 ${escapeHtml(item.district)}</strong>
          </span>
          <span class="sheet-meta-pill">
            <span>Tartib:</span>
            <strong>⏰ ${escapeHtml(item.work_type || 'Kunlik')}</strong>
          </span>
          <span class="sheet-meta-pill">
            <span>Tajriba:</span>
            <strong>⏳ ${escapeHtml(item.experience_years || '2 yil tajriba')}</strong>
          </span>
        </div>
      `;

      reviewsSectionHtml = `
        <div class="sheet-reviews-section">
          <div class="sheet-reviews-header">
            <h4 class="sheet-reviews-title">
              <span>⭐ Mijozlar izohlari</span>
              <span style="color: #b45309; font-size: 13px;">(${avgRating} / 5.0)</span>
            </h4>
            <button type="button" class="btn-open-review-modal" id="btnOpenReviewSheetModal">
              <span>✍️ Izoh qoldirish</span>
            </button>
          </div>
          <div id="sheetReviewsList">
            <div class="skeleton-shimmer-card" style="height: 70px;"></div>
          </div>
        </div>
      `;
    } else {
      workerMetaHtml = `
        <div class="sheet-meta-tags-row">
          <span class="sheet-meta-pill">
            <span>Kerakli xodim:</span>
            <strong>${prof === 'Enaga' ? '👶 Enaga' : '🧹 Farrosh'}</strong>
          </span>
          <span class="sheet-meta-pill">
            <span>Tuman:</span>
            <strong>📍 ${escapeHtml(item.district)}</strong>
          </span>
          <span class="sheet-meta-pill">
            <span>Tartib:</span>
            <strong>⏰ ${escapeHtml(item.work_type || 'Kunlik')}</strong>
          </span>
        </div>
      `;
    }

    sheetDetailBody.innerHTML = `
      <div class="sheet-hero-img-wrap">
        <img src="${coverUrl}" class="sheet-hero-cover-img" alt="${escapeHtml(title)}">
        <button class="sheet-floating-close-btn" id="modalCloseBtn">✕</button>
      </div>

      <div class="sheet-content-padding">
        <span class="sheet-category-tag">${isWorker ? (prof === 'Enaga' ? '👶 Enaga (Bolalar qarovi)' : '🧹 Farrosh (Tozalik ustasi)') : '📋 Mijoz buyurtmasi'}</span>
        <h3 class="sheet-main-title">${escapeHtml(title)}</h3>
        <p class="sheet-org-subtitle">📍 ${escapeHtml(item.district)} • ${escapeHtml(item.work_type || 'Kunlik')}</p>

        ${workerMetaHtml}

        <h4 class="sheet-section-title" style="margin-top: 16px;">${isWorker ? 'Xodim haqida' : 'Talablar va shartlar'}</h4>
        <p class="sheet-desc-text">${escapeHtml(description)}</p>

        <div class="sheet-fee-highlight-box">
          <div class="sheet-fee-meta">
            <span class="sheet-fee-label">${isWorker ? 'Kutilayotgan haq:' : 'Taklif qilingan haq:'}</span>
          </div>
          <span class="sheet-fee-bold-amount">${escapeHtml(salary)}</span>
        </div>

        <a href="tel:${escapeHtml(item.phone)}" class="sheet-giant-orange-cta" onclick="hapticImpact()">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>
          <span>Bog'lanish (${escapeHtml(item.phone)})</span>
        </a>

        ${item.telegram ? `
          <a href="https://t.me/${item.telegram.replace('@', '')}" target="_blank" class="sheet-tg-cta" onclick="hapticImpact()">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
            <span>Telegram orqali yozish</span>
          </a>
        ` : ""}

        ${reviewsSectionHtml}
      </div>
    `;

    document.getElementById("modalCloseBtn")?.addEventListener("click", () => {
      detailSheetModal.classList.remove("active");
    });

    if (isWorker) {
      document.getElementById("btnOpenReviewSheetModal")?.addEventListener("click", () => {
        openReviewModal(item);
      });
      loadWorkerReviews(item.id);
    }

    detailSheetModal.classList.add("active");
  }

  async function loadWorkerReviews(workerId) {
    const listEl = document.getElementById("sheetReviewsList");
    if (!listEl) return;

    try {
      const res = await fetch(`/api/workers/${workerId}/reviews`);
      const data = await res.json();
      const reviews = data.data || [];

      if (reviews.length === 0) {
        listEl.innerHTML = `
          <div class="review-empty-state">
            <span>💬 Hali hech kim izoh qoldirmagan. Birinchi bo'lib baholang!</span>
          </div>
        `;
        return;
      }

      listEl.innerHTML = "";
      reviews.forEach(r => {
        const itemCard = document.createElement("div");
        itemCard.className = "review-item-card";
        const starsText = "★".repeat(r.rating) + "☆".repeat(5 - r.rating);
        itemCard.innerHTML = `
          <div class="review-item-header">
            <span class="review-author-name">👤 ${escapeHtml(r.author_name)}</span>
            <span class="review-stars-gold">${starsText}</span>
          </div>
          <p class="review-comment-text">"${escapeHtml(r.comment)}"</p>
        `;
        listEl.appendChild(itemCard);
      });
    } catch (err) {
      console.error("loadWorkerReviews error:", err);
      listEl.innerHTML = '<p style="color:#ef4444; font-size:12px;">Izohlarni yuklashda xatolik yuz berdi.</p>';
    }
  }

  // --- REVIEW MODAL LOGIC ---
  function openReviewModal(worker) {
    hapticImpact();
    state.activeWorkerForReview = worker;
    modalWorkerNameText.textContent = worker.full_name;
    inputReviewComment.value = "";
    setReviewRating(5);
    reviewModal.classList.add("open");
  }

  function closeReviewModal() {
    reviewModal.classList.remove("open");
  }

  function setReviewRating(rating) {
    state.selectedRating = rating;
    const labels = [
      "",
      "Yomon (1 yulduz) ⭐",
      "Qoniqarsiz (2 yulduz) ⭐⭐",
      "O'rtacha (3 yulduz) ⭐⭐⭐",
      "Yaxshi (4 yulduz) ⭐⭐⭐⭐",
      "A'lo (5 yulduz) ⭐⭐⭐⭐⭐"
    ];
    reviewScoreLabel.textContent = labels[rating] || `${rating} yulduz`;

    starPickerRow.querySelectorAll(".star-pick-btn").forEach(btn => {
      const btnRating = parseInt(btn.dataset.rating, 10);
      btn.classList.toggle("active", btnRating <= rating);
    });
  }

  starPickerRow.querySelectorAll(".star-pick-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      hapticImpact();
      const r = parseInt(btn.dataset.rating, 10);
      setReviewRating(r);
    });
  });

  closeReviewModalBtn.addEventListener("click", closeReviewModal);
  reviewModal.addEventListener("click", (e) => {
    if (e.target === reviewModal) closeReviewModal();
  });

  btnSubmitReview.addEventListener("click", async () => {
    if (!state.activeWorkerForReview) return;
    const author = inputReviewAuthor.value.trim() || displayName;
    const comment = inputReviewComment.value.trim();

    if (!comment || comment.length < 3) {
      showToast("Iltimos, izoh matnini yozing (kamida 3 belgi)");
      return;
    }

    hapticImpact();
    btnSubmitReview.disabled = true;
    btnSubmitReview.textContent = "Yuborilmoqda...";

    try {
      const res = await fetch("/api/reviews", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          worker_id: state.activeWorkerForReview.id,
          author_name: author,
          author_user_id: tgUser.id,
          rating: state.selectedRating,
          comment: comment
        })
      });
      const data = await res.json();

      if (data.status === "ok") {
        hapticNotification("success");
        showToast("🎉 Rahmat! Izohingiz muvaffaqiyatli saqlandi!");
        closeReviewModal();
        await loadResumes();
        await loadWorkerReviews(state.activeWorkerForReview.id);
      } else {
        showToast(data.detail || "Izoh yuborishda xatolik");
      }
    } catch (e) {
      showToast("Server bilan bog'lanishda xatolik");
    } finally {
      btnSubmitReview.disabled = false;
      btnSubmitReview.textContent = "⭐ Bahoni yuborish";
    }
  });

  detailSheetModal.addEventListener("click", (e) => {
    if (e.target === detailSheetModal) detailSheetModal.classList.remove("active");
  });

  // --- TAB NAVIGATION ENGINE ---
  function switchTab(targetTab, profFilter = null) {
    hapticImpact();
    state.currentTab = targetTab;

    dockTabs.forEach(t => {
      let isTarget = t.dataset.nav === targetTab;
      if (targetTab === "explore" && profFilter) {
        isTarget = isTarget && t.dataset.prof === profFilter;
      }
      t.classList.toggle("active", isTarget);
    });

    [viewHome, viewExplore, viewWizard, viewProfile].forEach(v => v.classList.remove("active"));

    if (targetTab === "home") {
      viewHome.classList.add("active");
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (targetTab === "explore") {
      viewExplore.classList.add("active");
      if (profFilter) {
        setExploreMode(profFilter);
      } else {
        renderExploreCards();
      }
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (targetTab === "wizard") {
      viewWizard.classList.add("active");
      resetWizard();
      window.scrollTo({ top: 0, behavior: "smooth" });
    } else if (targetTab === "profile") {
      viewProfile.classList.add("active");
      loadMyPosts();
      window.scrollTo({ top: 0, behavior: "smooth" });
    }
  }

  function setExploreMode(mode) {
    state.exploreMode = mode;
    exploreHeaderTitle.textContent = mode === "vacancies" ? "Buyurtmalar" : (mode === "Enaga" ? "Enagalar" : "Farroshlar");
    exploreSegFarrosh.classList.toggle("active", mode === "Farrosh");
    exploreSegEnaga.classList.toggle("active", mode === "Enaga");
    exploreSegVacancies.classList.toggle("active", mode === "vacancies");
    if (mode === "vacancies") {
      loadVacancies();
    } else {
      loadResumes();
    }
  }

  dockTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      const nav = tab.dataset.nav;
      const prof = tab.dataset.prof || null;
      switchTab(nav, prof);
    });
  });

  // Home Quick Filter Pills
  topIndustryCarousel.querySelectorAll(".prayer-pill-item").forEach(item => {
    item.addEventListener("click", () => {
      hapticImpact();
      topIndustryCarousel.querySelectorAll(".prayer-pill-item").forEach(p => p.classList.remove("active"));
      item.classList.add("active");
      const prof = item.dataset.prof;
      if (prof === "Hammasi") {
        state.exploreMode = "Farrosh";
        switchTab("explore", "Farrosh");
      } else if (prof === "Buyurtmalar") {
        switchTab("explore", "vacancies");
      } else {
        switchTab("explore", prof);
      }
    });
  });

  // Home Services Squircles
  document.querySelectorAll(".squircle-service-item").forEach(item => {
    item.addEventListener("click", () => {
      const action = item.dataset.action;
      if (action === "farrosh") {
        switchTab("explore", "Farrosh");
      } else if (action === "enaga") {
        switchTab("explore", "Enaga");
      } else if (action === "wizard") {
        switchTab("wizard");
      } else if (action === "vacancies") {
        switchTab("explore", "vacancies");
      } else if (action === "profile") {
        switchTab("profile");
      }
    });
  });

  btnServicesViewAll?.addEventListener("click", () => switchTab("explore", "Farrosh"));
  btnFeaturedViewAll?.addEventListener("click", () => switchTab("explore", "Farrosh"));
  startWizardBtn?.addEventListener("click", () => switchTab("wizard"));

  // Explore Segmented Controls
  exploreSegFarrosh.addEventListener("click", () => {
    hapticImpact();
    setExploreMode("Farrosh");
  });

  exploreSegEnaga.addEventListener("click", () => {
    hapticImpact();
    setExploreMode("Enaga");
  });

  exploreSegVacancies.addEventListener("click", () => {
    hapticImpact();
    setExploreMode("vacancies");
  });

  // Explore Search
  let searchDebounce;
  exploreSearchInput.addEventListener("input", (e) => {
    const val = e.target.value.trim();
    state.searchQuery = val;
    exploreClearSearch.style.display = val ? "block" : "none";
    clearTimeout(searchDebounce);
    searchDebounce = setTimeout(() => {
      loadResumes();
      loadVacancies();
    }, 300);
  });

  exploreClearSearch.addEventListener("click", () => {
    exploreSearchInput.value = "";
    state.searchQuery = "";
    exploreClearSearch.style.display = "none";
    loadResumes();
    loadVacancies();
  });

  // Explore District Select
  exploreRegionSelect.addEventListener("change", (e) => {
    state.selectedDistrict = e.target.value;
    loadResumes();
    loadVacancies();
  });

  // Explore Work Type Chips
  exploreFilterChips.querySelectorAll(".cat-chip-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      hapticImpact();
      exploreFilterChips.querySelectorAll(".cat-chip-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.selectedWorkType = btn.dataset.wtype;
      loadResumes();
      loadVacancies();
    });
  });

  // --- WIZARD / ANKETA (5-STEP QUESTION FLOW) ---
  function resetWizard() {
    state.wizard.currentStep = 1;
    state.wizard.postType = "resume";
    state.wizard.profession = "Farrosh";
    state.wizard.title = "";
    state.wizard.age = 35;
    state.wizard.district = "";
    state.wizard.workType = "Kunlik (Bir martalik)";
    state.wizard.salary = "";
    state.wizard.phone = "";
    state.wizard.description = "";

    tileResume.classList.add("active");
    tileVacancy.classList.remove("active");
    inputWizTitle.value = "";
    inputWizAge.value = "35";
    inputWizRegion.value = "";
    inputWizSalary.value = "";
    inputWizPhone.value = "";
    inputWizDesc.value = "";

    wizProfSelector.querySelectorAll(".wiz-gender-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.prof === "Farrosh");
    });

    wizWorkTypePills.querySelectorAll(".wiz-gender-btn").forEach(b => {
      b.classList.toggle("active", b.dataset.wtype === "Kunlik (Bir martalik)");
    });

    updateWizardQuestionsCopy();
    goToStep(1);
  }

  function goToStep(step) {
    state.wizard.currentStep = step;
    stepBadgeNum.textContent = `${step} / 5-qadam`;
    stepFillBar.style.width = `${(step / 5) * 100}%`;

    const titles = [
      "E'lon turini tanlang",
      "Kasb va Shaxsiy ma'lumotlar",
      "Tuman va Ish tartibi",
      "Aloqa va Ma'lumot",
      "Tasdiqlash va Preview"
    ];
    stepBadgeTitle.textContent = titles[step - 1];

    for (let i = 1; i <= 5; i++) {
      const stepEl = document.getElementById(`wStep${i}`);
      stepEl.classList.toggle("active", i === step);
    }

    btnWizBack.style.display = step > 1 ? "flex" : "none";
    btnWizNext.style.display = step < 5 ? "flex" : "none";
    btnWizSubmit.style.display = step === 5 ? "flex" : "none";

    if (step === 5) renderWizardPreview();
  }

  tileResume.addEventListener("click", () => {
    hapticImpact();
    tileResume.classList.add("active");
    tileVacancy.classList.remove("active");
    state.wizard.postType = "resume";
    updateWizardQuestionsCopy();
  });

  tileVacancy.addEventListener("click", () => {
    hapticImpact();
    tileVacancy.classList.add("active");
    tileResume.classList.remove("active");
    state.wizard.postType = "vacancy";
    updateWizardQuestionsCopy();
  });

  wizProfSelector.querySelectorAll(".wiz-gender-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      hapticImpact();
      wizProfSelector.querySelectorAll(".wiz-gender-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.wizard.profession = btn.dataset.prof;
      updateWizardQuestionsCopy();
    });
  });

  wizWorkTypePills.querySelectorAll(".wiz-gender-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      hapticImpact();
      wizWorkTypePills.querySelectorAll(".wiz-gender-btn").forEach(b => b.classList.remove("active"));
      btn.classList.add("active");
      state.wizard.workType = btn.dataset.wtype;
    });
  });

  function updateWizardQuestionsCopy() {
    const isWorker = state.wizard.postType === "resume";
    const profName = state.wizard.profession === "Enaga" ? "Enaga" : "Farrosh";

    wizQ2Title.textContent = isWorker ? "Kasb va Shaxsiy ma'lumotlar" : "Kerakli xodim va Taklif";
    wizQ2Desc.textContent = isWorker ? `Siz ${profName} sifatida anketa to'ldiryapsiz:` : `Sizga ${profName} kerakmi? Talablaringizni kiriting:`;
    wizLblJobTitle.textContent = isWorker ? "To'liq ism va familiyangiz *" : "E'lon sarlavhasi (Masalan: Xonadonga farrosh kerak) *";
    inputWizTitle.placeholder = isWorker ? "Masalan: Dilnoza opa Karimova" : `Masalan: ${profName} kerak xonadonimizga`;

    if (wizAgeGroup) {
      wizAgeGroup.style.display = isWorker ? "block" : "none";
    }

    wizLblSalary.textContent = isWorker ? "Kutilayotgan xizmat haqi *" : "Taklif etilayotgan xizmat haqi *";
    wizLblDesc.textContent = isWorker ? "O'zingiz va tajribangiz haqida ma'lumot" : "Qo'shimcha talablar va qulayliklar";
  }

  document.querySelectorAll(".q-chip").forEach(chip => {
    chip.addEventListener("click", () => {
      hapticImpact();
      inputWizSalary.value = chip.textContent;
      state.wizard.salary = chip.textContent;
    });
  });

  btnWizNext.addEventListener("click", () => {
    hapticImpact();
    const cur = state.wizard.currentStep;

    if (cur === 1) {
      goToStep(2);
    } else if (cur === 2) {
      const title = inputWizTitle.value.trim();
      if (!title) {
        showToast(state.wizard.postType === "resume" ? "Iltimos, ismingizni kiriting" : "Iltimos, sarlavhani kiriting");
        return;
      }
      state.wizard.title = title;
      if (state.wizard.postType === "resume") {
        const ageVal = parseInt(inputWizAge.value, 10);
        if (!ageVal || ageVal < 18 || ageVal > 75) {
          showToast("Iltimos, haqiqiy yoshingizni kiriting (18-75)");
          return;
        }
        state.wizard.age = ageVal;
      }
      goToStep(3);
    } else if (cur === 3) {
      const district = inputWizRegion.value;
      const salary = inputWizSalary.value.trim();
      if (!district) {
        showToast("Iltimos, tuman yoki hududni tanlang");
        return;
      }
      if (!salary) {
        showToast("Iltimos, narx yoki kutilayotgan haqni kiriting");
        return;
      }
      state.wizard.district = district;
      state.wizard.salary = salary;
      goToStep(4);
    } else if (cur === 4) {
      const phone = inputWizPhone.value.trim();
      if (!phone) {
        showToast("Iltimos, telefon raqamingizni kiriting");
        return;
      }
      state.wizard.phone = phone;
      state.wizard.telegram = inputWizTelegram.value.trim();
      state.wizard.description = inputWizDesc.value.trim();
      goToStep(5);
    }
  });

  btnWizBack.addEventListener("click", () => {
    hapticImpact();
    if (state.wizard.currentStep > 1) {
      goToStep(state.wizard.currentStep - 1);
    }
  });

  function renderWizardPreview() {
    const isWorker = state.wizard.postType === "resume";
    const prof = state.wizard.profession;
    const coverUrl = categoryCovers[prof] || categoryCovers["Farrosh"];
    const districtText = (state.wizard.district || "Toshkent").replace(" tumani", "");

    wizPreviewCard.innerHTML = `
      <div class="card-cover-wrap">
        <img src="${coverUrl}" class="card-cover-img" alt="Preview">
        <span class="card-category-badge">${prof === 'Enaga' ? '👶 Enaga' : '🧹 Farrosh'}</span>
        ${isWorker ? `<span class="card-rating-badge">⭐ Yangi</span>` : '<span class="card-category-badge">📋 Buyurtma</span>'}
      </div>
      <div class="card-body-wrap">
        <h4 class="card-title-text">${escapeHtml(state.wizard.title)}</h4>
        <div class="card-tags-row">
          ${isWorker ? `<span class="card-age-tag">🎂 ${state.wizard.age} yosh</span>` : ''}
          <span class="card-district-tag">📍 ${escapeHtml(districtText)}</span>
          <span class="card-age-tag">⏰ ${(state.wizard.workType || 'Kunlik').split(' ')[0]}</span>
        </div>
        <div class="card-footer-row" style="margin-top: 10px;">
          <span class="card-salary-bold">${escapeHtml(state.wizard.salary)}</span>
          <div class="avatar-cluster">
            <img src="${sampleAvatars[0]}" alt="User">
            <img src="${sampleAvatars[1]}" alt="User">
          </div>
        </div>
      </div>
    `;
  }

  btnWizSubmit.addEventListener("click", async () => {
    hapticImpact();
    btnWizSubmit.disabled = true;
    btnWizSubmit.innerHTML = "<span>Yuklanmoqda...</span>";

    const isWorker = state.wizard.postType === "resume";
    const endpoint = isWorker ? "/api/resumes" : "/api/vacancies";

    const payload = isWorker ? {
      user_id: tgUser.id,
      full_name: state.wizard.title,
      profession: state.wizard.profession,
      age: state.wizard.age,
      district: state.wizard.district,
      work_type: state.wizard.workType,
      expected_salary: state.wizard.salary,
      experience_years: "Tajribali xodim",
      phone: state.wizard.phone,
      telegram: state.wizard.telegram,
      bio: state.wizard.description
    } : {
      user_id: tgUser.id,
      title: state.wizard.title,
      profession: state.wizard.profession,
      district: state.wizard.district,
      work_type: state.wizard.workType,
      salary: state.wizard.salary,
      phone: state.wizard.phone,
      telegram: state.wizard.telegram,
      description: state.wizard.description
    };

    try {
      const res = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();

      if (data.status === "ok") {
        hapticNotification("success");
        showToast("🎉 E'loningiz muvaffaqiyatli joylashtirildi!");
        await Promise.all([loadResumes(), loadVacancies(), loadMyPosts()]);
        if (isWorker) {
          switchTab("explore", state.wizard.profession);
        } else {
          switchTab("explore", "vacancies");
        }
      } else {
        showToast(data.detail || "Xatolik yuz berdi");
        hapticNotification("error");
      }
    } catch (err) {
      showToast("Server bilan bog'lanishda xatolik");
      hapticNotification("error");
    } finally {
      btnWizSubmit.disabled = false;
      btnWizSubmit.innerHTML = "<span>🚀 E'lonni joylash</span>";
    }
  });

  // --- URL HASH ROUTING ---
  function handleHashRouting() {
    const hash = window.location.hash.toLowerCase();
    if (hash === "#farrosh") {
      switchTab("explore", "Farrosh");
    } else if (hash === "#enaga") {
      switchTab("explore", "Enaga");
    } else if (hash === "#vacancies" || hash === "#buyurtmalar") {
      switchTab("explore", "vacancies");
    } else if (hash === "#create" || hash === "#anketa") {
      switchTab("wizard");
    } else if (hash === "#profile") {
      switchTab("profile");
    }
  }

  window.addEventListener("hashchange", handleHashRouting);

  // --- UTILITIES ---
  function showToast(text) {
    floatingToast.textContent = text;
    floatingToast.classList.add("show");
    setTimeout(() => { floatingToast.classList.remove("show"); }, 3200);
  }

  function hapticImpact() {
    try { tg?.HapticFeedback?.impactOccurred("medium"); } catch(e) {}
  }

  function hapticNotification(type) {
    try { tg?.HapticFeedback?.notificationOccurred(type); } catch(e) {}
  }

  function escapeHtml(str) {
    if (!str) return "";
    return String(str)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  fetchInitData();
});
