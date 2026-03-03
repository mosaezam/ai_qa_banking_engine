"""
AI QA Intelligence Engine — Enterprise Blueprint PDF Generator
Run: python generate_blueprint.py
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.platypus import KeepTogether
import datetime

# ─────────────────────────────────────────────────────────────────────────────
# COLOUR PALETTE
# ─────────────────────────────────────────────────────────────────────────────
DARK_BG      = colors.HexColor("#0d1117")
ACCENT_BLUE  = colors.HexColor("#2563EB")
ACCENT_CYAN  = colors.HexColor("#06B6D4")
ACCENT_GREEN = colors.HexColor("#10B981")
ACCENT_AMBER = colors.HexColor("#F59E0B")
ACCENT_RED   = colors.HexColor("#EF4444")
LIGHT_GRAY   = colors.HexColor("#F3F4F6")
MID_GRAY     = colors.HexColor("#6B7280")
DARK_GRAY    = colors.HexColor("#1F2937")
TEXT_BLACK   = colors.HexColor("#111827")
WHITE        = colors.white
TABLE_HEADER = colors.HexColor("#1E3A5F")
TABLE_ROW1   = colors.HexColor("#EFF6FF")
TABLE_ROW2   = colors.white
SECTION_BG   = colors.HexColor("#DBEAFE")


def build_styles():
    base = getSampleStyleSheet()

    styles = {}

    styles["cover_title"] = ParagraphStyle(
        "cover_title", parent=base["Title"],
        fontSize=34, textColor=WHITE, alignment=TA_CENTER,
        spaceAfter=6, fontName="Helvetica-Bold",
    )
    styles["cover_sub"] = ParagraphStyle(
        "cover_sub", parent=base["Normal"],
        fontSize=16, textColor=ACCENT_CYAN, alignment=TA_CENTER,
        spaceAfter=4, fontName="Helvetica",
    )
    styles["cover_meta"] = ParagraphStyle(
        "cover_meta", parent=base["Normal"],
        fontSize=11, textColor=colors.HexColor("#9CA3AF"), alignment=TA_CENTER,
        fontName="Helvetica",
    )
    styles["section_head"] = ParagraphStyle(
        "section_head", parent=base["Heading1"],
        fontSize=17, textColor=ACCENT_BLUE, spaceBefore=20, spaceAfter=8,
        fontName="Helvetica-Bold", borderPad=4,
    )
    styles["sub_head"] = ParagraphStyle(
        "sub_head", parent=base["Heading2"],
        fontSize=13, textColor=DARK_GRAY, spaceBefore=12, spaceAfter=6,
        fontName="Helvetica-Bold",
    )
    styles["sub_sub_head"] = ParagraphStyle(
        "sub_sub_head", parent=base["Heading3"],
        fontSize=11, textColor=ACCENT_BLUE, spaceBefore=8, spaceAfter=4,
        fontName="Helvetica-Bold",
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontSize=10, textColor=TEXT_BLACK, leading=15, fontName="Helvetica",
        spaceAfter=4,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"],
        fontSize=10, textColor=TEXT_BLACK, leading=14, fontName="Helvetica",
        leftIndent=16, spaceAfter=3,
        bulletIndent=4,
    )
    styles["code"] = ParagraphStyle(
        "code", parent=base["Code"],
        fontSize=8.5, textColor=colors.HexColor("#1E40AF"),
        backColor=colors.HexColor("#EFF6FF"),
        leftIndent=12, rightIndent=12, spaceBefore=4, spaceAfter=4,
        fontName="Courier", leading=13,
    )
    styles["table_header"] = ParagraphStyle(
        "table_header", parent=base["Normal"],
        fontSize=9, textColor=WHITE, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    styles["table_cell"] = ParagraphStyle(
        "table_cell", parent=base["Normal"],
        fontSize=9, textColor=TEXT_BLACK, fontName="Helvetica",
        leading=13,
    )
    styles["table_cell_bold"] = ParagraphStyle(
        "table_cell_bold", parent=base["Normal"],
        fontSize=9, textColor=TEXT_BLACK, fontName="Helvetica-Bold",
    )
    styles["tag_green"] = ParagraphStyle(
        "tag_green", parent=base["Normal"],
        fontSize=9, textColor=ACCENT_GREEN, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    styles["tag_red"] = ParagraphStyle(
        "tag_red", parent=base["Normal"],
        fontSize=9, textColor=ACCENT_RED, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    styles["tag_amber"] = ParagraphStyle(
        "tag_amber", parent=base["Normal"],
        fontSize=9, textColor=ACCENT_AMBER, fontName="Helvetica-Bold",
        alignment=TA_CENTER,
    )
    styles["footer"] = ParagraphStyle(
        "footer", parent=base["Normal"],
        fontSize=8, textColor=MID_GRAY, alignment=TA_CENTER, fontName="Helvetica",
    )
    styles["toc_item"] = ParagraphStyle(
        "toc_item", parent=base["Normal"],
        fontSize=10.5, textColor=ACCENT_BLUE, leading=18,
        fontName="Helvetica", leftIndent=0,
    )
    return styles


def hr(color=ACCENT_BLUE, width=1):
    return HRFlowable(width="100%", thickness=width, color=color, spaceAfter=8, spaceBefore=4)


def colored_table(data, col_widths, style_cmds=None):
    base_cmds = [
        ("BACKGROUND",  (0, 0), (-1, 0), TABLE_HEADER),
        ("TEXTCOLOR",   (0, 0), (-1, 0), WHITE),
        ("FONTNAME",    (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE",    (0, 0), (-1, 0), 9),
        ("ALIGN",       (0, 0), (-1, 0), "CENTER"),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [TABLE_ROW1, TABLE_ROW2]),
        ("GRID",        (0, 0), (-1, -1), 0.4, colors.HexColor("#CBD5E1")),
        ("FONTSIZE",    (0, 1), (-1, -1), 9),
        ("FONTNAME",    (0, 1), (-1, -1), "Helvetica"),
        ("TOPPADDING",  (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 0), (-1, 0), [TABLE_HEADER]),
    ]
    if style_cmds:
        base_cmds.extend(style_cmds)
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle(base_cmds))
    return t


def info_box(elements, style, title, lines, bg=SECTION_BG, title_color=ACCENT_BLUE):
    box_data = [[Paragraph(f"<b>{title}</b>", ParagraphStyle(
        "box_title", parent=style["body"],
        fontSize=10.5, textColor=title_color, fontName="Helvetica-Bold",
    ))]]
    for line in lines:
        box_data.append([Paragraph(line, style["body"])])
    t = Table(box_data, colWidths=[6.9 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), bg),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F0F9FF")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    elements.append(t)
    elements.append(Spacer(1, 0.12 * inch))


def build_cover(elements, style):
    # Dark cover block via a Table background
    cover_lines = [
        [Paragraph("AI QA INTELLIGENCE ENGINE", style["cover_title"])],
        [Paragraph("Enterprise Architecture &amp; Technical Blueprint", style["cover_sub"])],
        [Spacer(1, 0.12 * inch)],
        [Paragraph("Version 2.0.0  |  Confidential — For Enterprise &amp; Demo Use", style["cover_meta"])],
        [Paragraph(f"Document Date: {datetime.date.today().strftime('%B %d, %Y')}", style["cover_meta"])],
        [Spacer(1, 0.18 * inch)],
        [Paragraph("Automated. Intelligent. Governance-Ready.", ParagraphStyle(
            "tagline", parent=style["body"],
            fontSize=13, textColor=ACCENT_CYAN, alignment=TA_CENTER,
            fontName="Helvetica-BoldOblique",
        ))],
    ]
    cover = Table(cover_lines, colWidths=[6.9 * inch])
    cover.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("LEFTPADDING", (0, 0), (-1, -1), 24),
        ("RIGHTPADDING", (0, 0), (-1, -1), 24),
        ("ROUNDEDCORNERS", [6]),
    ]))
    elements.append(Spacer(1, 0.3 * inch))
    elements.append(cover)
    elements.append(Spacer(1, 0.35 * inch))

    # Executive summary box
    summary_data = [
        [Paragraph("<b>Executive Summary</b>", ParagraphStyle(
            "ex_title", parent=style["body"],
            fontSize=12, textColor=WHITE, fontName="Helvetica-Bold",
        ))],
        [Paragraph(
            "The <b>AI QA Intelligence Engine v2.0</b> is a fully automated, "
            "AI-powered test intelligence platform that ingests Jira user story XML files, "
            "analyses risk across 11 impact dimensions, scans live GitHub repositories for "
            "code-level risk signals, and generates structured test cases — complete with "
            "priority scoring, coverage analysis, compliance mapping, and governance "
            "enforcement. Built on FastAPI with a hybrid ML + rule-based risk engine, it "
            "delivers end-to-end QA intelligence from story intake to deployment gate.",
            ParagraphStyle(
                "ex_body", parent=style["body"],
                fontSize=10, textColor=colors.HexColor("#D1D5DB"),
                fontName="Helvetica", leading=15,
            )
        )],
    ]
    summary_table = Table(summary_data, colWidths=[6.9 * inch])
    summary_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1E3A5F")),
        ("BACKGROUND", (0, 1), (-1, -1), DARK_GRAY),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#374151")),
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3 * inch))

    # Key stats strip
    stats = [
        ["7", "11", "10", "4", "3"],
        ["AI Agents", "Impact Dimensions", "Domain Types", "Channels", "Export Formats"],
    ]
    stats_table = Table(stats, colWidths=[1.38 * inch] * 5)
    stats_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT_BLUE),
        ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#EFF6FF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 22),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 9),
        ("TEXTCOLOR", (0, 1), (-1, 1), DARK_GRAY),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#BFDBFE")),
    ]))
    elements.append(stats_table)
    elements.append(PageBreak())


def build_toc(elements, style):
    elements.append(Paragraph("TABLE OF CONTENTS", style["section_head"]))
    elements.append(hr())

    sections = [
        ("1", "System Architecture Overview"),
        ("2", "Agent Pipeline — 7 Agents in Detail"),
        ("    2.1", "Agent 1 — XML Parser"),
        ("    2.2", "Agent 2 — Impact Engine"),
        ("    2.3", "Agent 3 — Module Detector"),
        ("    2.4", "Agent 4 — GitHub Scanner"),
        ("    2.5", "Agent 5 — Generator Engine"),
        ("    2.6", "Agent 6 — Reviewer Engine"),
        ("    2.7", "Agent 7 — Governance Engine"),
        ("3", "ML Risk Predictor"),
        ("4", "API Endpoints Reference"),
        ("5", "Export Capabilities"),
        ("6", "AI Chat Assistant"),
        ("7", "Domain Detection Coverage"),
        ("8", "Impact Dimensions (11 Types)"),
        ("9", "Test Case Categories"),
        ("10", "Governance Decision Matrix"),
        ("11", "Technology Stack"),
        ("12", "Security & Compliance"),
        ("13", "Enterprise Roadmap"),
    ]

    for num, title in sections:
        indent = 24 if num.startswith("    ") else 0
        elements.append(Paragraph(
            f"{'&nbsp;' * (len(num) - len(num.lstrip()))}<b>{num.strip()}</b>  {title}",
            ParagraphStyle("toc", parent=style["toc_item"], leftIndent=indent)
        ))

    elements.append(PageBreak())


def build_architecture(elements, style):
    elements.append(Paragraph("1. SYSTEM ARCHITECTURE OVERVIEW", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph(
        "The engine follows a <b>sequential agent pipeline</b> architecture, where each agent "
        "is a discrete Python module with a single responsibility. Data flows through the "
        "pipeline as a dict, enriched at each stage, and ultimately rendered to the FastAPI "
        "Jinja2 dashboard. The system is stateless between requests — all state is held in "
        "<code>latest_result</code> in-memory for the active session.",
        style["body"]
    ))
    elements.append(Spacer(1, 0.12 * inch))

    # Pipeline flow table
    flow_data = [
        [Paragraph("Stage", style["table_header"]),
         Paragraph("Agent / Component", style["table_header"]),
         Paragraph("Input", style["table_header"]),
         Paragraph("Output", style["table_header"]),
         Paragraph("File", style["table_header"])],

        ["1", "XML Parser",        "Jira XML file",           "story dict",              "agents/xml_parser.py"],
        ["2", "Impact Engine",     "story dict",              "impact[] list",           "agents/impact_engine.py"],
        ["3", "Module Detector",   "story dict",              "module, channel",         "agents/module_detector.py"],
        ["4", "GitHub Scanner",    "repo_url (optional)",     "risk_signals dict",       "agents/github_scanner.py"],
        ["5", "ML Risk Predictor", "impact[], story, code_risk","risk_score, level, conf","ml/risk_predictor.py"],
        ["6", "Generator Engine",  "story + impact + risk",   "test_cases[]",            "agents/generator_engine.py"],
        ["7", "Reviewer Engine",   "impact + test_cases",     "coverage_score, gaps",    "agents/reviewer_engine.py"],
        ["8", "Governance Engine", "risk_score + coverage",   "APPROVE/REVIEW/BLOCK",    "agents/governance_engine.py"],
    ]

    col_w = [0.3*inch, 1.35*inch, 1.45*inch, 1.45*inch, 2.1*inch]
    t = colored_table(flow_data, col_w)
    elements.append(t)
    elements.append(Spacer(1, 0.15 * inch))

    info_box(elements, style, "Architecture Properties", [
        "• <b>Framework:</b> FastAPI (Python 3.12) with Jinja2 templating",
        "• <b>State:</b> In-memory (latest_result dict) — stateless per request",
        "• <b>ML Engine:</b> scikit-learn Random Forest via joblib (model.pkl + encoder.pkl)",
        "• <b>Frontend:</b> Single-page dark-theme dashboard (1300+ lines HTML/CSS/JS)",
        "• <b>Storage:</b> temp_uploads/ (UUID XML files, auto-cleaned), reports/ (exports)",
        "• <b>External API:</b> GitHub Contents API v3 (unauthenticated: 60 req/hr; token: 5000 req/hr)",
    ])
    elements.append(PageBreak())


def build_agents(elements, style):
    elements.append(Paragraph("2. AGENT PIPELINE — 7 AGENTS IN DETAIL", style["section_head"]))
    elements.append(hr())
    elements.append(Spacer(1, 0.08 * inch))

    # ── Agent 1 ──
    elements.append(Paragraph("2.1  Agent 1 — XML Parser", style["sub_head"]))
    elements.append(Paragraph(
        "Responsible for ingesting user story files and extracting structured text. "
        "Handles both well-formed and malformed XML using a two-pass strategy.",
        style["body"]
    ))
    agent1_data = [
        [Paragraph("Property", style["table_header"]), Paragraph("Detail", style["table_header"])],
        ["File",          "agents/xml_parser.py"],
        ["Entry Function","parse_jira_xml(file_path)"],
        ["Input",         "XML file path (UUID-named, saved in temp_uploads/)"],
        ["Output",        "dict: summary, description, priority, word_count"],
        ["Parser",        "xml.etree.ElementTree + BeautifulSoup (HTML cleanup)"],
        ["Jira Support",  "Detects <item> structure from Jira RSS export format"],
        ["Generic XML",   "Falls back to collecting all text nodes for any XML format"],
        ["Error Safety",  "Never crashes — returns _empty_response() on any failure"],
        ["HTML Stripping","BeautifulSoup strips HTML tags from description field"],
    ]
    elements.append(colored_table(agent1_data, [1.7*inch, 5.2*inch]))
    elements.append(Spacer(1, 0.15 * inch))

    # ── Agent 2 ──
    elements.append(Paragraph("2.2  Agent 2 — Impact Engine", style["sub_head"]))
    elements.append(Paragraph(
        "Performs keyword-based semantic analysis to identify which business impact areas "
        "are triggered by the user story. Returns a list of 0–11 impact labels.",
        style["body"]
    ))
    impact_data = [
        [Paragraph("Impact Area", style["table_header"]),
         Paragraph("Sample Trigger Keywords", style["table_header"]),
         Paragraph("Risk Weight", style["table_header"])],
        ["Financial Calculation Impact", "fee, sst, calculation, rounding, billing, tax, checkout", "HIGH"],
        ["API Contract Impact",         "api, endpoint, schema, payload, integration, rest, graphql", "HIGH"],
        ["Feature Flag Impact",         "toggle, rollout, feature flag, enable, disable, canary", "MEDIUM"],
        ["Middleware ESB Impact",       "gateway, swift, kafka, rabbitmq, retry, timeout, esb", "HIGH"],
        ["Core Banking Impact",         "debit, credit, ledger, posting, rollback, idempotent", "CRITICAL"],
        ["AML Compliance Impact",       "ofac, aml, kyc, gdpr, sanctions, bnm, pci, fatf", "CRITICAL"],
        ["Security Impact",             "auth, otp, 2fa, jwt, oauth, xss, sql injection, csrf", "HIGH"],
        ["Validation Impact",           "validate, required, mandatory, iban, format, constraint", "MEDIUM"],
        ["Limit Boundary Impact",       "limit, threshold, daily, cap, tier, exceed, quota", "MEDIUM"],
        ["Audit Trail Impact",          "audit, log, history, receipt, statement, track, record", "LOW"],
        ["UI Frontend Impact",          "screen, display, ui, modal, banner, responsive, mobile", "LOW"],
        ["High Complexity Story",       "word_count > 700 (auto-detected)", "MEDIUM"],
    ]
    elements.append(colored_table(impact_data, [2.2*inch, 3.4*inch, 1.1*inch]))
    elements.append(Spacer(1, 0.15 * inch))

    # ── Agent 3 ──
    elements.append(Paragraph("2.3  Agent 3 — Module Detector", style["sub_head"]))
    elements.append(Paragraph(
        "Detects the software domain and delivery channel from the user story text using "
        "keyword scoring. Enables domain-specific test case generation and compliance mapping.",
        style["body"]
    ))
    mod_data = [
        [Paragraph("Domain", style["table_header"]),
         Paragraph("Risk Profile", style["table_header"]),
         Paragraph("Compliance", style["table_header"]),
         Paragraph("Sample Keywords", style["table_header"])],
        ["payment",         "HIGH",     "PCI_DSS, AML, GDPR",    "payment, transfer, billing, wallet, swift"],
        ["authentication",  "HIGH",     "OWASP, GDPR",           "login, jwt, oauth, 2fa, otp, session"],
        ["security",        "CRITICAL", "OWASP, GDPR, ISO27001", "encryption, aml, vulnerability, firewall"],
        ["api_integration", "HIGH",     "—",                     "api, webhook, microservice, rest, graphql"],
        ["user_management", "MEDIUM",   "GDPR, CCPA",            "user, profile, registration, kyc"],
        ["notification",    "MEDIUM",   "—",                     "email, sms, push, alert, reminder"],
        ["reporting",       "MEDIUM",   "GDPR",                  "report, analytics, export, dashboard"],
        ["data_management", "MEDIUM",   "GDPR, CCPA",            "database, migration, sync, etl, pipeline"],
        ["ui_feature",      "LOW",      "—",                     "screen, form, layout, component, widget"],
        ["search",          "LOW",      "—",                     "search, filter, sort, pagination, index"],
    ]
    elements.append(colored_table(mod_data, [1.35*inch, 0.85*inch, 1.8*inch, 2.7*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    chan_data = [
        [Paragraph("Channel", style["table_header"]), Paragraph("Trigger Keywords", style["table_header"])],
        ["MOBILE", "mobile, android, ios, app, react native, flutter"],
        ["WEB",    "web, browser, frontend, react, angular, vue, internet banking"],
        ["API",    "api, backend, microservice, rest, graphql, integration"],
        ["CLI",    "cli, command, terminal, script, cron, batch"],
    ]
    elements.append(Paragraph("Channel Detection", style["sub_sub_head"]))
    elements.append(colored_table(chan_data, [1.2*inch, 5.5*inch]))
    elements.append(Spacer(1, 0.15 * inch))

    # ── Agent 4 ──
    elements.append(Paragraph("2.4  Agent 4 — GitHub Scanner", style["sub_head"]))
    elements.append(Paragraph(
        "Scans a live public GitHub repository for code-level risk signals using the "
        "GitHub Contents API. Analyses up to 40 source files across 16 supported languages. "
        "Risk signal counts feed directly into the ML risk score boost.",
        style["body"]
    ))
    gh_data = [
        [Paragraph("Property", style["table_header"]), Paragraph("Detail", style["table_header"])],
        ["File",              "agents/github_scanner.py"],
        ["Entry Function",    "scan_github_repo(repo_url, token=None, max_files=40)"],
        ["API Used",          "GitHub REST API v3 — /repos/{owner}/{repo}/git/trees/{branch}"],
        ["Auth",              "Optional Bearer token (PAT) for private repos or higher rate limits"],
        ["Rate Limit",        "60 req/hr (no token) | 5,000 req/hr (with token)"],
        ["Timeouts",          "Connect: 4s | Read: 8s (keeps dashboard responsive)"],
        ["Max Files",         "40 files per scan (configurable)"],
        ["Supported Langs",   ".js .ts .py .java .go .cs .rb .php .swift .kt .vue .jsx .tsx .scala .rs"],
        ["Skipped Paths",     "node_modules/, vendor/, dist/, build/, test/, migrations/, .github/"],
        ["Error Handling",    "404 → not found | 403 → rate limit | 401 → bad token | timeout → graceful"],
    ]
    elements.append(colored_table(gh_data, [1.7*inch, 5.2*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    sig_data = [
        [Paragraph("Risk Signal", style["table_header"]),
         Paragraph("Trigger Keywords (in file content)", style["table_header"]),
         Paragraph("ML Weight", style["table_header"])],
        ["validations",    "validate, validation, required, mandatory, assert, constraint", "×1"],
        ["payment_logic",  "payment, fee, charge, price, amount, billing, invoice, checkout, refund", "×3"],
        ["limit_checks",   "limit, threshold, max, minimum, quota, exceed, boundary, cap", "×2"],
        ["error_handling", "error, exception, throw, catch, fail, retry, fallback, reject", "×2"],
        ["auth_logic",     "auth, login, token, session, password, jwt, oauth, role", "×0 (context only)"],
        ["data_logic",     "database, query, insert, update, delete, transaction, sql, orm", "×0 (context only)"],
    ]
    elements.append(Paragraph("Risk Signal Detection", style["sub_sub_head"]))
    elements.append(colored_table(sig_data, [1.35*inch, 4.65*inch, 0.9*inch]))
    elements.append(Spacer(1, 0.15 * inch))

    # ── Agent 5 ──
    elements.append(Paragraph("2.5  Agent 5 — Generator Engine", style["sub_head"]))
    elements.append(Paragraph(
        "Core test case factory. Dynamically generates structured test cases based on "
        "detected impact areas and domain. Produces test cases across 10 specialized "
        "sections — always generating the core story flow, then conditionally adding "
        "impact-driven suites.",
        style["body"]
    ))
    gen_data = [
        [Paragraph("Section", style["table_header"]),
         Paragraph("Trigger Condition", style["table_header"]),
         Paragraph("# TCs", style["table_header"]),
         Paragraph("Test Types", style["table_header"])],
        ["1 — Core Story Flow",      "Always generated",                        "5",  "Functional, Audit"],
        ["2 — Financial Calculation","Financial Calculation Impact OR fee_logic>0","5", "Financial"],
        ["3 — UI Frontend",          "UI Frontend Impact",                       "3",  "UI, Layout"],
        ["4 — Feature Flag",         "Feature Flag Impact",                      "4",  "Feature Flag"],
        ["5 — API Contract",         "API Contract Impact OR validations>0",      "4",  "API"],
        ["6 — Middleware/ESB",       "Middleware ESB Impact OR error_handling>0", "3",  "Error Handling, Integration"],
        ["7 — Core Banking/Data",    "Core Banking Impact",                      "3",  "Data Integrity"],
        ["8 — Validation/Input",     "Validation Impact OR validations>0",       "4",  "Validation, Security"],
        ["9 — Limit/Boundary",       "Limit Boundary Impact OR limit_checks>0",  "3-4","Boundary"],
        ["10 — Compliance/Security", "AML/Security Impact OR PCI/AML compliance","2-4","Security, Compliance"],
    ]
    elements.append(colored_table(gen_data, [1.85*inch, 2.35*inch, 0.5*inch, 2.0*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    info_box(elements, style, "Test Case Structure (Each TC Contains)", [
        "• test_case_id (TC_001, TC_002, …)",
        "• module (domain name, uppercased)",
        "• channel (MOBILE / WEB / API / CLI)",
        "• summary (descriptive title with impact tag prefix e.g. [FIN], [SEC], [API])",
        "• priority (Critical / High / Medium / Low)",
        "• test_type (Functional / Financial / API / Validation / Security / Boundary / UI / Compliance…)",
        "• precondition (auto-generated from module + channel)",
        "• steps (numbered, multi-line)",
        "• expected_result (specific, verifiable outcome)",
    ])

    elements.append(PageBreak())

    # ── Agent 6 ──
    elements.append(Paragraph("2.6  Agent 6 — Reviewer Engine", style["sub_head"]))
    elements.append(Paragraph(
        "Performs automated QA review of the generated test suite. Scores coverage against "
        "expected impact areas using keyword matching, identifies gaps, and produces "
        "actionable recommendations.",
        style["body"]
    ))
    rev_data = [
        [Paragraph("Impact Area", style["table_header"]),
         Paragraph("Expected Keywords in TCs", style["table_header"]),
         Paragraph("Deduction if Missing", style["table_header"])],
        ["Core Banking Impact",         "debit, ledger, rollback, commit, transaction, idempotent", "-25%"],
        ["API Contract Impact",         "api, payload, response, schema, endpoint, contract",       "-20%"],
        ["Financial Calculation Impact","calculation, total, fee, rounding, payment, billing",       "-20%"],
        ["Feature Flag Impact",         "feature flag, toggle, config, flag, enabled, rollout",      "-15%"],
        ["High Complexity Story",       "boundary, limit, validation, edge case, negative",          "-20%"],
        ["No Negative Test Cases",      "(auto-detected: no 'invalid', 'reject', 'fail', 'error' TCs)","-10%"],
        ["Critical Priority Missing",   "(when risk is HIGH/CRITICAL but no Critical TCs)",          "-10%"],
    ]
    elements.append(colored_table(rev_data, [1.95*inch, 3.35*inch, 1.4*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    info_box(elements, style, "Review Outcomes", [
        "• <b>PASS:</b> coverage_score >= 80%",
        "• <b>FAIL:</b> coverage_score < 80%  (missing_areas list populated with recommendations)",
        "• <b>WEAK:</b> only 1 TC for an area when risk is HIGH/CRITICAL — partial deduction",
    ])
    elements.append(Spacer(1, 0.12 * inch))

    # ── Agent 7 ──
    elements.append(Paragraph("2.7  Agent 7 — Governance Engine", style["sub_head"]))
    elements.append(Paragraph(
        "Applies enterprise governance rules to determine deployment readiness. "
        "Acts as the final gate before a story is cleared for release.",
        style["body"]
    ))
    gov_data = [
        [Paragraph("Rule", style["table_header"]),
         Paragraph("Condition", style["table_header"]),
         Paragraph("Decision", style["table_header"]),
         Paragraph("Escalation", style["table_header"])],
        ["Rule 1 — High Risk",      "risk_score >= 75",                          "REVIEW",  "LEVEL_2 — Senior QE"],
        ["Rule 2 — Critical + PROD","risk_score == 100 AND environment == PROD",  "BLOCK",   "LEVEL_3 — Governance Board"],
        ["Rule 3 — Poor Coverage",  "coverage_score < 80%",                      "BLOCK",   "LEVEL_1"],
        ["Default — All Good",      "risk_score < 75 AND coverage >= 80%",        "APPROVE", "None"],
    ]
    elements.append(colored_table(gov_data, [1.8*inch, 2.5*inch, 1.0*inch, 1.4*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    risk_color_data = [
        [Paragraph("Risk Score", style["table_header"]),
         Paragraph("Color", style["table_header"]),
         Paragraph("Meaning", style["table_header"])],
        ["0 – 49",   "GREEN",  "Low risk — standard QA process"],
        ["50 – 74",  "YELLOW", "Medium risk — increased review recommended"],
        ["75 – 100", "RED",    "High/Critical risk — governance gate triggered"],
    ]
    elements.append(colored_table(risk_color_data, [1.2*inch, 1.2*inch, 4.3*inch]))
    elements.append(PageBreak())


def build_ml(elements, style):
    elements.append(Paragraph("3. ML RISK PREDICTOR", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph(
        "The ML Risk Predictor is a <b>hybrid engine</b> combining a trained scikit-learn "
        "Random Forest classifier with a rule-based technical code boost. "
        "The ML model provides a base risk band from story features; the code boost "
        "elevates the score based on actual source code complexity signals from GitHub.",
        style["body"]
    ))
    elements.append(Spacer(1, 0.12 * inch))

    ml_data = [
        [Paragraph("Step", style["table_header"]),
         Paragraph("Component", style["table_header"]),
         Paragraph("Detail", style["table_header"])],
        ["1 — Feature Extraction", "ML Base Features",
         "WordCount, FinancialImpact(0/1), APIImpact(0/1),\nCalculationImpact(0/1), UIImpact(0/1), PerformanceImpact(0/1)"],
        ["2 — ML Prediction",      "Random Forest (joblib)",
         "Predicts: LOW / MEDIUM / HIGH / CRITICAL\nOutputs class probabilities → confidence %"],
        ["3 — Base Score Map",     "Score Bands",
         "LOW→20 | MEDIUM→45 | HIGH→70 | CRITICAL→85"],
        ["4 — Code Boost",         "Technical Risk Signals",
         "validations×1 + payment_logic×3 + limit_checks×2 + error_handling×2\nCapped at +15 points"],
        ["5 — Final Score",        "risk_score",
         "base_score + technical_boost, capped at 100"],
        ["6 — Final Band",         "Recalculated Label",
         ">=85→CRITICAL | >=65→HIGH | >=40→MEDIUM | <40→LOW"],
    ]
    elements.append(colored_table(ml_data, [1.55*inch, 1.7*inch, 3.5*inch]))
    elements.append(Spacer(1, 0.12 * inch))

    info_box(elements, style, "ML Model Details", [
        "• <b>Algorithm:</b> Random Forest Classifier (scikit-learn)",
        "• <b>Files:</b> ml/model.pkl (classifier), ml/encoder.pkl (label encoder)",
        "• <b>Feature Count:</b> 6 fixed features — column names are immutable",
        "• <b>Confidence:</b> max(predict_proba()) × 100 — represents model certainty",
        "• <b>Boost Cap:</b> Technical boost capped at 15 to prevent all HIGH stories becoming CRITICAL",
        "• <b>Payment Logic Weight:</b> ×3 (highest) — financial code is inherently highest risk",
    ])
    elements.append(PageBreak())


def build_api(elements, style):
    elements.append(Paragraph("4. API ENDPOINTS REFERENCE", style["section_head"]))
    elements.append(hr())

    api_data = [
        [Paragraph("Method", style["table_header"]),
         Paragraph("Endpoint", style["table_header"]),
         Paragraph("Description", style["table_header"]),
         Paragraph("Auth", style["table_header"])],
        ["GET",  "/health",       "Health check — returns version 2.0.0", "None"],
        ["GET",  "/dashboard",    "Render dashboard with latest_result",  "None"],
        ["POST", "/dashboard",    "Run full analysis pipeline (XML upload + optional repo_url)", "None"],
        ["GET",  "/export/pdf",   "Export test cases as PDF",             "None"],
        ["GET",  "/export/docx",  "Export test cases as Word document",   "None"],
        ["GET",  "/export/excel", "Export test cases as Excel spreadsheet","None"],
        ["POST", "/chat",         "AI chat assistant (Claude Haiku / rule-based fallback)", "None"],
    ]
    elements.append(colored_table(api_data, [0.7*inch, 1.55*inch, 3.5*inch, 0.9*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    info_box(elements, style, "POST /dashboard — Request Fields", [
        "• <b>file</b> (multipart/form-data): Jira XML user story file",
        "• <b>repo_url</b> (form field, optional): Full GitHub URL e.g. https://github.com/owner/repo",
        "",
        "Response: Full HTML dashboard page with analysis results",
        "Side effect: Writes reports/execution_report.json (full JSON result)",
    ])
    elements.append(PageBreak())


def build_exports(elements, style):
    elements.append(Paragraph("5. EXPORT CAPABILITIES", style["section_head"]))
    elements.append(hr())

    exp_data = [
        [Paragraph("Format", style["table_header"]),
         Paragraph("Endpoint", style["table_header"]),
         Paragraph("Library", style["table_header"]),
         Paragraph("Contents", style["table_header"]),
         Paragraph("Filename", style["table_header"])],
        ["PDF",   "/export/pdf",   "ReportLab",       "All TCs with full structure", "test_cases.pdf"],
        ["Word",  "/export/docx",  "python-docx",     "All TCs with page breaks",    "test_cases.docx"],
        ["Excel", "/export/excel", "openpyxl",        "Tabular: all TC fields",      "test_cases.xlsx"],
        ["JSON",  "Auto (disk)",   "Python json",     "Full execution_report.json",  "reports/execution_report.json"],
    ]
    elements.append(colored_table(exp_data, [0.7*inch, 1.3*inch, 1.1*inch, 2.3*inch, 2.0*inch]))
    elements.append(Spacer(1, 0.12 * inch))

    info_box(elements, style, "Export Security Notes", [
        "• PDF: All fields passed through xml_escape() before ReportLab XML rendering (XSS prevention)",
        "• HTML dashboard: Jinja2 template uses {{ tc.steps | e | replace('\\n', '&lt;br&gt;') | safe }} (| e first)",
        "• Exports read from in-memory latest_result — no DB required",
    ])
    elements.append(PageBreak())


def build_chat(elements, style):
    elements.append(Paragraph("6. AI CHAT ASSISTANT", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph(
        "The chat endpoint provides an intelligent Q&amp;A interface over the current analysis. "
        "It uses <b>Claude Haiku (claude-haiku-4-5)</b> as the primary AI backend with "
        "automatic fallback to a rule-based responder when the Anthropic API key is not configured.",
        style["body"]
    ))
    elements.append(Spacer(1, 0.1 * inch))

    chat_data = [
        [Paragraph("Query Topic", style["table_header"]),
         Paragraph("Example Question", style["table_header"]),
         Paragraph("Handled By", style["table_header"])],
        ["Risk",        "What is the risk score and why?",          "Claude / fallback"],
        ["Coverage",    "What are the coverage gaps?",              "Claude / fallback"],
        ["Test Cases",  "How many test cases were generated?",      "Claude / fallback"],
        ["Impact",      "What are the detected impact areas?",      "Claude / fallback"],
        ["Governance",  "Is this story approved for deployment?",   "Claude / fallback"],
        ["GitHub",      "Why is GitHub giving a 403 error?",        "Claude / fallback"],
        ["Story",       "Tell me about the story",                  "Claude / fallback"],
        ["Suggestions", "How can I improve the test coverage?",     "Claude / fallback"],
        ["General",     "Any other question",                       "Claude (primary)"],
    ]
    elements.append(colored_table(chat_data, [1.5*inch, 2.7*inch, 2.5*inch]))
    elements.append(Spacer(1, 0.1 * inch))

    info_box(elements, style, "Chat Context Passed to Claude", [
        "Story summary, priority | Risk score and level | Coverage score and status",
        "Test case count | Impact areas | Missing coverage areas",
        "Governance decision | ML confidence | GitHub scan result (repo name, file count, errors)",
    ])
    elements.append(PageBreak())


def build_domains(elements, style):
    elements.append(Paragraph("7. DOMAIN DETECTION COVERAGE", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph(
        "The Module Detector scans the story text and assigns a domain by keyword frequency "
        "scoring. The highest-scoring domain wins. Default fallback: api_integration / WEB.",
        style["body"]
    ))
    elements.append(Spacer(1, 0.1 * inch))

    dom_data = [
        [Paragraph("Domain", style["table_header"]),
         Paragraph("Description", style["table_header"]),
         Paragraph("Risk", style["table_header"]),
         Paragraph("Compliance", style["table_header"]),
         Paragraph("Tx Limit", style["table_header"]),
         Paragraph("Daily Limit", style["table_header"])],
        ["payment",         "Payment / Financial Txn", "HIGH",     "PCI, AML, GDPR", "100,000", "500,000"],
        ["authentication",  "Auth & Authorization",    "HIGH",     "OWASP, GDPR",    "—",       "—"],
        ["security",        "Security & Compliance",   "CRITICAL", "OWASP,GDPR,ISO", "—",       "—"],
        ["api_integration", "API / Integration",       "HIGH",     "—",              "—",       "—"],
        ["user_management", "User Management",         "MEDIUM",   "GDPR, CCPA",     "—",       "—"],
        ["notification",    "Notification Service",    "MEDIUM",   "—",              "—",       "—"],
        ["reporting",       "Reporting & Analytics",   "MEDIUM",   "GDPR",           "—",       "—"],
        ["data_management", "Data Management",         "MEDIUM",   "GDPR, CCPA",     "—",       "—"],
        ["ui_feature",      "UI / Frontend Feature",   "LOW",      "—",              "—",       "—"],
        ["search",          "Search & Discovery",      "LOW",      "—",              "—",       "—"],
    ]
    elements.append(colored_table(dom_data,
        [1.15*inch, 1.55*inch, 0.75*inch, 1.25*inch, 0.9*inch, 0.9*inch]))
    elements.append(PageBreak())


def build_governance_matrix(elements, style):
    elements.append(Paragraph("10. GOVERNANCE DECISION MATRIX", style["section_head"]))
    elements.append(hr())

    matrix_data = [
        [Paragraph("Risk Score", style["table_header"]),
         Paragraph("Coverage", style["table_header"]),
         Paragraph("Environment", style["table_header"]),
         Paragraph("Decision", style["table_header"]),
         Paragraph("Escalation", style["table_header"]),
         Paragraph("Action Required", style["table_header"])],
        ["< 75",   ">= 80%", "Any",  "APPROVE", "None",    "Clear to deploy"],
        [">= 75",  ">= 80%", "Non-PROD", "REVIEW", "LEVEL_2", "Senior QE sign-off"],
        ["100",    ">= 80%", "PROD", "BLOCK",   "LEVEL_3", "Governance Board review"],
        ["Any",    "< 80%",  "Any",  "BLOCK",   "LEVEL_1", "Fix coverage gaps first"],
        [">= 75",  "< 80%",  "Any",  "BLOCK",   "LEVEL_1", "Both coverage + risk must pass"],
    ]
    elements.append(colored_table(matrix_data,
        [0.85*inch, 0.85*inch, 1.0*inch, 0.85*inch, 0.95*inch, 2.15*inch]))
    elements.append(Spacer(1, 0.12 * inch))

    info_box(elements, style, "Risk Color Thresholds", [
        "• GREEN  (score 0–49):    Low risk — standard QA process applies",
        "• YELLOW (score 50–74):   Medium risk — consider additional test coverage",
        "• RED    (score 75–100):  High/Critical risk — governance gate triggered, escalation required",
    ])
    elements.append(PageBreak())


def build_tech_stack(elements, style):
    elements.append(Paragraph("11. TECHNOLOGY STACK", style["section_head"]))
    elements.append(hr())

    tech_data = [
        [Paragraph("Layer", style["table_header"]),
         Paragraph("Technology", style["table_header"]),
         Paragraph("Purpose", style["table_header"])],
        ["Web Framework",     "FastAPI (Python 3.12)",     "REST API + HTML form handling"],
        ["Templating",        "Jinja2",                    "Server-side HTML rendering"],
        ["ML Engine",         "scikit-learn + joblib",     "Risk classification model"],
        ["Data Processing",   "pandas + numpy",            "ML feature matrix construction"],
        ["XML Parsing",       "xml.etree.ElementTree",     "User story XML ingestion"],
        ["HTML Cleanup",      "BeautifulSoup4",            "Strip HTML from Jira descriptions"],
        ["PDF Export",        "ReportLab",                 "PDF test case export"],
        ["Word Export",       "python-docx",               "DOCX test case export"],
        ["Excel Export",      "openpyxl",                  "XLSX test case export"],
        ["GitHub Integration","requests",                  "GitHub Contents API calls"],
        ["AI Chat",           "Anthropic Claude Haiku",    "Intelligent QA assistant (optional)"],
        ["Frontend",          "Vanilla JS + CSS",          "Dark-theme single-page dashboard"],
    ]
    elements.append(colored_table(tech_data, [1.6*inch, 2.1*inch, 3.0*inch]))
    elements.append(PageBreak())


def build_security(elements, style):
    elements.append(Paragraph("12. SECURITY & COMPLIANCE CONSIDERATIONS", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph("Input Security", style["sub_head"]))
    sec_items = [
        "XML files saved with UUID filenames to prevent path collision/traversal",
        "Temp files auto-deleted in a finally block after processing",
        "BeautifulSoup used to sanitise HTML content in story descriptions",
        "Jinja2 auto-escape enabled (| e) on all test case output in the dashboard",
        "xml_escape() applied to all fields before ReportLab PDF rendering",
        "Generated test cases include XSS and SQL injection test scenarios for Validation impact",
    ]
    for item in sec_items:
        elements.append(Paragraph(f"• {item}", style["bullet"]))
    elements.append(Spacer(1, 0.1 * inch))

    elements.append(Paragraph("Compliance Framework Mapping", style["sub_head"]))
    comp_data = [
        [Paragraph("Standard", style["table_header"]),
         Paragraph("Triggered For", style["table_header"]),
         Paragraph("TC Types Generated", style["table_header"])],
        ["PCI DSS",  "payment, security domains",          "Access control, data masking, secure transmission"],
        ["AML/KYC",  "AML Compliance Impact",              "Sanctions screening, declaration validation"],
        ["GDPR/CCPA","user_management, data_management",   "Data masking, consent, right-to-erasure awareness"],
        ["OWASP",    "authentication, security domains",   "Injection tests, auth bypass, session tests"],
        ["ISO 27001","security domain",                    "Encryption, access control, audit trail"],
    ]
    elements.append(colored_table(comp_data, [0.9*inch, 2.5*inch, 3.3*inch]))
    elements.append(PageBreak())


def build_roadmap(elements, style):
    elements.append(Paragraph("13. ENTERPRISE ROADMAP", style["section_head"]))
    elements.append(hr())

    elements.append(Paragraph(
        "The following features are identified for enterprise productionisation "
        "and can be scoped for phased delivery.",
        style["body"]
    ))
    elements.append(Spacer(1, 0.1 * inch))

    road_data = [
        [Paragraph("Phase", style["table_header"]),
         Paragraph("Feature", style["table_header"]),
         Paragraph("Description", style["table_header"]),
         Paragraph("Priority", style["table_header"])],
        ["1 — Core",  "Database Persistence",  "Replace in-memory state with PostgreSQL/SQLite for multi-user history", "HIGH"],
        ["1 — Core",  "Authentication",        "User login, JWT tokens, role-based access (QE / Manager / Admin)", "HIGH"],
        ["1 — Core",  "Multi-Tenancy",         "Project isolation — separate workspaces per team/project", "HIGH"],
        ["2 — Scale", "Jira Cloud API",        "Direct Jira integration — no XML export required", "MEDIUM"],
        ["2 — Scale", "GitHub Token Config",   "UI for entering GitHub PAT — removes 60 req/hr limit", "MEDIUM"],
        ["2 — Scale", "Async Processing",      "Background workers (Celery/Redis) for large repos", "MEDIUM"],
        ["2 — Scale", "ML Model Retraining",   "Feedback loop — QEs rate test cases to improve model", "MEDIUM"],
        ["3 — Enterprise", "CI/CD Plugin",     "Jenkins / GitHub Actions integration — block PRs on BLOCK decision", "HIGH"],
        ["3 — Enterprise", "Test Management",  "Export directly to Zephyr / Xray / TestRail", "HIGH"],
        ["3 — Enterprise", "Audit Dashboard",  "Full history of all story analyses with trend graphs", "MEDIUM"],
        ["3 — Enterprise", "LDAP/SSO",         "Enterprise directory integration for authentication", "LOW"],
        ["4 — AI++",  "LLM Story Writer",      "Auto-suggest story improvements for better test coverage", "LOW"],
        ["4 — AI++",  "Visual Test Recorder",  "Browser extension to record and generate UI test cases", "LOW"],
    ]
    elements.append(colored_table(road_data, [0.9*inch, 1.6*inch, 3.4*inch, 0.8*inch]))
    elements.append(Spacer(1, 0.15 * inch))

    # Closing box
    close_data = [[Paragraph(
        "<b>AI QA Intelligence Engine v2.0.0</b> — Built for teams that demand quality at speed.<br/>"
        "From story intake to governance gate, fully automated, fully auditable.",
        ParagraphStyle("close", parent=style["body"], fontSize=11,
                       textColor=WHITE, alignment=TA_CENTER, fontName="Helvetica-BoldOblique"),
    )]]
    close_table = Table(close_data, colWidths=[6.9 * inch])
    close_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), DARK_BG),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 18),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 18),
    ]))
    elements.append(close_table)


def add_page_numbers(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_GRAY)
    page_num = canvas.getPageNumber()
    canvas.drawCentredString(
        A4[0] / 2, 0.4 * inch,
        f"AI QA Intelligence Engine v2.0.0  |  Confidential  |  Page {page_num}"
    )
    canvas.restoreState()


def generate():
    output_path = "reports/AI_QA_Engine_Enterprise_Blueprint.pdf"
    import os; os.makedirs("reports", exist_ok=True)

    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.65 * inch,
        bottomMargin=0.65 * inch,
    )

    style = build_styles()
    elements = []

    build_cover(elements, style)
    build_toc(elements, style)
    build_architecture(elements, style)
    build_agents(elements, style)
    build_ml(elements, style)
    build_api(elements, style)
    build_exports(elements, style)
    build_chat(elements, style)
    build_domains(elements, style)
    build_governance_matrix(elements, style)
    build_tech_stack(elements, style)
    build_security(elements, style)
    build_roadmap(elements, style)

    doc.build(elements, onFirstPage=add_page_numbers, onLaterPages=add_page_numbers)
    print(f"\nBlueprint PDF generated: {output_path}")


if __name__ == "__main__":
    generate()
