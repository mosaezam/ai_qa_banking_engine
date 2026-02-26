def analyze_impact(story):

    description = story["description"]

    impact = []

    # Financial detection
    if any(keyword in description for keyword in ["sst", "fee", "total amount", "principal", "8%"]):
        impact.append("Financial Calculation Impact")

    # API detection
    if any(keyword in description for keyword in ["api", "inquiry", "response", "request"]):
        impact.append("API Contract Impact")

    # Feature flag detection
    if any(keyword in description for keyword in ["rmbp", "dcc", "feature flag"]):
        impact.append("Feature Flag Impact")

    # Middleware detection
    if "esb" in description:
        impact.append("Middleware ESB Impact")

    # Host detection
    if "cics" in description:
        impact.append("Host Processing Impact")

    # Core banking detection
    if any(keyword in description for keyword in ["debit", "credit", "core"]):
        impact.append("Core Banking Impact")

    # Complexity detection
    if story["word_count"] > 700:
        impact.append("High Complexity Story")

    return impact