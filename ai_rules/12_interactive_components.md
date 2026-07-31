# Alpine.js Interactive Components

**Requirement:** `base.html` MUST include Alpine.js CDN in `<head>`, AFTER Tailwind CDN.

## MANDATORY: Every generated app must have a proper navbar/footer

- **base.html** MUST contain: complete `<nav>` with logo + links, `<main>` block, and `<footer>`
- **Mobile**: navbar MUST collapse to hamburger menu below `md` breakpoint
- **No exceptions**: bare cards without nav/footer = broken output

## Plugin Requirements
| Component | Requires |
|---|---|
| Modal, Mobile Nav | Focus plugin |
| Accordion | Collapse plugin |

Load plugins BEFORE core Alpine:
```html
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/focus@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/@alpinejs/collapse@3.x.x/dist/cdn.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>