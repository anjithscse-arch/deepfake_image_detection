import io
import random
import string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def create_analysis_report(data):
    label     = data.get("label", "FAKE")
    fake_prob = data.get("fake_prob", 0)
    real_prob = data.get("real_prob", 0)
    filename  = data.get("filename", "uploaded_image")
    buf = io.BytesIO()
    doc = SimpleDocTemplate(buf, pagesize=A4,
                            rightMargin=0.75*inch, leftMargin=0.75*inch,
                            topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = getSampleStyleSheet()
    story  = []

    def draw_hr():
        return HRFlowable(width="100%", thickness=1, color=colors.HexColor("#dddddd"), spaceBefore=10, spaceAfter=10)

    title_style = ParagraphStyle("title", parent=styles["Title"],
                                 fontSize=18, textColor=colors.HexColor("#1a1a2e"),
                                 spaceAfter=6)
    heading2_style = styles["Heading2"]
    heading3_style = styles["Heading3"]
    normal_style = styles["Normal"]
    grey_italic = ParagraphStyle("grey_italic", parent=styles["Normal"], textColor=colors.grey, fontName="Helvetica-Oblique", fontSize=9)
    bold_style = ParagraphStyle("bold", parent=styles["Normal"], fontName="Helvetica-Bold")

    # Title
    story.append(Paragraph("Deepfake Image Detection System — Analysis Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%d %B %Y, %H:%M')}", normal_style))
    story.append(Spacer(1, 0.2*inch))

    # Verdict banner
    verdict_color = colors.HexColor("#e74c3c") if label == "FAKE" else colors.HexColor("#27ae60")
    verdict_data  = [[f"VERDICT: {label}  |  Fake: {fake_prob}%  |  Real: {real_prob}%"]]
    verdict_table = Table(verdict_data, colWidths=[6.5*inch])
    verdict_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (-1,-1), verdict_color),
        ("TEXTCOLOR",   (0,0), (-1,-1), colors.white),
        ("FONTSIZE",    (0,0), (-1,-1), 13),
        ("FONTNAME",    (0,0), (-1,-1), "Helvetica-Bold"),
        ("ALIGN",       (0,0), (-1,-1), "CENTER"),
        ("TOPPADDING",  (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1), 10),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(verdict_table)
    story.append(Spacer(1, 0.2*inch))

    # Analysis table
    story.append(Paragraph("Analysis Details", heading2_style))
    analysis_data = [
        ["File",         filename],
        ["Prediction",   label],
        ["Fake Probability",  f"{fake_prob}%"],
        ["Real Probability",  f"{real_prob}%"],
        ["Model",        "EfficientNet-B0"],
        ["Input Size",   "224 × 224 px"],
    ]
    tbl = Table(analysis_data, colWidths=[2*inch, 4.5*inch])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",  (0,0), (0,-1), colors.HexColor("#f0f0f0")),
        ("FONTNAME",    (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",    (0,0), (-1,-1), 10),
        ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.HexColor("#fafafa")]),
        ("GRID",        (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ("TOPPADDING",  (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1), 6),
    ]))
    story.append(tbl)
    story.append(Spacer(1, 0.2*inch))
    story.append(draw_hr())
    story.append(Spacer(1, 0.2*inch))

    report_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    if label == "FAKE":
        # What This Means
        story.append(Paragraph("What This Means", heading2_style))
        story.append(Paragraph("This image has been identified as AI-generated or digitally manipulated by the Deepfake Image Detection System. It should not be trusted as authentic, must not be shared further, and that using it to misrepresent, defame, or harass any individual is a punishable offence under Indian law.", normal_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Legal Warning Box
        warning_data = [[Paragraph("<b>⚠️ Legal Warning Under Indian Law</b>", ParagraphStyle("w_title", textColor=colors.HexColor("#c0392b"), fontSize=11))],
                        [Paragraph("Creating, distributing, or sharing AI-manipulated images of individuals without consent is a criminal offence in India. You may be prosecuted under one or more of the following laws.", normal_style)]]
        warning_table = Table(warning_data, colWidths=[6.5*inch])
        warning_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fdecea")),
            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#e74c3c")),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ]))
        story.append(warning_table)
        story.append(Spacer(1, 0.2*inch))

        # Applicable Indian Laws Table
        story.append(Paragraph("Applicable Indian Laws", heading3_style))
        laws_data = [
            [Paragraph("<b>Law / Section</b>", normal_style), Paragraph("<b>Description</b>", normal_style), Paragraph("<b>Punishment</b>", normal_style)],
            [Paragraph("IT Act 2000 — Section 66E", normal_style), Paragraph("Violation of privacy by capturing/publishing private images", normal_style), Paragraph("Imprisonment up to 3 years or fine up to ₹2,00,000", normal_style)],
            [Paragraph("IT Act 2000 — Section 66C", normal_style), Paragraph("Identity theft using digital media", normal_style), Paragraph("Imprisonment up to 3 years + fine up to ₹1,00,000", normal_style)],
            [Paragraph("IT Act 2000 — Section 67", normal_style), Paragraph("Publishing obscene material electronically", normal_style), Paragraph("Up to 3 years + ₹5,00,000 fine (first offence)", normal_style)],
            [Paragraph("IT Act 2000 — Section 67A", normal_style), Paragraph("Publishing sexually explicit content electronically", normal_style), Paragraph("Up to 5 years + ₹10,00,000 fine", normal_style)],
            [Paragraph("IPC Section 499–500", normal_style), Paragraph("Criminal defamation using fake images", normal_style), Paragraph("Imprisonment up to 2 years", normal_style)],
            [Paragraph("IPC Section 507", normal_style), Paragraph("Criminal intimidation by anonymous communication", normal_style), Paragraph("Imprisonment up to 2 years", normal_style)],
            [Paragraph("IPC Section 354C", normal_style), Paragraph("Voyeurism / misuse of images of women", normal_style), Paragraph("1 to 3 years (first offence), up to 7 years (repeat)", normal_style)],
            [Paragraph("POCSO Act 2012", normal_style), Paragraph("If the victim is a minor", normal_style), Paragraph("Minimum 7 years to life imprisonment", normal_style)],
            [Paragraph("Protection of Women from Domestic Violence Act 2005", normal_style), Paragraph("If used as digital abuse within domestic context", normal_style), Paragraph("Civil + criminal remedies", normal_style)]
        ]
        laws_table = Table(laws_data, colWidths=[1.8*inch, 2.7*inch, 2*inch])
        laws_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f0f0")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fafafa")])
        ]))
        story.append(laws_table)
        story.append(Spacer(1, 0.2*inch))
        story.append(draw_hr())
        story.append(Spacer(1, 0.2*inch))

        # Steps to Take
        story.append(Paragraph("Steps to Take if You Are a Victim", heading3_style))
        steps = [
            "1. Do not share, repost, or engage with the fake image further.",
            "2. Take timestamped screenshots and preserve all digital evidence.",
            "3. File a complaint immediately at cybercrime.gov.in or call 1930.",
            "4. Visit your nearest police station and file an FIR under the relevant IT Act section.",
            "5. Contact NCW (National Commission for Women) at 181 if the victim is a woman.",
            "6. Use StopNCII.org to hash and block the image from spreading on partner platforms.",
            "7. Consult a cyber lawyer — Legal Services Authorities provide free aid (call 15100).",
            "8. Reach out to iCall at 9152987821 for mental health support if you are distressed."
        ]
        for step in steps:
            story.append(Paragraph(step, normal_style))
            story.append(Spacer(1, 0.05*inch))
        story.append(Spacer(1, 0.15*inch))

        # Portals Table
        story.append(Paragraph("Indian Cybercrime Reporting Portals", heading3_style))
        portals_data = [
            [Paragraph("<b>Portal / Authority</b>", normal_style), Paragraph("<b>Contact</b>", normal_style), Paragraph("<b>Purpose</b>", normal_style)],
            [Paragraph("National Cyber Crime Reporting Portal", normal_style), Paragraph("cybercrime.gov.in<br/>Helpline 1930", normal_style), Paragraph("Report all cybercrimes including deepfakes", normal_style)],
            [Paragraph("National Commission for Women (NCW)", normal_style), Paragraph("ncw.nic.in<br/>Helpline 181", normal_style), Paragraph("Support for women victims of digital abuse", normal_style)],
            [Paragraph("Cyber Dost (MHA)", normal_style), Paragraph("cyberdost.mha.gov.in<br/>@cyberdostsupport", normal_style), Paragraph("Awareness and reporting support by Ministry of Home Affairs", normal_style)],
            [Paragraph("iCall Mental Health", normal_style), Paragraph("icallhelpline.org<br/>9152987821", normal_style), Paragraph("Free psychological counselling for victims", normal_style)],
            [Paragraph("National Legal Services Authority", normal_style), Paragraph("nalsa.gov.in<br/>15100", normal_style), Paragraph("Free legal aid for cybercrime victims", normal_style)],
            [Paragraph("StopNCII", normal_style), Paragraph("stopncii.org<br/>support@stopncii.org", normal_style), Paragraph("Hash-based image blocking across platforms", normal_style)],
            [Paragraph("Internet Watch Foundation", normal_style), Paragraph("iwf.org.uk<br/>report@iwf.org.uk", normal_style), Paragraph("International image abuse reporting", normal_style)]
        ]
        portals_table = Table(portals_data, colWidths=[2*inch, 1.7*inch, 2.8*inch])
        portals_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#f0f0f0")),
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
            ("VALIGN", (0,0), (-1,-1), "TOP"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#fafafa")])
        ]))
        story.append(portals_table)
        story.append(Spacer(1, 0.2*inch))

        # Evidence Preservation Guide
        evidence_data = [[Paragraph("<b>How to Preserve Evidence for FIR</b>", normal_style)],
                         [Paragraph("Take screenshots with date/time visible. Note down URLs, usernames, and platform names. Do not delete any messages or posts related to the incident. Save this PDF report as it can serve as supporting documentation when filing a complaint. Carry a copy of this report and your Aadhaar/ID when visiting a police station.", normal_style)]]
        evidence_table = Table(evidence_data, colWidths=[6.5*inch])
        evidence_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f5f5f5")),
            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#cccccc")),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10)
        ]))
        story.append(evidence_table)
        story.append(Spacer(1, 0.2*inch))

        # Document Authenticity Note
        story.append(Paragraph("This report was automatically generated by the Deepfake Image Detection System and may be submitted as supporting documentation when filing a cybercrime complaint at cybercrime.gov.in or at a local police station. Always supplement with human expert verification for legal proceedings.", grey_italic))

    else:
        # Authenticity Statement Box
        auth_data = [[Paragraph("<b>✅ Image Authenticity Verified</b>", ParagraphStyle("a_title", textColor=colors.HexColor("#27ae60"), fontSize=11))],
                     [Paragraph("This image has been analysed by the Deepfake Image Detection System. No significant indicators of AI generation, deepfake manipulation, or digital tampering were detected at the time of analysis.", normal_style)]]
        auth_box = Table(auth_data, colWidths=[6.5*inch])
        auth_box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#eafaf1")),
            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#27ae60")),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ]))
        story.append(auth_box)
        story.append(Spacer(1, 0.2*inch))

        # What This Means
        story.append(Paragraph("What This Means", heading2_style))
        story.append(Paragraph("The image appears consistent with authentic photographic content. This report may be used as a supporting document in situations where image authenticity needs to be demonstrated — such as in legal disputes, HR investigations, academic submissions, or media verification.", normal_style))
        story.append(Spacer(1, 0.2*inch))

        # Certificate of Authenticity Block
        cert_data = [
            [Paragraph("<b>Certificate of Authenticity</b>", ParagraphStyle("c_title", fontSize=12, alignment=1))],
            [Paragraph(f"<b>Image File:</b> {filename}", normal_style)],
            [Paragraph(f"<b>Analysis Date & Time:</b> {datetime.now().strftime('%d %B %Y, %H:%M:%S')} IST", normal_style)],
            [Paragraph("<b>Model Used:</b> EfficientNet-B0 (Deepfake Image Detection System)", normal_style)],
            [Paragraph(f"<b>Authenticity Score:</b> {real_prob}%", normal_style)],
            [Paragraph("<b>Verdict:</b> AUTHENTIC — No manipulation detected", bold_style)],
            [Paragraph(f"<b>Report ID:</b> {report_id}", normal_style)]
        ]
        cert_table = Table(cert_data, colWidths=[6.5*inch])
        cert_table.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#f0fdf4")),
            ("BOX", (0,0), (-1,-1), 2, colors.HexColor("#27ae60")),
            ("ALIGN", (0,0), (0,0), "CENTER"),
            ("TOPPADDING", (0,0), (-1,-1), 6),
            ("BOTTOMPADDING", (0,0), (-1,-1), 6),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
        ]))
        story.append(cert_table)
        story.append(Spacer(1, 0.2*inch))

        # Applicable Indian Context Note
        story.append(Paragraph("Applicable Indian Context", heading3_style))
        context_data = [
            [Paragraph("Court proceedings as supplementary digital evidence", normal_style)],
            [Paragraph("Police complaints to establish image authenticity", normal_style)],
            [Paragraph("Media/journalism verification", normal_style)],
            [Paragraph("HR and workplace investigations", normal_style)],
            [Paragraph("Academic integrity checks", normal_style)]
        ]
        context_table = Table(context_data, colWidths=[6.5*inch])
        context_table.setStyle(TableStyle([
            ("GRID", (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
            ("TOPPADDING", (0,0), (-1,-1), 5),
            ("BOTTOMPADDING", (0,0), (-1,-1), 5),
            ("ROWBACKGROUNDS", (0,0), (-1,-1), [colors.white, colors.HexColor("#fafafa")])
        ]))
        story.append(context_table)
        story.append(Spacer(1, 0.2*inch))

        # Limitations Disclaimer
        story.append(Spacer(1, 0.1*inch))
        limit_data = [[Paragraph("<b>Limitations Disclaimer</b>", ParagraphStyle("lim_title", textColor=colors.HexColor("#d35400")))],
                      [Paragraph("This certificate does not constitute legal proof of authenticity under the Indian Evidence Act 1872 or the Information Technology Act 2000. AI-based detection may produce false negatives. For legal or forensic proceedings, always verify with a CERT-In empanelled digital forensics expert or a court-appointed examiner.", normal_style)]]
        limit_box = Table(limit_data, colWidths=[6.5*inch])
        limit_box.setStyle(TableStyle([
            ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#fff8e1")),
            ("BOX", (0,0), (-1,-1), 1, colors.HexColor("#f39c12")),
            ("TOPPADDING", (0,0), (-1,-1), 8),
            ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ("LEFTPADDING", (0,0), (-1,-1), 10),
            ("RIGHTPADDING", (0,0), (-1,-1), 10),
        ]))
        story.append(limit_box)
        story.append(Spacer(1, 0.2*inch))

        # Verification Footer
        story.append(draw_hr())
        story.append(Paragraph(f"Generated by Deepfake Image Detection System. Report ID: {report_id}. Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}. This document is for informational purposes only and does not replace a certified forensic examination.", grey_italic))

    doc.build(story)
    buf.seek(0)
    return buf, "detection_report.pdf"
