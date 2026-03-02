def analyze_impact(story):

    description = story["description"].lower()
    summary = story["summary"].lower()
    text = description + " " + summary

    impact = []

    # Financial / Payment Calculation
    if any(k in text for k in [
        "sst", "fee", "total amount", "principal", "charge", "rate",
        "calculation", "rounding", "service fee", "agent fee",
        "payment", "billing", "invoice", "price", "cost", "tax",
        "discount", "refund", "checkout", "subtotal", "8%",
    ]):
        impact.append("Financial Calculation Impact")

    # API Contract
    if any(k in text for k in [
        "api", "inquiry", "response", "request", "payload", "schema",
        "contract", "endpoint", "integration", "microservice", "webhook",
        "rest", "graphql", "grpc", "http", "interface",
    ]):
        impact.append("API Contract Impact")

    # Feature Flag / Configuration
    if any(k in text for k in [
        "rmbp", "dcc", "feature flag", "toggle", "enable", "disable",
        "phase", "rollout", "flag", "config", "feature toggle",
        "ab test", "canary", "experiment", "launch darkly",
    ]):
        impact.append("Feature Flag Impact")

    # Middleware / Gateway / Integration Bus
    if any(k in text for k in [
        "esb", "gateway", "swift", "middleware", "routing", "timeout",
        "retry", "network", "mt103", "message queue", "kafka",
        "rabbitmq", "event", "broker", "bus", "connector",
    ]):
        impact.append("Middleware ESB Impact")

    # Core Banking / Data Integrity
    if any(k in text for k in [
        "debit", "credit", "core", "ledger", "posting", "balance",
        "account", "core banking", "atomic", "consistency",
        "data integrity", "rollback", "commit", "transaction",
        "idempotent", "reconcil",
    ]):
        impact.append("Core Banking Impact")

    # AML / Compliance
    if any(k in text for k in [
        "ofac", "aml", "fatf", "kyc", "compliance", "sanctions",
        "screening", "purpose code", "source of funds", "declaration",
        "bnm", "regulatory", "pci", "gdpr", "ccpa", "hipaa",
        "sox", "iso27001",
    ]):
        impact.append("AML Compliance Impact")

    # Security / Authentication
    if any(k in text for k in [
        "s2u", "secure2u", "authentication", "auth", "pci",
        "encryption", "mask", "2fa", "otp", "pin", "password",
        "jwt", "oauth", "token", "session", "xss", "sql injection",
        "csrf", "security", "vulnerability",
    ]):
        impact.append("Security Impact")

    # Validation / Input
    if any(k in text for k in [
        "validate", "validation", "invalid", "format", "mandatory",
        "required", "reject", "iban", "swift code", "bic",
        "card number", "account number", "input", "field", "form",
        "constraint", "rule",
    ]):
        impact.append("Validation Impact")

    # Limit / Boundary
    if any(k in text for k in [
        "limit", "threshold", "maximum", "minimum", "daily", "exceed",
        "boundary", "cap", "tier", "segment", "quota",
        "rate limit", "throttle",
    ]):
        impact.append("Limit Boundary Impact")

    # Audit Trail
    if any(k in text for k in [
        "audit", "trail", "log", "history", "statement", "reference",
        "record", "report", "receipt", "transaction history",
        "track", "monitor", "event log",
    ]):
        impact.append("Audit Trail Impact")

    # UI / Frontend
    if any(k in text for k in [
        "screen", "display", "tooltip", "label", "ui", "frontend",
        "page", "field", "confirmation", "receipt page", "banner",
        "modal", "button", "form", "layout", "responsive",
        "mobile", "accessibility",
    ]):
        impact.append("UI Frontend Impact")

    # Complexity
    if story["word_count"] > 700:
        impact.append("High Complexity Story")

    return impact
