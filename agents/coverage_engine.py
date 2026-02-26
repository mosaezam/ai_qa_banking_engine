def build_coverage_matrix(story, impact):

    coverage = {}

    # Always validate frontend flow
    coverage["Frontend"] = [
        "Functional flow validation",
        "Negative input validation",
        "Boundary amount validation"
    ]

    # Feature Flags
    if "Feature Flag Impact" in impact:
        coverage["Feature Flag"] = [
            "RMBP ON behaviour validation",
            "RMBP OFF behaviour validation",
            "DCC ON behaviour validation",
            "DCC OFF behaviour validation"
        ]

    # API Layer
    if "API Contract Impact" in impact:
        coverage["API"] = [
            "Request payload validation",
            "Response mapping validation",
            "Backward compatibility validation"
        ]

    # Middleware (ESB)
    if "Middleware ESB Impact" in impact:
        coverage["Middleware"] = [
            "ESB routing validation",
            "Timeout handling validation",
            "Retry mechanism validation"
        ]

    # Core Banking
    if "Core Banking Impact" in impact:
        coverage["Core Banking"] = [
            "Debit amount validation",
            "Credit amount validation",
            "Ledger consistency validation",
            "Rollback on failure validation"
        ]

    # Financial Logic
    if "Financial Calculation Impact" in impact:
        coverage["Financial Logic"] = [
            "8% SST calculation validation",
            "Total amount recalculation validation",
            "Service fee calculation validation"
        ]

    # Regression Scope (Always included)
    coverage["Regression Scope"] = [
        "MAE Overseas Transfer Flow",
        "S2U validation flow",
        "Receipt generation validation",
        "Transaction history validation",
        "Statement validation"
    ]

    return coverage