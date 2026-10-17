"""Baseline legal-case AI: learns from past decided cases.

Usage:
  python legal_ai.py demo                       # tiny synthetic smoke test
  python legal_ai.py train cases.csv            # train on your data
  python legal_ai.py predict "case text here"   # classify, predict outcome, find similar cases

cases.csv columns: text, case_type, outcome   (outcome e.g. allowed / dismissed / convicted / acquitted)
Get real data from the open datasets (eCourts/AWS Open Data, NyayaAnumana, PredEx, Indian Kanoon)
and convert to this format. This is a research baseline: every output needs human judge review.
"""
import sys, pickle
from pathlib import Path
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity

# Model lives next to this file so both CLI and FastAPI can find it
MODEL = str(Path(__file__).resolve().parent / "model.pkl")


def train(df):
    df = df.dropna(subset=["text"]).reset_index(drop=True)
    vec = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=200_000, sublinear_tf=True)
    X = vec.fit_transform(df["text"])
    models = {}
    for target in ("case_type", "outcome"):
        if target not in df or df[target].nunique() < 2:
            continue
        # temporal split is better for real data; random split keeps this baseline simple
        Xtr, Xte, ytr, yte = train_test_split(X, df[target], test_size=0.2, random_state=0)
        clf = LogisticRegression(max_iter=1000, class_weight="balanced").fit(Xtr, ytr)
        print(f"\n== {target} ==\n", classification_report(yte, clf.predict(Xte), zero_division=0))
        models[target] = clf
    pickle.dump({"vec": vec, "models": models, "X": X, "df": df}, open(MODEL, "wb"))
    print(f"Saved {MODEL}")


def predict(text, k=3):
    m = pickle.load(open(MODEL, "rb"))
    x = m["vec"].transform([text])
    for target, clf in m["models"].items():
        probs = clf.predict_proba(x)[0]
        best = probs.argmax()
        print(f"{target}: {clf.classes_[best]} (confidence {probs[best]:.0%})")
    sims = cosine_similarity(x, m["X"])[0].argsort()[::-1][:k]
    print("\nMost similar past cases:")
    for i in sims:
        r = m["df"].iloc[i]
        print(f"- [{r.get('case_type','?')} / {r.get('outcome','?')}] {r['text'][:120]}...")


def demo():
    rows = []
    for i in range(30):
        rows.append(("cheque dishonoured insufficient funds notice served section 138 payment not made", "cheque_bounce", "convicted"))
        rows.append(("cheque dishonoured but notice not served within thirty days section 138", "cheque_bounce", "acquitted"))
        rows.append(("motor accident claim compensation victim injured insurer liable negligence", "motor_accident", "allowed"))
        rows.append(("motor accident claim policy lapsed insurer not liable no valid licence", "motor_accident", "dismissed"))
    train(pd.DataFrame(rows, columns=["text", "case_type", "outcome"]))
    predict("complaint under section 138 cheque returned insufficient funds legal notice was served")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "demo"
    if cmd == "train":
        train(pd.read_csv(sys.argv[2]))
    elif cmd == "predict":
        predict(sys.argv[2])
    else:
        demo()
