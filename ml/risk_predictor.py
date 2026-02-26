import pandas as pd
import numpy as np
import joblib
import os

MODEL_PATH = "ml/model.pkl"
ENCODER_PATH = "ml/encoder.pkl"

# -------------------------
# Safe Model Loading
# -------------------------
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

if not os.path.exists(ENCODER_PATH):
    raise FileNotFoundError(f"Encoder file not found at {ENCODER_PATH}")

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


def calculate_risk_score(impact, story, code_risk=None):
    """
    Hybrid Risk Engine:
    - ML Base Prediction
    - Controlled Technical Boost
    - Final Risk Band Recalculation

    Returns:
        (risk_score, final_label, confidence)
    """

    # -------------------------
    # 1️⃣ ML BASE FEATURES
    # -------------------------
    features = {
        "WordCount": story.get("word_count", 0),
        "FinancialImpact(0/1)": int("Financial Calculation Impact" in impact),
        "APIImpact(0/1)": int("API Contract Impact" in impact),
        "CalculationImpact(0/1)": int("Core Banking Impact" in impact),
        "UIImpact(0/1)": int("Feature Flag Impact" in impact),
        "PerformanceImpact(0/1)": int("High Complexity Story" in impact),
    }

    X_new = pd.DataFrame([features])

    prediction = model.predict(X_new)
    probabilities = model.predict_proba(X_new)

    risk_label = encoder.inverse_transform(prediction)[0]
    confidence = round(float(np.max(probabilities)) * 100, 2)

    # Debugging output
    print("ML Predicted Label:", risk_label)
    print("ML Confidence:", confidence)
    print("Impact:", impact)
    print("Story Word Count:", story.get("word_count"))

    # -------------------------
    # 2️⃣ BASE SCORE MAPPING (Controlled)
    # -------------------------
    base_score_map = {
        "LOW": 20,
        "MEDIUM": 45,
        "HIGH": 70,
        "CRITICAL": 85,
    }

    base_score = base_score_map.get(risk_label, 45)

    # -------------------------
    # 3️⃣ TECHNICAL CODE BOOST
    # -------------------------
    technical_boost = 0

    if code_risk:
        technical_boost = (
            code_risk.get("validations", 0) * 1 +
            code_risk.get("fee_logic", 0) * 3 +
            code_risk.get("limit_checks", 0) * 2 +
            code_risk.get("error_handling", 0) * 2
        )

    # Cap technical boost to avoid everything becoming CRITICAL
    technical_boost = min(technical_boost, 15)

    # -------------------------
    # 4️⃣ FINAL SCORE
    # -------------------------
    risk_score = base_score + technical_boost
    risk_score = min(risk_score, 100)

    # -------------------------
    # 5️⃣ FINAL RISK BAND
    # -------------------------
    if risk_score >= 85:
        final_label = "CRITICAL"
    elif risk_score >= 65:
        final_label = "HIGH"
    elif risk_score >= 40:
        final_label = "MEDIUM"
    else:
        final_label = "LOW"

    return risk_score, final_label, confidence