#!/usr/bin/env python3
"""
Build data/cases.csv from open Indian judgment-prediction datasets.

Primary source: PredEx (L-NLProc) — expert-annotated accept/reject labels.
https://huggingface.co/datasets/L-NLProc/PredEx
https://github.com/ShubhamKumarNigam/PredEx

Usage:
  python scripts/build_cases_csv.py
  python scripts/build_cases_csv.py --max-rows 5000 --out data/cases.csv

Then train:
  python app/legal_ai.py train data/cases.csv

This is research data only. Cite PredEx / NyayaAnumana. Not a substitute for
judicial review. For Karnataka pilots, obtain formal data-sharing clearance.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUT = ROOT / "data" / "cases.csv"

# Direct CSV URLs (avoids HF datasets cast issues on mixed schemas)
PREDEX_URLS = [
    "https://huggingface.co/datasets/L-NLProc/PredEx/resolve/main/train.csv",
    "https://huggingface.co/datasets/L-NLProc/PredEx/resolve/main/test.csv",
]

# Heuristic case_type from free text (for UI filters / multi-task training)
TYPE_PATTERNS = [
    (r"\b(?:section\s*138|s\.?\s*138|cheque\s*bounce|dishonour(?:ed)?\s+of\s+cheque|negotiable\s+instruments?\s+act)\b", "cheque_bounce"),
    (r"\b(?:motor\s+accident|motor\s+vehicles?\s+act|m\.?v\.?\s*act|mac\s*t|compensation\s+for\s+(?:death|injury)|third\s+party\s+insurance)\b", "motor_accident"),
    (r"\b(?:consumer\s+protection|deficiency\s+in\s+service|unfair\s+trade\s+practice|district\s+consumer|national\s+consumer)\b", "consumer"),
    (r"\b(?:rent\s+control|eviction|tenant|landlord|lease\s+deed|premises)\b", "rent_tenancy"),
    (r"\b(?:pension|promotion|service\s+matter|disciplinary|government\s+servant|central\s+administrative|cat\b)\b", "govt_service"),
]


def infer_case_type(text: str) -> str:
    t = text.lower()
    for pattern, label in TYPE_PATTERNS:
        if re.search(pattern, t, re.I):
            return label
    return "general"


def label_to_outcome(label) -> str | None:
    try:
        v = int(label)
    except (TypeError, ValueError):
        s = str(label).strip().lower()
        if s in ("1", "allowed", "accepted", "grant", "granted", "yes", "true"):
            return "allowed"
        if s in ("0", "dismissed", "rejected", "deny", "denied", "no", "false"):
            return "dismissed"
        return None
    return "allowed" if v == 1 else "dismissed"


def load_predex(max_rows: int | None) -> pd.DataFrame:
    frames = []
    for url in PREDEX_URLS:
        print(f"Downloading {url} ...")
        try:
            df = pd.read_csv(url, low_memory=False)
        except Exception as e:
            print(f"  WARN: failed ({e})", file=sys.stderr)
            continue
        print(f"  columns={list(df.columns)} rows={len(df)}")
        frames.append(df)
    if not frames:
        raise SystemExit(
            "Could not download PredEx CSVs. Check network or download manually from "
            "https://huggingface.co/datasets/L-NLProc/PredEx"
        )
    raw = pd.concat(frames, ignore_index=True)

    # Prefer plain case text over instruction-wrapped "text"
    text_col = None
    for c in ("Input", "input", "case_text", "text", "Text"):
        if c in raw.columns:
            text_col = c
            break
    if text_col is None:
        raise SystemExit(f"No text column found. Columns: {list(raw.columns)}")

    label_col = None
    for c in ("Label", "label", "decision", "Decision"):
        if c in raw.columns:
            label_col = c
            break
    if label_col is None:
        raise SystemExit(f"No label column found. Columns: {list(raw.columns)}")

    rows = []
    for _, r in raw.iterrows():
        text = r.get(text_col)
        if not isinstance(text, str) or len(text.strip()) < 40:
            continue
        # Strip common instruction prefixes if present
        cleaned = re.sub(
            r"^###\s*Instruction:.*?###\s*Input:\s*",
            "",
            text,
            flags=re.I | re.S,
        ).strip()
        if len(cleaned) < 40:
            cleaned = text.strip()
        outcome = label_to_outcome(r.get(label_col))
        if outcome is None:
            continue
        rows.append(
            {
                "text": cleaned[:5000],
                "case_type": infer_case_type(cleaned),
                "outcome": outcome,
            }
        )
        if max_rows and len(rows) >= max_rows:
            break

    out = pd.DataFrame(rows)
    if out.empty:
        raise SystemExit("No usable rows after filtering.")
    return out


def main():
    ap = argparse.ArgumentParser(description="Build cases.csv from PredEx")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--max-rows", type=int, default=8000, help="Cap rows (0 = all)")
    args = ap.parse_args()
    max_rows = None if args.max_rows == 0 else args.max_rows

    df = load_predex(max_rows)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"\nWrote {len(df)} rows → {args.out}")
    print(df["outcome"].value_counts().to_string())
    print("\ncase_type distribution:")
    print(df["case_type"].value_counts().to_string())
    print(
        "\nNext:\n"
        f"  python app/legal_ai.py train {args.out}\n"
        "  # or POST the CSV to /api/train on the running server"
    )


if __name__ == "__main__":
    main()
