# AI–People's Court: operating model and pilot plan

**Status:** Research prototype specification. Not an application for judicial authority, not legal advice, and not evidence of court approval or operational readiness.

## 1. Purpose

AI–People's Court explores a workflow in which AI organises case material and prepares a reviewable draft, citizens independently scrutinise fairness and source support, material disagreements are documented, and a legally authorised judicial officer independently determines the matter.

The present implementation is a synthetic-data workflow demonstrator. It does not generate legal findings from a complete case record, retrieve or verify current legal authorities, authenticate evidence, conduct hearings, or issue a judgment. The draft text is supplied by a demo operator.

## 2. Non-negotiable boundary

- Every output is advisory and non-binding.
- No AI or panel output may automatically determine guilt, liability, bail, sentence, compensation, custody, or other legal outcome.
- A case reaches the demo `decided` state only when a human judicial-officer attestation is recorded. This status is a software workflow marker, **not** a valid court order.
- Use fictional/synthetic data only. The API rejects case creation unless the caller attests to synthetic data.
- The demo API is disabled by default. Enabling it requires `NYAYA_PEOPLES_COURT_DEMO_ENABLED=true` and `NYAYA_PEOPLES_COURT_DEMO_TOKEN` set to a random value of at least 24 characters. Do not expose the in-memory demo publicly.
- The workflow store is in memory and is lost on process restart. It has no real identity verification, institutional role management, durable audit storage, encryption-at-rest policy, or court-grade access controls. It is not suitable for real case files.

## 3. Implemented prototype workflow

1. Create a synthetic case with category, party labels, issue summary and source/evidence references.
2. Submit an explicitly labelled draft package with issues, authorities supplied, limitations and source-coverage note.
3. Record independent advisory reviews, including checks for fairness, contrary evidence and source traceability.
4. Record objections with severity and affected evidence references.
5. Record a response to each objection, including whether it remains unresolved.
6. Escalate objections or review disagreements to the judicial-review stage.
7. Record a judicial-officer determination attestation that the original record and panel dissent were considered and the decision was independently reached.
8. Inspect the workflow record and append-only-in-process audit events.

The state machine rejects duplicate reviewer submissions, invalid transitions, missing human-review requirements and judicial determinations without the required attestations. The audit history is only in memory and is not cryptographically tamper-evident.

## 4. Differentiated safeguards by case category

These are proposed product rules, not a statement that current Indian law authorises citizen adjudication.

| Category | Prototype / research treatment | Additional controls before any live pilot |
|---|---|---|
| Routine civil and contract | Draft and issue review, source mapping, competing submissions | Court-approved procedure, service and hearing rights, enforceability and appeal route |
| Consumer | Record completeness, transaction chronology, relief and calculations | Applicable consumer forum procedure and authority, consumer accessibility |
| Family | No automated recommendation about custody or family status | Privacy, child safety, sensitive evidence restrictions, judicial control of hearings |
| Criminal | Synthetic workflow only; no guilt, bail, sentencing or credibility predictions | No automated verdict/sentence; criminal-procedure review, defence rights, admissibility and burden-of-proof safeguards |
| Constitutional / public law | Research and draft structure only | Jurisdiction, authoritative precedents, public-interest and institutional review |
| Service / administrative | Evidence and timeline organisation | Statutory appeal routes, limitation and applicable service rules |
| Motor accident | Document inventory and arithmetic checks only | Evidence verification, damages methodology and judicial determination |
| Other / complex | Escalate for human legal review | Category-specific legal and procedural review before use |

Do not use AI to score a person's credibility, predict recidivism or flight risk, recommend bail, or generate a conviction or sentence. Do not infer an outcome from historical patterns or synthetic model confidence.

## 5. Legal feasibility and approvals

Before a real institutional trial, obtain a written legal opinion and approvals from the competent High Court / court administration and relevant authorities. Confirm the then-current status and applicability of the Supreme Court's 2026 draft AI regulations, all relevant High Court rules and directions, procedural statutes, constitutional requirements, privacy law, evidence rules, and institutional security policy.

A software workflow cannot itself confer judicial power. Any binding citizen-panel role or joint adjudicatory mechanism needs a lawful basis, defined jurisdiction, appointment/selection rules, impartiality and recusal safeguards, hearing rights, reasoned decisions, appeal/review route, and accountability arrangements. Until that exists, panel participation must remain non-binding and any live AI use must remain within the approved decision-support boundary.

## 6. Security and architecture gaps before live data

- Replace the shared demo token with institutional identity, MFA, least-privilege RBAC, session controls and independent reviewer identity verification.
- Replace in-memory storage with an approved, durable, transactional database; encrypt data in transit and at rest; design key management, backups and recovery.
- Add case-level tenant boundaries, document access controls, malware scanning, file integrity hashes, retention/deletion controls and audit exports.
- Make audit events durable, append-only and tamper-evident, with time synchronisation and restricted access.
- Complete a privacy impact assessment, data-flow map, lawful-basis analysis, data minimisation, breach-response plan and vendor/model data-use review.
- Prevent training or fine-tuning on court data without explicit institutional approval and legal basis.
- Establish source registry and citation verification; each proposition should link to official text and record source. Mark unresolved citations as unverified.
- Use a threat model, dependency and secret scanning, security testing, accessibility testing and independent penetration test before any exposure beyond a local test environment.
- The current synthetic workflow store is process-local and has no persistence guarantees. Do not use it for actual cases.

## 7. Evaluation protocol

Use fictional records first, including missing exhibits, contradictory dates, forged-looking metadata, conflicting submissions, incomplete translations, incorrect citations, sensitive-data traps and prompt-injection content embedded in documents.

Measure:
- factual/source traceability and unsupported-claim rate;
- citation existence and proposition support;
- coverage of each party's arguments and contrary evidence;
- critical omission and bias findings;
- objection detection, correction rate and unresolved disagreement rate;
- reviewer time, judicial correction time, usability and accessibility;
- API security and workflow-state integrity.

Averages must not hide critical failures. Set acceptance thresholds with independent legal experts and the institutional sponsor before testing. Compare against a documented human-only baseline. Do not claim backlog reduction, accuracy, fairness, or readiness level until a prospective, independently reviewed evaluation supports the claim.

## 8. Suggested 90-day pilot plan (planning target only)

**Days 1–15 — Governance and baseline**
- Identify a willing court / institution and sponsor.
- Confirm case category, legal authority, research ethics, data permission and security environment.
- Document current workflow, baseline time and quality measures.
- Approve synthetic test set, risk register, evaluation rubric and stop conditions.

**Days 16–35 — Technical hardening**
- Implement identity, RBAC, durable storage, document integrity and audit controls in a non-production environment.
- Add citation/source verification and structured evidence links.
- Review threat model, privacy impact and data-flow architecture.

**Days 36–55 — Synthetic evaluation**
- Run end-to-end state-machine, API, security and accessibility tests.
- Conduct adversarial tests and independent legal review of generated packages.
- Fix critical failures; stop if source traceability or procedural safeguards are insufficient.

**Days 56–75 — Shadow-mode evaluation**
- Only after institutional approval, use appropriately authorised data in the institution's approved environment.
- AI output has no legal effect and is not shown as a decision to litigants.
- Compare with normal process and record all corrections and adverse findings.

**Days 76–90 — Independent report**
- Publish methods, limitations, failure analysis and measured results to the sponsor.
- Decide to stop, redesign or seek a separately authorised next phase.
- Do not expand to binding citizen participation without a specific legal basis.

The 90-day period is a planning estimate; legal approvals, procurement and court calendars may take longer.

## 9. Local demo setup

Set environment variables only for a private local environment:

```bash
export NYAYA_PEOPLES_COURT_DEMO_ENABLED=true
export NYAYA_PEOPLES_COURT_DEMO_TOKEN="$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/peoples-court`. Paste the token in the page. Keep the service bound to loopback; do not use this configuration on a public host.

Run tests:

```bash
python -m unittest discover -s tests -v
```

## 10. API overview

When enabled, the prototype exposes:

- `GET /api/peoples-court` — status and limitations.
- `POST /api/peoples-court/cases` — create synthetic case.
- `GET /api/peoples-court/cases` and `GET /api/peoples-court/cases/{id}` — inspect cases.
- `POST /api/peoples-court/cases/{id}/draft` — submit draft package.
- `POST /api/peoples-court/cases/{id}/reviews` — independent panel review.
- `POST /api/peoples-court/cases/{id}/objections` — record objection.
- `POST /api/peoples-court/cases/{id}/objections/{objection_id}/response` — record response.
- `POST /api/peoples-court/cases/{id}/request-judicial-review` — escalate for review.
- `POST /api/peoples-court/cases/{id}/return-for-correction` — request correction.
- `POST /api/peoples-court/cases/{id}/determination` — record human determination attestation.

All workflow endpoints require `X-Demo-Token`. This is only a demo gate, not a substitute for authentication or authorisation.

## 11. Current implementation status

The repository now contains a workflow state machine and browser interface for synthetic demonstration. The following remain unimplemented and block any live-court use: real AI evidence analysis; authoritative legal retrieval and citation verification; secure document ingestion; durable storage; institutional authentication and authorisation; court-system integration; legally authorised citizen-panel procedure; accessibility and language validation; independent validation; production deployment controls; and a real adjudication instrument. This prototype does not constitute a fully operational or legally authorised AI–People's Court.
