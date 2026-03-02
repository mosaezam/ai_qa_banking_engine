def review_coverage(impact, test_cases, risk_level=None):

    coverage_score = 100
    missing_areas = []
    explanation = []
    recommendations = []

    impact_weights = {
        "Core Banking Impact": {
            "keywords": [
                "debit", "ledger", "reconcil", "posting",
                "data integrity", "rollback", "commit", "transaction",
                "idempotent",
            ],
            "weight": 25,
        },
        "API Contract Impact": {
            "keywords": [
                "api", "payload", "response", "schema",
                "endpoint", "contract", "request",
            ],
            "weight": 20,
        },
        "Financial Calculation Impact": {
            "keywords": [
                "calculation", "total", "fee", "rounding", "amount",
                "payment", "price", "billing", "charge",
            ],
            "weight": 20,
        },
        "Feature Flag Impact": {
            "keywords": [
                "feature flag", "toggle", "config", "flag",
                "enabled", "disabled", "rollout",
            ],
            "weight": 15,
        },
        "High Complexity Story": {
            "keywords": [
                "boundary", "limit", "validation", "edge case",
                "negative", "invalid",
            ],
            "weight": 20,
        },
    }

    # Check each impacted area
    for area, cfg in impact_weights.items():
        if area in impact:
            keywords = cfg["keywords"]
            weight = cfg["weight"]

            matched_tcs = [
                tc for tc in test_cases
                if any(
                    keyword in (
                        tc.get("summary", "").lower() + " " +
                        tc.get("steps", "").lower() + " " +
                        tc.get("expected_result", "").lower()
                    )
                    for keyword in keywords
                )
            ]

            if not matched_tcs:
                coverage_score -= weight
                missing_areas.append(area)
                explanation.append(
                    f"MISSING: {area} has no test coverage. "
                    f"Expected keywords: {keywords}"
                )
                recommendations.append(
                    f"Add test cases covering {area} — focus on: {', '.join(keywords)}"
                )
            elif len(matched_tcs) == 1 and risk_level in ["HIGH", "CRITICAL"]:
                coverage_score -= round(weight / 2)
                explanation.append(
                    f"WEAK: {area} has only 1 test case. "
                    f"Risk level is {risk_level} — more coverage needed."
                )
                recommendations.append(
                    f"Expand {area} test cases — add negative, boundary, and error scenario tests."
                )

    # Check for missing negative tests
    has_negative = any(
        any(word in tc.get("summary", "").lower()
            for word in ["negative", "invalid", "zero", "reject", "fail", "error", "exceed", "above"])
        for tc in test_cases
    )
    if not has_negative:
        coverage_score -= 10
        explanation.append("MISSING: No negative test cases found.")
        recommendations.append(
            "Add negative test cases — invalid inputs, zero values, boundary violations."
        )

    # Check for missing critical priority when risk is high
    if risk_level in ["HIGH", "CRITICAL"]:
        has_critical = any(tc.get("priority") == "Critical" for tc in test_cases)
        if not has_critical:
            coverage_score -= 10
            explanation.append(
                f"WARNING: Risk level is {risk_level} but no Critical priority test cases exist."
            )
            recommendations.append("Escalate at least 2 test cases to Critical priority.")

    return {
        "coverage_score": max(coverage_score, 0),
        "missing_areas": missing_areas,
        "explanation": explanation,
        "recommendations": recommendations,
        "total_test_cases": len(test_cases),
        "review_status": "PASS" if coverage_score >= 80 else "FAIL",
    }
