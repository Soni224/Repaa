#!/usr/bin/env python3
"""
SkillHunt Redesign Transformer v2
Transforms the gamified arcade into a clean professional tool.
"""

import re
import sys

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
# STEP 1: REMOVE GAMIFICATION CSS
# ═══════════════════════════════════════════════════════════

# Remove CSS blocks for gamification features
css_blocks_to_remove = [
    # Streak CSS
    (r'\.streak-fire\{[^}]+\}', 'streak-fire CSS'),
    (r'\.streak-info\{[^}]+\}', 'streak-info CSS'),
    (r'\.streak-count\{[^}]+\}', 'streak-count CSS'),
    (r'\.streak-label\{[^}]+\}', 'streak-label CSS'),
    (r'\.streak-days\{[^}]+\}', 'streak-days CSS'),
    (r'\.streak-day\{[^}]+\}', 'streak-day CSS'),
    (r'\.streak-day\.done\{[^}]+\}', 'streak-day.done CSS'),
    (r'\.streak-day\.today\{[^}]+\}', 'streak-day.today CSS'),
    (r'\.streak-day\.future\{[^}]+\}', 'streak-day.future CSS'),
    (r'\.streak-row\{[^}]+\}', 'streak-row CSS'),
    (r'\.streak-num\{[^}]+\}', 'streak-num CSS'),
    (r'\.streak-dots\{[^}]+\}', 'streak-dots CSS'),
    (r'\.streak-dot\{[^}]+\}', 'streak-dot CSS'),
    (r'\.streak-dot\.done\{[^}]+\}', 'streak-dot.done CSS'),
    (r'\.streak-dot\.today\{[^}]+\}', 'streak-dot.today CSS'),
    (r'\.streak-dot\.empty\{[^}]+\}', 'streak-dot.empty CSS'),
    (r'\.streak-freeze\{[^}]+\}', 'streak-freeze CSS'),
    (r'\.streak-freeze:hover\{[^}]+\}', 'streak-freeze:hover CSS'),
    
    # Hunter CSS
    (r'\.hunter-ring-wrap\{[^}]+\}', 'hunter-ring-wrap CSS'),
    (r'\.hunter-ring\{[^}]+\}', 'hunter-ring CSS'),
    (r'\.hunter-ring svg\{[^}]+\}', 'hunter-ring svg CSS'),
    (r'\.hunter-ring circle\{[^}]+\}', 'hunter-ring circle CSS'),
    (r'\.hunter-ring \.ring-bg\{[^}]+\}', 'hunter-ring .ring-bg CSS'),
    (r'\.hunter-ring \.ring-fill\{[^}]+\}', 'hunter-ring .ring-fill CSS'),
    (r'\.hunter-score-val\{[^}]+\}', 'hunter-score-val CSS'),
    (r'\.hunter-info\{[^}]+\}', 'hunter-info CSS'),
    (r'\.hunter-level\{[^}]+\}', 'hunter-level CSS'),
    (r'\.hunter-next\{[^}]+\}', 'hunter-next CSS'),
    (r'\.hunter-xp-bar\{[^}]+\}', 'hunter-xp-bar CSS'),
    (r'\.hunter-xp-fill\{[^}]+\}', 'hunter-xp-fill CSS'),
    
    # Bounty CSS
    (r'\.bounty-item\{[^}]+\}', 'bounty-item CSS'),
    (r'\.bounty-item:last-child\{[^}]+\}', 'bounty-item:last-child CSS'),
    (r'\.bounty-ico\{[^}]+\}', 'bounty-ico CSS'),
    (r'\.bounty-body\{[^}]+\}', 'bounty-body CSS'),
    (r'\.bounty-label\{[^}]+\}', 'bounty-label CSS'),
    (r'\.bounty-bar\{[^}]+\}', 'bounty-bar CSS'),
    (r'\.bounty-fill\{[^}]+\}', 'bounty-fill CSS'),
    (r'\.bounty-fill\.complete\{[^}]+\}', 'bounty-fill.complete CSS'),
    (r'\.bounty-reward\{[^}]+\}', 'bounty-reward CSS'),
    
    # Ghost counter CSS
    (r'\.ghost-counter\{[^}]+\}', 'ghost-counter CSS'),
    (r'\.ghost-counter span\{[^}]+\}', 'ghost-counter span CSS'),
    (r'\.ghost-trend\{[^}]+\}', 'ghost-trend CSS'),
    
    # Achievement CSS
    (r'\.ach-grid\{[^}]+\}', 'ach-grid CSS'),
    (r'\.ach-item\{[^}]+\}', 'ach-item CSS'),
    (r'\.ach-ring\{[^}]+\}', 'ach-ring CSS'),
    (r'\.ach-ring\.bronze\{[^}]+\}', 'ach-ring.bronze CSS'),
    (r'\.ach-ring\.silver\{[^}]+\}', 'ach-ring.silver CSS'),
    (r'\.ach-ring\.gold\{[^}]+\}', 'ach-ring.gold CSS'),
    (r'\.ach-ring\.locked\{[^}]+\}', 'ach-ring.locked CSS'),
    (r'\.ach-name\{[^}]+\}', 'ach-name CSS'),
    (r'\.ach-hint\{[^}]+\}', 'ach-hint CSS'),
    
    # Intel feed CSS
    (r'\.intel-item\{[^}]+\}', 'intel-item CSS'),
    (r'\.intel-item:last-child\{[^}]+\}', 'intel-item:last-child CSS'),
    (r'\.intel-ico\{[^}]+\}', 'intel-ico CSS'),
    (r'\.intel-text\{[^}]+\}', 'intel-text CSS'),
    (r'\.intel-text b\{[^}]+\}', 'intel-text b CSS'),
    (r'\.intel-time\{[^}]+\}', 'intel-time CSS'),
    
    # Market pulse CSS
    (r'\.pulse-row\{[^}]+\}', 'pulse-row CSS'),
    (r'\.pulse-row:last-child\{[^}]+\}', 'pulse-row:last-child CSS'),
    (r'\.pulse-cat\{[^}]+\}', 'pulse-cat CSS'),
    (r'\.pulse-bar\{[^}]+\}', 'pulse-bar CSS'),
    (r'\.pulse-fill\{[^}]+\}', 'pulse-fill CSS'),
    (r'\.pulse-trend\{[^}]+\}', 'pulse-trend CSS'),
    (r'\.pulse-up\{[^}]+\}', 'pulse-up CSS'),
    (r'\.pulse-down\{[^}]+\}', 'pulse-down CSS'),
    
    # Leaderboard CSS (in-page styles)
    (r'\.lb-item\{[^}]+\}', 'lb-item CSS'),
    (r'\.lb-item:last-child\{[^}]+\}', 'lb-item:last-child CSS'),
    (r'\.lb-item\.me\{[^}]+\}', 'lb-item.me CSS'),
    (r'\.lb-rank\{font-size[^}]+\}', 'lb-rank CSS (inline)'),
    (r'\.lb-rank\.gold\{color[^}]+\}', 'lb-rank.gold CSS'),
    (r'\.lb-rank\.silver\{color[^}]+\}', 'lb-rank.silver CSS'),
    (r'\.lb-rank\.bronze\{color[^}]+\}', 'lb-rank.bronze CSS'),
    (r'\.lb-av\{width:24px[^}]+\}', 'lb-av CSS (in-page)'),
    (r'\.lb-name\{flex:1[^}]+\}', 'lb-name CSS (in-page)'),
    (r'\.lb-xp\{[^}]+\}', 'lb-xp CSS'),
    
    # Skill radar CSS
    (r'\.radar-wrap\{[^}]+\}', 'radar-wrap CSS'),
    (r'\.radar-canvas\{[^}]+\}', 'radar-canvas CSS'),
    
    # Loyalty CSS
    (r'\.loy-balance\{[^}]+\}', 'loy-balance CSS'),
    (r'\.loy-label\{[^}]+\}', 'loy-label CSS'),
    (r'\.loy-shop\{[^}]+\}', 'loy-shop CSS'),
    (r'\.loy-item\{[^}]+\}', 'loy-item CSS'),
    (r'\.loy-item:hover\{[^}]+\}', 'loy-item:hover CSS'),
    (r'\.loy-item-name\{[^}]+\}', 'loy-item-name CSS'),
    (r'\.loy-item-cost\{[^}]+\}', 'loy-item-cost CSS'),
    
    # Profile views CSS
    (r'\.profile-views-widget\{[^}]+\}', 'profile-views-widget CSS'),
    (r'\.profile-views-header\{[^}]+\}', 'profile-views-header CSS'),
    (r'\.profile-views-title\{[^}]+\}', 'profile-views-title CSS'),
    (r'\.profile-views-title svg\{[^}]+\}', 'profile-views-title svg CSS'),
    (r'\.profile-views-count\{[^}]+\}', 'profile-views-count CSS'),
    (r'\.profile-views-list\{[^}]+\}', 'profile-views-list CSS'),
    (r'\.profile-views-item\{[^}]+\}', 'profile-views-item CSS'),
    (r'\.profile-views-item:hover\{[^}]+\}', 'profile-views-item:hover CSS'),
    (r'\.profile-views-avatar\{[^}]+\}', 'profile-views-avatar CSS'),
    (r'\.profile-views-info\{[^}]+\}', 'profile-views-info CSS'),
    (r'\.profile-views-name\{[^}]+\}', 'profile-views-name CSS'),
    (r'\.profile-views-detail\{[^}]+\}', 'profile-views-detail CSS'),
    (r'\.profile-views-time\{[^}]+\}', 'profile-views-time CSS'),
    (r'\.profile-views-gate\{[^}]+\}', 'profile-views-gate CSS'),
    (r'\.profile-views-gate-count\{[^}]+\}', 'profile-views-gate-count CSS'),
    (r'\.profile-views-gate-text\{[^}]+\}', 'profile-views-gate-text CSS'),
    (r'\.profile-views-gate-btn\{[^}]+\}', 'profile-views-gate-btn CSS'),
    (r'\.profile-views-gate-btn:hover\{[^}]+\}', 'profile-views-gate-btn:hover CSS'),
    
    # Dark mode hunter ring
    (r'\.dark \.hunter-ring \.ring-bg\{[^}]+\}', 'dark hunter-ring CSS'),
    
    # Leaderboard page 1 CSS (larger blocks)
    (r'\.lb-filter-tabs\{[^}]+\}', 'lb-filter-tabs CSS'),
    (r'\.lb-filter-tabs::-webkit-scrollbar\{[^}]+\}', 'lb-filter-tabs scrollbar CSS'),
    (r'\.lb-filter-tab\{[^}]+\}', 'lb-filter-tab CSS'),
    (r'\.lb-filter-tab\.active\{[^}]+\}', 'lb-filter-tab.active CSS'),
    (r'\.lb-your-card\{[^}]+\}', 'lb-your-card CSS'),
    (r'\.lb-your-rank\{[^}]+\}', 'lb-your-rank CSS'),
    (r'\.lb-your-info\{[^}]+\}', 'lb-your-info CSS'),
    (r'\.lb-your-name\{[^}]+\}', 'lb-your-name CSS'),
    (r'\.lb-your-score\{[^}]+\}', 'lb-your-score CSS'),
    (r'\.lb-row\{[^}]+\}', 'lb-row CSS'),
    (r'\.lb-row:hover\{[^}]+\}', 'lb-row:hover CSS'),
    (r'\.lb-rank\{width:24px[^}]+\}', 'lb-rank CSS (page1)'),
    (r'\.lb-rank\.gold\{background[^}]+\}', 'lb-rank.gold CSS (page1)'),
    (r'\.lb-rank\.silver\{background[^}]+\}', 'lb-rank.silver CSS (page1)'),
    (r'\.lb-rank\.bronze\{background[^}]+\}', 'lb-rank.bronze CSS (page1)'),
    (r'\.lb-av\{width:28px[^}]+\}', 'lb-av CSS (page1)'),
    (r'\.lb-name\{font-size:12px[^}]+\}', 'lb-name CSS (page1)'),
    (r'\.lb-score-val\{[^}]+\}', 'lb-score-val CSS'),
    (r'\.lb-plat-badges\{[^}]+\}', 'lb-plat-badges CSS'),
    (r'\.lb-plat-badge\{[^}]+\}', 'lb-plat-badge CSS'),
    (r'\.lb-plat-badge\.wb\{[^}]+\}', 'lb-plat-badge.wb CSS'),
    (r'\.lb-plat-badge\.ozon\{[^}]+\}', 'lb-plat-badge.ozon CSS'),
    (r'\.lb-plat-badge\.ym\{[^}]+\}', 'lb-plat-badge.ym CSS'),
    (r'\.lb-share-btn\{[^}]+\}', 'lb-share-btn CSS'),
    (r'\.lb-share-btn:hover\{[^}]+\}', 'lb-share-btn:hover CSS'),
    
    # Loyalty card CSS
    (r'\.loyalty-card\{[^}]+\}', 'loyalty-card CSS'),
]

for pattern, name in css_blocks_to_remove:
    new_content = re.sub(pattern, '', content)
    if new_content != content:
        content = new_content
        log(f'Removed {name}')

# ═══════════════════════════════════════════════════════════
# STEP 2: REMOVE GAMIFICATION HTML CONTAINERS
# ═══════════════════════════════════════════════════════════

# Remove proImpactContainer div
content = re.sub(
    r'\s*<!-- Pro Impact Card -->\s*<div id="proImpactContainer"></div>',
    '\n          <!-- Pro Impact moved to More → Тариф -->',
    content
)
log('Removed proImpactContainer div from home page')

# Remove profileViewsContainer div
content = re.sub(
    r'\s*<!-- Profile Views Widget -->\s*<div id="profileViewsContainer"></div>',
    '',
    content
)
log('Removed profileViewsContainer div from home page')

# Remove habitWidgets div
content = re.sub(
    r'\s*<!-- Habit-Forming Widgets Container -->\s*<div id="habitWidgets"></div>',
    '',
    content
)
log('Removed habitWidgets div from home page')

# ═══════════════════════════════════════════════════════════
# STEP 3: RESTRUCTURE HOME PAGE - Compact Greeting
# ═══════════════════════════════════════════════════════════

# Replace hero-metrics (two big metrics) with a single subtle line
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

# Make greeting more compact - replace hero-ai-card with a simpler version
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
# STEP 4: FIX EARLY ACCESS CARDS
# ═══════════════════════════════════════════════════════════

# Replace the card-early-access CSS with the new subtle style
content = re.sub(
    r'\.card-early-access\{[^}]+\}',
    '.card-early-access{border-left:3px solid rgba(212,160,58,.6)!important;background:rgba(212,160,58,.03)!important}',
    content
)
log('Updated card-early-access CSS - subtle gold left border')

content = re.sub(
    r'\.dark \.card-early-access\{[^}]+\}',
    '.dark .card-early-access{border-left:3px solid rgba(212,160,58,.5)!important;background:rgba(212,160,58,.06)!important}',
    content
)
log('Updated dark mode card-early-access CSS')

# Remove the shimmer ::after pseudo-element for early access
content = re.sub(
    r'\.card-early-access::after\{[^}]+\}',
    '',
    content
)
log('Removed card-early-access::after shimmer effect')

# ═══════════════════════════════════════════════════════════
# STEP 5: REMOVE GAMIFICATION JS FUNCTIONS
# ═══════════════════════════════════════════════════════════

# Remove the entire "Habit-Forming Features Engine" section
# From "// ═══════════════════════════════════════════════════════════" to "renderHabitWidgets();"
# We'll use a more targeted approach - remove specific functions

# Remove getStreakData, saveStreakData, checkStreak, useStreakFreeze, renderStreakWidget
content = re.sub(
    r"function getStreakData\(\)[^}]*\{[^}]*\}",
    '', content, flags=re.DOTALL
)
content = re.sub(
    r"function saveStreakData\(d\)[^}]*\{[^}]*\}",
    '', content
)
content = re.sub(
    r"function checkStreak\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function useStreakFreeze\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderStreakWidget\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed streak functions')

# Remove hunter score functions
content = re.sub(
    r"function getHunterData\(\)[^}]*\{[^}]*\}",
    '', content
)
content = re.sub(
    r"function calcHunterScore\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function getNextLevel\(score\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderHunterScore\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed hunter score functions')

# Remove bounty functions
content = re.sub(
    r"function getBounties\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function bumpBounty\(type\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderBounties\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed bounty functions')

# Remove ACHIEVEMENTS constant and related functions
content = re.sub(
    r"const ACHIEVEMENTS = \[.+?\];",
    '', content, flags=re.DOTALL
)
content = re.sub(
    r"function getAchievements\(\)[^}]*\{[^}]*\}",
    '', content
)
content = re.sub(
    r"function checkAchievements\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderAchievements\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed achievements functions')

# Remove intel feed functions
content = re.sub(
    r"function generateIntel\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderIntelFeed\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed intel feed functions')

# Remove market pulse functions
content = re.sub(
    r"function getMarketPulse\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderMarketPulse\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed market pulse functions')

# Remove loyalty functions
content = re.sub(
    r"function getLoyaltyData\(\)[^}]*\{[^}]*\}",
    '', content
)
content = re.sub(
    r"function addLoyaltyPoints\(pts\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function purchaseLoyaltyItem\(item\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderLoyalty\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed loyalty functions')

# Remove leaderboard functions
content = re.sub(
    r"function getLeaderboard\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderLeaderboard\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed leaderboard functions')

# Remove skill radar function
content = re.sub(
    r"function renderSkillRadar\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed skill radar function')

# Remove renderHabitWidgets function
content = re.sub(
    r"function renderHabitWidgets\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed renderHabitWidgets function')

# Remove renderProfileViews function
content = re.sub(
    r"function renderProfileViews\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed renderProfileViews function')

# Remove renderProImpact function
content = re.sub(
    r"function renderProImpact\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed renderProImpact function from home page')

# ═══════════════════════════════════════════════════════════
# STEP 6: REMOVE bumpBounty/addLoyaltyPoints CALLS FROM CORE FUNCTIONS
# ═══════════════════════════════════════════════════════════

# Remove from sendAICover
content = content.replace("  bumpBounty('apply');\n  bumpBounty('ai_letter');\n  addLoyaltyPoints(isPro() ? 30 : 15);", '')
log('Removed bumpBounty/addLoyaltyPoints from sendAICover')

# Remove from toggleSave
content = content.replace("    bumpBounty('save');\n    addLoyaltyPoints(isPro() ? 2 : 1);", '')
log('Removed bumpBounty/addLoyaltyPoints from toggleSave')

# Remove from applyToJob
content = content.replace("  bumpBounty('apply');\n  addLoyaltyPoints(isPro() ? 20 : 10);", '')
log('Removed bumpBounty/addLoyaltyPoints from applyToJob')

# Remove from openJobDetail
content = content.replace("  bumpBounty('view'); // Track viewing for bounties", '')
log('Removed bumpBounty from openJobDetail')

# Remove checkStreak() call from init
content = content.replace("  checkStreak();\n", '')
log('Removed checkStreak call from init')

# Remove renderHabitWidgets() call from init
content = content.replace("  renderHabitWidgets();\n", '', 1)
log('Removed renderHabitWidgets call from init')

# Remove renderProfileViews() call from init
content = content.replace("  renderProfileViews();\n", '', 1)
log('Removed renderProfileViews call from init')

# Remove renderProImpact() calls from various places
content = content.replace("  renderProImpact();\n", '', 1)  # from init
log('Removed renderProImpact call from init')

# Remove from startTrial
content = content.replace("  renderProImpact();\n", '', 1)
log('Removed renderProImpact call from startTrial')

# Remove from subscribePro
content = content.replace("  renderProImpact();\n", '', 1)
log('Removed renderProImpact call from subscribePro')

# Remove from skipTrialEnd
content = content.replace("  renderProImpact();\n", '', 1)
log('Removed renderProImpact call from skipTrialEnd')

# Remove from sendAICover
content = content.replace("  renderProImpact();\n", '', 1)
log('Removed renderProImpact call from sendAICover')

# Remove from applyToJob
content = content.replace("  renderProImpact();\n", '', 1)
log('Removed renderProImpact call from applyToJob')

# Remove addLoyaltyPoints(5) from checkStreak area (if still there)
content = re.sub(r"\s*addLoyaltyPoints\(5\);.*?// daily login points", '', content)
log('Removed addLoyaltyPoints(5) daily login points')

# Remove the habit-forming engine section header comments
content = content.replace("// ═══════════════════════════════════════════════════════════\n// ── Habit-Forming Features Engine ──\n// ═══════════════════════════════════════════════════════════", "")
log('Removed Habit-Forming Features Engine section header')

# Remove sub-section headers for deleted features
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
]:
    content = content.replace(header, '')

# ═══════════════════════════════════════════════════════════
# STEP 7: REMOVE GHOST COUNTER FROM JOB CARDS
# ═══════════════════════════════════════════════════════════

# Remove the ghost counter HTML from renderJobCard
content = re.sub(
    r"  const ghostHtml = pro\s*\? `[^`]+`\s*: `[^`]+`;",
    '', content
)
log('Removed ghost counter variable from renderJobCard')

# Remove ${ghostHtml} from the card template
content = content.replace("      ${ghostHtml}", '')
log('Removed ghost counter from card template')

# Remove the seed/viewing/applicants/trendUp variables used by ghost counter
content = re.sub(
    r"  const seed = job\.id \* 2654435761 >>> 0;\n  const viewing = 8 \+ \(seed % 40\);\n  const applicants = \(seed >> 8\) % 13;\n  const trendUp = \(seed >> 16\) % 4 \+ 1;",
    '', content
)
log('Removed ghost counter seed/viewing/applicants variables')

# ═══════════════════════════════════════════════════════════
# STEP 8: REPLACE ALL EMOJI
# ═══════════════════════════════════════════════════════════

# Define SVG icons for replacement
SVG_TARGET = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
SVG_BOLT = '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'

# Toast messages - remove emoji
content = content.replace("showToast('🎉 Pro-триал активирован на 3 дня!');", "showToast('Pro-триал активирован на 3 дня');")
content = content.replace("showToast('✨ Pro подписка активирована!');", "showToast('Pro подписка активирована');")
content = content.replace("showToast('✨ AI-отклик отправлен! Клиент получит уведомление.');", "showToast('AI-отклик отправлен. Клиент получит уведомление.');")
content = content.replace("showToast('Заказ сохранён ❤️');", "showToast('Заказ сохранён');")
content = content.replace("showToast('❄️ Заморозка стрика активирована');", "showToast('Заморозка стрика активирована');")  # probably already removed
content = content.replace("showToast('✅ Задание выполнено! +' + pts + ' очков');", "showToast('Задание выполнено! +' + pts + ' очков');")  # probably already removed
content = content.replace("showToast('✅ ' + (names[item]||item) + ' активирован!');", "showToast((names[item]||item) + ' активирован');")  # probably already removed

log('Updated toast messages - removed emoji')

# Remove emoji from various places in the file
emoji_replacements = {
    '🔥': '',
    '🎯': '',
    '👁️': '',
    '⚡': '',
    '🏅': '',
    '💎': '',
    '🏆': '',
    '📊': '',
    '🕵️': '',
    '🎨': '',
    '📋': '',
    '❄️': '',
    '🎁': '',
    '🎉': '',
    '✨': '',
    '❤️': '',
    '👋': '',
    '🚀': '',
    '💰': '',
    '👇': '',
    '⚠️': '',
    '🤖': '',
    '💾': '',
    '👀': '',
    '📈': '',
    '🤝': '',
    '👑': '',
    '🔒': '',
}

for emoji, replacement in emoji_replacements.items():
    if emoji in content:
        content = content.replace(emoji, replacement)
        log(f'Replaced emoji: {emoji}')

# ═══════════════════════════════════════════════════════════
# STEP 9: UPDATE PRO FEATURE LISTS (TRIAL WELCOME, TARIFF, ETC.)
# ═══════════════════════════════════════════════════════════

# Update trial welcome overlay - remove "Инсайты клиентов" and "Кто смотрел профиль" and "Разведка и стрики"
# Replace the last 3 features in the trial welcome

# Remove "Инсайты клиентов" feature
content = re.sub(
    r'''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-insight"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg></div>
          <div><div class="trial-welcome-feat-title">Инсайты клиентов</div><div class="trial-welcome-feat-desc">Узнайте, кто платит и как быстро</div></div>
        </div>''',
    '', content
)
log('Removed "Инсайты клиентов" from trial welcome')

# Remove "Кто смотрел профиль" feature
content = re.sub(
    r'''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-views"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg></div>
          <div><div class="trial-welcome-feat-title">Кто смотрел профиль</div><div class="trial-welcome-feat-desc">Не упускайте возможности — узнайте, кто вас ищет</div></div>
        </div>''',
    '', content
)
log('Removed "Кто смотрел профиль" from trial welcome')

# Remove "Разведка и стрики" feature (gamification)
content = re.sub(
    r'''        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico" style="background:linear-gradient\(135deg,var\(--warning\),#E8B84A\)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg></div>
          <div><div class="trial-welcome-feat-title">Разведка и стрики</div><div class="trial-welcome-feat-desc">Аналитика рынка, серия охоты, x2 награды и рейтинг</div></div>
        </div>''',
    '', content
)
log('Removed "Разведка и стрики" from trial welcome')

# Add "AI-сопроводительное письмо" feature to trial welcome
# Insert after "Безлимитные отклики и сохранения"
new_ai_letter_feat = '''
        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico ico-ai"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
          <div><div class="trial-welcome-feat-title">AI-сопроводительное письмо</div><div class="trial-welcome-feat-desc">Персонализированный отклик за 5 секунд</div></div>
        </div>'''

content = content.replace(
    '''          <div><div class="trial-welcome-feat-title">Безлимитные отклики и сохранения</div><div class="trial-welcome-feat-desc">На Free всего 3 отклика и 3 сохранения в месяц</div></div>
        </div>''',
    '''          <div><div class="trial-welcome-feat-title">Безлимитные отклики и сохранения</div><div class="trial-welcome-feat-desc">На Free всего 3 отклика и 3 сохранения в месяц</div></div>
        </div>''' + new_ai_letter_feat
)
log('Added "AI-сопроводительное письмо" to trial welcome')

# Add "Все заказы" feature
new_all_jobs_feat = '''
        <div class="trial-welcome-feat">
          <div class="trial-welcome-feat-ico" style="background:linear-gradient(135deg,var(--sky),var(--primary))"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg></div>
          <div><div class="trial-welcome-feat-title">Все заказы</div><div class="trial-welcome-feat-desc">На Free видно только 6 из 15 заказов</div></div>
        </div>'''

content = content.replace(
    new_ai_letter_feat,
    new_ai_letter_feat + new_all_jobs_feat
)
log('Added "Все заказы" to trial welcome')

# Update trial bar sub-text for Free users - remove "Инсайты"
content = content.replace(
    "AI-анализ · Стратегия · Ранний доступ · Инсайты",
    "AI-анализ · Стратегия · Ранний доступ"
)
log('Updated trial bar sub-text for Free users')

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
# STEP 10: UPDATE TARIFF COMPARISON TABLE
# ═══════════════════════════════════════════════════════════

# The tariff table is built dynamically in openMoreSub('tariff'). 
# We need to remove "Инсайты клиентов" and "Кто смотрел профиль" rows from it.
# These are in a long string concatenation. Let's find and remove them.

# Remove "Инсайты клиентов" row from tariff table
content = re.sub(
    r"<tr style=\"border-top:1px solid var\(--border-soft\)\"><td style=\"padding:8px 10px;font-weight:500;color:var\(--text\)\">Инсайты клиентов</td><td style=\"padding:8px 10px;text-align:center;color:var\(--text-3\)\">--</td><td style=\"padding:8px 10px;text-align:center;color:var\(--primary\);font-weight:600;[^"]*\">" \+ checkSvg \+ "</td></tr>",
    '', content
)
log('Removed "Инсайты клиентов" row from tariff comparison table')

# Remove "Кто смотрел профиль" row from tariff table
content = re.sub(
    r"<tr style=\"border-top:1px solid var\(--border-soft\)\"><td style=\"padding:8px 10px;font-weight:500;color:var\(--text\)\">Кто смотрел профиль</td><td style=\"padding:8px 10px;text-align:center;color:var\(--text-3\)\">Только счётчик</td><td style=\"padding:8px 10px;text-align:center;color:var\(--primary\);font-weight:600;[^"]*\">Полный список</td></tr>",
    '', content
)
log('Removed "Кто смотрел профиль" row from tariff comparison table')

# Remove "Инсайты клиентов" from tariff card feature list
content = re.sub(
    r"<div style=\"display:flex;align-items:center;gap:6px;font-size:12px;color:var\(--text-2\)\"><svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"[^\"]*\" stroke-width=\"2\"><polyline points=\"20 6 9 17 4 12\"/></svg>Инсайты клиентов</div>",
    '', content
)
log('Removed "Инсайты клиентов" from tariff card feature list')

# Remove "Кто смотрел профиль" from tariff card feature list
content = re.sub(
    r"<div style=\"display:flex;align-items:center;gap:6px;font-size:12px;color:var\(--text-2\)\"><svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"[^\"]*\" stroke-width=\"2\"><polyline points=\"20 6 9 17 4 12\"/></svg>Кто смотрел профиль</div>",
    '', content
)
log('Removed "Кто смотрел профиль" from tariff card feature list')

# Add "AI-сопроводительное письмо" to tariff card features (after AI-стратегия)
content = content.replace(
    "Ранний доступ к заказам</div>",
    "Ранний доступ к заказам</div><div style=\"display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-2)\"><svg width=\"14\" height=\"14\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"" + ('var(--success)' if 'var(--success)' in content[:content.find('Ранний доступ к заказам</div>')+500] else 'var(--text-3)') + "\" stroke-width=\"2\"><polyline points=\"20 6 9 17 4 12\"/></svg>AI-сопроводительное письмо</div>"
)
log('Added "AI-сопроводительное письмо" to tariff card features')

# Add "AI-письма" row to comparison table (after "AI-стратегия проекта" row)
# This is complex since the table is dynamically built. Let's add it after the AI-стратегия row.
ai_letter_table_row = '''<tr style="border-top:1px solid var(--border-soft)"><td style="padding:8px 10px;font-weight:500;color:var(--text)">AI-сопроводительное письмо</td><td style="padding:8px 10px;text-align:center;color:var(--text-3)">--</td><td style="padding:8px 10px;text-align:center;color:var(--primary);font-weight:600;' + proBg + '">' + checkSvg + '</td></tr>'''

content = content.replace(
    "Ранний доступ</td><td style=\"padding:8px 10px;text-align:center;color:var(--text-3)\">--</td><td style=\"padding:8px 10px;text-align:center;color:var(--primary);font-weight:600;' + proBg + '\">' + checkSvg + '</td></tr>",
    "Ранний доступ</td><td style=\"padding:8px 10px;text-align:center;color:var(--text-3)\">--</td><td style=\"padding:8px 10px;text-align:center;color:var(--primary);font-weight:600;' + proBg + '\">' + checkSvg + '</td></tr>" + ai_letter_table_row
)
log('Added "AI-сопроводительное письмо" row to comparison table')

# ═══════════════════════════════════════════════════════════
# STEP 11: UPDATE LIMIT MESSAGES - CALM, PROFESSIONAL
# ═══════════════════════════════════════════════════════════

# Update the trial bar when limit is hit - calm message
content = content.replace(
    "Разблокируйте безлимит с Pro",
    "Pro даёт безлимитные отклики"
)
log('Updated limit hit message in trial bar')

# Update the Free trial bar sub-text
content = content.replace(
    "Активируйте Pro со скидкой 50%!",
    "Pro даёт безлимитные отклики и AI"
)
log('Updated trial ending sub-text')

# Update the "Лимит откликов" trial bar - more calm
content = content.replace(
    "Лимит откликов",
    "Отклики использованы"
)
log('Updated "Лимит откликов" to "Отклики использованы"')

# ═══════════════════════════════════════════════════════════
# STEP 12: REMOVE Client Insights (too speculative)
# ═══════════════════════════════════════════════════════════

# Remove renderClientInsights and renderClientInsightsLocked functions
content = re.sub(
    r"function renderClientInsights\(job\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
content = re.sub(
    r"function renderClientInsightsLocked\(\)\{.+?^\}",
    '', content, flags=re.DOTALL|re.MULTILINE
)
log('Removed client insights functions')

# Remove client insights from job detail - find where it's called
content = re.sub(
    r"\$\{isPro\(\) \? renderClientInsights\(job\) : renderClientInsightsLocked\(\)\}",
    '', content
)
log('Removed client insights from job detail')

# ═══════════════════════════════════════════════════════════
# STEP 13: CLEAN UP EMPTY LINES / DOUBLE BLANKS
# ═══════════════════════════════════════════════════════════

# Replace 3+ consecutive blank lines with 2
content = re.sub(r'\n{4,}', '\n\n\n', content)
log('Cleaned up excessive blank lines')

# ═══════════════════════════════════════════════════════════
# STEP 14: UPDATE "Pro Impact" - move to tariff sub
# ═══════════════════════════════════════════════════════════

# We removed the Pro Impact card from the home page. The function renderProImpact is gone.
# When tariff page opens, we should still show the impact there.
# For now, we'll add a simple impact card to the tariff sub-page.
# The openMoreSub('tariff') already has the comparison table, so Pro Impact info is somewhat redundant.
# We'll keep it simple.

# ═══════════════════════════════════════════════════════════
# STEP 15: UPDATE REMAINING EMOJI-ADJACENT TEXT
# ═══════════════════════════════════════════════════════════

# Any remaining emoji patterns we might have missed
remaining_emoji = re.findall(r'[\U0001F300-\U0001F9FF\U00002702-\U000027B0\U0000FE00-\U0000FE0F\U0001F000-\U0001F02F\U0001F0A0-\U0001F0FF\U0001F100-\U0001F64F\U0001F680-\U0001F6FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002600-\U000026FF\U00002700-\U000027BF]', content)
if remaining_emoji:
    for em in set(remaining_emoji):
        content = content.replace(em, '')
    log(f'Removed {len(set(remaining_emoji))} remaining emoji types')

# ═══════════════════════════════════════════════════════════
# STEP 16: ENSURE NO BROKEN REFERENCES
# ═══════════════════════════════════════════════════════════

# Check for references to removed functions that might cause JS errors
broken_refs = [
    'renderHabitWidgets',
    'renderProfileViews',
    'renderProImpact',
    'checkStreak',
    'renderStreakWidget',
    'renderHunterScore',
    'renderBounties',
    'renderAchievements',
    'renderLoyalty',
    'renderIntelFeed',
    'renderMarketPulse',
    'renderLeaderboard',
    'renderSkillRadar',
    'bumpBounty',
    'addLoyaltyPoints',
    'getStreakData',
    'getHunterData',
    'getBounties',
    'getAchievements',
    'checkAchievements',
    'getLoyaltyData',
    'purchaseLoyaltyItem',
    'getLeaderboard',
    'generateIntel',
    'getMarketPulse',
    'calcHunterScore',
    'getNextLevel',
    'saveStreakData',
    'useStreakFreeze',
    'renderClientInsights',
    'renderClientInsightsLocked',
]

for ref in broken_refs:
    # Check if the function name appears as a call (not as a definition)
    # Look for patterns like `ref(` or `ref ()`
    call_pattern = rf'(?<!function ){ref}\s*\('
    matches = re.findall(call_pattern, content)
    if matches:
        print(f"  [WARN] Found {len(matches)} remaining call(s) to {ref}")

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
