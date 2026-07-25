# Requirements Analysis — Design Before Coding

Before generating ANY code, analyze the application and determine exactly what each module needs.

## The Golden Rule

**Do NOT automatically generate CRUD for every model.** Only build what each module actually needs.

## Two Application Patterns

### Pattern 1: Public Blog (Customer-Facing)

**Signals:** blog, articles, news, content site, public, visitors, readers, comments

**What visitors need:**
- Read-only ListView + DetailView for published content (no auth required)
- Comment form (may or may not require login — check the prompt)
- Category/tag filtering and search

**What staff need:**
- Full CRUD via Django Admin only — do NOT build a separate staff-facing CreateView/UpdateView/DeleteView unless the prompt explicitly asks for an author dashboard
- Draft/published status field so unpublished posts don't appear publicly

**Do NOT generate:** Public-facing create/edit/delete views for content — that's what /admin/ is for, unless the user explicitly asks for a "writer dashboard" or "submit a post" feature.

---

### Pattern 2: Private Record-Management System

**Signals:** system, records, management, staff, employee, internal, student, HR, inventory, attendance — see `09_skill_templates.md` for the full trigger-word list

**What staff/admins need:**
- Full CRUD via Django Admin (list_display, list_filter, search_fields, exports)
- A dashboard home page with real statistics — counts, breakdowns, recent activity
- LoginRequiredMixin on any page that isn't the public login screen

**What the general public needs:** Nothing, by default. This pattern has no public-facing pages unless the prompt explicitly says otherwise (e.g. "students should be able to log in and view their own grades").

**Do NOT generate:** A public homepage, public list/detail pages, or a signup flow — private systems don't get accounts created by strangers. If the prompt implies self-service accounts (e.g. "students register themselves"), that's a signal to blend in elements of Pattern 3 below rather than staying purely private.

---

### Pattern 3: Public SaaS / Multi-User App (hybrid of the two above)

**Signals:** dashboard, accounts, "each user has their own...", task manager, expense tracker, personal — anything implying every visitor gets their own private data, not shared public content

**What it needs:**
- Full authentication: login, logout, signup (per `05_validation.md`'s Auth Requirements)
- Every view that shows user-owned data MUST filter by `self.request.user` and inherit `LoginRequiredMixin`
- A per-user dashboard as the home page, not a generic public landing page
- Full CRUD for the user's own records (Create/Update/Delete restricted to records they own — never let one user edit another's data)

**Do NOT generate:** A separate admin-only view of all users' data unless explicitly asked — Django Admin already covers that for staff.

---

## Decision Checklist

Before writing any code, answer:
1. Does ANYONE outside staff/admins use this app? → If no, Pattern 2 (Private).
2. Do visitors only ever READ content, never create/own it? → Pattern 1 (Public Blog).
3. Does each user create/own their own private data? → Pattern 3 (Public SaaS).
4. If genuinely unsure, default to Pattern 2 (Private) — it's the safer, smaller-surface-area choice, and it's easier for the user to ask for public pages afterward than to strip out unwanted auth complexity.