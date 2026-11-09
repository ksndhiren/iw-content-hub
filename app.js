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
  const IS_LOCAL      = ['localhost', '127.0.0.1'].includes(location.hostname);
  const USE_LOCAL_IMAGES = new URLSearchParams(location.search).has('localImages');
  const IMAGE_BASE    = USE_LOCAL_IMAGES ? '' : 'https://pub-5f843c240ef6453bba67e131500424af.r2.dev';
  const FEATURED_URL  = 'data/featured.json';
  const SHORTS_URL    = 'data/shorts.json';
  const ANALYTICS_URL = 'data/analytics.json';
  const FEATURED_SEEN_KEY = 'iw-content-hub-featured-seen';
  const STATUS_API    = '/api/statuses';   // shared cross-device status store
  const STORAGE_KEY   = 'iw-content-hub-statuses';
  const COMMENTS_KEY  = 'iw-content-hub-comments';

  /** Ordered list of status values for cycling on badge click */
  const STATUS_CYCLE  = ['script-ready', 'in-review', 'approved', 'declined'];

  /** Human-readable labels for status values */
  const STATUS_LABELS = {
    'in-review': 'In Review',
    'script-ready': 'Script Ready',
    'approved':  'Approved',
    'declined':  'Declined',
  };

  /** Max hashtags to show per platform */
  const PLATFORM_HASHTAG_LIMIT = {
    'ig-fb':    5,
    'linkedin': 5,
    'x':        2,
  };

  /** Platforms that show thread-style captions for carousel posts */
  const THREAD_PLATFORMS = ['x'];

  /* -------------------------------------------------------------------------
     Module state
  ------------------------------------------------------------------------- */
  let allWeeks        = [];      // Full weeks array from JSON
  let currentDayLabel = null;    // when set, the day-grid is drilled into that day
  let featuredWeek    = null;    // Featured Jobs pseudo-week (from featured.json)
  let shortsWeek      = null;    // Shorts/Reels pseudo-week (from shorts.json)
  let analyticsData   = null;    // Ayrshare analytics summary (from analytics.json)
  let analyticsRange  = { mode: 'current', start: null, end: null }; // date filter
  let currentMode     = 'weekly';// 'weekly' | 'shorts' | 'featured' | 'analytics'
  let featuredSeen    = new Set();// auto-post ids the user has already seen (localStorage)
  let featuredNewIds  = new Set();// auto-post ids new since last visit (for badge + ribbon)
  let currentWeek     = null;    // Currently displayed week object
  let statuses        = {};      // { postId: statusString } persisted in localStorage
  let comments        = {};      // { postId: [{ text, ts }] } persisted in localStorage
  let overlayPostId   = null;    // Post currently open in overlay
  let currentSlideIdx = 0;       // Zero-based slide index in overlay
  let currentPlatform = 'ig-fb'; // Active platform tab
  let currentHashtags = [];      // Hashtags currently displayed (platform-filtered)
  let currentCaption  = '';      // Caption text currently displayed (platform-specific)

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
  let elContentSidebar;
  let elModeTabs;
  let elModeWeekly;
  let elModeShorts;
  let elModeFeatured;
  let elModeAnalytics;
  let elFeaturedBadge;
  let elAnalyticsView;

  /* -------------------------------------------------------------------------
     Initialisation
  ------------------------------------------------------------------------- */
  function init() {
    resolveElements();
    loadStatuses();
    loadComments();
    loadFeaturedSeen();
    fetchWeeks();
    fetchShorts();
    fetchFeatured();
    fetchAnalytics();
    fetchRemoteStatuses();   // pull shared statuses, then refresh what's on screen
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
    elContentSidebar    = document.getElementById('content-sidebar');
    elModeTabs          = document.getElementById('mode-tabs');
    elModeWeekly        = document.getElementById('mode-weekly');
    elModeShorts        = document.getElementById('mode-shorts');
    elModeFeatured      = document.getElementById('mode-featured');
    elModeAnalytics     = document.getElementById('mode-analytics');
    elFeaturedBadge     = document.getElementById('featured-badge');
    elAnalyticsView     = document.getElementById('analytics-view');
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
      const response = await fetch(DATA_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();
      // Latest week first, so the newest w/c is the default landing view and
      // sits at the top of the selector. Order by week number, then w/c date.
      allWeeks = (data.weeks || []).slice().sort(function (a, b) {
        var an = parseInt(String(a.id).replace(/\D/g, ''), 10) || 0;
        var bn = parseInt(String(b.id).replace(/\D/g, ''), 10) || 0;
        if (an !== bn) return bn - an;
        return (b.weekCommencing || '').localeCompare(a.weekCommencing || '');
      });
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

    currentDayLabel = null;
    renderWeekMeta(week);
    renderDays(week);
  }

  function renderWeekMeta(week, dayLabel) {
    const wcLabel = formatWC(week.weekCommencing);
    elWeekMeta.innerHTML = `
      <span class="week-meta__label">${escapeHtml(week.label)}</span>
      ${wcLabel ? `<span class="week-meta__date">${escapeHtml(wcLabel)}</span>` : ''}
      ${dayLabel ? `<span class="week-meta__day">${escapeHtml(dayLabel)}</span>` : ''}
    `;
  }

  /* Group a week's posts into days, preserving first-seen order. */
  function groupByDay(posts) {
    const order = [];
    const map = {};
    (posts || []).forEach(function (p) {
      const d = p.day || 'Unscheduled';
      if (!map[d]) { map[d] = []; order.push(d); }
      map[d].push(p);
    });
    return order.map(function (d) { return { day: d, posts: map[d] }; });
  }

  /* Render the week as DAY cards; clicking a day drills into its posts. */
  function renderDays(week) {
    currentDayLabel = null;
    elPostGrid.innerHTML = '';
    const days = groupByDay(week.posts);
    if (days.length === 0) { elEmptyState.hidden = false; return; }
    elEmptyState.hidden = true;
    days.forEach(function (grp) {
      elPostGrid.appendChild(buildDayCard(week, grp.day, grp.posts));
    });
  }

  function buildDayCard(week, dayLabel, dayPosts) {
    const article = document.createElement('article');
    article.className = 'post-card day-card';
    article.setAttribute('role', 'listitem');
    article.setAttribute('tabindex', '0');
    article.setAttribute('aria-label', `${dayLabel}, ${dayPosts.length} posts`);

    const thumbs = dayPosts.slice(0, 4).map(function (p) {
      const s = (p.slides || [])[0];
      const src = p.thumbnailPath || (s ? buildImagePath(week.id, p.id, s) : '');
      return src
        ? `<img class="day-card__cell" src="${src}" alt="" loading="lazy">`
        : `<div class="day-card__cell day-card__cell--empty"></div>`;
    }).join('');

    const lanes = dayPosts.map(function (p) {
      const lane = p.lane || 'post';
      return `<span class="lane-chip lane-chip--${escapeHtml(lane)}">${escapeHtml(laneLabel(lane))}</span>`;
    }).join('');

    article.innerHTML = `
      <div class="post-card__thumb day-card__thumb">
        <div class="day-card__grid">${thumbs}</div>
        <span class="post-card__slide-pill">${dayPosts.length} posts</span>
      </div>
      <div class="post-card__body">
        <h2 class="post-card__title">${escapeHtml(dayLabel)}</h2>
        <div class="post-card__meta day-card__lanes">${lanes}</div>
      </div>
    `;

    article.addEventListener('click', function () { openDay(week, dayLabel, dayPosts); });
    article.addEventListener('keydown', function (e) {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openDay(week, dayLabel, dayPosts); }
    });
    return article;
  }

  function laneLabel(lane) {
    const labels = {
      engagement: 'Poll',
      fun: 'Fun',
      infographic: 'Infographic',
      employer_guide: 'Employer guide'
    };
    return labels[lane] || lane;
  }

  /* Drill into one day: show its posts, with a back-to-days control. */
  function openDay(week, dayLabel, dayPosts) {
    currentDayLabel = dayLabel;
    renderWeekMeta(week, dayLabel);
    elPostGrid.innerHTML = '';
    elEmptyState.hidden = true;

    const back = document.createElement('button');
    back.type = 'button';
    back.className = 'grid-back';
    back.innerHTML = '&larr; All days';
    back.addEventListener('click', function () { renderWeekMeta(week); renderDays(week); });
    elPostGrid.appendChild(back);

    dayPosts.forEach(function (post) { elPostGrid.appendChild(buildPostCard(post)); });
  }

  /* -------------------------------------------------------------------------
     Featured Jobs
  ------------------------------------------------------------------------- */
  async function fetchFeatured() {
    try {
      const response = await fetch(FEATURED_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      featuredWeek = await response.json();
    } catch (err) {
      console.error('[IW Content Hub] Failed to load featured.json:', err);
      featuredWeek = null;
    }
    computeFeaturedNew();
    updateFeaturedBadge();
  }

  /* -------------------------------------------------------------------------
     Shorts / Reels
  ------------------------------------------------------------------------- */
  async function fetchShorts() {
    try {
      const response = await fetch(SHORTS_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      shortsWeek = await response.json();
    } catch (err) {
      console.error('[IW Content Hub] Failed to load shorts.json:', err);
      shortsWeek = null;
    }
  }

  /* -------------------------------------------------------------------------
     Analytics (Ayrshare) - data/analytics.json, built by build_analytics.py
  ------------------------------------------------------------------------- */
  async function fetchAnalytics() {
    try {
      const response = await fetch(ANALYTICS_URL, { cache: 'no-store' });
      if (!response.ok) throw new Error('HTTP ' + response.status);
      analyticsData = await response.json();
    } catch (err) {
      console.error('[IW Content Hub] Failed to load analytics.json:', err);
      analyticsData = null;
    }
    if (currentMode === 'analytics') renderAnalytics();
  }

  // Brand marks for each network (inline SVG, drawn white on a brand-colour chip).
  var PLAT_META = {
    instagram: { name: 'Instagram', colour: '#E1306C',
      icon: '<path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.42.56.21.96.47 1.38.89.42.42.68.82.9 1.38.16.42.36 1.05.41 2.22.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.22-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.7 3.7 0 01-1.38-.9 3.7 3.7 0 01-.9-1.38c-.16-.42-.36-1.05-.41-2.22C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.22.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.89.43-.17 1.06-.37 2.23-.42C8.42 2.17 8.8 2.16 12 2.16zm0 5.68A4.16 4.16 0 1016.16 12 4.16 4.16 0 0012 7.84zm0 6.86A2.7 2.7 0 1114.7 12 2.7 2.7 0 0112 14.7zm5.31-7.02a.97.97 0 11-.97-.97.97.97 0 01.97.97z"/>' },
    facebook:  { name: 'Facebook', colour: '#1877F2',
      icon: '<path d="M24 12.07C24 5.4 18.63 0 12 0S0 5.4 0 12.07C0 18.1 4.39 23.1 10.13 24v-8.44H7.08v-3.49h3.05V9.41c0-3.02 1.79-4.69 4.53-4.69 1.31 0 2.68.24 2.68.24v2.97h-1.5c-1.49 0-1.96.93-1.96 1.89v2.25h3.33l-.53 3.49h-2.8V24C19.61 23.1 24 18.1 24 12.07z"/>' },
    linkedin:  { name: 'LinkedIn', colour: '#0A66C2',
      icon: '<path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 112.06-2.07 2.07 2.07 0 01-2.06 2.07zm1.78 13.02H3.55V9h3.57v11.45zM22.22 0H1.77C.8 0 0 .78 0 1.75v20.5C0 23.2.8 24 1.77 24h20.45c.98 0 1.78-.8 1.78-1.75V1.75C24 .78 23.2 0 22.22 0z"/>' },
    threads:   { name: 'Threads', colour: '#111111',
      icon: '<path d="M17.3 11.13c-.09-.04-.18-.08-.27-.12-.16-2.94-1.77-4.62-4.47-4.64h-.04c-1.61 0-2.95.69-3.78 1.94l1.48 1.02c.62-.94 1.6-1.14 2.3-1.14h.02c.87 0 1.53.25 1.96.75.31.36.52.87.63 1.51-.82-.14-1.7-.18-2.65-.13-2.66.15-4.37 1.7-4.26 3.85.06 1.09.6 2.03 1.53 2.64.78.52 1.79.77 2.84.71 1.38-.07 2.47-.6 3.23-1.57.58-.74.94-1.7 1.11-2.9.68.41 1.18.95 1.46 1.6.47 1.1.5 2.9-.97 4.37-1.29 1.29-2.84 1.85-5.17 1.86-2.59-.02-4.55-.85-5.82-2.47C4.71 16.4 4.1 14.36 4.09 11.99c.01-2.37.62-4.41 1.81-6.05C7.17 4.33 9.13 3.5 11.72 3.48c2.61.02 4.58.85 5.86 2.48.63.8 1.11 1.81 1.42 3l1.86-.5c-.38-1.45-.98-2.7-1.8-3.74C17.3 2.6 14.79 1.5 11.73 1.48h-.02c-3.05.02-5.5 1.13-7.24 3.29C2.87 6.66 2.14 9.11 2.13 11.98v.01c.01 2.87.74 5.32 2.34 7.22 1.74 2.16 4.19 3.27 7.24 3.29h.02c2.72-.02 4.64-.73 6.22-2.31 2.07-2.06 2-4.65 1.32-6.24-.49-1.14-1.42-2.07-2.7-2.67z"/>' },
  };

  function renderAnalytics() {
    if (!elAnalyticsView) return;
    if (!analyticsData) {
      elAnalyticsView.innerHTML =
        '<div class="analytics-empty"><h2>Analytics</h2>' +
        '<p>No analytics yet. They are generated from Ayrshare once posts have gone out ' +
        '(the scheduled build writes <code>data/analytics.json</code>).</p></div>';
      return;
    }

    var d = analyticsData;
    var fmt = function (n) {
      return (n === null || n === undefined) ? '—' : Number(n).toLocaleString();
    };
    var when = d.generatedAt ? new Date(d.generatedAt).toLocaleString('en-GB',
      { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }) : '';

    var platforms = d.platforms || {};
    var series = d.series || {};
    var keys = Object.keys(PLAT_META).filter(function (k) { return platforms[k]; });

    // ---- Date-range filter --------------------------------------------------
    var ymd = function (dt) { return dt.toISOString().slice(0, 10); };
    var todayStr = ymd(new Date());
    var defStart = (function () { var s = new Date(); s.setUTCDate(s.getUTCDate() - 29); return ymd(s); })();
    var RANGES = [['current', 'Current'], ['7d', '7 days'], ['30d', '30 days'], ['90d', '90 days'], ['custom', 'Custom']];

    // Resolved [startStr, endStr] for the active mode, or null for "Current" (snapshot).
    function bounds() {
      var mode = analyticsRange.mode;
      if (mode === 'current') return null;
      if (mode === 'custom') return [analyticsRange.start || defStart, analyticsRange.end || todayStr];
      var days = mode === '7d' ? 7 : mode === '90d' ? 90 : 30;
      var start = new Date(); start.setUTCDate(start.getUTCDate() - (days - 1));
      return [ymd(start), todayStr];
    }
    var win = bounds();

    // Sum a daily series over the window; null if the network has no such series.
    function windowed(net, metric) {
      var s = series[net]; if (!s || !s[metric]) return null;
      var t = 0;
      s[metric].forEach(function (pt) { if (pt.d >= win[0] && pt.d <= win[1]) t += pt.v; });
      return t;
    }
    // Per-account {reach, views, engagement}: snapshot totals in "Current",
    // else summed from the daily series over the window.
    function metricsFor(k) {
      var p = platforms[k];
      if (!win) {
        var s = 0, any = false;
        ['likes', 'comments', 'shares'].forEach(function (m) {
          if (typeof p[m] === 'number') { s += p[m]; any = true; }
        });
        return {
          reach: (typeof p.reach === 'number' ? p.reach : null),
          views: (typeof p.views === 'number' ? p.views : null),
          engagement: any ? s : null,
        };
      }
      return { reach: windowed(k, 'reach'), views: windowed(k, 'views'), engagement: windowed(k, 'engagement') };
    }
    var perPlat = {};
    keys.forEach(function (k) { perPlat[k] = metricsFor(k); });

    // Sum one metric across accounts; returns {val, reporting}.
    function agg(pick) {
      var t = null, n = 0;
      keys.forEach(function (k) {
        var v = pick(k); if (typeof v === 'number') { t = (t || 0) + v; n++; }
      });
      return { val: t, reporting: n };
    }
    var aFollowers = agg(function (k) { return platforms[k].followers; });
    var aReach     = agg(function (k) { return perPlat[k].reach; });
    var aViews     = agg(function (k) { return perPlat[k].views; });
    var aEng       = agg(function (k) { return perPlat[k].engagement; });

    // ---- Overview tiles -----------------------------------------------------
    function tile(a, label) {
      return '<div class="an-tile"><span class="an-tile__val">' + fmt(a.val) + '</span>' +
             '<span class="an-tile__label">' + label + '</span>' +
             '<span class="an-tile__note">' + a.reporting + ' of ' + keys.length + ' accounts</span></div>';
    }
    var overview =
      tile(aFollowers, win ? 'Followers (now)' : 'Followers') +
      tile(aReach, 'Reach') + tile(aViews, 'Views') + tile(aEng, 'Engagement');

    // ---- Per-account cards --------------------------------------------------
    var platCards = keys.map(function (k) {
      var p = platforms[k], m = PLAT_META[k], mx = perPlat[k];
      function metric(label, val) {
        return '<div class="an-metric"><span class="an-metric__val">' + fmt(val) +
               '</span><span class="an-metric__label">' + label + '</span></div>';
      }
      var chip = '<span class="an-chip" style="background:' + m.colour + '">' +
        '<svg viewBox="0 0 24 24" width="18" height="18" fill="#fff" aria-hidden="true">' + m.icon + '</svg></span>';
      var handle = p.name ? '<span class="an-platform__handle">' + escapeHtml(p.name) + '</span>' : '';
      return '<div class="an-card an-platform an-platform--' + k + '">' +
        '<div class="an-platform__head">' + chip +
          '<span class="an-platform__id"><span class="an-platform__name">' + m.name + '</span>' + handle + '</span>' +
          '<span class="an-platform__followers">' + fmt(p.followers) + '<small>followers</small></span>' +
        '</div>' +
        '<div class="an-metrics an-metrics--3">' +
          metric('Reach', mx.reach) + metric('Views', mx.views) + metric('Engagement', mx.engagement) +
        '</div></div>';
    }).join('');

    // ---- Range selector -----------------------------------------------------
    var seg = '<div class="an-range" role="tablist">' + RANGES.map(function (r) {
      return '<button class="an-range__btn' + (analyticsRange.mode === r[0] ? ' is-active' : '') +
        '" data-range="' + r[0] + '" role="tab" aria-selected="' + (analyticsRange.mode === r[0]) + '">' + r[1] + '</button>';
    }).join('') + '</div>';
    var custom = analyticsRange.mode === 'custom'
      ? '<div class="an-custom">' +
          '<input type="date" class="an-date" id="an-date-start" value="' + (analyticsRange.start || defStart) + '" max="' + todayStr + '">' +
          '<span class="an-custom__sep">to</span>' +
          '<input type="date" class="an-date" id="an-date-end" value="' + (analyticsRange.end || todayStr) + '" max="' + todayStr + '">' +
          '<button class="an-apply" id="an-apply">Apply</button>' +
        '</div>'
      : '';
    var rangeLabel = win ? win[0] + ' → ' + win[1] : 'current totals';
    var foot = win
      ? '<p class="an-foot">Period figures use each network\'s daily data: Reach from Instagram, Views from Facebook &amp; Threads, Engagement from Facebook. A blank means that network doesn\'t report the metric for a date range. Followers is always the current total.</p>'
      : '<p class="an-foot">Current totals as each network reports them. Pick a date range to see reach, views and engagement for that period.</p>';

    elAnalyticsView.innerHTML =
      '<div class="an-head">' +
        '<h2>Analytics</h2>' +
        '<span class="an-sub">Ayrshare · ' + escapeHtml(rangeLabel) +
        (when ? ' · updated ' + when : '') + '</span>' +
      '</div>' +

      '<div class="an-toolbar">' + seg + custom + '</div>' +

      '<div class="an-overview">' + overview + '</div>' +

      '<section class="an-section"><h3 class="an-h3">By account</h3>' +
        '<div class="an-platforms">' + (platCards || '<p class="an-note">No platform data yet.</p>') + '</div>' +
        foot +
      '</section>';

    // ---- Wire the selector (re-renders in place, no refetch) -----------------
    Array.prototype.forEach.call(elAnalyticsView.querySelectorAll('.an-range__btn'), function (b) {
      b.addEventListener('click', function () {
        analyticsRange.mode = b.getAttribute('data-range');
        if (analyticsRange.mode === 'custom' && !analyticsRange.start) {
          analyticsRange.start = defStart; analyticsRange.end = todayStr;
        }
        renderAnalytics();
      });
    });
    var applyBtn = elAnalyticsView.querySelector('#an-apply');
    if (applyBtn) {
      applyBtn.addEventListener('click', function () {
        var s = elAnalyticsView.querySelector('#an-date-start').value;
        var e = elAnalyticsView.querySelector('#an-date-end').value;
        if (s && e) {
          if (s > e) { var t = s; s = e; e = t; }
          analyticsRange.start = s; analyticsRange.end = e; renderAnalytics();
        }
      });
    }
  }

  function renderShorts() {
    if (!shortsWeek) {
      elWeekMeta.innerHTML = '<span class="week-meta__label">Shorts / Reels</span>';
      elPostGrid.innerHTML = '';
      elEmptyState.hidden = false;
      return;
    }
    currentWeek = {
      id: shortsWeek.id || 'shorts',
      label: shortsWeek.label || 'Shorts / Reels',
      posts: shortsWeek.posts || [],
    };

    const generated = shortsWeek.generatedAt ? new Date(shortsWeek.generatedAt) : null;
    const generatedLabel = generated && !isNaN(generated)
      ? 'Generated ' + generated.toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })
      : 'Automated topic research';

    elWeekMeta.innerHTML = `
      <span class="week-meta__label">${escapeHtml(currentWeek.label)}</span>
      <span class="week-meta__date">${escapeHtml(generatedLabel)}</span>
    `;

    renderPostGrid(currentWeek.posts);
  }

  /* -------------------------------------------------------------------------
     Featured "new graphics" notification
     - Tracks which auto-generated (sourceId) posts the user has already seen,
       in localStorage. New ones drive the tab badge + a NEW ribbon on cards.
  ------------------------------------------------------------------------- */
  function loadFeaturedSeen() {
    try {
      const stored = localStorage.getItem(FEATURED_SEEN_KEY);
      featuredSeen = new Set(stored ? JSON.parse(stored) : []);
    } catch (_) {
      featuredSeen = new Set();
    }
  }

  function saveFeaturedSeen() {
    try {
      localStorage.setItem(FEATURED_SEEN_KEY, JSON.stringify([...featuredSeen]));
    } catch (_) { /* localStorage unavailable - continue */ }
  }

  /** Ids of auto-generated featured posts (the scraped ones). */
  function autoFeaturedIds() {
    return (featuredWeek && featuredWeek.posts || [])
      .filter(function (p) { return p.sourceId; })
      .map(function (p) { return p.id; });
  }

  function computeFeaturedNew() {
    // Anything the user hasn't seen yet is "new" (including on a first visit, so the
    // badge is always visible when there are featured graphics to review).
    const autoIds = autoFeaturedIds();
    featuredNewIds = new Set(autoIds.filter(function (id) { return !featuredSeen.has(id); }));
  }

  function updateFeaturedBadge() {
    if (!elFeaturedBadge) return;
    const unseen = autoFeaturedIds().filter(function (id) { return !featuredSeen.has(id); }).length;
    if (unseen > 0) {
      elFeaturedBadge.textContent = String(unseen);
      elFeaturedBadge.hidden = false;
      elFeaturedBadge.setAttribute('aria-label', unseen + ' new graphics');
    } else {
      elFeaturedBadge.hidden = true;
      elFeaturedBadge.textContent = '';
    }
  }

  /** Mark all current auto posts as seen (called when the user opens the tab). */
  function markFeaturedSeen() {
    autoFeaturedIds().forEach(function (id) { featuredSeen.add(id); });
    saveFeaturedSeen();
    updateFeaturedBadge();
  }

  function renderFeatured() {
    if (!featuredWeek) {
      elWeekMeta.innerHTML = '<span class="week-meta__label">Featured Jobs</span>';
      elPostGrid.innerHTML = '';
      elEmptyState.hidden = false;
      return;
    }
    currentWeek = featuredWeek;

    const posts = (featuredWeek.posts || []).slice().sort(function (a, b) {
      // Newest first: by numeric job id (higher id = more recently posted),
      // then by addedAt as a tiebreak.
      const ai = parseInt(a.sourceId || 0, 10), bi = parseInt(b.sourceId || 0, 10);
      if (ai !== bi) return bi - ai;
      return (b.addedAt || '') < (a.addedAt || '') ? -1 : 1;
    });

    const count = posts.length;
    elWeekMeta.innerHTML = `
      <span class="week-meta__label">${escapeHtml(featuredWeek.label)}</span>
      <span class="week-meta__date">${count} open ${count === 1 ? 'role' : 'roles'}</span>
    `;

    renderPostGrid(posts);
  }

  /** Switch between 'weekly', 'shorts', and 'featured' content modes. */
  function setMode(mode) {
    if (['weekly', 'shorts', 'featured', 'analytics'].indexOf(mode) === -1) return;
    currentMode = mode;

    const isWeekly    = (mode === 'weekly');
    const isShorts    = (mode === 'shorts');
    const isFeatured  = (mode === 'featured');
    const isAnalytics = (mode === 'analytics');
    elModeWeekly.classList.toggle('is-active', isWeekly);
    elModeShorts.classList.toggle('is-active', isShorts);
    elModeFeatured.classList.toggle('is-active', isFeatured);
    if (elModeAnalytics) elModeAnalytics.classList.toggle('is-active', isAnalytics);
    elModeWeekly.setAttribute('aria-selected', String(isWeekly));
    elModeShorts.setAttribute('aria-selected', String(isShorts));
    elModeFeatured.setAttribute('aria-selected', String(isFeatured));
    if (elModeAnalytics) elModeAnalytics.setAttribute('aria-selected', String(isAnalytics));

    // Week selector is only meaningful in weekly mode
    elWeekSelector.classList.toggle('is-hidden', !isWeekly);

    // Analytics has its own full-width view; the post grid / week meta belong to
    // the content modes. Toggle which surface is visible.
    if (elAnalyticsView) elAnalyticsView.hidden = !isAnalytics;
    elPostGrid.hidden = isAnalytics;
    elWeekMeta.hidden = isAnalytics;
    if (isAnalytics && elEmptyState) elEmptyState.hidden = true;

    if (isWeekly) {
      const weekId = elWeekSelector.value || (allWeeks[0] && allWeeks[0].id);
      if (weekId) renderWeek(weekId);
    } else if (isShorts) {
      renderShorts();
    } else if (isFeatured) {
      renderFeatured();
      // Opening the tab counts as reviewing: clear the badge (NEW ribbons remain
      // for this session so the user can still spot which ones are new).
      markFeaturedSeen();
    } else {
      renderAnalytics();
    }
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
    const slides     = post.slides || [];
    const isShort    = post.format === 'Short/Reel';
    const thumbSrc   = post.thumbnailPath || (slides[0] ? buildImagePath(currentWeek.id, post.id, slides[0]) : '');
    const slideCount = slides.length;
    const scoreLabel = typeof post.viralScore === 'number' ? Math.round(post.viralScore) + ' score' : 'Script ready';

    // Outer wrapper — role="listitem" matches the grid's role="list"
    const article = document.createElement('article');
    article.className = 'post-card';
    article.setAttribute('role', 'listitem');
    article.setAttribute('tabindex', '0');
    article.setAttribute('aria-label', `${post.title}, ${STATUS_LABELS[status]}`);
    article.dataset.postId = post.id;

    article.innerHTML = `
      <div class="post-card__thumb">
        ${thumbSrc ? `
          <img
            class="post-card__thumb-img"
            src="${thumbSrc}"
            alt="${escapeHtml(post.title)} — slide 1"
            loading="lazy"
            width="400"
            height="400"
          >
        ` : `
          <div class="post-card__short-thumb" aria-hidden="true">
            <span class="post-card__short-label">Short</span>
            <strong>${escapeHtml(scoreLabel)}</strong>
            <small>${escapeHtml(post.heygenStatus || 'Ready for HeyGen')}</small>
          </div>
        `}
        ${slideCount > 1 ? `<span class="post-card__slide-pill" aria-label="${slideCount} slides">${slideCount} slides</span>` : ''}
        ${isShort && post.durationTargetSeconds ? `<span class="post-card__slide-pill" aria-label="${post.durationTargetSeconds} seconds">${post.durationTargetSeconds}s</span>` : ''}
        ${featuredNewIds.has(post.id) ? '<span class="post-card__new-ribbon">New</span>' : ''}
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
    saveStatuses();          // local cache (offline / instant)
    pushRemoteStatus(postId, newStatus);
  }

  /* Shared status store (Cloudflare KV via /api/statuses). Falls back silently to
     localStorage-only if the endpoint isn't configured yet. */
  async function fetchRemoteStatuses() {
    if (IS_LOCAL) return;
    try {
      const res = await fetch(STATUS_API, { cache: 'no-store' });
      if (!res.ok) return;                         // 501 = KV not bound yet
      const remote = await res.json();
      if (remote && typeof remote === 'object') {
        // Shared store is the source of truth across devices.
        statuses = Object.assign({}, statuses, remote);
        saveStatuses();
        refreshVisibleStatuses();
      }
    } catch (_) { /* offline / no function - keep localStorage */ }
  }

  function pushRemoteStatus(postId, status) {
    if (IS_LOCAL) return;
    try {
      fetch(STATUS_API, {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ id: postId, status: status }),
      }).catch(function () {});
    } catch (_) { /* ignore */ }
  }

  /** Re-sync the status badges/dropdown currently on screen after a remote fetch. */
  function refreshVisibleStatuses() {
    if (!currentWeek) return;
    (currentWeek.posts || []).forEach(function (post) {
      const status = getStatus(post.id, post.status);
      const badge  = elPostGrid.querySelector('.status-badge[data-post-id="' + post.id + '"]');
      if (badge) {
        STATUS_CYCLE.forEach(function (s) { badge.classList.remove('status-badge--' + s); });
        badge.classList.add('status-badge--' + status);
        badge.textContent = STATUS_LABELS[status];
      }
    });
    if (overlayPostId) {
      const p = currentWeek.posts.find(function (x) { return x.id === overlayPostId; });
      if (p) elDetailStatus.value = getStatus(overlayPostId, p.status);
    }
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
    const hasSlides = Array.isArray(post.slides) && post.slides.length > 0;
    elDownloadSlideBtn.hidden = !hasSlides;
    elDownloadAllBtn.hidden = !hasSlides;

    // Load comments for this post
    renderComments(postId);
    elCommentTextarea.value = '';

    // Show overlay
    elOverlay.hidden = false;
    // Force reflow before adding class to trigger CSS transition
    void elOverlay.offsetWidth;
    elOverlay.classList.add('is-open');

    // Always start sidebar at top so title/status are visible first
    elContentSidebar.scrollTop = 0;

    // Trap focus — move to close button
    elOverlayClose.focus();

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
  }

  function closeOverlay() {
    elOverlay.classList.remove('is-open');

    // Capture the id before clearing it so focus-return works
    const returningPostId = overlayPostId;

    // Guarantee the card badge reflects the saved status when the overlay closes.
    // The change handler updates it in real-time, but this acts as a hard sync
    // so any edge case (mobile native picker, fast close, etc.) can't leave the
    // badge out of sync.
    if (returningPostId && currentWeek) {
      const post        = currentWeek.posts.find(function (p) { return p.id === returningPostId; });
      const savedStatus = getStatus(returningPostId, post ? post.status : 'in-review');
      const badge       = elPostGrid.querySelector('.status-badge[data-post-id="' + returningPostId + '"]');
      if (badge) {
        STATUS_CYCLE.forEach(function (s) { badge.classList.remove('status-badge--' + s); });
        badge.classList.add('status-badge--' + savedStatus);
        badge.textContent = STATUS_LABELS[savedStatus];
        badge.setAttribute('aria-label', 'Status: ' + STATUS_LABELS[savedStatus] + '. Click to cycle status.');
        const card = badge.closest('.post-card');
        if (card && post) card.setAttribute('aria-label', post.title + ', ' + STATUS_LABELS[savedStatus]);
      }
    }

    // Wait for fade-out before hiding. iOS Safari can drop transitionend,
    // so a timeout fallback guarantees hidden is always set.
    var hideTimer = setTimeout(function () { elOverlay.hidden = true; }, 250);
    elOverlay.addEventListener('transitionend', function handler() {
      clearTimeout(hideTimer);
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
    const slides = post.slides || [];
    const total  = slides.length;

    if (post.format === 'Short/Reel' && total === 0) {
      renderShortPreview(post);
      return;
    }

    removeShortPreview();
    elSlideImg.hidden = false;
    const slide    = slides[idx];
    const src      = buildImagePath(currentWeek.id, post.id, slide);

    elSlideImg.src = src;
    elSlideImg.alt = `${post.title} — slide ${idx + 1} of ${total}`;

    elSlideCounter.textContent = `${idx + 1} / ${total}`;

    elSlidePrev.disabled = (idx === 0);
    elSlideNext.disabled = (idx === total - 1);
  }

  function renderShortPreview(post) {
    const stage = elSlideImg.parentElement;
    if (!stage) return;
    elSlideImg.hidden = true;
    elSlideImg.removeAttribute('src');
    removeShortPreview();

    const preview = document.createElement('div');
    preview.className = 'short-preview';
    const score = typeof post.viralScore === 'number' ? Math.round(post.viralScore) + '/100' : 'Ready';
    const signals = (post.sourceSignals || []).slice(0, 3).map(function (signal) {
      return '<li>' + escapeHtml(signal.title || signal.source || 'Signal') + '</li>';
    }).join('');
    preview.innerHTML = `
      <div class="short-preview__frame">
        <span class="short-preview__eyebrow">Script-ready short</span>
        <h3>${escapeHtml(post.title)}</h3>
        <div class="short-preview__score">${escapeHtml(score)}</div>
        <p>${escapeHtml(post.spokenScript || 'Open the caption panel for the generated script and source signals.')}</p>
        ${signals ? '<ul class="short-preview__signals">' + signals + '</ul>' : ''}
      </div>
    `;
    stage.appendChild(preview);

    elSlideCounter.textContent = post.durationTargetSeconds ? post.durationTargetSeconds + 's' : 'Short';
    elSlidePrev.disabled = true;
    elSlideNext.disabled = true;
  }

  function removeShortPreview() {
    const stage = elSlideImg.parentElement;
    if (!stage) return;
    const existing = stage.querySelector('.short-preview');
    if (existing) existing.remove();
  }

  function navigateSlide(direction) {
    if (!overlayPostId || !currentWeek) return;
    const post  = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;
    const total = (post.slides || []).length;
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

  /** Detect iOS (iPhone / iPad including iPadOS which reports MacIntel on newer devices) */
  function isIOS() {
    return (
      /iPhone|iPod/.test(navigator.userAgent) ||
      /iPad/.test(navigator.userAgent) ||
      (navigator.maxTouchPoints > 1 && /Mac/.test(navigator.platform || ''))
    );
  }

  function isAndroid() {
    return /Android/i.test(navigator.userAgent || '');
  }

  function canUseMobileFileShare(files) {
    if (!(isIOS() || isAndroid())) return false;
    return !!(navigator.canShare && navigator.canShare({ files: files }) && navigator.share);
  }

  /**
   * Download the currently-displayed slide.
   * Uses Web Share API on mobile (opens native share sheet → Save to Gallery).
   * Falls back to blob download on desktop.
   */
  function downloadCurrentSlide() {
    if (!overlayPostId || !currentWeek) return;
    const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;
    if (!post.slides || post.slides.length === 0) return;

    const url      = buildImagePath(currentWeek.id, post.id, post.slides[currentSlideIdx]);
    const filename = post.id + '_slide_' + (currentSlideIdx + 1) + '.png';

    // cache:'reload' forces a fresh CORS request. The <img> that displays the
    // slide loads it no-CORS, caching a response with no Access-Control-Allow-
    // Origin header; a default fetch would reuse that and the browser would
    // block reading the blob. Reloading gets R2's CORS-enabled response.
    fetch(url, { cache: 'reload' })
      .then(function (r) { return r.blob(); })
      .then(function (blob) {
        const file = new File([blob], filename, { type: 'image/png' });

        // Web Share API — opens native share sheet on iOS/Android
        if (canUseMobileFileShare([file])) {
          return navigator.share({ files: [file] });
        }

        // iOS without Share API — open in new tab, long-press to save
        if (isIOS()) {
          window.open(URL.createObjectURL(blob), '_blank');
          return;
        }

        // Desktop — direct blob download
        const a = document.createElement('a');
        a.href = URL.createObjectURL(blob);
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      })
      .catch(function (err) {
        if (err && err.name !== 'AbortError') {
          console.error('[IW Content Hub] Download failed:', err);
        }
      });
  }

  /**
   * Download all slides for the open post.
   *
   * Priority:
   *  1. Web Share API (iOS 15+ / Android Chrome 86+) → native share sheet → Save to Gallery
   *  2. iOS without Share API → open each slide in a new tab (long-press to save)
   *  3. Desktop / Android → ZIP bundle via JSZip
   */
  async function downloadAllSlides() {
    if (!overlayPostId || !currentWeek) return;
    const post = currentWeek.posts.find(function (p) { return p.id === overlayPostId; });
    if (!post) return;
    if (!post.slides || post.slides.length === 0) return;

    // Single slide — reuse single-slide path
    if (post.slides.length === 1) {
      downloadCurrentSlide();
      return;
    }

    elDownloadAllBtn.disabled = true;
    elDownloadAllBtn.classList.add('is-downloading');

    try {
      const total = post.slides.length;
      const blobs = [];

      // Fetch all images as blobs
      for (let i = 0; i < total; i++) {
        elDownloadAllLabel.textContent = 'Loading ' + (i + 1) + ' / ' + total + '...';
        const url = buildImagePath(currentWeek.id, post.id, post.slides[i]);
        const res = await fetch(url, { cache: 'reload' });  // fresh CORS request (see downloadCurrentSlide)
        blobs.push(await res.blob());
      }

      const shareFiles = blobs.map(function (blob, i) {
        return new File([blob], post.id + '_slide_' + (i + 1) + '.png', { type: 'image/png' });
      });

      // ── Path 1: Web Share API ──────────────────────────────────────────────
      // Opens native iOS/Android share sheet — tap "Save Image" to add to gallery
      if (canUseMobileFileShare(shareFiles)) {
        elDownloadAllLabel.textContent = 'Opening share sheet...';
        await navigator.share({ title: post.title, files: shareFiles });
        elDownloadAllLabel.textContent = 'Download All Slides';
        return;
      }

      // ── Path 2: iOS without Share API ─────────────────────────────────────
      // Open each slide in a new tab; user long-presses → Save to Photos
      if (isIOS()) {
        for (let i = 0; i < total; i++) {
          elDownloadAllLabel.textContent = 'Opening ' + (i + 1) + ' / ' + total + '...';
          window.open(URL.createObjectURL(blobs[i]), '_blank');
          await new Promise(function (r) { setTimeout(r, 800); });
        }
        elDownloadAllLabel.textContent = 'Long-press each tab to save';
        setTimeout(function () { elDownloadAllLabel.textContent = 'Download All Slides'; }, 4000);
        return;
      }

      // ── Path 3: Desktop / Android — ZIP ───────────────────────────────────
      elDownloadAllLabel.textContent = 'Creating ZIP...';
      const zip    = new JSZip();
      const folder = zip.folder(post.id);
      blobs.forEach(function (blob, i) {
        folder.file('slide_' + (i + 1) + '.png', blob);
      });
      const content = await zip.generateAsync({ type: 'blob' });
      const a = document.createElement('a');
      a.href = URL.createObjectURL(content);
      a.download = post.id + '_slides.zip';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setTimeout(function () { URL.revokeObjectURL(a.href); }, 1000);
      elDownloadAllLabel.textContent = 'Downloaded!';
      setTimeout(function () { elDownloadAllLabel.textContent = 'Download All Slides'; }, 2000);

    } catch (err) {
      if (err && err.name !== 'AbortError') {
        console.error('[IW Content Hub] Download failed:', err);
      }
      elDownloadAllLabel.textContent = 'Download All Slides';
    } finally {
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

    // Mode toggle: Weekly Graphics / Featured Jobs
    elModeWeekly.addEventListener('click', function () { setMode('weekly'); });
    elModeShorts.addEventListener('click', function () { setMode('shorts'); });
    elModeFeatured.addEventListener('click', function () { setMode('featured'); });
    if (elModeAnalytics) elModeAnalytics.addEventListener('click', function () { setMode('analytics'); });

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
      if (!post) return;
      // Copy the caption currently shown (platform-specific for featured jobs).
      copyToClipboard(currentCaption || post.caption, elCopyCaptionBtn);
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
    const base = IMAGE_BASE ? IMAGE_BASE.replace(/\/$/, '') : 'images';
    const url = `${base}/${weekId}/${postId}/${filename}`;
    // R2 serves images with an immutable, one-year cache. When a slide is
    // re-rendered under the same filename, browsers would otherwise keep the
    // stale copy. Each week carries a `builtAt` version stamped at build time;
    // appending it as ?v= makes a re-render a fresh URL so viewers see updates.
    const wk = allWeeks.find(function (w) { return w.id === weekId; });
    const v = wk && wk.builtAt;
    return v ? `${url}?v=${encodeURIComponent(v)}` : url;
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
    const slides           = post.slides || [];
    const isCarousel       = slides.length > 1;
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
      // Prefer a platform-specific caption (featured jobs), else the single caption.
      currentCaption = (post.captions && post.captions[platform]) || post.caption || post.spokenScript || '';
      elDetailCaption.textContent = currentCaption;
    }
  }

  function renderHashtagsForPlatform(post, platform) {
    const limit     = PLATFORM_HASHTAG_LIMIT[platform] || 5;
    // Prefer a platform-specific hashtag set (featured jobs), else the shared list.
    const source    = (post.hashtagsByPlatform && post.hashtagsByPlatform[platform]) || post.hashtags || [];
    // Brand rule: hashtags are always lowercase (#techjobs, never #TechJobs).
    currentHashtags = source.slice(0, limit).map(function (t) {
      return typeof t === 'string' && t.charAt(0) === '#' ? '#' + t.slice(1).toLowerCase() : t;
    });

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
