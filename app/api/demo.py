from __future__ import annotations

import json
from string import Template

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from app.config import get_settings

router = APIRouter(tags=["demo"])


BASE_CSS = """
:root {
  color-scheme: light;
  --ink: #17202a;
  --muted: #5d6d7e;
  --line: #d8e1e8;
  --soft: #f5f8fa;
  --panel: #ffffff;
  --blue: #145a8d;
  --blue-soft: #eef6fc;
  --green: #1f7a63;
  --green-soft: #ecf8f4;
  --danger: #9f1d20;
  --danger-soft: #fff0f0;
  --shadow: 0 12px 30px rgba(20, 62, 89, 0.08);
}
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background: linear-gradient(180deg, #f8fbfc 0%, #ffffff 280px);
  line-height: 1.45;
}
a { color: inherit; }
.topnav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 14px 24px;
  border-bottom: 1px solid var(--line);
  background: rgba(255, 255, 255, 0.92);
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(12px);
}
.brand {
  font-weight: 800;
  color: var(--blue);
}
.navlinks {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}
.navlinks a {
  text-decoration: none;
  font-size: 14px;
  font-weight: 700;
  padding: 8px 10px;
  border-radius: 7px;
  color: var(--muted);
}
.navlinks a:hover,
.navlinks a:focus {
  background: var(--blue-soft);
  color: var(--blue);
}
.warning-strip {
  padding: 12px 24px;
  background: var(--danger-soft);
  border-bottom: 1px solid #f2c9c9;
  color: var(--danger);
  font-weight: 750;
}
.warning-strip span {
  display: inline-block;
  margin-right: 18px;
}
main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 24px 48px;
}
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(280px, 0.75fr);
  gap: 24px;
  align-items: start;
  padding: 20px 0 28px;
}
h1 {
  margin: 0 0 8px;
  font-size: clamp(32px, 5vw, 54px);
  letter-spacing: 0;
  line-height: 1.02;
}
.subtitle {
  color: var(--blue);
  font-size: 20px;
  font-weight: 750;
  margin: 0 0 18px;
}
p { color: var(--muted); margin: 0 0 14px; }
.panel,
.card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  box-shadow: var(--shadow);
}
.panel { padding: 18px; }
.status-card {
  display: grid;
  gap: 12px;
}
.status-row {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--line);
}
.status-row:last-child {
  border-bottom: 0;
  padding-bottom: 0;
}
.status-row strong {
  color: var(--muted);
  font-size: 13px;
}
.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--green);
  background: var(--green-soft);
  border: 1px solid #bde7d8;
  border-radius: 999px;
  padding: 3px 9px;
  font-weight: 800;
  font-size: 13px;
}
.version-label {
  display: inline-flex;
  margin: 0 0 14px;
  color: var(--blue);
  background: var(--blue-soft);
  border: 1px solid #c9dfef;
  border-radius: 999px;
  padding: 5px 10px;
  font-weight: 800;
  font-size: 13px;
}
.footer-note {
  max-width: 1180px;
  margin: 0 auto;
  padding: 0 24px 34px;
  color: var(--muted);
  font-size: 14px;
}
.footer-note strong {
  color: var(--ink);
}
.actions-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin: 10px 0 28px;
}
.card {
  display: block;
  padding: 16px;
  text-decoration: none;
  min-height: 112px;
}
.card strong {
  display: block;
  color: var(--blue);
  font-size: 17px;
  margin-bottom: 8px;
}
.card span {
  display: block;
  color: var(--muted);
  font-size: 14px;
}
.two-col {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}
h2 {
  margin: 0 0 12px;
  font-size: 20px;
}
ul {
  margin: 0;
  padding-left: 20px;
  color: var(--muted);
}
li { margin-bottom: 7px; }
button {
  border: 1px solid #b8c7d3;
  border-radius: 7px;
  background: var(--blue-soft);
  color: var(--blue);
  font: inherit;
  font-weight: 750;
  padding: 10px 12px;
  cursor: pointer;
}
button:hover,
button:focus {
  outline: 2px solid #7fb3d5;
  outline-offset: 1px;
}
button.secondary {
  background: #fff;
  color: var(--muted);
}
code,
pre {
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-size: 13px;
}
pre {
  overflow: auto;
  background: #101820;
  color: #eef5f8;
  padding: 14px;
  border-radius: 8px;
  max-height: 420px;
}
details {
  margin-top: 14px;
  border-top: 1px solid var(--line);
  padding-top: 12px;
}
summary {
  cursor: pointer;
  font-weight: 800;
}
@media (max-width: 900px) {
  .hero,
  .two-col,
  .actions-grid {
    grid-template-columns: 1fr;
  }
  main { padding: 20px 16px 36px; }
  .topnav { align-items: flex-start; flex-direction: column; }
}
"""


LANDING_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MedProtocol API Local Demo</title>
  <style>$css</style>
</head>
<body>
  <nav class="topnav">
    <div class="brand">MedProtocol API</div>
    <div class="navlinks">
      <a href="/">Home</a>
      <a href="/demo">Demo</a>
      <a href="/docs">API Docs</a>
      <a href="/health">Health</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>DEMO ONLY — NOT FOR REAL PATIENT CARE</span>
    <span>Do not enter real patient data</span>
    <span>No clinical protocol validated for real use</span>
  </div>
  <main>
    <section class="hero">
      <div>
        <div class="version-label">v0.1 local demo MVP</div>
        <h1>MedProtocol API</h1>
        <p class="subtitle">Protocol-based clinical triage API for frontline health systems</p>
        <p>
          MedProtocol API is a deterministic, protocol-based triage engine designed to
          integrate with existing systems such as field apps, SMS/USSD, DHIS2/OpenMRS-like
          systems, or NGO tools.
        </p>
        <p>
          This local demo does not provide diagnosis, does not replace clinicians, and does
          not use AI to make medical decisions. It only demonstrates safe architecture and
          integration patterns with fake cases.
        </p>
      </div>
      <aside class="panel status-card">
        <h2>Local Status</h2>
        <div class="status-row"><strong>API status</strong><span class="pill">online</span></div>
        <div class="status-row"><strong>Environment</strong><span>$environment</span></div>
        <div class="status-row"><strong>API version</strong><span>$version</span></div>
      </aside>
    </section>

    <section class="actions-grid" aria-label="Main demo links">
      <a class="card" href="/demo"><strong>Open Demo UI</strong><span>Run fake preset cases in a browser.</span></a>
      <a class="card" href="/docs"><strong>Open API Docs</strong><span>View Swagger/OpenAPI documentation.</span></a>
      <a class="card" href="/redoc"><strong>Open ReDoc</strong><span>Read another API documentation view.</span></a>
      <a class="card" href="/health"><strong>Check Health</strong><span>Confirm the API is responding.</span></a>
    </section>

    <section class="two-col">
      <div class="panel">
        <h2>What this demo proves</h2>
        <ul>
          <li>Deterministic rule engine</li>
          <li>Danger signs first</li>
          <li>Role-based output adaptation</li>
          <li>Audit trail</li>
          <li>SMS/USSD-ready summary</li>
          <li>Offline bundle concept</li>
        </ul>
      </div>
      <div class="panel">
        <h2>What this demo does not do</h2>
        <ul>
          <li>No diagnosis</li>
          <li>No treatment recommendation</li>
          <li>No medication or dosage</li>
          <li>No real clinical validation</li>
          <li>No real patient data</li>
        </ul>
      </div>
    </section>
  </main>
  <footer class="footer-note">
    <strong>Repository notes:</strong>
    PROJECT_STATUS.md, ROADMAP.md, MILESTONE_V0_1_LOCAL_DEMO.md, and docs/SCREENSHOT_GUIDE.md.
  </footer>
</body>
</html>"""
)


DEMO_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MedProtocol API Demo UI</title>
  <style>
    $css
    main.demo-layout {
      display: grid;
      grid-template-columns: minmax(290px, 390px) 1fr;
      gap: 22px;
    }
    .cases { display: grid; gap: 12px; }
    .case-button {
      width: 100%;
      text-align: left;
      background: #fff;
      color: var(--ink);
      box-shadow: none;
    }
    .case-button strong {
      display: block;
      color: var(--blue);
      margin-bottom: 6px;
      font-size: 16px;
    }
    .case-meta {
      display: grid;
      gap: 3px;
      color: var(--muted);
      font-size: 13px;
      font-weight: 500;
    }
    .case-purpose {
      display: block;
      margin-top: 8px;
      color: #34495e;
      font-size: 14px;
      font-weight: 650;
    }
    .status {
      margin-bottom: 12px;
      color: var(--muted);
      min-height: 22px;
    }
    .error { color: var(--danger); font-weight: 800; }
    .result-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .field {
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 12px;
      min-height: 72px;
      background: var(--soft);
    }
    .field strong {
      display: block;
      font-size: 12px;
      color: var(--muted);
      text-transform: uppercase;
      margin-bottom: 6px;
      letter-spacing: 0;
    }
    .wide { grid-column: 1 / -1; }
    .copy-row {
      display: none;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    .summary {
      display: none;
      margin-top: 14px;
      background: var(--green-soft);
      border: 1px solid #bde7d8;
      border-radius: 8px;
      padding: 14px;
    }
    .summary h3 { margin: 0 0 8px; font-size: 17px; }
    .audit-panel { display: none; }
    @media (max-width: 900px) {
      main.demo-layout { grid-template-columns: 1fr; }
      .copy-row { grid-template-columns: 1fr; }
      .result-grid { grid-template-columns: 1fr; }
    }
  </style>
</head>
<body>
  <nav class="topnav">
    <div class="brand">MedProtocol API</div>
    <div class="navlinks">
      <a href="/">Home</a>
      <a href="/demo">Demo</a>
      <a href="/docs">API Docs</a>
      <a href="/health">Health</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>DEMO ONLY — NOT FOR REAL PATIENT CARE</span>
    <span>Do not enter real patient data</span>
    <span>No clinical protocol validated for real use</span>
  </div>

  <main class="demo-layout">
    <section class="panel">
      <div class="version-label">v0.1 local demo MVP</div>
      <h1>Local Demo UI</h1>
      <p>
        Choose a fake case. The page calls the local API with a local demo API key.
        Do not enter or paste real patient information.
      </p>
      <h2>Fake test cases</h2>
      <div id="cases" class="cases"></div>
    </section>

    <section class="panel">
      <h2>Result</h2>
      <div id="status" class="status">Choose a fake case to run an evaluation.</div>
      <div class="result-grid">
        <div class="field"><strong>Urgency level</strong><span id="urgency">-</span></div>
        <div class="field"><strong>Referral required</strong><span id="referral">-</span></div>
        <div class="field wide"><strong>Immediate action</strong><span id="action">-</span></div>
        <div class="field"><strong>Danger signs detected</strong><span id="danger">-</span></div>
        <div class="field"><strong>Missing critical data</strong><span id="missing">-</span></div>
        <div class="field wide"><strong>Short SMS/USSD message</strong><span id="sms">-</span></div>
        <div class="field wide"><strong>Protocol/rule metadata</strong><span id="metadata">-</span></div>
        <div class="field"><strong>Audit ID</strong><span id="audit">-</span></div>
      </div>

      <div id="copyRow" class="copy-row">
        <button type="button" id="copyJson">Copy JSON response</button>
        <button type="button" id="copySms">Copy short SMS/USSD message</button>
        <button type="button" id="copyAudit">Copy audit ID</button>
        <button type="button" id="downloadJson">Download demo result as JSON</button>
      </div>

      <section id="summary" class="summary">
        <h3>Demo interpretation</h3>
        <div id="summaryText">-</div>
      </section>

      <details>
        <summary>Raw JSON response</summary>
        <pre id="raw">{}</pre>
      </details>

      <details id="auditPanel" class="audit-panel">
        <summary>Audit record JSON</summary>
        <button type="button" id="viewAudit" class="secondary">View audit record</button>
        <pre id="auditRaw">{}</pre>
      </details>
    </section>
  </main>
  <footer class="footer-note">
    <strong>Repository notes:</strong>
    DEMO_SCRIPT.md, PROJECT_STATUS.md, ROADMAP.md, and docs/SCREENSHOT_GUIDE.md.
  </footer>

  <script>
    const DEMO_API_KEY = $api_key_json;
    let latestResponse = null;
    let latestAudit = null;
    let latestCase = null;

    const basePayload = {
      patient_context: {
        patient_ref: null,
        age_months: 24,
        sex: "female",
        pregnancy_status: "not_applicable",
        weight_kg: 12
      },
      encounter_context: {
        country_code: "CF",
        region_code: null,
        setting: "rural_health_post",
        user_role: "community_health_worker",
        connectivity: "offline_capable",
        language: "fr"
      },
      clinical_inputs: {
        main_complaint: "fake_demo_case",
        duration_days: 2,
        danger_signs: {
          convulsions: false,
          lethargy_or_unconscious: false,
          unable_to_drink_or_breastfeed: false,
          respiratory_distress: false,
          severe_bleeding: false,
          severe_abdominal_pain: false,
          severe_headache_or_visual_disturbance: false
        },
        vitals: {
          temperature_c: 37.5,
          respiratory_rate: 28,
          heart_rate: 100
        }
      },
      resources_available: {
        referral_transport_available: false,
        phone_network_available: true,
        rapid_malaria_test_available: true,
        ors_available: true
      },
      client_context: {
        external_encounter_id: "fake-demo-browser-case",
        channel: "browser_demo",
        client_timestamp: "2026-06-28T12:00:00Z"
      }
    };

    function cloneBase() {
      return JSON.parse(JSON.stringify(basePayload));
    }

    const cases = [
      {
        label: "Child with danger signs",
        patientCategory: "Child 0–59 months, fake data",
        role: "community_health_worker",
        country: "CF",
        purpose: "Demonstrates urgent referral triggered by demo danger signs.",
        build: () => {
          const payload = cloneBase();
          payload.clinical_inputs.danger_signs.lethargy_or_unconscious = true;
          payload.clinical_inputs.danger_signs.unable_to_drink_or_breastfeed = true;
          return payload;
        }
      },
      {
        label: "Child without danger signs",
        patientCategory: "Child 0–59 months, fake data",
        role: "community_health_worker",
        country: "CF",
        purpose: "Demonstrates deterministic routine demo output when no demo danger sign is provided.",
        build: () => cloneBase()
      },
      {
        label: "Pregnant woman with danger signs",
        patientCategory: "Pregnancy, fake data",
        role: "midwife",
        country: "TD",
        purpose: "Demonstrates pregnancy demo danger-sign routing without diagnosis or treatment logic.",
        build: () => {
          const payload = cloneBase();
          payload.patient_context.age_months = 300;
          payload.patient_context.pregnancy_status = "pregnant";
          payload.patient_context.weight_kg = null;
          payload.encounter_context.country_code = "TD";
          payload.encounter_context.user_role = "midwife";
          payload.clinical_inputs.danger_signs.severe_bleeding = true;
          return payload;
        }
      },
      {
        label: "Missing critical data",
        patientCategory: "Incomplete fake encounter",
        role: "community_health_worker",
        country: "CF",
        purpose: "Demonstrates how the API flags missing information.",
        build: () => {
          const payload = cloneBase();
          payload.patient_context.age_months = null;
          payload.patient_context.weight_kg = null;
          payload.clinical_inputs.vitals.respiratory_rate = null;
          return payload;
        }
      },
      {
        label: "Community health worker scope",
        patientCategory: "Child 0–59 months, fake data",
        role: "community_health_worker",
        country: "CF",
        purpose: "Demonstrates role-based output constraints for a frontline worker.",
        build: () => {
          const payload = cloneBase();
          payload.encounter_context.user_role = "community_health_worker";
          payload.clinical_inputs.danger_signs.convulsions = true;
          return payload;
        }
      },
      {
        label: "Nurse scope",
        patientCategory: "Child 0–59 months, fake data",
        role: "nurse",
        country: "CF",
        purpose: "Demonstrates the same deterministic rule adapted for the nurse role.",
        build: () => {
          const payload = cloneBase();
          payload.encounter_context.user_role = "nurse";
          payload.clinical_inputs.danger_signs.convulsions = true;
          return payload;
        }
      }
    ];

    const ids = ["urgency", "referral", "action", "danger", "missing", "sms", "metadata", "audit"];
    function setText(id, value) {
      document.getElementById(id).textContent = value || "-";
    }
    function listText(value) {
      return Array.isArray(value) && value.length ? value.join(", ") : "None";
    }
    function resetResult() {
      ids.forEach((id) => setText(id, "-"));
      document.getElementById("raw").textContent = "{}";
      document.getElementById("auditRaw").textContent = "{}";
      document.getElementById("copyRow").style.display = "none";
      document.getElementById("summary").style.display = "none";
      document.getElementById("auditPanel").style.display = "none";
      latestResponse = null;
      latestAudit = null;
    }
    function metadataText(source) {
      if (!source) return "-";
      return "Protocol " + source.protocol_id
        + " / version " + source.protocol_version
        + " / rules " + listText(source.rule_ids)
        + " / " + source.validation_status
        + " / " + source.clinical_use_status
        + " / " + source.real_care_validation_status;
    }
    function demoSummary(body) {
      const rules = body.source && body.source.rule_ids ? body.source.rule_ids : [];
      const danger = listText(body.danger_signs_detected);
      const missing = listText(body.missing_critical_data);
      const role = latestCase ? latestCase.role : "selected demo role";
      return [
        "Triggered fake rule(s): " + listText(rules) + ".",
        "Urgency was selected by the deterministic demo rule output: " + body.urgency_level + ".",
        "Detected demo danger signs: " + danger + ".",
        "Missing critical data: " + missing + ".",
        "User role in this case: " + role + "; the API only adapts wording and allowed output scope.",
        "This remains demo-only, draft, not validated, and not for real patient care."
      ].join(" ");
    }
    async function copyText(value) {
      await navigator.clipboard.writeText(value || "");
    }
    function downloadJson() {
      if (!latestResponse) return;
      const blob = new Blob([JSON.stringify(latestResponse, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = (latestResponse.audit_id || "demo-result") + ".json";
      link.click();
      URL.revokeObjectURL(url);
    }
    async function viewAudit() {
      if (!latestResponse || !latestResponse.audit_id) return;
      const response = await fetch("/v1/audit/" + latestResponse.audit_id, {
        headers: {
          "X-API-Key": DEMO_API_KEY,
          "X-Request-ID": "req_demo_audit_" + Date.now(),
          "X-Correlation-ID": "corr_demo_browser"
        }
      });
      latestAudit = await response.json();
      document.getElementById("auditRaw").textContent = JSON.stringify(latestAudit, null, 2);
    }
    async function runCase(item) {
      resetResult();
      latestCase = item;
      document.getElementById("status").className = "status";
      document.getElementById("status").textContent = "Running: " + item.label;
      const response = await fetch("/v1/triage/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": DEMO_API_KEY,
          "X-Request-ID": "req_demo_browser_" + Date.now(),
          "X-Correlation-ID": "corr_demo_browser"
        },
        body: JSON.stringify(item.build())
      });
      const body = await response.json();
      latestResponse = body;
      document.getElementById("raw").textContent = JSON.stringify(body, null, 2);
      if (!response.ok) {
        document.getElementById("status").className = "status error";
        document.getElementById("status").textContent =
          (body.error && body.error.message) ? body.error.message : "The API returned an error.";
        return;
      }
      document.getElementById("status").textContent = "Completed: " + item.label;
      setText("urgency", body.urgency_level);
      setText(
        "referral",
        body.referral_required === null ? "Unknown" : (body.referral_required ? "Yes" : "No")
      );
      setText("action", body.immediate_action ? body.immediate_action.text : "-");
      setText("danger", listText(body.danger_signs_detected));
      setText("missing", listText(body.missing_critical_data));
      setText("sms", body.short_message);
      setText("metadata", metadataText(body.source));
      setText("audit", body.audit_id);
      document.getElementById("summaryText").textContent = demoSummary(body);
      document.getElementById("summary").style.display = "block";
      document.getElementById("copyRow").style.display = "grid";
      document.getElementById("auditPanel").style.display = "block";
    }

    document.getElementById("copyJson").addEventListener("click", () => {
      if (latestResponse) copyText(JSON.stringify(latestResponse, null, 2));
    });
    document.getElementById("copySms").addEventListener("click", () => {
      if (latestResponse) copyText(latestResponse.short_message);
    });
    document.getElementById("copyAudit").addEventListener("click", () => {
      if (latestResponse) copyText(latestResponse.audit_id);
    });
    document.getElementById("downloadJson").addEventListener("click", downloadJson);
    document.getElementById("viewAudit").addEventListener("click", () => {
      viewAudit().catch((error) => {
        document.getElementById("auditRaw").textContent =
          "Could not load audit record: " + error.message;
      });
    });

    const casesNode = document.getElementById("cases");
    cases.forEach((item) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "case-button";
      button.innerHTML =
        "<strong>" + item.label + "</strong>"
        + "<span class='case-meta'>"
        + "<span>Patient category: " + item.patientCategory + "</span>"
        + "<span>User role: " + item.role + "</span>"
        + "<span>Country: " + item.country + "</span>"
        + "</span>"
        + "<span class='case-purpose'>" + item.purpose + "</span>";
      button.addEventListener("click", () => runCase(item).catch((error) => {
        document.getElementById("status").className = "status error";
        document.getElementById("status").textContent =
          "Could not call the local API: " + error.message;
      }));
      casesNode.appendChild(button);
    });
  </script>
</body>
</html>"""
)


@router.get("/", response_class=HTMLResponse)
def landing_page() -> HTMLResponse:
    settings = get_settings()
    html = LANDING_TEMPLATE.substitute(
        css=BASE_CSS,
        environment=settings.environment,
        version=settings.version,
    )
    return HTMLResponse(content=html)


@router.get("/demo", response_class=HTMLResponse)
def demo_page() -> HTMLResponse:
    settings = get_settings()
    html = DEMO_TEMPLATE.substitute(
        css=BASE_CSS,
        api_key_json=json.dumps(settings.demo_api_key),
    )
    return HTMLResponse(content=html)
