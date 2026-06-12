#!/usr/bin/env python3
"""
SkillHunt Redesign Script — Phase 1: Remove gamification + update design system
Edits /home/z/my-project/upload/index (16) (2).html in-place
"""
import re

FILE = '/home/z/my-project/upload/index (16) (2).html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Original file: {original_len} chars, {content.count(chr(10))} lines")

# ════════════════════════════════════════════════════════════════
# PHASE 1: REMOVE GAMIFICATION CSS
# ════════════════════════════════════════════════════════════════

# 1a. Remove Streak CSS block
content = re.sub(
    r'/\* Streak \*/\n\.streak\{.*?\.streak-day\.future\{background:var\(--bg-input\);color:var\(--text-3\)\}\n',
    '', content, flags=re.DOTALL
)

# 1b. Remove Loyalty CSS block
content = re.sub(
    r'/\* Loyalty points \*/\n\.loyalty-card\{.*?\.loyalty-next\{font-size:11px;opacity:\.7;margin-top:8px\}\n',
    '', content, flags=re.DOTALL
)

# 1c. Remove Achievement CSS
content = re.sub(
    r'\.achievement-grid\{.*?\.achievement\.locked \.achievement-name\{color:var\(--text-3\)\}\n',
    '', content, flags=re.DOTALL
)

# 1d. Remove home-streak CSS
content = re.sub(
    r'\.home-streak\{.*?\.dark \.home-streak-num\{color:var\(--warning\)\}\n',
    '', content, flags=re.DOTALL
)

# 1e. Remove Repa Score & Leaderboard CSS
content = re.sub(
    r'/\* ── Repa Score & Leaderboard ──/\n\.repa-score-card\{.*?\.lb-share-btn:hover\{border-color:var\(--primary\);color:var\(--primary\);background:var\(--primary-soft\)\}\n',
    '', content, flags=re.DOTALL
)

# 1f. Remove Repa Score Detail CSS
content = re.sub(
    r'/\* Repa Score Detail \*/\n\.rs-hero\{.*?\.rs-rank-link a\{font-size:12px;font-weight:600;color:var\(--primary\);cursor:pointer\}\n',
    '', content, flags=re.DOTALL
)

# 1g. Remove ref-leaderboard CSS
content = re.sub(
    r'\.ref-leaderboard\{margin-top:14px\}\n\.ref-lb-item\{.*?\.ref-lb-rank\.gold\{background:#FFD700;color:#1A1A2E\}\n',
    '', content, flags=re.DOTALL
)

# 1h. Remove ghost-counter CSS
content = re.sub(
    r'/\* Ghost Counter \*/\n\.ghost-counter\{.*?\.ghost-trend\{font-size:9px;color:var\(--success\);font-weight:600\}\n',
    '', content, flags=re.DOTALL
)

# 1i. Remove bounty CSS
content = re.sub(
    r'\.bounty-item\{.*?\.bounty-reward\{font-size:10px;font-weight:700;color:var\(--warning\);flex-shrink:0;white-space:nowrap\}\n',
    '', content, flags=re.DOTALL
)

# 1j. Remove hunter-score CSS
content = re.sub(
    r'\.hunter-score-val\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1k. Remove streak-row, streak-dots in More panel CSS
content = re.sub(
    r'/\* Streak \*/\n\.streak-row\{.*?\.streak-freeze:hover\{text-decoration:underline\}\n',
    '', content, flags=re.DOTALL
)

# 1l. Remove confetti animation (gamification)
content = re.sub(
    r'@keyframes confetti\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1m. Remove bounceIn animation (too playful)
content = re.sub(
    r'@keyframes bounceIn\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1n. Remove float animation (too playful)
content = re.sub(
    r'@keyframes float\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1o. Remove glow animation (too flashy)
content = re.sub(
    r'@keyframes glow\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1p. Remove shake animation
content = re.sub(
    r'@keyframes shake\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1q. Remove bnavBadgePulse (too game-like)
content = re.sub(
    r'@keyframes bnavBadgePulse\{.*?\}\n',
    '', content, flags=re.DOTALL
)

# 1r. Remove sparkline CSS (too game-like)
content = re.sub(
    r'/\* Sparkline mini bar chart \*/\n\.sparkline\{.*?\.sparkline-bar\.low\{background:var\(--danger\);opacity:1\}\n',
    '', content, flags=re.DOTALL
)

# 1s. Remove seller-badge CSS  
content = re.sub(
    r'/\* Seller rating badge \*/\n\.seller-badge\{.*?\.seller-badge svg\{width:10px;height:10px\}\n',
    '', content, flags=re.DOTALL
)

# 1t. Remove Module 5: Monetization & Loyalty CSS comment and related
content = re.sub(
    r'/\* ═══ Module 5: Monetization & Loyalty ═══ \*/\n',
    '', content
)

# 1u. Remove achievement CSS in more panel
content = re.sub(
    r'/\* 6\. Achievement Badges \*/\n',
    '', content
)

# ════════════════════════════════════════════════════════════════
# PHASE 2: UPDATE DESIGN SYSTEM — Cold blue-violet professional palette
# ════════════════════════════════════════════════════════════════

# Update CSS variables for a colder, more professional look
content = content.replace(
    """  --primary: #6C7BD4;
  --primary-hover: #5B6AC3;
  --primary-light: #EEF0FA;
  --primary-soft: rgba(108,123,212,.06);
  --primary-glow: rgba(108,123,212,.15);
  --bg: #F5F6FA;
  --bg-card: #FFFFFF;
  --bg-card-milky: #FCFCFE;
  --bg-input: #ECEEF4;
  --bg-glass: rgba(255,255,255,.75);
  --text: #171B2D;
  --text-2: #5E6882;
  --text-3: #939DAD;
  --border: #E2E6EE;
  --border-soft: #ECF0F6;
  --success: #4CAF7D;
  --success-light: #EDFAF2;
  --danger: #D9534F;
  --danger-light: #FDF0EF;
  --warning: #D4A03A;
  --warning-light: #FBF5E6;
  --lavender: #8E7FD4;
  --lavender-light: #F2F0FA;
  --mint: #5BBF8F;
  --mint-light: #ECFAF3;
  --coral: #E07C6C;
  --coral-light: #FDF0ED;
  --sky: #5A9FD4;
  --sky-light: #ECF4FB;""",
    """  --primary: #5B6ABF;
  --primary-hover: #4D5BAE;
  --primary-light: #ECEEF8;
  --primary-soft: rgba(91,106,191,.05);
  --primary-glow: rgba(91,106,191,.12);
  --bg: #F4F5F9;
  --bg-card: #FFFFFF;
  --bg-card-milky: #FBFBFD;
  --bg-input: #EAECF2;
  --bg-glass: rgba(255,255,255,.78);
  --text: #1A1D2E;
  --text-2: #5C6478;
  --text-3: #8E96A8;
  --border: #DFE3EB;
  --border-soft: #E8ECF3;
  --success: #3D9E6E;
  --success-light: #EBF7F1;
  --danger: #C94844;
  --danger-light: #FBECEB;
  --warning: #C4922E;
  --warning-light: #F9F2E2;
  --lavender: #7E6FC4;
  --lavender-light: #F0EDF8;
  --mint: #4BAF82;
  --mint-light: #EAF8F1;
  --coral: #D06E5E;
  --coral-light: #FBEEE9;
  --sky: #4E94C4;
  --sky-light: #E9F1F8;"""
)

# Update dark theme variables
content = content.replace(
    """  --primary: #8A9BE8;
  --primary-hover: #9DADF0;
  --primary-light: #1A1E38;
  --primary-soft: rgba(138,155,232,.07);
  --primary-glow: rgba(138,155,232,.18);
  --bg: #0B0D14;
  --bg-card: #13161F;
  --bg-card-milky: #151820;
  --bg-input: #1C1F2C;
  --bg-glass: rgba(19,22,31,.8);
  --text: #E4E6EE;
  --text-2: #8891A8;
  --text-3: #4E576A;
  --border: #232838;
  --border-soft: #1C1F2C;
  --success: #4CAF7D;
  --success-light: #0F1F17;
  --danger: #D9534F;
  --danger-light: #1F1212;
  --warning: #D4A03A;
  --warning-light: #1F1A0E;
  --lavender: #9E8FD4;
  --lavender-light: #1A1628;
  --mint: #5BBF8F;
  --mint-light: #0F1F17;
  --coral: #D97A6C;
  --coral-light: #1F1512;
  --sky: #6BAAD4;
  --sky-light: #121C28;""",
    """  --primary: #7B8CD8;
  --primary-hover: #8E9FDF;
  --primary-light: #181C34;
  --primary-soft: rgba(123,140,216,.06);
  --primary-glow: rgba(123,140,216,.15);
  --bg: #0A0C13;
  --bg-card: #12151E;
  --bg-card-milky: #14171F;
  --bg-input: #1A1E2A;
  --bg-glass: rgba(18,21,30,.82);
  --text: #E2E4EC;
  --text-2: #848DA2;
  --text-3: #4A5266;
  --border: #222636;
  --border-soft: #1A1E2A;
  --success: #3D9E6E;
  --success-light: #0D1D15;
  --danger: #C94844;
  --danger-light: #1D1010;
  --warning: #C4922E;
  --warning-light: #1D180D;
  --lavender: #8E7FC4;
  --lavender-light: #181426;
  --mint: #4BAF82;
  --mint-light: #0D1D15;
  --coral: #D06E5E;
  --coral-light: #1D1310;
  --sky: #5A9AC4;
  --sky-light: #101A26;"""
)

# ════════════════════════════════════════════════════════════════
# PHASE 3: REMOVE GAMIFICATION FROM HTML
# ════════════════════════════════════════════════════════════════

# 3a. Remove home-streak HTML block from feed (between trialBarContainer and guided steps)
content = re.sub(
    r'\n\s*<!-- Streak Widget -->.*?<!-- End Streak Widget -->\n',
    '\n', content, flags=re.DOTALL
)

# 3b. Remove any streak HTML between trialBarContainer and guided steps
content = re.sub(
    r'(<div id="trialBarContainer"></div>)\s*\n\s*\n\s*\n\s*(<!-- Guided Steps)',
    r'\1\n\n          \2', content, flags=re.DOTALL
)

# ════════════════════════════════════════════════════════════════
# PHASE 4: REMOVE GAMIFICATION FROM JS
# ════════════════════════════════════════════════════════════════

# 4a. Remove ghost counter from job card rendering
content = content.replace(
    """  // Ghost counter (FOMO) — deterministic random from job.id
  const seed = job.id * 2654435761 >>> 0;
  const viewing = 8 + (seed % 40);
  const applicants = (seed >> 8) % 13;
  const trendUp = (seed >> 16) % 4 + 1;
  const ghostHtml = pro
    ? `<div class="ghost-counter"><span>${viewing}</span><span>${applicants} отклика</span><span class="ghost-trend">↑ +${trendUp} за час</span></div>`
    : `<div class="ghost-counter"><span>${Math.floor(viewing/10)*10}+</span><span>несколько</span></div>`;""",
    """  // Ghost counter removed — professional redesign"""
)

# 4b. Remove ghost counter usage in card HTML
content = content.replace('${ghostHtml}', '')

# 4c. Remove gamification comment
content = content.replace('// ── Gamification features removed per product strategy ──', '// ── Gamification features removed ──')

# 4d. Remove streak-related JS in More panel sub-screens
# The streak rendering was likely in openMoreSub function — let's clean it

# ════════════════════════════════════════════════════════════════
# PHASE 5: UPDATE TITLE & META
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '<title>SkillHunt — AI-фриланс в одном клике</title>',
    '<title>SkillHunt — AI-платформа для фрилансеров</title>'
)

# ════════════════════════════════════════════════════════════════
# PHASE 6: REDESIGN HOME SCREEN — Calm, professional
# ════════════════════════════════════════════════════════════════

# 6a. Simplify hero greeting — remove "Pro" badge from name, make it calmer
content = content.replace(
    """          <!-- Hero Greeting — Simplified -->
          <div class="hero-greeting animate-in" id="feedGreeting">
            <div class="hero-greeting-row">
              <div class="hero-greeting-avatar" id="userAvatar">А</div>
              <div class="hero-greeting-body">
                <div class="hero-greeting-time" id="greetingTime">Добрый день,</div>
                <div class="hero-greeting-name" id="userName">Александр <span class="home-greeting-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>Pro</span></div>
              </div>
              <div class="hero-online"><span class="hero-online-dot"></span>Онлайн</div>
            </div>
          </div>""",
    """          <!-- Hero Greeting — Calm & Professional -->
          <div class="hero-greeting animate-in" id="feedGreeting">
            <div class="hero-greeting-row">
              <div class="hero-greeting-avatar" id="userAvatar">А</div>
              <div class="hero-greeting-body">
                <div class="hero-greeting-time" id="greetingTime">Добрый день,</div>
                <div class="hero-greeting-name" id="userName">Александр</div>
              </div>
            </div>
          </div>"""
)

# 6b. Replace AI Hero Card — calmer, professional tone
content = content.replace(
    """          <!-- AI Hero Card — One Clear Action -->
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
          </div>""",
    """          <!-- AI Insight Card — Professional, calm -->
          <div class="hero-ai-card animate-in dot-pattern">
            <div class="hero-ai-match">
              <div class="hero-ai-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="14" y1="11" x2="8" y2="11"/></svg>
              </div>
              <div class="hero-ai-text">
                <div class="hero-ai-headline">Найдены заказы по вашему профилю</div>
                <div class="hero-ai-reason">
                  <span class="hero-ai-reason-tag">GPT API</span>
                  <span class="hero-ai-reason-tag">React</span>
                  <span class="hero-ai-reason-tag">Python</span>
                </div>
              </div>
            </div>
            <button class="hero-cta" onclick="filterFeedCategory('all')">
              Посмотреть заказы
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg>
            </button>
          </div>"""
)

# 6c. Remove guided steps (too onboarding-game-like)
content = content.replace(
    """          <!-- Guided Steps — 1-2-3 Onboarding -->
          <div class="guided-steps animate-in">
            <div class="guided-step" onclick="guidedStep1()" style="cursor:pointer">
              <span class="guided-step-num">1</span>
              Откройте
            </div>
            <span class="guided-arrow">&#8594;</span>
            <div class="guided-step" onclick="guidedStep2()" style="cursor:pointer">
              <span class="guided-step-num">2</span>
              Отфильтруйте
            </div>
            <span class="guided-arrow">&#8594;</span>
            <div class="guided-step" onclick="guidedStep3()" style="cursor:pointer">
              <span class="guided-step-num">3</span>
              Откликнитесь
            </div>
          </div>""",
    ''  # Remove entirely
)

# 6d. Remove hero-secondary shimmer (too flashy)
content = re.sub(r'\.hero-cta-shimmer\{.*?\}\n', '', content, flags=re.DOTALL)

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"New file: {new_len} chars, {content.count(chr(10))} lines")
print(f"Removed: {original_len - new_len} chars ({((original_len - new_len) / original_len * 100):.1f}%)")
print("Phase 1 complete!")
