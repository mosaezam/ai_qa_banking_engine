import pandas as pd
import numpy as np
import joblib

MODEL_PATH = "ml/model.pkl"
ENCODER_PATH = "ml/encoder.pkl"

model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)


def calculate_risk_score(impact, story):

    features = {
        "WordCount": story["word_count"],
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
    confidence = round(np.max(probabilities) * 100, 2)

    score_map = {
        "LOW": 25,
        "MEDIUM": 50,
        "HIGH": 75,
        "CRITICAL": 100,
    }

    return score_map.get(risk_label, 50), risk_label, confidence