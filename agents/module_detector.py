# ============================================================
# agents/module_detector.py
# Dynamic Module & Channel Detector — MAE Overseas Transfers
# Supports: BAKONG, FTT, MOT, WESTERNUNION, VISADIRECT, EIPO
# ============================================================

OVERSEAS_MODULES = {
    "bakong": {
        "keywords": ["bakong", "cambodia", "nbc", "khmer", "riel", "phnom penh"],
        "description": "Bakong Cross-Border Transfer (Cambodia)",
        "folder": "bakong",
        "risk_profile": "HIGH",
        "limits": {"transaction": 50000, "daily": 50000},
        "compliance": ["SST", "BNM_FX", "FATF"]
    },
    "ftt": {
        "keywords": ["ftt", "fund transfer", "ibft", "interbank", "duitnow",
                     "instant transfer", "rentas", "giro"],
        "description": "Fund Transfer & Transaction (Local Interbank)",
        "folder": "ftt",
        "risk_profile": "HIGH",
        "limits": {"transaction": 100000, "daily": 100000},
        "compliance": ["SST", "BNM_RENTAS", "FATF"]
    },
    "mot": {
        "keywords": ["mot", "maybank overseas", "overseas transfer", "telegraphic",
                     "tt transfer", "swift transfer", "wire transfer", "foreign transfer",
                     "international transfer", "remittance", "iban"],
        "description": "Maybank Overseas Transfer (MOT)",
        "folder": "mot",
        "risk_profile": "HIGH",
        "limits": {"transaction": 50000, "daily": 50000},
        "compliance": ["SST", "BNM_FX", "SWIFT", "FATF", "AML"]
    },
    "westernunion": {
        "keywords": ["western union", "wu transfer", "wu", "mtcn",
                     "cash pickup", "wu agent", "money transfer"],
        "description": "Western Union Money Transfer",
        "folder": "westernunion",
        "risk_profile": "HIGH",
        "limits": {"transaction": 10000, "daily": 10000},
        "compliance": ["SST", "BNM_FX", "OFAC", "FATF", "AML", "KYC"]
    },
    "visadirect": {
        "keywords": ["visa direct", "visa push", "visa card transfer",
                     "push payment", "card-to-card", "visa network",
                     "bin lookup", "luhn"],
        "description": "Visa Direct Push Payment",
        "folder": "visadirect",
        "risk_profile": "HIGH",
        "limits": {"transaction": 25000, "daily": 25000},
        "compliance": ["SST", "VISA_NETWORK", "PCI_DSS", "FATF"]
    },
    "eipo": {
        "keywords": ["eipo", "electronic interbank payment", "interbank payment order",
                     "swift", "bic", "sha charges", "our charges", "ben charges",
                     "charge type", "purpose code", "beneficiary bank"],
        "description": "Electronic Interbank Payment Order (EIPO)",
        "folder": "eipo",
        "risk_profile": "CRITICAL",
        "limits": {"transaction": 100000, "daily": 100000},
        "compliance": ["SST", "BNM_FX", "SWIFT_MT103", "FATF", "AML", "OFAC"]
    },
}

CHANNEL_KEYWORDS = {
    "MAE":     ["mae", "maya", "mobile", "android", "ios", "app"],
    "M2U_WEB": ["m2u", "maybank2u", "web", "browser", "internet banking"],
    "M2UBIZ":  ["m2ubiz", "business", "corporate"],
    "API":     ["api", "backend", "microservice", "integration"],
}


def detect_module(story: dict) -> str:
    text = (
        story.get("summary", "") + " " +
        story.get("description", "") + " " +
        story.get("title", "")
    ).lower()

    scores = {}
    for module, config in OVERSEAS_MODULES.items():
        score = sum(1 for kw in config["keywords"] if kw in text)
        if score > 0:
            scores[module] = score

    return max(scores, key=scores.get) if scores else "ftt"


def detect_channel(story: dict) -> str:
    text = (
        story.get("summary", "") + " " +
        story.get("description", "") + " " +
        story.get("title", "")
    ).lower()

    scores = {}
    for channel, keywords in CHANNEL_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text)
        if score > 0:
            scores[channel] = score

    return max(scores, key=scores.get) if scores else "MAE"


def detect_module_and_channel(story: dict) -> tuple:
    return detect_module(story), detect_channel(story)


def get_module_description(module: str) -> str:
    return OVERSEAS_MODULES.get(module, {}).get("description", module.upper())


def get_module_folder(module: str) -> str:
    return OVERSEAS_MODULES.get(module, {}).get("folder", module.lower())


def get_module_risk_profile(module: str) -> str:
    return OVERSEAS_MODULES.get(module, {}).get("risk_profile", "HIGH")


def get_module_compliance(module: str) -> list:
    return OVERSEAS_MODULES.get(module, {}).get("compliance", [])


def get_module_limits(module: str) -> dict:
    return OVERSEAS_MODULES.get(module, {}).get("limits", {"transaction": 50000, "daily": 50000})