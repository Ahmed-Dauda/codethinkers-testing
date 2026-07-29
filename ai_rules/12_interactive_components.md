# Alpine.js Interactive Components

**Requirement:** `base.html` must include Alpine.js CDN in `<head>`, AFTER Tailwind CDN and Design System styles:

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

All components use Design System CSS variables (`--surface`, `--ink`, `--border`, `--brand`, `--radius-md`). Restyle by swapping Design System, never hardcoding colors. Keep all `aria-*` attributes, `Escape` handling, and focus management — they're required for accessibility.

---

## ⚠️ MANDATORY: Mobile Navigation — Every Generated App

**Every single generated app, with no exceptions, must hide the full
navbar on mobile (below the `md` breakpoint) and replace it with
either the Mobile Nav Drawer (#5) or the App Shell Sidebar (#7).**

This is a hard requirement, not a style preference. A navbar that just
wraps, shrinks, or overflows horizontally on a small screen is NOT
acceptable output — that reads as unfinished/broken, not "simple."
Every app the person opens on their phone (which is most first
impressions of a generated app) needs to feel like a real native-style
app: a hamburger icon, a slide-in panel, a backdrop, real transitions.

**Which one to use:**
- **Public-facing pages** (marketing, blog, landing page, content site)
  → Mobile Nav Drawer (#5), paired with whichever navbar
  variant (1A-4B) from `10_ui_patterns.md` supplies the desktop link
  content.
- **Authenticated/dashboard areas** (any app where a logged-in user
  sees multiple internal pages regularly) → App Shell Sidebar (#7),
  which already has its own built-in mobile drawer behavior.

**Never** ship a bare `<nav>` copied straight from `10_ui_patterns.md`
without wrapping it in one of these two patterns first. Treat the
Navbar 1A-4B examples in that file as supplying ONLY the link
list/branding content — the actual responsive shell (desktop bar +
mobile drawer) always comes from this file.

---

## 1. Dropdown Menu

```html
<div x-data="{ open: false }" class="relative inline-block text-left">
    <button
        @click="open = !open"
        @keydown.escape.window="open = false"
        :aria-expanded="open"
        aria-haspopup="true"
        class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium
               bg-[var(--surface)] text-[var(--ink)] border border-[var(--border)]
               rounded-[var(--radius-md)] hover:bg-[var(--surface-hover,var(--surface))]
               focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2
               transition-colors duration-200"
    >
        Options
        <svg class="w-4 h-4 transition-transform" :class="open && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
    </button>
    <div
        x-show="open"
        @click.outside="open = false"
        x-transition:enter="transition ease-out duration-150"
        x-transition:enter-start="opacity-0 scale-95"
        x-transition:enter-end="opacity-100 scale-100"
        x-transition:leave="transition ease-in duration-100"
        x-transition:leave-start="opacity-100 scale-100"
        x-transition:leave-end="opacity-0 scale-95"
        class="absolute right-0 mt-2 w-48 origin-top-right
               bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-md)]
               shadow-[var(--shadow-card,0_4px_12px_rgba(0,0,0,0.1))] py-1 z-50"
        role="menu"
        style="display: none;"
    >
        <a href="#" class="block px-4 py-2 text-sm text-[var(--ink)] hover:bg-[var(--surface-hover,var(--bg))] transition-colors" role="menuitem">Edit</a>
        <a href="#" class="block px-4 py-2 text-sm text-[var(--ink)] hover:bg-[var(--surface-hover,var(--bg))] transition-colors" role="menuitem">Duplicate</a>
        <div class="border-t border-[var(--border)] my-1"></div>
        <a href="#" class="block px-4 py-2 text-sm text-red-500 hover:bg-[var(--surface-hover,var(--bg))] transition-colors" role="menuitem">Delete</a>
    </div>
</div>
```

---

## 2. Modal / Dialog

Requires Focus plugin (load BEFORE core Alpine):

```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

```html
<div x-data="{ open: false }">
    <button
        @click="open = true"
        class="px-4 py-2 bg-[var(--brand)] text-white rounded-[var(--radius-md)]
               hover:opacity-90 active:scale-[0.98] transition
               focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2"
    >
        Open Dialog
    </button>
    <div
        x-show="open"
        x-trap.noscroll="open"
        @keydown.escape.window="open = false"
        class="fixed inset-0 z-50 flex items-center justify-center p-4"
        style="display: none;"
    >
        <div
            x-show="open"
            x-transition:enter="transition ease-out duration-200"
            x-transition:enter-start="opacity-0"
            x-transition:enter-end="opacity-100"
            x-transition:leave="transition ease-in duration-150"
            x-transition:leave-start="opacity-100"
            x-transition:leave-end="opacity-0"
            @click="open = false"
            class="fixed inset-0 bg-black/50"
        ></div>
        <div
            x-show="open"
            x-transition:enter="transition ease-out duration-200"
            x-transition:enter-start="opacity-0 scale-95"
            x-transition:enter-end="opacity-100 scale-100"
            x-transition:leave="transition ease-in duration-150"
            x-transition:leave-start="opacity-100 scale-100"
            x-transition:leave-end="opacity-0 scale-95"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            class="relative bg-[var(--surface)] rounded-[var(--radius-md)] shadow-xl
                   max-w-md w-full p-6"
        >
            <h3 id="modal-title" class="font-display text-xl font-semibold text-[var(--ink)] mb-2">Confirm Action</h3>
            <p class="text-sm text-[var(--ink-muted)] mb-6">Are you sure you want to continue? This cannot be undone.</p>
            <div class="flex justify-end gap-3">
                <button @click="open = false" class="px-4 py-2 text-sm font-medium text-[var(--ink)] border border-[var(--border)] rounded-[var(--radius-md)] hover:bg-[var(--bg)] transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2">Cancel</button>
                <button @click="open = false" class="px-4 py-2 text-sm font-medium bg-[var(--brand)] text-white rounded-[var(--radius-md)] hover:opacity-90 active:scale-[0.98] transition focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2">Confirm</button>
            </div>
        </div>
    </div>
</div>
```

---

## 3. Toast / Flash Notification

```html
{% if messages %}
<div class="fixed top-4 right-4 z-50 space-y-2" x-data>
    {% for message in messages %}
    <div
        x-data="{ show: true }"
        x-init="setTimeout(() => show = false, 5000)"
        x-show="show"
        x-transition:enter="transition ease-out duration-200"
        x-transition:enter-start="opacity-0 translate-x-4"
        x-transition:enter-end="opacity-100 translate-x-0"
        x-transition:leave="transition ease-in duration-150"
        x-transition:leave-start="opacity-100"
        x-transition:leave-end="opacity-0"
        role="status"
        class="flex items-center gap-3 max-w-sm px-4 py-3
               bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-md)]
               shadow-[var(--shadow-card,0_4px_12px_rgba(0,0,0,0.15))]"
    >
        <span class="text-sm text-[var(--ink)]">{{ message }}</span>
        <button @click="show = false" class="ml-auto text-[var(--ink-muted)] hover:text-[var(--ink)]" aria-label="Dismiss">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
            </svg>
        </button>
    </div>
    {% endfor %}
</div>
{% endif %}
```

---

## 4. Tabs

```html
<div x-data="{ tab: 'overview' }">
    <div class="flex gap-1 border-b border-[var(--border)]" role="tablist">
        <button
            @click="tab = 'overview'"
            :class="tab === 'overview' ? 'border-[var(--brand)] text-[var(--brand)]' : 'border-transparent text-[var(--ink-muted)] hover:text-[var(--ink)]'"
            class="px-4 py-2 text-sm font-medium border-b-2 transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--brand)]"
            role="tab" :aria-selected="tab === 'overview'"
        >Overview</button>
        <button
            @click="tab = 'activity'"
            :class="tab === 'activity' ? 'border-[var(--brand)] text-[var(--brand)]' : 'border-transparent text-[var(--ink-muted)] hover:text-[var(--ink)]'"
            class="px-4 py-2 text-sm font-medium border-b-2 transition-colors focus:outline-none focus:ring-2 focus:ring-[var(--brand)]"
            role="tab" :aria-selected="tab === 'activity'"
        >Activity</button>
    </div>
    <div class="py-4">
        <div x-show="tab === 'overview'" x-transition.opacity role="tabpanel">Overview content goes here.</div>
        <div x-show="tab === 'activity'" x-transition.opacity role="tabpanel" style="display: none;">Activity content goes here.</div>
    </div>
</div>
```

---

## 5. Mobile Nav — Slide-In Drawer (REQUIRED for all public-facing pages)

The base44/Lovable/Replit pattern: a full-height drawer that slides in
from the side with a backdrop, NOT a dropdown that pushes content down,
and NOT a navbar that just wraps/shrinks. Requires Focus plugin for
`x-trap` (same as Modal). This is the default navbar shell for every
generated app's public pages — see the mandatory section at the top.

```html
<nav x-data="{ open: false }" class="sticky top-0 z-50 bg-[var(--surface)] border-b border-[var(--border)]">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-display font-bold text-[var(--ink)]">{{ app_name }}</a>
            <div class="hidden md:flex items-center gap-6">
                <a href="/" class="text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors">Home</a>
                <a href="/admin/" class="text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors">Admin</a>
            </div>
            <button
                @click="open = true"
                class="md:hidden text-[var(--ink)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-[var(--radius-md)] p-2"
                aria-label="Open menu"
            >
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
            </button>
        </div>
    </div>

    <!-- Drawer -->
    <div
        x-show="open"
        x-trap.noscroll="open"
        @keydown.escape.window="open = false"
        class="fixed inset-0 z-50 md:hidden"
        style="display: none;"
    >
        <div
            x-show="open"
            x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0" x-transition:enter-end="opacity-100"
            x-transition:leave="transition ease-in duration-150" x-transition:leave-start="opacity-100" x-transition:leave-end="opacity-0"
            @click="open = false"
            class="fixed inset-0 bg-black/50"
        ></div>
        <div
            x-show="open"
            x-transition:enter="transition ease-out duration-250" x-transition:enter-start="translate-x-full" x-transition:enter-end="translate-x-0"
            x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="translate-x-full"
            role="dialog" aria-modal="true"
            class="fixed inset-y-0 right-0 w-72 bg-[var(--surface)] border-l border-[var(--border)] p-6 flex flex-col"
        >
            <div class="flex justify-between items-center mb-8">
                <span class="font-display font-bold text-[var(--ink)]">{{ app_name }}</span>
                <button @click="open = false" class="text-[var(--ink-muted)] hover:text-[var(--ink)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-[var(--radius-md)] p-1" aria-label="Close menu">
                    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>
            <div class="space-y-1">
                <a href="/" class="block px-3 py-2.5 text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Home</a>
                <a href="/admin/" class="block px-3 py-2.5 text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Admin</a>
            </div>
        </div>
    </div>
</nav>
```
---

## 6. Accordion

Requires Collapse plugin (load BEFORE core Alpine):

```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

```html
<div class="divide-y divide-[var(--border)] border border-[var(--border)] rounded-[var(--radius-md)]" x-data="{ openItem: null }">
    <div>
        <button
            @click="openItem = openItem === 1 ? null : 1"
            :aria-expanded="openItem === 1"
            class="w-full flex justify-between items-center px-4 py-3 text-left text-sm font-medium
                   text-[var(--ink)] hover:bg-[var(--bg)] transition-colors
                   focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-inset"
        >
            What's included in the free plan?
            <svg class="w-4 h-4 transition-transform flex-shrink-0" :class="openItem === 1 && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div x-show="openItem === 1" x-collapse class="px-4 pb-3 text-sm text-[var(--ink-muted)]" style="display: none;">
            Everything you need to get started, including core features and community support.
        </div>
    </div>
    <div>
        <button
            @click="openItem = openItem === 2 ? null : 2"
            :aria-expanded="openItem === 2"
            class="w-full flex justify-between items-center px-4 py-3 text-left text-sm font-medium
                   text-[var(--ink)] hover:bg-[var(--bg)] transition-colors
                   focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-inset"
        >
            Can I upgrade later?
            <svg class="w-4 h-4 transition-transform flex-shrink-0" :class="openItem === 2 && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div x-show="openItem === 2" x-collapse class="px-4 pb-3 text-sm text-[var(--ink-muted)]" style="display: none;">
            Yes, upgrade or downgrade at any time from your account settings.
        </div>
    </div>
</div>
```

---

## 7. App Shell — Sidebar Layout (REQUIRED for all authenticated/dashboard pages)

The defining layout pattern of base44/Lovable/Replit-generated apps:
a persistent left sidebar (icons + labels) instead of a top navbar, for
any authenticated/dashboard-style area. Has its own built-in mobile
drawer — satisfies the mandatory mobile nav requirement on its own,
no need to also add pattern #5 on the same page. Use this INSTEAD OF a
top navbar for dashboard-type pages and any multi-page authenticated
app — keep the top navbar (#5) for public-facing marketing/content
pages only.

```html
<div x-data="{ sidebarOpen: false }" class="flex h-screen overflow-hidden bg-[var(--bg)]">
    <!-- Desktop sidebar -->
    <aside class="hidden md:flex md:flex-col w-64 bg-[var(--surface)] border-r border-[var(--border)] p-4">
        <div class="flex items-center gap-2 px-2 mb-8">
            <div class="w-8 h-8 rounded-[var(--radius-md)] bg-[var(--brand)] flex items-center justify-center text-white font-display font-bold">{{ app_name|slice:":1" }}</div>
            <span class="font-display font-semibold text-[var(--ink)]">{{ app_name }}</span>
        </div>
        <nav class="flex-1 space-y-1">
            <a href="/" class="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-[var(--radius-md)] bg-[var(--brand)]/10 text-[var(--brand)]">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" /></svg>
                Dashboard
            </a>
            <a href="/admin/" class="flex items-center gap-3 px-3 py-2 text-sm font-medium rounded-[var(--radius-md)] text-[var(--ink-muted)] hover:bg-[var(--bg)] hover:text-[var(--ink)] transition-colors">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" /></svg>
                Admin
            </a>
        </nav>
    </aside>

    <!-- Mobile drawer (same pattern as #5, reused for sidebar nav) -->
    <div x-show="sidebarOpen" x-trap.noscroll="sidebarOpen" @keydown.escape.window="sidebarOpen = false" class="fixed inset-0 z-50 md:hidden" style="display: none;">
        <div x-show="sidebarOpen" x-transition.opacity @click="sidebarOpen = false" class="fixed inset-0 bg-black/50"></div>
        <div x-show="sidebarOpen" x-transition:enter="transition ease-out duration-250" x-transition:enter-start="-translate-x-full" x-transition:enter-end="translate-x-0"
             x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="-translate-x-full"
             class="fixed inset-y-0 left-0 w-64 bg-[var(--surface)] p-4">
            <nav class="space-y-1 mt-4">
                <a href="/" class="block px-3 py-2.5 text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)]">Dashboard</a>
                <a href="/admin/" class="block px-3 py-2.5 text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)]">Admin</a>
            </nav>
        </div>
    </div>

    <!-- Main content -->
    <div class="flex-1 flex flex-col overflow-hidden">
        <header class="md:hidden flex items-center justify-between h-14 px-4 border-b border-[var(--border)] bg-[var(--surface)]">
            <button @click="sidebarOpen = true" class="text-[var(--ink)] p-2" aria-label="Open menu">
                <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
            <span class="font-display font-semibold text-[var(--ink)]">{{ app_name }}</span>
            <div class="w-9"></div>
        </header>
        <main class="flex-1 overflow-y-auto p-6">
            {% block content %}{% endblock %}
        </main>
    </div>
</div>
```

---

## 8. Command Palette (Cmd+K)

The signature interaction of Linear/base44/Lovable-style tools —
global search-and-navigate triggered by `Cmd+K`/`Ctrl+K`. Include on
dashboard/sidebar-shell pages as a polish touch; optional elsewhere.

```html
<div
    x-data="{
        open: false,
        query: '',
        items: [
            { label: 'Dashboard', url: '/', icon: 'home' },
            { label: 'Admin', url: '/admin/', icon: 'settings' },
        ],
        get filtered() {
            return this.query === '' ? this.items : this.items.filter(i => i.label.toLowerCase().includes(this.query.toLowerCase()));
        }
    }"
    @keydown.window.prevent.cmd.k="open = true"
    @keydown.window.prevent.ctrl.k="open = true"
    @keydown.escape.window="open = false"
>
    <div
        x-show="open"
        x-trap.noscroll="open"
        class="fixed inset-0 z-50 flex items-start justify-center pt-24 px-4"
        style="display: none;"
    >
        <div x-show="open" x-transition.opacity @click="open = false" class="fixed inset-0 bg-black/50"></div>
        <div
            x-show="open"
            x-transition:enter="transition ease-out duration-150" x-transition:enter-start="opacity-0 scale-95" x-transition:enter-end="opacity-100 scale-100"
            role="dialog" aria-modal="true" aria-label="Command palette"
            class="relative w-full max-w-lg bg-[var(--surface)] border border-[var(--border)] rounded-[var(--radius-md)] shadow-xl overflow-hidden"
        >
            <div class="flex items-center gap-3 px-4 border-b border-[var(--border)]">
                <svg class="w-4 h-4 text-[var(--ink-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
                <input
                    x-model="query"
                    x-ref="cmdInput"
                    x-init="$watch('open', v => v && setTimeout(() => $refs.cmdInput.focus(), 50))"
                    type="text"
                    placeholder="Search or jump to..."
                    class="flex-1 bg-transparent py-3 text-sm text-[var(--ink)] placeholder-[var(--ink-muted)] focus:outline-none"
                />
                <kbd class="text-xs text-[var(--ink-muted)] border border-[var(--border)] rounded px-1.5 py-0.5">Esc</kbd>
            </div>
            <div class="max-h-72 overflow-y-auto py-2">
                <template x-for="item in filtered" :key="item.label">
                    <a :href="item.url" @click="open = false" class="flex items-center gap-3 px-4 py-2.5 text-sm text-[var(--ink)] hover:bg-[var(--bg)] transition-colors">
                        <span x-text="item.label"></span>
                    </a>
                </template>
                <p x-show="filtered.length === 0" class="px-4 py-6 text-sm text-center text-[var(--ink-muted)]">No results found.</p>
            </div>
        </div>
    </div>
    <button
        @click="open = true"
        class="hidden md:flex items-center gap-2 px-3 py-1.5 text-sm text-[var(--ink-muted)] bg-[var(--bg)] border border-[var(--border)] rounded-[var(--radius-md)] hover:border-[var(--brand)] transition-colors"
    >
        <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" /></svg>
        Search
        <kbd class="ml-2 text-xs border border-[var(--border)] rounded px-1.5 py-0.5">⌘K</kbd>
    </button>
</div>
```

---

## Plugin Requirements

| Component | Requires |
|---|---|
| Dropdown, Tabs, Toast | Core Alpine only |
| Modal/Dialog, Mobile Nav Drawer, App Shell Sidebar, Command Palette | Core Alpine + Focus plugin |
| Accordion | Core Alpine + Collapse plugin |

Full `<head>` when all used:

```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

Plugins MUST load before core Alpine.

---

## Checklist

- [ ] Every page's navbar hides fully on mobile and shows a hamburger
      → drawer/sidebar instead — no wrapping/shrinking navbars, ever
- [ ] Public pages use Mobile Nav Drawer (#5); authenticated/dashboard
      pages use App Shell Sidebar (#7) — not a bare navbar on either
- [ ] Use only these 8 patterns — no hand-invented JS
- [ ] Required plugins loaded, before core Alpine
- [ ] `style="display: none;"` on every `x-show` element
- [ ] All colors use Design System CSS variables
- [ ] Escape/click-outside close on all dismissible elements