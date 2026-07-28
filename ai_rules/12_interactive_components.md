# Alpine.js Interactive Components

**Requirement:** `base.html` must include Alpine.js CDN in `<head>`, AFTER Tailwind CDN and Design System styles:

```html
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

All components use Design System CSS variables (`--surface`, `--ink`, `--border`, `--brand`, `--radius-md`). Restyle by swapping Design System, never hardcoding colors. Keep all `aria-*` attributes, `Escape` handling, and focus management — they're required for accessibility.

**Motion:** use `cubic-bezier(0.16, 1, 0.3, 1)` (a soft "overshoot" ease) for anything entering the screen — this single curve is most of what separates a "made with a framework" feel from a hand-polished one. Standard `ease-out`/`ease-in` is fine for exits, since exits don't need personality.

---

## 1. Dropdown Menu

```html
<div x-data="{ open: false }" class="relative inline-block text-left">
    <button
        @click="open = !open"
        @keydown.escape.window="open = false"
        :aria-expanded="open"
        aria-haspopup="true"
        class="inline-flex items-center gap-2 px-4 py-2.5 text-sm font-medium
               bg-[var(--surface)] text-[var(--ink)] border border-[var(--border)]
               rounded-[var(--radius-md)] shadow-sm
               hover:border-[var(--brand)]/40 hover:shadow-md
               active:scale-[0.98]
               focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2
               transition-all duration-200"
    >
        Options
        <svg class="w-4 h-4 text-[var(--ink-muted)] transition-transform duration-300" :class="open && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
        </svg>
    </button>
    <div
        x-show="open"
        @click.outside="open = false"
        x-transition:enter="transition ease-[cubic-bezier(0.16,1,0.3,1)] duration-200"
        x-transition:enter-start="opacity-0 scale-95 -translate-y-1"
        x-transition:enter-end="opacity-100 scale-100 translate-y-0"
        x-transition:leave="transition ease-in duration-100"
        x-transition:leave-start="opacity-100 scale-100"
        x-transition:leave-end="opacity-0 scale-95"
        class="absolute right-0 mt-2 w-52 origin-top-right
               bg-[var(--surface)]/95 backdrop-blur-sm border border-[var(--border)] rounded-[var(--radius-md)]
               shadow-[0_10px_38px_-10px_rgba(0,0,0,0.2),0_10px_20px_-15px_rgba(0,0,0,0.15)] py-1.5 z-50"
        role="menu"
        style="display: none;"
    >
        <a href="#" class="flex items-center gap-2.5 px-3.5 py-2.5 mx-1 text-sm text-[var(--ink)] rounded-[calc(var(--radius-md)-4px)] hover:bg-[var(--bg)] transition-colors" role="menuitem">
            <svg class="w-4 h-4 text-[var(--ink-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/></svg>
            Edit
        </a>
        <a href="#" class="flex items-center gap-2.5 px-3.5 py-2.5 mx-1 text-sm text-[var(--ink)] rounded-[calc(var(--radius-md)-4px)] hover:bg-[var(--bg)] transition-colors" role="menuitem">
            <svg class="w-4 h-4 text-[var(--ink-muted)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"/></svg>
            Duplicate
        </a>
        <div class="border-t border-[var(--border)] my-1.5 mx-2"></div>
        <a href="#" class="flex items-center gap-2.5 px-3.5 py-2.5 mx-1 text-sm text-red-500 rounded-[calc(var(--radius-md)-4px)] hover:bg-red-50 transition-colors" role="menuitem">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/></svg>
            Delete
        </a>
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
        class="px-4 py-2.5 bg-[var(--brand)] text-white text-sm font-medium rounded-[var(--radius-md)]
               shadow-sm hover:shadow-lg hover:brightness-110 active:scale-[0.98] transition-all duration-200
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
            x-transition:enter="transition ease-out duration-300"
            x-transition:enter-start="opacity-0"
            x-transition:enter-end="opacity-100"
            x-transition:leave="transition ease-in duration-200"
            x-transition:leave-start="opacity-100"
            x-transition:leave-end="opacity-0"
            @click="open = false"
            class="fixed inset-0 bg-black/40 backdrop-blur-sm"
        ></div>
        <div
            x-show="open"
            x-transition:enter="transition ease-[cubic-bezier(0.16,1,0.3,1)] duration-300"
            x-transition:enter-start="opacity-0 scale-90 translate-y-4"
            x-transition:enter-end="opacity-100 scale-100 translate-y-0"
            x-transition:leave="transition ease-in duration-150"
            x-transition:leave-start="opacity-100 scale-100"
            x-transition:leave-end="opacity-0 scale-95"
            role="dialog"
            aria-modal="true"
            aria-labelledby="modal-title"
            class="relative bg-[var(--surface)] rounded-[calc(var(--radius-md)+4px)] shadow-2xl ring-1 ring-black/5
                   max-w-md w-full p-7"
        >
            <div class="w-11 h-11 rounded-full bg-red-50 flex items-center justify-center mb-4">
                <svg class="w-5 h-5 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
            </div>
            <h3 id="modal-title" class="font-display text-lg font-semibold text-[var(--ink)] mb-1.5">Confirm Action</h3>
            <p class="text-sm text-[var(--ink-muted)] mb-6 leading-relaxed">Are you sure you want to continue? This cannot be undone.</p>
            <div class="flex justify-end gap-3">
                <button @click="open = false" class="px-4 py-2.5 text-sm font-medium text-[var(--ink)] border border-[var(--border)] rounded-[var(--radius-md)] hover:bg-[var(--bg)] active:scale-[0.98] transition-all focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2">Cancel</button>
                <button @click="open = false" class="px-4 py-2.5 text-sm font-medium bg-[var(--brand)] text-white rounded-[var(--radius-md)] shadow-sm hover:shadow-md hover:brightness-110 active:scale-[0.98] transition-all focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-offset-2">Confirm</button>
            </div>
        </div>
    </div>
</div>
```

---

## 3. Toast / Flash Notification

Icon varies by Django message tag (`success`, `error`, `warning`, `info`) — falls back to a neutral dot if untagged.

```html
{% if messages %}
<div class="fixed top-4 right-4 z-50 space-y-2.5 w-full max-w-sm" x-data>
    {% for message in messages %}
    <div
        x-data="{ show: true }"
        x-init="setTimeout(() => show = false, 5000)"
        x-show="show"
        x-transition:enter="transition ease-[cubic-bezier(0.16,1,0.3,1)] duration-300"
        x-transition:enter-start="opacity-0 translate-x-8 scale-95"
        x-transition:enter-end="opacity-100 translate-x-0 scale-100"
        x-transition:leave="transition ease-in duration-200"
        x-transition:leave-start="opacity-100"
        x-transition:leave-end="opacity-0 scale-95"
        role="status"
        class="flex items-start gap-3 px-4 py-3.5
               bg-[var(--surface)]/95 backdrop-blur-sm border border-[var(--border)] rounded-[var(--radius-md)]
               shadow-[0_10px_38px_-10px_rgba(0,0,0,0.25)]"
    >
        {% if message.tags == 'success' %}
        <div class="w-5 h-5 rounded-full bg-green-100 flex items-center justify-center flex-shrink-0 mt-0.5">
            <svg class="w-3 h-3 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M5 13l4 4L19 7"/></svg>
        </div>
        {% elif message.tags == 'error' %}
        <div class="w-5 h-5 rounded-full bg-red-100 flex items-center justify-center flex-shrink-0 mt-0.5">
            <svg class="w-3 h-3 text-red-600" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12"/></svg>
        </div>
        {% else %}
        <div class="w-5 h-5 rounded-full bg-[var(--brand)]/10 flex items-center justify-center flex-shrink-0 mt-0.5">
            <svg class="w-3 h-3 text-[var(--brand)]" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="3"><path stroke-linecap="round" stroke-linejoin="round" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/></svg>
        </div>
        {% endif %}
        <span class="text-sm text-[var(--ink)] leading-snug pt-0.5">{{ message }}</span>
        <button @click="show = false" class="ml-auto text-[var(--ink-muted)] hover:text-[var(--ink)] transition-colors flex-shrink-0" aria-label="Dismiss">
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

Underline slides between tabs rather than snapping — the single detail that makes tabs feel "designed."

```html
<div x-data="{ tab: 'overview' }">
    <div class="relative flex gap-1 border-b border-[var(--border)]" role="tablist">
        <button
            @click="tab = 'overview'"
            :class="tab === 'overview' ? 'text-[var(--brand)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink)]'"
            class="relative px-4 py-2.5 text-sm font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-t-[var(--radius-md)]"
            role="tab" :aria-selected="tab === 'overview'"
        >
            Overview
            <span x-show="tab === 'overview'" class="absolute left-0 right-0 -bottom-px h-0.5 bg-[var(--brand)] rounded-full"></span>
        </button>
        <button
            @click="tab = 'activity'"
            :class="tab === 'activity' ? 'text-[var(--brand)]' : 'text-[var(--ink-muted)] hover:text-[var(--ink)]'"
            class="relative px-4 py-2.5 text-sm font-medium transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-t-[var(--radius-md)]"
            role="tab" :aria-selected="tab === 'activity'"
        >
            Activity
            <span x-show="tab === 'activity'" class="absolute left-0 right-0 -bottom-px h-0.5 bg-[var(--brand)] rounded-full"></span>
        </button>
    </div>
    <div class="py-5">
        <div x-show="tab === 'overview'" x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 translate-y-1" x-transition:enter-end="opacity-100 translate-y-0" role="tabpanel">Overview content goes here.</div>
        <div x-show="tab === 'activity'" x-transition:enter="transition ease-out duration-200" x-transition:enter-start="opacity-0 translate-y-1" x-transition:enter-end="opacity-100 translate-y-0" role="tabpanel" style="display: none;">Activity content goes here.</div>
    </div>
</div>
```

---

## 5. Mobile Nav Toggle

```html
<nav x-data="{ open: false }" class="sticky top-0 z-50 bg-[var(--surface)]/90 backdrop-blur-md border-b border-[var(--border)]">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-display font-bold text-[var(--ink)] tracking-tight">{{ app_name }}</a>
            <div class="hidden md:flex items-center gap-1">
                <a href="/" class="px-3 py-2 text-sm font-medium text-[var(--ink-muted)] hover:text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Home</a>
                <a href="/admin/" class="px-3 py-2 text-sm font-medium text-[var(--ink-muted)] hover:text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Admin</a>
            </div>
            <button
                @click="open = !open"
                class="md:hidden text-[var(--ink)] focus:outline-none focus:ring-2 focus:ring-[var(--brand)] rounded-[var(--radius-md)] p-2 hover:bg-[var(--bg)] transition-colors"
                :aria-expanded="open" aria-label="Toggle menu"
            >
                <svg x-show="!open" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" />
                </svg>
                <svg x-show="open" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" style="display: none;">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </div>
        <div
            x-show="open"
            x-transition:enter="transition ease-[cubic-bezier(0.16,1,0.3,1)] duration-250"
            x-transition:enter-start="opacity-0 -translate-y-2"
            x-transition:enter-end="opacity-100 translate-y-0"
            x-transition:leave="transition ease-in duration-150"
            x-transition:leave-start="opacity-100"
            x-transition:leave-end="opacity-0"
            class="md:hidden pb-4 space-y-1"
            style="display: none;"
        >
            <a href="/" class="block px-3 py-2.5 text-sm font-medium text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Home</a>
            <a href="/admin/" class="block px-3 py-2.5 text-sm font-medium text-[var(--ink)] hover:bg-[var(--bg)] rounded-[var(--radius-md)] transition-colors">Admin</a>
        </div>
    </div>
</nav>
```

---

## 6. Accordion

Chevron rotates rather than a plus/minus swap — smoother, and works with the same icon in both states.

```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
```

```html
<div class="divide-y divide-[var(--border)] border border-[var(--border)] rounded-[calc(var(--radius-md)+2px)] overflow-hidden shadow-sm" x-data="{ openItem: null }">
    <div>
        <button
            @click="openItem = openItem === 1 ? null : 1"
            :aria-expanded="openItem === 1"
            class="w-full flex justify-between items-center gap-4 px-5 py-4 text-left text-sm font-medium
                   text-[var(--ink)] hover:bg-[var(--bg)] transition-colors
                   focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-inset"
        >
            What's included in the free plan?
            <svg class="w-4 h-4 text-[var(--ink-muted)] transition-transform duration-300 flex-shrink-0" :class="openItem === 1 && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div x-show="openItem === 1" x-collapse class="px-5 pb-4 text-sm text-[var(--ink-muted)] leading-relaxed" style="display: none;">
            Everything you need to get started, including core features and community support.
        </div>
    </div>
    <div>
        <button
            @click="openItem = openItem === 2 ? null : 2"
            :aria-expanded="openItem === 2"
            class="w-full flex justify-between items-center gap-4 px-5 py-4 text-left text-sm font-medium
                   text-[var(--ink)] hover:bg-[var(--bg)] transition-colors
                   focus:outline-none focus:ring-2 focus:ring-[var(--brand)] focus:ring-inset"
        >
            Can I upgrade later?
            <svg class="w-4 h-4 text-[var(--ink-muted)] transition-transform duration-300 flex-shrink-0" :class="openItem === 2 && 'rotate-180'" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M19 9l-7 7-7-7" />
            </svg>
        </button>
        <div x-show="openItem === 2" x-collapse class="px-5 pb-4 text-sm text-[var(--ink-muted)] leading-relaxed" style="display: none;">
            Yes, upgrade or downgrade at any time from your account settings.
        </div>
    </div>
</div>
```

---

## 7. Skeleton Loader

Not in the original set, but this is one of the highest-leverage additions for that "polished app" feel — shown while data loads instead of a blank flash or spinner.

```html
<div class="animate-pulse space-y-3">
    <div class="h-4 bg-[var(--border)] rounded-[var(--radius-md)] w-2/3"></div>
    <div class="h-4 bg-[var(--border)] rounded-[var(--radius-md)] w-full"></div>
    <div class="h-4 bg-[var(--border)] rounded-[var(--radius-md)] w-5/6"></div>
</div>
```

---

## Plugin Requirements

| Component | Requires |
|---|---|
| Dropdown, Tabs, Mobile Nav, Toast, Skeleton | Core Alpine only |
| Modal/Dialog | Core Alpine + Focus plugin |
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

- [ ] Use only these 7 patterns — no hand-invented JS
- [ ] Required plugins loaded, before core Alpine
- [ ] `style="display: none;"` on every `x-show` element
- [ ] All colors use Design System CSS variables — no hardcoded hex
- [ ] Escape/click-outside close on all dismissible elements
- [ ] Entering elements use the soft-overshoot ease; exits use plain ease-in/out
- [ ] Interactive elements have a visible `active:scale-[0.98]` or similar press feedback