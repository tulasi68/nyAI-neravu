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

## Government First application note

The repository is a prototype / pre-pilot project. Do not claim TRL 7, live-court validation, measured reductions in pendency, legal accuracy or government adoption without evidence meeting the programme's requirements. A government pilot depends on programme eligibility, institutional sponsorship, approvals and selection.

## Licence and contributions

Please treat all outputs as advisory drafts only. Contributions should prioritise source traceability, legal-authority integrity, privacy, security, accessibility, testability and human oversight.

**Nyaya Neravu — supporting reviewable drafting assistance while preserving judicial independence.**
