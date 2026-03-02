def analyze_impact(story):

    description = story["description"].lower()
    summary = story["summary"].lower()
    text = description + " " + summary

    impact = []

    # Financial Calculation
    if any(k in text for k in ["sst", "fee", "total amount", "principal",
                                "8%", "charge", "rate", "calculation",
                                "rounding", "service fee", "agent fee"]):
        impact.append("Financial Calculation Impact")

    # API Contract
    if any(k in text for k in ["api", "inquiry", "response", "request",
                                "payload", "schema", "contract", "endpoint",
                                "integration", "microservice"]):
        impact.append("API Contract Impact")

    # Feature Flag / DCC
    if any(k in text for k in ["rmbp", "dcc", "feature flag", "toggle",
                                "enable", "disable", "phase", "rollout",
                                "flag", "config"]):
        impact.append("Feature Flag Impact")

    # Middleware / Gateway / SWIFT
    if any(k in text for k in ["esb", "gateway", "swift", "nbc", "wu",
                                "middleware", "routing", "timeout", "retry",
                                "network", "visa network", "mt103"]):
        impact.append("Middleware ESB Impact")

    # Core Banking / Ledger
    if any(k in text for k in ["debit", "credit", "core", "ledger",
                                "posting", "balance", "account", "cics",
                                "core banking", "atomic"]):
        impact.append("Core Banking Impact")

    # AML / Compliance
    if any(k in text for k in ["ofac", "aml", "fatf", "kyc", "compliance",
                                "sanctions", "screening", "purpose code",
                                "source of funds", "declaration", "bnm",
                                "regulatory", "pci"]):
        impact.append("AML Compliance Impact")

    # Security / Authentication
    if any(k in text for k in ["s2u", "secure2u", "authentication", "auth",
                                "pci", "encryption", "mask", "luhn",
                                "2fa", "otp", "pin", "password"]):
        impact.append("Security Impact")

    # Validation / Input
    if any(k in text for k in ["validate", "validation", "invalid",
                                "format", "mandatory", "required", "reject",
                                "iban", "swift code", "bic", "bin lookup",
                                "card number", "account number"]):
        impact.append("Validation Impact")

    # Limit / Boundary
    if any(k in text for k in ["limit", "threshold", "maximum", "minimum",
                                "daily", "exceed", "boundary", "cap",
                                "tier", "segment", "premier", "standard"]):
        impact.append("Limit Boundary Impact")

    # Audit Trail
    if any(k in text for k in ["audit", "trail", "log", "history",
                                "statement", "reference", "record",
                                "report", "receipt", "transaction history"]):
        impact.append("Audit Trail Impact")

    # UI / Frontend
    if any(k in text for k in ["screen", "display", "tooltip", "label",
                                "ui", "frontend", "page", "field",
                                "confirmation", "receipt page", "banner"]):
        impact.append("UI Frontend Impact")

    # Complexity
    if story["word_count"] > 700:
        impact.append("High Complexity Story")

    return impact