import sys
import logging
import os
import json

from agents.xml_parser import parse_jira_xml
from agents.impact_engine import analyze_impact
from agents.coverage_engine import build_coverage_matrix
from agents.generator_engine import generate_test_cases
from agents.reviewer_engine import review_coverage
from agents.config_loader import load_config
from ml.risk_predictor import calculate_risk_score

ENGINE_VERSION = "1.0.0"


def setup_logging():
    base_path = os.getcwd()
    log_dir = os.path.join(base_path, "logs")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = os.path.join(log_dir, "engine.log")

    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True
    )

    logging.info("Logging initialized successfully")


def main():

    setup_logging()
    logging.info(f"AI QA Overseas Engine v{ENGINE_VERSION} started")

    if len(sys.argv) < 2:
        print("Usage: python -m app.main data/ftt.xml")
        logging.warning("No XML file provided")
        return

    xml_path = sys.argv[1]

    # =========================================
    # STEP 1 – Parse Story
    # =========================================
    story = parse_jira_xml(xml_path)
    logging.info("Story parsed successfully")

    # =========================================
    # STEP 2 – Load Configuration
    # =========================================
    config = load_config("config.yaml")

    # =========================================
    # MODULE AUTO-DETECTION
    # =========================================

    summary = story["summary"].upper()

    if config.get("module") == "AUTO":
        if "BAKONG" in summary:
            module = "BAKONG"
        elif "FTT" in summary:
            module = "FTT"
        elif "WESTERN UNION" in summary:
            module = "WESTERN_UNION"
        elif "VISA" in summary:
            module = "VISA_DIRECT"
        elif "MOT" in summary:
            module = "MOT"
        else:
            module = "UNKNOWN"
    else:
        module = config.get("module")
    logging.info(f"Channel: {config.get('channel')}")
    logging.info(f"Environment: {config.get('environment')}")
    logging.info(f"Module: {module}")

    # =========================================
    # STEP 3 – Impact Analysis
    # =========================================
    impact = analyze_impact(story)
    logging.info(f"Impact Areas: {impact}")

    # =========================================
    # STEP 4 – Risk Scoring
    # =========================================
    risk_score, risk_level, confidence = calculate_risk_score(impact, story)
    logging.info(f"Risk Score: {risk_score}")
    logging.info(f"Risk Level: {risk_level}")
    logging.info(f"Confidence: {confidence}%")

    # =========================================
    # STEP 5 – Test Case Generation
    # =========================================
    test_cases = generate_test_cases(story, impact, config)
    logging.info(f"Generated {len(test_cases)} test cases")

    # =========================================
    # STEP 6 – Coverage Review
    # =========================================
    review = review_coverage(impact, test_cases)
    logging.info(f"Coverage Score: {review['coverage_score']}")

    # =========================================
    # JSON REPORT GENERATION
    # =========================================
    if not os.path.exists("reports"):
        os.makedirs("reports")

    report_data = {
        "engine_version": ENGINE_VERSION,
        "channel": config.get("channel"),
        "environment": config.get("environment"),
        "story_summary": story["summary"],
        "priority": story["priority"],
        "word_count": story["word_count"],
        "impact_areas": impact,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "coverage_score": review["coverage_score"],
        "missing_areas": review["missing_areas"],
        "explanation": review.get("explanation", []),
        "test_cases": test_cases
    }

    with open("reports/execution_report.json", "w") as f:
        json.dump(report_data, f, indent=4)

    logging.info("Execution report generated successfully")

    # =========================================
    # OUTPUT
    # =========================================

    print("\n================================================")
    print(f"AI QA OVERSEAS ENGINE - v{ENGINE_VERSION}")
    print("================================================\n")

    print("Channel      :", config.get("channel"))
    print("Environment  :", config.get("environment"))
    print("Module       :", module)

    print("\nStory Summary :", story["summary"])
    print("Priority      :", story["priority"])
    print("Word Count    :", story["word_count"])

    print("\nDetected Impact Areas:")
    for item in impact:
        print(" -", item)

    print("\nRisk Assessment:")
    print("  Risk Score :", risk_score, "/ 100")
    print("  Risk Level :", risk_level)
    print("  Confidence :", confidence, "%")

    print("\nCoverage Quality Review:")
    print("  Coverage Score :", review["coverage_score"], "%")

    print("\nExplainability Report:")
    if review.get("explanation"):
        for exp in review["explanation"]:
            print(" -", exp)
    else:
        print(" All impact areas properly covered.")

    if review["missing_areas"]:
        print("\nMissing Areas:")
        for m in review["missing_areas"]:
            print(" -", m)
    else:
        print("\nAll critical areas covered.")

    print("\nGenerated Test Cases:")
    for tc in test_cases:
        print(" ", tc)

    print("\n------------------------------------------------\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Execution failed: {str(e)}")
        print("System Error occurred. Check logs/engine.log for details.")