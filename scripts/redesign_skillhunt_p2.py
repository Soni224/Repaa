#!/usr/bin/env python3
"""
SkillHunt Redesign Script — Phase 2: Add Responses screen, restructure navigation
"""
import re

FILE = '/home/z/my-project/upload/index (16) (2).html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Starting: {original_len} chars, {content.count(chr(10))} lines")

# ════════════════════════════════════════════════════════════════
# STEP 1: Change slider from 3 pages to 4 pages
# ════════════════════════════════════════════════════════════════

# 1a. Update slider-inner width from 300% to 400%
content = content.replace(
    '.slider-inner{display:flex;width:300%;height:100dvh;',
    '.slider-inner{display:flex;width:400%;height:100dvh;'
)

# 1b. Update slider-page from 33.333% to 25%
content = content.replace(
    '.slider-page{flex:0 0 33.333%;width:33.333%;',
    '.slider-page{flex:0 0 25%;width:25%;'
)

# 1c. Update switchTab translateX calculation
content = content.replace(
    "inner.style.transform = `translateX(-${index * 33.333}%)`;",
    "inner.style.transform = `translateX(-${index * 25}%)`;"
)

# 1d. Update swipe boundaries from < 2 to < 3
content = content.replace(
    "if (diffX > 0 && currentTab < 2) switchTab(currentTab + 1);",
    "if (diffX > 0 && currentTab < 3) switchTab(currentTab + 1);"
)

# ════════════════════════════════════════════════════════════════
# STEP 2: Add new page 3 — Отклики (Responses/History)
# ════════════════════════════════════════════════════════════════

# Insert after the closing </div> of page2 (Сохранённые)
saved_page_end = content.find('      <!-- ═══ Page 3: Сохранённые (Saved) — Redesigned ═══ -->')
if saved_page_end == -1:
    # Try alternate marker
    saved_page_end = content.find('<!-- ═══ Page 3: Сохранённые')

# Actually let's find the end of page2's slider-page div
# After page2 (Сохранённые), there are closing divs before the slider-inner close
# Find the pattern: after savedJobList content, before the slider-inner closes

responses_page_html = '''
      <!-- ═══ Page 4: Отклики (Responses) ═══ -->
      <div class="slider-page" id="page3" role="region" aria-label="Отклики">
        <div class="content" id="responsesContent">

          <!-- Responses Header -->
          <div class="animate-in">
            <div class="page-header">
              <div class="page-header-ico ico-primary">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
              </div>
              <div>
                <div class="page-header-title gradient-text">Отклики</div>
                <div class="page-header-sub">Статус ваших откликов</div>
              </div>
            </div>
          </div>

          <!-- Response Status Filter -->
          <div class="animate-in mb-12">
            <div class="tabs" id="responseStatusTabs" style="flex-wrap:wrap">
              <button class="tab active" data-status="all" onclick="filterResponses('all',this)">Все</button>
              <button class="tab" data-status="sent" onclick="filterResponses('sent',this)">Отправленные</button>
              <button class="tab" data-status="viewed" onclick="filterResponses('viewed',this)">Просмотренные</button>
              <button class="tab" data-status="replied" onclick="filterResponses('replied',this)">Ответили</button>
            </div>
          </div>

          <!-- Response Summary -->
          <div class="animate-in mb-12" id="responseSummary"></div>

          <!-- Responses List -->
          <div id="responsesList"></div>

          <!-- Responses Empty -->
          <div id="responsesEmpty" class="empty" style="display:none">
            <div class="empty-illust">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            </div>
            <div class="empty-title">Пока нет откликов</div>
            <div class="empty-desc">Найдите подходящий заказ и отправьте отклик — он появится здесь</div>
            <button class="btn btn-p" onclick="switchTab(1)">Найти заказы</button>
          </div>

        </div>
      </div>
'''

# Find the closing tags after page2 and insert before slider-inner closing
# The structure is: </div> (page2) </div> (slider-inner)
# Find the marker after page2 content
insert_marker = '      </div>\n\n    </div>\n  </div>\n\n  <!-- ═══ Bottom Navigation ═══ -->'
if insert_marker in content:
    content = content.replace(
        insert_marker,
        responses_page_html + '\n    </div>\n  </div>\n\n  <!-- ═══ Bottom Navigation ═══ -->'
    )
    print("✓ Inserted Responses page HTML")
else:
    print("⚠ Could not find insertion point for Responses page")
    # Try alternate approach
    alt_marker = '    </div>\n  </div>\n\n  <!-- ═══ Bottom Navigation ═══ -->'
    if alt_marker in content:
        content = content.replace(
            alt_marker,
            responses_page_html + '    </div>\n  </div>\n\n  <!-- ═══ Bottom Navigation ═══ -->'
        )
        print("✓ Inserted Responses page HTML (alt marker)")

# ════════════════════════════════════════════════════════════════
# STEP 3: Restructure bottom navigation — 4 direct tabs
# ════════════════════════════════════════════════════════════════

# Replace entire nav with: Лента, Поиск, Отклики, Ещё
# (Сохранённые moved to Feed header as bookmark icon)

new_nav = '''  <!-- ═══ Bottom Navigation ═══ -->
  <nav class="bnav" id="bnav" role="navigation" aria-label="Основная навигация">
    <div class="bnav-in">
      <div class="bnav-pill" id="navPill"></div>
      <button class="bnav-i active" data-tab="0" onclick="switchTab(0)" aria-label="Лента">
        <div class="bnav-i-ico">
          <svg class="ico-outline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
          <svg class="ico-filled" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><rect x="9" y="12" width="6" height="10"/></svg>
        </div>
        <span>Лента</span>
      </button>
      <button class="bnav-i" data-tab="1" onclick="switchTab(1)" aria-label="Поиск">
        <div class="bnav-i-ico">
          <svg class="ico-outline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <svg class="ico-filled" viewBox="0 0 24 24" fill="currentColor" stroke="none"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65" stroke="currentColor" stroke-width="2.5"/></svg>
        </div>
        <span>Поиск</span>
      </button>
      <button class="bnav-i" data-tab="3" onclick="switchTab(3)" aria-label="Отклики">
        <div class="bnav-i-ico">
          <svg class="ico-outline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
          <svg class="ico-filled" viewBox="0 0 24 24" fill="currentColor" stroke="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
        </div>
        <span>Отклики</span>
      </button>
      <button class="bnav-i" data-tab="more" onclick="openMorePanel()" aria-label="Ещё">
        <div class="bnav-i-ico">
          <svg class="ico-outline" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="1"/><circle cx="19" cy="12" r="1"/><circle cx="5" cy="12" r="1"/></svg>
          <svg class="ico-filled" viewBox="0 0 24 24" fill="currentColor" stroke="none"><circle cx="12" cy="12" r="2.5"/><circle cx="19" cy="12" r="2.5"/><circle cx="5" cy="12" r="2.5"/></svg>
        </div>
        <span>Ещё</span>
      </button>
    </div>
  </nav>'''

# Find and replace the nav section
nav_start = content.find('  <!-- ═══ Bottom Navigation ═══ -->')
nav_end = content.find('</nav>', nav_start) + len('</nav>')
if nav_start != -1 and nav_end != -1:
    content = content[:nav_start] + new_nav + content[nav_end:]
    print("✓ Replaced bottom navigation")

# ════════════════════════════════════════════════════════════════
# STEP 4: Add saved-jobs icon to Feed header (bookmark)
# ════════════════════════════════════════════════════════════════

# Add a bookmark button to the hero greeting row
content = content.replace(
    '''          <!-- Hero Greeting — Calm & Professional -->
          <div class="hero-greeting animate-in" id="feedGreeting">
            <div class="hero-greeting-row">
              <div class="hero-greeting-avatar" id="userAvatar">А</div>
              <div class="hero-greeting-body">
                <div class="hero-greeting-time" id="greetingTime">Добрый день,</div>
                <div class="hero-greeting-name" id="userName">Александр</div>
              </div>
            </div>
          </div>''',
    '''          <!-- Hero Greeting — Calm & Professional -->
          <div class="hero-greeting animate-in" id="feedGreeting">
            <div class="hero-greeting-row">
              <div class="hero-greeting-avatar" id="userAvatar">А</div>
              <div class="hero-greeting-body">
                <div class="hero-greeting-time" id="greetingTime">Добрый день,</div>
                <div class="hero-greeting-name" id="userName">Александр</div>
              </div>
              <button style="width:36px;height:36px;border-radius:10px;background:var(--bg-card);border:1px solid var(--border-soft);display:flex;align-items:center;justify-content:center;cursor:pointer;flex-shrink:0;transition:all .2s" onclick="switchTab(2)" aria-label="Сохранённые заказы">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="var(--text-2)" stroke-width="2"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>
              </button>
            </div>
          </div>'''
)
print("✓ Added bookmark icon to Feed header")

# ════════════════════════════════════════════════════════════════
# STEP 5: Update switchTab JS to handle 4 pages
# ════════════════════════════════════════════════════════════════

# Update tab names array
content = content.replace(
    "const tabNames = ['Лента', 'Поиск', 'Сохранённые'];",
    "const tabNames = ['Лента', 'Поиск', 'Сохранённые', 'Отклики'];"
)

# Add Responses tab refresh in switchTab
content = content.replace(
    '''  // Refresh content when switching tabs
  if (index === 2) renderSavedJobs();
  if (index === 1) renderSearchResults();''',
    '''  // Refresh content when switching tabs
  if (index === 2) renderSavedJobs();
  if (index === 1) renderSearchResults();
  if (index === 3) renderResponses();'''
)

# ════════════════════════════════════════════════════════════════
# STEP 6: Add Responses rendering JavaScript
# ════════════════════════════════════════════════════════════════

responses_js = '''
// ── Responses/History Screen ──
let responseFilter = 'all';

function filterResponses(status, btn) {
  responseFilter = status;
  // Update tabs
  document.querySelectorAll('#responseStatusTabs .tab').forEach(t => t.classList.remove('active'));
  if (btn) btn.classList.add('active');
  renderResponses();
}

function renderResponses() {
  const apps = lsGetJSON('skillhunt_applications', []);
  const container = document.getElementById('responsesList');
  const emptyEl = document.getElementById('responsesEmpty');
  const summaryEl = document.getElementById('responseSummary');
  if (!container) return;
  
  // Simulate status transitions for mock data
  const now = Date.now();
  apps.forEach(app => {
    if (!app.status) app.status = 'sent';
    if (app.status === 'sent') {
      const sentTime = new Date(app.date).getTime();
      const hoursPassed = (now - sentTime) / (1000 * 60 * 60);
      if (hoursPassed > 48) app.status = 'viewed';
    }
    if (app.status === 'viewed') {
      const sentTime = new Date(app.date).getTime();
      const hoursPassed = (now - sentTime) / (1000 * 60 * 60);
      if (hoursPassed > 96 && Math.random() > 0.5) app.status = 'replied';
    }
  });
  lsSetJSON('skillhunt_applications', apps);
  
  // Filter
  const filtered = responseFilter === 'all' ? apps : apps.filter(a => a.status === responseFilter);
  
  // Summary
  const sent = apps.filter(a => a.status === 'sent').length;
  const viewed = apps.filter(a => a.status === 'viewed').length;
  const replied = apps.filter(a => a.status === 'replied').length;
  const total = apps.length;
  
  if (summaryEl) {
    summaryEl.innerHTML = `
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
        <div style="text-align:center;padding:10px;background:var(--primary-light);border-radius:var(--radius-xs)">
          <div style="font-size:18px;font-weight:700;color:var(--primary)">${sent}</div>
          <div style="font-size:10px;color:var(--text-3);font-weight:600">Отправлено</div>
        </div>
        <div style="text-align:center;padding:10px;background:var(--sky-light);border-radius:var(--radius-xs)">
          <div style="font-size:18px;font-weight:700;color:var(--sky)">${viewed}</div>
          <div style="font-size:10px;color:var(--text-3);font-weight:600">Просмотрено</div>
        </div>
        <div style="text-align:center;padding:10px;background:var(--success-light);border-radius:var(--radius-xs)">
          <div style="font-size:18px;font-weight:700;color:var(--success)">${replied}</div>
          <div style="font-size:10px;color:var(--text-3);font-weight:600">Ответили</div>
        </div>
      </div>`;
  }
  
  if (filtered.length === 0) {
    container.innerHTML = '';
    if (emptyEl) emptyEl.style.display = 'block';
    return;
  }
  
  if (emptyEl) emptyEl.style.display = 'none';
  
  // Sort by date descending
  filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
  
  const statusConfig = {
    sent: { label: 'Отправлено', color: 'var(--primary)', bg: 'var(--primary-light)', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>' },
    viewed: { label: 'Просмотрено', color: 'var(--sky)', bg: 'var(--sky-light)', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>' },
    replied: { label: 'Ответили', color: 'var(--success)', bg: 'var(--success-light)', icon: '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>' }
  };
  
  container.innerHTML = filtered.map(app => {
    const job = MOCK_JOBS.find(j => j.id === app.jobId);
    if (!job) return '';
    const st = statusConfig[app.status] || statusConfig.sent;
    const dateStr = formatDate(app.date);
    const aiBadge = app.aiGenerated ? '<span style="font-size:9px;font-weight:700;color:var(--lavender);background:var(--lavender-light);padding:2px 6px;border-radius:var(--radius-full)">AI</span>' : '';
    
    return `
      <div class="card animate-in" style="padding:14px;margin-bottom:8px;cursor:pointer" onclick="openJobDetail(${job.id})">
        <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:8px">
          <div style="display:flex;align-items:center;gap:6px">
            <span style="display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:var(--radius-full);font-size:10px;font-weight:600;color:${st.color};background:${st.bg}">${st.icon} ${st.label}</span>
            ${aiBadge}
          </div>
          <span style="font-size:10px;color:var(--text-3)">${dateStr}</span>
        </div>
        <div style="font-size:14px;font-weight:600;color:var(--text);margin-bottom:4px;line-height:1.3">${esc(job.title)}</div>
        <div style="font-size:12px;color:var(--text-2)">$${job.budgetMin.toLocaleString()} — $${job.budgetMax.toLocaleString()}</div>
      </div>`;
  }).join('');
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  const now = new Date();
  const diffMs = now - d;
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);
  
  if (diffMins < 1) return 'Только что';
  if (diffMins < 60) return diffMins + ' мин. назад';
  if (diffHours < 24) return diffHours + ' ч. назад';
  if (diffDays < 7) return diffDays + ' дн. назад';
  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
}

function showApplicationsView() {
  switchTab(3);
}
'''

# Insert the responses JS before the init function
content = content.replace(
    '// ── Gamification features removed ─\n\nfunction init()',
    responses_js + '\n// ── Init ──\nfunction init()'
)
print("✓ Added Responses JavaScript")

# ════════════════════════════════════════════════════════════════
# STEP 7: Add Responses CSS for status indicators
# ════════════════════════════════════════════════════════════════

responses_css = '''
/* ── Responses Status Indicators ── */
.response-status{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:var(--radius-full);font-size:10px;font-weight:600}
.response-status.sent{color:var(--primary);background:var(--primary-light)}
.response-status.viewed{color:var(--sky);background:var(--sky-light)}
.response-status.replied{color:var(--success);background:var(--success-light)}
.response-status svg{width:12px;height:12px}
'''

# Insert CSS before the shell styles
content = content.replace(
    '/* ── Shell ── */',
    responses_css + '\n/* ── Shell ── */'
)
print("✓ Added Responses CSS")

# ════════════════════════════════════════════════════════════════
# STEP 8: Update init() to render responses
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '''    renderFeed();
    renderSearchResults();
    renderSavedJobs();''',
    '''    renderFeed();
    renderSearchResults();
    renderSavedJobs();
    renderResponses();'''
)
print("✓ Updated init() to render responses")

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nFinal: {new_len} chars, {content.count(chr(10))} lines")
print(f"Added: {new_len - original_len} chars")
print("Phase 2 complete!")
