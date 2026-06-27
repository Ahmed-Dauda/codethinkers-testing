# Daily Development Workflow — CodeThinkers

## Branch Strategy

Maintain these branches at all times:

* `development` → Active development. Does not deploy anywhere — just your working branch and GitHub backup.
* `staging` → Reviewed features ready for production. Deploys automatically to `https://staging.codethinkers.org`.
* `main` → Production branch. Deploys automatically to `https://codethinkers.org`.

---

# Daily Development Process

## Step 1 — Start from `development`

Always begin new work on the `development` branch.

```bash
git branch
git checkout development
git pull origin development
```

---

## Step 2 — Develop

* Implement your changes.
* Test locally.
* Ensure there are no obvious errors before committing.

---

## Step 3 — Push to `development`

```bash
git add .
git commit -m "feat: describe what you changed"
git push origin development
```

This only backs up your work to GitHub. It does not deploy anywhere yet.

---

## Step 4 — Merge to `staging` and test

```bash
git checkout staging
git pull origin staging
git merge development
git push origin staging
```

After deployment:

* Wait for the deployment notification.
* Open `https://staging.codethinkers.org`.
* Test the new feature thoroughly.
* Verify existing functionality still works

Only proceed to production if staging passes all tests.

---

## Step 5 — Tag current production before touching it

**Always do this before merging anything into `main`** — it's your rollback point if the new deployment fails.

```bash
git checkout main
git pull origin main
git tag -a v1.x-stable -m "describe what's in this stable release"
git push origin v1.x-stable
```

Increment the version each time (`v1.1-stable`, `v1.2-stable`, etc.) so you can always identify and return to a specific past release.

**Example:**
```bash
git tag -a v1.1-stable -m "Added project preview links, fixed ALLOWED_HOSTS config"
git push origin v1.1-stable
```

---

## Step 6 — Deploy to Production

Merge tested and reviewed code from `staging` into `main`.

```bash
git merge staging --no-ff -m "deploy: describe what you are releasing"
git push origin main
```

Wait for deployment to complete, then verify production:

* Visit `codethinkers.org`.
* Test the newly deployed feature.
* Confirm no regressions exist.

If everything works, you're done — the tag from Step 5 stays as your safety net for next time.

---

# Rollback Procedure

If a production deployment fails — or you need to return to any earlier confirmed-stable release — reset `main` to the relevant tag:

```bash
git checkout main
git reset --hard v1.x-stable
git push origin main --force
```

Replace `v1.x-stable` with the specific tag you need (e.g. the tag from Step 5 for the most recent rollback, or an older tag like `v1.0-stable` for a historical release).

You can also trigger the rollback workflow manually from GitHub Actions, if configured.

---

# Commit Message Convention

Use clear commit prefixes:

```text
feat: add new project preview feature
fix: resolve file upload not saving issue
style: update dashboard colors
refactor: clean up webprojects views
hotfix: critical login bug
```

---

# Weekly Maintenance — Sync Staging Database with Production

Keep staging realistic by refreshing it from production data periodically (e.g. weekly).

```bash
# On the server — dump production
sudo -u postgres /usr/lib/postgresql/17/bin/pg_dump -Fc codethinkers > /tmp/codethinkers_for_staging.dump

# Drop and recreate the staging database cleanly
sudo -u postgres psql -c "DROP DATABASE IF EXISTS codethinkers_staging;"
sudo -u postgres psql -c "CREATE DATABASE codethinkers_staging OWNER codethinkers_user;"

# Restore into staging (always use the matching pg_restore version — see note below)
sudo -u postgres /usr/lib/postgresql/17/bin/pg_restore -d codethinkers_staging /tmp/codethinkers_for_staging.dump --no-owner --role=codethinkers_user

# Verify the restore
sudo -u postgres /usr/lib/postgresql/17/bin/psql -d codethinkers_staging -c "SELECT count(*) FROM auth_user;"
```

After restoring, apply any pending migrations on staging (this is additive and safe — it won't touch existing rows):

```bash
cd /var/www/codethinkers-staging
python manage.py migrate
systemctl restart codethinkers-staging
```

**Important — Postgres version note:** this server has both Postgres 16 and 17 installed (`/usr/lib/postgresql/16/bin` and `/usr/lib/postgresql/17/bin`). The default `pg_dump`/`pg_restore` on PATH may resolve to v16, while `psql` resolves to v17. Always use the explicit `/usr/lib/postgresql/17/bin/...` path for dump/restore operations to avoid a `"unsupported version in file header"` error.

---

# Database Reference

| Environment | Database name          | DB user            | `.env` location                          |
|-------------|-------------------------|---------------------|--------------------------------------------|
| Production  | `codethinkers`          | `codethinkers_user` | `/var/www/codethinkers/.env`               |
| Staging     | `codethinkers_staging`  | `codethinkers_user` | `/var/www/codethinkers-staging/.env`       |

Production and staging are **separate Postgres databases** on the same server, under the same DB user role. They must never share a `DATABASE_URL` — keeping them isolated means staging experiments can never corrupt live production data.

---

# Rules

* Always develop on `development` — never deploy from it directly.
* Never push directly to `main` without testing on staging first.
* Test every feature on `https://staging.codethinkers.org` before merging to `main`.
* Always tag the current `main` **before** merging new code into it.
* Verify production immediately after every deployment.
* Use stable tags for rollback whenever something breaks.
* Never let staging and production point at the same database — verify `DATABASE_URL` in both `.env` files if anything looks off.
* Take a fresh `pg_dump` backup of production before any risky migration or manual database operation.
* Rotate any credential (API keys, DB passwords, server passwords) immediately if it's ever pasted into a chat, ticket, or shared document.