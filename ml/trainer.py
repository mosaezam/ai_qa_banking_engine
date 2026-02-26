import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "ml/model.pkl"
ENCODER_PATH = "ml/encoder.pkl"


def train_model():
    print("\n🔄 Training ML model...")

    df = pd.read_csv("datasets/historical_stories.csv")

    X = df[
        [
            "WordCount",
            "FinancialImpact(0/1)",
            "APIImpact(0/1)",
            "CalculationImpact(0/1)",
            "UIImpact(0/1)",
            "PerformanceImpact(0/1)",
        ]
    ]

    encoder = LabelEncoder()
    y = encoder.fit_transform(df["RiskLabel"])

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    joblib.dump(encoder, ENCODER_PATH)

    print("✅ Model trained and saved successfully.")