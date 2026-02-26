import os


def scan_codebase(module_name):
    """
    Scan banking codebase and return detected risk signals.
    Works with absolute path resolution (production safe).
    """

    # -----------------------------
    # 1️⃣ Resolve absolute base path
    # -----------------------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    base_path = os.path.join(
        BASE_DIR,
        "banking-transfer-system",
        "overseas",
        module_name.lower()  # ensure lowercase match
    )

    print("Scanning module path:", base_path)

    # -----------------------------
    # 2️⃣ Initialize risk signals
    # -----------------------------
    risk_signals = {
        "validations": 0,
        "fee_logic": 0,
        "limit_checks": 0,
        "error_handling": 0
    }

    # -----------------------------
    # 3️⃣ Check path exists
    # -----------------------------
    if not os.path.exists(base_path):
        print("❌ Module path not found:", base_path)
        return risk_signals

    # -----------------------------
    # 4️⃣ Walk through JS files
    # -----------------------------
    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read().lower()

                        # Validation logic
                        if "validate" in content:
                            risk_signals["validations"] += 1

                        # Fee / SST logic
                        if "fee" in content or "sst" in content:
                            risk_signals["fee_logic"] += 1

                        # Limit checks
                        if "limit" in content:
                            risk_signals["limit_checks"] += 1

                        # Error handling
                        if "error" in content or "throw" in content:
                            risk_signals["error_handling"] += 1

                except Exception as e:
                    print(f"⚠️ Error reading {file_path}: {e}")

    # -----------------------------
    # 5️⃣ Final Output
    # -----------------------------
    print("✅ Code Risk Signals:", risk_signals)
    return risk_signals