# Application Classification

## Private Application
**Purpose:** Internal use only
**Primary Users:** Administrators, Staff
**Generate:**
- Django models
- Django Admin (full configuration with ExportAdminMixin)
- Authentication (if needed)
- Reports (if requested)
**Do NOT generate:** Public frontend pages unless explicitly asked.

## Public Application
**Purpose:** Users interact through a website
**Primary Users:** Customers, Students, Parents, Teachers, Employees
**Generate:**
- Django models
- Django Admin
- Authentication
- Public pages (home, list, detail, forms)
- User dashboard (when appropriate)
- Forms and business workflows

## Decision Rule
- If ONLY administrators/staff use it → **Private Application**
- If people outside administration use it → **Public Application**

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
**Public Application** requiring models for Project, Skill, and
Experience — it is NOT a static site with no database, even though it
may feel content-light. Treat every named repeatable section as a
model unless the request explicitly says "static" or "no database
needed."