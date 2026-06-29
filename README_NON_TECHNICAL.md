# MedProtocol API Local Demo Guide for macOS

This guide assumes you are not technical.

The demo is only for fake test cases. It is not for real patient care. Do not enter real patient data.

## What You Need First

Install Docker Desktop for Mac:

https://www.docker.com/products/docker-desktop/

Docker Desktop lets this project run in a self-contained local environment. You do not need to install Python, PostgreSQL, uv, or any developer tools yourself.

Before starting the demo:

1. Open Docker Desktop.
2. Wait until Docker says it is running.
3. Keep Docker Desktop open.

## Start the Demo

The easiest option is double-click:

```text
start_demo.command
```

If macOS blocks it, right-click the file, choose Open, then confirm.

When startup succeeds, the terminal window will show:

```text
MedProtocol API local demo is ready.
```

## Open the Landing Page

Open this in your browser:

http://localhost:8000

You should see a banner:

```text
DEMO ONLY — NOT FOR REAL PATIENT CARE
```

Click:

```text
Open Demo UI
```

Or open the demo page directly:

http://localhost:8000/demo

## Test Fake Cases

On the demo page, click the fake case buttons:

- Child with danger signs
- Child without danger signs
- Pregnant woman with danger signs
- Missing critical data
- Community health worker scope
- Nurse scope

Each click should show:

- urgency level;
- referral required yes/no;
- immediate action;
- danger signs detected;
- missing critical data;
- short SMS/USSD message;
- protocol and rule metadata;
- audit ID;
- raw JSON response.

Only use the fake cases. Do not type or paste real patient information anywhere.

## Open Swagger Docs

Swagger is the technical API documentation page:

http://localhost:8000/docs

ReDoc is another documentation view:

http://localhost:8000/redoc

You do not need to understand these pages to test the simple demo UI.

## Stop the Demo

Double-click:

```text
stop_demo.command
```

This stops the local containers but keeps the local demo database.

## Reset the Demo

Double-click:

```text
reset_demo.command
```

This removes the local demo database and starts again from a clean state.

## If Something Fails

Please send:

- a screenshot of the terminal window;
- a screenshot of Docker Desktop;
- the page URL you tried to open;
- the error text shown in the browser, if any.

To view technical logs, open Terminal in this folder and run:

```bash
./scripts/demo_logs.sh
```
