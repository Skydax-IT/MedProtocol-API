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
.button-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  border: 1px solid var(--blue);
  border-radius: 7px;
  background: var(--blue);
  color: #fff;
  font-weight: 800;
  padding: 11px 14px;
  min-height: 44px;
}
.button-link.secondary {
  background: #fff;
  color: var(--blue);
}
.button-link.tertiary {
  border-color: transparent;
  background: transparent;
  color: var(--blue);
  padding-left: 0;
}
.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  margin: 18px 0 8px;
}
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
.section {
  padding: 34px 0;
  border-top: 1px solid var(--line);
}
.section:first-child { border-top: 0; }
.section-kicker {
  color: var(--blue);
  font-size: 13px;
  font-weight: 850;
  margin-bottom: 8px;
  text-transform: uppercase;
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
.panel.plain {
  box-shadow: none;
}
.callout {
  border: 1px solid #bde7d8;
  border-radius: 8px;
  background: var(--green-soft);
  padding: 14px;
  color: #164d3f;
  font-weight: 700;
}
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
.feature-grid,
.audience-grid,
.case-grid,
.metric-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}
.feature-grid.two {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
.flow {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  align-items: stretch;
}
.flow-step {
  position: relative;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  padding: 16px;
  min-height: 112px;
}
.flow-step strong,
.mini-card strong {
  display: block;
  color: var(--blue);
  margin-bottom: 8px;
}
.flow-step span,
.mini-card span {
  color: var(--muted);
  font-size: 14px;
}
.mini-card {
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
  padding: 16px;
}
.case-button.selected {
  border-color: var(--blue);
  background: var(--blue-soft);
}
.step-label {
  display: inline-flex;
  color: var(--blue);
  font-size: 13px;
  font-weight: 850;
  margin-bottom: 8px;
}
.result-layout {
  display: grid;
  grid-template-columns: minmax(280px, 0.9fr) minmax(0, 1.1fr);
  gap: 18px;
}
.muted-note {
  color: var(--muted);
  font-size: 13px;
}
.summary-box {
  display: none;
  margin-top: 14px;
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
  .actions-grid,
  .feature-grid,
  .feature-grid.two,
  .audience-grid,
  .case-grid,
  .metric-grid,
  .flow,
  .result-layout {
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
  <title>MedProtocol API Overview</title>
  <style>$css</style>
</head>
<body>
  <nav class="topnav">
    <div class="brand">MedProtocol API</div>
    <div class="navlinks">
      <a href="/">Overview</a>
      <a href="/guided-demo">Guided Demo</a>
      <a href="/demo">Technical Demo Console</a>
      <a href="/docs">Technical Docs</a>
      <a href="/health">System Status</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>DEMO ONLY — NOT FOR REAL PATIENT CARE</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>
  <main>
    <section class="hero">
      <div>
        <div class="version-label">$demo_label</div>
        <p class="subtitle">A protocol-based triage layer for frontline health systems</p>
        <h1>Turn clinical protocols into safe, traceable triage workflows</h1>
        <p>
          MedProtocol API helps existing field health tools apply structured triage rules,
          detect danger signs first, adapt outputs by health worker role, and keep an audit
          trail — without replacing clinicians or making diagnoses.
        </p>
        <div class="button-row">
          <a class="button-link" href="/guided-demo">View guided demo</a>
          <a class="button-link secondary" href="#integration">See how it integrates</a>
          <a class="button-link tertiary" href="/docs">Technical API docs</a>
        </div>
      </div>
      <aside class="panel status-card">
        <h2>Demo status</h2>
        <div class="status-row"><strong>API status</strong><span class="pill">online</span></div>
        <div class="status-row"><strong>Environment</strong><span>$environment</span></div>
        <div class="status-row"><strong>Demo mode</strong><span>$demo_mode</span></div>
        <div class="status-row"><strong>API version</strong><span>$version</span></div>
        <p class="muted-note">
          This public demo uses fake cases only and shows the product concept, not clinical validation.
        </p>
      </aside>
    </section>

    <section class="section">
      <div class="section-kicker">The field problem</div>
      <h2>Protocols are hard to keep consistent across frontline tools</h2>
      <div class="feature-grid">
        <div class="mini-card"><strong>Data collection is not enough</strong><span>Many field tools collect observations but do not consistently guide what should happen next.</span></div>
        <div class="mini-card"><strong>Protocols live in many formats</strong><span>Clinical guidance may exist as PDFs, paper checklists, training material, or local workflows.</span></div>
        <div class="mini-card"><strong>Decision trees are rebuilt repeatedly</strong><span>Each NGO, ministry project, or integrator often recreates similar logic in a different system.</span></div>
        <div class="mini-card"><strong>Updates are difficult to trace</strong><span>Rule changes, auditability, versioning, and review history are hard to manage across deployments.</span></div>
        <div class="mini-card"><strong>Roles matter</strong><span>A community health worker, nurse, midwife, and doctor may need different wording and scope.</span></div>
        <div class="mini-card"><strong>Connectivity is uneven</strong><span>Low-connectivity settings make consistent, updatable guidance even harder to deliver.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">The MedProtocol approach</div>
      <h2>Existing apps keep their workflow. MedProtocol adds the protocol layer.</h2>
      <p>
        An app, SMS/USSD service, or health information system sends structured observations.
        MedProtocol checks danger signs first, applies explicit deterministic rules, returns a
        clear triage output, and records why that output was generated. The same design can later
        support offline bundles for low-connectivity use.
      </p>
      <div class="flow" aria-label="MedProtocol integration flow">
        <div class="flow-step"><strong>Field app / SMS / tablet</strong><span>Sends structured observations from a fake encounter.</span></div>
        <div class="flow-step"><strong>MedProtocol API</strong><span>Applies explicit, versioned, demo-only rules.</span></div>
        <div class="flow-step"><strong>Triage output + audit trail</strong><span>Returns urgency, role-aware wording, and rule metadata.</span></div>
        <div class="flow-step"><strong>Existing system / referral workflow</strong><span>Stores or displays the result in the partner system.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="two-col">
        <div class="panel">
          <h2>What it is</h2>
          <ul>
            <li>Protocol-based triage API</li>
            <li>Deterministic rule engine</li>
            <li>Integration layer for existing systems</li>
            <li>Role-aware output composer</li>
            <li>Audit and versioning layer</li>
            <li>Demo of a future offline-ready architecture</li>
          </ul>
        </div>
        <div class="panel">
          <h2>What it is not</h2>
          <ul>
            <li>Not a doctor</li>
            <li>Not a diagnosis engine</li>
            <li>Not a chatbot</li>
            <li>Not a treatment engine</li>
            <li>Not a replacement for clinical judgment</li>
            <li>Not validated for real care</li>
          </ul>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">Who could use this</div>
      <h2>Built for health programs that already have tools and workflows</h2>
      <div class="audience-grid">
        <div class="mini-card"><strong>NGOs with field health apps</strong><span>Add traceable triage logic without rebuilding the whole application.</span></div>
        <div class="mini-card"><strong>Ministries of health</strong><span>Explore how approved protocols could be versioned and distributed later.</span></div>
        <div class="mini-card"><strong>Digital health integrators</strong><span>Connect a deterministic protocol layer to existing platforms.</span></div>
        <div class="mini-card"><strong>Community health programs</strong><span>Adapt outputs to frontline roles and low-connectivity workflows.</span></div>
        <div class="mini-card"><strong>SMS/USSD service providers</strong><span>Request the next best structured question or a short message output.</span></div>
        <div class="mini-card"><strong>Rural health programs</strong><span>Design for settings where connectivity and referral pathways vary.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">Safety by design</div>
      <h2>Designed to be explainable before it is clinically ambitious</h2>
      <div class="feature-grid two">
        <div class="mini-card"><strong>Explicit rules</strong><span>Rules are written, versioned, testable, and not generated by an AI model.</span></div>
        <div class="mini-card"><strong>Traceable outputs</strong><span>Every output includes protocol and rule metadata.</span></div>
        <div class="mini-card"><strong>Role-aware wording</strong><span>Scope of practice controls what is shown for each health worker role.</span></div>
        <div class="mini-card"><strong>Missing data surfaced</strong><span>Critical missing information is shown instead of hidden.</span></div>
        <div class="mini-card"><strong>Risk first</strong><span>Severe risk defaults to referral or escalation wording in this demo architecture.</span></div>
        <div class="mini-card"><strong>Governance required</strong><span>Real deployment would require medical validation, legal review, privacy/security review, and country approval.</span></div>
      </div>
    </section>

    <section class="section" id="integration">
      <div class="section-kicker">Integration</div>
      <h2>Designed to plug into existing systems</h2>
      <div class="feature-grid two">
        <div class="mini-card"><strong>Field app triage</strong><span>A field app sends structured observations. The API returns triage output and audit metadata.</span></div>
        <div class="mini-card"><strong>SMS/USSD sessions</strong><span>A low-bandwidth session asks what to ask next. The API returns the next structured question.</span></div>
        <div class="mini-card"><strong>DHIS2/OpenMRS-like systems</strong><span>A health information system stores encounter data. The API adds decision and audit metadata.</span></div>
        <div class="mini-card"><strong>Offline bundle concept</strong><span>Future bundles could support low-connectivity use with versioned rule packages.</span></div>
      </div>
      <p class="muted-note">
        Structured observations means selected fields such as age group, role, setting, and danger signs.
        It does not mean free-text diagnosis.
      </p>
    </section>

    <section class="section">
      <div class="panel">
        <h2>Explore the demo</h2>
        <p>
          Start with the guided demo if you are reviewing the product concept. Use the technical
          docs only if you want to inspect the API contract.
        </p>
        <div class="button-row">
          <a class="button-link" href="/guided-demo">Explore the guided demo</a>
          <a class="button-link secondary" href="/docs">Open technical docs</a>
          <a class="button-link secondary" href="/health">System status</a>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer-note">
    <strong>Repository notes:</strong>
    PROJECT_STATUS.md, ROADMAP.md, DEMO_SCRIPT.md, docs/BUSINESS_DEMO_CHECKLIST.md, and docs/SCREENSHOT_GUIDE.md.
  </footer>
</body>
</html>"""
)


GUIDED_DEMO_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MedProtocol API Guided Demo</title>
  <style>
    $css
    main.guided-layout {
      display: grid;
      grid-template-columns: minmax(280px, 380px) 1fr;
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
    .case-button span {
      display: block;
      color: var(--muted);
      font-size: 14px;
      font-weight: 550;
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
    .result-grid {
      display: grid;
      grid-template-columns: repeat(2, minmax(0, 1fr));
      gap: 12px;
    }
    .wide { grid-column: 1 / -1; }
    .copy-row {
      display: none;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 10px;
      margin: 14px 0;
    }
    .status {
      color: var(--muted);
      min-height: 22px;
      margin-bottom: 12px;
    }
    .error { color: var(--danger); font-weight: 800; }
    @media (max-width: 900px) {
      main.guided-layout,
      .copy-row,
      .result-grid {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <nav class="topnav">
    <div class="brand">MedProtocol API</div>
    <div class="navlinks">
      <a href="/">Overview</a>
      <a href="/guided-demo">Guided Demo</a>
      <a href="/demo">Technical Demo Console</a>
      <a href="/docs">Technical Docs</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>DEMO ONLY — NOT FOR REAL PATIENT CARE</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>

  <main class="guided-layout">
    <section class="panel">
      <div class="version-label">$demo_label</div>
      <h1>Guided Demo</h1>
      <p>
        This walkthrough shows how an existing field app might send fake structured observations,
        what MedProtocol API does with them, and why the result is traceable.
      </p>
      <p class="callout">Fake cases only. Do not type or paste real patient information.</p>
      <h2>Choose a fake story</h2>
      <div id="guidedCases" class="cases"></div>
    </section>

    <section class="panel">
      <div class="step-label">Step 1 — Field observation</div>
      <h2 id="caseTitle">Example: child with danger signs</h2>
      <p id="casePurpose">Demonstrates danger signs being checked before any action wording.</p>
      <div class="result-grid">
        <div class="field"><strong>Fake case</strong><span>For demonstration only</span></div>
        <div class="field"><strong>Patient group</strong><span id="patientGroup">-</span></div>
        <div class="field"><strong>Context</strong><span id="context">-</span></div>
        <div class="field"><strong>User role</strong><span id="role">-</span></div>
        <div class="field wide"><strong>Observed danger signs</strong><span id="observations">-</span></div>
      </div>
      <div class="button-row">
        <button type="button" id="runGuided">Run demo triage</button>
      </div>

      <section class="section">
        <div class="step-label">Step 2 — Protocol engine result</div>
        <h2>What the field worker sees</h2>
        <div id="guidedStatus" class="status">Run the fake case to see the demo output.</div>
        <div class="result-grid">
          <div class="field"><strong>Urgency level</strong><span id="guidedUrgency">-</span></div>
          <div class="field"><strong>Referral required</strong><span id="guidedReferral">-</span></div>
          <div class="field wide"><strong>Immediate action</strong><span id="guidedAction">-</span></div>
          <div class="field"><strong>Danger signs detected</strong><span id="guidedDanger">-</span></div>
          <div class="field"><strong>Missing critical data</strong><span id="guidedMissing">-</span></div>
          <div class="field wide"><strong>Short message for low-connectivity channels</strong><span id="guidedSms">-</span></div>
          <div class="field wide"><strong>Why this output was generated</strong><span id="guidedWhy">-</span></div>
        </div>
      </section>

      <section class="section">
        <div class="step-label">Step 3 — Traceability</div>
        <h2>Why it is auditable</h2>
        <div class="result-grid">
          <div class="field"><strong>Rule ID</strong><span id="guidedRule">-</span></div>
          <div class="field"><strong>Protocol version</strong><span id="guidedProtocol">-</span></div>
          <div class="field"><strong>Validation status</strong><span id="guidedValidation">-</span></div>
          <div class="field"><strong>Audit ID</strong><span id="guidedAudit">-</span></div>
          <div class="field"><strong>Role used</strong><span id="guidedRole">-</span></div>
          <div class="field"><strong>Demo-only status</strong><span id="guidedDemoStatus">-</span></div>
        </div>

        <div id="guidedCopyRow" class="copy-row">
          <button type="button" id="copySummary">Copy non-technical summary</button>
          <button type="button" id="copyGuidedSms">Copy SMS/USSD message</button>
          <button type="button" id="copyTechnicalJson">Copy technical JSON</button>
          <button type="button" id="downloadGuidedJson">Download demo result JSON</button>
        </div>

        <details>
          <summary>Technical details for developers</summary>
          <p class="muted-note">Endpoint used: <code>POST /v1/triage/evaluate</code> and <code>GET /v1/audit/{audit_id}</code>.</p>
          <h3>Raw JSON response</h3>
          <pre id="guidedRaw">{}</pre>
          <h3>Audit record</h3>
          <pre id="guidedAuditRaw">{}</pre>
        </details>
      </section>
    </section>
  </main>
  <footer class="footer-note">
    <strong>For technical reviewers:</strong>
    use the <a href="/demo">Technical Demo Console</a>, <a href="/docs">Swagger docs</a>, or <a href="/redoc">Alternative API Docs</a>.
  </footer>

  <script>
    const DEMO_API_KEY = $api_key_json;
    let selectedCase = null;
    let latestResponse = null;
    let latestAudit = null;

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
        main_complaint: "fake_guided_demo_case",
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
        external_encounter_id: "fake-guided-demo-case",
        channel: "guided_browser_demo",
        client_timestamp: "2026-06-29T12:00:00Z"
      }
    };

    function cloneBase() {
      return JSON.parse(JSON.stringify(basePayload));
    }

    const guidedCases = [
      {
        label: "Child with danger signs",
        patientGroup: "Child 0-59 months",
        context: "Rural health post",
        role: "community_health_worker",
        observations: "Lethargy/unconscious; unable to drink/breastfeed",
        purpose: "Shows danger signs being prioritized first and escalation wording returned.",
        build: () => {
          const payload = cloneBase();
          payload.clinical_inputs.danger_signs.lethargy_or_unconscious = true;
          payload.clinical_inputs.danger_signs.unable_to_drink_or_breastfeed = true;
          return payload;
        }
      },
      {
        label: "Pregnant woman with danger signs",
        patientGroup: "Pregnancy, fake data",
        context: "Rural maternity contact point",
        role: "midwife",
        observations: "Severe bleeding",
        purpose: "Shows role-aware output for a pregnancy danger-sign demo rule.",
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
        patientGroup: "Incomplete fake encounter",
        context: "Community follow-up",
        role: "community_health_worker",
        observations: "Age and respiratory rate are missing",
        purpose: "Shows that missing critical information is surfaced instead of hidden.",
        build: () => {
          const payload = cloneBase();
          payload.patient_context.age_months = null;
          payload.patient_context.weight_kg = null;
          payload.clinical_inputs.vitals.respiratory_rate = null;
          return payload;
        }
      }
    ];

    function setText(id, value) {
      document.getElementById(id).textContent = value || "-";
    }
    function listText(value) {
      return Array.isArray(value) && value.length ? value.join(", ") : "None";
    }
    function resetOutput() {
      ["guidedUrgency", "guidedReferral", "guidedAction", "guidedDanger", "guidedMissing",
       "guidedSms", "guidedWhy", "guidedRule", "guidedProtocol", "guidedValidation",
       "guidedAudit", "guidedRole", "guidedDemoStatus"].forEach((id) => setText(id, "-"));
      document.getElementById("guidedRaw").textContent = "{}";
      document.getElementById("guidedAuditRaw").textContent = "{}";
      document.getElementById("guidedCopyRow").style.display = "none";
      latestResponse = null;
      latestAudit = null;
    }
    function selectCase(item, button) {
      selectedCase = item;
      document.querySelectorAll(".case-button").forEach((node) => node.classList.remove("selected"));
      button.classList.add("selected");
      setText("caseTitle", "Example: " + item.label.toLowerCase());
      setText("casePurpose", item.purpose);
      setText("patientGroup", item.patientGroup);
      setText("context", item.context);
      setText("role", item.role);
      setText("observations", item.observations);
      resetOutput();
    }
    function nonTechnicalSummary() {
      if (!latestResponse || !selectedCase) return "";
      return [
        "MedProtocol API guided demo summary:",
        "Fake case: " + selectedCase.label + ".",
        "Urgency: " + latestResponse.urgency_level + ".",
        "Referral required: " + (latestResponse.referral_required ? "yes" : "no or unknown") + ".",
        "Detected danger signs: " + listText(latestResponse.danger_signs_detected) + ".",
        "Missing critical data: " + listText(latestResponse.missing_critical_data) + ".",
        "This is demo-only, not validated, not a diagnosis, and not for real patient care."
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
      link.download = (latestResponse.audit_id || "guided-demo-result") + ".json";
      link.click();
      URL.revokeObjectURL(url);
    }
    async function loadAudit() {
      if (!latestResponse || !latestResponse.audit_id) return;
      const response = await fetch("/v1/audit/" + latestResponse.audit_id, {
        headers: {
          "X-API-Key": DEMO_API_KEY,
          "X-Request-ID": "req_guided_audit_" + Date.now(),
          "X-Correlation-ID": "corr_guided_browser"
        }
      });
      latestAudit = await response.json();
      document.getElementById("guidedAuditRaw").textContent = JSON.stringify(latestAudit, null, 2);
    }
    async function runGuidedCase() {
      if (!selectedCase) return;
      resetOutput();
      const statusNode = document.getElementById("guidedStatus");
      statusNode.className = "status";
      statusNode.textContent = "Running the fake case through MedProtocol API...";
      const response = await fetch("/v1/triage/evaluate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-API-Key": DEMO_API_KEY,
          "X-Request-ID": "req_guided_browser_" + Date.now(),
          "X-Correlation-ID": "corr_guided_browser"
        },
        body: JSON.stringify(selectedCase.build())
      });
      const body = await response.json();
      latestResponse = body;
      document.getElementById("guidedRaw").textContent = JSON.stringify(body, null, 2);
      if (!response.ok) {
        statusNode.className = "status error";
        statusNode.textContent =
          (body.error && body.error.message) ? body.error.message : "The API returned an error.";
        return;
      }
      statusNode.textContent = "Demo result generated from fake structured observations.";
      setText("guidedUrgency", body.urgency_level);
      setText("guidedReferral", body.referral_required ? "Yes" : "No or unknown");
      setText("guidedAction", body.immediate_action ? body.immediate_action.text : "-");
      setText("guidedDanger", listText(body.danger_signs_detected));
      setText("guidedMissing", listText(body.missing_critical_data));
      setText("guidedSms", body.short_message);
      setText(
        "guidedWhy",
        "The demo engine matched explicit rule(s): " + listText(body.source.rule_ids)
        + ". It did not make a diagnosis."
      );
      setText("guidedRule", listText(body.source.rule_ids));
      setText("guidedProtocol", body.source.protocol_version);
      setText("guidedValidation", body.source.validation_status);
      setText("guidedAudit", body.audit_id);
      setText("guidedRole", selectedCase.role);
      setText(
        "guidedDemoStatus",
        body.source.clinical_use_status + " / " + body.source.real_care_validation_status
      );
      document.getElementById("guidedCopyRow").style.display = "grid";
      await loadAudit();
    }

    const caseList = document.getElementById("guidedCases");
    guidedCases.forEach((item, index) => {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "case-button";
      button.innerHTML = "<strong>" + item.label + "</strong><span>" + item.purpose + "</span>";
      button.addEventListener("click", () => selectCase(item, button));
      caseList.appendChild(button);
      if (index === 0) selectCase(item, button);
    });

    document.getElementById("runGuided").addEventListener("click", () => {
      runGuidedCase().catch((error) => {
        const statusNode = document.getElementById("guidedStatus");
        statusNode.className = "status error";
        statusNode.textContent = "Could not call the demo API: " + error.message;
      });
    });
    document.getElementById("copySummary").addEventListener("click", () => {
      copyText(nonTechnicalSummary());
    });
    document.getElementById("copyGuidedSms").addEventListener("click", () => {
      if (latestResponse) copyText(latestResponse.short_message);
    });
    document.getElementById("copyTechnicalJson").addEventListener("click", () => {
      if (latestResponse) copyText(JSON.stringify(latestResponse, null, 2));
    });
    document.getElementById("downloadGuidedJson").addEventListener("click", downloadJson);
  </script>
</body>
</html>"""
)


DEMO_TEMPLATE = Template(
    """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>MedProtocol API Technical Demo Console</title>
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
      <a href="/">Overview</a>
      <a href="/guided-demo">Guided Demo</a>
      <a href="/demo">Technical Demo Console</a>
      <a href="/docs">Technical Docs</a>
      <a href="/health">System Status</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>DEMO ONLY — NOT FOR REAL PATIENT CARE</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>

  <main class="demo-layout">
    <section class="panel">
      <div class="version-label">$demo_label</div>
      <h1>Technical Demo Console</h1>
      <p>
        For developers, technical reviewers, API testing, JSON inspection, and audit inspection.
        For a non-technical overview, use the Guided Demo page.
      </p>
      <div class="button-row">
        <a class="button-link" href="/guided-demo">Open Guided Demo</a>
      </div>
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
    DEMO_SCRIPT.md, PROJECT_STATUS.md, ROADMAP.md, docs/BUSINESS_DEMO_CHECKLIST.md, and docs/SCREENSHOT_GUIDE.md.
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
        demo_label=settings.demo_label,
        environment=settings.environment,
        demo_mode="enabled" if settings.demo_mode else "disabled",
        version=settings.version,
    )
    return HTMLResponse(content=html)


@router.get("/guided-demo", response_class=HTMLResponse)
def guided_demo_page() -> HTMLResponse:
    settings = get_settings()
    html = GUIDED_DEMO_TEMPLATE.substitute(
        css=BASE_CSS,
        demo_label=settings.demo_label,
        api_key_json=json.dumps(settings.demo_api_key),
    )
    return HTMLResponse(content=html)


@router.get("/demo", response_class=HTMLResponse)
def demo_page() -> HTMLResponse:
    settings = get_settings()
    html = DEMO_TEMPLATE.substitute(
        css=BASE_CSS,
        demo_label=settings.demo_label,
        api_key_json=json.dumps(settings.demo_api_key),
    )
    return HTMLResponse(content=html)
