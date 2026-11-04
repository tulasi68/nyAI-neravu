# Nyai-Neravu: Master Strategy and Prototype Implementation Plan

**Version:** 1.0  
**Prepared:** 4 November 2026  
**Project:** Nyai-Neravu (nyAI-neravu)  
**Purpose:** Strategy baseline for a Karnataka startup proposal, expert consultation, and staged prototype development  
**Status:** Concept and research prototype proposal — not a funding application, legal opinion, court approval, or claim of operational readiness

---

## Executive summary

Nyai-Neravu proposes an Indian legal-knowledge and case-workflow platform that connects authoritative legal materials to structured, auditable assistance throughout a case lifecycle. Its long-term vision is to help people and authorised legal professionals understand how the Constitution, statutes, rules, regulations and judicial decisions relate to a specific legal question, then assist with organising case records, identifying missing information, conducting structured party exchanges, testing competing arguments, preparing a traceable draft decision, and supporting authorised human judicial review.

The core proposition is **not an autonomous AI judge**. It is a verifiable legal knowledge and case-preparation system, with explicit human accountability and procedural safeguards. The long-term concept may explore more interactive digital hearings and multi-agent review, but the first pilot should be narrower: source-grounded case preparation and judgment-drafting assistance for a carefully selected case category, using synthetic or institution-authorised data and a qualified human reviewer.

The project has an existing software repository with a basic case dashboard, a template-based judgment composer, synthetic-data ML demonstrations, a deterministic Section 138 date-checking endpoint, and a synthetic-only AI–People's Court workflow. These are early prototypes. They do not yet constitute a comprehensive Indian legal repository, semantic legal-reasoning engine, validated evidence-analysis system, production security architecture, or court-integrated service.

The proposed near-term deliverable is a **clickable end-to-end workflow demonstrator** with realistic placeholders at every major stage. It will make the intended product understandable to a startup evaluator, judge, law-school researcher or potential institutional partner without pretending that unavailable legal data or AI capability already exists. The mock-up should be useful for discussion and requirements discovery; its placeholder data must remain visibly labelled.

## 1. Vision and problem statement

### 1.1 Vision

Make legal knowledge more navigable and case preparation more transparent by connecting every important claim, argument, legal proposition and draft finding to its source, while keeping due process and the authorised decision-maker at the centre.

### 1.2 Problem hypothesis

Potential problems to validate with legal professionals and court stakeholders include:

- Legal materials are spread across multiple portals, document formats, languages and publication systems.
- Finding a complete and current set of applicable authorities can require substantial manual work.
- Long case records can make it difficult to maintain a clear chronology, issue list, evidence map and record of competing submissions.
- Missing, contradictory or poorly referenced material can be discovered late.
- Draft preparation and review may involve repetitive organisation, citation checking and formatting.
- Parties may struggle to understand the procedural stage, what is missing, what they can respond to and what happens next.
- Digital workflows can improve access only if accessibility, language, representation, privacy and procedural fairness are designed in from the beginning.

These are hypotheses, not yet measured findings about all Indian courts. Before making quantitative claims, the project should interview stakeholders and establish a baseline for a specific case category and workflow.

### 1.3 Intended value

**For authorised legal professionals and courts**
- Structured case chronologies, issue maps and document inventories.
- Source-linked summaries and a visible list of missing or conflicting material.
- Legal research assistance that distinguishes binding, persuasive, superseded and unverified authorities.
- Draft structures that preserve the parties' competing positions and identify unsupported statements.
- Reviewable audit history and measurable correction effort.

**For litigants and representatives**
- Clearer explanations of procedural steps and requested information.
- A structured way to submit and respond to materials where permitted by the relevant procedure.
- Accessible status information without representing the AI as a judge or lawyer.
- A clear record of what was submitted, what remains disputed and what the authorised court has decided.

**For public institutions and research partners**
- A controlled, measurable environment for evaluating legal AI safeguards.
- Evidence about where AI assistance is useful, unreliable or inappropriate.
- A staged route from synthetic demonstration to approved shadow-mode evaluation, if an institution chooses to participate.

## 2. Product principles and non-negotiable boundaries

1. **Human legal authority remains intact.** Software does not acquire judicial power by implementing a workflow or generating a document.
2. **Source-first answers.** Material legal statements should link to source text and identify jurisdiction, date, version, court and relevant paragraph/section where available.
3. **No fabricated completeness.** Missing documents, unverified authorities and unresolved questions remain explicit.
4. **Equal procedural opportunity.** Each party must have an appropriate opportunity to see and respond to material relied on, subject to lawful confidentiality and protective orders.
5. **No hidden outcome scoring.** Synthetic ML predictions are not used to recommend guilt, liability, bail, sentence, compensation, custody or disposition.
6. **No consensus-as-truth.** Agreement among three AI models is a review signal, not proof of legal correctness.
7. **Privacy by design.** Development uses fictional data. Real case data is prohibited until an authorised institution approves the lawful basis, environment, access controls, retention, model/vendor terms and security plan.
8. **Accessible and multilingual by design.** Language assistance must preserve the original text, flag uncertain translation and provide a way to correct errors.
9. **Auditable change history.** Inputs, source versions, model/configuration versions, reviewer actions, corrections and output versions should be traceable.
10. **No claims ahead of evidence.** No claim of legal accuracy, bias elimination, court adoption, backlog reduction, technology readiness level or production readiness without documented evaluation.

## 3. Product scope: long-term platform and first pilot

### 3.1 Long-term platform vision

The broader system has six connected engines:

A. **Indian Legal Knowledge Engine** — versioned laws, rules, regulations, judgments and official legal materials, connected through citation and legal-relationship graphs.

B. **Case Understanding and Evidence Engine** — document inventory, OCR, extraction, chronology, issue framing, evidence references, contradictions, missing information and party attribution.

C. **Fair-Hearing Workflow Engine** — notices, submissions, counter-submissions, questions, response deadlines, accessibility and a procedural record.

D. **Independent Analysis and Challenge Engine** — multiple analysis passes, contrary-authority search, source verification, counterarguments, uncertainty reporting and escalation.

E. **Draft Decision and Human Review Engine** — issue-wise draft reasoning, review annotations, corrections, final human decision reference and appeal-related workflow information.

F. **Trust, Audit and Governance Engine** — identity, role controls, privacy, security, source/model versioning, audit exports, monitoring, incident handling and independent evaluation.

### 3.2 Recommended first pilot

The initial pilot should **not** attempt nationwide ingestion of all law, automated hearings or AI adjudication. It should demonstrate one defined workflow and one carefully selected case category.

Recommended pilot objective:

> Evaluate whether source-grounded case-record organisation and judgment-drafting assistance can reduce avoidable preparation effort while preserving factual traceability, treatment of contrary material, legal-source integrity and full human control.

The case category must be selected with an authorised legal/institutional partner. A category such as routine, document-heavy matters may be explored, but no category should be declared suitable without legal and procedural review. Criminal, family, custody, liberty, credibility-sensitive and other high-impact decisions require especially restrictive treatment; the prototype must not recommend guilt, bail, sentence or credibility findings.

### 3.3 Prototype now

The current mock-up will represent the full envisioned flow with sample records and editable placeholders:

1. Case intake and jurisdiction.
2. Document and evidence inventory.
3. Case chronology and issue framing.
4. Legal knowledge search and authority graph.
5. Party submissions and counter-questions.
6. Three independent AI review lanes.
7. Disagreement, omission and source verification.
8. Draft decision with issue-wise reasoning.
9. Human judicial review and decision reference.
10. Audit trail, correction history and appeal information.

All prototype data and simulated AI output must be clearly marked fictional or illustrative. No model call, live law search, court integration, or real legal decision should be implied unless actually implemented and validated.

## 4. Legal knowledge strategy

### 4.1 Source hierarchy

The source registry should prioritise authoritative primary material and record provenance. Depending on the material and legal permissions, candidate source classes include:

- Constitution of India and amendments.
- Central Acts and subordinate legislation.
- State Acts, rules, notifications, circulars and applicable Karnataka materials.
- Supreme Court judgments and orders.
- High Court judgments and orders, including relevant Karnataka High Court materials.
- Other court/tribunal decisions where relevant and lawfully available.
- Official procedural rules, practice directions and administrative notifications.
- Carefully identified secondary commentary as commentary—not as binding law.

The project must assess terms of use, copyright, access conditions, bulk download permissions, APIs, update frequency and completeness for each source. A publicly viewable page does not automatically grant permission to bulk-republish or use the material for every purpose.

### 4.2 Data model

At minimum, each source record should capture:

- Stable internal ID and source-system ID.
- Source type and official/secondary status.
- Title, court/authority, jurisdiction, case number/citation, date and language.
- Official URL or document identifier and retrieval timestamp.
- Document hash and original file preservation reference.
- Text/OCR version, page/paragraph/section coordinates and extraction quality.
- Enactment/amendment/effective dates where applicable.
- Cited-by, cites, follows, distinguishes, overrules, interprets and related-provision links, with provenance for each relationship.
- Verification state: imported, OCR-reviewed, metadata-verified, text-verified, legal-treatment-reviewed, superseded or unresolved.
- Access/licensing classification and retention rules.

### 4.3 Retrieval and legal relationships

The intended engine should combine keyword search, structured filters, citation graph traversal and semantic retrieval. Retrieval results should be reranked using jurisdiction, court hierarchy, date, legal status, subject matter and factual/legal relevance. Each answer should separate:

- The source text.
- A faithful summary.
- The legal proposition being considered.
- The reason the source may apply.
- Contrary or distinguishing authorities.
- The current verification state.
- Any uncertainty or missing research.

A generated summary must never overwrite the original source. Legal relationships should not be inferred solely from text similarity; they need provenance and appropriate review. The system must account for amendments, commencement dates, prospective/retrospective operation and the legal treatment of precedents.

### 4.4 Updates and coverage claims

Define a source-by-source ingestion and update service with reconciliation, failed-update alerts, duplicate detection and version history. Show users the last successful update and known coverage gaps. Do not claim “all Indian law” until coverage has been audited against a defined, published inventory. “Comprehensive” should always be scoped by source, jurisdiction, period, language and document type.

## 5. End-to-end case lifecycle

### Stage 1 — Intake and eligibility
Capture case type, jurisdiction, parties/representatives, requested relief, procedural stage, dates, urgency, accessibility/language needs and source-system reference. Verify jurisdiction and eligibility through rules reviewed by legal experts. The system should not silently accept an out-of-scope matter.

### Stage 2 — Record collection and integrity
Accept authorised documents through approved channels. Preserve originals, calculate hashes, record upload/source metadata, run malware checks, classify sensitive information, and maintain page/paragraph references. OCR confidence and extraction errors must be visible. Never treat an OCR transcript as the original evidence.

### Stage 3 — Chronology, issues and missing information
Produce a proposed chronology and issue list, with every item attributed to a party or source. Identify conflicts and missing documents. Each party should be able to correct factual extraction or challenge an attribution through the approved process.

### Stage 4 — Legal research
Retrieve relevant legal materials, explain why each is included, show contrary authorities and distinguish binding from persuasive authority. Verify citation existence and proposition support. If verification fails, label it unresolved and prevent it from being presented as confirmed law.

### Stage 5 — Party submissions and questions
Provide a structured submission space only within a legally approved process. Each request for additional material should identify the question, why it matters, deadline and response opportunity. The system must not coach one party secretly or disclose protected information. Any counter-question must be neutral, recorded and available to the parties as required by procedure.

### Stage 6 — Independent analysis
Run separate analytical tasks: issue/element mapping, evidence-to-claim mapping, contrary-evidence search, legal-authority checking, procedural completeness and alternative interpretation. Keep outputs separately attributable. A “three-model panel” may be explored, but different providers do not guarantee independence; data handling and confidentiality conditions must be reviewed before using external APIs.

### Stage 7 — Challenge and reconciliation
Compare substantive reasons, citations, evidence references and unresolved questions. Do not reduce disagreement to a majority vote. Escalate conflicting legal authorities, unsupported material findings, critical extraction uncertainty, missing responses or high-impact questions. Preserve dissent and the reason for any resolution.

### Stage 8 — Draft decision package
Prepare a structured draft containing procedural history, issues, each party's arguments, undisputed and disputed facts, evidence references, applicable law, competing interpretations, issue-wise proposed findings, relief analysis, unresolved issues and a source/limitations appendix. Distinguish proposed AI analysis from judicial findings. All operative orders remain for the authorised decision-maker.

### Stage 9 — Human review and decision
The authorised reviewer can inspect sources, request correction, change reasoning, reject the draft or create a decision independently. The system records reviewer identity, role, version and decision reference. It must not represent a draft, attestation or demo status as a valid judgment.

### Stage 10 — Post-decision and appeal information
Where legally and institutionally appropriate, present the issued decision reference, service/status information, applicable procedural next steps and appeal/review information from verified sources. Never invent a limitation period or imply an appeal route without checking the governing law and facts.

## 6. Multi-agent review design

### 6.1 Proposed roles

- **Analyst:** extracts issues, chronology and competing submissions.
- **Independent challenger:** attempts to find omitted facts, contrary authorities and alternative legal interpretations.
- **Source auditor:** checks citations, quotations, proposition support, source versions and unsupported claims.
- **Coordinator:** compares findings and produces a disagreement report; it does not vote to determine the legal outcome.

Potential future providers include models from different vendors, subject to procurement, API access, privacy, residency, retention, security and cost assessment. Model identities and versions must be recorded. If one provider is unavailable, the system must disclose that the intended independent review did not occur.

### 6.2 Why agreement is not proof

Models can share training data, retrieval errors, prompting biases and common blind spots. Three agents may all accept an outdated or misinterpreted authority. Accordingly:

- Check sources independently of model-generated citations.
- Give agents the same verified record and preserve provenance.
- Where practical, vary tasks and reasoning approaches rather than merely asking three models the same question.
- Evaluate agent agreement and disagreement against expert-labelled test cases.
- Escalate critical disagreement; never let a simple majority override authoritative law.
- Maintain an explicit abstention state for insufficient evidence or unverifiable law.

## 7. Human rights, fairness and safety

Required design controls include:

- Equal access to the material relied on, with appropriate legal exceptions.
- Notice and meaningful opportunity to respond.
- Human accessibility routes for people with disabilities, limited connectivity or low digital literacy.
- Language support that retains original text and flags uncertain translation.
- Conflict-of-interest, recusal and reviewer-independence procedures for any human panel.
- No automated credibility scoring, guilt determination, sentencing, bail recommendation, child-custody recommendation or similar high-impact disposition.
- No use of protected characteristics or proxies as unsupported decision factors.
- Clear explanations of system limitations and routes to challenge errors.
- Separate handling of confidential, sealed, child-related, medical, financial and other sensitive records.
- No public exposure of case documents or audit logs.
- Security and legal review of prompt injection in documents, malicious files and data-exfiltration risks.

Citizen review, if explored, is initially advisory research only. A legally binding citizen jury or AI adjudicatory role requires a specific lawful basis and institutional design; it cannot be created by software alone.

## 8. Technical architecture and data boundaries

### Prototype layer
Static or server-rendered UI, synthetic fixtures, simulated AI lanes and mock event log. The prototype must work without API keys and must display “simulation” labels. Browser storage, if used, is only for temporary demo convenience and not a secure record store.

### Research layer
FastAPI service; typed case/record/issue/authority/review schemas; local or approved object storage; relational metadata store; search index; vector index only when justified; retrieval service; source verifier; model gateway; evaluation harness; audit event service. Use synthetic/anonymised test records until approvals are in place.

### Institution-approved pilot layer
Institutional identity and MFA, least-privilege role controls, case-level authorization, approved hosting, encryption, managed keys, backups, monitoring, security incident process, durable tamper-evident audit, data retention/deletion controls, vendor review and penetration testing. The institution must own or approve the operational data boundary.

### Production boundary
No production design should be assumed complete until it has passed legal, privacy, security, accessibility, reliability and operational acceptance reviews. External model providers must not receive case material until the institution has approved the processing terms and data-flow design.

## 9. Governance, law and approvals

Before any real-case pilot, obtain qualified Indian legal advice and written approval from the competent institution. Confirm the legal status and applicability at that time of all relevant constitutional provisions, procedural statutes, evidence law, court rules and directions, privacy/data-protection law, records-retention requirements, government security requirements, and applicable AI governance guidance.

The project must not assume that a startup grant, research memorandum or technology partnership authorises access to case records or judicial decision-making. A pilot agreement should define scope, data controller/processor roles where applicable, lawful basis, permitted uses, model training restrictions, access, retention, breach response, publication, liability, audit, human oversight, evaluation, stop conditions and exit/data deletion.

The exact legal analysis should be undertaken by qualified counsel with institutional stakeholders. This document is a planning framework, not a legal opinion.

## 10. Evaluation plan and success measures

Define the evaluation rubric with legal experts before testing. Use synthetic and expert-reviewed fictional cases first, then authorised anonymised or shadow-mode data only if approved.

Suggested metrics:
- **Source integrity:** citation existence, source authenticity, correct version/date, proposition support.
- **Factual traceability:** proportion of material factual statements with valid source links; unsupported-claim rate.
- **Completeness:** issue coverage, party-argument coverage, contrary-evidence coverage, missing-document detection.
- **Reasoning review:** material error rate, critical omission rate, quality of alternative interpretations, unresolved ambiguity.
- **Fairness:** equal representation of submissions, consistent process, accessibility and language error rates.
- **Workflow quality:** completion rate, reviewer correction effort, time spent per task, usability and abandonment.
- **Reliability/security:** access-control tests, audit integrity, data leakage tests, prompt-injection resilience, service availability.
- **Human outcomes:** expert assessment of usefulness and workload—not simply model agreement.

Report denominators, case mix, confidence intervals where appropriate, critical failures separately and limitations. Compare against a documented human-only baseline. Do not claim that the system reduces pendency until a suitable prospective evaluation supports the claim.

## 11. Delivery roadmap

### Phase 0 — Strategy and stakeholder discovery (0–4 weeks; planning estimate)
- Finalise product boundary and target pilot workflow.
- Interview legal professionals, court administration, law-school researchers and potential public-sector sponsors.
- Select a candidate case category only after legal and institutional review.
- Map current workflow and collect baseline estimates.
- Prepare a source inventory, risk register, evaluation plan and stakeholder feedback record.

**Exit criteria:** documented problem validation, named target user, defined pilot boundary, initial legal questions and agreed evaluation measures.

### Phase 1 — Clickable workflow demonstrator (1–3 weeks; planning estimate)
- Build an integrated dashboard covering every major stage.
- Use fictional sample data and explicitly simulated AI outputs.
- Allow navigation, editing of mock submissions, staged review, objection, draft review, human approval reference and audit display.
- Include source cards, uncertainty states, missing-evidence flags and visible limitations.
- Prepare a demo script and screenshots.

**Exit criteria:** a stakeholder can understand the proposed workflow in a short demonstration without being misled about what is implemented.

### Phase 2 — Verified legal-source demonstrator (4–10 weeks; planning estimate)
- Select a small, licensed/authorised corpus of primary legal materials.
- Implement ingestion, metadata, text/page/paragraph provenance and version tracking.
- Add search and source-linked answers with explicit uncertainty.
- Create a legal expert evaluation set and citation-validation tests.

**Exit criteria:** every demonstrator answer has inspectable source references; known coverage and failure limits are published.

### Phase 3 — Record-grounded case analysis (8–16 weeks; planning estimate)
- Add document ingestion, OCR confidence, chronology, issue map and claim/evidence links.
- Add source and contradiction checks and structured draft generation.
- Add adversarial tests for omissions, incorrect dates, contrary evidence, hallucinated citations and malicious document text.
- Evaluate with qualified legal reviewers using synthetic records.

**Exit criteria:** independently reviewed results meet pre-agreed thresholds and no critical safeguard failures remain unresolved.

### Phase 4 — Institution-approved shadow pilot (duration determined with partner)
- Execute approved data/security/legal agreements.
- Operate in a controlled environment with no automatic legal effect.
- Compare output and review effort against normal workflow.
- Report failures, corrections, benefits and limits.

**Exit criteria:** partner accepts an independent evaluation report and chooses whether to continue, redesign or stop.

### Phase 5 — Carefully governed expansion
Only after a successful evaluation and separate approvals should the project expand to additional sources, languages, case types, or court-system integrations. Any change in legal effect or decision authority requires separate legal and institutional approval.

All timelines are estimates for planning and depend on partner access, source permissions, technical scope and review capacity.

## 12. Team and resource strategy

A credible early project does not need to build the entire legal corpus. It needs to prove a small, defensible capability and secure expert feedback.

Minimum skills needed across the project:
- Product owner and software engineer.
- Indian legal researcher or qualified legal reviewer.
- Data/IR engineer for source ingestion, search and provenance.
- Security/privacy reviewer before any sensitive data use.
- UX/accessibility and Kannada/English language expertise as scope grows.
- Institutional sponsor for any live workflow.

One founder may coordinate and build the early prototype, but should not claim to independently supply legal validation, court authority, nationwide data coverage or production security. Seek collaboration with a law school, legal aid organisation, public institution or research partner for domain review and evaluation.

Cost drivers include data permissions and curation, legal expert time, OCR and storage, search infrastructure, model/API usage, secure hosting, independent evaluation and security testing. The first prototype should use local/static mock data and avoid paid model calls. A funding request should be based on itemised work packages and partner-confirmed scope, not a speculative nationwide build estimate.

## 13. Karnataka startup proposal framing

### Suggested working title
**Nyai-Neravu: Source-Grounded AI Assistance for Transparent Case Preparation and Judicial Review**

### Suggested short description
Nyai-Neravu is a research-stage legal technology platform concept that connects Indian legal sources to structured case preparation. It aims to help authorised legal professionals organise evidence, trace factual and legal assertions to sources, identify missing or conflicting material, compare competing arguments and prepare reviewable draft decisions. The proposed initial pilot is narrow and human-supervised, with synthetic-data validation first and institution-approved shadow evaluation only after legal, privacy and security approvals.

### Innovation claim
The proposed differentiation is the integration of:
- Legal-source provenance and versioning.
- Record-to-issue-to-authority traceability.
- Explicit contrary-evidence and missing-information checks.
- Independent AI challenge lanes with disagreement preservation.
- A structured party-response workflow.
- Human judicial control and auditable draft correction.

These are proposed capabilities to demonstrate and validate, not claims that the current repository already delivers them end-to-end.

### Public value
Potential benefits to test include reduced repetitive preparation work, improved transparency of sources and missing information, better-structured records, and more reviewable draft documents. Avoid promising that AI will eliminate corruption, bias, backlog or judicial error. Instead, test whether specific controls reduce measurable errors or effort under controlled conditions.

### Stage and readiness statement
Describe the project as a **software prototype / concept-validation stage**. State that current AI outputs are simulated or limited, data is synthetic, no court integration or judicial authority is established, and a legal/institutional partner is sought for validation. Do not claim a TRL number unless the relevant programme's criteria have been assessed and documented.

### Proposed grant work packages
1. Product discovery and legal/procedural design.
2. Clickable workflow demonstrator.
3. Small authoritative legal-source corpus and provenance prototype.
4. Synthetic case-record analysis and source verification.
5. Independent legal, privacy, security and accessibility evaluation.
6. Partner workshop and pilot feasibility report.

Budget and milestones should be adjusted to the specific Karnataka programme's eligibility rules, current call, allowed expenses, matching requirements, procurement route and deadline. Do not assume a grant or work order will be awarded.

## 14. Expert outreach plan

Approach a judge, retired judge, law faculty member or legal research centre with a request for **critique and guidance**, not endorsement or access to confidential cases.

A first discussion should ask:
1. Which narrow case-preparation task causes repetitive effort today?
2. Which source materials can be used lawfully and reliably?
3. What is the minimum acceptable citation and evidence traceability?
4. What risks or procedural requirements would make the workflow unacceptable?
5. What case category, if any, is appropriate for synthetic or shadow-mode evaluation?
6. What institutional approval and research ethics steps are required?
7. What measurable success criteria would justify a second phase?

Do not use an individual's name, logo, comments or meeting as an endorsement without written permission. Do not send confidential records to the prototype. A law school can be a research and evaluation partner, but it cannot by itself authorise court use unless it has the relevant authority.

## 15. Principal risks and mitigations

| Risk | Mitigation |
|---|---|
| Hallucinated or outdated law | Primary-source registry, versioning, citation checks, legal review and abstention |
| Three agents agree on a wrong answer | Independent source validation, adversarial challenge, expert-labelled evaluation; no majority-vote verdict |
| One party's evidence is omitted | Party attribution, source maps, response rights, contrary-evidence checks and review |
| Biased or inaccessible process | Accessibility testing, language controls, fairness review and human complaint route |
| Sensitive case data leakage | Synthetic-first development, approved environment, least privilege, vendor review and retention controls |
| False impression of court authority | Persistent prototype labels, human decision boundary and careful public claims |
| Data coverage is overstated | Published source inventory, coverage status and update timestamps |
| Prototype overreaches | Narrow pilot scope, stage gates, documented stop conditions and partner approval |
| No institutional partner | Validate demand with interviews before spending on expensive data ingestion or multi-agent infrastructure |
| Founder capacity / funding gap | Prioritise demonstrator, obtain domain collaboration, budget by work package and avoid nationwide scope initially |

## 16. Immediate next actions

1. Review the integrated workflow mock-up and confirm that the story is understandable.
2. Prepare a short demo script and one-page concept note from this strategy.
3. Identify the specific Karnataka startup call and map its actual eligibility, deadline, deliverables and budget rules.
4. Arrange 3–5 discovery conversations with legal professionals, law-school researchers and potential public-sector stakeholders.
5. Select a pilot use case only after feedback.
6. Keep all public descriptions precise about what is simulated, what exists in code and what remains a hypothesis.
7. Make no live-data or court-use commitment until an authorised partner and qualified counsel approve the plan.

---

## Appendix A — What exists today versus what is proposed

| Capability | Current repository position | Target |
|---|---|---|
| Existing dashboard | Basic demo dashboard with synthetic records and legacy ML labels | Clear product landing and guided workflow |
| Judgment draft | Template-based composition from supplied fields | Source-grounded, issue-wise, reviewable draft |
| Legal knowledge repository | Not implemented as a comprehensive corpus | Versioned primary-source registry and legal relationships |
| Legal research | No complete live, authoritative legal retrieval pipeline | Source-linked retrieval with citation and treatment checks |
| Document evidence analysis | Limited synthetic traceability aid | Page/paragraph-level document and claim mapping |
| Online party hearing | Workflow concept and mock steps only | Institution-approved, procedure-compliant submission and response workflow |
| Three-AI review | Proposed concept, not an established independent review system | Evaluated independent analysis lanes and disagreement controls |
| Human judicial review | Demonstration workflow markers only | Approved workflow under competent institutional authority |
| Audit | In-memory demo event history in one workflow | Durable, access-controlled, tamper-evident audit with export |
| Security and identity | Not court-grade; demo token/in-memory limitations | Institutional identity, MFA, RBAC, data controls and independent testing |
| Court integration | Not implemented | Only through approved institutional interfaces |
| Legal validity | Not established | Determined by competent authorities; software cannot create it |

## Appendix B — Short positioning statement

Nyai-Neravu is not presented as a replacement for judges or as a claim that AI can eliminate bias. It is a proposal to make legal research and case preparation more traceable, structured and reviewable. Its initial objective is to test whether source-grounded assistance can reduce repetitive work without weakening due process, transparency or human accountability. The long-term ambition is a connected legal knowledge and case workflow platform, developed incrementally with legal experts and authorised institutions.
