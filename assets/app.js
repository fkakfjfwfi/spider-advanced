/* 爬虫进阶 · 共享脚本：侧边章节高亮 + 打卡进度持久化（localStorage） */
(function () {
  var KEY = 'spiderAdvancedProgress';
  var TOTALS = { c01: 6, c02: 6, c03: 6, c04: 6, c05: 6, c06: 6, c07: 6, c08: 6, c09: 6, c10: 6 }; // 每章 6 个打卡点，共 60

  function load() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function save(o) {
    try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) {}
  }
  var state = load();

  var boxes = document.querySelectorAll('input[type="checkbox"][data-persist]');
  boxes.forEach(function (cb) {
    if (!cb.id) return;
    if (state[cb.id]) cb.checked = true;
    cb.addEventListener('change', function () {
      state[cb.id] = cb.checked;
      save(state);
      paint();
    });
  });

  function counts() {
    var done = {}, total = {}, d = 0, t = 0, k;
    for (k in TOTALS) { total[k] = TOTALS[k]; done[k] = 0; }
    for (var key in state) {
      var m = /^(c\d+)-/.exec(key);
      if (m && state[key] && total[m[1]] !== undefined) done[m[1]]++;
    }
    for (k in TOTALS) { d += done[k]; t += TOTALS[k]; }
    return { done: done, total: total, allDone: d, allTotal: t };
  }

  function paint() {
    var c = counts();
    document.querySelectorAll('[data-progress-bar]').forEach(function (el) {
      var which = el.getAttribute('data-progress-bar');
      var d, t;
      if (which === 'all' || which === '') { d = c.allDone; t = c.allTotal; }
      else { d = c.done[which] || 0; t = c.total[which] || 0; }
      el.style.width = (t ? (d / t * 100) : 0) + '%';
    });
    document.querySelectorAll('[data-progress-label]').forEach(function (el) {
      var which = el.getAttribute('data-progress-label');
      if (which === 'all' || which === '') el.textContent = c.allDone + ' / ' + c.allTotal + ' 项已打卡';
      else el.textContent = (c.done[which] || 0) + ' / ' + (c.total[which] || 0) + ' · 本章打卡';
    });
    document.querySelectorAll('[data-chapter-progress]').forEach(function (el) {
      var which = el.getAttribute('data-chapter-progress');
      el.textContent = (c.done[which] || 0) + '/' + (c.total[which] || 0);
    });
  }

  // 侧边/导航高亮：<body data-page="c01">
  var page = document.body.getAttribute('data-page');
  if (page) {
    document.querySelectorAll('[data-nav]').forEach(function (a) {
      if (a.getAttribute('data-nav') === page) a.classList.add('active');
    });
  }

  paint();
})();
