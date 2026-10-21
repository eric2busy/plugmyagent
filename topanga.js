// PlugMyAgent Topanga preview: theme toggle, catalog filter, tabs, copy button.
(function () {
  'use strict';

  // Theme toggle: light default, dark via data-theme on <html>, persisted.
  var themeBtn = document.querySelector('[data-theme-toggle]');
  if (themeBtn) {
    themeBtn.addEventListener('click', function () {
      var cur = document.documentElement.getAttribute('data-theme') || 'light';
      var next = cur === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      try { localStorage.setItem('topanga-theme', next); } catch (e) {}
    });
  }

  // Catalog filter: render rows once, filter by hiding, update the count.
  var search = document.getElementById('catalogSearch');
  function setPill(value) { document.querySelectorAll('.filter-pills .pill').forEach(function (x) { var on = x.getAttribute('data-value') === value; x.classList.toggle('active', on); x.setAttribute('aria-selected', on ? 'true' : 'false'); }); }
  function activeCat() { var a = document.querySelector('.filter-pills .pill.active'); return a ? a.getAttribute('data-value') : ''; }
  var rows = document.querySelectorAll('[data-catalog-row]');
  var count = document.getElementById('catalogCount');
  var empty = document.getElementById('catalogEmpty');
  var clear = document.getElementById('catalogClear');
  if (search && rows.length) {
    var total = rows.length;
    function apply() {
      var q = search.value.trim().toLowerCase();
      var cat = activeCat();
      var shown = 0;
      rows.forEach(function (r) {
        var okQ = !q || r.getAttribute('data-search').indexOf(q) !== -1;
        var okC = !cat || r.getAttribute('data-category').split('|').indexOf(cat) !== -1;
        var show = okQ && okC;
        r.style.display = show ? '' : 'none';
        if (show) shown++;
      });
      if (count) count.textContent = 'Showing ' + shown + ' of ' + total + ' ' + (count.getAttribute('data-count-label') || 'APIs');
      if (empty) empty.hidden = shown !== 0;
    }
    search.addEventListener('input', apply);
    document.querySelectorAll('.filter-pills .pill').forEach(function (p) { p.addEventListener('click', function () { setPill(p.getAttribute('data-value')); apply(); }); });
    if (clear) clear.addEventListener('click', function () { search.value = ''; setPill(''); apply(); });
  }

  // Tabs: roving tabindex, arrow keys move, Home/End jump.
  var tabs = document.querySelectorAll('[role="tab"]');
  if (tabs.length) {
    function activate(tab, focus) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute('aria-selected', on ? 'true' : 'false');
        t.setAttribute('tabindex', on ? '0' : '-1');
        t.classList.toggle('active', on);
        document.getElementById(t.getAttribute('aria-controls')).hidden = !on;
      });
      if (focus) tab.focus();
    }
    tabs.forEach(function (t, i) {
      t.addEventListener('click', function () { activate(t, false); });
      t.addEventListener('keydown', function (e) {
        if (e.key === 'Home') { activate(tabs[0], true); e.preventDefault(); return; }
        if (e.key === 'End') { activate(tabs[tabs.length - 1], true); e.preventDefault(); return; }
        var dir = e.key === 'ArrowRight' ? 1 : e.key === 'ArrowLeft' ? -1 : 0;
        if (dir) { activate(tabs[(i + dir + tabs.length) % tabs.length], true); e.preventDefault(); }
      });
    });
  }

  // Copy button: copies the referenced code block, confirms briefly.
  document.querySelectorAll('[data-copy]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var target = document.querySelector(btn.getAttribute('data-copy'));
      var text = target ? target.textContent : '';
      function done() {
        var old = btn.textContent;
        btn.textContent = 'Copied';
        setTimeout(function () { btn.textContent = old; }, 1500);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(done);
      } else { done(); }
    });
  });
})();

  // Hamburger menu: toggle the mobile nav panel.
  var burger = document.getElementById('burger');
  var mnav = document.getElementById('mnav');
  if (burger && mnav) {
    burger.addEventListener('click', function () {
      var open = mnav.classList.toggle('open');
      document.body.classList.toggle('nav-open', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    mnav.addEventListener('click', function (e) {
      if (e.target.closest('a')) { mnav.classList.remove('open'); document.body.classList.remove('nav-open'); burger.setAttribute('aria-expanded', 'false'); }
    });
  }

  // Home aero header: transparent over the photo; solid bar once scrolled.
  if (document.body.classList.contains('home-aero')) {
    var onAeroScroll = function () {
      document.body.classList.toggle('hdr-solid', window.scrollY > 24);
    };
    window.addEventListener('scroll', onAeroScroll, { passive: true });
    onAeroScroll();
  }

  // Setup-page tabs: deep-link via hash (e.g. #muse, #instinct).
  var hashTabs = document.querySelector('[data-hash-tabs]');
  if (hashTabs) {
    var tabBtns = hashTabs.querySelectorAll('[role="tab"]');
    function activateBySlug(slug) {
      var found = null;
      tabBtns.forEach(function (t) { if (t.getAttribute('data-tab') === slug) found = t; });
      if (found) found.click();
    }
    tabBtns.forEach(function (t) {
      t.addEventListener('click', function () {
        try { history.replaceState(null, '', '#' + t.getAttribute('data-tab')); } catch (e) {}
      });
    });
    var start = (window.location.hash || '').replace('#', '');
    if (start) activateBySlug(start);
  }

  // Stack: localStorage cart, key plugmyagent_stack_v1 (array of slugs).
  var STACK_KEY = 'plugmyagent_stack_v1';
  function readStack() {
    try { var v = JSON.parse(localStorage.getItem(STACK_KEY) || '[]'); return Array.isArray(v) ? v : []; } catch (e) { return []; }
  }
  function writeStack(a) { try { localStorage.setItem(STACK_KEY, JSON.stringify(a)); } catch (e) {} }
  function refreshStackCounts() {
    var n = readStack().length;
    document.querySelectorAll('[data-stack-count]').forEach(function (el) {
      el.textContent = n ? String(n) : '';
      var btn = el.closest('.stack-icon-btn');
      if (btn) btn.classList.toggle('has-items', n > 0);
    });
  }
  document.querySelectorAll('[data-add-stack]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var slug = btn.getAttribute('data-add-stack');
      var stack = readStack();
      if (stack.indexOf(slug) === -1) { stack.push(slug); writeStack(stack); refreshStackCounts(); }
      var old = btn.textContent;
      btn.textContent = 'Added';
      setTimeout(function () { btn.textContent = old; }, 1500);
    });
  });
  refreshStackCounts();

  // Stack page rendering.
  var stackList = document.getElementById('stackList');
  var stackData = document.getElementById('stackData');
  if (stackList && stackData) {
    var catalogBySlug = {};
    try { JSON.parse(stackData.textContent).forEach(function (e) { catalogBySlug[e.slug] = e; }); } catch (e) {}
    var emptyEl = document.getElementById('stackEmpty');
    var summaryEl = document.getElementById('stackSummary');
    var clearBtn = document.getElementById('stackClear');
    function renderStack() {
      var stack = readStack();
      var items = stack.map(function (s) { return catalogBySlug[s]; }).filter(Boolean);
      stackList.innerHTML = '';
      if (!items.length) {
        if (emptyEl) emptyEl.hidden = false;
        if (summaryEl) summaryEl.hidden = true;
        refreshStackCounts();
        return;
      }
      if (emptyEl) emptyEl.hidden = true;
      if (summaryEl) summaryEl.hidden = false;
      items.forEach(function (api, i) {
        var card = document.createElement('section');
        card.className = 'card stack-item';
        card.innerHTML =
          '<div class="stack-item-top"><div><h3>' + api.name + '</h3><p>' + api.tagline + '</p></div>'
          + '<span class="badge">' + api.category + '</span></div>'
          + '<div class="stack-item-actions">'
          + '<a class="btn btn-secondary btn-sm" href="../api/' + api.slug + '/">Details</a>'
          + '<a class="btn btn-secondary btn-sm" href="' + api.docs_url + '">Docs</a>'
          + '<button class="icon-btn" type="button" data-stack-act="up" data-stack-idx="' + i + '"' + (i === 0 ? ' disabled' : '') + '>Up</button>'
          + '<button class="icon-btn" type="button" data-stack-act="down" data-stack-idx="' + i + '"' + (i === items.length - 1 ? ' disabled' : '') + '>Down</button>'
          + '<button class="icon-btn" type="button" data-stack-act="remove" data-stack-idx="' + i + '">Remove</button>'
          + '</div>';
        stackList.appendChild(card);
      });
      var summaryCount = document.getElementById('stackSummaryCount');
      if (summaryCount) summaryCount.textContent = items.length + (items.length === 1 ? ' API' : ' APIs');
      refreshStackCounts();
    }
    stackList.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-stack-act]');
      if (!btn) return;
      var stack = readStack();
      var idx = parseInt(btn.getAttribute('data-stack-idx'), 10);
      var act = btn.getAttribute('data-stack-act');
      if (act === 'remove') stack.splice(idx, 1);
      else if (act === 'up' && idx > 0) { var t = stack[idx - 1]; stack[idx - 1] = stack[idx]; stack[idx] = t; }
      else if (act === 'down' && idx < stack.length - 1) { var u = stack[idx + 1]; stack[idx + 1] = stack[idx]; stack[idx] = u; }
      writeStack(stack);
      renderStack();
    });
    if (clearBtn) clearBtn.addEventListener('click', function () { writeStack([]); renderStack(); });
    renderStack();
  }

  // Hero global search: lazy-load search-index.json, live grouped results.
  var heroInput = document.getElementById('heroSearch');
  var heroResults = document.getElementById('heroResults');
  if (heroInput && heroResults) {
    var heroIndex = null, heroLoading = null, heroActive = -1, heroItems = [];
    function heroFetch() {
      if (heroIndex) return Promise.resolve(heroIndex);
      if (!heroLoading) {
        heroLoading = fetch('search-index.json').then(function (r) { return r.json(); }).then(function (d) { heroIndex = d; return d; }).catch(function () { return []; });
      }
      return heroLoading;
    }
    function heroClose() { heroResults.hidden = true; heroInput.setAttribute('aria-expanded', 'false'); heroActive = -1; heroItems = []; document.body.classList.remove('search-open'); }
    function heroEsc(x) { return String(x == null ? '' : x).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
    function heroTile(name) {
      return '';
    }
    function heroRender(q, list) {
      if (!list.length) {
        heroResults.innerHTML = '<div class="hero-results-empty">No matches for "' + heroEsc(q) + '". <a href="catalog/?q=' + encodeURIComponent(q) + '">Search the catalog</a></div>';
      } else {
        var groups = {}, order = ['API', 'MCP', 'Component', 'Guide'];
        var labels = { API: 'APIs', MCP: 'MCP servers', Component: 'Components', Guide: 'Guides' };
        list.forEach(function (it) { (groups[it.t] = groups[it.t] || []).push(it); });
        var html = '';
        order.forEach(function (t) {
          if (!groups[t]) return;
          html += '<div class="hero-result-group"><div class="hero-result-head">' + labels[t] + '</div>';
          groups[t].forEach(function (it) {
            html += '<a class="hero-result" role="option" href="' + heroEsc(it.u) + '"><span class="r-title">' + heroTile(it.n) + heroEsc(it.n) + '</span><span class="r-snip">' + heroEsc(it.s) + '</span></a>';
          });
          html += '</div>';
        });
        heroResults.innerHTML = html;
      }
      heroResults.hidden = false;
      document.body.classList.add('search-open');
      heroInput.setAttribute('aria-expanded', 'true');
      heroItems = Array.prototype.slice.call(heroResults.querySelectorAll('.hero-result'));
    }
    function heroSearch(q) {
      var needle = q.trim().toLowerCase();
      if (needle.length < 2) { heroClose(); return; }
      heroFetch().then(function (idx) {
        var words = needle.split(/\s+/);
        var scored = [];
        idx.forEach(function (it) {
          var blob = (it.q || '').toLowerCase();
          var ok = words.every(function (w) { return blob.indexOf(w) !== -1; });
          if (!ok) return;
          var name = it.n.toLowerCase();
          var score = name.indexOf(needle) === 0 ? 3 : (name.indexOf(needle) !== -1 ? 2 : 1);
          scored.push({ it: it, score: score });
        });
        scored.sort(function (a, b) { return b.score - a.score; });
        heroRender(q.trim(), scored.slice(0, 8).map(function (x) { return x.it; }));
      });
    }
    document.querySelectorAll('[data-hero-try]').forEach(function (btn) {
      btn.addEventListener('click', function () {
        heroInput.value = btn.getAttribute('data-hero-try');
        heroInput.focus();
        heroInput.dispatchEvent(new Event('input', { bubbles: true }));
      });
    });
    var heroTimer = null;
    heroInput.addEventListener('input', function () {
      clearTimeout(heroTimer);
      var v = heroInput.value;
      heroTimer = setTimeout(function () { heroSearch(v); }, 100);
    });
    heroInput.addEventListener('focus', function () { if (heroInput.value.trim().length >= 2) heroSearch(heroInput.value); });
    heroInput.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') { heroClose(); heroInput.blur(); }
      else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (!heroItems.length) return;
        e.preventDefault();
        heroActive = e.key === 'ArrowDown' ? (heroActive + 1) % heroItems.length : (heroActive - 1 + heroItems.length) % heroItems.length;
        heroItems.forEach(function (el, i) { el.classList.toggle('active', i === heroActive); });
      } else if (e.key === 'Enter' && heroActive >= 0 && heroItems[heroActive]) {
        e.preventDefault();
        window.location.href = heroItems[heroActive].getAttribute('href');
      }
    });
    document.addEventListener('click', function (e) {
      if (!heroInput.contains(e.target) && !heroResults.contains(e.target)) heroClose();
    });
  }

  // Directory pages: pre-fill the filter from ?q= (hero-search deep links).
  var dirSearch = document.getElementById('catalogSearch');
  if (dirSearch) {
    try {
      var dq = new URLSearchParams(window.location.search).get('q');
      if (dq) { dirSearch.value = dq; dirSearch.dispatchEvent(new Event('input', { bubbles: true })); }
    } catch (e) {}
  }

  // Copy-text buttons (card install commands, prompt parts): copy the attribute.
  document.querySelectorAll('[data-copy-text]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var text = btn.getAttribute('data-copy-text') || '';
      function done() { var old = btn.textContent; btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = old; }, 1500); }
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done).catch(done); } else { done(); }
    });
  });

  // Tools: API Key Checker (shape only, nothing leaves the browser).
  var keyBtn = document.getElementById('keyCheckBtn');
  if (keyBtn) {
    keyBtn.addEventListener('click', function () {
      var provider = document.getElementById('keyProvider').value;
      var input = document.getElementById('keyInput');
      var out = document.getElementById('keyResult');
      var key = (input.value || '').trim();
      var checks = [];
      function check(ok, label) { checks.push({ ok: ok, label: label }); }
      check(key.length > 0, 'Something was pasted');
      check(!/\s/.test(key), 'No spaces inside the key');
      if (provider === 'openai') {
        check(key.indexOf('sk-') === 0, 'Starts with sk-');
        check(key.length >= 20, 'At least 20 characters long');
      } else if (provider === 'anthropic') {
        check(key.indexOf('sk-ant-') === 0, 'Starts with sk-ant-');
        check(key.length >= 20, 'At least 20 characters long');
      } else if (provider === 'google') {
        check(key.indexOf('AIza') === 0, 'Starts with AIza');
        check(key.length === 39, '39 characters long');
      } else {
        check(key.length >= 8, 'At least 8 characters long');
      }
      var bad = checks.filter(function (c) { return !c.ok; });
      out.hidden = false;
      out.className = 'tool-result' + (bad.length ? ' bad' : ' ok');
      var items = checks.map(function (c) { return '<li>' + (c.ok ? 'Pass: ' : 'Fail: ') + c.label + '</li>'; }).join('');
      out.innerHTML = (bad.length
        ? '<strong>Shape does not look right.</strong> This checks the format only, not whether the key works.'
        : '<strong>Shape looks right.</strong> This checks the format only, not whether the key works.')
        + '<ul>' + items + '</ul>';
    });
  }

  // Tools: MCP Config Validator (shape only, nothing leaves the browser).
  var cfgBtn = document.getElementById('configCheckBtn');
  if (cfgBtn) {
    cfgBtn.addEventListener('click', function () {
      var raw = document.getElementById('configInput').value || '';
      var out = document.getElementById('configResult');
      var problems = [];
      var parsed = null;
      try { parsed = JSON.parse(raw); } catch (e) { problems.push('Not valid JSON: ' + e.message); }
      var names = [];
      if (parsed && !problems.length) {
        if (!parsed.mcpServers || typeof parsed.mcpServers !== 'object' || Array.isArray(parsed.mcpServers)) {
          problems.push('Top level needs an "mcpServers" object.');
        } else {
          names = Object.keys(parsed.mcpServers);
          if (!names.length) problems.push('"mcpServers" is empty: add at least one server.');
          names.forEach(function (name) {
            var srv = parsed.mcpServers[name];
            if (!srv || typeof srv !== 'object' || Array.isArray(srv)) { problems.push('Server "' + name + '" is not an object.'); return; }
            if (typeof srv.command !== 'string' && typeof srv.url !== 'string') {
              problems.push('Server "' + name + '" needs a "command" or a "url".');
            }
            if (srv.args !== undefined && !Array.isArray(srv.args)) {
              problems.push('Server "' + name + '": "args" must be a list.');
            }
          });
        }
      }
      out.hidden = false;
      out.className = 'tool-result' + (problems.length ? ' bad' : ' ok');
      out.innerHTML = problems.length
        ? '<strong>Config has problems.</strong><ul>' + problems.map(function (p) { return '<li>' + p + '</li>'; }).join('') + '</ul>'
        : '<strong>Config looks right.</strong> Found ' + names.length + ' server(s): ' + names.join(', ') + '. This checks the shape only, not the connection.';
    });
  }

  // Per-client config tabs on detail pages.
  document.querySelectorAll('[data-cfgtabs]').forEach(function (group) {
    var card = group.closest('section') || document;
    var btns = group.querySelectorAll('[data-cfg-btn]');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var target = btn.getAttribute('data-cfg-btn');
        btns.forEach(function (b) {
          var on = b === btn;
          b.classList.toggle('active', on);
          b.setAttribute('aria-selected', on ? 'true' : 'false');
        });
        card.querySelectorAll('[data-cfg-panel]').forEach(function (p) {
          p.hidden = p.getAttribute('data-cfg-panel') !== target;
        });
      });
    });
  });

  // Codeblock copy buttons (makeover pattern: button + sibling <pre>).
  document.querySelectorAll('.codeblock .copy-btn').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var pre = btn.parentElement.querySelector('pre');
      var text = pre ? pre.textContent : '';
      function done() { var old = btn.textContent; btn.textContent = 'Copied'; setTimeout(function () { btn.textContent = old; }, 1500); }
      if (navigator.clipboard && navigator.clipboard.writeText) { navigator.clipboard.writeText(text).then(done).catch(done); } else { done(); }
    });
  });
