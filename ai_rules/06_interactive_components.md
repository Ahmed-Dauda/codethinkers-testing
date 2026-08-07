# ⚠️ READ THIS FIRST — DESIGN QUALITY IS MANDATORY

You are generating production-ready apps that must look like Base44, Lovable, or Replit output. Every template you generate must pass this visual checklist:

- [ ] Gradient hero section (bg-gradient-to-br from-COLOR-600 to-COLOR-700) with text-5xl heading
- [ ] Stats cards have colored icon badges, not plain numbers
- [ ] Cards use rounded-2xl + shadow + hover:-translate-y-1
- [ ] No "Content coming soon" or placeholder text anywhere
- [ ] No plain gray backgrounds — use brand color tints
- [ ] Section spacing is py-16+, not py-8
- [ ] Buttons have active:scale-95

If your output fails any of these, it is a FAILED BUILD. Do not return JSON until every template passes this checklist.

## CRITICAL: Template Rules — Violations Cause Build Failure

1. **base.html is MANDATORY** — every app MUST include a complete `base.html` with navbar, footer, and mobile menu. Never skip it. The navbar MUST include links relevant to the app type: e-commerce apps need Products/Cart, dashboards need sidebar navigation, public sites need relevant pages. Never just "Home" and "Admin" — that reads as unfinished.
2. **Every template MUST extend base.html** — `{% extends "base.html" %}` must be the FIRST line of every HTML template except base.html itself. Never generate standalone `<html><head><body>` documents.
3. **Templates only contain content blocks** — the body of every template (after `{% extends "base.html" %}`) should ONLY have `{% block content %}` and its contents. No `<html>`, `<head>`, `<body>`, or Tailwind CDN script tags.
4. **base.html owns all structure** — navbar, footer, sidebar, Tailwind CDN, Alpine.js, and Design System variables live ONLY in base.html.
5. **Every content element MUST be styled** — never use bare `<ul>`, `<li>`, `<div>`, or `<h1>` without Tailwind classes. Cards need `bg-white rounded-lg shadow p-6`, lists need proper spacing, forms need styled inputs. A page with plain unstyled HTML elements is a failed build.

Example of CORRECT home.html:
```html
{% extends "base.html" %}
{% block content %}
<div class="max-w-7xl mx-auto">
    <h1 class="text-3xl font-bold mb-6">Restaurants</h1>
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        {% for restaurant in object_list %}
        <div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
            <h2 class="font-semibold text-lg">{{ restaurant.name }}</h2>
            <p class="text-gray-500">{{ restaurant.location }}</p>
        </div>
        {% endfor %}
    </div>
</div>
{% endblock %}

6. **Navbar links must match the app** — the navigation must include links to the app's actual pages/models. E-commerce apps need Products/Cart/Categories. Dashboards need links to each management section. Public sites need relevant pages (Menu, About, Contact). "Home" and "Admin" alone is never acceptable — it means the AI didn't think about the app's structure.

## Design Quality — Base44/Replit-Level Polish (MANDATORY)

Every generated app must look production-ready, not like a scaffold. Apply these rules to EVERY template:

### Color & Atmosphere
1. **Never use plain gray (`bg-gray-50`, `text-gray-500`) as the dominant color.** Pick a brand color and use its lighter variants for backgrounds. `bg-indigo-50` > `bg-gray-50`.
2. **Use gradient heroes** — `bg-gradient-to-br from-indigo-600 to-purple-700` with white text makes any app look premium instantly.
3. **Dark mode-ready cards** — use `bg-white` cards on colored backgrounds, not gray cards on gray backgrounds.

### Cards & Lists
4. **Cards must have hover effects** — `hover:shadow-lg hover:-translate-y-1 transition-all duration-300` on every card.
5. **Stats cards need icons** — every stat must have a colored icon badge (`bg-indigo-100 text-indigo-600 rounded-lg p-2`) next to the number.
6. **Empty states must be designed** — never show "No items found" as plain text. Use an icon + styled message box.

### Typography & Spacing
7. **Hero sections need big type** — `text-5xl font-extrabold` for hero headings, `text-xl text-gray-300` for subtitles.
8. **Section spacing** — every section needs `py-16 md:py-24`, not `py-8`.
9. **Badge/tag styling** — use `px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-700` for labels.

### Interactive Elements
10. **Buttons need press feedback** — `active:scale-95 transition-transform` on every button.
11. **Form inputs need focus rings** — `focus:ring-2 focus:ring-indigo-500 focus:border-transparent` on every input.
12. **Navbar needs backdrop blur** — `bg-white/80 backdrop-blur-md` makes it feel native.

### Images & Media
13. **Use gradient placeholders for images** — `<div class="bg-gradient-to-br from-indigo-400 to-purple-500 w-full h-48 rounded-lg"></div>` instead of broken image icons.
14. **Avatar initials** — `rounded-full bg-indigo-600 text-white flex items-center justify-center` for user avatars.

### Example: CORRECT vs WRONG

WRONG (reads as scaffold):
```html
<div class="bg-gray-50 p-4">
    <h1 class="text-2xl">Products</h1>
    <div class="grid grid-cols-3 gap-4">
        <div class="border p-4">{{ product.name }}</div>
    </div>
</div> E-commerce apps need Products/Cart/Categories. Dashboards need links to each management section. Public sites need relevant pages (Menu, About, Contact). "Home" and "Admin" alone is never acceptable — it means the AI didn't think about the app's structure.

## DashboardView Pattern

DashboardView MUST always include a get_queryset or model. Never generate a bare ListView without one:

```python
class DashboardView(TemplateView):
    template_name = 'dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        context['total_teachers'] = Teacher.objects.count()
        return context

This is the defining base44/Lovable/Replit signature — a persistent left
sidebar with icons + labels, not a top navbar, for **Pattern A** apps per
`01_navigation_layout_decision.md`: dashboards, admin panels, and
data-heavy multi-page apps where a logged-in user spends most of their
time.

- **Consult `01_navigation_layout_decision.md` first.** Do not reach for
  this component by default — it applies only when the app has been
  classified as Pattern A.
- Use for: CRM, School/Hospital Management, Inventory, POS, Accounting, HR,
  Analytics, ERP, Project Management, LMS Teacher Portal, Admin Panels, or
  any other app whose primary surface is data-heavy and authenticated.
- Skip for:
  - Pattern B (public marketing/content sites — blog, portfolio, landing
    page, restaurant/hotel/church/NGO site) → use **Top Navbar — Public
    Site Layout** instead.
  - Pattern C (consumer apps — ecommerce, food ordering, streaming, social,
    booking, job board, dating, quiz, music, recipe, fitness) → use **Top
    Navbar — Consumer App Layout** instead.
  - Pattern D (workspace apps — Figma/Notion/Trello-style) → use
    **Workspace Shell** instead.
  - Pattern E (auth pages) → never use a sidebar; use **Auth Card Layout**.
  - Pattern F (wizards/checkout/multi-step forms) → never use a sidebar;
    use **Step Wizard Shell**.
- If uncertain which pattern applies, default to a top navigation, not this
  sidebar — see the Selection Rules in `01_navigation_layout_decision.md`.
- Includes its own built-in mobile drawer — satisfies the mobile-menu
  requirement on its own on Pattern A pages, no separate top navbar needed.

### App Shell — Sidebar Layout (Pattern A)

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

---

## Top Navbar — Public Site Layout (Pattern B)

For public-facing marketing/content sites (blog, portfolio, landing page, restaurant, hotel, church, NGO). Uses a clean top navbar with mobile drawer.

```html
<nav x-data="{ open: false }" class="sticky top-0 z-50 bg-white/80 backdrop-blur border-b border-gray-200">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="font-bold text-lg text-gray-900">{{ app_name }}</a>
                    <div class="hidden md:flex items-center gap-6 text-sm">
                                    <!-- APP-SPECIFIC LINKS: Generate based on app type. Public site = Menu, About, Contact. E-commerce = Products, Cart. Dashboard = management sections. Never just Home/Admin. -->
                    <a href="/" class="text-gray-600 hover:text-gray-900 transition-colors duration-200">Home</a>
                    <a href="/menu/" class="text-gray-600 hover:text-gray-900 transition-colors duration-200">Menu</a>
                    <a href="/contact/" class="text-gray-600 hover:text-gray-900 transition-colors duration-200">Contact</a>
                    <a href="/admin/" class="text-gray-600 hover:text-gray-900 transition-colors duration-200">Admin</a>
                </div>
            <button @click="open = true" class="md:hidden p-2 rounded-lg text-gray-600 focus:outline-none focus:ring-2 focus:ring-indigo-500" aria-label="Open menu">
                <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M4 6h16M4 12h16M4 18h16" /></svg>
            </button>
        </div>
    </div>
    <div x-show="open" x-trap.noscroll="open" @keydown.escape.window="open = false" class="fixed inset-0 z-50 md:hidden" style="display: none;">
        <div x-show="open" x-transition.opacity @click="open = false" class="fixed inset-0 bg-black/50"></div>
        <div x-show="open" x-transition:enter="transition ease-out duration-250" x-transition:enter-start="translate-x-full" x-transition:enter-end="translate-x-0" x-transition:leave="transition ease-in duration-200" x-transition:leave-start="translate-x-0" x-transition:leave-end="translate-x-full" class="fixed inset-y-0 right-0 w-72 bg-white border-l border-gray-200 p-6">
            <div class="flex justify-between items-center mb-8">
                <span class="font-bold text-gray-900">{{ app_name }}</span>
                <button @click="open = false" class="text-gray-500 p-1">&times;</button>
            </div>
            <a href="/" class="block px-3 py-2.5 rounded-lg text-gray-900 hover:bg-gray-50 transition-colors duration-200">Home</a>
            <a href="/admin/" class="block px-3 py-2.5 rounded-lg text-gray-900 hover:bg-gray-50 transition-colors duration-200">Admin</a>
        </div>
    </div>
</nav>

## If the app doesn't fit Pattern A, B, or C

Default to **Top Navbar — Public Site Layout (Pattern B)** with these links:
- Home
- The app's main feature pages (based on the models/views generated)
- Admin

**CRITICAL: Never just "Home" and "Admin".** Look at the models and views you generated. If you created a Student model with a ListView, add a "Students" link. If you created a Blog model, add a "Blog" link. The navbar must reflect what the app actually does. Two links means you didn't think about the app's structure.