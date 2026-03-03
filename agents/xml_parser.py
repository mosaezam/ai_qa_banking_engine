import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup


def parse_jira_xml(file_path):
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Try parsing normally first
        try:
            root = ET.fromstring(content)
        except ET.ParseError:
            # If malformed, try trimming before first "<"
            first_tag = content.find("<")
            if first_tag == -1:
                return _empty_response("No valid XML content found.")
            content = content[first_tag:]
            root = ET.fromstring(content)

        # -----------------------------
        # UNIVERSAL TEXT EXTRACTION
        # -----------------------------

        summary = ""
        description = ""
        priority = ""

        # Try common Jira RSS structure
        item = root.find(".//item")

        if item is not None:
            summary = item.findtext("title", default="")
            priority = item.findtext("priority", default="")

            description_element = item.find("description")
            if description_element is not None:
                raw_desc = ET.tostring(description_element, encoding="unicode")
                description = _clean_html(raw_desc)

        else:
            # Generic XML handling (any structure)

            # Try common tags
            summary = (
                root.findtext(".//summary")
                or root.findtext(".//title")
                or ""
            )

            priority = (
                root.findtext(".//priority")
                or ""
            )

            # Collect ALL text nodes
            all_text = []
            for elem in root.iter():
                if elem.text and elem.text.strip():
                    all_text.append(elem.text.strip())

            description = " ".join(all_text)
            description = _clean_html(description)

        if not description:
            description = "No readable description found."

        return {
            "summary": summary.strip(),
            "description": description.lower(),
            "priority": priority.strip(),
            "word_count": len(description.split())
        }

    except Exception as e:
        # NEVER crash your FastAPI app
        return _empty_response(f"XML Processing Error: {str(e)}")


# -----------------------------
# Helper Functions
# -----------------------------

def _clean_html(raw_text):
    soup = BeautifulSoup(raw_text, "html.parser")
    return soup.get_text(separator=" ").strip()


def _empty_response(message):
    return {
        "summary": "",
        "description": message.lower(),
        "priority": "",
        "word_count": 0
    }