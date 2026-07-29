# UI Patterns — Structure + Design System

⚠️ Two independent decisions happen here, in this order:

1. **STRUCTURE** — which navbar/footer/card layout fits the app type
   (Private / Blog / SaaS / Education). Table below, unchanged from
   before.
2. **DESIGN SYSTEM** — which visual personality (fonts, colors, radius,
   shadows) the whole project uses. Chosen based on the project's actual
   vibe/industry, NOT tied to app type. A blog and a SaaS dashboard can
   both use the "Editorial" system; two SaaS dashboards can use two
   completely different systems.

Never skip step 2 and fall back to defaults. A project with no design
system chosen is a project that will look like every other AI-generated
app — flat gray/white, Inter font, `rounded-lg`, indigo-600, drop
shadows on every card. That combination is banned outright (see
"Banned Defaults" below), not just discouraged.

---

## Banned Defaults (never use these together — this IS the generic look)

- Font: Inter, as the only font on the page
- Primary color: `indigo-600` or `blue-600` with no other named color
- Radius: `rounded-lg` used uniformly on every element with no variation
- Shadow: plain `shadow` or `shadow-md` on every single card with no
  distinction between elevation levels
- A purple-to-indigo gradient hero background
- Generic Heroicons-style thin-stroke icons as the *only* visual accent

Any ONE of these alone is fine. All of them together, applied uniformly
across a whole project, is the exact "AI slop" fingerprint researchers
and users now recognize on sight. The Design Systems below are built
specifically to avoid this combination.

---

## Design Quality Bar (applies to EVERY generated app, every Design System)

Choosing a good Design System isn't enough on its own — sloppy execution
of a good system still looks bad. Check all six of these before
considering a build done, regardless of which system was chosen.

### 1. Typographic Scale — never one size everywhere

Use distinct sizes for distinct roles, not `text-lg`/`font-semibold`
repeated on a hero AND a card title:

- **Hero/display**: `text-5xl md:text-6xl font-display font-bold leading-[1.05]`
- **Section heading**: `text-3xl md:text-4xl font-display font-semibold`
- **Card/subheading title**: `text-xl font-semibold`
- **Body text**: `text-base leading-relaxed`
- **Caption/meta**: `text-sm text-[var(--ink-muted)]`

A page with only 1-2 distinct text sizes on it has no hierarchy and
will look flat no matter how good the color palette is.

### 2. Spacing Rhythm — one consistent scale, not arbitrary values

Stick to an 8px-based scale throughout: `gap-2` (8px), `gap-4` (16),
`gap-6` (24), `gap-8` (32), `gap-12` (48), `gap-16` (64), `gap-24` (96
— section breaks only). Major/hero sections get generous vertical
padding (`py-24 md:py-32`); dense components (nav, table rows) stay
tight (`py-4`/`py-6`). Don't mix odd one-off values like `pt-5 pb-11`
picked ad hoc — every spacing value should trace back to this scale.

### 3. Real Content — never literal placeholder filler

Never output "Lorem ipsum dolor sit amet," "Sample text goes here," or
"Feature One / Feature Two / Feature Three." Write plausible,
subject-specific placeholder content instead:

- Essay portfolio: real-sounding titles ("The Quiet Cost of
  Convenience," "On Being Late to Everything") with 2-3 sentence
  excerpts that actually sound like an essay opening, not filler.
- SaaS features: plausible, specific feature names and one-sentence
  benefits tied to the actual product, not generic numbered labels.
- Any listing (products, courses, team members): specific-sounding
  names/titles, not "Item 1," "Item 2."

If the person's prompt doesn't give enough detail to invent plausible
content, infer from the domain — a "task manager for freelancers"
justifies invented task names like "Invoice Acme Corp" or "Follow up
on contract," not "Task 1."

### 4. Image Treatment — every image is styled with intent

- Fixed aspect ratio per content type: `aspect-video` for article/post
  covers, `aspect-square` for avatars/thumbnails — always paired with
  `object-cover`, never a bare fixed height that risks awkward cropping.
- Text-over-image needs a gradient scrim for legibility:
  `absolute inset-0 bg-gradient-to-t from-black/60 to-transparent`.
- Interactive image cards get a subtle hover treatment:
  `overflow-hidden` on the container, `group-hover:scale-105
  transition-transform duration-300` on the image itself.
- Never leave a bare `<img>` with no rounding, fit, or hover treatment
  sitting inside an otherwise-styled card.

### 5. Micro-interactions — every interactive element responds

- Every link, button, and card needs both a `hover:` AND a `focus:`
  state — hover alone fails keyboard/accessibility and feels
  incomplete.
- Every hover-affected element needs a `transition-colors duration-200`
  (or `transition-all` when multiple properties change) — an instant
  color snap with no transition reads as cheap.
- Focus rings for accessibility and polish:
  `focus:outline-none focus:ring-2 focus:ring-[var(--brand)]
  focus:ring-offset-2`.
- Buttons get a subtle press state: `active:scale-[0.98]`.
- Cards in a grid get a subtle lift on hover:
  `hover:-translate-y-0.5 transition-transform`, paired with an
  increased shadow/glow where the Design System uses one.

### 6. Design Self-Check — run before returning the build

- [ ] No Banned Default combination present anywhere (Inter-only +
      indigo-600 + uniform `rounded-lg` + plain `shadow`, together)
- [ ] At least 3 distinct type sizes in use with clear hierarchy — not
      everything `text-base` or `text-lg`
- [ ] All spacing traces to the 8px-based scale, no arbitrary odd values
- [ ] All placeholder content is specific/plausible to the subject —
      zero literal "Lorem ipsum" or "Sample Text"
- [ ] Every image has a fixed aspect ratio + `object-cover`, styled
      with intent, not a bare `<img>` tag
- [ ] Every interactive element has `hover:`, `focus:`, and a
      `transition-*` class
- [ ] Every color/font/radius/shadow class references the chosen
      Design System's CSS variables — no hardcoded indigo/gray/
      `rounded-lg` leftover from the structural reference examples below

---

## Structure Selection Table (unchanged)

| App Type | Footer | Navbar | Card |
|----------|--------|--------|------|
| Private / Admin-Only / Staff Records / Internal | Footer 1A/1B | Navbar 1A/1B | Card 1A/1B |
| Public Blog / Content / Read-Only / Articles | Footer 2A/2B | Navbar 2A/2B | Card 2A/2B |
| Public Full CRUD / SaaS / Dashboard / User Accounts | Footer 3A/3B | Navbar 3A/3B | Card 3A/3B |
| Education / School / LMS / CBT / Student Portal | Footer 4A/4B | Navbar 4A/4B | Card 4A/4B |
| Data-heavy Dashboard / Analytics / Admin Console | Sidebar Shell (Section 5) — no navbar/footer | — | Card 5A/5B |
| Game / Quiz / Coding Exercise / Interactive Challenge | HUD Shell (Section 6) — no navbar/footer | — | Card 6A/6B |

**Data-heavy Dashboard vs. Public SaaS (row 3):** if the app's PRIMARY
surface is charts/tables/metrics viewed constantly by a logged-in user
(analytics, admin console, ops dashboard) → use the Section 5 Sidebar
Shell instead of Navbar 3. If it's a SaaS product where the dashboard
is just one of several pages alongside marketing/settings/billing →
Navbar 3 is still right, and individual dashboard PAGES can still use
Card 5A/5B for stat displays.

**Game/Quiz trigger words:** game, quiz, coding exercise, interactive
challenge, puzzle, timed test, practice problem, tic-tac-toe/hangman/
memory-match style mini-games. Use the Section 6 HUD Shell — these
should NOT get a normal navbar/footer at all; full chrome breaks
immersion and wastes screen space on what's usually a small, focused
interaction.

**If the app has ANY public-facing pages, use Footer/Navbar/Card 2, 3, or
4 — NOT the Private (1) set.**

⚠️ CRITICAL — AUTH-DEPENDENT LINKS: Some navbar variants contain
`{% url 'login' %}`, `{% url 'logout' %}`, or `{% url 'signup' %}`.
These only exist if you are ALSO generating a real authentication
system in this build. For admin-managed CRUD apps — the default unless
the user explicitly requests public self-service signup/login — use a
plain `<a href="/admin/">Admin</a>` link instead. A stray
`{% url 'login' %}` tag with no matching URL definition crashes the
page with `NoReverseMatch` the instant it renders.

---

## Design System Selection

⚠️ TOKEN-EFFICIENCY REQUIREMENT: Do NOT reproduce a Design System's full
CSS variable block inline in every build — this is the single biggest
cause of truncated/incomplete AI responses. Each system is pre-built as
a static CSS file. Emit ONE line referencing it instead of the ~20-line
`<style>` block:

```html
<link rel="stylesheet" href="{% static 'design_systems/editorial.css' %}">
```

File names, one per system: `editorial.css`, `technical-mono.css`,
`warm-soft.css`, `brutalist.css`, `modern-bold.css`. Still include the
matching Google Fonts `<link>` (that part is short and varies too much
to templatize). Only the CSS variables + base rules move to the static
file — never regenerate that block by hand.

Pick ONE based on the project's actual subject matter and tone — not
randomly, not always the same one. Rough guide:

| Vibe / Industry signal | Design System |
|---|---|
| Content, writing, publications, personal brand, portfolio, editorial | **A — Editorial** |
| Tech tools, internal dashboards, admin systems, data-heavy, engineering | **B — Technical Mono** |
| Youth-facing, wellness, community, food, lifestyle, friendly products | **C — Warm Soft** |
| Print-poster, zine, retro-web, intentionally raw/anti-corporate | **D — Brutalist** |
| Modern SaaS, startups, events, product launches — bold but sleek, not raw | **E — Modern Bold** |
| Premium/luxury, high-end services, boutique brands, exclusivity | **G — Midnight Luxury** |
| Developer tools, technical docs, code-adjacent, restrained/professional dark | **H — Dark Minimal** |
| Genuinely unsure / nothing fits | Default to **A — Editorial** — it's the safest broad fit, never Inter/indigo defaults |

⚠️ Do not confuse "bold" with "brutalist." Brutalist (D) is a specific
retro/print-poster aesthetic — hard offset shadows, flat primary
colors, thick borders. It reads as raw and dated ON PURPOSE. If the
request is for a modern startup/product that should feel confident and
current (not retro), use **E — Modern Bold** instead, even if the
person's wording literally says "bold," "loud," or "impossible to
ignore" — those words describe the desired IMPACT, not the Brutalist
aesthetic specifically.

Each system below defines: Google Fonts import, CSS variables (inject
in `<head>` inside a `<style>` block), and how to reference them in
Tailwind via arbitrary-value syntax (`bg-[var(--brand)]`,
`rounded-[var(--radius-md)]`, etc.) since the Tailwind CDN build has no
custom config file.

---

### Design System A — Editorial

Serif display type against a warm, paper-like background. Confident,
calm, content-forward. Avoids every banned default: no Inter, no
indigo, no uniform rounded-lg.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --font-display: 'Fraunces', serif;
    --font-body: 'Work Sans', sans-serif;
    --bg: #FBF7F0;
    --surface: #FFFFFF;
    --ink: #211D1A;
    --ink-muted: #6B655D;
    --brand: #7A4A2B;
    --brand-hover: #613A22;
    --accent: #B5542C;
    --border: #E5DDD0;
    --radius-sm: 2px;
    --radius-md: 4px;
    --shadow-card: 0 1px 2px rgba(33,29,26,0.06), 0 1px 1px rgba(33,29,26,0.04);
  }
  body { font-family: var(--font-body); background: var(--bg); color: var(--ink); }
  h1, h2, h3, .font-display { font-family: var(--font-display); }
</style>
```

Usage pattern in components: swap `bg-white` -> `bg-[var(--surface)]`,
`bg-indigo-600` -> `bg-[var(--brand)]`, `text-gray-900` ->
`text-[var(--ink)]`, `text-gray-500` -> `text-[var(--ink-muted)]`,
`rounded-lg` -> `rounded-[var(--radius-md)]`, `shadow` ->
`shadow-[var(--shadow-card)]`, headings get `font-display` class added.

---

### Design System B — Technical Mono

Dense, dark, data-forward. Monospace for numbers/labels, sharp corners,
thin borders instead of soft shadows.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=IBM+Plex+Sans:wght@400;500;600&display=swap" rel="stylesheet">
<style>
  :root {
    --font-mono: 'IBM Plex Mono', monospace;
    --font-body: 'IBM Plex Sans', sans-serif;
    --bg: #0B0E11;
    --surface: #14181D;
    --ink: #E6E8EA;
    --ink-muted: #8A9199;
    --brand: #3DDC97;
    --brand-hover: #2FBF82;
    --accent: #F2C94C;
    --border: #262B31;
    --radius-sm: 0px;
    --radius-md: 2px;
    --shadow-card: none;
  }
  body { font-family: var(--font-body); background: var(--bg); color: var(--ink); }
  .font-mono, .stat-value { font-family: var(--font-mono); }
</style>
```

Usage pattern: cards use `border border-[var(--border)]` INSTEAD of
shadow (`--shadow-card: none`), numeric stat values get `font-mono`
class, radius stays near-0 throughout (`rounded-[var(--radius-sm)]`),
`bg-white`/`bg-gray-50` -> `bg-[var(--surface)]`.

---

### Design System C — Warm Soft

Friendly, rounded, approachable. Generous radius, soft colored shadows
(not gray), pastel-adjacent palette.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Quicksand:wght@500;600;700&family=Nunito+Sans:wght@400;600;700&display=swap" rel="stylesheet">
<style>
  :root {
    --font-display: 'Quicksand', sans-serif;
    --font-body: 'Nunito Sans', sans-serif;
    --bg: #FFF8F3;
    --surface: #FFFFFF;
    --ink: #3D2E26;
    --ink-muted: #8C7A70;
    --brand: #FF6B4A;
    --brand-hover: #E85535;
    --accent: #4AB8A1;
    --border: #FBE4D6;
    --radius-sm: 12px;
    --radius-md: 20px;
    --shadow-card: 0 8px 20px -6px rgba(255,107,74,0.18);
  }
  body { font-family: var(--font-body); background: var(--bg); color: var(--ink); }
  h1, h2, h3, .font-display { font-family: var(--font-display); }
</style>
```

Usage pattern: everything gets generous radius
(`rounded-[var(--radius-md)]` on cards, not the thin default), shadows
use the brand-tinted `--shadow-card` instead of gray, buttons/icons use
`--brand` (a warm coral, not indigo).

---

### Design System D — Brutalist

High contrast, thick borders, hard offset shadows (no blur), zero
radius. Built to stand out, not blend in.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Archivo:wght@400;600;800&display=swap" rel="stylesheet">
<style>
  :root {
    --font-display: 'Archivo', sans-serif;
    --font-mono: 'Space Mono', monospace;
    --bg: #F5F3EF;
    --surface: #FFFFFF;
    --ink: #0A0A0A;
    --ink-muted: #52504C;
    --brand: #FFDE00;
    --brand-ink: #0A0A0A;
    --accent: #0047FF;
    --border: #0A0A0A;
    --radius-sm: 0px;
    --shadow-hard: 4px 4px 0 0 #0A0A0A;
  }
  body { font-family: var(--font-body, sans-serif); background: var(--bg); color: var(--ink); }
  h1, h2, h3, .font-display { font-family: var(--font-display); font-weight: 800; }
  .brutal-card { border: 2px solid var(--border); box-shadow: var(--shadow-hard); }
</style>
```

Usage pattern: cards get `class="brutal-card"` instead of
`shadow rounded-lg` — a solid 2px black border plus a hard offset
shadow with NO blur. Buttons use `bg-[var(--brand)]
text-[var(--brand-ink)] border-2 border-[var(--border)]`, never a soft
gradient. Radius is 0 everywhere.

---

### Design System E — Modern Bold

Dark mode, a single vibrant gradient accent, huge confident display
type, soft glow instead of hard shadow. This is the "modern startup"
look — Linear/Vercel/Stripe territory — not print-poster brutalism.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500&display=swap" rel="stylesheet">
<style>
  :root {
    --font-display: 'Space Grotesk', sans-serif;
    --font-body: 'Inter', sans-serif;
    --bg: #0A0A0F;
    --surface: #15151C;
    --surface-hover: #1D1D26;
    --ink: #F2F2F7;
    --ink-muted: #8E8E9E;
    --brand: #7C5CFF;
    --brand-2: #22D3EE;
    --border: #26262F;
    --radius-md: 14px;
    --radius-lg: 20px;
    --shadow-glow: 0 0 40px -8px rgba(124,92,255,0.35);
  }
  body { font-family: var(--font-body); background: var(--bg); color: var(--ink); }
  h1, h2, h3, .font-display { font-family: var(--font-display); }
  .gradient-text {
    background: linear-gradient(90deg, var(--brand), var(--brand-2));
    -webkit-background-clip: text; background-clip: text; color: transparent;
  }
  .gradient-border {
    position: relative; background: var(--surface);
  }
  .gradient-border::before {
    content: ''; position: absolute; inset: 0; padding: 1px; border-radius: inherit;
    background: linear-gradient(135deg, var(--brand), var(--brand-2));
    -webkit-mask: linear-gradient(#000 0 0) content-box, linear-gradient(#000 0 0);
    -webkit-mask-composite: xor; mask-composite: exclude;
  }
</style>
```

Note: this system only makes sense on a **dark** background — don't
apply `--bg`/`--surface` here to a light-mode page, the glow shadow and
gradient-clip text need the dark backdrop to read correctly.

Usage pattern: hero headline gets `class="font-display gradient-text"`
for the key phrase, cards use `bg-[var(--surface)] rounded-[var(--radius-lg)]`
with `hover:bg-[var(--surface-hover)]` (no border needed, or use
`gradient-border` class sparingly on 1-2 hero elements only — not every
card, or the effect stops feeling special), buttons use a solid
`bg-[var(--brand)]` with `shadow-[var(--shadow-glow)]` on hover, never
a flat shadow.

---

### Design System G — Midnight Luxury

Premium, elegant dark. Warm gold accent against near-black, serif
display type. For high-end/boutique/exclusive-feeling brands — the
opposite mood of Modern Bold's tech-startup energy.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Manrope:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{% static 'design_systems/midnight-luxury.css' %}">
```

Usage pattern: generous negative space, thin gold borders used
sparingly (not on every element), headline type set larger and looser
(`tracking-wide`) than other systems — restraint is the point, not
density.

---

### Design System H — Dark Minimal

Restrained, monochrome dark with exactly one accent color. GitHub/
Vercel/developer-tool territory — for technical docs, code-adjacent
products, or any dark-mode request that should read as professional
and quiet rather than dramatic.

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{% static 'design_systems/dark-minimal.css' %}">
```

Usage pattern: almost no shadows (`--shadow-card: none`, matches
Technical Mono's approach), a single blue accent (`--brand`) used
sparingly for links/primary actions only, borders do the separation
work instead of elevation.

---

## Applying a Design System to the Structural Templates

The navbar/footer/card examples below (from the original structure
table) stay as reference for LAYOUT — but every hardcoded color/radius/
shadow class in them must be swapped for the chosen Design System's
variables before use. Do not ship them with the literal
`bg-indigo-600`/`rounded-lg`/`shadow` classes still in place.

**Example — Card 1A (Stat Card), rewritten for Design System B (Technical Mono):**

```html
<div class="bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-sm)] p-6 flex items-center gap-4">
    <div class="bg-[var(--brand)]/10 text-[var(--brand)] rounded-[var(--radius-sm)] p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2a4 4 0 014-4h3m0 0l-3-3m3 3l-3 3M4 7h6m-6 4h6m-6 4h6" />
        </svg>
    </div>
    <div>
        <p class="text-sm text-[var(--ink-muted)]">Total Records</p>
        <p class="text-2xl font-mono text-[var(--ink)]">{{ total_count }}</p>
    </div>
</div>
```

**Same Card 1A, rewritten for Design System D (Brutalist):**

```html
<div class="brutal-card bg-[var(--surface)] p-6 flex items-center gap-4">
    <div class="bg-[var(--brand)] text-[var(--brand-ink)] border-2 border-[var(--border)] p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2a4 4 0 014-4h3m0 0l-3-3m3 3l-3 3M4 7h6m-6 4h6m-6 4h6" />
        </svg>
    </div>
    <div>
        <p class="text-sm font-mono uppercase tracking-wide text-[var(--ink-muted)]">Total Records</p>
        <p class="text-2xl font-display font-extrabold text-[var(--ink)]">{{ total_count }}</p>
    </div>
</div>
```

Apply this same substitution logic to every navbar, footer, and card
variant in the structure section (kept below, unchanged as layout
reference) — never ship the raw indigo/gray version once a Design
System has been chosen.

---

# Structural Reference (layout only — restyle per Design System above)

# 1. Private / Admin-Only System

## Footer 1A: Simple

```html
<footer class="mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-6 text-center text-sm">
        &copy; {% now "Y" %} {{ app_name }}. Internal use only. All rights reserved.
    </div>
</footer>
```

## Footer 1B: With System Links

```html
<footer class="mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-sm">&copy; {% now "Y" %} {{ app_name }}. Internal use only.</p>
        <div class="flex gap-6 text-sm">
            <a href="/admin/" class="hover:opacity-70 transition">Admin Panel</a>
            <a href="#" class="hover:opacity-70 transition">Support</a>
            <a href="#" class="hover:opacity-70 transition">System Status</a>
        </div>
    </div>
</footer>
```

## Navbar 1A: Simple Bar

```html
<nav class="sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-display font-bold">{{ app_name }}</a>
            <div class="flex items-center gap-6">
                <a href="/" class="hover:opacity-70 transition">Dashboard</a>
                <a href="/admin/" class="hover:opacity-70 transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Navbar 1B: Dark Top Bar

```html
<nav class="sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full" style="background: var(--brand)"></span>
                <a href="/" class="text-xl font-display font-bold">{{ app_name }}</a>
            </div>
            <div class="flex items-center gap-6 text-sm">
                <a href="/" class="hover:opacity-70 transition">Dashboard</a>
                <a href="/admin/" class="hover:opacity-70 transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Card 1A: Stat Card with Icon — layout reference

(See fully-restyled examples above for System B and D. Layout: icon in
a tinted/bordered box on the left, label + large value on the right.)

## Card 1B: Alert/Status Card with Icon — layout reference

Layout: left accent border, icon badge, title + description stacked.
Restyle border/icon-badge color per chosen Design System's `--accent`.

---

# 2. Public Blog / Content

## Footer 2A: 3-Column
Layout: brand blurb / quick links / social links, 3 even columns,
divider line, copyright row below. Restyle background/text per system.

## Footer 2B: Newsletter Signup
Layout: brand blurb + inline email signup form on one row, copyright
row below. Restyle input/button per system.

## Navbar 2A: Sticky with Search
Layout: logo left, search input center, nav links right.

## Navbar 2B: Centered Logo
Layout: logo centered on its own row, nav links centered below on a
second row with a divider.

## Card 2A: Article Preview Card with Icon
Layout: image top, category tag + icon, title, excerpt.

## Card 2B: Category Card with Icon
Layout: horizontal, icon badge left, category name + post count right.

---

# 3. Public SaaS / Dashboard

## Footer 3A: 4-Column
Layout: brand / product links / support links / legal links, 4 even
columns, copyright row below.

## Footer 3B: Simple Band
Layout: full-width brand band, then a slim copyright + links row below.

## Navbar 3A: Standard Bar
Layout: logo left, nav links right.

## Navbar 3B: With Avatar Placeholder
Layout: logo left, nav links + circular avatar badge right.

## Card 3A: Feature Card with Icon
Layout: icon badge top-left, title, description below.

## Card 3B: Stat Card with Trend Icon
Layout: label + trend icon on top row, large value below.

---

# 4. Education / School / LMS

## Footer 4A: Community & Resources
Layout: brand / community links / resource links / legal, 4 columns.

## Footer 4B: Contact & Social
Layout: brand + contact blurb left, link list right, copyright below.

## Navbar 4A: Portal Links
Layout: logo left, nav links right.

## Navbar 4B: With Announcement Bar
Layout: slim announcement strip above a standard navbar.

## Card 4A: Course Card with Icon
Layout: icon badge top, course title + description.

## Card 4B: Progress/Achievement Card with Icon
Layout: icon badge left, label + large percentage/value right.

---

## Base Template Requirement

`base.html` MUST contain:
- `<!DOCTYPE html>` structure
- Tailwind CSS CDN in `<head>`
- The chosen Design System's Google Fonts `<link>` tag, AND a
  `<link rel="stylesheet" href="{% static 'design_systems/<name>.css' %}">`
  tag referencing the matching static file — NEVER an inline `<style>`
  block reproducing the variables (see Token-Efficiency Requirement
  above). Both go in `<head>`, AFTER the Tailwind CDN script tag.
- `{% load static %}` at the very top of the template, above
  `<!DOCTYPE html>` — required for the `{% static %}` tag to work
- The chosen navbar variant, restyled per the Design System, inside
  `{% block navbar %}{% endblock %}`
- Flash messages area
- `{% block content %}{% endblock %}` for page content
- The chosen footer variant, restyled per the Design System, inside
  `{% block footer %}{% endblock %}`

Every other template MUST extend `base.html`:

```html
{% extends "base.html" %}
{% block content %}
...page content...
{% endblock %}
```

Never generate a standalone page template with its own `<!DOCTYPE html>`.