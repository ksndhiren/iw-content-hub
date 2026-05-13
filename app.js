/**
 * IW Content Hub — app.js
 *
 * Responsibilities:
 *  - Fetch weeks.json and populate the week selector + post grid
 *  - Persist post statuses in localStorage
 *  - Open/close the post detail overlay
 *  - Drive the slide viewer (prev/next, keyboard nav)
 *  - Copy caption and hashtags to clipboard
 *
 * Pattern: IIFE to avoid polluting the global namespace.
 */
(function () {
  'use strict';

  /* -------------------------------------------------------------------------
     Constants
  ------------------------------------------------------------------------- */
  const DATA_URL      = 'data/weeks.json';
  const STORAGE_KEY   = 'iw-content-hub-statuses';
  const COMMENTS_KEY  = 'iw-content-hub-comments';

  /** Ordered list of status values for cycling on badge click */
  const STATUS_CYCLE  = ['in-review', 'approved', 'declined'];

  /** Human-readable labels for status values */
  const STATUS_LABELS = {
    'in-review': 'In Review',
    'approved':  'Approved',
    'declined':  'Declined',
  };

  /** Max hashtags to show per platform */
  const PLATFORM_HASHTAG_LIMIT = {
    'ig-fb':    5,
    'linkedin': 5,
    'x':        2,
    'threads':  5,
  };

  /** Platforms that show thread-style captions for carousel posts */
  const THREAD_PLATFORMS = ['x', 'threads'];

  /* -------------------------------------------------------------------------
     Module state
  ------------------------------------------------------------------------- */
  let allWeeks        = [];      // Full weeks array from JSON
  let currentWeek     = null;    // Currently displayed week object
  let statuses        = {};      // { postId: statusString } persisted in localStorage
  let comments        = {};      // { postId: [{ text, ts }] } persisted in localStorage
  let overlayPostId   = null;    // Post currently open in overlay
  let currentSlideIdx = 0;       // Zero-based slide index in overlay
  let currentPlatform = 'ig-fb'; // Active platform tab
  let currentHashtags = [];      // Hashtags currently displayed (platform-filtered)

  /* -------------------------------------------------------------------------
     DOM references (resolved once after DOMContentLoaded)
  ------------------------------------------------------------------------- */
  let elWeekSelector;
  let elWeekMeta;
  let elPostGrid;
  let elEmptyState;
  let elOverlay;
  let elOverlayBackdrop;
  let elOverlayClose;
  let elSlideImg;
  let elSlidePrev;
  let elSlideNext;
  let elSlideCounter;
  let elOverlayTitle;
  let elDetailDay;
  let elDetailPlatform;
  let elDetailStatus;
  let elDetailCaption;
  let elDetailHashtags;
  let elCopyCaptionBtn;
  let elCopyHashtagsBtn;
  let elDownloadSlideBtn;
  let elDownloadAllBtn;
  let elDownloadAllLabel;
  let elCommentList;
  let elCommentTextarea;
  let elCommentSubmitBtn;
  let elPlatformTabs;
  let elCaptionStandard;
  let elCaptionThread;
  let elThreadList;
  let elCopyThreadBtn;

  /* -------------------------------------------------------------------------
     Initialisation
  ------------------------------------------------------------------------- */
  function init() {
    resolveElements();
    loadStatuses();
    loadComments();
    fetchWeeks();
    bindGlobalEvents();
  }

  /** Cache all DOM references up front — avoids repeated querySelector calls */
  function resolveElements() {
    elWeekSelector    = document.getElementById('week-selector');
    elWeekMeta        = document.getElementById('week-meta');
    elPostGrid        = document.getElementById('post-grid');
    elEmptyState      = document.getElementById('empty-state');
    elOverlay         = document.getElementById('overlay');
    elOverlayBackdrop = document.getElementById('overlay-backdrop');
    elOverlayClose    = document.getElementById('overlay-close');
    elSlideImg        = document.getElementById('slide-img');
    elSlidePrev       = document.getElementById('slide-prev');
    elSlideNext       = document.getElementById('slide-next');
    elSlideCounter    = document.getElementById('slide-counter');
    elOverlayTitle    = document.getElementById('overlay-title');
    elDetailDay       = document.getElementById('detail-day');
    elDetailPlatform  = document.getElementById('detail-platform');
    elDetailStatus    = document.getElementById('detail-status');
    elDetailCaption   = document.getElementById('detail-caption');
    elDetailHashtags  = document.getElementById('detail-hashtags');
    elCopyCaptionBtn  = document.getElementById('copy-caption-btn');
    elCopyHashtagsBtn = document.getElementById('copy-hashtags-btn');
    elDownloadSlideBtn  = document.getElementById('download-slide-btn');
    elDownloadAllBtn    = document.getElementById('download-all-btn');
    elDownloadAllLabel  = document.getElementById('download-all-label');
    elCommentList       = document.getElementById('comment-list');
    elCommentTextarea   = document.getElementById('comment-textarea');
    elCommentSubmitBtn  = document.getElementById('comment-submit-btn');
    elPlatformTabs      = document.getElementById('platform-tabs');
    elCaptionStandard   = document.getElementById('caption-standard');
    elCaptionThread     = document.getElementById('caption-thread');
    elThreadList        = document.getElementById('thread-list');
    elCopyThreadBtn     = document.getElementById('copy-thread-btn');
  }

  /* -------------------------------------------------------------------------
     Data loading
  ------------------------------------------------------------------------- */
  function loadStatuses() {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      statuses = stored ? JSON.parse(stored) : {};
    } catch (_) {
      statuses = {};
    }
  }

  function saveStatuses() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(statuses));
    } catch (_) {
      // localStorage unavailable (private browsing etc.) - silently continue
    }
  }

  function loadComments() {
    try {
      const stored = localStorage.getItem(COMMENTS_KEY);
      comments = stored ? JSON.parse(stored) : {};
    } catch (_) {
      comments = {};
    }
  }

  function saveComments() {
    try {
      localStorage.setItem(COMMENTS_KEY, JSON.stringify(comments));
    } catch (_) {
      // localStorage unavailable - silently continue
    }
  }

  async function fetchWeeks() {
    try {
      const response = await fetch(DATA_URL);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      allWeeks = data.weeks || [];
      populateWeekSelector();
    } catch (err) {
      console.error('[IW Content Hub] Failed to load weeks.json:', err);
      elWeekMeta.innerHTML = '<span class="week-meta__label" style="color: var(--color-coral)">Failed to load data.</span>';
    }
  }

  /* -------------------------------------------------------------------------
     Week selector
  ------------------------------------------------------------------------- */
  function populateWeekSelector() {
    // Clear placeholder options
    elWeekSelector.innerHTML = '';

    if (allWeeks.length === 0) {
      const opt = document.createElement('option');
      opt.textContent = 'No weeks available';
      elWeekSelector.appendChild(opt);
      return;
    }

    allWeeks.forEach(function (week) {
      const opt = document.createElement('option');
      opt.value = week.id;
      opt.textContent = formatWC(week.weekCommencing) || week.label;
      elWeekSelector.appendChild(opt);
    });

    // Default to the first (most recent) week
    elWeekSelector.value = allWeeks[0].id;
    renderWeek(allWeeks[0].id);
  }

  function renderWeek(weekId) {
    const week = allWeeks.find(function (w) { return w.id === weekId; });
    if (!week) return;
    currentWeek = week;

    // Update meta bar
    const wcLabel = formatWC(week.weekCommencing);
    elWeekMeta.innerHTML = `
      <span class="week-meta__label">${escapeHtml(week.label)}</span>
      ${wcLabel ? `<span class="week-meta__date">${escapeHtml(wcLabel)}</span>` : ''}
    `;

    // Render cards
    renderPostGrid(week.posts || []);
  }

  /* -------------------------------------------------------------------------
     Post grid rendering
  ------------------------------------------------------------------------- */
  function renderPostGrid(posts) {
    elPostGrid.innerHTML = '';

    if (posts.length === 0) {
      elEmptyState.hidden = false;
      return;
    }

    elEmptyState.hidden = true;

    posts.forEach(function (post) {
      const card = buildPostCard(post);
      elPostGrid.appendChild(card);
    });
  }

  function buildPostCard(post) {
    const status     = getStatus(post.id, post.status);
    const thumbSrc   = buildImagePath(currentWeek.id, post.id, post.slides[0]);
    const slideCount = post.slides.length;

    // Outer wrapper — role="listitem" matches the grid's role="list"
    const article = document.createElement('article');
    article.className = 'post-card';
    article.setAttribute('role', 'listitem');
    article.setAttribute('tabindex', '0');
    article.setAttribute('aria-label', `${post.title}, ${STATUS_LABELS[status]}`);
    article.dataset.postId = post.id;

    article.innerHTML = `
      <div class="post-card__thumb">
        <img
          class="post-card__thumb-img"
          src="${thumbSrc}"
          alt="${escapeHtml(post.title)} — slide 1"
          loading="lazy"
          width="400"
          height="400"
        >
        ${slideCount > 1 ? `<span class="post-card__slide-pill" aria-label="${slideCount} slides">${slideCount} slides</span>` : ''}
      </div>
      <div class="post-card__body">
        <h2 class="post-card__title">${escapeHtml(post.title)}</h2>
        <div class="post-card__meta">
          <span class="day-label">${escapeHtml(post.day)}</span>
          <span class="platform-badge">${escapeHtml(post.platform)}</span>
        </div>
        <div class="post-card__status">
          <button
            class="status-badge status-badge--${status}"
            data-post-id="${post.id}"
            aria-label="Status: ${STATUS_LABELS[status]}. Click to cycle status."
          >${STATUS_LABELS[status]}</button>
        </div>
      </div>
    `;

    // Open overlay when card (but not the status badge) is clicked
    article.addEventListener('click', function (e) {
      // Let the badge handler deal with badge clicks
      if (e.target.closest('.status-badge')) return;
      openOverlay(post.id);
    });

    // Keyboard: Enter/Space to open overlay
    article.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        openOverlay(post.id);
      }
    });

    // Status badge click — cycle status
    const badge = article.querySelector('.status-badge');
    badge.addEventListener('click', function (e) {
      e.stopPropagation();
      cycleStatus(post.id, badge, article);
    });

    return article;
  }

  /* -------------------------------------------------------------------------
     Status management
  ------------------------------------------------------------------------- */
  function getStatus(postId, defaultStatus) {
    return statuses[postId] || defaultStatus;
  }

  function setStatus(postId, newStatus) {
    statuses[postId] = newStatus;
    saveStatuses();
  }

  function cycleStatus(postId, badgeEl, cardEl) {
    const current = getStatus(postId, 'in-review');
    const nextIdx = (STATUS_CYCLE.indexOf(current) + 1) % STATUS_CYCLE.length;
    const next    = STATUS_CYCLE[nextIdx];

    setStatus(postId, next);

    // Update badge appearance
    STATUS_CYCLE.forEach(function (s) { badgeEl.classList.remove('status-badge--' + s); });
    badgeEl.classList.add('status-badge--' + next);
    badgeEl.textContent = STATUS_LABELS[next];
    badgeEl.setAttribute('aria-label', `Status: ${STATUS_LABELS[next]}. Click to cycle status.`);

    // Update card aria-label
    const post = currentWeek && currentWeek.posts.find(function (p) { return p.id === postId; });
    if (post) {
      cardEl.setAttribute('aria-label', `${post.title}, ${STATUS_LABELS[next]}`);
    }

    // Sync with open overlay if same post
    if (overlayPostId === postId) {
      elDetailStatus.value = next;
    }
  }

  /* -------------------------------------------------------------------------
     Overlay
  ------------------------------------------------------------------------- */
  function openOverlay(postId) {
    const post = currentWeek && currentWeek.posts.find(function (p) { return p.id === postId; });
    if (!post) return;

    overlayPostId   = postId;
    currentSlideIdx = 0;

    // Populate sidebar content
    elOverlayTitle.textContent   = post.title;
    elDetailDay.textContent      = post.day;
    elDetailPlatform.textContent = post.platform;
    elDetailPlatform.className   = 'platform-badge';
    elDetailStatus.value         = getStatus(post.id, post.status);

    // Reset to default platform then render platform-aware content
    currentPlatform = 'ig-fb';
    updatePlatformTabs();
    renderCaptionForPlatform(post, currentPlatform);
    renderHashtagsForPlatform(post, currentPlatform);

    // Load first slide
    renderSlide(post, 0);

    // Load comments for this post
    renderComments(postId);
    elCommentTextarea.value = '';

    // Show overlay
    elOverlay.hidden = false;
    // Force reflow before adding class to trigger CSS transition
    void elOverlay.offsetWidth;
    elOverlay.classList.add('is-open');

    // Trap focus — move to close button
    elOverlayClose.focus();

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }

  function closeOverlay() {
    elOverlay.classList.remove('is-open');

    // Capture the id before clearing it so focus-return works
    const returningPostId = overlayPostId;

    // Wait for fade-out before hiding
    elOverlay.addEventListener('transitionend', function handler() {
      elOverlay.hidden = true;
      elOverlay.removeEventListener('transitionend', handler);
    });

    overlayPostId = null;
    document.body.style.overflow = '';

    // Return focus to the triggering card
    if (currentWeek && returningPostId) {
      const card = elPostGrid.querySelector(`[data-post-id="${returningPostId}"]`);
      if (card) card.focus();
    }
  }

  function renderSlide(post, idx) {
    const slide    = post.slides[idx];
    const src      = buildImagePath(currentWeek.id, post.id, slide);
    const total    = post.slides.length;

    elSlideImg.src = src;
    elSlideImg.alt = `${post.title} — slide ${idx + 1} of ${total}`;

    elSlideCounter.textContent = `${idx + 1} / ${total}`;

    elSlidePrev.disabled = (idx === 0);
    elSlideNext.disabled = (idx === total - 1);
  }

  function navigateSlide(direction) {
    if (!overlayPostId || !currentWeek) return;
    const post  = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;
    const total = post.slides.length;
    const next  = currentSlideIdx + direction;

    if (next < 0 || next >= total) return;

    currentSlideIdx = next;
    renderSlide(post, currentSlideIdx);
  }

  /* -------------------------------------------------------------------------
     Clipboard helpers
  ------------------------------------------------------------------------- */
  function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(function () {
      const original = button.textContent;
      button.textContent = 'Copied!';
      button.classList.add('is-copied');
      setTimeout(function () {
        button.textContent = original;
        button.classList.remove('is-copied');
      }, 2000);
    }).catch(function (err) {
      console.error('[IW Content Hub] Clipboard write failed:', err);
    });
  }

  /* -------------------------------------------------------------------------
     Downloads
  ------------------------------------------------------------------------- */
  function downloadCurrentSlide() {
    if (!overlayPostId || !currentWeek) return;
    const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;

    const url      = buildImagePath(currentWeek.id, post.id, post.slides[currentSlideIdx]);
    const filename = post.id + '_slide_' + (currentSlideIdx + 1) + '.png';

    fetch(url)
      .then(function (r) { return r.blob(); })
      .then(function (blob) {
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(a.href);
      })
      .catch(function (err) {
        console.error('[IW Content Hub] Download failed:', err);
      });
  }

  async function downloadAllSlides() {
    if (!overlayPostId || !currentWeek) return;
    const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;

    const isSingle = post.slides.length === 1;

    // Single slide - just download directly, no ZIP needed
    if (isSingle) {
      downloadCurrentSlide();
      return;
    }

    // Multi-slide - bundle as ZIP
    elDownloadAllBtn.disabled = true;
    elDownloadAllBtn.classList.add('is-downloading');
    elDownloadAllLabel.textContent = 'Preparing ZIP...';

    try {
      const zip     = new JSZip();
      const folder  = zip.folder(post.id);
      const total   = post.slides.length;

      for (let i = 0; i < total; i++) {
        elDownloadAllLabel.textContent = 'Downloading ' + (i + 1) + ' / ' + total + '...';
        const url      = buildImagePath(currentWeek.id, post.id, post.slides[i]);
        const response = await fetch(url);
        const blob     = await response.blob();
        folder.file('slide_' + (i + 1) + '.png', blob);
      }

      elDownloadAllLabel.textContent = 'Creating ZIP...';
      const content = await zip.generateAsync({ type: 'blob' });

      const a = document.createElement('a');
      a.href = URL.createObjectURL(content);
      a.download = post.id + '_slides.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(a.href);

      elDownloadAllLabel.textContent = 'Downloaded!';
      setTimeout(function () {
        elDownloadAllLabel.textContent = 'Download All Slides';
        elDownloadAllBtn.classList.remove('is-downloading');
        elDownloadAllBtn.disabled = false;
      }, 2000);

    } catch (err) {
      console.error('[IW Content Hub] ZIP download failed:', err);
      elDownloadAllLabel.textContent = 'Download All Slides';
      elDownloadAllBtn.classList.remove('is-downloading');
      elDownloadAllBtn.disabled = false;
    }
  }

  /* -------------------------------------------------------------------------
     Comments
  ------------------------------------------------------------------------- */
  function renderComments(postId) {
    elCommentList.innerHTML = '';
    const postComments = (comments[postId] || []);

    postComments.forEach(function (c) {
      const item = document.createElement('div');
      item.className = 'comment-item';

      const meta = document.createElement('div');
      meta.className = 'comment-item__meta';
      meta.textContent = formatCommentDate(c.ts);

      const text = document.createElement('div');
      text.className = 'comment-item__text';
      text.textContent = c.text;

      item.appendChild(meta);
      item.appendChild(text);
      elCommentList.appendChild(item);
    });

    // Scroll to bottom so newest comment is visible
    if (postComments.length > 0) {
      elCommentList.lastElementChild.scrollIntoView({ block: 'nearest' });
    }
  }

  function addComment(postId, text) {
    if (!postId || !text.trim()) return;

    if (!comments[postId]) comments[postId] = [];
    comments[postId].push({ text: text.trim(), ts: Date.now() });
    saveComments();
    renderComments(postId);
  }

  function formatCommentDate(ts) {
    const d = new Date(ts);
    return d.toLocaleDateString('en-GB', {
      day: 'numeric', month: 'short', year: 'numeric',
      hour: '2-digit', minute: '2-digit',
    });
  }

  /* -------------------------------------------------------------------------
     Event binding
  ------------------------------------------------------------------------- */
  function bindGlobalEvents() {
    // Week selector change
    elWeekSelector.addEventListener('change', function () {
      renderWeek(elWeekSelector.value);
    });

    // Overlay: close button
    elOverlayClose.addEventListener('click', closeOverlay);

    // Overlay: click on the backdrop (outside the panel) to close
    elOverlayBackdrop.addEventListener('click', closeOverlay);

    // Slide prev/next
    elSlidePrev.addEventListener('click', function () { navigateSlide(-1); });
    elSlideNext.addEventListener('click', function () { navigateSlide(+1); });

    // Status dropdown change in overlay
    elDetailStatus.addEventListener('change', function () {
      if (!overlayPostId) return;
      const newStatus = elDetailStatus.value;
      setStatus(overlayPostId, newStatus);

      // Reflect in the card grid
      const badge = elPostGrid.querySelector(`.status-badge[data-post-id="${overlayPostId}"]`);
      if (badge) {
        const card  = badge.closest('.post-card');
        STATUS_CYCLE.forEach(function (s) { badge.classList.remove('status-badge--' + s); });
        badge.classList.add('status-badge--' + newStatus);
        badge.textContent = STATUS_LABELS[newStatus];
        badge.setAttribute('aria-label', `Status: ${STATUS_LABELS[newStatus]}. Click to cycle status.`);

        if (card) {
          const post = currentWeek && currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
          if (post) card.setAttribute('aria-label', `${post.title}, ${STATUS_LABELS[newStatus]}`);
        }
      }
    });

    // Copy caption
    elCopyCaptionBtn.addEventListener('click', function () {
      if (!overlayPostId || !currentWeek) return;
      const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
      if (post) copyToClipboard(post.caption, elCopyCaptionBtn);
    });

    // Copy hashtags (copies only the platform-filtered set currently shown)
    elCopyHashtagsBtn.addEventListener('click', function () {
      if (currentHashtags.length) copyToClipboard(currentHashtags.join(' '), elCopyHashtagsBtn);
    });

    // Submit comment via button
    elCommentSubmitBtn.addEventListener('click', function () {
      if (!overlayPostId) return;
      addComment(overlayPostId, elCommentTextarea.value);
      elCommentTextarea.value = '';
      elCommentTextarea.focus();
    });

    // Submit comment via Ctrl+Enter / Cmd+Enter in textarea
    elCommentTextarea.addEventListener('keydown', function (e) {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        if (!overlayPostId) return;
        addComment(overlayPostId, elCommentTextarea.value);
        elCommentTextarea.value = '';
      }
    });

    // Platform tab clicks
    elPlatformTabs.querySelectorAll('.platform-tab').forEach(function (btn) {
      btn.addEventListener('click', function () { switchPlatform(btn.dataset.platform); });
    });

    // Copy full thread
    elCopyThreadBtn.addEventListener('click', function () {
      if (!overlayPostId || !currentWeek) return;
      const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
      if (post && post.captionThread) copyToClipboard(post.captionThread.join('\n\n'), elCopyThreadBtn);
    });

    // Download current slide
    elDownloadSlideBtn.addEventListener('click', downloadCurrentSlide);

    // Download all slides (ZIP for multi-slide, direct for single)
    elDownloadAllBtn.addEventListener('click', downloadAllSlides);

    // Keyboard navigation
    document.addEventListener('keydown', function (e) {
      if (elOverlay.hidden) return;

      if (e.key === 'Escape') {
        closeOverlay();
      } else if (e.key === 'ArrowLeft') {
        navigateSlide(-1);
      } else if (e.key === 'ArrowRight') {
        navigateSlide(+1);
      }
    });
  }

  /* -------------------------------------------------------------------------
     Utility: build image path
  ------------------------------------------------------------------------- */
  function buildImagePath(weekId, postId, filename) {
    return `images/${weekId}/${postId}/${filename}`;
  }

  /* -------------------------------------------------------------------------
     Platform switching
  ------------------------------------------------------------------------- */
  function switchPlatform(platform) {
    currentPlatform = platform;
    updatePlatformTabs();
    if (!overlayPostId || !currentWeek) return;
    const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;
    renderCaptionForPlatform(post, platform);
    renderHashtagsForPlatform(post, platform);
  }

  function updatePlatformTabs() {
    elPlatformTabs.querySelectorAll('.platform-tab').forEach(function (btn) {
      const active = btn.dataset.platform === currentPlatform;
      btn.classList.toggle('is-active', active);
      btn.setAttribute('aria-selected', String(active));
    });
  }

  function renderCaptionForPlatform(post, platform) {
    const isCarousel       = post.slides.length > 1;
    const isThreadPlatform = THREAD_PLATFORMS.includes(platform);
    const hasThread        = isCarousel && isThreadPlatform &&
                             Array.isArray(post.captionThread) && post.captionThread.length > 0;

    if (hasThread) {
      elCaptionStandard.hidden = true;
      elCaptionThread.hidden   = false;
      renderThreadList(post.captionThread);
    } else {
      elCaptionStandard.hidden = false;
      elCaptionThread.hidden   = true;
      elDetailCaption.textContent = post.caption;
    }
  }

  function renderHashtagsForPlatform(post, platform) {
    const limit     = PLATFORM_HASHTAG_LIMIT[platform] || 5;
    currentHashtags = (post.hashtags || []).slice(0, limit);

    elDetailHashtags.innerHTML = '';
    currentHashtags.forEach(function (tag) {
      const pill = document.createElement('span');
      pill.className   = 'hashtag-pill';
      pill.textContent = tag;
      elDetailHashtags.appendChild(pill);
    });
  }

  function renderThreadList(tweets) {
    elThreadList.innerHTML = '';
    tweets.forEach(function (tweet, i) {
      const charCount = tweet.length;
      const isOver    = charCount > 280;

      const item = document.createElement('div');
      item.className = 'thread-item';
      item.innerHTML =
        '<div class="thread-item__header">' +
          '<span class="thread-item__num">' + (i + 1) + '</span>' +
          '<span class="thread-item__chars' + (isOver ? ' is-over' : '') + '">' + charCount + '/280</span>' +
          '<button class="thread-item__copy" data-idx="' + i + '" aria-label="Copy post ' + (i + 1) + '">Copy</button>' +
        '</div>' +
        '<div class="thread-item__text">' + escapeHtml(tweet) + '</div>';

      elThreadList.appendChild(item);
    });

    // Bind individual copy buttons
    elThreadList.querySelectorAll('.thread-item__copy').forEach(function (btn) {
      btn.addEventListener('click', function () {
        if (!overlayPostId || !currentWeek) return;
        const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
        if (!post || !post.captionThread) return;
        copyToClipboard(post.captionThread[parseInt(btn.dataset.idx, 10)], btn);
      });
    });
  }

  /**
   * Format a week-commencing ISO date string (YYYY-MM-DD) as "w/c 11th May"
   * Falls back to the raw string if parsing fails.
   */
  function formatWC(dateStr) {
    if (!dateStr) return '';
    const d = new Date(dateStr + 'T00:00:00Z');
    if (isNaN(d)) return dateStr;
    const day   = d.getUTCDate();
    const month = d.toLocaleDateString('en-GB', { month: 'long', timeZone: 'UTC' });
    return 'w/c ' + ordinal(day) + ' ' + month;
  }

  /** Return number with English ordinal suffix — 1st, 2nd, 3rd, 4th … 11th … 21st */
  function ordinal(n) {
    const mod100 = n % 100;
    const mod10  = n % 10;
    if (mod100 >= 11 && mod100 <= 13) return n + 'th';
    if (mod10 === 1) return n + 'st';
    if (mod10 === 2) return n + 'nd';
    if (mod10 === 3) return n + 'rd';
    return n + 'th';
  }

  /** Minimal HTML escaping to avoid XSS from JSON data */
  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#39;');
  }

  /* -------------------------------------------------------------------------
     Bootstrap
  ------------------------------------------------------------------------- */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
