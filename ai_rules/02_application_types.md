# Application Classification

⚠️ This decision happens FIRST, before any UI pattern, footer, or
Design System selection — those all read `app_type` as an input, they
don't influence it. Get this step right and everything downstream
follows correctly.

---

## Step 1 — Determine Access Model (who uses it)

| Access Model | Primary Users | Generate |
|---|---|---|
| **Private** | Administrators, staff only | Models, Django Admin (full config, ExportAdminMixin), NO public frontend unless explicitly asked |
| **Public** | Customers, students, parents, teachers, employees, general users | Models, Django Admin, public pages (home/list/detail/forms), user dashboard where appropriate |

**Decision Rule:** If ONLY administrators/staff interact with the system → Private. If ANYONE outside administration (even a single named role like "customer" or "student") interacts with it → Public. When in doubt, default to **Public** — it's the safer assumption for real-world usage and costs nothing extra if some pages end up admin-only anyway.

---

## Step 2 — Determine App Type (what kind of app this is)

This is the classification that `thinking.app_type` MUST reflect, and
it is INDEPENDENT of Step 1 — a Games app can be Public, a Dashboard
can be Private. Pick exactly ONE. This value drives UI Pattern
selection (structure + Design System) downstream — get it wrong here
and every visual decision after it will be wrong too.

| App Type | Trigger Signals (any ONE of these in the core request is enough) |
|---|---|
| **CRUD / Records System** | "manage," "track," "records," "database of," generic list/add/edit/delete of some entity, no other signal below applies |
| **Content / Blog / Publication** | "blog," "articles," "posts," "publish," "news," primarily READ-facing content, not user-generated |
| **E-commerce / Marketplace** | "sell," "buy," "cart," "checkout," "products," "orders," "payment," "inventory" |
| **Dashboard / Analytics** | "dashboard," "analytics," "metrics," "KPI," "reports," "monitor," "insights" — AND the charts/numbers ARE the primary content, not a side feature of a CRUD app |
| **Games / Quizzes / Gamified** | "quiz," "trivia," "streak," "leaderboard," "points," "score," "level up," "badges," "challenge," "game" — if ANY of these describe the CORE mechanic, this wins over every other category, even if the app also has user accounts or admin-managed content |
| **Booking / Scheduling** | "book," "appointment," "reserve," "calendar," "schedule," "availability" |
| **Portfolio / Personal Brand** | "portfolio," "personal website," "showcase my work," "resume," "about me" — see Content Sections rule below, this is NOT automatically static |
| **Education / LMS / Student Portal** | "course," "student," "enrollment," "grade," "curriculum," "learning," "bootcamp," "class" — but check Games signals FIRST; a gamified learning app is Games, not this |
| **Internal Tool / Admin System** | Pure Private-access-model apps with no distinct type above — staff records, inventory management, internal reporting |

**Priority order when multiple signals appear:** Games > E-commerce > Dashboard > Booking > Education > Content > Portfolio > CRUD (generic fallback). Games wins over Education specifically because a gamified learning app's core UX (scores, streaks, leaderboards) needs Design System G, not the standard Education styling — the learning *subject matter* doesn't change what the *interaction pattern* needs.

**Default when genuinely ambiguous:** CRUD / Records System — it's the safest fallback and matches the most common real-world request pattern (an entity with fields, managed via admin, sometimes shown to users).

---

## Step 3 — Cross-Check Before Finalizing

Before writing `thinking.app_type`, verify it against what you're
actually about to generate:

- If you classified as Games but aren't planning score/streak/leaderboard
  models and views — you misclassified. Re-check Step 2's trigger table.
- If you classified as Private but the request mentions ANY named
  end-user role (student, customer, patient, member) interacting with
  it — you misclassified. Re-check Step 1.
- `thinking.app_type` must be one of the exact category names from the
  Step 2 table (e.g. "Games / Quizzes / Gamified", not a paraphrase
  like "Public SaaS" or "Interactive App") — downstream UI pattern
  selection matches on these exact category names.

---

## Content Sections MUST Be Data-Driven, Not Hardcoded

If the user's request includes repeatable content sections — Projects,
Skills, Experience, Testimonials, Portfolio items, Team members,
Products, Services, etc. — these MUST be real Django models manageable
through the admin panel, NOT hardcoded HTML in the template.

This applies even for "static-feeling" sites like portfolios and landing
pages. A "Projects" section is not static content — it's data the user
will want to add/edit/remove over time without touching code. For each
repeatable content type mentioned in the request, generate:

- A model with real fields matching what the section displays
  (e.g. `Project`: title, description, image, link, technologies)
- A view that queries the model and passes it to the template
- Admin registration so the content can be managed via /admin/
- A template that loops over the queried data with `{% for %}`,
  never hardcoded repeated HTML blocks

Only skip a model for genuinely non-repeating, single-instance content
(e.g. a one-time "About Me" paragraph, a single hero headline). Even
then, prefer a simple singleton model if the user might want to edit
it without redeploying.

A "Contact Form" needs a model too (to store submissions) — but its
content isn't admin-editable the way Projects/Skills are; it's a form
that writes new rows, not a list of rows to display.

⚠️ A "portfolio website with projects, skills, and experience" is a
**Public** access model, **Portfolio / Personal Brand** app type,
requiring models for Project, Skill, and Experience — it is NOT a
static site with no database, even though it may feel content-light.
Treat every named repeatable section as a model unless the request
explicitly says "static" or "no database needed."