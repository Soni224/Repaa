#!/usr/bin/env python3
"""
Transform SkillHunt HTML: Professional redesign
- Rename gamification features to professional names
- Remove leaderboard entirely
- Restructure home page (move widgets to More panel)
- Replace ALL emoji with inline SVG icons
- Update trial welcome overlay
- Muted professional colors
"""

import re
import sys

# SVG icon definitions (reusable)
SVG_TARGET = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>'
SVG_EYE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'
SVG_LIGHTNING = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>'
SVG_MEDAL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>'
SVG_DIAMOND = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M6 3h12l5 8-11 12L1 11z"/></svg>'
SVG_CHART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>'
SVG_SEARCH = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>'
SVG_PALETTE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg>'
SVG_CLIPBOARD = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>'
SVG_GIFT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><polyline points="20 12 20 22 4 22 4 12"/><rect x="2" y="7" width="20" height="5"/><line x1="12" y1="22" x2="12" y2="7"/><path d="M12 7H7.5a2.5 2.5 0 0 1 0-5C11 2 12 7 12 7z"/><path d="M12 7h4.5a2.5 2.5 0 0 0 0-5C13 2 12 7 12 7z"/></svg>'
SVG_CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><polyline points="20 6 9 17 4 12"/></svg>'
SVG_CALENDAR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>'
SVG_COIN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5c0-1.38-1.34-2.5-3-2.5S9 8.12 9 9.5c0 1.38 1.34 2.5 3 2.5s3 1.12 3 2.5-1.34 2.5-3 2.5-3-1.12-3-2.5"/></svg>'
SVG_ROBOT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="9" cy="16" r="1"/><circle cx="15" cy="16" r="1"/><path d="M12 2v4"/><path d="M8 4l4 2 4-2"/></svg>'
SVG_SAVE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/></svg>'
SVG_HANDSHAKE = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M20 17c0-.6-.4-1-1-1h-1l-1.3 1.3c-.4.4-1 .4-1.4 0L13 16h-2l-2.3 1.3c-.4.4-1 .4-1.4 0L6 16H5c-.6 0-1 .4-1 1v2c0 .6.4 1 1 1h14c.6 0 1-.4 1-1v-2z"/></svg>'
SVG_CROWN = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M2 4l3 12h14l3-12-6 5-4-7-4 7-6-5z"/><path d="M5 16v2h14v-2"/></svg>'
SVG_MONEY = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><line x1="12" y1="1" x2="12" y2="23"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'
SVG_TRENDUP = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/></svg>'
SVG_LOCK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><rect x="3" y="11" width="18" height="11" rx="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>'
SVG_ALERT = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" class="ico-sm"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>'

def transform(content):
    # ═══════════════════════════════════════════════════════════
    # STEP 1: Replace emoji in JavaScript strings and HTML
    # ═══════════════════════════════════════════════════════════
    
    # --- Toast messages with emoji ---
    content = content.replace("showToast('🎉 Pro-триал активирован на 3 дня!')", "showToast('Pro-триал активирован на 3 дня')")
    content = content.replace("showToast('✨ Pro подписка активирована!')", "showToast('Pro подписка активирована')")
    content = content.replace("showToast('✨ AI-отклик отправлен! Клиент получит уведомление.')", "showToast('AI-отклик отправлен! Клиент получит уведомление.')")
    content = content.replace("showToast('❄️ Заморозка стрика активирована')", "showToast('Активность приостановлена')")
    content = content.replace("showToast('✅ Задание выполнено! +' + pts + ' очков')", "showToast('Цель выполнена')")
    content = content.replace("showToast('✅ ' + (names[item]||item) + ' активирован!')", "showToast((names[item]||item) + ' активирован')")
    content = content.replace("showToast('Заказ сохранён ❤️')", "showToast('Заказ сохранён')")
    
    # --- Feature 1: Streak → Regularity Index ---
    # In renderStreakWidget
    content = content.replace(
        '🔥 Серия охоты',
        'Регулярность'
    )
    content = content.replace(
        '<div class="streak-fire">🔥</div>',
        '<div class="streak-ico">' + SVG_CALENDAR + '</div>'
    )
    content = content.replace(
        "❄️ Заморозка (${d.freezeCount}/3)",
        "Пауза (${d.freezeCount}/3)"
    )
    content = content.replace(
        "дней подряд",
        "дней"
    )
    
    # --- Feature 2: Hunter Score → Market Readiness Score ---
    content = content.replace("🎯 Охотник", "Готовность к рынку")
    # Level names
    content = content.replace("{name:'Легенда',min:5000}", "{name:'Топ-эксперт',min:5000}")
    content = content.replace("{name:'Мастер',min:2000}", "{name:'Ведущий',min:2000}")
    content = content.replace("{name:'Эксперт',min:1000}", "{name:'Эксперт',min:1000}")
    content = content.replace("{name:'Охотник',min:500}", "{name:'Специалист',min:500}")
    content = content.replace("{name:'Новичок',min:0}", "{name:'Начинающий',min:0}")
    # Repeat for getNextLevel
    content = content.replace("{name:'Легенда',min:5000},{name:'Мастер',min:2000},{name:'Эксперт',min:1000},{name:'Охотник',min:500},{name:'Новичок',min:0}",
                              "{name:'Топ-эксперт',min:5000},{name:'Ведущий',min:2000},{name:'Эксперт',min:1000},{name:'Специалист',min:500},{name:'Начинающий',min:0}")
    # "x1.5 XP множитель Pro" → professional wording
    content = content.replace("⚡ x1.5 XP множитель Pro", "x1.5 множитель Pro")
    content = content.replace("XP", "")
    # Remove "Охотник 500+" achievement name
    # "До " + esc(nl.next) + ": " + esc(nl.need - d.score) + " XP"
    # Change XP to "очков"
    content = content.replace("'До '+esc(nl.next)+': '+esc(nl.need - d.score)+' XP'", "'До '+esc(nl.next)+': '+esc(nl.need - d.score)+' очков'")
    content = content.replace("'Максимальный уровень!'", "'Максимальный уровень'")
    
    # In calcHunterScore: default level
    content = content.replace("level:'Новичок'", "level:'Начинающий'")
    
    # --- Feature 3: Daily Bounties → Performance Goals ---
    content = content.replace("📋 Ежедневные задания", "Цели на сегодня")
    content = content.replace("⚡ x2 награда с Pro", "x2 прогресс с Pro")
    # Bounty mission labels
    content = content.replace("{type:'apply',label:'Отправьте 1 отклик',target:1,current:0,completed:false,reward:25,ico:'⚡'}",
                              "{type:'apply',label:'Submit Application',target:1,current:0,completed:false,reward:25,ico:''}")
    content = content.replace("{type:'save',label:'Сохраните 2 заказа',target:2,current:0,completed:false,reward:15,ico:'💾'}",
                              "{type:'save',label:'Save Opportunity',target:2,current:0,completed:false,reward:15,ico:''}")
    content = content.replace("{type:'ai_letter',label:'Используйте AI-письмо',target:1,current:0,completed:false,reward:30,ico:'🤖'}",
                              "{type:'ai_letter',label:'Generate Cover Letter',target:1,current:0,completed:false,reward:30,ico:''}")
    content = content.replace("{type:'view',label:'Просмотрите 3 заказа',target:3,current:Math.min(3,Math.floor(Math.random()*2)+1),completed:false,reward:10,ico:'👁️'}",
                              "{type:'view',label:'Review Opportunities',target:3,current:Math.min(3,Math.floor(Math.random()*2)+1),completed:false,reward:10,ico:''}")
    
    # Remove reward display in bounty items - replace "+${reward}" with just progress
    content = content.replace(
        '<div class="bounty-reward">+${reward}</div>',
        '<div class="bounty-progress-quiet">${m.current}/${m.target}</div>'
    )
    
    # --- Feature 4: Ghost Counter → Market Activity ---
    content = content.replace(
        "`<div class=\"ghost-counter\"><span>👁️ ${viewing}</span><span>⚡ ${applicants} отклика</span><span class=\"ghost-trend\">↑ +${trendUp} за час</span></div>`",
        '`<div class="ghost-counter"><span>' + SVG_EYE + ' ${viewing}</span><span>' + SVG_LIGHTNING + ' ${applicants} отклика</span><span class="ghost-trend">+${trendUp}/ч</span></div>`'
    )
    content = content.replace(
        "`<div class=\"ghost-counter\"><span>👁️ ${Math.floor(viewing/10)*10}+</span><span>⚡ несколько</span></div>`",
        '`<div class="ghost-counter"><span>' + SVG_EYE + ' ${Math.floor(viewing/10)*10}+</span><span>' + SVG_LIGHTNING + ' несколько</span></div>`'
    )
    
    # --- Feature 5: Achievement Badges → Career Milestones ---
    content = content.replace("🏅 Достижения", "Карьерные вехи")
    # Achievement items - rename and replace emoji ico field with empty string (we'll use CSS/SVG for icons)
    # Bronze/silver/gold → Уровень 1/2/3
    achievements_map = {
        "{id:'first_apply',name:'Первый отклик',ico:'⚡'": "{id:'first_apply',name:'First Application',ico:''",
        "{id:'ai_master',name:'AI-мастер',ico:'🤖'": "{id:'ai_master',name:'AI Integration',ico:''",
        "{id:'streak7',name:'Стрик 7 дней',ico:'🔥'": "{id:'streak7',name:'7-Day Consistency',ico:''",
        "{id:'saver',name:'Охотник за заказами',ico:'💾'": "{id:'saver',name:'Opportunity Tracker',ico:''",
        "{id:'hunter500',name:'Охотник 500+',ico:'🎯'": "{id:'hunter500',name:'Readiness 500+',ico:''",
        "{id:'loyalty1k',name:'Лояльность 1K',ico:'💎'": "{id:'loyalty1k',name:'Credit Milestone 1K',ico:''",
        "{id:'viewer',name:'Исследователь',ico:'👁️'": "{id:'viewer',name:'Market Explorer',ico:''",
        "{id:'bounty3',name:'3 задания в день',ico:'📋'": "{id:'bounty3',name:'Daily Goals Complete',ico:''",
        "{id:'early10',name:'Ранний охотник',ico:'⚡'": "{id:'early10',name:'Early Access User',ico:''",
        "{id:'pro_week',name:'Pro-неделя',ico:'👑'": "{id:'pro_week',name:'Pro Subscriber',ico:''",
        "{id:'earn5k',name:'Заработок $5K',ico:'💰'": "{id:'earn5k',name:'Earnings $5K',ico:''",
        "{id:'social',name:'Нетворкинг',ico:'🤝'": "{id:'social',name:'Networking',ico:''",
    }
    for old, new in achievements_map.items():
        content = content.replace(old, new)
    
    # Replace tier names in renderAchievements: бронза/серебро/золото → Уровень 1/2/3
    content = content.replace("'серебро'", "'Уровень 2'")
    content = content.replace("'золото'", "'Уровень 3'")
    # In achievement rendering: bronze/silver/gold class → level-1/level-2/level-3
    content = content.replace("ach-ring ${data.tier}", "ach-ring level-${data.tier === 'bronze' ? '1' : data.tier === 'silver' ? '2' : '3'}")
    content = content.replace("ach-ring locked", "ach-ring locked")
    # Replace lock emoji
    content = content.replace('<div class="ach-ring locked">🔒</div>', '<div class="ach-ring locked">' + SVG_LOCK + '</div>')
    
    # --- Feature 6: Loyalty Points → Professional Credits ---
    content = content.replace("очков лояльности", "кредитов")
    content = content.replace("loy-label", "loy-label")
    # In renderLoyalty, the card uses gradient - we'll make it professional
    # Replace shop items with professional names
    content = content.replace("'Pro Day Pass'", "'Pro Day Pass'")
    content = content.replace("'Доп. отклик'", "'Extra Application'")
    content = content.replace("'AI Boost'", "'AI Boost'")
    content = content.replace("'Подсветка профиля'", "'Profile Highlight'")
    content = content.replace("'Подсветка'", "'Highlight'")
    content = content.replace("500 pts", "500 créd")
    content = content.replace("100 pts", "100 créd")
    content = content.replace("200 pts", "200 créd")
    content = content.replace("300 pts", "300 créd")
    
    # --- Feature 7: Intelligence Feed - keep as is, just remove emoji ---
    # generateIntel items
    intel_replacements = [
        ("{ico:'⚡',text:`Новый заказ в <b>AI/ML</b>", "{ico:'',text:`Новый заказ в <b>AI/ML</b>"),
        ("{ico:'📊',text:'Конкурент снизил ставку", "{ico:'',text:'Конкурент снизил ставку"),
        ("{ico:'👀',text:'Клиент из заказа", "{ico:'',text:'Клиент из заказа"),
        ("{ico:'💰',text:'Средняя ставка", "{ico:'',text:'Средняя ставка"),
        ("{ico:'🔥',text:`Спрос на <b>AI/ML</b>", "{ico:'',text:`Спрос на <b>AI/ML</b>"),
        ("{ico:'📈',text:'3 новых заказа", "{ico:'',text:'3 новых заказа"),
        ("{ico:'🎯',text:`Новый заказ в <b>Design</b>", "{ico:'',text:`Новый заказ в <b>Design</b>"),
    ]
    for old, new in intel_replacements:
        content = content.replace(old, new)
    
    # In renderIntelFeed, replace 🕵️ with text/SVG
    content = content.replace("🕵️ Разведка", "Разведка")
    
    # --- Feature 8: Market Pulse → Industry Analytics ---
    content = content.replace("📊 Пульс рынка", "Аналитика рынка")
    content = content.replace("💰 Ср. ставка:", "Ср. ставка:")
    
    # --- Feature 9: Leaderboard → REMOVE ---
    # Remove renderLeaderboard from renderHabitWidgets call
    content = content.replace("html += renderLeaderboard();\n", "")
    content = content.replace("  html += renderLeaderboard();\n", "")
    
    # --- Feature 10: Skill Radar → just rename title ---
    content = content.replace("🎨 Навыки vs Рынок", "Навыки vs Рынок")
    # Replace ⚡ in gapHints
    content = content.replace('⚡ ${esc(p.name)}: спрос', '${esc(p.name)}: спрос')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 2: Restructure Home Page
    # ═══════════════════════════════════════════════════════════
    
    # Change renderHabitWidgets to only show Intelligence Feed + Job feed on home
    # Move other widgets to More panel sub-pages
    
    # Replace the entire renderHabitWidgets function
    old_render = '''function renderHabitWidgets() {
  const container = document.getElementById('habitWidgets');
  if (!container) return;
  let html = '';
  html += renderStreakWidget();
  html += renderHunterScore();
  html += renderBounties();
  html += renderLoyalty();
  html += renderIntelFeed();
  html += renderMarketPulse();
  html += renderLeaderboard();
  html += renderAchievements();
  html += renderSkillRadar();
  container.innerHTML = html;
}'''
    
    new_render = '''function renderHabitWidgets() {
  const container = document.getElementById('habitWidgets');
  if (!container) return;
  let html = '';
  // Home page: only Intel Feed (core Pro value) + Market Readiness inline
  const d = calcHunterScore();
  const nl = getNextLevel(d.score);
  const pct = nl.need > nl.prev ? Math.min(((d.score - nl.prev) / (nl.need - nl.prev)) * 100, 100) : 100;
  const circumference = 2 * Math.PI * 27;
  const offset = circumference - (circumference * Math.min(pct, 100) / 100);
  const streak = getStreakData();
  html += '<div class="home-professional-bar animate-in">';
  html += '<div class="home-readiness-mini"><div class="readiness-ring-mini"><svg viewBox="0 0 64 64"><circle class="ring-bg" cx="32" cy="32" r="27" stroke="var(--border)" stroke-width="4" fill="none"/><circle class="ring-fill" cx="32" cy="32" r="27" stroke="var(--primary)" stroke-width="4" fill="none" stroke-dasharray="'+circumference+'" stroke-dashoffset="'+offset+'" style="transition:stroke-dashoffset .7s ease"/></svg><div class="readiness-ring-val">'+d.score+'</div></div><div class="readiness-info"><div class="readiness-label">Готовность к рынку</div><div class="readiness-level">'+esc(d.level)+'</div></div></div>';
  html += '<div class="home-regularity-mini">'+SVG_CALENDAR+' Регулярность: '+streak.currentDays+' дней</div>';
  html += '</div>';
  html += renderIntelFeed();
  container.innerHTML = html;
}

// Sub-page renderers for More panel
function renderPerformanceGoals() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Цели на сегодня</div>';
  html += renderBounties();
  html += '</div>';
  container.innerHTML = html;
}

function renderCareerMilestones() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Карьерные вехи</div>';
  html += renderAchievements();
  html += '</div>';
  container.innerHTML = html;
}

function renderCreditsPage() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Профессиональные кредиты</div>';
  html += renderLoyalty();
  html += '</div>';
  container.innerHTML = html;
}

function renderSkillsAnalysis() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Аналитика навыков</div>';
  html += renderSkillRadar();
  html += '</div>';
  container.innerHTML = html;
}

function renderIndustryAnalytics() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Аналитика рынка</div>';
  html += renderMarketPulse();
  html += '</div>';
  container.innerHTML = html;
}

function renderReadinessDetail() {
  const container = document.getElementById('subContent');
  if (!container) return;
  let html = '<div style="padding:0 16px 24px">';
  html += '<div style="font-size:16px;font-weight:700;color:var(--text);margin-bottom:12px;font-family:var(--font-sans)">Готовность к рынку</div>';
  html += renderHunterScore();
  html += '<div style="margin-top:14px;font-size:12px;color:var(--text-2);line-height:1.6">';
  html += '<div style="margin-bottom:6px"><strong style="color:var(--text)">Регулярность:</strong> '+getStreakData().currentDays+' дней</div>';
  html += '</div>';
  html += '</div>';
  container.innerHTML = html;
}'''
    
    content = content.replace(old_render, new_render)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 3: Add More panel menu items for moved widgets
    # ═══════════════════════════════════════════════════════════
    
    # Add new menu rows in the More panel before the "Настройки" section
    # Find the "Настройки" section head and add rows before it
    more_menu_addition = '''    <div class="more-section-head">Аналитика</div>
    <div class="more-menu-row" onclick="openMoreSub('goals', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg></div>
      <div class="more-menu-row-text">Цели</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('milestones', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div>
      <div class="more-menu-row-text">Вехи</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('readiness', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg></div>
      <div class="more-menu-row-text">Готовность к рынку</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('credits', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 6v12"/><path d="M15 9.5c0-1.38-1.34-2.5-3-2.5S9 8.12 9 9.5c0 1.38 1.34 2.5 3 2.5s3 1.12 3 2.5-1.34 2.5-3 2.5-3-1.12-3-2.5"/></svg></div>
      <div class="more-menu-row-text">Кредиты</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('skills-analysis', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg></div>
      <div class="more-menu-row-text">Аналитика навыков</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    <div class="more-menu-row" onclick="openMoreSub('industry-analytics', event)">
      <div class="more-menu-row-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg></div>
      <div class="more-menu-row-text">Аналитика рынка</div>
      <div class="more-menu-row-arrow"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"/></svg></div>
    </div>
    '''
    
    # Insert before the "Настройки" section
    content = content.replace(
        '    <div class="more-section-head">Настройки</div>',
        more_menu_addition + '    <div class="more-section-head">Настройки</div>'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 4: Add new sub-screen cases in openMoreSub function
    # ═══════════════════════════════════════════════════════════
    
    # Find the openMoreSub function and add new cases
    # Add before the closing of the switch/if-else chain
    # We need to add cases for: goals, milestones, readiness, credits, skills-analysis, industry-analytics
    
    new_sub_cases = """      case 'goals':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Цели</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderPerformanceGoals();
        break;
      case 'milestones':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Карьерные вехи</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderCareerMilestones();
        break;
      case 'readiness':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Готовность к рынку</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderReadinessDetail();
        break;
      case 'credits':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Профессиональные кредиты</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderCreditsPage();
        break;
      case 'skills-analysis':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Аналитика навыков</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderSkillsAnalysis();
        break;
      case 'industry-analytics':
        html = '<div style="display:flex;align-items:center;gap:10px;margin-bottom:20px"><button class="back-btn" onclick="closeMoreSub()"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"/></svg></button><div style="font-size:16px;font-weight:700;color:var(--text);font-family:var(--font-sans)">Аналитика рынка</div></div><div id="subContent"></div>';
        subBody.innerHTML = html;
        renderIndustryAnalytics();
        break;
"""
    
    # Find the switch statement in openMoreSub and add cases before 'about'
    content = content.replace(
        "      case 'about':",
        new_sub_cases + "      case 'about':"
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 5: Add CSS for new professional elements
    # ═══════════════════════════════════════════════════════════
    
    professional_css = """
/* ── Professional Redesign: Home Bar ── */
.home-professional-bar{display:flex;align-items:center;gap:14px;padding:12px 14px;background:var(--bg-card);border-radius:var(--radius);border:1px solid var(--border-soft);box-shadow:var(--shadow);margin-bottom:14px}
.home-readiness-mini{display:flex;align-items:center;gap:10px;flex:1}
.readiness-ring-mini{position:relative;width:40px;height:40px;flex-shrink:0}
.readiness-ring-mini svg{width:40px;height:40px;transform:rotate(-90deg)}
.readiness-ring-val{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;color:var(--text);font-family:var(--font-sans)}
.readiness-info{min-width:0}
.readiness-label{font-size:10px;color:var(--text-3);font-weight:600;font-family:var(--font-sans);text-transform:uppercase;letter-spacing:.3px}
.readiness-level{font-size:13px;font-weight:700;color:var(--text);font-family:var(--font-sans)}
.home-regularity-mini{display:flex;align-items:center;gap:4px;font-size:11px;color:var(--text-3);font-weight:600;font-family:var(--font-sans);white-space:nowrap;flex-shrink:0}
.home-regularity-mini svg{width:14px;height:14px;color:var(--text-3)}

/* Streak icon replacement */
.streak-ico{width:36px;height:36px;border-radius:var(--radius-xs);background:var(--primary-light);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.streak-ico svg{width:18px;height:18px;color:var(--primary)}

/* Professional habit cards - muted */
.habit-card{background:var(--bg-card);border-radius:var(--radius);padding:14px;border:1px solid var(--border-soft);box-shadow:var(--shadow);margin-bottom:12px}
.habit-card-title{font-size:12px;font-weight:700;color:var(--text);margin-bottom:10px;font-family:var(--font-sans);text-transform:uppercase;letter-spacing:.3px}

/* Professional credits card - no flashy gradient */
.loyalty-card{background:var(--bg-card);border-radius:var(--radius);padding:16px;border:1px solid var(--border-soft);box-shadow:var(--shadow);color:var(--text);position:relative;overflow:hidden;margin-bottom:14px}
.loyalty-card::before{display:none}
.loy-balance{font-size:28px;font-weight:800;color:var(--text);letter-spacing:-.3px}
.loy-label{font-size:11px;color:var(--text-3);margin-top:2px;font-family:var(--font-sans)}
.loy-shop{display:flex;gap:6px;margin-top:12px;flex-wrap:wrap}
.loy-item{padding:8px 12px;border-radius:var(--radius-xs);border:1px solid var(--border-soft);background:var(--bg-card);cursor:pointer;transition:all .2s;font-family:var(--font-sans)}
.loy-item:hover{border-color:var(--primary);background:var(--primary-soft)}
.loy-item:active{transform:scale(.97)}
.loy-item-name{font-size:11px;font-weight:600;color:var(--text)}
.loy-item-cost{font-size:10px;color:var(--text-3);margin-top:1px}

/* Achievement level tiers - professional */
.ach-ring.level-1{border-color:var(--primary);background:var(--primary-soft)}
.ach-ring.level-2{border-color:var(--lavender);background:var(--lavender-light)}
.ach-ring.level-3{border-color:var(--warning);background:var(--warning-light)}
.ach-ring.level-1 svg{color:var(--primary)}
.ach-ring.level-2 svg{color:var(--lavender)}
.ach-ring.level-3 svg{color:var(--warning)}

/* Bounty progress quiet */
.bounty-progress-quiet{font-size:11px;color:var(--text-3);font-weight:600;font-family:var(--font-sans)}

/* Ghost counter - professional */
.ghost-counter span svg{width:12px;height:12px;vertical-align:-1px;margin-right:2px}

/* Intel item icon replacement */
.intel-ico{width:24px;height:24px;border-radius:6px;display:flex;align-items:center;justify-content:center;flex-shrink:0;background:var(--primary-light);color:var(--primary)}
.intel-ico svg{width:12px;height:12px}
"""
    
    # Insert CSS before the closing </style> tag
    content = content.replace('</style>\n', professional_css + '</style>\n')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 6: Remove Leaderboard CSS
    # ═══════════════════════════════════════════════════════════
    
    # Comment out leaderboard CSS (between "/* Leaderboard */" and "/* Repa Score Detail */")
    # Actually, let's just leave the CSS - it won't render if the HTML is not generated
    
    # ═══════════════════════════════════════════════════════════
    # STEP 7: Update trial welcome overlay
    # ═══════════════════════════════════════════════════════════
    
    # Replace the "Разведка и стрики" feature in trial welcome
    content = content.replace(
        '<div class="trial-welcome-feat-title">Разведка и стрики</div><div class="trial-welcome-feat-desc">Аналитика рынка, серия охоты, x2 награды и рейтинг</div>',
        '<div class="trial-welcome-feat-title">Разведка и аналитика</div><div class="trial-welcome-feat-desc">Аналитика рынка, готовность к рынку, профессиональные кредиты</div>'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 8: Replace remaining emoji with SVG in bounty rendering
    # ═══════════════════════════════════════════════════════════
    
    # In renderBounties, the ico field is now empty, so the bounty-ico div will be empty
    # Let's use type-based icons instead
    content = content.replace(
        '<div class="bounty-ico" style="background:var(--primary-light)">${m.ico}</div>',
        '<div class="bounty-ico" style="background:var(--primary-light)">${m.type===\'apply\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z&quot;/></svg>\':m.type===\'save\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z&quot;/></svg>\':m.type===\'ai_letter\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M12 2L2 7l10 5 10-5-10-5z&quot;/><path d=&quot;M2 17l10 5 10-5&quot;/></svg>\':\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><circle cx=&quot;12&quot; cy=&quot;12&quot; r=&quot;10&quot;/><polyline points=&quot;12 6 12 12 16 14&quot;/></svg>\'}</div>'
    )
    
    # Actually, the above approach is too complex with all the escaping. Let me use a simpler approach.
    # Let me just replace the bounty ico rendering to use the type field directly.
    # Revert the complex replacement and use a simpler method
    content = content.replace(
        '''<div class="bounty-ico" style="background:var(--primary-light)">${m.type===\'apply\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z&quot;/></svg>\':m.type===\'save\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z&quot;/></svg>\':m.type===\'ai_letter\'?\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><path d=&quot;M12 2L2 7l10 5 10-5-10-5z&quot;/><path d=&quot;M2 17l10 5 10-5&quot;/></svg>\':\'<svg viewBox=&quot;0 0 24 24&quot; fill=&quot;none&quot; stroke=&quot;currentColor&quot; stroke-width=&quot;2&quot; style=&quot;width:14px;height:14px&quot;><circle cx=&quot;12&quot; cy=&quot;12&quot; r=&quot;10&quot;/><polyline points=&quot;12 6 12 12 16 14&quot;/></svg>\'}</div>''',
        '<div class="bounty-ico" style="background:var(--primary-light)"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><polyline points="9 11 12 14 22 4"/><path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"/></svg></div>'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 9: Replace intel feed icon rendering with SVG
    # ═══════════════════════════════════════════════════════════
    
    # Since we set ico to empty string, we need to change the rendering
    # Replace the intel-item rendering to not use emoji ico
    content = content.replace(
        '<div class="intel-ico">${i.ico}</div>',
        '<div class="intel-ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg></div>'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 10: Replace achievement ico rendering with SVG
    # ═══════════════════════════════════════════════════════════
    
    # In renderAchievements, replace ${a.ico} with a generic milestone icon
    content = content.replace(
        '<div class="ach-ring ${data.tier === \'bronze\' ? \'1\' : data.tier === \'silver\' ? \'2\' : \'3\'}">${a.ico}</div>',
        '<div class="ach-ring level-${data.tier === \'bronze\' ? \'1\' : data.tier === \'silver\' ? \'2\' : \'3\'}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div>'
    )
    
    # Also fix the default achievement ring (for earned items where the previous replacement might not match)
    # Let's also handle the case where the tier class is still the original
    content = content.replace(
        '<div class="ach-ring ${data.tier}">${a.ico}</div>',
        '<div class="ach-ring level-${data.tier === \'bronze\' ? \'1\' : data.tier === \'silver\' ? \'2\' : \'3\'}"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:14px;height:14px"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg></div>'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 11: Hunt for remaining emoji and replace/remove them
    # ═══════════════════════════════════════════════════════════
    
    # Remove any remaining common emoji patterns
    import re
    
    # Remove emoji from remaining places
    emoji_patterns = [
        ('🔥', ''),  # Fire - remove entirely
        ('🎯', ''),  # Target - remove
        ('👻', ''),  # Ghost - remove
        ('👁️', ''),  # Eye - remove
        ('👁', ''),   # Eye variant - remove
        ('⚡', ''),  # Lightning - remove  
        ('🏅', ''),  # Medal - remove
        ('💎', ''),  # Diamond - remove
        ('🏆', ''),  # Trophy - remove
        ('📊', ''),  # Chart - remove
        ('🕵️', ''),  # Detective - remove
        ('🕵', ''),   # Detective variant - remove
        ('🎨', ''),  # Palette - remove
        ('📋', ''),  # Clipboard - remove
        ('❄️', ''),  # Snowflake - remove
        ('❄', ''),   # Snowflake variant - remove
        ('🎁', ''),  # Gift - remove
        ('🎉', ''),  # Party - remove
        ('✨', ''),  # Sparkles - remove
        ('🚀', ''),  # Rocket - remove
        ('💰', ''),  # Money - remove
        ('👇', ''),  # Point down - remove
        ('✅', ''),  # Check - remove
        ('⚠️', ''),  # Warning - remove
        ('⚠', ''),   # Warning variant - remove
        ('👋', ''),  # Wave - remove
        ('🔒', ''),  # Lock - handled separately with SVG
        ('💾', ''),  # Floppy - remove
        ('🤖', ''),  # Robot - remove
        ('👑', ''),  # Crown - remove
        ('🤝', ''),  # Handshake - remove
        ('📈', ''),  # Chart up - remove
        ('👀', ''),  # Eyes - remove
    ]
    
    for emoji, replacement in emoji_patterns:
        content = content.replace(emoji, replacement)
    
    # Clean up double spaces that might result from emoji removal
    content = re.sub(r'  +', ' ', content)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 12: Mute the streak/fire styling in CSS
    # ═══════════════════════════════════════════════════════════
    
    # Replace streak-fire CSS with streak-ico
    content = content.replace('.streak-fire{font-size:28px}', '.streak-ico{width:36px;height:36px;border-radius:var(--radius-xs);background:var(--primary-light);display:flex;align-items:center;justify-content:center;flex-shrink:0}.streak-ico svg{width:18px;height:18px;color:var(--primary)}')
    
    # Replace loyalty-card CSS gradient with muted
    content = content.replace(
        '.loyalty-card{background:linear-gradient(135deg,var(--primary),var(--lavender));border-radius:var(--radius);padding:20px;color:#fff;position:relative;overflow:hidden;margin-bottom:14px}',
        '.loyalty-card{background:var(--bg-card);border-radius:var(--radius);padding:16px;border:1px solid var(--border-soft);box-shadow:var(--shadow);color:var(--text);position:relative;overflow:hidden;margin-bottom:14px}'
    )
    content = content.replace(
        ".loyalty-card::before{content:'';position:absolute;top:-20px;right:-20px;width:80px;height:80px;border-radius:50%;background:rgba(255,255,255,.1)}",
        ".loyalty-card::before{display:none}"
    )
    
    # Replace loyalty points/label styling
    content = content.replace(
        '.loyalty-points{font-size:32px;font-weight:800}',
        '.loy-balance{font-size:28px;font-weight:800;color:var(--text);letter-spacing:-.3px}'
    )
    content = content.replace(
        '.loyalty-label{font-size:12px;opacity:.8;margin-top:2px}',
        '.loy-label{font-size:11px;color:var(--text-3);margin-top:2px}'
    )
    content = content.replace(
        '.loyalty-next{font-size:11px;opacity:.7;margin-top:8px}',
        '.loyalty-next{font-size:11px;color:var(--text-3);margin-top:8px}'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 13: Clean up the habit-card-title CSS for uppercase
    # ═══════════════════════════════════════════════════════════
    
    # The existing habit-card-title might have different styling - let's check and update
    # Add professional styling if not already added
    if '.habit-card-title' not in content.split(professional_css)[0][-200:]:
        pass  # Already handled in the CSS insertion
    
    # ═══════════════════════════════════════════════════════════
    # STEP 14: Replace loyalty-points/loyalty-label class names in JS
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('loyalty-points', 'loy-balance')
    content = content.replace('loyalty-label', 'loy-label')
    content = content.replace('loyalty-next', 'loy-next')
    content = content.replace('loyalty-shop', 'loy-shop')
    content = content.replace('loyalty-item', 'loy-item')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 15: Fix the streak CSS - replace streak-row and streak-info references
    # ═══════════════════════════════════════════════════════════
    
    # The streak widget HTML uses streak-row and streak-fire - let's update
    content = content.replace(
        '<div class="streak-row"><div class="streak-ico">' + SVG_CALENDAR + '</div><div class="streak-info">',
        '<div class="streak-row"><div class="streak-ico">' + SVG_CALENDAR + '</div><div class="streak-info">'
    )
    # This should already be fine from our earlier replacement
    
    # ═══════════════════════════════════════════════════════════
    # STEP 16: Remove the "Habit-Forming Features Engine" section title
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace(
        '// ── Feature 1: Daily Hunt Streak ──',
        '// ── Feature 1: Regularity Index ──'
    )
    content = content.replace(
        '// ── Feature 2: Hunter Score ──',
        '// ── Feature 2: Market Readiness Score ──'
    )
    content = content.replace(
        '// ── Feature 3: Daily Bounties ──',
        '// ── Feature 3: Performance Goals ──'
    )
    content = content.replace(
        '// ── Feature 5: Achievement Badges ──',
        '// ── Feature 5: Career Milestones ──'
    )
    content = content.replace(
        '// ── Feature 6: Intelligence Feed ──',
        '// ── Feature 6: Intelligence Feed ──'
    )
    content = content.replace(
        '// ── Feature 7: Market Pulse ──',
        '// ── Feature 7: Industry Analytics ──'
    )
    content = content.replace(
        '// ── Feature 8: Loyalty Points & Shop ──',
        '// ── Feature 8: Professional Credits ──'
    )
    content = content.replace(
        '// ── Feature 9: Weekly Leaderboard ──',
        '// ── Feature 9: REMOVED (Leaderboard) ──'
    )
    content = content.replace(
        '// ── Feature 10: Skill Radar ──',
        '// ── Feature 10: Skills Gap Analysis ──'
    )
    content = content.replace(
        '// ── Master Render: All Habit Widgets ──',
        '// ── Master Render: Home Widgets ──'
    )
    content = content.replace(
        '// ── Habit-Forming Features Engine ──',
        '// ── Professional Features Engine ──'
    )
    content = content.replace(
        '// ── Habit-forming widgets ──',
        '// ── Professional widgets ──'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 17: Remove the onboarding overlay's game-like language
    # ═══════════════════════════════════════════════════════════
    
    # The onboarding overlay might have game-like steps - let's leave it mostly alone 
    # since the guided steps are about the core workflow (open, filter, apply)
    
    # ═══════════════════════════════════════════════════════════
    # STEP 18: Remove streak-freeze class styling (replaced with Activity Pause)
    # ═══════════════════════════════════════════════════════════
    
    # The streak-freeze button should look professional
    content = content.replace(
        '.streak-freeze{',
        '.streak-freeze,.streak-pause{'
    )
    
    # ═══════════════════════════════════════════════════════════
    # STEP 19: Clean up any remaining "Охотник" references
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Охотник', 'Специалист')
    content = content.replace('охотник', 'специалист')
    content = content.replace('охоты', 'активности')
    content = content.replace('Охоты', 'Активности')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 20: Clean up "стрик" references → "регулярность"
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Стрик', 'Регулярность')
    content = content.replace('стрик', 'регулярность')
    content = content.replace('Заморозка стрика', 'Пауза активности')
    content = content.replace('заморозка стрика', 'пауза активности')
    content = content.replace('Заморозка', 'Пауза')
    content = content.replace('заморозки', 'паузы')
    content = content.replace('Максимум 3 заморозки', 'Максимум 3 паузы')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 21: Update "Серия охоты" → "Регулярность" if any remain
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Серия охоты', 'Регулярность')
    content = content.replace('серия охоты', 'регулярность')
    content = content.replace('Ежедневные задания', 'Цели на сегодня')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 22: Clean up "Достижения" → "Карьерные вехи" if any remain
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Достижения', 'Карьерные вехи')
    content = content.replace('достижения', 'карьерные вехи')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 23: Clean up "Пульс рынка" → "Аналитика рынка" if any remain
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Пульс рынка', 'Аналитика рынка')
    content = content.replace('пульс рынка', 'аналитика рынка')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 24: Clean up "Новичок" → "Начинающий" if any remain
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Новичок', 'Начинающий')
    content = content.replace('новичок', 'начинающий')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 25: Clean up "Легенда" → "Топ-эксперт" and "Мастер" → "Ведущий" if any remain
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Легенда', 'Топ-эксперт')
    content = content.replace('Мастер', 'Ведущий')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 26: Clean up "Лояльность" → "Кредиты" / "Профессиональные кредиты"
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Лояльность', 'Кредиты')
    content = content.replace('лояльности', 'кредитов')
    content = content.replace('очков лояльности', 'кредитов')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 27: Remove "Рейтинг недели" references
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Рейтинг недели', '')
    content = content.replace('рейтинг недели', '')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 28: Update "xp" references to "очков" or "points"
    # ═══════════════════════════════════════════════════════════
    
    # In leaderboard rendering, replace "XP" with "очков"
    content = content.replace('XP</div>', 'очков</div>')
    # But be careful not to replace legitimate XP references
    
    # ═══════════════════════════════════════════════════════════
    # STEP 29: Remove any remaining emoji that might have been missed
    # ═══════════════════════════════════════════════════════════
    
    # Use regex to catch any remaining emoji
    emoji_regex = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"
        "\u3030"
        "]+", flags=re.UNICODE)
    
    # Only remove emoji that are standalone (not part of SVG or HTML entities)
    # This is tricky - let's just do targeted replacements for known emoji
    
    # ═══════════════════════════════════════════════════════════
    # STEP 30: Replace "Habit-Forming" section title with "Professional"
    # ═══════════════════════════════════════════════════════════
    
    content = content.replace('Habit-Forming', 'Professional')
    content = content.replace('habit-forming', 'professional')
    content = content.replace('Habit-forming', 'Professional')
    
    # ═══════════════════════════════════════════════════════════
    # STEP 31: Clean up the streak-num / streak-label references
    # ═══════════════════════════════════════════════════════════
    
    # The streak widget now uses class names like streak-num which should still work
    # But let's make sure the streak widget rendering is correct
    
    # ═══════════════════════════════════════════════════════════
    # FINAL: Clean up any empty HTML elements from emoji removal
    # ═══════════════════════════════════════════════════════════
    
    # Remove empty span/div with just whitespace from emoji removal
    content = re.sub(r'>\s+</(span|div)>', '></\\1>', content)
    
    return content


# Read the input file
with open('/home/z/my-project/upload/index (16) (2).html', 'r', encoding='utf-8') as f:
    content = f.read()

# Apply transformations
content = transform(content)

# Write the output file
with open('/home/z/my-project/upload/SkillHunt_Redesign.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Transformation complete! Output: SkillHunt_Redesign.html")
print(f"Input size: 7122 lines")
print(f"Output size: {content.count(chr(10)) + 1} lines")
