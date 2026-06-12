#!/usr/bin/env python3
"""
SkillHunt Redesign Script — Phase 3: Profile redesign, subscription cleanup, professional tone
"""
import re

FILE = '/home/z/my-project/upload/index (16) (2).html'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

original_len = len(content)
print(f"Starting: {original_len} chars, {content.count(chr(10))} lines")

# ════════════════════════════════════════════════════════════════
# STEP 1: Redesign More Panel Profile section
# ════════════════════════════════════════════════════════════════

# Replace profile bar with profile completeness indicator
content = content.replace(
    '''    <!-- Profile -->
    <div class="more-profile-bar">
      <div class="more-profile-av" id="moreAvatar">А</div>
      <div class="more-profile-info">
        <div class="more-profile-name" id="moreName">Александр</div>
        <div class="more-profile-plan">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/></svg>
          AI Freelancer
        </div>
      </div>
    </div>''',
    '''    <!-- Profile -->
    <div class="more-profile-bar" style="cursor:pointer" onclick="openMoreSub('edit-profile', event)">
      <div class="more-profile-av" id="moreAvatar">А</div>
      <div class="more-profile-info" style="flex:1;min-width:0">
        <div class="more-profile-name" id="moreName">Александр</div>
        <div style="display:flex;align-items:center;gap:6px;margin-top:4px">
          <div style="flex:1;height:3px;background:var(--bg-input);border-radius:2px;overflow:hidden;max-width:100px">
            <div id="profileCompletenessBar" style="height:100%;background:var(--success);border-radius:2px;width:65%;transition:width .5s"></div>
          </div>
          <span id="profileCompletenessText" style="font-size:10px;color:var(--text-3);font-weight:600">65%</span>
        </div>
      </div>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="var(--text-3)" stroke-width="2" style="flex-shrink:0"><polyline points="9 18 15 12 9 6"/></svg>
    </div>'''
)
print("✓ Redesigned profile bar with completeness indicator")

# ════════════════════════════════════════════════════════════════
# STEP 2: Simplify balance card — calmer tone
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '''    <!-- Balance Card -->
    <div class="more-balance-card">
      <div class="more-balance-top">
        <div class="more-balance-label">Баланс токенов</div>
        <div class="more-balance-link" onclick="openMoreSub('payments', event)">История</div>
      </div>
      <div class="more-balance-value">847</div>
      <div class="more-balance-row" onclick="showToast('Потрачено сегодня: 23 токена')">
        <div class="more-balance-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>
        <div class="more-balance-row-text">Потрачено сегодня: 23</div>
        <div class="more-balance-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
      </div>
      <button class="more-balance-action" onclick="openMoreSub('buy-tokens')">Купить токены</button>
    </div>''',
    '''    <!-- Balance Card — Calm, professional -->
    <div class="more-balance-card">
      <div class="more-balance-top">
        <div class="more-balance-label">Баланс токенов</div>
        <div class="more-balance-link" onclick="openMoreSub('payments', event)">История</div>
      </div>
      <div class="more-balance-value">847</div>
      <button class="more-balance-action" onclick="openMoreSub('buy-tokens')">Пополнить баланс</button>
    </div>'''
)
print("✓ Simplified balance card")

# ════════════════════════════════════════════════════════════════
# STEP 3: Clean up "NEW" badges — professional tone, no hype
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '<span class="tag tag-primary" style="margin-left:auto;margin-right:4px">NEW</span>',
    '<span style="font-size:9px;font-weight:600;padding:2px 6px;border-radius:var(--radius-full);color:var(--lavender);background:var(--lavender-light);margin-left:auto;margin-right:4px">AI</span>'
)
print("✓ Replaced NEW badge with calmer AI badge")

# ════════════════════════════════════════════════════════════════
# STEP 4: Update subscription section — calmer wording
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '''    <div class="more-section-head">Подписка</div>
    <div class="more-menu-row" onclick="openMoreSub('tariff', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
      <div class="more-menu-row-text">Тариф</div>
      <span class="tag tag-primary" style="margin-left:auto;margin-right:4px" id="moreTariffBadge">Pro</span>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>''',
    '''    <div class="more-section-head">Подписка</div>
    <div class="more-menu-row" onclick="openMoreSub('tariff', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg></div>
      <div class="more-menu-row-text">План подписки</div>
      <span style="font-size:11px;font-weight:600;color:var(--primary);margin-left:auto;margin-right:4px" id="moreTariffBadge">Pro</span>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>'''
)
print("✓ Updated subscription section wording")

# ════════════════════════════════════════════════════════════════
# STEP 5: Update AI Strategy wording — professional, no "victory" language
# ════════════════════════════════════════════════════════════════

content = content.replace(
    "genSub.textContent = 'Формируем стратегию победы...';",
    "genSub.textContent = 'Формируем рекомендации...';"
)
content = content.replace(
    "genSub.textContent = 'Анализируем конкурентов и бюджет';",
    "genSub.textContent = 'Анализируем заказ и бюджет';"
)
content = content.replace(
    '<div class="ai-strategy-prob-title">Вероятность победы</div>',
    '<div class="ai-strategy-prob-title">Шанс получения заказа</div>'
)
content = content.replace(
    "'Высокий шанс! Ваш профиль хорошо подходит.'",
    "'Хорошее совпадение. Ваш профиль подходит.'"
)
content = content.replace(
    "'Хорошие шансы. Следуйте стратегии ниже.'",
    "'Среднее совпадение. Следуйте рекомендациям ниже.'"
)
content = content.replace(
    "'Средний шанс. Потребуется сильный отклик.'",
    "'Низкое совпадение. Потребуется тщательная подготовка.'"
)
content = content.replace(
    '<button class="ai-strategy-apply" onclick="applyWithStrategy(${jobId})"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg> Применить стратегию</button>',
    '<button class="ai-strategy-apply" onclick="applyWithStrategy(${jobId})"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg> Подготовить отклик</button>'
)
print("✓ Updated AI Strategy professional wording")

# ════════════════════════════════════════════════════════════════
# STEP 6: Update trial bar wording — professional, not pushy
# ════════════════════════════════════════════════════════════════

content = content.replace(
    "'Активируйте Pro со скидкой 50%!'",
    "'Оформите Pro для полного доступа'"
)
content = content.replace(
    "'AI-анализ · Стратегия · Ранний доступ'",
    "'AI-анализ · Стратегия · Ранний доступ'"
)
content = content.replace(
    "'Разблокируйте безлимит с Pro'",
    "'Полный доступ доступен с Pro'"
)
content = content.replace(
    "'AI-анализ · Стратегия · Ранний доступ · Инсайты'",
    "'AI-анализ · Стратегия · Ранний доступ'"
)
content = content.replace(
    "'Попробуйте Pro <span class=\"trial-days\">3 дня</span>'",
    "'Pro-доступ <span class=\"trial-days\">3 дня</span>'"
)
print("✓ Updated trial bar professional wording")

# ════════════════════════════════════════════════════════════════
# STEP 7: Update Pro Impact Card wording
# ════════════════════════════════════════════════════════════════

content = content.replace(
    "Ваш Pro-результат",
    "Ваша статистика Pro"
)
content = content.replace(
    "Потенциал",
    "Потенц. заработок"
)
content = content.replace(
    "На Free вы бы отправили <b>всего ' + FREE_APP_LIMIT + ' откликов/мес</b> и видели <b>6 из 15 заказов</b>",
    "Без Pro — <b>' + FREE_APP_LIMIT + ' откликов/мес</b> и <b>6 из 15 заказов</b>"
)
content = content.replace(
    "Сохранить Pro со скидкой",
    "Оформить Pro"
)
print("✓ Updated Pro Impact Card wording")

# ════════════════════════════════════════════════════════════════
# STEP 8: Update trial end overlay wording
# ════════════════════════════════════════════════════════════════

content = content.replace(
    "'Триал завершён'",
    "'Пробный период завершён'"
)
content = content.replace(
    "'Ваш 3-дневный Pro-триал закончился'",
    "'Пробный доступ к Pro завершён'"
)
content = content.replace(
    "'Сохранить Pro за $'",
    "'Оформить Pro за $'"
)
print("✓ Updated trial end overlay wording")

# ════════════════════════════════════════════════════════════════
# STEP 9: Add profile completeness JS function
# ════════════════════════════════════════════════════════════════

profile_completeness_js = '''
// ── Profile Completeness ──
function updateProfileCompleteness() {
  const profile = lsGetJSON('skillhunt_profile', null) || getDefaultProfile();
  const skills = lsGetJSON('skillhunt_custom_skills', []);
  const portfolio = lsGetJSON('skillhunt_portfolio', []);
  
  let score = 0;
  let total = 5;
  
  // Has name
  if (profile.name && profile.name.length > 1) score++;
  // Has skills
  if (skills.length >= 3) score++;
  // Has portfolio
  if (portfolio.length >= 1) score++;
  // Has bio/description
  if (profile.bio && profile.bio.length > 10) score++;
  // Has hourly rate
  if (profile.rate && profile.rate > 0) score++;
  
  const percent = Math.round((score / total) * 100);
  
  const bar = document.getElementById('profileCompletenessBar');
  const text = document.getElementById('profileCompletenessText');
  if (bar) bar.style.width = percent + '%';
  if (text) text.textContent = percent + '%';
}

'''

# Insert before init function
content = content.replace(
    '// ── Init ──\nfunction init()',
    profile_completeness_js + '// ── Init ──\nfunction init()'
)

# Also call updateProfileCompleteness in init
content = content.replace(
    '''  loadProfile();
  loadNotifSettings();''',
    '''  loadProfile();
  loadNotifSettings();
  updateProfileCompleteness();'''
)
print("✓ Added profile completeness JS")

# ════════════════════════════════════════════════════════════════
# STEP 10: Remove duplicate "Уведомления" row (appears twice)
# ════════════════════════════════════════════════════════════════

# The notifications row appears in both "Инструменты" and "Настройки" sections
# Remove the one from "Инструменты"
first_notif = content.find('''    <div class="more-menu-row" onclick="openMoreSub('notifications', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></div>
      <div class="more-menu-row-text">Уведомления</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('templates' ''')

if first_notif != -1:
    # Replace the duplicate — keep the one in settings, remove from tools
    content = content.replace(
        '''    <div class="more-menu-row" onclick="openMoreSub('notifications', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 8A6 6 0 0 0 6 8c0 7-3 9-3 9h18s-3-2-3-9"/><path d="M13.73 21a2 2 0 0 1-3.46 0"/></svg></div>
      <div class="more-menu-row-text">Уведомления</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('templates' ''',
        '''    <div class="more-menu-row" onclick="openMoreSub('templates' ''',
        1  # Replace only first occurrence
    )
    print("✓ Removed duplicate notifications row")

# ════════════════════════════════════════════════════════════════
# STEP 11: Update page title
# ════════════════════════════════════════════════════════════════

content = content.replace(
    '<title>SkillHunt — AI-платформа для фрилансеров</title>',
    '<title>SkillHunt — AI-платформа для фрилансеров</title>'
)

# ════════════════════════════════════════════════════════════════
# SAVE
# ════════════════════════════════════════════════════════════════

with open(FILE, 'w', encoding='utf-8') as f:
    f.write(content)

new_len = len(content)
print(f"\nFinal: {new_len} chars, {content.count(chr(10))} lines")
print(f"Delta: {new_len - original_len} chars")
print("Phase 3 complete!")
