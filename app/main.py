"""
Nyaya Assist (nyAI-neravu) — FastAPI backend
AI-assisted case resolution prototype for Karnataka courts.

This is decision-support software only. Every recommendation must be
reviewed by a human judge. Not a substitute for judicial decision-making.
"""

from __future__ import annotations

import os
import pickle
from datetime import date
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import io

# Support both package import (uvicorn app.main:app) and direct run from app/
try:
    from app.rules import check_section_138
except ImportError:
    from rules import check_section_138

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
MODEL_PATH = BASE_DIR / "model.pkl"
DATA_DIR = ROOT_DIR / "data"
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="Nyaya Assist (nyAI-neravu)",
    description=(
        "AI-assisted case resolution prototype for Karnataka. "
        "Learns patterns from past decided cases and applies statutory rules. "
        "Decision-support only — every output requires human judicial review."
    ),
    version="0.1.0",
    contact={"name": "Nyaya Assist Team"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Case facts / complaint text")
    k: int = Field(3, ge=1, le=10, description="Number of similar past cases to return")


class PredictResponse(BaseModel):
    case_type: Optional[str] = None
    case_type_confidence: Optional[float] = None
    outcome: Optional[str] = None
    outcome_confidence: Optional[float] = None
    similar_cases: List[dict] = []


class Section138Request(BaseModel):
    cheque_date: date
    presented: date
    return_memo: date
    notice_sent: date
    notice_received: date
    complaint_filed: date


class Section138Response(BaseModel):
    statutory_ok: bool
    issues: List[str]


class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    message: str


# ---------------------------------------------------------------------------
# Model helpers
# ---------------------------------------------------------------------------
def ensure_demo_model() -> None:
    """Train a tiny synthetic model if none exists (for first-run demo)."""
    if MODEL_PATH.exists():
        return
    rows = []
    for _ in range(30):
        rows.append(
            (
                "cheque dishonoured insufficient funds notice served section 138 payment not made",
                "cheque_bounce",
                "convicted",
            )
        )
        rows.append(
            (
                "cheque dishonoured but notice not served within thirty days section 138",
                "cheque_bounce",
                "acquitted",
            )
        )
        rows.append(
            (
                "motor accident claim compensation victim injured insurer liable negligence",
                "motor_accident",
                "allowed",
            )
        )
        rows.append(
            (
                "motor accident claim policy lapsed insurer not liable no valid licence",
                "motor_accident",
                "dismissed",
            )
        )
    df = pd.DataFrame(rows, columns=["text", "case_type", "outcome"])
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split

    df = df.dropna(subset=["text"]).reset_index(drop=True)
    vec = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_features=200_000, sublinear_tf=True
    )
    X = vec.fit_transform(df["text"])
    models = {}
    for target in ("case_type", "outcome"):
        if target not in df or df[target].nunique() < 2:
            continue
        Xtr, Xte, ytr, yte = train_test_split(X, df[target], test_size=0.2, random_state=0)
        clf = LogisticRegression(max_iter=1000, class_weight="balanced").fit(Xtr, ytr)
        models[target] = clf
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"vec": vec, "models": models, "X": X, "df": df}, f)


def load_model():
    if not MODEL_PATH.exists():
        ensure_demo_model()
    with open(MODEL_PATH, "rb") as f:
        return pickle.load(f)


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
@app.get("/api/health", response_model=HealthResponse)
def health():
    loaded = MODEL_PATH.exists()
    return HealthResponse(
        status="ok",
        model_loaded=loaded,
        message="Nyaya Assist backend is running. AI outputs are decision-support only.",
    )


@app.post("/api/predict", response_model=PredictResponse)
def predict(req: PredictRequest):
    try:
        m = load_model()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model load failed: {e}")

    x = m["vec"].transform([req.text])
    result = PredictResponse()

    for target, clf in m["models"].items():
        probs = clf.predict_proba(x)[0]
        best = int(probs.argmax())
        label = str(clf.classes_[best])
        conf = float(probs[best])
        if target == "case_type":
            result.case_type = label
            result.case_type_confidence = round(conf, 4)
        elif target == "outcome":
            result.outcome = label
            result.outcome_confidence = round(conf, 4)

    from sklearn.metrics.pairwise import cosine_similarity

    sims = cosine_similarity(x, m["X"])[0].argsort()[::-1][: req.k]
    similar = []
    for i in sims:
        r = m["df"].iloc[int(i)]
        similar.append(
            {
                "case_type": r.get("case_type", "?"),
                "outcome": r.get("outcome", "?"),
                "text": str(r["text"])[:200],
            }
        )
    result.similar_cases = similar
    return result


@app.post("/api/rules/section-138", response_model=Section138Response)
def section_138(req: Section138Request):
    out = check_section_138(
        req.cheque_date,
        req.presented,
        req.return_memo,
        req.notice_sent,
        req.notice_received,
        req.complaint_filed,
    )
    return Section138Response(**out)


@app.post("/api/train-demo")
def train_demo():
    """Force re-train the synthetic demo model (useful for demos)."""
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    ensure_demo_model()
    return {"status": "ok", "message": "Demo model trained and saved."}


@app.post("/api/train")
async def train_from_csv(file: UploadFile = File(...)):
    """
    Upload a CSV with columns: text, case_type, outcome
    and retrain the live model. Research / decision-support only.
    """
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a .csv file")

    raw = await file.read()
    if len(raw) > 80 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="CSV too large (max 80 MB)")

    try:
        df = pd.read_csv(io.BytesIO(raw))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not parse CSV: {e}")

    colmap = {c: c.lower().strip() for c in df.columns}
    df = df.rename(columns=colmap)
    if "text" not in df.columns or "outcome" not in df.columns:
        raise HTTPException(
            status_code=400,
            detail="CSV must have columns: text, outcome (optional: case_type)",
        )
    if "case_type" not in df.columns:
        df["case_type"] = "general"

    df = df.dropna(subset=["text", "outcome"]).reset_index(drop=True)
    df["text"] = df["text"].astype(str).str.slice(0, 5000)
    df["outcome"] = df["outcome"].astype(str).str.strip().str.lower()
    df["case_type"] = df["case_type"].astype(str).str.strip().str.lower()

    if len(df) < 20:
        raise HTTPException(status_code=400, detail="Need at least 20 labeled rows")
    if df["outcome"].nunique() < 2:
        raise HTTPException(status_code=400, detail="Need at least 2 distinct outcomes")

    # Cap for free-tier memory safety
    if len(df) > 25000:
        df = df.sample(n=25000, random_state=0).reset_index(drop=True)

    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report

    vec = TfidfVectorizer(
        ngram_range=(1, 2), min_df=2, max_features=80_000, sublinear_tf=True
    )
    X = vec.fit_transform(df["text"])
    models = {}
    reports = {}
    for target in ("case_type", "outcome"):
        if df[target].nunique() < 2:
            continue
        Xtr, Xte, ytr, yte = train_test_split(
            X, df[target], test_size=0.15, random_state=0
        )
        clf = LogisticRegression(max_iter=1000, class_weight="balanced").fit(Xtr, ytr)
        models[target] = clf
        reports[target] = classification_report(
            yte, clf.predict(Xte), zero_division=0, output_dict=False
        )

    if not models:
        raise HTTPException(status_code=400, detail="Could not train any target column")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump({"vec": vec, "models": models, "X": X, "df": df}, f)

    return {
        "status": "ok",
        "rows": len(df),
        "targets": list(models.keys()),
        "outcome_counts": df["outcome"].value_counts().to_dict(),
        "case_type_counts": df["case_type"].value_counts().head(12).to_dict(),
        "message": "Model retrained from uploaded CSV. Decision-support only.",
        "reports": reports,
    }


# ---------------------------------------------------------------------------
# Serve frontend
# ---------------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        return HTMLResponse(
            "<h1>Nyaya Assist</h1><p>Frontend not found. Place index.html in frontend/</p>",
            status_code=404,
        )
    return FileResponse(index)


# Mount static assets if any are added later
if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")


# ---------------------------------------------------------------------------
# Startup
# ---------------------------------------------------------------------------
@app.on_event("startup")
def startup():
    ensure_demo_model()
