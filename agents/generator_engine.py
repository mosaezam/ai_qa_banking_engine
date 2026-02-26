def generate_test_cases(story, 
                        impact, 
                        config,
                        code_risk=None,
                        risk_score=None,
                        risk_level=None
                 ): 

    module = "FTT" if "ftt" in story["summary"].lower() else "BAKONG"
    channel = "MAE"

    test_cases = []
    tc_counter = 1

    def create_test_case(summary, steps, expected, priority="High"):
        nonlocal tc_counter
        tc_id = f"TC_{tc_counter:03}"
        tc_counter += 1

        return {
            "test_case_id": tc_id,
            "module": module,
            "channel": channel,
            "summary": summary,
            "priority": priority,
            "test_type": "Manual",
            "precondition": f"User logged into {channel} and navigated to {module} module",
            "steps": steps,
            "expected_result": expected
        }

    # -------------------------
    # BASE TESTS (Always Add)
    # -------------------------

    test_cases.append(create_test_case(
        summary="Verify successful transaction flow",
        steps="1. Initiate transfer\n2. Enter valid amount\n3. Submit transfer",
        expected="Transaction should complete successfully"
    ))

    # -------------------------
    # IMPACT BASED TESTS
    # -------------------------

    if "Financial Calculation Impact" in impact:
        test_cases.append(create_test_case(
            summary="Verify SST calculation accuracy",
            steps="1. Enter transfer amount\n2. Validate SST calculation",
            expected="SST must match configured percentage"
        ))

    if "API Contract Impact" in impact:
        test_cases.append(create_test_case(
            summary="Verify API request and response schema",
            steps="1. Trigger transfer\n2. Inspect API payload",
            expected="API must follow defined contract"
        ))

    if "Core Banking Impact" in impact:
        test_cases.append(create_test_case(
            summary="Verify ledger posting in core banking",
            steps="1. Complete transfer\n2. Verify ledger entry",
            expected="Ledger must reflect transaction"
        ))

    # -------------------------
    # CODE RISK BASED TESTS
    # -------------------------

    if code_risk:

        if code_risk.get("limit_checks", 0) > 0:
            test_cases.append(create_test_case(
                summary="Verify transfer limit boundary validation",
                steps="1. Enter amount equal to daily limit\n2. Submit transfer",
                expected="System must allow within limit"
            ))

        if code_risk.get("fee_logic", 0) > 0:
            test_cases.append(create_test_case(
                summary="Verify fee rounding precision",
                steps="1. Enter decimal amount\n2. Validate fee rounding",
                expected="Fee rounding must follow business rules"
            ))

        if code_risk.get("error_handling", 0) > 2:
            test_cases.append(create_test_case(
                summary="Verify transaction failure handling",
                steps="1. Simulate backend failure\n2. Submit transfer",
                expected="Proper error must be shown"
            ))

    # -------------------------
    # 🔥 RISK-BASED SCALING
    # -------------------------

    if risk_level in ["HIGH", "CRITICAL"]:

        test_cases.append(create_test_case(
            summary="Verify negative amount validation",
            steps="1. Enter negative transfer amount\n2. Submit",
            expected="System must reject negative values",
            priority="Critical"
        ))

        test_cases.append(create_test_case(
            summary="Verify zero amount validation",
            steps="1. Enter zero transfer amount\n2. Submit",
            expected="System must not allow zero transfer",
            priority="Critical"
        ))

    if risk_level == "CRITICAL":

        test_cases.append(create_test_case(
            summary="Verify timeout handling for external API",
            steps="1. Simulate API timeout\n2. Submit transfer",
            expected="System must retry or show timeout message",
            priority="Critical"
        ))

        test_cases.append(create_test_case(
            summary="Verify concurrent transaction handling",
            steps="1. Trigger multiple simultaneous transfers",
            expected="System must maintain consistency",
            priority="Critical"
        ))

    return test_cases