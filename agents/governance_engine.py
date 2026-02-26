def get_risk_color(risk_score):
    if risk_score < 50:
        return "GREEN"
    elif risk_score < 75:
        return "YELLOW"
    else:
        return "RED"


def apply_governance_rules(risk_score, coverage_score, environment):

    # 🔹 Calculate color inside governance
    risk_color = get_risk_color(risk_score)

    approval_required = None
    release_status = "APPROVED"
    escalation_level = None

    # Rule 1: High or Critical Risk requires Senior QE Approval
    if risk_score >= 75:
        approval_required = "Senior QE Approval Required"
        escalation_level = "LEVEL_2"

    # Rule 2: Critical Risk in PROD requires Governance Board Review
    if risk_score == 100 and environment == "PROD":
        approval_required = "Governance Board Approval Required"
        escalation_level = "LEVEL_3"
        release_status = "BLOCKED"

    # Rule 3: Poor Coverage blocks release
    if coverage_score < 80:
        release_status = "BLOCKED"
        escalation_level = "LEVEL_1"

    # Decision logic for dashboard
    if release_status == "BLOCKED":
        decision = "BLOCK"
    elif approval_required:
        decision = "REVIEW"
    else:
        decision = "APPROVE"

    return {
        "decision": decision,
        "risk_color": risk_color,
        "approval_required": approval_required,
        "release_status": release_status,
        "escalation_level": escalation_level
    }