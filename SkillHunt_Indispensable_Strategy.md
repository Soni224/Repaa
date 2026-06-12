# SkillHunt: From "Job Board" to "I Can't Live Without This"

## Implementation Plan: 10 Features That Create Psychological Dependency

---

## CODEBASE ANALYSIS SUMMARY

**What exists (CSS defined but NOT rendered):**
- `.streak` / `.home-streak` — daily streak display
- `.achievement-grid` / `.achievement` — badge collection
- `.loyalty-card` — loyalty points card
- `.repa-score-card` — reputation score ring
- `.badge-row` / `.badge-ring` — badge showcase (bronze/silver/gold/locked)

**What's functional but underwhelming:**
- 3-tab layout (Feed → Search → Saved)
- Pro subscription ($4.99/mo) with trial
- AI cover letter & strategy (Pro-gated)
- 15 mock jobs with category filters

**The fundamental problem:** Nothing makes you open the app TOMORROW. Nothing makes you feel LOSS if you delete it. Nothing makes you say "I'm a SkillHunt user" as an identity.

---

## FEATURE #1: 🔥 DAILY HUNT STREAK

**Priority:** #1 (HIGHEST — this is the foundation every other feature builds on)

### Psychological Mechanism
**Loss aversion + sunk cost fallacy + endowment effect.** The brain feels the pain of losing something 2x more than the pleasure of gaining it. A 7-day streak represents INVESTED TIME that the user literally cannot bear to lose. Each day they continue, the sunk cost grows, making it harder to stop. This is the same mechanism that keeps Duolingo users coming back — not the desire to learn, but the fear of losing their streak.

### Exact UX Flow

**When the user opens the app each day:**

1. **Streak Counter Widget** appears at the TOP of the Feed page, right below the greeting, BEFORE any job cards. It uses the existing `.home-streak` CSS class.

   Visual: `🔥 7` | "7-day hunt streak" | `[Mon][Tue][Wed][Thu][Fri][Sat][Sun]` (filled dots)

2. **Daily Check-in Animation:** When the streak increments (first open of the day), a full-screen celebration fires for 1.5 seconds:
   - Streak number pulses and scales up with `@keyframes scoreCountUp`
   - Particles (small emoji-style icons: 🔥⚡💰) float upward
   - Haptic feedback via `tg.HapticFeedback.notificationOccurred('success')`
   - Toast: "🔥 Day 7! You're on fire!"

3. **Streak Freeze (Pro-only):** If a user hasn't opened the app by 8pm local time, Pro users see a Telegram notification: "Your 7-day streak is about to break! 🔥 Use Streak Freeze to protect it." Inside the app, they see a "🧊 Streak Freeze" button that protects 1 day. Free users see the same prompt but with "🔒 Streak Freeze — Pro only".

4. **Streak Milestones:** At days 3, 7, 14, 30, 60, 90 — a special badge unlocks (ties into Feature #4 Achievements). The milestone overlay shows: "🏅 First Week Hunter — You've checked in 7 days straight. Top 12% of freelancers."

### How It Creates Dependency
- **Daily anxiety:** "I haven't checked in today, my streak will die"
- **Numerical identity:** "I'm a 23-day streak hunter" becomes a thing they SAY about themselves
- **Milestone anticipation:** Day 6 makes you EXTREMELY motivated to open on Day 7
- **Streak Freeze as Pro anchor:** The ONLY way to protect your streak when life happens is Pro. This turns every vacation, every sick day into a Pro conversion moment

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Streak tracking | ✅ Yes | ✅ Yes |
| Streak Freeze | ❌ (see it locked) | ✅ 2 per month |
| Milestone celebrations | Basic toast | Full animation + badge |
| Streak-based XP bonus | 1x | 1.5x multiplier |

### HTML/CSS/JS Changes

**HTML:** Add streak widget container in Feed page after `#feedGreeting`:
```html
<div id="streakContainer"></div>
```

**CSS:** Already exists! `.home-streak`, `.home-streak-num`, `.home-streak-body`, `.home-streak-text`, `.home-streak-dots`, `.home-streak-dot` — all defined but unused. Add:
```css
.streak-freeze-btn { ... }
.streak-freeze-locked { ... }
.streak-milestone-overlay { ... }
@keyframes streakPulse { ... }
```

**JS State:**
```javascript
// In localStorage: skillhunt_streak
{
  currentStreak: 7,
  lastCheckIn: "2025-01-15",
  longestStreak: 12,
  freezesUsed: 0,
  freezesMax: 2, // Pro only
  milestones: [3, 7] // unlocked milestone days
}
```

**JS Functions:**
- `checkStreak()` — called on init, compares lastCheckIn with today
- `incrementStreak()` — updates streak state, triggers animation
- `useStreakFreeze()` — Pro-only, protects streak for 1 day
- `renderStreakWidget()` — renders the `.home-streak` component
- `showStreakMilestone(day)` — full-screen celebration overlay

---

## FEATURE #2: 🎯 HUNTER SCORE (Your Freelancer Identity Number)

**Priority:** #2 (This is the IDENTITY anchor — the number that defines them)

### Psychological Mechanism
**Self-determination theory + social identity theory + endowment effect.** When users have a quantified "score" that they've built over time, it becomes part of their self-concept. They don't just "use SkillHunt" — they "have a Hunter Score of 847." This number feels like property they've earned. Walking away means abandoning an asset. The ring visualization (already in CSS as `.repa-score-card`) creates a visual "completeness" urge — an incomplete ring is psychologically uncomfortable.

### Exact UX Flow

1. **Hunter Score Ring** appears in the Feed page, below the streak widget. Uses the existing `.repa-score-card` CSS with the SVG ring.

   Visual: Circular ring (partially filled) | Score: 847 | Level: "Silver Hunter" | "1,153 XP to Gold"

2. **XP Gain Micro-animations:** Every action in the app earns XP:
   - Open the app daily: +10 XP
   - View a job detail: +5 XP
   - Save a job: +5 XP
   - Apply to a job: +20 XP
   - Use AI cover letter: +15 XP
   - Maintain 7-day streak: +50 XP bonus
   
   Each XP gain shows a floating "+10 XP" animation near the Hunter Score ring.

3. **Level Tiers (using existing CSS):**
   - 0-499: 🔤 Beginner (bronze ring, `#CD7F32`)
   - 500-1499: ⚔️ Hunter (silver ring, `#9CA3AF`)
   - 1500-4999: 🏆 Pro Hunter (gold ring, `#E6B800`)
   - 5000+: 💎 Elite (diamond ring, `#67E8F9`)

4. **Hunter Score Detail Page:** Tap the ring to see a full breakdown:
   - Score breakdown (Applications: 340, Activity: 280, Streak: 227)
   - Current level badge
   - Progress to next level
   - Comparison: "You're in the top 23% of hunters"

### How It Creates Dependency
- **Numerical identity:** People MEMORIZE their scores. "I'm at 847" becomes a status symbol
- **Visual incompleteness:** A ring at 68% fill creates an itch to fill it
- **Progress never lost:** The score only goes UP. This creates an "investment portfolio" that's painful to abandon
- **Level names as identity:** "I'm a Gold Hunter" becomes something they say in Telegram groups

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Score tracking | ✅ | ✅ |
| XP per action | Base rate | 1.5x multiplier |
| Score breakdown | Total only | Detailed by category |
| Leaderboard rank | Hidden | Visible with rank # |
| Level-up celebration | Toast only | Full-screen badge animation |

### HTML/CSS/JS Changes

**HTML:** Add score container in Feed:
```html
<div id="hunterScoreContainer"></div>
```

**CSS:** Already exists! `.repa-score-card`, `.repa-score-ring`, `.repa-score-ring-val`, `.repa-score-level`, `.repa-score-detail` — all defined. Add:
```css
.xp-float { position:absolute; animation: xpFloat 1.2s ease forwards; }
@keyframes xpFloat { 0%{opacity:1;transform:translateY(0)} 100%{opacity:0;transform:translateY(-40px)} }
.hunter-level-badge { /* using existing .rs-level-badge styles */ }
```

**JS State:**
```javascript
// localStorage: skillhunt_hunter_score
{
  totalXP: 847,
  level: "silver",
  breakdown: { applications: 340, activity: 280, streak: 227 },
  history: [] // XP gain events for the float animations
}
```

**JS Functions:**
- `getHunterScore()` — reads/persists score state
- `awardXP(amount, reason)` — adds XP, triggers float animation, checks level-up
- `calculateLevel(xp)` — returns level name and color
- `renderHunterScore()` — renders the score ring widget
- `showLevelUp(newLevel)` — full-screen celebration with `@keyframes badgePop`

---

## FEATURE #3: 📋 DAILY BOUNTIES (Today's Missions)

**Priority:** #3 (This is the DAILY HOOK — the reason they open at 9am)

### Psychological Mechanism
**Variable ratio reinforcement + goal gradient effect + Zeigarnik effect.** Variable rewards (the bounties change daily) are the most addictive reward schedule known to psychology — this is what makes slot machines compelling. The goal gradient effect means people accelerate effort as they approach completion (3/4 bounties done = EXTREMELY motivated to finish). The Zeigarnik effect means incomplete tasks create cognitive tension that persists until resolved.

### Exact UX Flow

1. **Bounty Card** appears at the top of Feed, above all jobs, with a distinct visual style (gradient border, slightly larger):

   ```
   ┌─────────────────────────────────────┐
   │ 🎯 TODAY'S BOUNTIES          2/4   │
   │ ━━━━━━━━━━━━━━━━━━░░░░░░░░░░  50% │
   │                                     │
   │ ✅ Open SkillHunt          +10 XP  │
   │ ✅ View 3 job details      +15 XP  │
   │ ⬜ Apply to 1 job          +25 XP  │
   │ ⬜ Save 2 jobs             +10 XP  │
   │                                     │
   │ 🎁 Reward: 50 Loyalty Points       │
   └─────────────────────────────────────┘
   ```

2. **Bounty Types (rotating daily from a pool of 20):**
   - Easy: Open app, check feed, view profile
   - Medium: View 3 job details, save 2 jobs, search with filters
   - Hard: Apply to a job (costs an application), use AI feature, share a job
   - Streak: Maintain 3+ day streak (auto-completes for streakers)

3. **Bounty Reset:** Every day at midnight (user's local time), bounties refresh. The old ones disappear — FOREVER. This creates genuine FOMO: "I didn't complete yesterday's bounties and I lost 60 XP."

4. **Bounty Completion Animation:** When the last bounty is checked off, a confetti burst fires, the progress bar fills with a satisfying animation, and the reward is instantly credited.

### How It Creates Dependency
- **Daily structure:** Users plan their morning around completing bounties
- **FOMO:** Incomplete bounties = lost XP = lost progress = anxiety
- **Variable reward:** Different bounties each day = unpredictable = more dopamine
- **Goal gradient:** 3/4 done = can't stop now
- **Time pressure:** "I have until midnight" creates urgency

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Daily bounties | 3 per day | 5 per day |
| XP per bounty | Base | 1.5x |
| Bonus reward | 30 Loyalty Points | 50 + rare badge chance |
| Streak bounty | ❌ | ✅ (auto-completes for streakers) |

### HTML/CSS/JS Changes

**HTML:** Add bounty container in Feed after streak:
```html
<div id="bountyContainer"></div>
```

**CSS:** New styles needed:
```css
.bounty-card { background: var(--bg-card); border-radius: var(--radius); border: 2px solid transparent; background-clip: padding-box; position: relative; overflow: hidden; }
.bounty-card::before { content:''; position:absolute; inset:-2px; border-radius:inherit; background:linear-gradient(135deg,var(--primary),var(--lavender),var(--mint)); z-index:-1; }
.bounty-progress { height:6px; background:var(--bg-input); border-radius:3px; overflow:hidden; }
.bounty-progress-fill { height:100%; background:linear-gradient(90deg,var(--primary),var(--mint)); border-radius:3px; transition:width .5s cubic-bezier(.22,1,.36,1); }
.bounty-item { display:flex; align-items:center; gap:10px; padding:8px 0; border-bottom:1px solid var(--border-soft); }
.bounty-item:last-child { border-bottom:none; }
.bounty-check { width:20px; height:20px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
.bounty-check.done { background:var(--success); color:#fff; }
.bounty-check.pending { background:var(--bg-input); border:2px solid var(--border); }
.bounty-xp { font-size:11px; font-weight:700; color:var(--primary); margin-left:auto; }
```

**JS State:**
```javascript
// localStorage: skillhunt_bounties
{
  date: "2025-01-15",
  bounties: [
    { id: "daily_open", text: "Open SkillHunt", xp: 10, done: true },
    { id: "view_3_jobs", text: "View 3 job details", xp: 15, done: false, progress: 1, target: 3 },
    { id: "apply_1", text: "Apply to 1 job", xp: 25, done: false },
    { id: "save_2", text: "Save 2 jobs", xp: 10, done: false, progress: 0, target: 2 }
  ],
  completed: false
}
```

**JS Functions:**
- `generateDailyBounties()` — picks from bounty pool based on date seed
- `checkBountyProgress(bountyId)` — updates bounty state on actions
- `renderBountyCard()` — renders the bounty widget
- `completeBounty(id)` — marks done, awards XP, checks if all complete
- `resetBountiesIfNewDay()` — called on init, checks date

---

## FEATURE #4: 🏅 ACHIEVEMENT BADGES (Your Trophy Collection)

**Priority:** #4 (SUNK COST — this is the collection they can't bear to lose)

### Psychological Mechanism
**Collection instinct + completion drive + IKEA effect.** Humans have a deep innate drive to COLLECT and COMPLETE sets. When you have 7 of 9 achievements in a row, the cognitive tension of the 2 missing spots is almost unbearable. The IKEA effect means we value things more when we've invested effort into them. An achievement earned through 30 days of streaks feels VALUABLE in a way that a gifted badge never could.

### Exact UX Flow

1. **Achievement Showcase** appears as a horizontal scrollable row on the Feed page, below bounties:

   ```
   ┌──────────────────────────────────────────────┐
   │ 🏅 Achievements (4/12)                       │
   │                                               │
   │ [🔥]  [📋]  [❄️]  [🎯]  [🔒]  [🔒]  [🔒]  │
   │ 3-Day  First  Ice   First  ???    ???    ???  │
   │ Streak  Apply  Break Hunt                       │
   └──────────────────────────────────────────────┘
   ```

   Uses existing `.achievement-grid` / `.achievement` CSS.

2. **Achievement Definitions (12 total):**
   
   **Streak achievements (3):**
   - 🔥 Week Warrior — 7-day streak (bronze)
   - 🔥🔥 Flame Keeper — 30-day streak (silver)
   - 🔥🔥🔥 Eternal Fire — 90-day streak (gold)
   
   **Action achievements (4):**
   - 📋 First Blood — First job application
   - 🎯 Sharpshooter — Apply to 5 jobs with 85%+ match
   - 💰 Big League — Apply to a job with $5K+ budget
   - 🧠 AI Powered — Use AI cover letter 3 times
   
   **Social achievements (3):**
   - 👁️ Watched — 10 profile views
   - ⭐ Client Favorite — Get a "viewed" status on 3 applications
   - 🏆 Top 10% — Reach top 10% on Hunter Score leaderboard
   
   **Collection achievements (2):**
   - 📚 Curator — Save 10 jobs across 3 categories
   - 💎 Completionist — Unlock all other achievements

3. **Achievement Unlock Animation:** When an achievement unlocks, a modal appears with:
   - Badge icon scaling from 0 with `@keyframes badgePop` (already in CSS!)
   - Name and description
   - XP reward (+50 XP for bronze, +100 for silver, +200 for gold)
   - "Share to Telegram" button

4. **Profile Badge Display:** Earned achievements appear as small icons next to the user's name in the greeting and in the More panel profile.

### How It Creates Dependency
- **Collection urge:** Missing badges create visual "holes" that itch to be filled
- **Completion drive:** "4/12" makes you want to get to 12/12
- **Social signaling:** Visible badges in profile = status
- **Sunk cost:** All those achievements = months of investment = can't leave
- **Rarity signaling:** Gold achievements are rare and valuable

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Visible achievements | 6 basic | All 12 |
| Achievement XP bonus | +25 XP | +50 XP per unlock |
| Share to Telegram | ❌ | ✅ |
| Profile badge display | 1 badge | All earned badges |
| Progress hints | ❌ | ✅ ("2 more AI letters for 🧠") |

### HTML/CSS/JS Changes

**HTML:** Add achievement row in Feed:
```html
<div id="achievementRowContainer"></div>
```

**CSS:** Already exists! `.achievement-grid`, `.achievement`, `.achievement.earned`, `.achievement.locked`, `.achievement-ico`, `.achievement-name` — all defined. Also `.badge-row`, `.badge-ring` with bronze/silver/gold/locked variants. Add:
```css
.achievement-scroll { display:flex; gap:8px; overflow-x:auto; padding:4px 0; -webkit-overflow-scrolling:touch; }
.achievement-scroll::-webkit-scrollbar { display:none; }
.achievement-unlock-overlay { /* modal for unlock celebration */ }
```

**JS State:**
```javascript
// localStorage: skillhunt_achievements
{
  earned: ["week_warrior", "first_blood", "ice_break", "first_hunt"],
  progress: {
    "sharpshooter": { current: 3, target: 5 },
    "ai_powered": { current: 1, target: 3 },
    "curator": { current: 4, target: 10 }
  }
}
```

**JS Functions:**
- `defineAchievements()` — returns array of all 12 achievement definitions
- `checkAchievementUnlocks()` — called after every action, checks if new achievements earned
- `unlockAchievement(id)` — triggers unlock animation, awards XP
- `renderAchievementRow()` — renders the scrollable row
- `shareAchievement(id)` — Telegram share (Pro only)

---

## FEATURE #5: 👻 GHOST COUNTER (Real-Time FOMO on Every Job)

**Priority:** #5 (This creates the ANXIETY that makes them check constantly)

### Psychological Mechanism
**Social proof + scarcity + loss aversion.** When you see "14 people are viewing this job right now" your brain interprets it as competition and scarcity. The mere presence of other interested parties makes the opportunity feel more valuable (social proof) and more urgent (scarcity). This is the same mechanism that makes booking.com's "3 people are looking at this hotel" so effective.

### Exact UX Flow

1. **Ghost Counter on Job Cards:** Every job card in the feed shows a subtle live indicator:

   ```
   👁️ 14 viewing · ⚡ 3 applied
   ```

   The numbers are simulated but feel real. They slowly increase over time for each job.

2. **"Viewing Now" Pulse:** A small pulsing green dot next to the viewer count, making it feel LIVE:
   ```css
   .ghost-pulse { width:6px; height:6px; border-radius:50%; background:var(--success); animation: ghostPulse 2s ease infinite; }
   @keyframes ghostPulse { 0%,100%{opacity:.4;transform:scale(1)} 50%{opacity:1;transform:scale(1.3)} }
   ```

3. **Hot Job Alert:** Jobs with 5+ viewers get a "🔥 Hot" badge. Jobs with applications closing soon show "⏰ Closing soon" with a countdown.

4. **Your Competition (Pro):** On job detail, Pro users see the existing competitor analysis enhanced with:
   - "Your rank: #4 out of 14 applicants" (already exists in `renderCompetitorAnalysis`)
   - NEW: "⚡ 2 new applicants since you viewed this job"
   - NEW: Activity graph showing when most applicants submitted (optimal timing)

### How It Creates Dependency
- **Constant urgency:** Every job feels like it's slipping away
- **Competition anxiety:** "I need to apply before more people do"
- **Checking behavior:** Users return to see if "their" jobs have more competitors
- **Premium insight value:** Pro users get actionable competitive data = higher close rate = Pro justifies itself

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Viewer count | "👁️ 14 viewing" | "👁️ 14 viewing · 📊 3 from your category" |
| Applicant count | Total only | Total + your rank |
| New applicant alerts | ❌ | ✅ "2 new since your last visit" |
| Optimal apply timing | ❌ | ✅ Best time graph |
| Hot job indicator | ✅ Basic 🔥 | ✅ + detailed heat score |

### HTML/CSS/JS Changes

**CSS:** New styles:
```css
.ghost-counter { display:flex; align-items:center; gap:4px; font-size:10px; color:var(--text-3); margin-top:6px; }
.ghost-pulse { width:6px; height:6px; border-radius:50%; background:var(--success); animation:ghostPulse 2s ease infinite; }
.hot-badge { font-size:9px; font-weight:700; padding:1px 6px; border-radius:var(--radius-full); background:rgba(224,108,117,.1); color:var(--danger); }
```

**JS:** Modify `renderJobCard()` to include ghost counter:
```javascript
// Simulated viewing counts based on job posted time + random seed
function getGhostCounters(job) {
  const seed = job.id * 17 + new Date().getHours();
  const viewers = 5 + (seed % 30); // 5-34 viewers
  const applicants = Math.floor(viewers * 0.25); // ~25% applied
  const isHot = viewers > 15;
  return { viewers, applicants, isHot };
}
```

---

## FEATURE #6: 💎 LOYALTY POINTS & REWARD SHOP

**Priority:** #6 (Long-term investment that compounds — can't walk away from accrued value)

### Psychological Mechanism
**Token economy + endowment effect + delayed gratification.** When users accumulate a currency that can be spent on real value, they develop a strong sense of ownership over their balance. 2,847 loyalty points feels like MONEY — you can't just delete the app and lose $28.47 in equivalent value. The reward shop creates goals to save toward (like a redemption arc), and the constant accrual creates a "never cash out" dynamic where the balance always feels too valuable to abandon.

### Exact UX Flow

1. **Loyalty Card** uses the existing `.loyalty-card` CSS — a beautiful gradient card in the More panel:

   ```
   ┌─────────────────────────────────┐
   │  💎 2,847                       │
   │  Loyalty Points                 │
   │  Next: Pro Day Pass (500 pts)   │
   │  ━━━━━━━━━━━━━░░░░░░░  85%     │
   └─────────────────────────────────┘
   ```

2. **Earning Points:**
   - Daily check-in: +5 pts
   - Complete all daily bounties: +30 pts (Free), +50 pts (Pro)
   - Apply to a job: +10 pts
   - Streak bonus (7-day): +50 pts
   - Achievement unlock: +25-100 pts (varies by badge tier)
   - Profile completeness: +20 pts (one-time)

3. **Reward Shop (tap card to open):**
   - 🎫 Pro Day Pass — 500 pts (24h of Pro features)
   - 🔥 Streak Freeze — 200 pts (protect 1 day)
   - 👁️ Client Insight Peek — 100 pts (see insights for 1 job)
   - 🤖 AI Cover Letter — 150 pts (1 AI-generated letter)
   - ⚡ Early Access for 1 Day — 300 pts
   - 🎨 Profile Theme — 750 pts (exclusive avatar ring color)
   - 💎 "Diamond" Level Skip — 5000 pts (jump to next Hunter Score level)

4. **Points Balance in Header:** A small 💎 icon with balance appears next to the user avatar in the greeting bar.

### How It Creates Dependency
- **Accrued value feels like money:** Can't abandon 2,847 points
- **Saving goals create stickiness:** "Just 200 more points for Pro Day Pass"
- **Frequent small rewards reinforce behavior:** +5 pts on check-in = micro-dopamine
- **Pro features become accessible:** Free users can TASTE Pro via points = conversion hook
- **Compound effect:** Long-term users have enormous balances = enormous switching cost

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Points per action | Base rate | 2x multiplier |
| Daily check-in | +5 pts | +10 pts |
| Bounty completion | +30 pts | +50 pts |
| Reward prices | Standard | 20% discount |
| Exclusive rewards | ❌ | ✅ Profile themes, leaderboard badges |
| Points expiration | Never | Never |

### HTML/CSS/JS Changes

**CSS:** Already exists! `.loyalty-card`, `.loyalty-points`, `.loyalty-label`, `.loyalty-next`. Add:
```css
.loyalty-balance-mini { font-size:11px; font-weight:700; color:var(--primary); display:inline-flex; align-items:center; gap:3px; }
.reward-item { display:flex; align-items:center; gap:12px; padding:12px; border-radius:var(--radius-sm); background:var(--bg-card); border:1px solid var(--border-soft); margin-bottom:8px; cursor:pointer; }
.reward-item:hover { border-color:var(--primary); }
.reward-ico { width:36px; height:36px; border-radius:8px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.reward-price { font-size:12px; font-weight:700; color:var(--primary); margin-left:auto; }
```

**JS State:**
```javascript
// localStorage: skillhunt_loyalty
{
  balance: 2847,
  totalEarned: 4230,
  totalSpent: 1383,
  history: [
    { date: "2025-01-15", action: "daily_checkin", amount: 5 },
    { date: "2025-01-15", action: "bounty_complete", amount: 30 },
    { date: "2025-01-14", action: "redeem:streak_freeze", amount: -200 }
  ]
}
```

**JS Functions:**
- `awardLoyaltyPoints(amount, reason)` — adds points + shows +N animation
- `spendLoyaltyPoints(amount, rewardId)` — validates balance, deducts, activates reward
- `renderLoyaltyCard()` — renders the gradient card
- `openRewardShop()` — full-screen overlay with reward items
- `activateReward(rewardId)` — applies the reward effect

---

## FEATURE #7: 📊 MARKET PULSE (Live Market Dashboard)

**Priority:** #7 (Creates the NEWS HABIT — like checking stock prices)

### Psychological Mechanism
**Information foraging theory + FOMO + identity reinforcement.** Freelancers naturally want to know "what's the market doing?" — it's their livelihood. By turning market data into a real-time feed of insights, we create the same checking habit as stock traders have with Bloomberg. The pulse also reinforces identity: "I check the SkillHunt Pulse every morning because I'm a serious freelancer who stays informed."

### Exact UX Flow

1. **Market Pulse Widget** on Feed page (collapsible):
   ```
   ┌─────────────────────────────────────┐
   │ 📊 Market Pulse          Today ↓    │
   │                                     │
   │ 🔥 AI/ML demand +42% this week     │
   │ 💰 Avg budget: $4,200 (+8%)        │
   │ ⚡ 23 new jobs in last 24h          │
   │ 📈 React Native trending ↑          │
   │ 🏆 Your category: TOP 3 hottest     │
   └─────────────────────────────────────┘
   ```

2. **Dynamic Market Data (simulated):**
   - Category demand changes (random walk, seeded by date)
   - Average budget trends (based on mock job data)
   - New job counts (simulated hourly)
   - Trending skills (rotates from skill pool)
   - User's category ranking (always slightly flattering)

3. **Weekly Market Summary (Pro):** A detailed weekly digest:
   - Category performance chart
   - Skills supply/demand ratio
   - Rate recommendations
   - "Your market position" percentile

4. **Market Alerts:** When a category surges, a push-style notification appears:
   ```
   🚀 AI/ML demand spiked +28% today! 5 new high-budget jobs posted.
   ```

### How It Creates Dependency
- **News habit:** Like checking stock prices or Hacker News
- **FOMO:** "What if my category is trending and I miss it?"
- **Identity:** "I stay on top of the market" = part of being a serious freelancer
- **Decision support:** Makes users feel the app helps them make CAREER decisions, not just find jobs

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Pulse widget | 3 data points | 5 data points |
| Weekly summary | ❌ | ✅ Full report |
| Trending skills | Top 3 | Top 10 + growth rates |
| Rate recommendations | ❌ | ✅ Personalized |
| Market alerts | Basic | Real-time + category-specific |

### HTML/CSS/JS Changes

**HTML:** Add pulse container in Feed:
```html
<div id="marketPulseContainer"></div>
```

**CSS:** New styles:
```css
.pulse-card { background:var(--bg-card); border-radius:var(--radius); padding:14px; border:1px solid var(--border-soft); margin-bottom:12px; box-shadow:var(--shadow); }
.pulse-header { display:flex; align-items:center; justify-content:space-between; margin-bottom:10px; }
.pulse-item { display:flex; align-items:center; gap:8px; padding:6px 0; font-size:12px; color:var(--text-2); }
.pulse-item-emoji { font-size:14px; }
.pulse-change { font-size:11px; font-weight:700; margin-left:auto; }
.pulse-change.up { color:var(--success); }
.pulse-change.down { color:var(--danger); }
```

**JS Functions:**
- `generateMarketPulse()` — creates daily market data from date seed
- `renderMarketPulse()` — renders the pulse widget
- `checkMarketAlerts()` — compares today vs yesterday, generates alerts

---

## FEATURE #8: 🏆 WEEKLY HUNTER LEADERBOARD

**Priority:** #8 (Social proof + competitive drive + status maintenance)

### Psychological Mechanism
**Social comparison theory + status anxiety + loss of rank.** People evaluate themselves relative to peers. A visible leaderboard creates both the DESIRE to climb (dopamine from ranking up) and the FEAR of falling (loss aversion from ranking down). Once someone reaches Top 10, they will do ANYTHING to stay there. The weekly reset creates recurring drama and fresh entry points.

### Exact UX Flow

1. **Leaderboard Tab** added as a 4th bottom nav position (replacing "More" which moves to a profile icon in the header):

   Wait — better approach: Leaderboard as a sub-screen accessible from the Hunter Score card. Tap the score ring → see score detail → "View Leaderboard" button.

2. **Leaderboard Display (uses existing CSS):**
   ```
   ┌──────────────────────────────────┐
   │ 🏆 Weekly Leaderboard            │
   │ Resets in: 4d 12h                │
   │                                  │
   │ 🥇 Мария К.    💎 4,230 pts     │
   │ 🥈 Дмитрий С.  💎 3,891 pts     │
   │ 🥉 Анна В.     💎 3,447 pts     │
   │ 4  Олег П.     💎 2,998 pts     │
   │ ─── You ──────────────────────   │
   │ 12 Александр   💎 1,847 pts  ↑3 │
   │ ──────────────────────────────── │
   │ 13 Елена Р.    💎 1,802 pts  ↓2 │
   └──────────────────────────────────┘
   ```

3. **Mock Users (20 simulated competitors):**
   Names, scores, and activity levels are generated from a seed. Scores change slightly each day to simulate a living leaderboard.

4. **Weekly Reset & Rewards:**
   - Top 3: Exclusive profile badge + 500 loyalty points
   - Top 10: 200 loyalty points
   - Top 50: 50 loyalty points
   - After reset, everyone starts fresh = new hope = continued engagement

5. **Rank Change Indicators:** ↑3 (green) or ↓2 (red) arrows show movement since yesterday.

### How It Creates Dependency
- **Status maintenance:** Being Top 10 = identity. You don't abandon a platform where you're ranked.
- **Competitive fire:** "I'm 50 points behind Anna — I can catch her"
- **Weekly drama:** Reset creates fresh narrative every week
- **Social proof:** Seeing others active normalizes and validates the platform

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Leaderboard visible | Top 20 only | Full rankings |
| Your rank shown | ✅ | ✅ + rank projection |
| Historical ranks | ❌ | ✅ Last 4 weeks |
| Weekly reward points | Base | 2x multiplier |
| "Challenge" feature | ❌ | ✅ Directly challenge a rival |

### HTML/CSS/JS Changes

**CSS:** Already exists! `.lb-your-rank`, `.lb-rank`, `.lb-rank.gold`, `.lb-rank.silver`, `.lb-rank.bronze`, `.lb-score-val` — all defined. Add:
```css
.rank-change { font-size:10px; font-weight:700; }
.rank-change.up { color:var(--success); }
.rank-change.down { color:var(--danger); }
.leaderboard-reset { font-size:11px; color:var(--text-3); text-align:center; padding:8px; }
```

**JS State:**
```javascript
// localStorage: skillhunt_leaderboard
{
  weekKey: "2025-W03",
  userRank: 12,
  lastRank: 15,
  viewedThisWeek: true
}
```

**JS Functions:**
- `generateLeaderboard()` — creates 20 mock users with seeded scores
- `calculateUserRank()` — inserts user into leaderboard
- `renderLeaderboard()` — renders the leaderboard list
- `checkWeeklyReset()` — called on init, checks if new week

---

## FEATURE #9: 🕵️ INTELLIGENCE FEED (Your Unfair Advantage)

**Priority:** #9 (The PRO KILLER FEATURE — the thing that makes $5/mo feel like stealing)

### Psychological Mechanism
**Information asymmetry + exclusivity + strategic advantage.** When Pro users feel they have information that Free users don't, the subscription stops feeling like an expense and starts feeling like a WEAPON. "I know things others don't" is one of the most powerful psychological states. This transforms Pro from "nice features" to "competitive advantage I'd be stupid to give up."

### Exact UX Flow

1. **Intelligence Feed** appears as a subtle card in the Feed for Pro users:

   ```
   ┌─────────────────────────────────────┐
   │ 🕵️ Intel · Pro Exclusive            │
   │                                     │
   │ ⚡ Client "Дмитрий К." typically    │
   │    responds within 2h (apply now!)  │
   │                                     │
   │ 💡 Budget insight: "ML-модель" job  │
   │    usually pays at max range ($8K)  │
   │                                     │
   │ 🎯 Apply before 6pm for best        │
   │    response rate (based on history) │
   └─────────────────────────────────────┘
   ```

2. **Intelligence Types:**
   - ⚡ Client Response Patterns: "This client typically responds in 2h" / "This client takes 3-5 days"
   - 💡 Budget Insights: "This client usually pays at budget max" / "Average accepted bid: $4.2K"
   - 🎯 Timing Intel: "Best apply time for this category: 9-11am"
   - 🔍 Competitor Intel: "12 applicants so far — lower than average for this budget"
   - 📈 Market Intel: "Demand for React Native grew 34% this month"

3. **For Free Users:** They see a BLURRED version of the Intel card:
   ```
   ┌─────────────────────────────────────┐
   │ 🕵️ Intel · 🔒 Pro Exclusive         │
   │ ████████████████████████████████     │
   │ ████████████████████████████         │
   │ ██████████████████████████████████   │
   │                                     │
   │ [Unlock Pro to see intel →]         │
   └─────────────────────────────────────┘
   ```

### How It Creates Dependency
- **Information is power:** Knowing client behavior = winning more contracts
- **Exclusivity reinforcement:** "I see what others can't" = identity
- **Practical value:** Directly leads to better application outcomes
- **Fear of blindness:** Canceling Pro = going back to applying BLIND = unacceptable

### Pro vs Free Difference
This IS the Pro/Free difference. Free sees blurred intel. Pro sees everything.

### HTML/CSS/JS Changes

**CSS:**
```css
.intel-card { background:var(--bg-card); border-radius:var(--radius); padding:14px; border:1px solid rgba(108,123,212,.2); margin-bottom:12px; position:relative; overflow:hidden; }
.intel-card::before { content:''; position:absolute; top:0; left:0; right:0; height:3px; background:linear-gradient(90deg,var(--primary),var(--lavender)); }
.intel-header { display:flex; align-items:center; gap:8px; margin-bottom:10px; font-size:13px; font-weight:700; color:var(--text); }
.intel-item { display:flex; align-items:flex-start; gap:8px; padding:6px 0; font-size:12px; color:var(--text-2); line-height:1.4; }
.intel-emoji { font-size:14px; flex-shrink:0; margin-top:1px; }
.intel-blur { filter:blur(4px); user-select:none; pointer-events:none; }
.intel-unlock { text-align:center; padding:12px; }
.intel-unlock-btn { display:inline-flex; align-items:center; gap:6px; padding:8px 20px; background:var(--primary); color:#fff; border-radius:var(--radius-full); font-size:13px; font-weight:700; cursor:pointer; }
```

**JS Functions:**
- `generateIntelForJob(job)` — creates simulated intelligence data
- `renderIntelCard(job)` — renders intel (blurred for Free)
- `renderIntelFeed()` — renders intel for top 3 relevant jobs

---

## FEATURE #10: 🎨 SKILL RADAR & GAP ANALYSIS (Your Growth Map)

**Priority:** #10 (Long-term identity investment — makes the app your career GPS)

### Psychological Mechanism
**Self-improvement drive + visualization bias + identity commitment.** When people see a visual representation of their skills vs market demand, it creates a powerful "gap" that motivates action. The radar chart makes strengths feel REAL (confirmation) and weaknesses feel URGENT (gap). Over time, as users invest in filling gaps through the app's guidance, the radar becomes a documented GROWTH STORY that they can't walk away from.

### Exact UX Flow

1. **Skill Radar** accessible from the More panel → Skills section (enhanced):

   ```
   ┌─────────────────────────────────┐
   │ 🎯 Your Skill Radar             │
   │                                 │
   │      [Radar Chart SVG]         │
   │      Your Skills vs Market      │
   │                                 │
   │ 🟢 Python       92% (HOT)      │
   │ 🟢 TensorFlow   85%            │
   │ 🟡 Docker       45% (DEMAND↑)  │
   │ 🔴 Kubernetes   20% (GAP)      │
   │ 🔴 RUST         5%  (EMERGING) │
   │                                 │
   │ 💡 Add Kubernetes to match 34%  │
   │    more jobs (+$2.1K avg)       │
   └─────────────────────────────────┘
   ```

2. **Radar Chart:** SVG radar/pentagon chart showing:
   - Your skill levels (filled area)
   - Market demand levels (outline)
   - Overlap = employability score

3. **Gap Analysis Recommendations:**
   - "Add Kubernetes → match 34% more jobs"
   - "Your Python is in top 5% → highlight in applications"
   - "React Native demand surged → consider adding"

4. **Growth Timeline (Pro):** Track how your radar has changed over time:
   - "Your Docker skill grew from 20% → 45% this month"
   - Visual diff of radar charts (this month vs last month)

### How It Creates Dependency
- **Career GPS:** The app isn't just finding jobs — it's GUIDING YOUR CAREER
- **Documented growth:** "Look how much I've improved" = emotional investment
- **Gap motivation:** An incomplete radar is psychologically uncomfortable
- **Personalization deepens:** More data = better recommendations = can't start over

### Pro vs Free Difference
| Aspect | Free | Pro |
|--------|------|-----|
| Radar chart | ✅ Static | ✅ Animated |
| Market demand overlay | ❌ | ✅ |
| Gap recommendations | 1 tip | Full analysis |
| Growth timeline | ❌ | ✅ Monthly history |
| Salary impact estimates | ❌ | ✅ "+$2.1K avg" |

### HTML/CSS/JS Changes

**CSS:**
```css
.radar-card { background:var(--bg-card); border-radius:var(--radius); padding:16px; border:1px solid var(--border-soft); margin-bottom:12px; }
.radar-svg { width:100%; max-width:220px; margin:0 auto; display:block; }
.skill-gap-item { display:flex; align-items:center; gap:8px; padding:8px 0; border-bottom:1px solid var(--border-soft); font-size:12px; }
.skill-gap-item:last-child { border-bottom:none; }
.skill-gap-bar { height:4px; border-radius:2px; flex:1; background:var(--bg-input); overflow:hidden; }
.skill-gap-fill { height:100%; border-radius:2px; transition:width .7s cubic-bezier(.22,1,.36,1); }
.skill-gap-fill.green { background:var(--success); }
.skill-gap-fill.yellow { background:var(--warning); }
.skill-gap-fill.red { background:var(--danger); }
.skill-recommendation { padding:10px; background:var(--primary-light); border-radius:var(--radius-sm); font-size:12px; color:var(--primary); margin-top:10px; }
```

**JS Functions:**
- `generateRadarData()` — creates radar chart coordinates from user skills
- `getMarketDemand(skill)` — returns simulated demand score
- `renderSkillRadar()` — renders SVG radar chart + gap list
- `getSkillRecommendations()` — analyzes gaps, returns sorted recommendations

---

## IMPLEMENTATION PRIORITY & DEPENDENCY MAP

```
PHASE 1 (Week 1) — The Daily Hook:
├── Feature #1: Daily Streak ─────────── foundation, all others reference it
├── Feature #2: Hunter Score ─────────── XP system, all others award XP
└── Feature #3: Daily Bounties ───────── daily engagement driver

PHASE 2 (Week 2) — The Collection:
├── Feature #4: Achievement Badges ───── depends on Streak + Score + Bounties
└── Feature #5: Ghost Counter ────────── quick win, modifies existing renderJobCard

PHASE 3 (Week 3) — The Investment:
├── Feature #6: Loyalty Points ───────── depends on all Phase 1+2 features
└── Feature #7: Market Pulse ─────────── standalone, adds news habit

PHASE 4 (Week 4) — The Identity:
├── Feature #8: Leaderboard ──────────── depends on Hunter Score
├── Feature #9: Intelligence Feed ────── Pro killer feature
└── Feature #10: Skill Radar ─────────── long-term career investment
```

---

## FEED PAGE LAYOUT (After All Features)

The Feed page transforms from a flat job list into an engaging dashboard:

```
┌──────────────────────────────────┐
│ [Avatar] Добрый день,            │ ← Greeting (existing)
│ Александр ✓Pro    ● Online       │
├──────────────────────────────────┤
│ 🔥 7-day streak                  │ ← Feature #1: Streak
│ [●][●][●][●][●][●][○][○]        │
├──────────────────────────────────┤
│ 🎯 Hunter Score: 847             │ ← Feature #2: Score Ring
│ [═══════════░░░░] Silver         │
├──────────────────────────────────┤
│ 📋 Today's Bounties      2/4    │ ← Feature #3: Bounties
│ ✅ Open app  ✅ View 3 jobs      │
│ ⬜ Apply   ⬜ Save 2 jobs        │
├──────────────────────────────────┤
│ 🏅 Achievements (4/12)          │ ← Feature #4: Badges
│ [🔥][📋][❄️][🎯][🔒][🔒]        │
├──────────────────────────────────┤
│ 📊 Market Pulse                  │ ← Feature #7: Pulse
│ AI/ML demand +42% · Avg $4.2K    │
├──────────────────────────────────┤
│ 🕵️ Intel · Pro                   │ ← Feature #9: Intel
│ Client responds in 2h...         │
├──────────────────────────────────┤
│ Pro Trial Bar                    │ ← Existing
├──────────────────────────────────┤
│ 3 заказа совпадают на 85%+      │ ← Existing Hero Card
├──────────────────────────────────┤
│ [All][AI/ML][Design][Dev]...     │ ← Existing Category Tabs
│                                  │
│ ┌──────────────────────────────┐ │
│ │ Job Card 1                   │ │ ← Enhanced with Ghost Counter
│ │ 👁️ 14 viewing · ⚡ 3 applied │ │ ← Feature #5
│ └──────────────────────────────┘ │
│ ┌──────────────────────────────┐ │
│ │ Job Card 2                   │ │
│ │ ...                          │ │
│ └──────────────────────────────┘ │
└──────────────────────────────────┘
```

---

## XP & LOYALTY POINT ECONOMY

### XP Earning Table
| Action | Free XP | Pro XP (1.5x) |
|--------|---------|----------------|
| Daily check-in | 10 | 15 |
| View job detail | 5 | 8 |
| Save a job | 5 | 8 |
| Apply to a job | 20 | 30 |
| Use AI cover | 15 | 23 |
| Complete all bounties | 30 | 45 |
| 7-day streak bonus | 50 | 75 |
| Achievement unlock (bronze) | 25 | 38 |
| Achievement unlock (silver) | 50 | 75 |
| Achievement unlock (gold) | 100 | 150 |
| Weekly leaderboard top 10 | 50 | 75 |

### Loyalty Points Earning Table
| Action | Free Pts | Pro Pts (2x) |
|--------|----------|---------------|
| Daily check-in | 5 | 10 |
| Complete all bounties | 30 | 50 |
| Apply to a job | 10 | 20 |
| 7-day streak | 50 | 100 |
| Achievement unlock | 25 | 50 |
| Profile complete | 20 | 40 |

### Reward Shop Prices
| Reward | Pts | Pro Discount |
|--------|-----|---------------|
| Streak Freeze | 200 | 160 |
| Client Insight Peek | 100 | 80 |
| AI Cover Letter | 150 | 120 |
| Pro Day Pass (24h) | 500 | 400 |
| Early Access (1 day) | 300 | 240 |
| Profile Theme | 750 | 600 |
| Level Skip | 5000 | 4000 |

---

## KEY METRICS TO TRACK (Simulated in App)

1. **DAU/MAU ratio** — Target: 0.4+ (40% of monthly users come daily)
2. **Streak length distribution** — Target: median 7+ days
3. **Bounty completion rate** — Target: 60%+ complete all daily bounties
4. **Hunter Score growth** — Target: +100 XP/week average
5. **Achievement unlock rate** — Target: 2+ per user per month
6. **Pro conversion from Streak Freeze** — Target: 15% of Free users who see freeze prompt
7. **Loyalty point balance** — Target: 1000+ pts average (too valuable to abandon)
8. **Leaderboard check frequency** — Target: 3+ times per week per user

---

## THE PSYCHOLOGICAL FLYWHEEL

```
Open app (streak anxiety)
    → Complete bounties (variable reward)
        → Earn XP (progress addiction)
            → See ghost counters (FOMO)
                → Apply to jobs (real utility)
                    → Check leaderboard (status)
                        → Earn achievements (collection)
                            → Check market pulse (news habit)
                                → See intel (Pro advantage)
                                    → Can't cancel Pro (fear of blindness)
                                        → Come back tomorrow (streak)
```

This is a self-reinforcing loop. Each feature feeds the next. The user never reaches a "done" state — there's always another bounty, another point, another badge, another rank to maintain.

---

## WHAT MAKES THIS DIFFERENT FROM "DARK PATTERNS"

These features are NOT manipulative because:
1. **They align with user goals** — Freelancers WANT to find jobs, improve skills, and earn more
2. **The habits they build are genuinely useful** — Checking the market daily = being informed
3. **Pro features deliver real value** — Intel that helps you win contracts = worth $5/mo
4. **No deception** — Ghost counters are simulated but represent real market dynamics
5. **User agency** — Every engagement is opt-in; bounties can be ignored; streaks can be frozen

The key insight: **The best retention strategies don't TRICK users into staying — they make staying genuinely beneficial, then make the benefits VISIBLE and MEASURABLE.**
