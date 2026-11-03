# AI–People's Court traceability milestone

## What was added

- `app/case_analysis.py`: deterministic, source-traceable analysis of **synthetic** case excerpts.
- `POST /api/peoples-court/analyze-record`: endpoint protected by the existing demo token and disabled-by-default demo gate.
- A browser form on `/peoples-court` for issues, source excerpts, party positions and specific claims with cited references.
- `tests/test_case_analysis.py`: checks synthetic-only validation, unknown references, candidate source mapping, and missing citations.

## What the report does

1. Inventories the provided source excerpts and their identifiers.
2. Creates candidate issue-to-source links using lexical overlap only.
3. Flags claims whose citations do not exist in the supplied source inventory.
4. Reports claims with no citations.
5. Highlights possible language/negation differences between source excerpts for human review.
6. Keeps the parties' positions visible rather than selecting a winner.

## Important limitation

This is **not semantic AI case analysis**. It does not read uploaded PDFs, verify source authenticity, determine admissibility, decide whether an exhibit proves a claim, retrieve or verify law, or issue a legal outcome. The lexical-overlap method may miss relevant evidence and produce false matches. All source links are candidates for a qualified human reviewer.

## Manual test

With the demo API enabled locally as described in the README, open `/peoples-court`, enter the demo token, go to **Synthetic record analysis: source traceability**, and use fictional excerpts such as:

- `Ex.P1 | Fictional agreement | Both parties signed the written agreement.`
- `Ex.D1 | Fictional reply | The respondent denies signing the agreement.`

Add a fictional issue and claims citing each reference. The report should show candidate links and should flag any deliberately misspelled citation such as `MISSING-EXHIBIT`.

Run all tests with:

```bash
python -m unittest discover -s tests -v
```

A passing unit test suite verifies the implemented code paths only; it does not establish legal accuracy or production readiness.
