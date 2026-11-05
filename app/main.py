"""
Nyaya Assist (nyAI-neravu) — FastAPI backend
AI-assisted case resolution prototype for Karnataka courts.

This is decision-support software only. Every recommendation must be
reviewed by a human judge. Not a substitute for judicial decision-making.
"""

from __future__ import annotations

import os
import pickle
import secrets
from datetime import date
from pathlib import Path
from typing import List, Optional

import pandas as pd
from fastapi import FastAPI, File, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
import io

try:
    from app.rules import check_section_138
    from app.judgment_drafter import JudgmentRequest, build_draft
    from app import peoples_court as pc
    from app.case_analysis import AnalysisRequest, analyze_record
except ImportError:
    from rules import check_section_138
    from judgment_drafter import JudgmentRequest, build_draft
    import peoples_court as pc
    from case_analysis import AnalysisRequest, analyze_record

BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
MODEL_PATH = BASE_DIR / "model.pkl"
DATA_DIR = ROOT_DIR / "data"
FRONTEND_DIR = ROOT_DIR / "frontend"

app = FastAPI(
    title="Nyaya Assist (nyAI-neravu)",
    description=(
        "AI-assisted case resolution prototype for Karnataka. "
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

class PredictRequest(BaseModel):
    text: str = Field(..., min_length=10)
    k: int = Field(3, ge=1, le=10)

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

def ensure_demo_model() -> None:
    if MODEL_PATH.exists():
        return
    rows = []
    for _ in range(30):
        rows.append(("cheque dishonoured insufficient funds notice served section 138 payment not made", "cheque_bounce", "convicted"))
        rows.append(("cheque dishonoured but notice not served within thirty days section 138", "cheque_bounce", "acquitted"))
        rows.append(("motor accident claim compensation victim injured insurer liable negligence", "motor_accident", "allowed"))
        rows.append(("motor accident claim policy lapsed insurer not liable no valid licence", "motor_accident", "dismissed"))
    df = pd.DataFrame(rows, columns=["text", "case_type", "outcome"])
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import train_test_split
    df = df.dropna(subset=["text"]).reset_index(drop=True)
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200_000, sublinear_tf=True)
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

@app.get("/api/health", response_model=HealthResponse)
def health():
    loaded = MODEL_PATH.exists()
    return HealthResponse(status="ok", model_loaded=loaded, message="Nyaya Assist backend is running. AI outputs are decision-support only.")

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
        similar.append({"case_type": r.get("case_type", "?"), "outcome": r.get("outcome", "?"), "text": str(r["text"])[:200]})
    result.similar_cases = similar
    return result

@app.post("/api/judgment-draft")
def judgment_draft(req: JudgmentRequest):
    try:
        return build_draft(req)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not compose draft: {e}")

@app.post("/api/rules/section-138", response_model=Section138Response)
def section_138(req: Section138Request):
    out = check_section_138(req.cheque_date, req.presented, req.return_memo, req.notice_sent, req.notice_received, req.complaint_filed)
    return Section138Response(**out)

@app.post("/api/train-demo")
def train_demo():
    if MODEL_PATH.exists():
        MODEL_PATH.unlink()
    ensure_demo_model()
    return {"status": "ok", "message": "Demo model trained and saved."}

def _require_peoples_court_demo(x_demo_token: Optional[str]) -> None:
    if os.getenv("NYAYA_PEOPLES_COURT_DEMO_ENABLED", "").lower() != "true":
        raise HTTPException(status_code=404, detail="People's Court demo API is disabled.")
    expected = os.getenv("NYAYA_PEOPLES_COURT_DEMO_TOKEN", "")
    if len(expected) < 24:
        raise HTTPException(status_code=503, detail="Demo token is not safely configured.")
    if not x_demo_token or not secrets.compare_digest(x_demo_token, expected):
        raise HTTPException(status_code=401, detail="Valid X-Demo-Token header required.")

@app.get("/api/peoples-court")
def peoples_court_status():
    enabled = os.getenv("NYAYA_PEOPLES_COURT_DEMO_ENABLED", "").lower() == "true"
    return {"product": "AI–People's Court", "status": "enabled" if enabled else "disabled", "mode": "synthetic-only, non-binding research prototype", "durability": "in-memory only", "legal_effect": "No AI output is a court order.", "production_ready": False}

@app.post("/api/peoples-court/analyze-record")
def pc_analyze_record(req: AnalysisRequest, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return analyze_record(req)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@app.post("/api/peoples-court/cases")
def pc_create_case(req: pc.CaseCreate, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.create(req).model_dump(mode="json")
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

@app.get("/api/peoples-court/cases")
def pc_list_cases(x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    return {"cases": pc.store.list(), "count": len(pc.store.list())}

@app.get("/api/peoples-court/cases/{case_id}")
def pc_get_case(case_id: str, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.get(case_id).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")

@app.post("/api/peoples-court/cases/{case_id}/draft")
def pc_submit_draft(case_id: str, req: pc.DraftSubmission, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.submit_draft(case_id, req).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/reviews")
def pc_submit_review(case_id: str, req: pc.PanelReviewCreate, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.review(case_id, req).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/objections")
def pc_raise_objection(case_id: str, req: pc.ObjectionCreate, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.object(case_id, req).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case or objection not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/objections/{objection_id}/response")
def pc_respond_objection(case_id: str, objection_id: str, req: pc.ObjectionResponse, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.respond(case_id, objection_id, req, "demo_advisory_responder").model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case or objection not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/request-judicial-review")
def pc_request_judicial_review(case_id: str, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.request_judicial_review(case_id, "demo_case_operator").model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/return-for-correction")
def pc_return_for_correction(case_id: str, reason: str, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.return_for_correction(case_id, "demo_review_operator", reason).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.post("/api/peoples-court/cases/{case_id}/determination")
def pc_record_determination(case_id: str, req: pc.JudicialDetermination, x_demo_token: Optional[str] = Header(None)):
    _require_peoples_court_demo(x_demo_token)
    try:
        return pc.store.determine(case_id, req).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="Demo case not found.")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))

@app.get("/workbench.js")
def serve_workbench_js():
    """Serve the workbench navigation script."""
    js = FRONTEND_DIR / "workbench.js"
    if not js.exists():
        raise HTTPException(status_code=404, detail="workbench.js not found.")
    return FileResponse(js, media_type="application/javascript")

@app.get("/workbench", response_class=HTMLResponse)
def serve_workbench():
    page = FRONTEND_DIR / "nyai-neravu-workbench.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Nyai-Neravu workbench page not found.")
    return FileResponse(page)

@app.get("/peoples-court", response_class=HTMLResponse)
def serve_peoples_court():
    page = FRONTEND_DIR / "peoples-court.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="People's Court demo page not found.")
    return FileResponse(page)

@app.get("/judgment-drafting", response_class=HTMLResponse)
def serve_judgment_drafting():
    page = FRONTEND_DIR / "judgment-drafting.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Judgment drafting page not found")
    return FileResponse(page)

@app.get("/dashboard", response_class=HTMLResponse)
def serve_dashboard():
    """Legacy secretary / multi-role dashboard."""
    page = FRONTEND_DIR / "dashboard.html"
    if not page.exists():
        raise HTTPException(status_code=404, detail="Dashboard page not found.")
    return FileResponse(page)

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    index = FRONTEND_DIR / "index.html"
    if not index.exists():
        raise HTTPException(status_code=404, detail="Frontend not found")
    return FileResponse(index)

@app.on_event("startup")
def startup():
    ensure_demo_model()
