import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

MODEL_PATH = "ml/model.pkl"
ENCODER_PATH = "ml/encoder.pkl"


def evaluate_model():
    print("\n=========== ML MODEL EVALUATION ===========")

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

    encoder = joblib.load(ENCODER_PATH)
    y = encoder.transform(df["RiskLabel"])  # ✅ FIX HERE

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    model = joblib.load(MODEL_PATH)

    y_pred = model.predict(X_test)

    print("Model Accuracy :", round(accuracy_score(y_test, y_pred) * 100, 2), "%")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred, target_names=encoder.classes_))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("============================================\n")