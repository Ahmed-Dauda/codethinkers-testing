# UI Patterns — Auto-Selected by App Type

Every project MUST include a footer, a navbar, and use the icon card
pattern for dashboard/feature/stat sections. They are automatically
selected based on the application type.

⚠️ IMPORTANT: All HTML examples below are COMPLETE code to copy directly
into templates. Do NOT use `{% include %}` for these — just paste the
HTML directly.

⚠️ Two variants exist for each element per app type (A and B). Pick
ONE variant per element — do not mix, and do not use both A and B in
the same project. If unsure which variant, default to **A**.

⚠️ CRITICAL — AUTH-DEPENDENT LINKS: Some navbar variants below contain
`{% url 'login' %}`, `{% url 'logout' %}`, or `{% url 'signup' %}`.
These URL names only exist if you are ALSO generating a real
authentication system (login/logout/signup views, urls, and templates)
in this build. For admin-managed CRUD apps — the default unless the
user explicitly requests public self-service signup/login — DO NOT use
those tags. Use a plain `<a href="/admin/">Admin</a>` link instead.
Leaving a `{% url 'login' %}`/`{% url 'logout' %}`/`{% url 'signup' %}`
tag with no matching URL definition crashes the page with
`NoReverseMatch` the instant it renders — this is a hard requirement,
not a style preference.

---

## Selection Table

| App Type | Footer | Navbar | Card |
|----------|--------|--------|------|
| Private / Admin-Only / Staff Records / Internal | Footer 1A/1B | Navbar 1A/1B | Card 1A/1B |
| Public Blog / Content / Read-Only / Articles | Footer 2A/2B | Navbar 2A/2B | Card 2A/2B |
| Public Full CRUD / SaaS / Dashboard / User Accounts | Footer 3A/3B | Navbar 3A/3B | Card 3A/3B |
| Education / School / LMS / CBT / Student Portal | Footer 4A/4B | Navbar 4A/4B | Card 4A/4B |

**If the app has ANY public-facing pages, use Footer/Navbar/Card 2, 3, or
4 — NOT the Private (1) set.**

---

# 1. Private / Admin-Only System

## Footer 1A: Simple

```html
<footer class="bg-gray-800 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-6 text-center text-sm text-gray-400">
        &copy; {% now "Y" %} {{ app_name }}. Internal use only. All rights reserved.
    </div>
</footer>
```

## Footer 1B: With System Links

```html
<footer class="bg-gray-900 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-6 flex flex-col md:flex-row items-center justify-between gap-4">
        <p class="text-sm text-gray-400">&copy; {% now "Y" %} {{ app_name }}. Internal use only.</p>
        <div class="flex gap-6 text-sm text-gray-400">
            <a href="/admin/" class="hover:text-white transition">Admin Panel</a>
            <a href="#" class="hover:text-white transition">Support</a>
            <a href="#" class="hover:text-white transition">System Status</a>
        </div>
    </div>
</footer>
```

## Navbar 1A: Simple Bar

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-bold text-indigo-600">{{ app_name }}</a>
            <div class="flex items-center gap-6">
                <a href="/" class="text-gray-600 hover:text-indigo-600 transition">Dashboard</a>
                <a href="/admin/" class="text-gray-600 hover:text-indigo-600 transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Navbar 1B: Dark Top Bar

```html
<nav class="bg-gray-900 text-white sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-green-400"></span>
                <a href="/" class="text-xl font-bold">{{ app_name }}</a>
            </div>
            <div class="flex items-center gap-6 text-sm text-gray-300">
                <a href="/" class="hover:text-white transition">Dashboard</a>
                <a href="/admin/" class="hover:text-white transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Card 1A: Stat Card with Icon

```html
<div class="bg-white rounded-lg shadow p-6 flex items-center gap-4">
    <div class="bg-indigo-100 text-indigo-600 rounded-full p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 17v-2a4 4 0 014-4h3m0 0l-3-3m3 3l-3 3M4 7h6m-6 4h6m-6 4h6" />
        </svg>
    </div>
    <div>
        <p class="text-sm text-gray-500">Total Records</p>
        <p class="text-2xl font-bold text-gray-900">{{ total_count }}</p>
    </div>
</div>
```

## Card 1B: Alert/Status Card with Icon

```html
<div class="bg-white rounded-lg shadow p-6 border-l-4 border-amber-500">
    <div class="flex items-start gap-3">
        <div class="bg-amber-100 text-amber-600 rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M12 9v2m0 4h.01M10.29 3.86l-8.18 14.18A2 2 0 004 21h16a2 2 0 001.89-2.96L13.71 3.86a2 2 0 00-3.42 0z" />
            </svg>
        </div>
        <div>
            <p class="font-semibold text-gray-900">Needs Attention</p>
            <p class="text-sm text-gray-500">{{ alert_count }} items pending review</p>
        </div>
    </div>
</div>
```

---

# 2. Public Blog / Content

## Footer 2A: 3-Column

```html
<footer class="bg-gray-800 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
                <h3 class="text-lg font-semibold mb-4">{{ app_name }}</h3>
                <p class="text-gray-400 text-sm">Your source for quality content.</p>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Quick Links</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="/" class="hover:text-white transition">Home</a></li>
                    <li><a href="/admin/" class="hover:text-white transition">Admin</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Connect</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="#" class="hover:text-white transition">Twitter</a></li>
                    <li><a href="#" class="hover:text-white transition">LinkedIn</a></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
            &copy; {% now "Y" %} {{ app_name }}. All rights reserved.
        </div>
    </div>
</footer>
```

## Footer 2B: Newsletter Signup

```html
<footer class="bg-gray-800 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="flex flex-col md:flex-row justify-between items-center gap-6 border-b border-gray-700 pb-8">
            <div>
                <h3 class="text-lg font-semibold">{{ app_name }}</h3>
                <p class="text-gray-400 text-sm mt-1">Never miss a new post.</p>
            </div>
            <form class="flex gap-2 w-full md:w-auto">
                <input type="email" placeholder="Your email" class="px-4 py-2 rounded bg-gray-700 text-white text-sm flex-1 md:w-64" />
                <button type="submit" class="bg-indigo-600 hover:bg-indigo-700 transition px-4 py-2 rounded text-sm font-semibold">Subscribe</button>
            </form>
        </div>
        <div class="mt-6 text-center text-sm text-gray-400">
            &copy; {% now "Y" %} {{ app_name }}. All rights reserved.
        </div>
    </div>
</footer>
```

## Navbar 2A: Sticky with Search

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16 gap-4">
            <a href="/" class="text-xl font-bold text-indigo-600 whitespace-nowrap">{{ app_name }}</a>
            <input type="text" placeholder="Search articles..." class="hidden md:block border border-gray-300 rounded px-3 py-1.5 text-sm w-64 focus:outline-none focus:ring-2 focus:ring-indigo-500" />
            <div class="flex items-center gap-6">
                <a href="/" class="text-gray-600 hover:text-indigo-600 transition">Home</a>
                <a href="#" class="text-gray-600 hover:text-indigo-600 transition">Categories</a>
            </div>
        </div>
    </div>
</nav>
```

## Navbar 2B: Centered Logo

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 py-3">
        <div class="text-center mb-2">
            <a href="/" class="text-2xl font-bold text-indigo-600 tracking-tight">{{ app_name }}</a>
        </div>
        <div class="flex justify-center gap-8 text-sm text-gray-600 border-t border-gray-100 pt-2">
            <a href="/" class="hover:text-indigo-600 transition">Home</a>
            <a href="#" class="hover:text-indigo-600 transition">Categories</a>
            <a href="#" class="hover:text-indigo-600 transition">About</a>
            <a href="#" class="hover:text-indigo-600 transition">Contact</a>
        </div>
    </div>
</nav>
```

## Card 2A: Article Preview Card with Icon

```html
<div class="bg-white rounded-lg shadow overflow-hidden">
    <img src="https://picsum.photos/600/400?random={{ forloop.counter }}" class="w-full h-40 object-cover" alt="{{ post.title }}" />
    <div class="p-5">
        <div class="flex items-center gap-2 text-indigo-600 text-xs font-semibold mb-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
            </svg>
            {{ post.category }}
        </div>
        <h3 class="font-bold text-gray-900 mb-2">{{ post.title }}</h3>
        <p class="text-sm text-gray-500">{{ post.excerpt }}</p>
    </div>
</div>
```

## Card 2B: Category Card with Icon

```html
<a href="#" class="bg-white rounded-lg shadow p-6 flex items-center gap-4 hover:shadow-md transition">
    <div class="bg-indigo-100 text-indigo-600 rounded-full p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h4l2 2h8a2 2 0 012 2v1M5 20h14a2 2 0 002-2v-6a2 2 0 00-2-2H9a2 2 0 00-2 2v6a2 2 0 01-2 2z" />
        </svg>
    </div>
    <div>
        <p class="font-semibold text-gray-900">{{ category.name }}</p>
        <p class="text-sm text-gray-500">{{ category.post_count }} posts</p>
    </div>
</a>
```

---

# 3. Public SaaS / Dashboard

## Footer 3A: 4-Column

```html
<footer class="bg-gray-800 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <h3 class="text-lg font-semibold mb-4">{{ app_name }}</h3>
                <p class="text-gray-400 text-sm">Built with Django & Tailwind CSS.</p>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Product</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="/" class="hover:text-white transition">Home</a></li>
                    <li><a href="/admin/" class="hover:text-white transition">Admin</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Support</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="#" class="hover:text-white transition">Help Center</a></li>
                    <li><a href="#" class="hover:text-white transition">Contact</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Legal</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="#" class="hover:text-white transition">Privacy</a></li>
                    <li><a href="#" class="hover:text-white transition">Terms</a></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
            &copy; {% now "Y" %} {{ app_name }}. All rights reserved.
        </div>
    </div>
</footer>
```

## Footer 3B: Simple Band

```html
<footer class="bg-gray-800 text-white mt-auto">
    <div class="bg-indigo-600">
        <div class="max-w-7xl mx-auto px-4 py-8 text-center">
            <h3 class="text-xl font-bold">{{ app_name }}</h3>
            <p class="text-indigo-100 text-sm mt-1">Built with Django & Tailwind CSS.</p>
        </div>
    </div>
    <div class="max-w-7xl mx-auto px-4 py-6 flex flex-col md:flex-row justify-between items-center gap-4 text-sm text-gray-400">
        <p>&copy; {% now "Y" %} {{ app_name }}. All rights reserved.</p>
        <div class="flex gap-6">
            <a href="/admin/" class="hover:text-white transition">Admin</a>
            <a href="#" class="hover:text-white transition">Contact</a>
        </div>
    </div>
</footer>
```

## Navbar 3A: Standard Bar

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-bold text-indigo-600">{{ app_name }}</a>
            <div class="flex items-center gap-6">
                <a href="/" class="text-gray-600 hover:text-indigo-600 transition">Home</a>
                <a href="/admin/" class="text-gray-600 hover:text-indigo-600 transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Navbar 3B: With Avatar Placeholder

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-bold text-indigo-600">{{ app_name }}</a>
            <div class="flex items-center gap-6">
                <a href="/" class="text-gray-600 hover:text-indigo-600 transition">Dashboard</a>
                <a href="/admin/" class="text-gray-600 hover:text-indigo-600 transition">Admin</a>
                <div class="w-8 h-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center text-sm font-semibold">
                    A
                </div>
            </div>
        </div>
    </div>
</nav>
```

## Card 3A: Feature Card with Icon

```html
<div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
    <div class="bg-indigo-100 text-indigo-600 rounded-lg w-12 h-12 flex items-center justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
    </div>
    <h3 class="font-bold text-gray-900 mb-2">{{ feature.title }}</h3>
    <p class="text-sm text-gray-500">{{ feature.description }}</p>
</div>
```

## Card 3B: Stat Card with Trend Icon

```html
<div class="bg-white rounded-lg shadow p-6">
    <div class="flex items-center justify-between mb-2">
        <p class="text-sm text-gray-500">{{ stat.label }}</p>
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
    </div>
    <p class="text-2xl font-bold text-gray-900">{{ stat.value }}</p>
</div>
```

---

# 4. Education / School / LMS

## Footer 4A: Community & Resources

```html
<footer class="bg-indigo-950 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8">
        <div class="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
                <h3 class="text-lg font-semibold mb-4">{{ app_name }}</h3>
                <p class="text-gray-400 text-sm">Empowering students to succeed.</p>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Community</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="/" class="hover:text-white transition">Home</a></li>
                    <li><a href="#" class="hover:text-white transition">Academic Calendar</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Resources</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="#" class="hover:text-white transition">Parent Portal</a></li>
                    <li><a href="#" class="hover:text-white transition">Contact Staff</a></li>
                </ul>
            </div>
            <div>
                <h4 class="text-lg font-semibold mb-4">Legal</h4>
                <ul class="space-y-2 text-sm text-gray-400">
                    <li><a href="#" class="hover:text-white transition">Privacy</a></li>
                    <li><a href="#" class="hover:text-white transition">Accessibility</a></li>
                </ul>
            </div>
        </div>
        <div class="border-t border-gray-700 mt-8 pt-6 text-center text-sm text-gray-400">
            &copy; {% now "Y" %} {{ app_name }}. All rights reserved.
        </div>
    </div>
</footer>
```

## Footer 4B: Contact & Social

```html
<footer class="bg-indigo-950 text-white mt-auto">
    <div class="max-w-7xl mx-auto px-4 py-8 flex flex-col md:flex-row justify-between items-center gap-6">
        <div class="text-center md:text-left">
            <h3 class="text-lg font-semibold">{{ app_name }}</h3>
            <p class="text-gray-400 text-sm mt-1">Questions? Reach out to our office.</p>
        </div>
        <div class="flex gap-6 text-sm text-gray-400">
            <a href="#" class="hover:text-white transition">Admissions</a>
            <a href="#" class="hover:text-white transition">Staff Directory</a>
            <a href="#" class="hover:text-white transition">Contact</a>
        </div>
    </div>
    <div class="border-t border-gray-800 py-4 text-center text-sm text-gray-500">
        &copy; {% now "Y" %} {{ app_name }}. All rights reserved.
    </div>
</footer>
```

## Navbar 4A: Portal Links

```html
<nav class="bg-white shadow sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4">
        <div class="flex justify-between items-center h-16">
            <a href="/" class="text-xl font-bold text-indigo-700">{{ app_name }}</a>
            <div class="flex items-center gap-6">
                <a href="/" class="text-gray-600 hover:text-indigo-700 transition">Home</a>
                <a href="/admin/" class="text-gray-600 hover:text-indigo-700 transition">Admin</a>
            </div>
        </div>
    </div>
</nav>
```

## Navbar 4B: With Announcement Bar

```html
<div>
    <div class="bg-indigo-700 text-white text-center text-xs py-1.5 px-4">
        Enrollment for the next term is now open.
    </div>
    <nav class="bg-white shadow sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4">
            <div class="flex justify-between items-center h-16">
                <a href="/" class="text-xl font-bold text-indigo-700">{{ app_name }}</a>
                <div class="flex items-center gap-6">
                    <a href="/" class="text-gray-600 hover:text-indigo-700 transition">Home</a>
                    <a href="/admin/" class="text-gray-600 hover:text-indigo-700 transition">Admin</a>
                </div>
            </div>
        </div>
    </nav>
</div>
```

## Card 4A: Course Card with Icon

```html
<div class="bg-white rounded-lg shadow p-6 hover:shadow-md transition">
    <div class="bg-indigo-100 text-indigo-700 rounded-lg w-12 h-12 flex items-center justify-center mb-4">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
        </svg>
    </div>
    <h3 class="font-bold text-gray-900 mb-1">{{ course.title }}</h3>
    <p class="text-sm text-gray-500">{{ course.description }}</p>
</div>
```

## Card 4B: Progress/Achievement Card with Icon

```html
<div class="bg-white rounded-lg shadow p-6 flex items-center gap-4">
    <div class="bg-amber-100 text-amber-600 rounded-full p-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path stroke-linecap="round" stroke-linejoin="round" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
    </div>
    <div>
        <p class="text-sm text-gray-500">Current Grade</p>
        <p class="text-2xl font-bold text-gray-900">{{ student.grade }}%</p>
    </div>
</div>
```

---

## Base Template Requirement (still applies)

`base.html` MUST contain:
- `<!DOCTYPE html>` structure
- Tailwind CSS CDN in `<head>`
- The chosen navbar variant inside `{% block navbar %}{% endblock %}`
- Flash messages area
- `{% block content %}{% endblock %}` for page content
- The chosen footer variant inside `{% block footer %}{% endblock %}`

Every other template MUST extend `base.html`:

```html
{% extends "base.html" %}
{% block content %}
...page content...
{% endblock %}
```

Never generate a standalone page template with its own `<!DOCTYPE html>`.