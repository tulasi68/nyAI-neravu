# Nyaya Neravu (nyAI-neravu)

**AI-assisted judicial workflow and judgment-drafting prototype for evaluation in Karnataka**

> **Important scope and safety notice**
>
> This repository is a research / decision-support prototype. It is not an autonomous adjudication system and must not determine guilt, liability, compensation, sentence or the outcome of a case. Any draft requires independent review by an authorised legal reviewer and/or judicial officer. This demo uses synthetic case data only.
>
> **The machine-learning demonstration is trained on synthetic examples. Its predicted outcome labels are not evidence of real-world accuracy and must not be used to recommend or determine a real case outcome.** The present judgment composer assembles supplied information into a structured draft; it does not independently understand or authenticate the full case record, conduct live legal research, or verify citations.

## Recommended initial pilot scope

The recommended first public-sector use case is **human-reviewed, record-grounded judgment drafting assistance**, subject to an authorised institution confirming a genuine need and approving the pilot.

The intended workflow is to help authorised users organise supplied case particulars, procedural history, each party's position, evidence references, issues for determination, legal authorities and issue-wise analysis into an editable draft. Missing inputs should remain visible. Material assertions should be linked to the source record wherever possible. Findings and the operative order remain for independent judicial determination.

This repository does not establish that the system has been validated in a live court environment, reduced pendency, improved outcomes or achieved a particular Technology Readiness Level.

## What is included

| Component | Description |
|---|---|
| Interactive demonstration UI | Case Operator, Party, Judge and Secretary Dashboard views. Case records and simulated AI outputs are demo material. |
| Machine-learning baseline | TF-IDF and Logistic Regression demonstration for case-type classification, outcome labels and similar-example retrieval. Synthetic-data results must not be treated as judicial evidence or validated predictions. |
| Statutory rules demonstration | Deterministic date checks for selected Section 138 Negotiable Instruments Act timelines. These checks do not decide whether all legal ingredients are proved and require legal review. |
| FastAPI backend | Serves the UI and exposes prediction, rule-checking and judgment-draft endpoints. |
| Judgment Drafting workspace | Case-linked form and structured draft output, with missing-information flags and editable/downloadable text. |
| AI–People's Court workflow prototype | Synthetic-only case intake, advisory panel reviews, objections, response tracking, judicial-review escalation, determination attestations and in-memory audit trail. |

## Case-linked judgment drafting (v1)

The app includes a **Judgment Drafting workspace** at `/judgment-drafting`. In Case Operator, select a case using its checkbox; a per-case **Draft judgment for this case** action appears for selected cases (and cases with a proposal). The workspace carries available demo particulars through tab-scoped session storage rather than putting case facts in the URL. The imported summary and evidence descriptions must be verified against the official record.

The backend endpoint `POST /api/judgment-draft` composes a conventional draft structure from information explicitly supplied by the user, including party narratives, supplied evidence, submissions, issues, analysis and user-provided legal authorities. It uses placeholders and flags missing information rather than intentionally filling gaps with invented facts.

**Current limitation:** the composer is template-based. It does not independently analyse uploaded case files, retrieve current case law, authenticate exhibits or certify legal correctness. All authorities must be independently verified. Use only synthetic, anonymised or appropriately authorised case material, and never send confidential records to an unapproved service.

See [Judgment Drafting v1 API guide](docs/judgment-drafting-v1.md), [Government First pilot readiness plan](docs/government-first-pilot-readiness.md), and interactive API documentation at `/docs` when the service is running.

## Quick start

### Static demonstration

Open `frontend/index.html` in a modern browser or serve it with a static file server.

### Full stack

```bash
git clone https://github.com/tulasi68/nyAI-neravu.git
cd nyAI-neravu

python -m venv .venv
# Windows: .venv\\Scripts\\activate
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000`; API docs are at `http://localhost:8000/docs`, and health status at `http://localhost:8000/api/health`.

### Run draft-composer regression tests

```bash
python -m unittest discover -s tests -v
```

These tests cover draft labels, missing-input behaviour and preservation of supplied references. They do **not** establish legal accuracy, security, operational readiness or suitability for court use.

## Architecture

- Frontend: HTML, CSS and JavaScript.
- Backend: FastAPI, Pydantic, pandas and scikit-learn.
- Draft composer: deterministic structured assembly of user-provided material.
- Section 138 rule endpoint: date checks only, not a complete legal assessment.

## Data and model limitations

The repository demo uses synthetic data. The included ML demonstration should remain isolated from any real judicial workflow unless a separately approved research protocol, appropriate dataset, independent validation, governance and legal review support a different use. High confidence from a model trained on synthetic examples is not evidence of real-world reliability.

Do not train on, upload or expose actual case records without a lawful basis, institutional authorisation and approved privacy/security arrangements. No real court integration or approved operational deployment is established by this repository.

## Pilot roadmap

1. **Prototype tests:** Add and run automated tests for input validation, source references, missing information and safety labels.
2. **Synthetic-record evaluation:** Test deliberately incomplete and contradictory fictional records.
3. **Expert review:** Obtain structured review of factual traceability, citation validity, completeness and correction effort.
4. **Institution-approved controlled pilot:** Proceed only with an authorised partner, written data/security arrangements, agreed evaluation criteria and human oversight.
5. **Operational validation:** Document results and limitations before making any readiness or impact claim.

See [Government First pilot readiness plan](docs/government-first-pilot-readiness.md) for the readiness gaps and eligibility checklist.

## Master strategy and integrated workflow mock-up

The full product vision, legal-source strategy, case lifecycle, multi-agent safeguards, human-authority boundary, staged roadmap, evaluation plan, risk register and Karnataka startup proposal framing are documented in [Nyai-Neravu Master Strategy](docs/nyai-neravu-master-strategy.md).

The integrated, clickable workflow mock-up is available at **[/workbench](https://nyai-neravu.onrender.com/workbench)** when deployed, or by opening `frontend/nyai-neravu-workbench.html` in a browser. It walks through case intake, evidence and chronology, legal-source placeholders, party submissions, three simulated review roles, draft decision, human review and audit/next steps. The interactions are local to the browser session; it does not call AI providers, retrieve live law, persist real cases, notify parties or issue decisions. All sample content is fictional.

This mock-up is intended for product discussion with startup evaluators, legal experts and potential academic or institutional partners. It must not be presented as a working legal-reasoning engine or an authorised court service.

## AI–People's Court workflow prototype

The prototype workflow is available at `/peoples-court`. It demonstrates a proposed sequence of synthetic case intake, draft-package submission, independent citizen review, objection recording and response, escalation, and a human judicial-officer determination attestation. See [AI–People's Court proposal and pilot plan](docs/ai-peoples-court-proposal.md).

The workflow API is **disabled by default**. To test locally with fictional records only:

```bash
export NYAYA_PEOPLES_COURT_DEMO_ENABLED=true
export NYAYA_PEOPLES_COURT_DEMO_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/peoples-court` and paste the generated token. Keep the server bound to loopback. The demo store is process-local and is lost on restart. The shared demo token is not production authentication; do not expose this service publicly or enter real case data.

This prototype does **not** independently analyse a complete case record, verify live legal authorities, authenticate exhibits, integrate with a court, or issue valid judgments. The panel is advisory. The `decided` status is a workflow marker only, not a legal order. Real deployment requires institutional authorisation, a durable and secure data architecture, identity and access controls, independent legal/security validation, and a lawful adjudicatory framework.

Run the workflow regression tests with:

```bash
python -m unittest discover -s tests -v
```

## Synthetic case-record traceability analysis

The AI–People's Court page now includes a **synthetic record traceability** workspace. It maps supplied issues to candidate source excerpts using lexical overlap, lists claims and cited references, flags unknown citations and uncited claims, and highlights potential language/negation differences for human review. See [the traceability milestone notes](docs/case-record-traceability.md).

This is a deterministic completeness aid, **not semantic legal AI**. It does not verify that an exhibit proves a claim, authenticate documents, assess admissibility, retrieve current Indian law, or recommend an outcome. Synthetic data only; demo API remains disabled by default.

## Government First application note

The repository is a prototype / pre-pilot project. Do not claim TRL 7, live-court validation, measured reductions in pendency, legal accuracy or government adoption without evidence meeting the programme's requirements. A government pilot depends on programme eligibility, institutional sponsorship, approvals and selection.

## Licence and contributions

Please treat all outputs as advisory drafts only. Contributions should prioritise source traceability, legal-authority integrity, privacy, security, accessibility, testability and human oversight.

**Nyaya Neravu — supporting reviewable drafting assistance while preserving judicial independence.**
