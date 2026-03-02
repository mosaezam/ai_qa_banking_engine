from agents.module_detector import (
    detect_module_and_channel,
    get_module_description,
    get_module_compliance,
    get_module_limits
)


def generate_test_cases(story, impact, config, code_risk=None, risk_score=None, risk_level=None):

    # =========================================
    # MODULE DETECTION
    # =========================================
    module_name, channel = detect_module_and_channel(story)
    module = module_name.upper()
    module_desc = get_module_description(module_name)
    compliance_list = get_module_compliance(module_name)
    limits = get_module_limits(module_name)
    tx_limit = limits.get("transaction", 50000)
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
            "precondition": f"User is logged into {channel} with valid credentials and sufficient balance for {module_desc}",
            "steps": steps,
            "expected_result": expected
        }

    # =========================================
    # SECTION 1 — USER STORY FLOW (Always)
    # =========================================

    test_cases.append(tc(
        summary=f"[STORY] Verify end-to-end {module} transfer — New Transfer",
        steps=f"1. Login to {channel}\n2. Navigate: Transfer > Overseas > {module_desc}\n3. Select New Transfer\n4. Enter valid recipient details\n5. Enter valid amount\n6. Review confirmation screen\n7. Authenticate via Secure2u\n8. Submit",
        expected="Transaction completes. Reference number generated. Receipt page shows all transfer details.",
        priority="Critical"
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module} favourite transfer flow",
        steps=f"1. Login to {channel}\n2. Navigate: Transfer > Overseas > {module_desc}\n3. Select Favourite Transfer\n4. Select saved recipient\n5. Enter amount\n6. Confirm and submit",
        expected="Favourite transfer completes successfully using pre-saved recipient details",
        priority="High"
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module} confirmation page shows all required fields",
        steps="1. Enter valid transfer details\n2. Proceed to confirmation screen\n3. Check all fields present",
        expected="Confirmation shows: Principal, Service Fee, SST, Agent Fee, Total Amount, Recipient Name, Reference, Exchange Rate",
        priority="Critical"
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module} receipt page generated after successful transfer",
        steps="1. Complete successful transfer\n2. Click PDF on receipt\n3. Verify all fields on receipt",
        expected="Receipt shows: Reference No, Date/Time, Amount, Fee breakdown, SST, Recipient details, Status: SUCCESS",
        priority="High"
    ))

    test_cases.append(tc(
        summary=f"[STORY] Verify {module} transaction visible in M2U transaction history",
        steps="1. Complete transfer\n2. Navigate to Transaction History / Statement\n3. Locate the transaction",
        expected="History shows: Amount, Fee, SST, Date, Reference No, Status, Recipient",
        priority="High"
    ))

    # =========================================
    # SECTION 2 — FINANCIAL CALCULATION IMPACT
    # =========================================

    if "Financial Calculation Impact" in impact or (code_risk and code_risk.get("fee_logic", 0) > 0):

        test_cases.append(tc(
            summary=f"[FIN] Verify SST 8% calculated correctly on service fee",
            steps="1. Enter transfer amount with applicable service fee\n2. Proceed to confirmation\n3. Verify: SST = Service Fee × 8%",
            expected="SST = exactly 8% of Service Fee. Rounded to 2 decimal places. Displayed as separate line item.",
            priority="Critical", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[FIN] Verify total amount = Principal + Service Fee + SST(SF) + Agent Fee + SST(AF)",
            steps="1. Enter amount with charges\n2. On confirmation: manually calculate total\n3. Compare with displayed total",
            expected="Total Amount = Principal + Service Fee + 8% SST on Service Fee + Agent Fee + 8% SST on Agent Fee",
            priority="Critical", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[FIN] Verify BAU flow when NO charges applicable",
            steps="1. Initiate transfer with zero service fee\n2. Check confirmation screen",
            expected="Service Fee = RM 0.00. Agent Fee = RM 0.00. SST lines NOT displayed. Total = Principal only. BAU unchanged.",
            priority="High", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[FIN] Verify fee rounding with decimal transfer amounts",
            steps="1. Enter RM 1234.56\n2. Check fee on confirmation\n3. Verify 2 decimal rounding",
            expected="Fee rounded to exactly 2 decimal places. No floating point errors. Consistent across all screens.",
            priority="High", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[FIN] Verify S2U screen shows total amount labelled (Includes 8% SST)",
            steps="1. Initiate transfer with charges\n2. Reach S2U screen\n3. Verify total amount label",
            expected="S2U shows: Total Amount (Includes 8% SST) = Principal + All Fees + All SST amounts",
            priority="Critical", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[FIN] Verify agent/beneficiary bank fee SST line item added",
            steps="1. Initiate transfer with agent fee applicable\n2. Check confirmation screen",
            expected="New line: '8% SST on Agent Fee' displayed separately. Amount = Agent Fee × 8%",
            priority="Critical", test_type="Financial"
        ))

    # =========================================
    # SECTION 3 — UI FRONTEND IMPACT
    # =========================================

    if "UI Frontend Impact" in impact:

        test_cases.append(tc(
            summary=f"[UI] Verify SST tooltip text updated on transfer details screen",
            steps="1. Navigate to {module_desc} transfer details\n2. Click info/tooltip icon next to Agent/Beneficiary Bank Fee\n3. Read tooltip content",
            expected="Tooltip: 'If an agent/beneficiary bank fee is applicable, the fee (inclusive of 8% SST) will be paid from your local accounts during the transfer details later.'",
            priority="High", test_type="UI"
        ))

        test_cases.append(tc(
            summary=f"[UI] Verify (Includes 8% SST) label appears only when charges applicable",
            steps="1. Test with transfer having charges — verify SST label shown\n2. Test with zero charge transfer — verify SST label NOT shown",
            expected="SST label conditional: shown only when fee > 0. Hidden for zero-charge transfers.",
            priority="Critical", test_type="UI"
        ))

        test_cases.append(tc(
            summary=f"[UI] Verify all new SST field labels displayed on confirmation page",
            steps="1. Complete transfer details with charges\n2. On confirmation: verify all new labels",
            expected="Labels present: 'Service Fee', '8% SST on Service Fee', 'Agent Fee', '8% SST on Agent Fee', 'Total Amount (Includes 8% SST)'",
            priority="High", test_type="UI"
        ))

    # =========================================
    # SECTION 4 — FEATURE FLAG IMPACT
    # =========================================

    if "Feature Flag Impact" in impact:

        test_cases.append(tc(
            summary="[FLAG] DCC=ON RMBP=ON — SST displayed in UI and SST deducted in backend",
            steps="1. Set DCC flag = ON in backend config\n2. Set RMBP flag = ON in frontend config\n3. Initiate transfer with service fee\n4. Check confirmation screen for SST label\n5. Complete transfer\n6. Verify amount deducted from account",
            expected="Frontend: SST label shown with '(Includes 8% SST)'. Backend: SST amount correctly deducted. Total = Principal + Fee + SST.",
            priority="Critical", test_type="Feature Flag"
        ))

        test_cases.append(tc(
            summary="[FLAG] DCC=OFF RMBP=OFF — No SST in UI and no SST deducted (Full BAU)",
            steps="1. Set DCC flag = OFF\n2. Set RMBP flag = OFF\n3. Initiate transfer\n4. Check confirmation — no SST label\n5. Complete transfer\n6. Verify deducted amount",
            expected="Frontend: No SST label shown anywhere. Backend: No SST deducted. Total = Principal + Fee only. Full BAU behaviour.",
            priority="Critical", test_type="Feature Flag"
        ))

        test_cases.append(tc(
            summary="[FLAG] DCC=ON RMBP=OFF — SST NOT shown in UI but SST IS silently deducted (CRITICAL RISK)",
            steps="1. Set DCC = ON, RMBP = OFF\n2. Initiate transfer\n3. Confirm screen — verify NO SST label shown\n4. Complete transfer\n5. Check actual amount deducted from account\n6. Compare displayed total vs actual deduction",
            expected="Frontend: No SST label (RMBP=OFF hides UI). Backend: SST silently deducted (DCC=ON charges backend). Actual deduction = Principal + Fee + SST even though SST not visible to customer.",
            priority="Critical", test_type="Feature Flag"
        ))

        test_cases.append(tc(
            summary="[FLAG] DCC=OFF RMBP=ON — SST shown in UI but NO SST deducted in backend",
            steps="1. Set DCC = OFF, RMBP = ON\n2. Initiate transfer\n3. Check if SST label appears on screen\n4. Complete transfer\n5. Verify actual amount deducted",
            expected="Frontend may show SST label (RMBP=ON). Backend: NO SST deducted (DCC=OFF). Actual deduction = Principal + Fee only. No mismatch between displayed and charged amount.",
            priority="Critical", test_type="Feature Flag"
        ))

        test_cases.append(tc(
            summary="[FLAG] Verify DCC flag controls backend SST calculation independently",
            steps="1. Toggle DCC ON — verify SST calculated in backend\n2. Toggle DCC OFF — verify no SST in backend\n3. Keep RMBP unchanged throughout",
            expected="DCC exclusively controls backend SST deduction. Changing RMBP has zero effect on backend calculation.",
            priority="High", test_type="Feature Flag"
        ))

        test_cases.append(tc(
            summary="[FLAG] Verify RMBP flag controls frontend SST display independently",
            steps="1. Toggle RMBP ON — verify SST label shown on all screens\n2. Toggle RMBP OFF — verify SST label hidden\n3. Keep DCC unchanged throughout",
            expected="RMBP exclusively controls frontend SST visibility. Changing DCC has zero effect on UI display.",
            priority="High", test_type="Feature Flag"
        ))

    # =========================================
    # SECTION 5 — API CONTRACT IMPACT
    # =========================================

    if "API Contract Impact" in impact or (code_risk and code_risk.get("validations", 0) > 0):

        test_cases.append(tc(
            summary=f"[API] Verify API request payload includes all required fields",
            steps="1. Initiate transfer\n2. Capture API request\n3. Verify all mandatory fields present in payload",
            expected="API payload contains: amount, currency, recipient, fee, sst, channel, moduleType, referenceNo",
            priority="High", test_type="API"
        ))

        test_cases.append(tc(
            summary=f"[API] Verify API response schema matches expected contract",
            steps="1. Complete transfer\n2. Capture API response\n3. Verify response fields",
            expected="Response contains: status, referenceNo, transactionId, totalAmount, feeBreakdown, timestamp",
            priority="High", test_type="API"
        ))

        test_cases.append(tc(
            summary=f"[API] Verify backward compatibility — existing fields unchanged",
            steps="1. Call API with existing request format\n2. Verify existing response fields still present",
            expected="All existing API fields unchanged. New SST fields added. No breaking changes.",
            priority="Critical", test_type="API"
        ))

    # =========================================
    # SECTION 6 — MIDDLEWARE / GATEWAY IMPACT
    # =========================================

    if "Middleware ESB Impact" in impact or (code_risk and code_risk.get("error_handling", 0) > 0):

        test_cases.append(tc(
            summary=f"[MW] Verify gateway timeout handling and retry mechanism",
            steps="1. Simulate gateway timeout\n2. Submit transfer\n3. Observe retry behaviour",
            expected="System auto-retries up to configured limit. If all retries fail: transaction rolled back, user notified.",
            priority="Critical", test_type="Error Handling"
        ))

        test_cases.append(tc(
            summary=f"[MW] Verify ESB routing to correct {module} backend service",
            steps="1. Submit {module} transfer\n2. Verify request routed to correct backend\n3. Check response",
            expected="ESB routes to {module_desc} service. Correct backend processes the transaction.",
            priority="High", test_type="Integration"
        ))

        test_cases.append(tc(
            summary=f"[MW] Verify duplicate transaction not posted on retry",
            steps="1. Submit transfer\n2. Simulate timeout\n3. System retries\n4. Check if duplicate posted",
            expected="Idempotency key prevents duplicate posting. Only one ledger entry created even after retry.",
            priority="Critical", test_type="Data Integrity"
        ))

    # =========================================
    # SECTION 7 — CORE BANKING IMPACT
    # =========================================

    if "Core Banking Impact" in impact:

        test_cases.append(tc(
            summary=f"[CORE] Verify ledger debit posting — correct amount deducted",
            steps="1. Note balance before transfer\n2. Complete transfer\n3. Check account balance after",
            expected="Balance reduced by exactly: Principal + Service Fee + SST + Agent Fee. No extra deductions.",
            priority="Critical", test_type="Financial"
        ))

        test_cases.append(tc(
            summary=f"[CORE] Verify transaction rollback on core banking failure",
            steps="1. Simulate core banking failure mid-transaction\n2. Check account balance\n3. Check transaction history",
            expected="Transaction rolled back completely. Balance unchanged. No partial posting. Error shown to user.",
            priority="Critical", test_type="Data Integrity"
        ))

        test_cases.append(tc(
            summary=f"[CORE] Verify ledger entry includes SST breakdown",
            steps="1. Complete transfer with SST charges\n2. Check core banking ledger entry",
            expected="Ledger has separate entries for: Principal, Service Fee, SST on Service Fee, Agent Fee, SST on Agent Fee",
            priority="High", test_type="Financial"
        ))

    # =========================================
    # SECTION 8 — VALIDATION IMPACT
    # =========================================

    if "Validation Impact" in impact or (code_risk and code_risk.get("validations", 0) > 0):

        test_cases.append(tc(
            summary=f"[VAL] Verify all mandatory fields validated before submission",
            steps="1. Leave each mandatory field empty one at a time\n2. Attempt submission after each",
            expected="Each empty mandatory field triggers inline validation error. Submission blocked.",
            priority="High", test_type="Validation"
        ))

        test_cases.append(tc(
            summary=f"[VAL] Verify special characters rejected in text fields",
            steps="1. Enter <script>, SQL injection, emoji in name fields\n2. Attempt submission",
            expected="Special characters sanitised or rejected. No XSS or injection vulnerabilities.",
            priority="High", test_type="Security"
        ))

        test_cases.append(tc(
            summary=f"[VAL] Verify amount field accepts only valid numeric format",
            steps="1. Enter letters in amount field\n2. Enter negative number\n3. Enter valid decimal",
            expected="Letters rejected. Negative rejected. Valid decimal accepted up to 2 decimal places.",
            priority="High", test_type="Validation"
        ))

    # =========================================
    # SECTION 9 — LIMIT BOUNDARY IMPACT
    # =========================================

    if "Limit Boundary Impact" in impact or (code_risk and code_risk.get("limit_checks", 0) > 0):

        test_cases.append(tc(
            summary=f"[LIMIT] Verify transfer within limit accepted (RM {tx_limit - 1:,})",
            steps=f"1. Enter RM {tx_limit - 1:,}\n2. Submit transfer",
            expected=f"Transfer accepted. No limit error. Proceeds to confirmation.",
            priority="Critical", test_type="Boundary"
        ))

        test_cases.append(tc(
            summary=f"[LIMIT] Verify transfer at exact limit accepted (RM {tx_limit:,})",
            steps=f"1. Enter exactly RM {tx_limit:,}\n2. Submit transfer",
            expected=f"Transfer accepted at exact limit of RM {tx_limit:,}.",
            priority="Critical", test_type="Boundary"
        ))

        test_cases.append(tc(
            summary=f"[LIMIT] Verify transfer above limit rejected (RM {tx_limit + 1:,})",
            steps=f"1. Enter RM {tx_limit + 1:,}\n2. Submit transfer",
            expected=f"Transfer rejected. Error: 'Amount exceeds transaction limit of RM {tx_limit:,}'",
            priority="Critical", test_type="Boundary"
        ))

        test_cases.append(tc(
            summary=f"[LIMIT] Verify daily limit accumulation blocks further transfers",
            steps=f"1. Complete transfers totalling RM {daily_limit:,}\n2. Attempt one more transfer",
            expected=f"Further transfer rejected. Error: 'Daily limit of RM {daily_limit:,} reached. Try again tomorrow.'",
            priority="High", test_type="Boundary"
        ))

    # =========================================
    # SECTION 10 — AML COMPLIANCE IMPACT
    # =========================================

    if "AML Compliance Impact" in impact or "AML" in compliance_list or "OFAC" in compliance_list:

        test_cases.append(tc(
            summary=f"[AML] Verify OFAC sanctions screening before transaction processed",
            steps="1. Enter recipient name matching OFAC list\n2. Submit transfer\n3. Observe result",
            expected="System screens against OFAC before processing. Sanctioned recipient rejected with error. Audit logged.",
            priority="Critical", test_type="Compliance"
        ))

        test_cases.append(tc(
            summary=f"[AML] Verify source of funds declaration triggered for high amounts",
            steps="1. Enter amount at AML threshold\n2. Check if declaration screen appears",
            expected="Source of funds declaration mandatory at configured threshold. Cannot proceed without completion.",
            priority="Critical", test_type="Compliance"
        ))

        test_cases.append(tc(
            summary=f"[AML] Verify purpose of transfer mandatory field",
            steps="1. Attempt submission without purpose of transfer\n2. Select valid purpose and retry",
            expected="Purpose of transfer mandatory. Valid options listed. Cannot submit without selection.",
            priority="High", test_type="Compliance"
        ))

    return test_cases