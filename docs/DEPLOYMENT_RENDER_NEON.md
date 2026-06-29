# Deploying the Demo to Render and Neon

This guide is for a free or low-cost hosted demo. It is not a production deployment guide and not a clinical pilot guide.

The online demo must stay clearly marked:

```text
DEMO ONLY — NOT FOR REAL PATIENT CARE
```

Do not enter real patient data. Do not claim medical validation.

## What You Need

- A GitHub repository with this project pushed.
- A free Neon account for PostgreSQL.
- A free Render account for the FastAPI web service.

Free tiers can sleep, restart, or change limits. That is acceptable for feedback demos, but not acceptable for clinical use.

## 1. Create the Neon Database

1. Open Neon.
2. Create a new project.
3. Create or use the default PostgreSQL database.
4. Copy the database connection string.
5. If Neon provides a pooled and direct connection string, start with the direct connection string for migrations.
6. Make sure the connection string starts with `postgresql://` or `postgres://`.
7. Paste it into Render as `DATABASE_URL`. The app automatically converts standard Neon PostgreSQL URLs to the installed `psycopg` driver.

The normalized internal form looks like:

```text
postgresql+psycopg://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

Keep the real value private. Do not paste it into GitHub files.

## 2. Create the Render Web Service

1. Open Render.
2. Create a new Web Service.
3. Connect the GitHub repository.
4. Choose Docker as the runtime.
5. Use the included `Dockerfile`.
6. Use the default Docker start command from the repository:

```text
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

7. Set the health check path to:

```text
/health
```

The included `render.yaml` is a starting Blueprint. It intentionally does not contain real secrets.

## 3. Set Render Environment Variables

Set these values in the Render dashboard:

```text
APP_ENV=demo
DEMO_MODE=true
DATABASE_URL=your-neon-sqlalchemy-url
API_KEY_PEPPER=generate-a-long-random-secret-in-render
DEMO_API_KEY=generate-a-demo-key-for-this-hosted-demo
DEMO_TENANT_ID=tenant_demo
CORS_ALLOWED_ORIGINS=https://your-render-service.onrender.com
LOG_LEVEL=INFO
RATE_LIMIT_PER_MINUTE=120
```

Do not use the local demo key online.

## 4. Deploy

1. Click deploy in Render.
2. Wait for the build to finish.
3. Open the Render public URL.
4. Confirm these pages load:

```text
/
/guided-demo
/health
/ready
/demo
/docs
/redoc
```

At this point the API may be running before the database has tables. If `/ready` shows the database is not ready, run migrations and seed demo data.

## 5. Initialize the Hosted Demo Database

Use Render Shell or a one-off job if available. Run:

```bash
./scripts/hosted_demo_init.sh
```

This runs:

```bash
alembic upgrade head
python -m app.seed
```

The seed command creates only:

- fake demo tenant;
- hashed demo API key;
- demo-only protocols;
- demo-only rules.

It does not seed real patient data.

## 6. Verify the Hosted Demo

Open these URLs using your Render public HTTPS URL:

```text
https://your-render-service.onrender.com/
https://your-render-service.onrender.com/guided-demo
https://your-render-service.onrender.com/health
https://your-render-service.onrender.com/ready
https://your-render-service.onrender.com/demo
https://your-render-service.onrender.com/docs
https://your-render-service.onrender.com/redoc
```

Start with `/`. It should immediately explain MedProtocol API in business language for non-technical reviewers.

Then run one fake case in `/guided-demo` and confirm:

- warning banner is visible;
- no real patient data is requested;
- a fake result appears;
- an audit ID is generated;
- raw JSON is hidden by default under technical details.

Use `/docs` only for API or technical review. Use `/demo` only as the Technical Demo Console for developers.

## 7. Stop or Delete the Online Demo

If you no longer want the demo online:

1. Pause or delete the Render web service.
2. Delete the Neon database if it is no longer needed.
3. Delete any demo API key values from provider dashboards.

## Important Limits

- This is not production hosting.
- Free services may sleep or become temporarily unavailable.
- No real patient data may be entered.
- No real clinical rules may be added.
- No diagnosis, treatment, medication, dosage, prescription, or procedure logic may be added.
