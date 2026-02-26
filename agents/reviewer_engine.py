def review_coverage(impact, test_cases):

    coverage_score = 100
    missing_areas = []
    explanation = []

    impact_keywords = {
        "Core Banking Impact": ["debit", "ledger", "reconciliation"],
        "API Contract Impact": ["api", "payload", "response"],
        "Financial Calculation Impact": ["sst", "calculation", "total"],
        "Feature Flag Impact": ["rmbp", "dcc"],
    }

    for area, keywords in impact_keywords.items():
        if area in impact:
            found = any(
                any(keyword in tc.lower() for keyword in keywords)
                for tc in test_cases
            )
            if not found:
                coverage_score -= 20
                missing_areas.append(area)
                explanation.append(
                    f"{area} detected but no test case contains keywords: {keywords}"
                )

    return {
        "coverage_score": max(coverage_score, 0),
        "missing_areas": missing_areas,
        "explanation": explanation
    }