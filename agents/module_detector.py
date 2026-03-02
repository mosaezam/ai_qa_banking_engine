# ============================================================
# agents/module_detector.py
# Generic Domain & Channel Detector — works for any project
# Detects: payment, authentication, user_management, api_integration,
#          notification, reporting, data_management, security,
#          ui_feature, search
# ============================================================

SOFTWARE_DOMAINS = {
    "payment": {
        "keywords": [
            "payment", "transfer", "transaction", "checkout", "billing",
            "invoice", "fee", "charge", "wallet", "refund", "subscription",
            "order", "cart", "banking", "overseas", "wire", "swift",
            "remittance", "fintech", "debit", "credit", "bank",
        ],
        "description": "Payment / Financial Transaction",
        "risk_profile": "HIGH",
        "limits": {"transaction": 100000, "daily": 500000},
    },
    "authentication": {
        "keywords": [
            "login", "logout", "auth", "jwt", "oauth", "session",
            "password", "token", "sso", "2fa", "otp", "mfa",
            "credential", "signup", "register", "forgot password",
            "reset password", "secure2u", "s2u",
        ],
        "description": "Authentication & Authorization",
        "risk_profile": "HIGH",
        "limits": {"attempts": 5, "session_timeout": 3600},
    },
    "user_management": {
        "keywords": [
            "user", "profile", "account", "registration", "customer",
            "member", "kyc", "onboarding", "identity", "personal",
            "preferences", "settings",
        ],
        "description": "User Management",
        "risk_profile": "MEDIUM",
        "limits": {},
    },
    "api_integration": {
        "keywords": [
            "api", "integration", "webhook", "endpoint", "microservice",
            "service", "connector", "bridge", "third-party", "external",
            "rest", "graphql", "soap", "http", "grpc", "esb",
        ],
        "description": "API / Integration",
        "risk_profile": "HIGH",
        "limits": {},
    },
    "notification": {
        "keywords": [
            "notification", "email", "sms", "push", "alert", "message",
            "broadcast", "reminder", "inbox", "template",
        ],
        "description": "Notification Service",
        "risk_profile": "MEDIUM",
        "limits": {},
    },
    "reporting": {
        "keywords": [
            "report", "analytics", "dashboard", "export", "statement",
            "summary", "audit", "log", "history", "chart", "graph",
            "metrics", "kpi", "receipt",
        ],
        "description": "Reporting & Analytics",
        "risk_profile": "MEDIUM",
        "limits": {},
    },
    "data_management": {
        "keywords": [
            "data", "database", "import", "migration", "backup",
            "sync", "storage", "record", "archive", "etl", "pipeline",
        ],
        "description": "Data Management",
        "risk_profile": "MEDIUM",
        "limits": {},
    },
    "security": {
        "keywords": [
            "security", "encryption", "compliance", "gdpr", "aml", "kyc",
            "pci", "vulnerability", "patch", "firewall",
            "ofac", "fatf", "sanctions", "penetration",
        ],
        "description": "Security & Compliance",
        "risk_profile": "CRITICAL",
        "limits": {},
    },
    "ui_feature": {
        "keywords": [
            "ui", "screen", "page", "form", "display", "layout", "design",
            "frontend", "component", "button", "modal", "widget",
            "dropdown", "responsive", "accessibility", "banner", "tooltip",
        ],
        "description": "UI / Frontend Feature",
        "risk_profile": "LOW",
        "limits": {},
    },
    "search": {
        "keywords": [
            "search", "filter", "sort", "query", "lookup", "find",
            "list", "browse", "pagination", "facet", "index",
        ],
        "description": "Search & Discovery",
        "risk_profile": "LOW",
        "limits": {},
    },
}

CHANNEL_KEYWORDS = {
    "MOBILE": [
        "mobile", "android", "ios", "app", "tablet",
        "react native", "flutter",
    ],
    "WEB": [
        "web", "browser", "frontend", "react", "angular", "vue",
        "html", "css", "internet banking", "online portal",
    ],
    "API": [
        "api", "backend", "microservice", "service",
        "rest", "graphql", "integration",
    ],
    "CLI": ["cli", "command", "terminal", "script", "cron", "batch", "job"],
}

_COMPLIANCE_MAP = {
    "payment":         ["PCI_DSS", "AML", "GDPR"],
    "authentication":  ["OWASP", "GDPR"],
    "security":        ["OWASP", "GDPR", "ISO27001", "PCI_DSS"],
    "user_management": ["GDPR", "CCPA"],
    "data_management": ["GDPR", "CCPA"],
    "reporting":       ["GDPR"],
}


def detect_module(story: dict) -> str:
    text = (
        story.get("summary", "") + " " +
        story.get("description", "") + " " +
        story.get("title", "")
    ).lower()

    scores = {}
    for domain, config in SOFTWARE_DOMAINS.items():
        score = sum(1 for kw in config["keywords"] if kw in text)
        if score > 0:
            scores[domain] = score

    return max(scores, key=scores.get) if scores else "api_integration"


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

    return max(scores, key=scores.get) if scores else "WEB"


def detect_module_and_channel(story: dict) -> tuple:
    return detect_module(story), detect_channel(story)


def get_module_description(module: str) -> str:
    return SOFTWARE_DOMAINS.get(module, {}).get(
        "description",
        module.replace("_", " ").title()
    )


def get_module_folder(module: str) -> str:
    return module.lower()


def get_module_risk_profile(module: str) -> str:
    return SOFTWARE_DOMAINS.get(module, {}).get("risk_profile", "MEDIUM")


def get_module_compliance(module: str) -> list:
    return _COMPLIANCE_MAP.get(module, [])


def get_module_limits(module: str) -> dict:
    return SOFTWARE_DOMAINS.get(module, {}).get("limits", {})
