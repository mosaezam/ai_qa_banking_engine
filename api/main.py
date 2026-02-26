from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_303_SEE_OTHER
import shutil
import os

from agents.xml_parser import parse_jira_xml
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

# Store latest result (demo purpose)
latest_result = None


# ============================
# GET DASHBOARD (Always Clean)
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

    temp_path = f"temp_{file.filename}"

    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Run engine
    story = parse_jira_xml(temp_path)
    config = load_config("config.yaml")
    impact = analyze_impact(story)

    risk_score, risk_level, confidence = calculate_risk_score(impact, story)
    risk_color = get_risk_color(risk_score)

    test_cases = generate_test_cases(story, impact, config)
    review = review_coverage(impact, test_cases)

    governance = apply_governance_rules(
        risk_score=risk_score,
        coverage_score=review["coverage_score"],
        environment=config.get("environment")
    )

    os.remove(temp_path)

    # Save result
    latest_result = {
        "story_summary": story["summary"],
        "risk_score": risk_score,
        "risk_level": risk_level,
        "risk_color": governance.get("risk_color", risk_color),
        "confidence": confidence,
        "coverage_score": review["coverage_score"],
        "governance_decision": governance.get("decision", "REVIEW"),
        "impact_areas": impact,
        "test_cases": test_cases
    }

    # Show result directly (NO redirect)
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        **latest_result
    })


# ============================
# EXPORT PDF
# ============================
@app.get("/export/pdf")
def export_pdf():
    global latest_result

    if not latest_result:
        return {"error": "No test cases available"}

    file_path = "test_cases.pdf"
    doc = SimpleDocTemplate(file_path)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("<b>Generated Test Cases</b>", styles["Heading1"]))
    elements.append(Spacer(1, 0.3 * inch))

    for tc in latest_result["test_cases"]:
        elements.append(Paragraph(tc, styles["Normal"]))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    return FileResponse(file_path, media_type="application/pdf", filename="test_cases.pdf")


# ============================
# EXPORT DOCX
# ============================
@app.get("/export/docx")
def export_docx():
    global latest_result

    if not latest_result:
        return {"error": "No test cases available"}

    file_path = "test_cases.docx"
    document = Document()
    document.add_heading("Generated Test Cases", level=1)

    for tc in latest_result["test_cases"]:
        document.add_paragraph(tc)

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
    global latest_result

    if not latest_result:
        return {"error": "No test cases available"}

    file_path = "test_cases.xlsx"
    wb = Workbook()
    ws = wb.active
    ws.title = "Test Cases"

    ws.append(["Test Case"])

    for tc in latest_result["test_cases"]:
        ws.append([tc])

    wb.save(file_path)

    return FileResponse(
        file_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="test_cases.xlsx"
    )