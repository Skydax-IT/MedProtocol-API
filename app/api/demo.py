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
  --ink: #102133;
  --muted: #5c7183;
  --line: #d9e5ec;
  --soft: #f5f9fb;
  --panel: #ffffff;
  --navy: #0d2b45;
  --blue: #12618f;
  --blue-soft: #eaf6fb;
  --teal: #137f7a;
  --teal-soft: #e8f7f4;
  --green: #25815f;
  --green-soft: #ecf8f2;
  --gold: #b46b21;
  --danger: #9b2028;
  --danger-soft: #fff2f2;
  --shadow: 0 22px 70px rgba(20, 62, 89, 0.12);
  --shadow-soft: 0 12px 32px rgba(18, 97, 143, 0.10);
  --radius: 18px;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  color: var(--ink);
  background:
    radial-gradient(circle at 12% 4%, rgba(19, 127, 122, 0.16), transparent 34%),
    radial-gradient(circle at 88% 0%, rgba(18, 97, 143, 0.14), transparent 30%),
    linear-gradient(180deg, #f7fbfd 0%, #ffffff 520px);
  line-height: 1.55;
}
a { color: inherit; }
.button-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  border: 1px solid #0f6d9e;
  border-radius: 999px;
  background: linear-gradient(135deg, #0f6d9e, #12847d);
  color: #fff;
  font-weight: 800;
  padding: 12px 18px;
  min-height: 46px;
  box-shadow: 0 14px 34px rgba(18, 97, 143, 0.22);
  transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
}
.button-link:hover,
.button-link:focus {
  transform: translateY(-1px);
  box-shadow: 0 18px 42px rgba(18, 97, 143, 0.28);
}
.button-link.secondary {
  background: #fff;
  color: var(--blue);
  border-color: #c7dbe6;
  box-shadow: none;
}
.button-link.tertiary {
  border-color: transparent;
  background: transparent;
  color: var(--blue);
  padding-left: 0;
  box-shadow: none;
}
.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
  margin: 24px 0 8px;
}
.topnav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 16px 28px;
  border-bottom: 1px solid rgba(217, 229, 236, 0.72);
  background: rgba(255, 255, 255, 0.82);
  position: sticky;
  top: 0;
  z-index: 10;
  backdrop-filter: blur(18px);
}
.brand {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  font-weight: 900;
  color: var(--navy);
  letter-spacing: 0;
}
.brand::before {
  content: "";
  width: 28px;
  height: 28px;
  border-radius: 9px;
  background:
    linear-gradient(135deg, rgba(255,255,255,0.35), transparent),
    linear-gradient(135deg, #0f6d9e, #17a080);
  box-shadow: 0 10px 22px rgba(18, 97, 143, 0.20);
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
  padding: 9px 11px;
  border-radius: 999px;
  color: var(--muted);
  transition: background 160ms ease, color 160ms ease;
}
.navlinks a:hover,
.navlinks a:focus {
  background: var(--blue-soft);
  color: var(--blue);
}
.warning-strip {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  padding: 12px 28px;
  background: rgba(255, 242, 242, 0.94);
  border-bottom: 1px solid #f0c9cc;
  color: var(--danger);
  font-weight: 800;
}
.warning-strip span {
  display: inline-block;
}
main {
  max-width: 1180px;
  margin: 0 auto;
  padding: 42px 24px 56px;
}
.section {
  padding: 58px 0;
  border-top: 1px solid rgba(217, 229, 236, 0.78);
}
.section:first-child { border-top: 0; }
.section-kicker {
  color: var(--teal);
  font-size: 13px;
  font-weight: 850;
  margin-bottom: 10px;
  text-transform: uppercase;
}
.hero {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(360px, 0.88fr);
  gap: 40px;
  align-items: center;
  padding: 24px 0 56px;
}
h1 {
  margin: 0 0 16px;
  color: var(--navy);
  font-size: clamp(40px, 6vw, 74px);
  letter-spacing: 0;
  line-height: 0.98;
}
.subtitle {
  color: var(--teal);
  font-size: 19px;
  font-weight: 850;
  margin: 0 0 14px;
}
p {
  color: var(--muted);
  margin: 0 0 16px;
  font-size: 16px;
}
.lead {
  max-width: 720px;
  color: #43596b;
  font-size: 20px;
}
.panel,
.card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.90);
  box-shadow: var(--shadow);
}
.panel { padding: 22px; }
.panel.plain {
  box-shadow: none;
}
.callout {
  border: 1px solid #bfe6de;
  border-radius: 14px;
  background: var(--green-soft);
  padding: 15px 16px;
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
  padding-bottom: 12px;
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
  padding: 5px 10px;
  font-weight: 800;
  font-size: 13px;
}
.version-label {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 18px;
  color: #0f6d62;
  background: rgba(232, 247, 244, 0.92);
  border: 1px solid #bfe6de;
  border-radius: 999px;
  padding: 7px 12px;
  font-weight: 800;
  font-size: 13px;
}
.version-label::before {
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #19a985;
}
.footer-note {
  max-width: 1180px;
  margin: 0 auto;
  padding: 12px 24px 40px;
  color: var(--muted);
  font-size: 14px;
  border-top: 1px solid rgba(217, 229, 236, 0.78);
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
.hero-visual {
  position: relative;
  display: grid;
  gap: 14px;
  padding: 18px;
  border: 1px solid rgba(203, 221, 230, 0.92);
  border-radius: 28px;
  background:
    linear-gradient(145deg, rgba(255,255,255,0.96), rgba(235,247,250,0.86));
  box-shadow: var(--shadow);
  overflow: hidden;
}
.hero-visual::before {
  content: "";
  position: absolute;
  inset: -80px -70px auto auto;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background: rgba(19, 127, 122, 0.14);
}
.mock-card {
  position: relative;
  border: 1px solid rgba(203, 221, 230, 0.92);
  border-radius: 18px;
  background: #fff;
  padding: 16px;
  box-shadow: var(--shadow-soft);
  animation: float-in 680ms ease both;
}
.mock-card:nth-child(2) { animation-delay: 90ms; }
.mock-card:nth-child(3) { animation-delay: 180ms; }
.mock-card strong {
  display: block;
  color: var(--navy);
  margin-bottom: 8px;
}
.mock-card span,
.mock-row {
  display: block;
  color: var(--muted);
  font-size: 14px;
}
.mock-engine {
  background: linear-gradient(135deg, #0d2b45, #12618f);
  color: #fff;
}
.mock-engine strong,
.mock-engine span {
  color: #fff;
}
.mock-arrow {
  justify-self: center;
  color: var(--teal);
  font-weight: 900;
}
.mock-metric {
  display: inline-flex;
  margin: 5px 6px 0 0;
  border-radius: 999px;
  background: var(--blue-soft);
  color: var(--blue);
  padding: 5px 9px;
  font-size: 12px;
  font-weight: 800;
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
  gap: 14px;
  align-items: stretch;
}
.flow-step {
  position: relative;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  padding: 18px;
  min-height: 128px;
  box-shadow: var(--shadow-soft);
  transition: transform 180ms ease, box-shadow 180ms ease;
}
.flow-step:hover,
.mini-card:hover,
.case-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}
.flow-step strong,
.mini-card strong {
  display: block;
  color: var(--navy);
  margin-bottom: 8px;
}
.flow-step span,
.mini-card span {
  color: var(--muted);
  font-size: 14px;
}
.mini-card {
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--panel);
  padding: 18px;
  box-shadow: var(--shadow-soft);
  transition: transform 180ms ease, box-shadow 180ms ease;
}
.case-button.selected {
  border-color: #3aa89c;
  background: linear-gradient(135deg, #ffffff, var(--teal-soft));
}
.step-label {
  display: inline-flex;
  color: var(--teal);
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
  padding: 18px;
  text-decoration: none;
  min-height: 112px;
}
.card strong {
  display: block;
  color: var(--navy);
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
  margin: 0 0 14px;
  color: var(--navy);
  font-size: clamp(24px, 3vw, 38px);
  line-height: 1.12;
}
ul {
  margin: 0;
  padding-left: 20px;
  color: var(--muted);
}
li { margin-bottom: 7px; }
button {
  border: 1px solid #b8d3dc;
  border-radius: 999px;
  background: #fff;
  color: var(--blue);
  font: inherit;
  font-weight: 750;
  padding: 11px 14px;
  cursor: pointer;
  transition: transform 160ms ease, box-shadow 160ms ease, background 160ms ease;
}
button:hover,
button:focus {
  background: var(--blue-soft);
  box-shadow: var(--shadow-soft);
  transform: translateY(-1px);
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
  border-radius: 14px;
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
  color: var(--navy);
}
@keyframes float-in {
  from {
    opacity: 0;
    transform: translateY(12px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  h1 { font-size: clamp(36px, 13vw, 54px); }
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
      <a href="#integration">Integration</a>
      <a href="#safety">Safety</a>
      <a href="/docs">Technical Docs</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>Demo only — not for real patient care</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>
  <main>
    <section class="hero">
      <div>
        <div class="version-label">Demo only — not for real patient care</div>
        <p class="subtitle">A protocol-based triage layer for frontline health systems</p>
        <h1>Clinical protocol logic, ready for frontline systems</h1>
        <p class="lead">
          MedProtocol API is designed to turn validated clinical protocols into structured,
          traceable triage workflows that existing field tools can call — without replacing
          clinicians or making diagnoses.
        </p>
        <div class="button-row">
          <a class="button-link" href="/guided-demo">Try the guided demo</a>
          <a class="button-link secondary" href="#integration">See integration flow</a>
          <a class="button-link tertiary" href="/docs">For developers: API docs</a>
        </div>
      </div>
      <aside class="hero-visual" aria-label="Product flow mockup">
        <div class="mock-card">
          <strong>Field observation</strong>
          <span>Rural health post · community health worker</span>
          <span class="mock-metric">Danger signs selected</span>
          <span class="mock-metric">No free text</span>
        </div>
        <div class="mock-arrow">↓</div>
        <div class="mock-card mock-engine">
          <strong>MedProtocol API engine</strong>
          <span>Danger signs first · role-aware rules · versioned demo protocol</span>
        </div>
        <div class="mock-arrow">↓</div>
        <div class="mock-card">
          <strong>Triage output + audit</strong>
          <span>Urgency, short message, rule ID, audit trail</span>
          <span class="mock-metric">No diagnosis</span>
          <span class="mock-metric">Demo only</span>
        </div>
        <div class="mock-card status-card">
          <strong>Prototype status</strong>
          <div class="status-row"><strong>API version</strong><span>$api_version</span></div>
          <div class="status-row"><strong>Demo UX version</strong><span>$demo_ux_version</span></div>
          <div class="status-row"><strong>Product stage</strong><span>$product_stage</span></div>
          <div class="status-row"><strong>Clinical status</strong><span>$clinical_status</span></div>
        </div>
      </aside>
    </section>

    <section class="section">
      <div class="section-kicker">Problem</div>
      <h2>The gap in digital health is not data collection. It is safe action guidance.</h2>
      <div class="feature-grid">
        <div class="mini-card"><strong>Field tools collect data</strong><span>Symptoms, visits, and activity data are captured, but action guidance is often inconsistent.</span></div>
        <div class="mini-card"><strong>Protocols stay fragmented</strong><span>Guidance may remain in PDFs, paper checklists, training material, or hard-coded forms.</span></div>
        <div class="mini-card"><strong>Logic is hard to reuse</strong><span>Decision trees become difficult to maintain, audit, and update across programs.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">Solution</div>
      <h2>A protocol layer that plugs into existing systems</h2>
      <div class="flow" aria-label="MedProtocol integration flow">
        <div class="flow-step"><strong>1. Structured observations</strong><span>An existing field app sends selected signs, context, and role.</span></div>
        <div class="flow-step"><strong>2. Danger signs first</strong><span>The engine checks severe-risk indicators before action wording.</span></div>
        <div class="flow-step"><strong>3. Role and version</strong><span>Rules are applied by role, country, and protocol version.</span></div>
        <div class="flow-step"><strong>4. Output and audit</strong><span>The system returns a short triage message and traceable audit trail.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">Why it matters</div>
      <h2>Safer operational workflows without rebuilding every tool</h2>
      <div class="feature-grid">
        <div class="mini-card"><strong>Faster triage workflows</strong><span>Give frontline systems a consistent protocol layer to call.</span></div>
        <div class="mini-card"><strong>Safer escalation logic</strong><span>Prioritize danger signs and referral wording in the demo architecture.</span></div>
        <div class="mini-card"><strong>Traceable protocol decisions</strong><span>Return rule IDs, protocol versions, and audit records with every evaluation.</span></div>
        <div class="mini-card"><strong>Easier integration</strong><span>Designed for NGOs, ministries, and implementers already running digital tools.</span></div>
      </div>
    </section>

    <section class="section">
      <div class="section-kicker">Designed for</div>
      <h2>Teams working across public health delivery</h2>
      <div class="audience-grid">
        <div class="mini-card"><strong>NGOs</strong><span>Field health apps and program workflows.</span></div>
        <div class="mini-card"><strong>Ministries of Health</strong><span>Future protocol governance and country approval workflows.</span></div>
        <div class="mini-card"><strong>Digital health integrators</strong><span>API-first triage logic for existing systems.</span></div>
        <div class="mini-card"><strong>Community health programs</strong><span>Role-aware frontline guidance concepts.</span></div>
        <div class="mini-card"><strong>SMS/USSD providers</strong><span>Short-message and next-question workflows.</span></div>
        <div class="mini-card"><strong>Rural health programs</strong><span>Low-connectivity and offline bundle planning.</span></div>
      </div>
    </section>

    <section class="section" id="safety">
      <div class="section-kicker">Safety by design</div>
      <h2>Explicit, traceable, and conservative by default</h2>
      <div class="feature-grid two">
        <div class="mini-card"><strong>Deterministic rules, not AI diagnosis</strong><span>No LLM or generative system makes clinical decisions.</span></div>
        <div class="mini-card"><strong>Danger signs first</strong><span>Severe-risk indicators are prioritized before any output wording.</span></div>
        <div class="mini-card"><strong>Role-based outputs</strong><span>Outputs are adapted to health worker scope.</span></div>
        <div class="mini-card"><strong>Missing data highlighted</strong><span>Critical gaps are surfaced instead of hidden.</span></div>
        <div class="mini-card"><strong>Audit trail for every decision</strong><span>Protocol version, rule IDs, and audit IDs are returned.</span></div>
        <div class="mini-card"><strong>Validation required</strong><span>Medical validation, legal review, privacy/security review, and country approval are required before any real pilot.</span></div>
      </div>
    </section>

    <section class="section" id="integration">
      <div class="section-kicker">Integration</div>
      <h2>Built for the systems health programs already use</h2>
      <div class="flow" aria-label="Public demo integration flow">
        <div class="flow-step"><strong>Field app / SMS / Tablet</strong><span>Structured observations from an existing workflow.</span></div>
        <div class="flow-step"><strong>MedProtocol API</strong><span>Deterministic protocol layer and role-aware output composer.</span></div>
        <div class="flow-step"><strong>Triage output + audit</strong><span>Short message, urgency level, rule IDs, and audit record.</span></div>
        <div class="flow-step"><strong>Existing health system</strong><span>DHIS2/OpenMRS-like systems, NGO tools, or referral workflows.</span></div>
      </div>
      <p class="muted-note">
        The architecture also leaves room for future offline bundle concepts for low-connectivity programs.
      </p>
    </section>

    <section class="section">
      <div class="panel">
        <h2>Explore the concept safely</h2>
        <p>
          The guided demo uses fake cases only. Technical docs remain available for API reviewers.
        </p>
        <div class="button-row">
          <a class="button-link" href="/guided-demo">Open guided demo</a>
          <a class="button-link secondary" href="/docs">View technical docs</a>
          <a class="button-link secondary" href="https://github.com/Skydax-IT/MedProtocol-API/blob/main/PROJECT_STATUS.md">Read project status</a>
        </div>
      </div>
    </section>
  </main>
  <footer class="footer-note">
    <strong>Secondary links:</strong>
    <a href="/demo">Technical Demo Console</a> ·
    <a href="/health">System Status</a> ·
    <a href="/redoc">ReDoc</a> ·
    <a href="https://github.com/Skydax-IT/MedProtocol-API/blob/main/PROJECT_STATUS.md">Project Status</a> ·
    <a href="https://github.com/Skydax-IT/MedProtocol-API/blob/main/ROADMAP.md">Roadmap</a>
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
      grid-template-columns: minmax(300px, 390px) 1fr;
      gap: 26px;
      align-items: start;
    }
    .cases { display: grid; gap: 12px; }
    .case-button {
      width: 100%;
      text-align: left;
      background: #fff;
      color: var(--ink);
      border-radius: 18px;
      box-shadow: var(--shadow-soft);
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
      border-radius: 16px;
      padding: 14px;
      min-height: 72px;
      background: linear-gradient(180deg, #ffffff, var(--soft));
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
      gap: 14px;
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
      <a href="/#integration">Integration</a>
      <a href="/#safety">Safety</a>
      <a href="/demo">Technical Demo Console</a>
      <a href="/docs">Technical Docs</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>Demo only — not for real patient care</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>

  <main class="guided-layout">
    <section class="panel">
      <div class="version-label">$demo_label</div>
      <h1>Guided product walkthrough</h1>
      <p class="lead">
        This guided demo uses fake cases to show how an existing field tool could call MedProtocol API.
        It is not a clinical tool and must not be used for real patients.
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
        <div class="field wide"><strong>What the field worker observes</strong><span id="observations">-</span></div>
        <div class="field wide"><strong>What MedProtocol checks</strong><span id="checks">-</span></div>
      </div>
      <div class="button-row">
        <button type="button" id="runGuided">Run demo triage</button>
      </div>

      <section class="section">
        <div class="step-label">Step 2 — Protocol engine result</div>
        <h2>What the field worker would see</h2>
        <div id="guidedStatus" class="status">Run the fake case to see the demo output.</div>
        <div class="result-grid">
          <div class="field"><strong>Urgency level</strong><span id="guidedUrgency">-</span></div>
          <div class="field"><strong>Referral required</strong><span id="guidedReferral">-</span></div>
          <div class="field wide"><strong>Immediate action</strong><span id="guidedAction">-</span></div>
          <div class="field"><strong>Danger signs detected</strong><span id="guidedDanger">-</span></div>
          <div class="field"><strong>Missing critical data</strong><span id="guidedMissing">-</span></div>
          <div class="field wide"><strong>Low-connectivity message</strong><span id="guidedSms">-</span></div>
          <div class="field wide"><strong>Why this was triggered</strong><span id="guidedWhy">-</span></div>
        </div>
      </section>

      <section class="section">
        <div class="step-label">Step 3 — Traceability</div>
        <h2>Traceability</h2>
        <div class="result-grid">
          <div class="field"><strong>Rule ID</strong><span id="guidedRule">-</span></div>
          <div class="field"><strong>Protocol version</strong><span id="guidedProtocol">-</span></div>
          <div class="field"><strong>Validation status</strong><span id="guidedValidation">-</span></div>
          <div class="field"><strong>Audit ID</strong><span id="guidedAudit">-</span></div>
          <div class="field"><strong>Role used</strong><span id="guidedRole">-</span></div>
          <div class="field"><strong>Demo-only status</strong><span id="guidedDemoStatus">-</span></div>
        </div>

        <div id="guidedCopyRow" class="copy-row">
          <button type="button" id="copySummary">Copy summary</button>
          <button type="button" id="copyGuidedSms">Copy SMS/USSD message</button>
          <button type="button" id="copyTechnicalJson">Copy JSON</button>
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
    use the <a href="/demo">Technical Demo Console</a>, <a href="/docs">Technical Docs</a>, or <a href="/redoc">Alternative API Docs</a>.
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
        checks: "Danger signs first, then role scope and demo protocol metadata.",
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
        checks: "Pregnancy danger sign demo rule, midwife role, and protocol version.",
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
        checks: "Missing critical data before producing a complete demo interpretation.",
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
      setText("checks", item.checks);
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
      border-radius: 16px;
      padding: 14px;
      min-height: 72px;
      background: linear-gradient(180deg, #ffffff, var(--soft));
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
      <a href="/#integration">Integration</a>
      <a href="/#safety">Safety</a>
      <a href="/demo">Technical Demo Console</a>
      <a href="/docs">Technical Docs</a>
    </div>
  </nav>
  <div class="warning-strip">
    <span>Demo only — not for real patient care</span>
    <span>No real patient data. No validated clinical protocol. No diagnosis or treatment recommendation.</span>
  </div>

  <main class="demo-layout">
    <section class="panel">
      <div class="version-label">$demo_label</div>
      <h1>Technical Demo Console</h1>
      <p>
        This page is for developers and technical reviewers. For a non-technical walkthrough,
        open the Guided Demo.
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
        api_version=settings.version,
        demo_ux_version=f"v{settings.demo_version} polished business demo",
        product_stage=settings.product_stage.title(),
        clinical_status="Demo only — not validated for real care",
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
