import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

def parse_jira_xml(file_path):

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    # Find real XML start
    start_index = content.find("<rss")
    if start_index == -1:
        raise ValueError("No <rss> root found")

    xml_content = content[start_index:]
    root = ET.fromstring(xml_content)

    item = root.find(".//item")
    if item is None:
        raise ValueError("No <item> found")

    # Title (Jira RSS uses <title>)
    summary = item.find("title").text if item.find("title") is not None else ""

    # Extract FULL description including nested HTML
    description_element = item.find("description")
    description_raw = ET.tostring(description_element, encoding="unicode") if description_element is not None else ""

    # Clean HTML
    soup = BeautifulSoup(description_raw, "html.parser")
    description = soup.get_text(separator=" ").lower()

    priority = item.findtext("priority", default="")

    return {
        "summary": summary,
        "description": description,
        "priority": priority,
        "word_count": len(description.split())
    }