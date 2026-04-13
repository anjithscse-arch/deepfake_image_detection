import sys

with open("app.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith("@app.route(\"/generate_report\""):
        start_idx = i
    if line.startswith("if __name__ == \"__main__\":"):
        end_idx = i
        break

pdf_code = lines[start_idx+1:end_idx] # from def generate_report(): to end
# We need to construct pdf_generator.py
imports = """import io
import random
import string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def create_analysis_report(data):
"""

pdf_body = []
started_body = False
for line in pdf_code:
    if line.strip() == "buf = io.BytesIO()":
        started_body = True
    
    if line.strip() == "return send_file(buf, mimetype=\"application/pdf\",":
        pdf_body.append("    return buf, \"detection_report.pdf\"\n")
        break
    elif line.strip() == "as_attachment=True, download_name=\"detection_report.pdf\")":
        pass
    else:
        if line.startswith("    import io") or line.startswith("    from "):
            continue
        if started_body or line.strip().startswith("label") or line.strip().startswith("fake_prob") or line.strip().startswith("real_prob") or line.strip().startswith("filename"):
            pdf_body.append(line)

with open("pdf_generator.py", "w", encoding="utf-8") as f:
    f.write(imports + "".join(pdf_body))

new_app_code = lines[:start_idx] + [
    "from pdf_generator import create_analysis_report\n\n",
    "@app.route(\"/generate_report\", methods=[\"POST\"])\n",
    "def generate_report():\n",
    "    data = request.json\n",
    "    buf, download_name = create_analysis_report(data)\n",
    "    return send_file(buf, mimetype=\"application/pdf\", as_attachment=True, download_name=download_name)\n\n"
] + lines[end_idx:]

# Remove old imports from the top if any? Wait, in app.py we still have io, random?
# random and io are not removed but that's fine.

with open("app.py", "w", encoding="utf-8") as f:
    f.writelines(new_app_code)

print("Refactor complete.")
