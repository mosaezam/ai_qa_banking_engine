def generate_test_cases(story, impact, config):

    test_cases = []
    tc_id = 1

    def add_case(description):
        nonlocal tc_id
        test_cases.append(f"TC{tc_id:03d} - {description}")
        tc_id += 1

    channel = config.get("channel", "MAE")

    # =====================================================
    # CHANNEL LOGIC
    # =====================================================

    # -----------------------
    # 🟢 MAE (RMBP + DCC)
    # -----------------------
    if channel == "MAE":

        # ONLINE (RMBP=ON + DCC=ON)
        add_case("[MAE ONLINE] Verify frontend allows transaction when RMBP=ON")
        add_case("[MAE ONLINE] Verify backend propagates SST when DCC=ON")
        add_case("[MAE ONLINE] Verify SST calculated correctly at configured percentage")
        add_case("[MAE ONLINE] Verify total amount = principal + fee + SST")

        # Middleware
        add_case("[MAE ONLINE] Verify ESB payload contains SST")
        add_case("[MAE ONLINE] Verify CICS maps SST correctly")

        # Core Banking
        add_case("[MAE ONLINE] Verify core banking deducts total including SST")
        add_case("[MAE ONLINE] Verify debit-credit reconciliation in core banking")

        # API
        add_case("[MAE ONLINE] Validate API request includes SST field")
        add_case("[MAE ONLINE] Validate API response reflects updated fee structure")

        # Control systems
        add_case("[MAE ONLINE] Verify CCPP reflects SST component correctly")
        add_case("[MAE ONLINE] Verify RSA CQ/Deny/Review flow unaffected")

        # OFFLINE (RMBP=OFF + DCC=OFF)
        add_case("[MAE OFFLINE] Verify frontend hides SST when RMBP=OFF")
        add_case("[MAE OFFLINE] Verify backend suppresses SST when DCC=OFF")
        add_case("[MAE OFFLINE] Verify no SST calculated")
        add_case("[MAE OFFLINE] Verify total amount excludes SST")

        # Middleware
        add_case("[MAE OFFLINE] Verify ESB payload excludes SST")
        add_case("[MAE OFFLINE] Verify CICS does not map SST")

        # Core Banking
        add_case("[MAE OFFLINE] Verify core banking deducts without SST")
        add_case("[MAE OFFLINE] Verify debit-credit reconciliation without SST")

        # API
        add_case("[MAE OFFLINE] Validate API request excludes SST field")
        add_case("[MAE OFFLINE] Validate API response excludes SST structure")

    # -----------------------
    # 🔵 M2U (DCC Only)
    # -----------------------
    elif channel == "M2U":

        # ONLINE (DCC=ON)
        add_case("[M2U ONLINE] Verify frontend displays SST when DCC=ON")
        add_case("[M2U ONLINE] Verify backend propagates SST when DCC=ON")
        add_case("[M2U ONLINE] Verify SST calculated correctly")
        add_case("[M2U ONLINE] Verify total amount includes SST")

        # Middleware
        add_case("[M2U ONLINE] Verify ESB payload contains SST")
        add_case("[M2U ONLINE] Verify CICS maps SST correctly")

        # Core Banking
        add_case("[M2U ONLINE] Verify core banking deducts total including SST")
        add_case("[M2U ONLINE] Verify debit-credit reconciliation in core banking")

        # API
        add_case("[M2U ONLINE] Validate API request includes SST field")
        add_case("[M2U ONLINE] Validate API response reflects updated fee structure")

        # OFFLINE (DCC=OFF)
        add_case("[M2U OFFLINE] Verify frontend hides SST when DCC=OFF")
        add_case("[M2U OFFLINE] Verify backend suppresses SST when DCC=OFF")
        add_case("[M2U OFFLINE] Verify no SST calculated")
        add_case("[M2U OFFLINE] Verify total amount excludes SST")

        # Middleware
        add_case("[M2U OFFLINE] Verify ESB payload excludes SST")
        add_case("[M2U OFFLINE] Verify CICS does not map SST")

        # Core Banking
        add_case("[M2U OFFLINE] Verify core banking deducts without SST")
        add_case("[M2U OFFLINE] Verify debit-credit reconciliation without SST")

        # API
        add_case("[M2U OFFLINE] Validate API request excludes SST field")
        add_case("[M2U OFFLINE] Validate API response excludes SST structure")

    # =====================================================
    # COMMON VALIDATIONS
    # =====================================================

    add_case("Verify minimum transfer boundary amount")
    add_case("Verify maximum transfer boundary amount")
    add_case("Verify invalid amount scenario")
    add_case("Verify invalid currency scenario")
    add_case("Verify concurrent transactions handled correctly")
    add_case("Verify performance under peak load")

    return test_cases