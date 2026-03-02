from agents.module_detector import (
    detect_module_and_channel,
    get_module_description,
    get_module_compliance,
    get_module_limits,
)


def generate_test_cases(story, impact, _config, code_risk=None, _risk_score=None, _risk_level=None):

    # ─────────────────────────────────────────────
    # MODULE / DOMAIN DETECTION
    # ─────────────────────────────────────────────
    module_name, channel = detect_module_and_channel(story)
    module = module_name.upper()
    module_desc = get_module_description(module_name)
    compliance_list = get_module_compliance(module_name)
    limits = get_module_limits(module_name)
    tx_limit = limits.get("transaction", 10000)
    daily_limit = limits.get("daily", 50000)

    test_cases = []
    tc_counter = 1

    def tc(summary, steps, expected, priority="High", test_type="Functional"):
        nonlocal tc_counter
        tc_id = f"TC_{tc_counter:03}"
        tc_counter += 1
        return {
            "test_case_id": tc_id,
            "module": module,
            "channel": channel,
            "summary": summary,
            "priority": priority,
            "test_type": test_type,
            "precondition": (
                f"User is authenticated in {channel} with valid credentials "
                f"and required permissions for {module_desc}"
            ),
            "steps": steps,
            "expected_result": expected,
        }

    # ═══════════════════════════════════════════════════════════════
    # SECTION 1 — CORE USER STORY FLOW (Always Generated)
    # ═══════════════════════════════════════════════════════════════

    test_cases.append(tc(
        summary=f"[STORY] Verify end-to-end happy path — {module_desc}",
        steps=(
            f"1. Authenticate in {channel}\n"
            f"2. Navigate to the {module_desc} feature\n"
            "3. Enter all required inputs with valid data\n"
            "4. Review confirmation/preview screen\n"
            "5. Submit and complete the action"
        ),
        expected=(
            "Action completes successfully. "
            "Confirmation/reference number is generated. "
            "Success screen shows all relevant details."
        ),
        priority="Critical",
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module_desc} with saved/recent data",
        steps=(
            f"1. Authenticate in {channel}\n"
            f"2. Navigate to {module_desc}\n"
            "3. Select from previously saved / recent entries\n"
            "4. Review pre-filled details\n"
            "5. Confirm and submit"
        ),
        expected=(
            "Saved data loads correctly with all fields pre-populated. "
            "Submission succeeds with expected outcome."
        ),
        priority="High",
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify confirmation screen shows all required information",
        steps=(
            "1. Enter valid input for all fields\n"
            "2. Proceed to confirmation/preview step\n"
            "3. Verify every field and label is present and correct"
        ),
        expected=(
            "Confirmation screen displays: all input data, summary totals, "
            "reference details, and action description. No data is missing or truncated."
        ),
        priority="Critical",
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify success/receipt screen after completing {module_desc}",
        steps=(
            "1. Complete the full flow successfully\n"
            "2. Review the success / receipt screen\n"
            "3. Verify all details match the submitted data"
        ),
        expected=(
            "Receipt/success screen shows: reference number, timestamp, "
            "summary of action, status as SUCCESS. All values match what was submitted."
        ),
        priority="High",
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module_desc} activity visible in history/audit log",
        steps=(
            "1. Complete the action successfully\n"
            "2. Navigate to history / activity log\n"
            "3. Locate and verify the entry"
        ),
        expected=(
            "History shows the entry with correct: amount/value, date/time, "
            "reference number, status, and relevant details."
        ),
        priority="High",
    ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 2 — FINANCIAL / PAYMENT CALCULATION IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Financial Calculation Impact" in impact or (code_risk and code_risk.get("fee_logic", 0) > 0):

        test_cases.append(tc(
            summary="[FIN] Verify fee/charge calculation is mathematically correct",
            steps=(
                "1. Enter an amount with applicable fees/charges\n"
                "2. Proceed to confirmation screen\n"
                "3. Manually calculate expected total\n"
                "4. Compare with displayed total"
            ),
            expected=(
                "Displayed fee/charge equals the expected calculated amount. "
                "Rounded to 2 decimal places with no floating-point errors."
            ),
            priority="Critical", test_type="Financial",
        ))

        test_cases.append(tc(
            summary="[FIN] Verify total amount = sum of all individual components",
            steps=(
                "1. Enter amount with multiple fee components\n"
                "2. On confirmation screen, manually verify: principal + all charges = total\n"
                "3. Compare with displayed grand total"
            ),
            expected=(
                "Total Amount = Principal + all applicable fees and taxes. "
                "All line items individually visible. Sum matches grand total."
            ),
            priority="Critical", test_type="Financial",
        ))

        test_cases.append(tc(
            summary="[FIN] Verify zero-charge scenario behaves correctly",
            steps=(
                "1. Initiate action where no fees are applicable\n"
                "2. Check confirmation screen"
            ),
            expected=(
                "Fee lines show 0.00 or are hidden. "
                "Total = principal only. No incorrect charge applied."
            ),
            priority="High", test_type="Financial",
        ))

        test_cases.append(tc(
            summary="[FIN] Verify rounding with decimal input amounts",
            steps=(
                "1. Enter an amount with multiple decimal places (e.g. 1234.567)\n"
                "2. Check calculated fee and total on confirmation"
            ),
            expected=(
                "All monetary values rounded correctly to 2 decimal places. "
                "Consistent rounding across all screens."
            ),
            priority="High", test_type="Financial",
        ))

        test_cases.append(tc(
            summary="[FIN] Verify payment/charge breakdown is visible on confirmation screen",
            steps=(
                "1. Initiate with applicable charges\n"
                "2. Reach confirmation screen\n"
                "3. Verify each line item is labelled and displayed"
            ),
            expected=(
                "All fee components displayed as separate labelled line items. "
                "Grand total clearly indicated."
            ),
            priority="High", test_type="Financial",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 3 — UI / FRONTEND IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "UI Frontend Impact" in impact:

        test_cases.append(tc(
            summary="[UI] Verify all required fields and labels are displayed correctly",
            steps=(
                f"1. Navigate to {module_desc} in {channel}\n"
                "2. Check all visible fields have correct labels\n"
                "3. Verify no field is missing or misaligned"
            ),
            expected=(
                "All required fields visible with correct labels. "
                "No missing, overlapping, or broken UI elements."
            ),
            priority="High", test_type="UI",
        ))

        test_cases.append(tc(
            summary="[UI] Verify conditional display logic — elements shown/hidden correctly",
            steps=(
                "1. Test with condition that should show element — verify it appears\n"
                "2. Test with condition that should hide element — verify it is absent"
            ),
            expected=(
                "Conditional UI elements appear only when their condition is met. "
                "Hidden when condition is not met."
            ),
            priority="Critical", test_type="UI",
        ))

        test_cases.append(tc(
            summary="[UI] Verify responsive layout renders correctly across screen sizes",
            steps=(
                "1. Open feature on desktop browser\n"
                "2. Resize to tablet viewport\n"
                "3. Resize to mobile viewport\n"
                "4. Check layout at each size"
            ),
            expected=(
                "Layout adapts correctly at each viewport. "
                "No overlapping elements, no horizontal scroll on mobile."
            ),
            priority="Medium", test_type="UI",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 4 — FEATURE FLAG IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Feature Flag Impact" in impact:

        test_cases.append(tc(
            summary="[FLAG] Verify feature enabled: correct behaviour when flag is ON",
            steps=(
                "1. Set feature flag to ON/enabled in configuration\n"
                "2. Navigate to the affected feature\n"
                "3. Verify expected behaviour is active"
            ),
            expected=(
                "Feature behaves as designed when enabled. "
                "All new functionality accessible and working correctly."
            ),
            priority="Critical", test_type="Feature Flag",
        ))

        test_cases.append(tc(
            summary="[FLAG] Verify feature disabled: BAU behaviour when flag is OFF",
            steps=(
                "1. Set feature flag to OFF/disabled\n"
                "2. Navigate to the affected feature\n"
                "3. Verify BAU (before-feature) behaviour is restored"
            ),
            expected=(
                "Original BAU behaviour when flag is OFF. "
                "No new feature elements visible or active."
            ),
            priority="Critical", test_type="Feature Flag",
        ))

        test_cases.append(tc(
            summary="[FLAG] Verify flags are independent — toggling one does not affect another",
            steps=(
                "1. Toggle flag A ON, keep flag B OFF — verify each behaves independently\n"
                "2. Toggle flag B ON, keep flag A OFF — verify no cross-contamination"
            ),
            expected=(
                "Each flag controls only its own scope. "
                "No unintended side effects when toggling flags independently."
            ),
            priority="High", test_type="Feature Flag",
        ))

        test_cases.append(tc(
            summary="[FLAG] Verify feature rollout does not break existing functionality",
            steps=(
                "1. Enable the feature flag\n"
                "2. Run regression on all existing features in the module\n"
                "3. Verify no existing flows are broken"
            ),
            expected=(
                "All pre-existing features continue to work correctly. "
                "No regressions introduced by enabling the flag."
            ),
            priority="Critical", test_type="Feature Flag",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 5 — API CONTRACT IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "API Contract Impact" in impact or (code_risk and code_risk.get("validations", 0) > 0):

        test_cases.append(tc(
            summary="[API] Verify API request payload includes all required fields",
            steps=(
                "1. Initiate the action\n"
                "2. Capture the outbound API request\n"
                "3. Verify all mandatory fields are present with correct data types"
            ),
            expected=(
                "API payload contains all required fields with correct types and values. "
                "No missing or null mandatory fields."
            ),
            priority="High", test_type="API",
        ))

        test_cases.append(tc(
            summary="[API] Verify API response schema matches the expected contract",
            steps=(
                "1. Execute a successful action\n"
                "2. Capture the API response\n"
                "3. Validate response fields against the API contract/specification"
            ),
            expected=(
                "Response contains all documented fields with correct data types. "
                "No undocumented fields added without notice."
            ),
            priority="High", test_type="API",
        ))

        test_cases.append(tc(
            summary="[API] Verify backward compatibility — existing API fields unchanged",
            steps=(
                "1. Call the API with the existing request format\n"
                "2. Verify all existing response fields still present and unchanged"
            ),
            expected=(
                "All pre-existing API fields remain unchanged. "
                "New fields added additively. No breaking changes."
            ),
            priority="Critical", test_type="API",
        ))

        test_cases.append(tc(
            summary="[API] Verify API returns correct HTTP status codes",
            steps=(
                "1. Test success scenario — verify 200/201\n"
                "2. Test invalid input — verify 400\n"
                "3. Test unauthorized — verify 401/403\n"
                "4. Test not found — verify 404"
            ),
            expected=(
                "Correct HTTP status codes returned for each scenario. "
                "Error responses include descriptive message body."
            ),
            priority="High", test_type="API",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 6 — MIDDLEWARE / INTEGRATION IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Middleware ESB Impact" in impact or (code_risk and code_risk.get("error_handling", 0) > 0):

        test_cases.append(tc(
            summary="[MW] Verify timeout handling and automatic retry mechanism",
            steps=(
                "1. Simulate a downstream service timeout\n"
                "2. Submit the action\n"
                "3. Observe system retry behaviour"
            ),
            expected=(
                "System retries up to the configured limit. "
                "If all retries fail: action is rolled back and user is notified."
            ),
            priority="Critical", test_type="Error Handling",
        ))

        test_cases.append(tc(
            summary="[MW] Verify routing to correct downstream service",
            steps=(
                f"1. Submit a {module_desc} action\n"
                "2. Verify request is routed to the correct backend/service\n"
                "3. Confirm correct response is returned"
            ),
            expected=(
                f"Request routed to the {module_desc} service. "
                "Correct backend processes the request and returns expected response."
            ),
            priority="High", test_type="Integration",
        ))

        test_cases.append(tc(
            summary="[MW] Verify no duplicate processing on retry",
            steps=(
                "1. Submit action\n"
                "2. Simulate a timeout mid-process\n"
                "3. System auto-retries\n"
                "4. Verify no duplicate record is created"
            ),
            expected=(
                "Idempotency mechanism prevents duplicate processing. "
                "Only one record/entry created even after retry."
            ),
            priority="Critical", test_type="Data Integrity",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 7 — CORE BANKING / DATA INTEGRITY IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Core Banking Impact" in impact:

        test_cases.append(tc(
            summary="[CORE] Verify data is persisted correctly after successful submission",
            steps=(
                "1. Note state before action\n"
                "2. Complete action successfully\n"
                "3. Query database / verify in system"
            ),
            expected=(
                "Data saved accurately with all fields. "
                "Values match exactly what was submitted. "
                "No data truncation or corruption."
            ),
            priority="Critical", test_type="Data Integrity",
        ))

        test_cases.append(tc(
            summary="[CORE] Verify full rollback on processing failure",
            steps=(
                "1. Simulate a backend failure mid-transaction\n"
                "2. Check system state after failure\n"
                "3. Verify records and balances"
            ),
            expected=(
                "Transaction rolled back completely. "
                "System state unchanged from before the attempt. "
                "No partial data committed. Error message shown to user."
            ),
            priority="Critical", test_type="Data Integrity",
        ))

        test_cases.append(tc(
            summary="[CORE] Verify ledger/audit entry created with complete breakdown",
            steps=(
                "1. Complete action with multiple data components\n"
                "2. Check the audit/ledger record created"
            ),
            expected=(
                "Record includes separate entries for each component. "
                "All amounts and metadata recorded accurately."
            ),
            priority="High", test_type="Data Integrity",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 8 — VALIDATION / INPUT IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Validation Impact" in impact or (code_risk and code_risk.get("validations", 0) > 0):

        test_cases.append(tc(
            summary="[VAL] Verify all mandatory fields are validated before submission",
            steps=(
                "1. Leave each mandatory field empty one at a time\n"
                "2. Attempt to submit after each empty field\n"
                "3. Verify inline validation message appears"
            ),
            expected=(
                "Each empty mandatory field triggers an inline validation error. "
                "Submission blocked until all required fields are filled."
            ),
            priority="High", test_type="Validation",
        ))

        test_cases.append(tc(
            summary="[VAL] Verify special characters and injection attempts are rejected",
            steps=(
                "1. Enter HTML special characters (&lt;, &gt;, &amp;) in text fields\n"
                "2. Enter SQL injection patterns (e.g. ' OR 1=1 --)\n"
                "3. Attempt submission"
            ),
            expected=(
                "Special characters sanitised or rejected. "
                "No XSS, SQL injection, or other injection vulnerabilities."
            ),
            priority="High", test_type="Security",
        ))

        test_cases.append(tc(
            summary="[VAL] Verify amount/numeric field accepts only valid format",
            steps=(
                "1. Enter alphabetic characters in numeric field\n"
                "2. Enter negative number\n"
                "3. Enter a valid positive decimal"
            ),
            expected=(
                "Alphabetic input rejected. Negative numbers rejected. "
                "Valid positive decimals accepted up to allowed precision."
            ),
            priority="High", test_type="Validation",
        ))

        test_cases.append(tc(
            summary="[VAL] Verify field-level format validation (email, phone, ID, etc.)",
            steps=(
                "1. Enter incorrectly formatted value in each format-constrained field\n"
                "2. Attempt submission\n"
                "3. Enter correctly formatted value and retry"
            ),
            expected=(
                "Invalid format triggers inline error with clear guidance. "
                "Valid format passes validation. Submission proceeds."
            ),
            priority="Medium", test_type="Validation",
        ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 9 — LIMIT / BOUNDARY IMPACT
    # ═══════════════════════════════════════════════════════════════

    if "Limit Boundary Impact" in impact or (code_risk and code_risk.get("limit_checks", 0) > 0):

        below = max(tx_limit - 1, 1) if tx_limit else 9999
        at = tx_limit if tx_limit else 10000
        above = (tx_limit + 1) if tx_limit else 10001

        test_cases.append(tc(
            summary=f"[LIMIT] Verify action within limit is accepted ({below:,})",
            steps=(
                f"1. Enter value {below:,} (one below the limit)\n"
                "2. Submit the action"
            ),
            expected="Action accepted. No limit error. Proceeds to confirmation.",
            priority="Critical", test_type="Boundary",
        ))

        test_cases.append(tc(
            summary=f"[LIMIT] Verify action at exact limit is accepted ({at:,})",
            steps=(
                f"1. Enter exactly {at:,} (at the defined limit)\n"
                "2. Submit the action"
            ),
            expected=f"Action accepted at exact limit of {at:,}.",
            priority="Critical", test_type="Boundary",
        ))

        test_cases.append(tc(
            summary=f"[LIMIT] Verify action above limit is rejected ({above:,})",
            steps=(
                f"1. Enter {above:,} (one above the limit)\n"
                "2. Submit the action"
            ),
            expected=f"Action rejected. Error message shown: 'Exceeds limit of {at:,}'.",
            priority="Critical", test_type="Boundary",
        ))

        if daily_limit:
            test_cases.append(tc(
                summary=f"[LIMIT] Verify accumulated daily limit blocks further actions",
                steps=(
                    f"1. Complete actions totalling {daily_limit:,}\n"
                    "2. Attempt one more action"
                ),
                expected=(
                    f"Further action rejected. Error: 'Daily limit of {daily_limit:,} reached.'"
                ),
                priority="High", test_type="Boundary",
            ))

    # ═══════════════════════════════════════════════════════════════
    # SECTION 10 — COMPLIANCE / SECURITY IMPACT
    # ═══════════════════════════════════════════════════════════════

    if (
        "AML Compliance Impact" in impact
        or "Security Impact" in impact
        or "AML" in compliance_list
        or "PCI_DSS" in compliance_list
    ):

        test_cases.append(tc(
            summary="[SEC] Verify access control — unauthorised user cannot access feature",
            steps=(
                "1. Attempt to access the feature without authentication\n"
                "2. Attempt with a user lacking required permissions\n"
                "3. Verify in both cases"
            ),
            expected=(
                "Unauthenticated request redirected to login. "
                "Insufficient permissions returns 403 Forbidden. "
                "No data is leaked."
            ),
            priority="Critical", test_type="Security",
        ))

        test_cases.append(tc(
            summary="[SEC] Verify sensitive data is masked in UI and logs",
            steps=(
                "1. Complete the action\n"
                "2. Check UI fields for sensitive data (passwords, card numbers, IDs)\n"
                "3. Check application logs"
            ),
            expected=(
                "Sensitive fields are masked in the UI (e.g. ****1234). "
                "No sensitive data in plaintext in logs."
            ),
            priority="Critical", test_type="Security",
        ))

        if "AML Compliance Impact" in impact or "AML" in compliance_list:
            test_cases.append(tc(
                summary="[AML] Verify sanctions/compliance screening before processing",
                steps=(
                    "1. Enter a party name/ID that triggers a compliance flag\n"
                    "2. Submit the action\n"
                    "3. Observe result"
                ),
                expected=(
                    "System screens against compliance lists before processing. "
                    "Flagged entry is rejected with audit log created."
                ),
                priority="Critical", test_type="Compliance",
            ))

            test_cases.append(tc(
                summary="[AML] Verify declaration/purpose field is mandatory for high-risk actions",
                steps=(
                    "1. Attempt submission without completing the required declaration\n"
                    "2. Complete declaration and retry"
                ),
                expected=(
                    "Submission blocked without declaration. "
                    "Valid declaration allows submission to proceed."
                ),
                priority="High", test_type="Compliance",
            ))

    return test_cases
