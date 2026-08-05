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
### App Shell — Sidebar Layout

```html
<div x-data="{ sidebarOpen: false }" class="min-h-screen flex bg-[var(--bg)]">

    <!-- Desktop sidebar -->
    <aside class="hidden md:flex md:flex-col w-64 flex-shrink-0 bg-[var(--surface)] border-r border-[var(--border)]">
        <div class="h-16 flex items-center px-6 border-b border-[var(--border)]">
            <a href="/" class="font-bold text-lg text-[var(--ink)]">{{ app_name }}</a>
        </div>
        <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
            <a href="/" class="flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius-md)] text-sm font-medium text-[var(--ink)] bg-[var(--brand)]/10 text-[var(--brand)] transition-colors duration-200">
                <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                Dashboard
            </a>
            <a href="/admin/" class="flex items-center gap-3 px-3 py-2.5 rounded-[var(--radius-md)] text-sm font-medium text-[var(--ink-muted)] hover:bg-[var(--bg)] hover:text-[var(--ink)] transition-colors duration-200">
                <svg class="w-5 h-5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /></svg>
                Admin
            </a>
        </nav>
        <div class="border-t border-[var(--border)] p-4 flex items-center gap-3">
            <div class="w-9 h-9 rounded-full bg-[var(--brand)] text-white flex items-center justify-center text-xs font-semibold flex-shrink-0">
                {{ user.username|first|upper }}
            </div>
            <div class="min-w-0 flex-1">
                <p class="text-sm font-medium text-[var(--ink)] truncate">{{ user.username }}</p>
                <a href="{% url 'logout' %}" class="text-xs text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors duration-200">Sign out</a>
            </div>
        </div>
    </aside>

    <!-- Mobile drawer -->
    <div x-show="sidebarOpen" x-trap.noscroll="sidebarOpen" @keydown.escape.window="sidebarOpen = false" class="fixed inset-0 z-50 md:hidden" style="display: none;">
        <div x-show="sidebarOpen" x-transition.opacity @click="sidebarOpen = false" class="fixed inset-0 bg-black/50"></div>
        <div x-show="sidebarOpen"
             x-transition:enter="transition ease-out duration-250" x-transition:enter-start="-translate-x-full" x-transition:enter-end="translate-x-0"
             x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="-translate-x-full"
             class="fixed inset-y-0 left-0 w-72 bg-[var(--surface)] border-r border-[var(--border)] p-4 flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <span class="font-bold text-[var(--ink)]">{{ app_name }}</span>
                <button @click="sidebarOpen = false" class="text-[var(--ink-muted)] hover:text-[var(--ink)] p-1 focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-[var(--radius-md)]" aria-label="Close menu">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" /></svg>
                </button>
            </div>
            <a href="/" class="px-3 py-2.5 rounded-[var(--radius-md)] text-[var(--ink)] hover:bg-[var(--bg)] transition-colors duration-200">Dashboard</a>
            <a href="/admin/" class="px-3 py-2.5 rounded-[var(--radius-md)] text-[var(--ink)] hover:bg-[var(--bg)] transition-colors duration-200">Admin</a>
        </div>
    </div>

    <div class="flex-1 flex flex-col min-w-0">
        <header class="h-16 flex items-center justify-between px-4 md:px-6 bg-[var(--surface)] border-b border-[var(--border)]">
            <button @click="sidebarOpen = true" class="md:hidden p-2 rounded-[var(--radius-md)] text-[var(--ink)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)]" aria-label="Open menu">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
            <span class="font-semibold text-[var(--ink)] md:hidden">{{ app_name }}</span>
            <div class="w-8 md:hidden"></div>
        </header>
        <main class="flex-1 overflow-y-auto p-4 md:p-8">
            {% block content %}{% endblock %}
        </main>
    </div>
</div>
```

Requires the Focus plugin (per the Plugin Requirements table below) for `x-trap.noscroll` on the mobile drawer.

### Command Palette (Cmd+K)

```html
<div x-data="{
        paletteOpen: false,
        query: '',
        items: [
            { label: 'Dashboard', href: '/', icon: 'home' },
            { label: 'Admin', href: '/admin/', icon: 'settings' },
        ],
        get filtered() {
            if (!this.query) return this.items;
            return this.items.filter(i => i.label.toLowerCase().includes(this.query.toLowerCase()));
        }
     }"
     @keydown.window="if ((event.metaKey || event.ctrlKey) && event.key === 'k') { event.preventDefault(); paletteOpen = true; }">

    <div x-show="paletteOpen" x-trap.noscroll="paletteOpen" @keydown.escape.window="paletteOpen = false" class="fixed inset-0 z-[60]" style="display: none;">
        <div x-show="paletteOpen" x-transition.opacity @click="paletteOpen = false" class="fixed inset-0 bg-black/50"></div>
        <div x-show="paletteOpen"
             x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 scale-95" x-transition:enter-end="opacity-100 scale-100"
             class="fixed top-24 left-1/2 -translate-x-1/2 w-full max-w-lg bg-[var(--surface)] rounded-[var(--radius-md)] border border-[var(--border)] shadow-[var(--shadow-card)] overflow-hidden">
            <div class="flex items-center px-4 border-b border-[var(--border)]">
                <svg class="w-4 h-4 text-[var(--ink-muted)] flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                <input x-model="query" x-ref="paletteInput" x-init="$watch('paletteOpen', v => v && setTimeout(() => $refs.paletteInput.focus(), 50))"
                       type="text" placeholder="Search or jump to..."
                       class="w-full px-3 py-3.5 bg-transparent text-sm text-[var(--ink)] focus:outline-none">
                <kbd class="text-xs text-[var(--ink-muted)] border border-[var(--border)] rounded px-1.5 py-0.5">Esc</kbd>
            </div>
            <ul class="max-h-72 overflow-y-auto py-2">
                <template x-for="item in filtered" :key="item.href">
                    <li>
                        <a :href="item.href" @click="paletteOpen = false"
                           class="flex items-center gap-3 px-4 py-2.5 text-sm text-[var(--ink)] hover:bg-[var(--bg)] transition-colors duration-200">
                            <span x-text="item.label"></span>
                        </a>
                    </li>
                </template>
                <li x-show="filtered.length === 0" class="px-4 py-6 text-center text-sm text-[var(--ink-muted)]">No results</li>
            </ul>
        </div>
    </div>
</div>
```

Requires the Focus plugin for `x-trap.noscroll`. Bind the trigger button (e.g. in the App Shell header) with `@click="paletteOpen = true"`.

## OPTIONAL: Command Palette (Cmd+K) for SaaS/dashboard apps

Global search-and-navigate via `Cmd+K`/`Ctrl+K` is a recognizable
"this feels like a real product" signal in base44/Linear/Replit-style
tools — but only build it when the app has enough real navigable
content (multiple distinct pages/records) to make search meaningful.

Do NOT include a Command Palette that only lists 1-2 static links
(e.g. just "Dashboard" and "Admin") — a palette with nothing real to
search is worse than no palette at all. Only add it once the app has
generated enough real pages/models that a working search list can be
populated from actual `items` (not placeholders).

Default: skip it. Add it only when explicitly requested, or when the
app has clearly outgrown simple sidebar navigation.

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
| Modal, Mobile Nav, App Shell Sidebar | Focus plugin |
| Command Palette (if built) | Focus plugin |
| Accordion | Collapse plugin |

Load plugins BEFORE core Alpine:
```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```