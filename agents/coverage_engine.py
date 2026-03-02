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

    def create_test_case(summary, steps, expected, priority="High", test_type="Functional"):
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
            "precondition": f"User is logged into {channel} with valid credentials and has sufficient balance for {module_desc}",
            "steps": steps,
            "expected_result": expected
        }

    # =========================================
    # SECTION 1 — USER STORY FLOW TESTS
    # =========================================

    test_cases.append(create_test_case(
        summary=f"[STORY] Verify end-to-end {module} transfer flow on {channel}",
        steps=f"1. Login to {channel}\n2. Navigate to Overseas Transfer > {module_desc}\n3. Select New Transfer\n4. Enter valid recipient details\n5. Enter valid amount\n6. Review confirmation screen\n7. Authenticate via Secure2u\n8. Submit transaction",
        expected=f"Transaction completes successfully with reference number generated. Receipt page displayed with all transfer details.",
        priority="Critical"
    ))

    test_cases.append(create_test_case(
        summary=f"[STORY] Verify {module} favourite transfer flow",
        steps=f"1. Login to {channel}\n2. Navigate to Overseas Transfer > {module_desc}\n3. Select Favourite Transfer\n4. Select saved recipient\n5. Enter amount\n6. Submit",
        expected="Favourite transfer completes successfully using saved recipient details",
        priority="High"
    ))

    test_cases.append(create_test_case(
        summary=f"[STORY] Verify {module} confirmation page displays correct details",
        steps="1. Initiate transfer with valid details\n2. Proceed to confirmation screen\n3. Verify all fields displayed",
        expected="Confirmation page shows: Principal amount, Service Fee, SST amount, Total Amount, Recipient details, Exchange rate (if applicable)",
        priority="Critical"
    ))

    test_cases.append(create_test_case(
        summary=f"[STORY] Verify {module} receipt page after successful transfer",
        steps="1. Complete successful transfer\n2. Click PDF to generate receipt\n3. Verify receipt contents",
        expected="Receipt shows transaction reference, date/time, amount, fee breakdown, recipient details",
        priority="High"
    ))

    test_cases.append(create_test_case(
        summary=f"[STORY] Verify {module} transaction appears in transaction history",
        steps="1. Complete transfer\n2. Navigate to Transaction History\n3. Locate the transaction",
        expected="Transaction history shows correct amount, fee, date, reference number and status",
        priority="High"
    ))

    # =========================================
    # SECTION 2 — FINANCIAL CALCULATION TESTS
    # =========================================

    if "Financial Calculation Impact" in impact or (code_risk and code_risk.get("fee_logic", 0) > 0):

        test_cases.append(create_test_case(
            summary=f"[FEE] Verify SST 8% calculation on service fee for {module}",
            steps="1. Enter transfer amount with applicable service fee\n2. Proceed to confirmation\n3. Verify SST = Service Fee × 8%",
            expected="SST amount = exactly 8% of service fee. Rounded to 2 decimal places.",
            priority="Critical",
            test_type="Financial"
        ))

        test_cases.append(create_test_case(
            summary=f"[FEE] Verify total amount calculation includes all charges",
            steps="1. Enter transfer amount\n2. Check total on confirmation screen\n3. Manually calculate: Principal + Service Fee + SST + Agent Fee",
            expected=f"Total Amount = Principal + Service Fee + SST on Service Fee + Agent/Beneficiary Bank Fee + SST on Agent Fee",
            priority="Critical",
            test_type="Financial"
        ))

        test_cases.append(create_test_case(
            summary=f"[FEE] Verify fee display when NO charges applicable (BAU flow)",
            steps="1. Initiate transfer where no service fee applies\n2. Check confirmation screen",
            expected="Service Fee and Agent Fee fields show RM 0.00. SST line not displayed. BAU flow unchanged.",
            priority="High",
            test_type="Financial"
        ))

        test_cases.append(create_test_case(
            summary=f"[FEE] Verify fee rounding with decimal transfer amounts",
            steps="1. Enter amount like RM 1234.56\n2. Proceed to confirmation\n3. Verify fee rounding",
            expected="Fee rounded correctly to 2 decimal places per business rules. No floating point errors.",
            priority="High",
            test_type="Financial"
        ))

        test_cases.append(create_test_case(
            summary=f"[FEE] Verify S2U screen shows correct total amount including SST",
            steps="1. Initiate transfer\n2. Reach S2U authentication screen\n3. Verify total amount displayed",
            expected="S2U screen total = Principal + Service Fee SST + Agent Fee SST. Labelled '(Includes 8% SST)'",
            priority="Critical",
            test_type="Financial"
        ))

    # =========================================
    # SECTION 3 — CODEBASE SIGNAL TESTS
    # =========================================

    if code_risk:

        if code_risk.get("validations", 0) > 0:
            test_cases.append(create_test_case(
                summary=f"[CODE] Verify recipient details validation in {module}",
                steps="1. Leave mandatory recipient fields empty\n2. Attempt to proceed\n3. Enter invalid format values\n4. Attempt to proceed",
                expected="System shows field-level validation errors. Cannot proceed without valid recipient details.",
                priority="High",
                test_type="Validation"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify input field format validation",
                steps="1. Enter special characters in name fields\n2. Enter letters in amount field\n3. Attempt submission",
                expected="System rejects invalid input formats with appropriate error messages",
                priority="High",
                test_type="Validation"
            ))

        if code_risk.get("limit_checks", 0) > 0:
            test_cases.append(create_test_case(
                summary=f"[CODE] Verify transaction limit — amount within limit (RM {tx_limit:,})",
                steps=f"1. Enter amount below RM {tx_limit:,}\n2. Submit transfer",
                expected="Transfer proceeds successfully. No limit error shown.",
                priority="Critical",
                test_type="Boundary"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify transaction limit — amount equal to limit (RM {tx_limit:,})",
                steps=f"1. Enter amount exactly RM {tx_limit:,}\n2. Submit transfer",
                expected=f"Transfer allowed at exact limit of RM {tx_limit:,}",
                priority="Critical",
                test_type="Boundary"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify transaction limit — amount exceeds limit (RM {tx_limit + 1:,})",
                steps=f"1. Enter amount RM {tx_limit + 1:,}\n2. Submit transfer",
                expected=f"System rejects transfer. Error: 'Exceeds transaction limit of RM {tx_limit:,}'",
                priority="Critical",
                test_type="Boundary"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify daily limit accumulation across multiple transfers",
                steps=f"1. Complete transfers totalling RM {daily_limit:,}\n2. Attempt another transfer",
                expected=f"System rejects transfer once daily limit of RM {daily_limit:,} is reached",
                priority="High",
                test_type="Boundary"
            ))

        if code_risk.get("fee_logic", 0) > 0:
            test_cases.append(create_test_case(
                summary=f"[CODE] Verify fee calculation for minimum transfer amount",
                steps="1. Enter minimum allowed transfer amount\n2. Check fee on confirmation",
                expected="Fee calculated correctly even for minimum amount. No negative or zero fee errors.",
                priority="High",
                test_type="Financial"
            ))

        if code_risk.get("error_handling", 0) > 0:
            test_cases.append(create_test_case(
                summary=f"[CODE] Verify error handling when backend gateway is unavailable",
                steps="1. Simulate gateway timeout/unavailability\n2. Submit transfer\n3. Observe system response",
                expected="System shows user-friendly error message. Transaction not submitted. No duplicate posting.",
                priority="Critical",
                test_type="Error Handling"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify duplicate transaction prevention",
                steps="1. Submit transfer successfully\n2. Immediately resubmit same transaction within 60 seconds",
                expected="System detects duplicate and prevents double submission with appropriate warning",
                priority="Critical",
                test_type="Error Handling"
            ))

            test_cases.append(create_test_case(
                summary=f"[CODE] Verify audit trail logging for all transactions",
                steps="1. Complete a transfer\n2. Verify audit log entry",
                expected="Audit trail captures: timestamp, user ID, amount, recipient, reference number, status",
                priority="High",
                test_type="Audit"
            ))

    # =========================================
    # SECTION 4 — MODULE-SPECIFIC TESTS
    # =========================================

    if module_name == "bakong":
        test_cases.append(create_test_case(
            summary="[BAKONG] Verify Bakong ID format validation",
            steps="1. Enter invalid Bakong ID format\n2. Enter valid Bakong ID\n3. Verify acceptance",
            expected="Invalid Bakong ID rejected. Valid ID accepted and registered with NBC gateway.",
            priority="Critical", test_type="Validation"
        ))
        test_cases.append(create_test_case(
            summary="[BAKONG] Verify KHR and USD currency selection",
            steps="1. Select KHR as destination currency\n2. Verify exchange rate displayed\n3. Repeat with USD",
            expected="Both KHR and USD accepted. Exchange rate fetched from NBC. Other currencies rejected.",
            priority="High", test_type="Functional"
        ))
        test_cases.append(create_test_case(
            summary="[BAKONG] Verify NBC bank code validation",
            steps="1. Enter invalid NBC bank code\n2. Enter valid 6-digit NBC code\n3. Submit",
            expected="Invalid code rejected. Valid NBC code verified against NBC registry.",
            priority="High", test_type="Validation"
        ))

    elif module_name == "ftt":
        test_cases.append(create_test_case(
            summary="[FTT] Verify DuitNow ID types — Mobile, NRIC, Passport, Business Reg",
            steps="1. Test transfer using Mobile number as DuitNow ID\n2. Repeat with NRIC\n3. Repeat with Passport",
            expected="All valid DuitNow ID types accepted. Invalid types rejected with error.",
            priority="Critical", test_type="Functional"
        ))
        test_cases.append(create_test_case(
            summary="[FTT] Verify tiered limit — Standard vs Premier customer",
            steps="1. Login as Standard customer\n2. Attempt RM 75,000 transfer\n3. Login as Premier customer\n4. Attempt same amount",
            expected="Standard customer: rejected. Premier customer: allowed.",
            priority="Critical", test_type="Boundary"
        ))
        test_cases.append(create_test_case(
            summary="[FTT] Verify DuitNow instant transfer zero fee",
            steps="1. Initiate DuitNow transfer\n2. Check fee on confirmation",
            expected="DuitNow transfer shows RM 0.00 service fee. IBFT shows RM 0.50.",
            priority="High", test_type="Financial"
        ))

    elif module_name == "mot":
        test_cases.append(create_test_case(
            summary="[MOT] Verify SWIFT/BIC code format validation",
            steps="1. Enter invalid SWIFT code (wrong length/format)\n2. Enter valid 8 or 11 character BIC\n3. Submit",
            expected="Invalid SWIFT code rejected with format error. Valid BIC accepted.",
            priority="Critical", test_type="Validation"
        ))
        test_cases.append(create_test_case(
            summary="[MOT] Verify IBAN validation for European destinations",
            steps="1. Select European destination country\n2. Enter invalid IBAN\n3. Enter valid IBAN",
            expected="IBAN mandatory for EU destinations. Invalid format rejected. Valid IBAN accepted.",
            priority="Critical", test_type="Validation"
        ))
        test_cases.append(create_test_case(
            summary="[MOT] Verify live BNM exchange rate display with timestamp",
            steps="1. Initiate MOT transfer\n2. Check exchange rate displayed on screen",
            expected="Live exchange rate shown with BNM timestamp. Rate updates on refresh.",
            priority="High", test_type="Functional"
        ))

    elif module_name == "westernunion":
        test_cases.append(create_test_case(
            summary="[WU] Verify MTCN generation after successful transfer",
            steps="1. Complete WU transfer\n2. Check receipt for MTCN",
            expected="10-digit MTCN generated and displayed on receipt. Recipient can use MTCN for cash pickup.",
            priority="Critical", test_type="Functional"
        ))
        test_cases.append(create_test_case(
            summary="[WU] Verify OFAC sanctions screening before submission",
            steps="1. Enter recipient name flagged in OFAC list\n2. Attempt submission",
            expected="System screens against OFAC before MTCN generation. Flagged recipients rejected.",
            priority="Critical", test_type="Compliance"
        ))
        test_cases.append(create_test_case(
            summary="[WU] Verify source of funds declaration for amounts above RM 3,000",
            steps="1. Enter amount RM 2,999 — no declaration needed\n2. Enter amount RM 3,000 — declaration required",
            expected="Below RM 3,000: no source of funds required. RM 3,000 and above: mandatory declaration.",
            priority="Critical", test_type="Compliance"
        ))
        test_cases.append(create_test_case(
            summary="[WU] Verify recipient ID mandatory for all WU transfers",
            steps="1. Attempt transfer without recipient ID\n2. Enter valid ID type and number",
            expected="Transfer rejected without recipient ID. Valid ID accepted for KYC compliance.",
            priority="High", test_type="Compliance"
        ))

    elif module_name == "visadirect":
        test_cases.append(create_test_case(
            summary="[VISA] Verify Luhn algorithm validation on recipient card number",
            steps="1. Enter card number that fails Luhn check\n2. Enter valid Visa card number",
            expected="Invalid Luhn card rejected immediately. Valid card passes and proceeds.",
            priority="Critical", test_type="Validation"
        ))
        test_cases.append(create_test_case(
            summary="[VISA] Verify BIN lookup for Visa Direct eligibility",
            steps="1. Enter non-Visa card number\n2. Enter Visa card not eligible for push payment\n3. Enter eligible Visa card",
            expected="Non-eligible cards rejected. Only Visa Direct eligible cards accepted.",
            priority="Critical", test_type="Validation"
        ))
        test_cases.append(create_test_case(
            summary="[VISA] Verify purpose code mandatory above RM 10,000",
            steps="1. Enter RM 9,999 — no purpose code needed\n2. Enter RM 10,001 — purpose code required",
            expected="Below RM 10,000: purpose code optional. Above RM 10,000: mandatory selection.",
            priority="High", test_type="Compliance"
        ))
        test_cases.append(create_test_case(
            summary="[VISA] Verify card number masked on confirmation and receipt",
            steps="1. Enter 16-digit card number\n2. Check confirmation screen\n3. Check receipt",
            expected="Card shown as ****-****-****-XXXX (last 4 digits only). PCI DSS compliant.",
            priority="Critical", test_type="Security"
        ))

    elif module_name == "eipo":
        test_cases.append(create_test_case(
            summary="[EIPO] Verify OUR charge type — sender pays all charges",
            steps="1. Select OUR charge type\n2. Check fee breakdown on confirmation",
            expected="Sender pays full service fee + agent fee. Beneficiary receives full principal amount.",
            priority="Critical", test_type="Financial"
        ))
        test_cases.append(create_test_case(
            summary="[EIPO] Verify SHA charge type — shared charges",
            steps="1. Select SHA charge type\n2. Check fee breakdown on confirmation",
            expected="Service fee deducted from sender. Agent fee deducted from beneficiary amount.",
            priority="Critical", test_type="Financial"
        ))
        test_cases.append(create_test_case(
            summary="[EIPO] Verify BEN charge type — beneficiary pays all",
            steps="1. Select BEN charge type\n2. Check fee breakdown on confirmation",
            expected="No fee charged to sender. Full charges deducted from beneficiary amount.",
            priority="High", test_type="Financial"
        ))
        test_cases.append(create_test_case(
            summary="[EIPO] Verify purpose code mandatory for all EIPO transfers",
            steps="1. Attempt EIPO transfer without purpose code\n2. Select valid purpose code and retry",
            expected="Transfer rejected without purpose code. Valid purpose codes: TRADE, SALARY, INVESTMENT, PERSONAL, EDUCATION, MEDICAL",
            priority="Critical", test_type="Compliance"
        ))
        test_cases.append(create_test_case(
            summary="[EIPO] Verify SWIFT MT103 reference generated on confirmation",
            steps="1. Complete EIPO transfer\n2. Check receipt for SWIFT reference",
            expected="SWIFT MT103 reference number generated and stored in audit trail for regulatory compliance",
            priority="Critical", test_type="Functional"
        ))

    # =========================================
    # SECTION 5 — COMPLIANCE TESTS
    # =========================================

    if "SST" in compliance_list:
        test_cases.append(create_test_case(
            summary=f"[COMPLIANCE] Verify SST tooltip content updated for {module}",
            steps="1. Navigate to transfer details screen\n2. Click SST tooltip/info icon\n3. Verify tooltip message",
            expected="Tooltip shows: 'The fee (inclusive of 8% SST) will be paid from your local account during transfer'",
            priority="High", test_type="Compliance"
        ))

    if "AML" in compliance_list or "FATF" in compliance_list:
        test_cases.append(create_test_case(
            summary=f"[COMPLIANCE] Verify AML screening for high-value {module} transfers",
            steps="1. Initiate transfer above AML threshold\n2. Verify screening triggered\n3. Check audit log",
            expected="AML screening triggered for high-value transfers. Result logged in audit trail.",
            priority="Critical", test_type="Compliance"
        ))

    if "BNM_FX" in compliance_list:
        test_cases.append(create_test_case(
            summary=f"[COMPLIANCE] Verify BNM foreign exchange compliance for {module}",
            steps="1. Initiate overseas transfer\n2. Verify exchange rate source\n3. Check BNM rate applied",
            expected="Exchange rate sourced from BNM. Rate displayed with timestamp. Compliant with BNM FX regulations.",
            priority="High", test_type="Compliance"
        ))

    # =========================================
    # SECTION 6 — NEGATIVE TESTS
    # =========================================

    test_cases.append(create_test_case(
        summary=f"[NEGATIVE] Verify rejection of zero transfer amount",
        steps="1. Enter RM 0.00 as transfer amount\n2. Attempt to proceed",
        expected="System rejects zero amount with error: 'Amount must be greater than zero'",
        priority="Critical", test_type="Negative"
    ))

    test_cases.append(create_test_case(
        summary=f"[NEGATIVE] Verify rejection of negative transfer amount",
        steps="1. Enter negative amount e.g. -100\n2. Attempt to proceed",
        expected="System rejects negative amount. Field should not accept negative values.",
        priority="Critical", test_type="Negative"
    ))

    test_cases.append(create_test_case(
        summary=f"[NEGATIVE] Verify transfer rejected when account has insufficient balance",
        steps="1. Enter amount exceeding available account balance\n2. Submit transfer",
        expected="System rejects transfer with error: 'Insufficient balance'",
        priority="Critical", test_type="Negative"
    ))

    test_cases.append(create_test_case(
        summary=f"[NEGATIVE] Verify mandatory fields cannot be left empty",
        steps="1. Leave all mandatory fields empty\n2. Attempt to submit",
        expected="System highlights all empty mandatory fields. Submission blocked until all fields completed.",
        priority="High", test_type="Negative"
    ))

    test_cases.append(create_test_case(
        summary=f"[NEGATIVE] Verify session timeout handling during transfer",
        steps="1. Start transfer flow\n2. Leave session idle until timeout\n3. Attempt to submit",
        expected="Session expired message shown. User redirected to login. Transaction not submitted.",
        priority="High", test_type="Security"
    ))

    # =========================================
    # SECTION 7 — RISK-BASED SCALING
    # =========================================

    if risk_level in ["HIGH", "CRITICAL"]:

        test_cases.append(create_test_case(
            summary=f"[RISK] Verify Secure2u authentication required for {module} transfer",
            steps="1. Complete transfer details\n2. Verify S2U challenge triggered\n3. Approve on S2U\n4. Submit",
            expected="S2U authentication mandatory before submission. Transfer rejected without S2U approval.",
            priority="Critical", test_type="Security"
        ))

        test_cases.append(create_test_case(
            summary=f"[RISK] Verify ledger posting accuracy after transfer completion",
            steps="1. Note account balance before transfer\n2. Complete transfer\n3. Verify balance deducted correctly",
            expected="Account balance reduced by: Principal + Service Fee + SST. Ledger entry created in core banking.",
            priority="Critical", test_type="Financial"
        ))

        test_cases.append(create_test_case(
            summary=f"[RISK] Verify data integrity — no partial transaction posting",
            steps="1. Simulate failure mid-transaction\n2. Check account balance\n3. Check transaction history",
            expected="Either full transaction posted or nothing posted. No partial deductions. Atomic transaction.",
            priority="Critical", test_type="Data Integrity"
        ))

    if risk_level == "CRITICAL":

        test_cases.append(create_test_case(
            summary=f"[RISK-CRITICAL] Verify external gateway timeout handling",
            steps="1. Simulate gateway timeout\n2. Submit transfer\n3. Check system response",
            expected="System shows timeout message. Auto-retry triggered. If retry fails, transaction rolled back.",
            priority="Critical", test_type="Error Handling"
        ))

        test_cases.append(create_test_case(
            summary=f"[RISK-CRITICAL] Verify concurrent transfer submissions handled correctly",
            steps="1. Submit same transfer simultaneously from 2 devices\n2. Check both results",
            expected="Only one transaction succeeds. System prevents double posting. Duplicate detected.",
            priority="Critical", test_type="Data Integrity"
        ))

        test_cases.append(create_test_case(
            summary=f"[RISK-CRITICAL] Verify complete audit trail for regulatory compliance",
            steps="1. Complete transfer\n2. Check audit trail log\n3. Verify all required fields captured",
            expected="Audit trail contains: user ID, timestamp, IP address, amount, recipient, reference, status, compliance checks",
            priority="Critical", test_type="Audit"
        ))

    return test_cases