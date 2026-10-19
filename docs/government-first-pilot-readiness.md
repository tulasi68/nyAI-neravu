# Government First Readiness Plan — Nyaya Neravu

**Status:** Internal working document; not a funding application or a claim of operational readiness.

## 1. Current position

The repository contains a prototype with:
- A case-linked judgment-drafting interface.
- A structured backend composer that assembles user-supplied information into a formal draft.
- A synthetic-data machine-learning demonstration that classifies case type and predicts outcome labels.
- A deterministic Section 138 date-rule endpoint.

The current draft composer is a template-based composition tool. It does not independently reason over the case file, retrieve current law, authenticate source documents, or validate legal citations. The ML model is trained on synthetic examples and must not be presented as evidence of real-world judicial prediction accuracy.

**Do not claim TRL 7, live-court validation, measurable reduction in pendency, legal accuracy, or government adoption without documented evidence.**

## 2. Recommended product boundary for a first pilot

Prioritise **record-grounded judgment drafting assistance**, not automated dispute resolution or outcome prediction.

The judge or authorised legal reviewer remains responsible for findings, reasoning and the final order. Do not use model predictions to recommend guilt, liability, compensation, sentence, or disposition. Any synthetic prediction display should be conspicuously marked as demonstration-only and excluded from the proposed pilot workflow unless separately justified and approved.

## 3. Readiness gaps to close

### A. Case record and traceability
- Ingest only documents authorised for the pilot.
- Preserve original document identity, page number and stable record references.
- Keep quotations separate from summaries and AI-generated analysis.
- For every material factual assertion, show a source reference or mark it unsupported.
- Detect missing, conflicting and unreadable material instead of silently completing it.

### B. Legal authority integrity
- Provide a source for each statute or case citation.
- Record court, case name/number, date, citation and source URL or document identifier where available.
- Verify that the cited authority exists and that the quoted proposition is supported by the source.
- Mark authorities as unverified until checked against an authoritative source.
- Never fabricate citations or imply that live legal research has been performed when it has not.

### C. Judicial safeguards
- Clearly separate pleadings, party submissions, evidence, disputed facts, proposed analysis and judicial findings.
- Include contrary evidence and arguments, not just material supporting one side.
- Require human approval for every finding and operative direction.
- Keep an audit trail of source inputs, draft versions, edits and review decisions.
- Ensure that no AI-generated output is automatically issued as a judgment or order.

### D. Privacy and security
- Do not upload real case files to an unapproved hosting or model service.
- Use synthetic or properly anonymised material during development.
- Define role-based access, retention, deletion, encryption, incident response and audit requirements with the pilot institution.
- Complete an institutional security and data-protection review before any live-data trial.

### E. Evaluation
- Create an approved, representative evaluation set with a documented source and permission basis.
- Use independent qualified reviewers and a written scoring rubric.
- Measure factual support, citation validity, issue coverage, treatment of contrary evidence, unsupported statements, correction effort and usability.
- Record critical failures separately; do not hide them in an average score.
- Compare against a documented baseline and publish limitations alongside results.

## 4. Proposed staged validation

1. **Offline prototype tests:** Unit tests, API tests, input validation and explicit checks that missing facts remain missing.
2. **Synthetic-record evaluation:** Test end-to-end workflows using fictional case records and deliberately planted gaps or contradictions.
3. **Expert review:** Obtain structured feedback from qualified legal reviewers using approved sample material.
4. **Institution-approved controlled pilot:** Proceed only after a suitable institution, security approval, data protocol, evaluation plan and responsibilities are documented.
5. **Operational validation:** Claim a readiness level only when evidence meets the programme's definition. A working demo alone is insufficient.

## 5. Suggested pilot deliverables

- Requirements and baseline report agreed with the institutional partner.
- Tested case-linked drafting workflow.
- Source-linked record summary and issue-wise draft structure.
- Legal-source verification and unsupported-claim reporting.
- Security, access-control and data-handling documentation.
- Test report including critical failures and corrective actions.
- Human-review evaluation report and recommendation to continue, redesign or stop.

## 6. Government First eligibility checklist

- [ ] Karnataka Startup recognition certificate received and verified.
- [ ] DPIIT recognition status confirmed; required certificate available if mandatory.
- [ ] Incorporation/LLP records and turnover eligibility confirmed.
- [ ] Institutional use case and authorised pilot sponsor identified.
- [ ] Actual readiness level evidenced; no unsupported TRL claim.
- [ ] Technical proposal, architecture, milestones and indicative budget prepared.
- [ ] Compliance and security requirements confirmed with the programme administrator.
- [ ] Pilot data and access arrangements approved in writing.

## 7. Positioning statement

Nyaya Neravu is a prototype for **human-reviewed, record-grounded judgment drafting assistance**. It is not an autonomous judge, and the present repository does not establish operational judicial validation. The proposed Government First engagement should be framed as a request to assess and validate a narrowly scoped workflow under institutional supervision, subject to programme eligibility and approval.
