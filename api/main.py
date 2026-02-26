from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import shutil
import os
import json

from agents.xml_parser import parse_jira_xml
from agents.code_scanner import scan_codebase
from agents.impact_engine import analyze_impact
from agents.generator_engine import generate_test_cases
from agents.reviewer_engine import review_coverage
from agents.config_loader import load_config
from ml.risk_predictor import calculate_risk_score
from agents.governance_engine import apply_governance_rules, get_risk_color

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from docx import Document
from openpyxl import Workbook


app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Store latest result (in-memory for dashboard)
latest_result = {"test_cases": []}


# ============================
# GET DASHBOARD
# ============================
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    return templates.TemplateResponse("dashboard.html", {
        "request": request
    })


# ============================
# POST → RUN ENGINE
# ============================
@app.post("/dashboard")
async def analyze_dashboard(request: Request, file: UploadFile = File(...)):
    global latest_result

    os.makedirs("reports", exist_ok=True)

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run engine
    story = parse_jira_xml(temp_path)
    config = load_config("config.yaml")
    impact = analyze_impact(story)

    module_name = "bakong" if "bakong" in story["summary"].lower() else "ftt"
    code_risk = scan_codebase(module_name)

    risk_score, risk_level, confidence = calculate_risk_score(impact, story, code_risk)
    risk_color = get_risk_color(risk_score)

    test_cases = generate_test_cases(
        story,
        impact,
        config,
        code_risk,
        risk_score,
        risk_level
    )

    review = review_coverage(impact, test_cases)

    governance = apply_governance_rules(
        risk_score=risk_score,
        coverage_score=review["coverage_score"],
        environment=config.get("environment")
    )

    os.remove(temp_path)

    # ============================
    # SAVE EXECUTION REPORT
    # ============================
    latest_result = {
        "engine_version": "1.0.0",
        "channel": "MAE",
        "environment": config.get("environment"),
        "story_summary": story["summary"],
        "priority": story.get("priority", "Medium"),
        "word_count": story["word_count"],
        "impact_areas": impact,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_color": risk_color,
        "confidence": confidence,
        "coverage_score": review["coverage_score"],
        "missing_areas": review["missing_areas"],
        "explanation": review["explanation"],
        "governance_decision": governance.get("decision", "REVIEW"),
        "test_cases": test_cases
    }

    with open("reports/execution_report.json", "w") as f:
        json.dump(latest_result, f, indent=4)

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        **latest_result
    })


# ============================
# EXPORT PDF
# ============================
@app.get("/export/pdf")
def export_pdf():
    if not latest_result.get("test_cases"):
        return {"error": "No test cases available"}

    os.makedirs("reports", exist_ok=True)
    file_path = "reports/test_cases.pdf"

    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Generated Test Cases</b>", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    for tc in latest_result["test_cases"]:
        content = f"""
        <b>{tc['test_case_id']} - {tc['summary']}</b><br/>
        Module: {tc['module']} | Channel: {tc['channel']} | Priority: {tc['priority']} | Type: {tc['test_type']}<br/>
        <b>Precondition:</b> {tc['precondition']}<br/>
        <b>Steps:</b> {tc['steps']}<br/>
        <b>Expected:</b> {tc['expected_result']}<br/><br/>
        """

        elements.append(Paragraph(content, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return FileResponse(file_path, media_type="application/pdf", filename="test_cases.pdf")


# ============================
# EXPORT DOCX
# ============================
@app.get("/export/docx")
def export_docx():
    if not latest_result.get("test_cases"):
        return {"error": "No test cases available"}

    os.makedirs("reports", exist_ok=True)
    file_path = "reports/test_cases.docx"

    document = Document()
    document.add_heading("Generated Test Cases", level=1)

    for tc in latest_result["test_cases"]:
        document.add_heading(f"{tc['test_case_id']} - {tc['summary']}", level=2)
        document.add_paragraph(f"Module: {tc['module']}")
        document.add_paragraph(f"Channel: {tc['channel']}")
        document.add_paragraph(f"Priority: {tc['priority']}")
        document.add_paragraph(f"Type: {tc['test_type']}")
        document.add_paragraph("Precondition:")
        document.add_paragraph(tc["precondition"])
        document.add_paragraph("Steps:")
        document.add_paragraph(tc["steps"])
        document.add_paragraph("Expected Result:")
        document.add_paragraph(tc["expected_result"])
        document.add_page_break()

    document.save(file_path)

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename="test_cases.docx"
    )


# ============================
# EXPORT EXCEL
# ============================
@app.get("/export/excel")
def export_excel():
    if not latest_result.get("test_cases"):
        return {"error": "No test cases available"}

    os.makedirs("reports", exist_ok=True)
    file_path = "reports/test_cases.xlsx"

    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    headers = [
        "Test Case ID",
        "Module",
        "Channel",
        "Summary",
        "Priority",
        "Test Type",
        "Precondition",
        "Steps",
        "Expected Result"
    ]

    ws.append(headers)

    for tc in latest_result["test_cases"]:
        ws.append([
            tc["test_case_id"],
            tc["module"],
            tc["channel"],
            tc["summary"],
            tc["priority"],
            tc["test_type"],
            tc["precondition"],
            tc["steps"],
            tc["expected_result"],
        ])

    wb.save(file_path)

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="test_cases.xlsx"
    )