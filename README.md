# Nyaya Assist (nyAI-neravu)

**AI-assisted case resolution for Karnataka courts**  
*A decision-support prototype submitted for the Government of Karnataka call for solutions to people-centric issues.*

> **Important disclaimer**  
> This is research / decision-support software only.  
> Every AI proposal **must** be reviewed by a human judge.  
> It is **not** a substitute for judicial decision-making, does not use real court data in this demo, and must never be treated as an automatic ruling.

---

## The problem we address

Karnataka (and India) faces a large backlog of pending cases. A significant share of the pendency consists of relatively routine matters — cheque bounce (Section 138 NI Act), motor accident claims, consumer disputes, rent & tenancy, and routine service matters. These cases often follow well-established patterns and statutory timelines. Long delays hurt ordinary citizens, small businesses and the credibility of the justice system.

**Nyaya Assist** proposes a practical, transparent workflow that:

1. Learns patterns from *past decided cases* (case type + outcome).
2. Applies clear statutory rules (e.g. Section 138 timelines).
3. Generates a draft proposal that both parties can accept or reject.
4. Escalates automatically to a judge if either party objects or the matter is complex.
5. Keeps a full activity trail for accountability.

The goal is **faster resolution of simple cases** while preserving the judge’s final authority and the parties’ right to be heard.

---

## What is included in this repository

| Component | Description |
|-----------|-------------|
| **Interactive demo UI** | Four role views (Case Operator, Party, Judge, Secretary Dashboard). Fully clickable, works offline. All cases and AI outputs are simulated. |
| **Machine-learning baseline** (`app/legal_ai.py`) | TF-IDF + Logistic Regression that classifies case type, predicts likely outcome, and retrieves similar past cases. |
| **Statutory rules engine** (`app/rules.py`) | Deterministic checks for Section 138 NI Act limitation periods (can be extended to other Acts). |
| **FastAPI backend** (`app/main.py`) | Serves the UI, exposes `/api/predict` and `/api/rules/section-138`, trains a demo model on first run. |

---

## Structured judicial judgment drafting (v1)

The app includes a **case-linked Judgment Drafting workspace** at `/judgment-drafting`. In Case Operator, select a case using its checkbox; a per-case **Draft judgment for this case** action appears for selected cases (and cases with a proposal). The workspace pre-fills the case number, title, parties, case summary, case-operator status and available evidence descriptions using tab-scoped session transfer. It does not treat model predictions as findings, and it does not invent missing record details. Complete and verify the remaining inputs, then generate an editable draft, review missing-information flags, and copy or download the text. The workspace calls `POST /api/judgment-draft`.

The backend now includes an initial structured draft composer at `POST /api/judgment-draft`. It prepares a conventional judgment outline from case details, party narratives, supplied evidence, submissions, issue-wise analysis and user-supplied verified authorities. Missing information is explicitly flagged rather than invented.

This is a **drafting aid only**: it does not decide outcomes, perform live legal research, or certify that a draft is legally correct. Every draft requires independent legal and judicial review. See [the v1 API guide](docs/judgment-drafting-v1.md) and the interactive API documentation at `/docs`.

## Quick start (local)

### 1. Static demo only (no Python needed)

```bash
# Just open the HTML file in any modern browser
open frontend/index.html
# or serve it with any static server
```

In the UI:

1. Switch to **Case operator**.
2. Click **Start learning**.
3. Select a few pending cases → **Apply learning** → **Send proposal to parties**.
4. Click **Demo: simulate party replies**.
5. Check the **Secretary dashboard** and the **Judge** view for escalated cases.

### 2. Full stack (UI + real model API)

```bash
# Clone
git clone https://github.com/tulasi68/nyAI-neravu.git
cd nyAI-neravu

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000  

- The same interactive UI is served.
- API documentation (Swagger): http://localhost:8000/docs  
- Health check: http://localhost:8000/api/health  

Example prediction:

```bash
curl -X POST http://localhost:8000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "complaint under section 138 cheque returned insufficient funds legal notice was served"}'
```

---

## Architecture (high level)

```
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Case Operator  │────▶│  Learning + Rules    │────▶│  AI Proposal    │
│  (select cases) │     │  (legal_ai + rules)  │     │  (draft order)  │
└─────────────────┘     └──────────────────────┘     └────────┬────────┘
                                                              │
                                                              ▼
┌─────────────────┐     ┌──────────────────────┐     ┌─────────────────┐
│  Party Accept / │◀────│  Both parties decide │────▶│  Escalation to  │
│  Reject         │     │                      │     │  Judge          │
└─────────────────┘     └──────────────────────┘     └─────────────────┘
```

- If **both parties accept** → case can be closed as settled (with judicial oversight).
- If **either rejects** or confidence is low → automatic escalation to a judge with full history and documents.

---

## Data note

This prototype ships with **synthetic data only**.  

For a real pilot the system can be trained on open datasets (eCourts / AWS Open Data, NyayaAnumana, PredEx, Indian Kanoon extracts) after proper anonymisation and legal clearance. The training script expects a simple CSV:

```
text,case_type,outcome
"...",cheque_bounce,convicted
...
```

---

## Roadmap (suggested for a Karnataka pilot)

| Phase | Focus |
|-------|--------|
| **0 – Demo (this repo)** | Interactive workflow + baseline model + Section 138 rules |
| **1 – Pilot design** | Select 1–2 court complexes, define data-sharing & privacy protocol, Kannada UI |
| **2 – Integration** | eCourts case status feed, secure document store, role-based auth (SSO) |
| **3 – Evaluation** | Measure reduction in average disposal time for routine cases while tracking quality & appeal rates |
| **4 – Scale** | Additional case categories, multi-language support, audit dashboard for High Court / Law Department |

---

## Technology stack

- Frontend: pure HTML/CSS/JS (no framework) — easy to host and audit
- Backend: FastAPI + scikit-learn + pandas
- Rules: pure Python (easy for legal experts to review and extend)
- Deployment options: any static host for the UI; Railway / Render / Fly.io / on-prem VM for the API

---

## Licence & contribution

This repository is published for evaluation by the Government of Karnataka and interested stakeholders.  

Please treat all AI outputs as **advisory only**.  

For questions or to discuss a pilot, open an issue in this repository or contact the maintainers.

---

**Nyaya Assist / nyAI-neravu**  
*Supporting faster justice for the people of Karnataka — under the supervision of the judiciary.*
