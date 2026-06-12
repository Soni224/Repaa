#!/usr/bin/env python3
"""
SkillHunt Redesign Transformer v3
Transforms the gamified arcade into a clean professional tool.
"""

import re

INPUT = '/home/z/my-project/upload/index (16) (2).html'
OUTPUT = '/home/z/my-project/upload/SkillHunt_Redesign.html'

with open(INPUT, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
changes = []

def log(msg):
    changes.append(msg)
    print(f"  [OK] {msg}")

# ═══════════════════════════════════════════════════════════
# STEP 1: REMOVE GAMIFICATION CSS (using line-by-line approach)
# ═══════════════════════════════════════════════════════════

css_prefixes_to_remove = [
    '.streak-', '.hunter-', '.bounty-', '.ach-', '.lb-', '.loy-',
    '.ghost-', '.pulse-', '.intel-', '.radar-', '.profile-views-',
    '.loyalty-card',
]

lines = content.split('\n')
new_lines = []
skip_line = False
for line in lines:
    stripped = line.strip()
    should_remove = False
    
    # Check if this CSS rule starts with a gamification prefix
    for prefix in css_prefixes_to_remove:
        if stripped.startswith(prefix) or stripped.startswith('.dark ' + prefix):
            should_remove = True
            break
    
    # Also check for multi-line CSS rules that start with gamification prefixes
    # but have content on the same line (e.g. .streak-fire{font-size:28px})
    for prefix in css_prefixes_to_remove:
        if prefix in stripped and '{' in stripped and '}' in stripped:
            # Single-line CSS rule with gamification prefix
            should_remove = True
            break
    
    if not should_remove:
        new_lines.append(line)

content = '\n'.join(new_lines)
log('Removed gamification CSS by prefix matching')

# ═══════════════════════════════════════════════════════════
# STEP 2: REMOVE GAMIFICATION HTML CONTAINERS
# ═══════════════════════════════════════════════════════════

content = content.replace(
    '          <!-- Pro Impact Card -->\n          <div id="proImpactContainer"></div>',
    '          <!-- Pro Impact moved to More > Тариф -->'
)
log('Removed proImpactContainer div from home page')

content = content.replace(
    '          <!-- Profile Views Widget -->\n          <div id="profileViewsContainer"></div>',
    ''
)
log('Removed profileViewsContainer div from home page')

content = content.replace(
    '          <!-- Habit-Forming Widgets Container -->\n          <div id="habitWidgets"></div>',
    ''
)
log('Removed habitWidgets div from home page')

# ═══════════════════════════════════════════════════════════
# STEP 3: RESTRUCTURE HOME PAGE - Compact Greeting
# ═══════════════════════════════════════════════════════════

# Replace hero-metrics with a single subtle line
content = content.replace(
    '''          <!-- Minimal Metrics — Just 2 -->
          <div class="hero-metrics animate-in">
            <div class="hero-metric" onclick="showApplicationsView()">
              <div class="hero-metric-dot" style="background:var(--primary);box-shadow:0 0 6px rgba(108,123,212,.4)"></div>
              <div class="hero-metric-info">
                <div class="hero-metric-val">12</div>
                <div class="hero-metric-label">Заказы</div>
              </div>
            </div>
            <div class="hero-metric" onclick="showApplicationsView()">
              <div class="hero-metric-dot" style="background:var(--success);box-shadow:0 0 6px rgba(76,175,125,.4)"></div>
              <div class="hero-metric-info">
                <div class="hero-metric-val" id="heroAppCount">5</div>
                <div class="hero-metric-label">Отклики</div>
              </div>
            </div>
          </div>''',
    '''          <!-- Subtle metric -->
          <div style="font-size:12px;color:var(--text-3);font-family:var(--font-sans);margin-bottom:4px" class="animate-in" id="heroSubtext">5 подходящих заказов</div>'''
)
log('Replaced hero-metrics with compact single-line metric')

# Make AI card more compact
content = content.replace(
    '''          <!-- AI Hero Card — One Clear Action -->
          <div class="hero-ai-card animate-in dot-pattern">
            <div class="hero-ai-match">
              <div class="hero-ai-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>
              </div>
              <div class="hero-ai-text">
                <div class="hero-ai-headline"><b>3 заказа</b> совпадают на 85%+</div>
                <div class="hero-ai-reason">
                  <span class="hero-ai-reason-tag">GPT API</span>
                  <span class="hero-ai-reason-tag">React</span>
                  <span class="hero-ai-reason-tag">Python</span>
                  <span style="color:var(--text-3)">— по вашим навыкам</span>
                </div>
              </div>
            </div>
            <button class="hero-cta" onclick="filterFeedCategory('ai');showToast('Показаны релевантные заказы')">
              <span class="hero-cta-shimmer"></span>
              Посмотреть заказы
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
            <div class="hero-secondary">или <span onclick="switchTab(1)">настроить фильтры</span></div>
          </div>''',
    '''          <!-- Compact AI match hint -->
          <div class="animate-in" style="display:flex;align-items:center;gap:8px;padding:10px 14px;background:var(--primary-soft);border-radius:var(--radius-sm);margin-bottom:12px;border:1px solid rgba(108,123,212,.1)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--primary)" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>
            <span style="font-size:12px;color:var(--text-2);font-family:var(--font-sans)"><b style="color:var(--primary)">3 заказа</b> совпадают на 85%+</span>
            <button style="margin-left:auto;font-size:11px;font-weight:600;color:var(--primary);font-family:var(--font-sans)" onclick="filterFeedCategory('ai')">Смотреть</button>
          </div>'''
)
log('Replaced hero-ai-card with compact match hint')

# ═══════════════════════════════════════════════════════════
# STEP 4: FIX EARLY ACCESS CARDS - subtle CSS only
# ═══════════════════════════════════════════════════════════

content = re.sub(
    r'\.card-early-access\{[^}]+\}',
    '.card-early-access{border-left:3px solid rgba(212,160,58,.6)!important;background:rgba(212,160,58,.03)!important}',
    content
)
log('Updated card-early-access CSS')

content = re.sub(
    r'\.dark \.card-early-access\{[^}]+\}',
    '.dark .card-early-access{border-left:3px solid rgba(212,160,58,.5)!important;background:rgba(212,160,58,.06)!important}',
    content
)
log('Updated dark mode card-early-access CSS')

content = re.sub(r'\.card-early-access::after\{[^}]+\}', '', content)
log('Removed card-early-access::after shimmer')

# ═══════════════════════════════════════════════════════════
# STEP 5: REMOVE GAMIFICATION JS FUNCTIONS
# ═══════════════════════════════════════════════════════════

# Remove entire habit-forming section between markers
# We'll target specific function blocks

js_functions_to_remove = [
    'getStreakData',
    'saveStreakData', 
    'checkStreak',
    'useStreakFreeze',
    'renderStreakWidget',
    'getHunterData',
    'calcHunterScore',
    'getNextLevel',
    'renderHunterScore',
    'getBounties',
    'bumpBounty',
    'renderBounties',
    'renderAchievements',
    'checkAchievements',
    'generateIntel',
    'renderIntelFeed',
    'getMarketPulse',
    'renderMarketPulse',
    'getLoyaltyData',
    'addLoyaltyPoints',
    'purchaseLoyaltyItem',
    'renderLoyalty',
    'getLeaderboard',
    'renderLeaderboard',
    'renderSkillRadar',
    'renderHabitWidgets',
    'renderProfileViews',
    'renderProImpact',
    'renderClientInsights',
    'renderClientInsightsLocked',
]

for func_name in js_functions_to_remove:
    # Match function declarations with various signatures
    # Pattern: function name(...) { ... } where braces are balanced
    pattern = r'function ' + func_name + r'\s*\([^)]*\)\s*\{'
    
    # Find the start position
    match = re.search(pattern, content)
    if match:
        start = match.start()
        # Find matching closing brace
        brace_count = 0
        pos = match.end() - 1  # position of opening brace
        for i in range(pos, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end = i + 1
                    content = content[:start] + content[end:]
                    log(f'Removed function {func_name}')
                    break

# Remove ACHIEVEMENTS constant
content = re.sub(
    r"const ACHIEVEMENTS = \[.+?\];",
    '', content, flags=re.DOTALL
)
log('Removed ACHIEVEMENTS constant')

# Remove getAchievements function (simple one-liner)
content = re.sub(r"function getAchievements\(\)\s*\{[^}]*\}", '', content)
log('Removed getAchievements function')

# Remove section headers
for header in [
    "// ── Feature 1: Daily Hunt Streak ──",
    "// ── Feature 2: Hunter Score ──",
    "// ── Feature 3: Daily Bounties ──",
    "// ── Feature 5: Achievement Badges ──",
    "// ── Feature 6: Intelligence Feed ──",
    "// ── Feature 7: Market Pulse ──",
    "// ── Feature 8: Loyalty Points & Shop ──",
    "// ── Feature 9: Weekly Leaderboard ──",
    "// ── Feature 10: Skill Radar ──",
    "// ── Master Render: All Habit Widgets ──",
    "// ── Profile Views Widget (Home Page) ──",
    "// ── Pro Impact Card ──",
]:
    content = content.replace(header, '')

# Remove the big section header
content = content.replace("// ═══════════════════════════════════════════════════════════\n// ── Habit-Forming Features Engine ──\n// ═══════════════════════════════════════════════════════════", "")

log('Removed section headers')

# ═══════════════════════════════════════════════════════════
# STEP 6: REMOVE bumpBounty/addLoyaltyPoints CALLS
# ═══════════════════════════════════════════════════════════

# Remove bumpBounty calls
content = re.sub(r"\s*bumpBounty\([^)]*\);\s*//?[^\n]*", '', content)
content = re.sub(r"\s*bumpBounty\([^)]*\);\s*", '', content)
log('Removed all bumpBounty calls')

# Remove addLoyaltyPoints calls
content = re.sub(r"\s*addLoyaltyPoints\([^)]*\);\s*//?[^\n]*", '', content)
content = re.sub(r"\s*addLoyaltyPoints\([^)]*\);\s*", '', content)
log('Removed all addLoyaltyPoints calls')

# Remove checkStreak call from init
content = content.replace("  checkStreak();\n", '')
log('Removed checkStreak call from init')

# Remove renderHabitWidgets calls
content = re.sub(r"\s*renderHabitWidgets\(\);\s*", '', content)
log('Removed renderHabitWidgets calls')

# Remove renderProfileViews calls
content = re.sub(r"\s*renderProfileViews\(\);\s*", '', content)
log('Removed renderProfileViews calls')

# Remove renderProImpact calls
content = re.sub(r"\s*renderProImpact\(\);\s*", '', content)
log('Removed renderProImpact calls')

# Remove Client Insights from job detail
content = re.sub(
    r'\$\{isPro\(\) \? renderClientInsights\(job\) : renderClientInsightsLocked\(\)\}',
    '', content
)
log('Removed client insights from job detail')

# ═══════════════════════════════════════════════════════════
# STEP 7: REMOVE GHOST COUNTER FROM JOB CARDS
# ═══════════════════════════════════════════════════════════

# Remove ghost counter variable
content = re.sub(
    r"  const seed = job\.id \* 2654435761 >>> 0;\n  const viewing = 8 \+ \(seed % 40\);\n  const applicants = \(seed >> 8\) % 13;\n  const trendUp = \(seed >> 16\) % 4 \+ 1;\n  const ghostHtml = pro\s*\n\s*\? `[^`]+`\s*\n\s*: `[^`]+`;",
    '', content
)
log('Removed ghost counter from renderJobCard')

# Remove ${ghostHtml} from card template
content = content.replace("      ${ghostHtml}", '')
log('Removed ghost counter from card template')

# ═══════════════════════════════════════════════════════════
# STEP 8: REPLACE ALL EMOJI
# ═══════════════════════════════════════════════════════════

# Toast messages
content = content.replace("showToast('🎉 Pro-триал активирован на 3 дня!');", "showToast('Pro-триал активирован на 3 дня');")
content = content.replace("showToast('✨ Pro подписка активирована!');", "showToast('Pro подписка активирована');")
content = content.replace("showToast('✨ AI-отклик отправлен! Клиент получит уведомление.');", "showToast('AI-отклик отправлен. Клиент получит уведомление.');")
content = content.replace("showToast('Заказ сохранён ❤️');", "showToast('Заказ сохранён');")
log('Updated toast messages - removed emoji')

# Remove all emoji characters
emoji_list = ['🔥','🎯','👁️','⚡','🏅','💎','🏆','📊','🕵️','🎨','📋','❄️','🎁','🎉','✨','❤️','👋','🚀','💰','👇','⚠️','🤖','💾','👀','📈','🤝','👑','🔒','✅']
for emoji in emoji_list:
    if emoji in content:
        content = content.replace(emoji, '')

# Catch any remaining emoji with a broad Unicode pattern
remaining = re.findall(r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\U0001F600-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]', content)
if remaining:
    for em in set(remaining):
        content = content.replace(em, '')
    log(f'Removed {len(set(remaining))} additional emoji types')

log('Removed all emoji from file')

# ═══════════════════════════════════════════════════════════
# STEP 9: UPDATE PRO FEATURE LISTS
# ═══════════════════════════════════════════════════════════

# Remove "Инсайты клиентов" from trial welcome overlay
content = content.replace('''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-insight"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
          <div><div class="trial-welcome-feat-title">Инсайты клиентов</div><div class="trial-welcome-feat-desc">Узнайте, кто платит и как быстро</div></div>
        </div>''', '')
log('Removed "Инсайты клиентов" from trial welcome')

# Remove "Кто смотрел профиль" from trial welcome overlay
content = content.replace('''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-views"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></div>
          <div><div class="trial-welcome-feat-title">Кто смотрел профиль</div><div class="trial-welcome-feat-desc">Не упускайте возможности — узнайте, кто вас ищет</div></div>
        </div>''', '')
log('Removed "Кто смотрел профиль" from trial welcome')

# Remove "Разведка и стрики" from trial welcome overlay
content = content.replace('''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico" style="background:linear-gradient(135deg,var(--warning),#E8B84A)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
          <div><div class="trial-welcome-feat-title">Разведка и стрики</div><div class="trial-welcome-feat-desc">Аналитика рынка, серия охоты, x2 награды и рейтинг</div></div>
        </div>''', '')
log('Removed "Разведка и стрики" from trial welcome')

# Add new Pro features to trial welcome
new_features_html = '''
        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-ai"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div><div class="trial-welcome-feat-title">AI-сопроводительное письмо</div><div class="trial-welcome-feat-desc">Персонализированный отклик за 5 секунд</div></div>
        </div>
        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico" style="background:linear-gradient(135deg,var(--sky),var(--primary))"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
          <div><div class="trial-welcome-feat-title">Все заказы</div><div class="trial-welcome-feat-desc">На Free видно только 6 из 15 заказов</div></div>
        </div>'''

# Insert after the "Безлимитные отклики и сохранения" feature
anchor = '          <div><div class="trial-welcome-feat-title">Безлимитные отклики и сохранения</div><div class="trial-welcome-feat-desc">На Free всего 3 отклика и 3 сохранения в месяц</div></div>\n        </div>'
if anchor in content:
    content = content.replace(anchor, anchor + new_features_html)
    log('Added "AI-сопроводительное письмо" and "Все заказы" to trial welcome')

# Update trial bar sub-text for Free users
content = content.replace(
    "AI-анализ · Стратегия · Ранний доступ · Инсайты",
    "AI-анализ · Стратегия · Ранний доступ"
)
log('Updated trial bar sub-text')

# Update showProUpgrade description
content = content.replace(
    "Получите безлимитные отклики, AI и приоритет",
    "Безлимитные отклики, AI-анализ и ранний доступ"
)
log('Updated showProUpgrade description')

# Update trial end sub text
content = content.replace(
    "Не теряйте momentum — сохраните Pro",
    "Сохраните доступ к Pro-возможностям"
)
log('Updated trial end sub-text')

# ═══════════════════════════════════════════════════════════
# STEP 10: UPDATE TARIFF TABLE - remove rows
# ═══════════════════════════════════════════════════════════

# These are in the dynamic JS string in openMoreSub('tariff')
# Simple string replacements since the text is unique enough

# Remove "Инсайты клиентов" from tariff card feature list
content = content.replace(
    '''Инсайты клиентов</div>''',
    ''  # Remove the whole div by removing the distinctive text
)
log('Removed "Инсайты клиентов" from tariff features')

# Remove "Кто смотрел профиль" from tariff card feature list
content = content.replace(
    '''Кто смотрел профиль</div>''',
    ''
)
log('Removed "Кто смотрел профиль" from tariff features')

# Remove "Инсайты клиентов" row from comparison table (dynamically built)
# The row text is unique, let's find and remove it
content = content.replace(
    '>Инсайты клиентов</td>',
    '>REMOVED_INSIGHTS</td>'  # Mark first, then remove the whole row
)

# Remove "Кто смотрел профиль" row from comparison table
content = content.replace(
    '>Кто смотрел профиль</td>',
    '>REMOVED_PROFILE_VIEWS</td>'
)

# Now remove the marked rows (they're in JS template strings)
# Pattern: entire <tr>...</tr> containing the marker
content = re.sub(r"<tr[^>]*>.*?REMOVED_INSIGHTS.*?</tr>", '', content, flags=re.DOTALL)
content = re.sub(r"<tr[^>]*>.*?REMOVED_PROFILE_VIEWS.*?</tr>", '', content, flags=re.DOTALL)
log('Removed "Инсайты клиентов" and "Кто смотрел профиль" from tariff comparison table')

# Add "AI-сопроводительное письмо" row to comparison table
# After "Ранний доступ" row
content = content.replace(
    "Ранний доступ</td>",
    "Ранний доступ</td></tr>' + '<tr style=\"border-top:1px solid var(--border-soft)\"><td style=\"padding:8px 10px;font-weight:500;color:var(--text)\">AI-сопроводительное письмо</td><td style=\"padding:8px 10px;text-align:center;color:var(--text-3)\">--</td><td style=\"padding:8px 10px;text-align:center;color:var(--primary);font-weight:600;' + proBg + '\">' + checkSvg + '</td"
)
log('Added "AI-сопроводительное письмо" to comparison table')

# ═══════════════════════════════════════════════════════════
# STEP 11: UPDATE LIMIT MESSAGES - CALM, PROFESSIONAL
# ═══════════════════════════════════════════════════════════

content = content.replace(
    "Разблокируйте безлимит с Pro",
    "Pro даёт безлимитные отклики"
)
log('Updated limit hit message')

content = content.replace(
    "Активируйте Pro со скидкой 50%!",
    "Pro даёт безлимитные отклики и AI"
)
log('Updated trial ending sub-text')

content = content.replace(
    "Лимит откликов",
    "Отклики использованы"
)
log('Updated "Лимит откликов" to "Отклики использованы"')

# ═══════════════════════════════════════════════════════════
# STEP 12: CLEAN UP
# ═══════════════════════════════════════════════════════════

# Remove multiple consecutive blank lines
content = re.sub(r'\n{4,}', '\n\n\n', content)
log('Cleaned up excessive blank lines')

# ═══════════════════════════════════════════════════════════
# CHECK FOR BROKEN REFERENCES
# ═══════════════════════════════════════════════════════════

broken_refs = [
    'renderHabitWidgets', 'renderProfileViews', 'renderProImpact',
    'checkStreak', 'renderStreakWidget', 'renderHunterScore',
    'renderBounties', 'renderAchievements', 'renderLoyalty',
    'renderIntelFeed', 'renderMarketPulse', 'renderLeaderboard',
    'renderSkillRadar', 'bumpBounty', 'addLoyaltyPoints',
    'getStreakData', 'getHunterData', 'getBounties',
    'getAchievements', 'checkAchievements', 'getLoyaltyData',
    'purchaseLoyaltyItem', 'getLeaderboard', 'generateIntel',
    'getMarketPulse', 'calcHunterScore', 'getNextLevel',
    'saveStreakData', 'useStreakFreeze',
    'renderClientInsights', 'renderClientInsightsLocked',
]

print("\n  Checking for broken references...")
for ref in broken_refs:
    # Look for function calls (not definitions)
    pattern = rf'(?<!function\s)(?<!const\s){ref}\s*\('
    matches = re.findall(pattern, content)
    if matches:
        print(f"  [WARN] Found {len(matches)} remaining reference(s) to {ref}")

# ═══════════════════════════════════════════════════════════
# WRITE OUTPUT
# ═══════════════════════════════════════════════════════════

with open(OUTPUT, 'w', encoding='utf-8') as f:
    f.write(content)

final_len = len(content)
reduction = original_len - final_len
pct = (reduction / original_len) * 100

print(f"\n{'='*60}")
print(f"TRANSFORMATION COMPLETE")
print(f"{'='*60}")
print(f"Original size: {original_len:,} chars")
print(f"Final size:    {final_len:,} chars")
print(f"Reduction:     {reduction:,} chars ({pct:.1f}%)")
print(f"Output:        {OUTPUT}")
print(f"\nChanges made: {len(changes)}")
for c in changes:
    print(f"  - {c}")
