def review_coverage(impact, test_cases):

    coverage_score = 100
    missing_areas = []
    explanation = []

    impact_keywords = {
        "Core Banking Impact": ["debit", "ledger", "reconciliation", "posting"],
        "API Contract Impact": ["api", "payload", "response", "schema"],
        "Financial Calculation Impact": ["sst", "calculation", "total", "fee"],
        "Feature Flag Impact": ["rmbp", "dcc", "feature flag"],
        "High Complexity Story": ["boundary", "limit", "validation"],
    }

    for area, keywords in impact_keywords.items():

        if area in impact:

            found = any(
                any(
                    keyword in (
                        tc.get("summary", "").lower()
                        + " "
                        + tc.get("steps", "").lower()
                        + " "
                        + tc.get("expected_result", "").lower()
                    )
                    for keyword in keywords
                )
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