import os

def scan_codebase(module_name, base_path="../banking-transfer-system/overseas"):
    """
    Scans JS files of a module and extracts technical risk signals.
    """

    module_path = os.path.join(base_path, module_name.lower())

    risk_signals = {
        "validations": 0,
        "fee_logic": 0,
        "limit_checks": 0,
        "error_handling": 0
    }

    if not os.path.exists(module_path):
        print(f"Module path not found: {module_path}")
        return risk_signals

    for root, _, files in os.walk(module_path):
        for file in files:
            if file.endswith(".js"):
                file_path = os.path.join(root, file)

                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().lower()

                    risk_signals["validations"] += content.count("validate")
                    risk_signals["fee_logic"] += content.count("fee")
                    risk_signals["limit_checks"] += content.count("limit")
                    risk_signals["error_handling"] += content.count("error")

    return risk_signals