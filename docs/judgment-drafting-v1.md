# Judgment drafting v1

The API endpoint `POST /api/judgment-draft` composes a formal, editable draft from case material explicitly supplied by an authorised user.

## What this version does

- Produces conventional judicial sections: parties, procedural history, each side's case, evidence, submissions, points for determination, authorities, issue-wise analysis, conclusion and proposed operative order.
- Preserves supplied exhibit references and source excerpts.
- Flags missing inputs and uses visible placeholders instead of filling gaps with invented facts.
- Returns `status: draft_for_human_review`, missing-information items and safety checks.

## What it does not do

- It does not autonomously determine guilt, liability, compensation, sentence or other outcome.
- It does not retrieve or verify case law live; the caller must provide verified authorities.
- It does not establish that a draft is legally correct or court-ready.
- It does not replace judicial review, hearing rights, or applicable court procedures.

## Example request

```json
{
  "case_type": "Section 138 Negotiable Instruments Act",
  "case_number": "TEST/1",
  "case_title": "A v B",
  "complainant_case": "Summary of the pleaded case, with record references.",
  "defence_case": "Fair summary of the defence, with record references.",
  "procedural_history": "Material dates and procedural orders from the case file.",
  "evidence": [
    {
      "reference": "Ex.P1",
      "description": "Copy of cheque",
      "record_excerpt": "Relevant text transcribed from the authenticated exhibit"
    }
  ],
  "submissions": [
    {"party": "Complainant", "text": "Submission actually recorded at hearing"}
  ],
  "issues": [
    {
      "question": "Whether the statutory requirements are established on the evidence?",
      "applicable_law": "Insert the verified statutory provisions and legal test.",
      "analysis": "Reviewer-prepared analysis tied to evidence, including contrary material.",
      "record_references": ["Ex.P1"]
    }
  ],
  "verified_legal_authorities": ["Insert verified legislation and authorities with accurate citations"],
  "proposed_disposition": "Leave for independent judicial determination.",
  "proposed_order": "Leave for completion by the authorised judicial officer."
}
```

Send this JSON to `POST /api/judgment-draft` with `Content-Type: application/json`. API documentation is available at `/docs` when the FastAPI service is running.

**Important:** Use only anonymised or appropriately authorised records. Do not send confidential court data to a service that has not been approved for it. Every output is an unapproved draft requiring independent legal and judicial review.
