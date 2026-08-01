# Alpine.js Interactive Components

**Requirement:** `base.html` MUST include Alpine.js CDN in `<head>`, AFTER Tailwind CDN.

## MANDATORY: Every generated app must have navbar, footer, mobile menu, and cards

- **base.html** MUST contain: complete `<nav>` with logo + links, `<main>` block, and `<footer>`
- **Mobile**: navbar MUST collapse to hamburger menu below `md` breakpoint — never a navbar that just wraps or shrinks
- **Cards**: any stat, feature, dashboard, or listing-style content block MUST use the Card pattern (icon badge + label/value, or icon badge + title/description) matching the app's Structure type in `10_ui_patterns.md` — never bare unstyled `<div>` blocks or plain text lists
- **No exceptions**: bare cards without nav/footer, a navbar with no mobile collapse, or dashboard content with no card styling = broken output, not a style choice

## Navbar — modern, with mobile drawer built in

```html
<nav x-data="{ open: false }" class="sticky top-0 z-50 bg-[var(--surface)]/80 backdrop-blur border-b border-[var(--border)]">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="font-display font-bold text-lg text-[var(--ink)]">{{ app_name }}</a>

            <div class="hidden md:flex items-center gap-6 text-sm">
                <a href="/" class="text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors">Home</a>
                <a href="/admin/" class="text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors">Admin</a>
                {% if user.is_authenticated %}
                <div class="w-8 h-8 rounded-full bg-[var(--brand)] text-white flex items-center justify-center text-xs font-semibold">
                    {{ user.username|first|upper }}
                </div>
                {% else %}
                <a href="{% url 'login' %}" class="px-3 py-1.5 rounded-[var(--radius-md)] bg-[var(--brand)] text-white text-sm font-medium hover:opacity-90 active:scale-[0.98] transition">Sign in</a>
                {% endif %}
            </div>

            <button @click="open = true" class="md:hidden p-2 rounded-[var(--radius-md)] text-[var(--ink)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]" aria-label="Open menu">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
        </div>
    </div>

    <div x-show="open" x-trap.noscroll="open" @keydown.escape.window="open = false" class="fixed inset-0 z-50 md:hidden" style="display: none;">
        <div x-show="open" x-transition.opacity @click="open = false" class="fixed inset-0 bg-black/50"></div>
        <div x-show="open"
             x-transition:enter="transition ease-out duration-250" x-transition:enter-start="translate-x-full" x-transition:enter-end="translate-x-0"
             x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="translate-x-full"
             class="fixed inset-y-0 right-0 w-72 bg-[var(--surface)] border-l border-[var(--border)] p-6 flex flex-col">
            <div class="flex justify-between items-center mb-8">
                <span class="font-display font-bold text-[var(--ink)]">{{ app_name }}</span>
                <button @click="open = false" class="text-[var(--ink-muted)] hover:text-[var(--ink)] p-1 focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-[var(--radius-md)]" aria-label="Close menu">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <a href="/" class="px-3 py-2.5 rounded-[var(--radius-md)] text-[var(--ink)] hover:bg-[var(--bg)] transition-colors">Home</a>
            <a href="/admin/" class="px-3 py-2.5 rounded-[var(--radius-md)] text-[var(--ink)] hover:bg-[var(--bg)] transition-colors">Admin</a>
        </div>
    </div>
</nav>
```

## Footer — modern, minimal

```html
<footer class="mt-auto border-t border-[var(--border)] bg-[var(--surface)]">
    <div class="max-w-7xl mx-auto px-4 py-8 flex flex-col md:flex-row justify-between items-center gap-4">
        <span class="font-display font-semibold text-[var(--ink)]">{{ app_name }}</span>
        <div class="flex gap-6 text-sm text-[var(--ink-muted)]">
            <a href="/" class="hover:text-[var(--ink)] transition-colors">Home</a>
            <a href="/admin/" class="hover:text-[var(--ink)] transition-colors">Admin</a>
            <a href="#" class="hover:text-[var(--ink)] transition-colors">Privacy</a>
        </div>
        <span class="text-sm text-[var(--ink-muted)]">&copy; {% now "Y" %} {{ app_name }}</span>
    </div>
</footer>
```

## Card — modern stat card with icon

```html
<div class="bg-[var(--surface)] rounded-[var(--radius-md)] p-6 flex items-center gap-4 border border-[var(--border)] hover:-translate-y-0.5 hover:shadow-[var(--shadow-glow,var(--shadow-card))] transition">
    <div class="w-11 h-11 rounded-[var(--radius-md)] bg-[var(--brand)]/10 text-[var(--brand)] flex items-center justify-center flex-shrink-0">
        <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2a4 4 0 014-4h3m0 0l-3-3m3 3l-3 3M4 7h6m-6 4h6m-6 4h6" /></svg>
    </div>
    <div>
        <p class="text-sm text-[var(--ink-muted)]">{{ stat_label }}</p>
        <p class="text-2xl font-display font-bold text-[var(--ink)]">{{ stat_value }}</p>
    </div>
</div>
```

---

## MANDATORY: App Shell Sidebar for dashboard/authenticated apps

This is the defining base44/Lovable/Replit signature — a persistent left
sidebar with icons + labels, not a top navbar, for any area a logged-in
user visits repeatedly (dashboards, admin-style multi-page apps).

- Use for: any app where `Pattern 3` (Public SaaS, per
  `02_application_classification.md`) applies, or the app has a
  dashboard/analytics/data-heavy surface
- Skip for: purely public marketing/content pages (blog, portfolio,
  landing page with no login) — those use the standard top navbar +
  mobile drawer instead
- Includes its own built-in mobile drawer — satisfies the mobile-menu
  requirement on its own on these pages, no separate top navbar needed
- See the full App Shell Sidebar pattern in the component library
  (search this file's history / `12_interactive_components.md` full
  version for "App Shell — Sidebar Layout")

## RECOMMENDED: Command Palette (Cmd+K) for SaaS/dashboard apps

Global search-and-navigate via `Cmd+K`/`Ctrl+K` is the single most
recognizable "this feels like a real product" signal in base44/Linear/
Replit-style tools. Include it on any Pattern 3 (SaaS) app with more
than a couple of internal pages — optional elsewhere, but strongly
preferred whenever an App Shell Sidebar is present.

## Professional polish — non-negotiable on every interactive element

- Every hover state has a `transition-colors duration-200` (or
  `transition-all` when multiple properties change) — an instant snap
  reads as unfinished
- Every focusable element has a visible `focus:ring-2` in the Design
  System's `--brand` color — never `focus:outline-none` alone
- Buttons get `active:scale-[0.98]` for a tactile press feel
- Cards in a grid get `hover:-translate-y-0.5` plus the Design
  System's elevation/glow token, not a flat static state
- If the app has user accounts, the navbar/sidebar MUST include an
  avatar or initials badge for the logged-in user — a bare "Logout"
  text link with no visual account presence reads as unfinished

## Plugin Requirements
| Component | Requires |
|---|---|
| Modal, Mobile Nav, App Shell Sidebar, Command Palette | Focus plugin |
| Accordion | Collapse plugin |

Load plugins BEFORE core Alpine:
```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```