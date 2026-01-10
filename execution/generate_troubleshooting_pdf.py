#!/usr/bin/env python3
"""
Generate a professional PDF document for Oil Tank Transfer Box troubleshooting guide.
Uses reportlab for PDF generation.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

def create_troubleshooting_pdf(output_path):
    """Generate the troubleshooting PDF document."""

    # Create the PDF document
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    # Container for PDF elements
    story = []

    # Get styles
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a1a1a'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    heading1_style = ParagraphStyle(
        'CustomHeading1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )

    heading2_style = ParagraphStyle(
        'CustomHeading2',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=10,
        spaceBefore=15,
        fontName='Helvetica-Bold'
    )

    heading3_style = ParagraphStyle(
        'CustomHeading3',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )

    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['BodyText'],
        fontSize=10,
        leftIndent=20,
        spaceAfter=4,
        fontName='Helvetica'
    )

    # Title page
    story.append(Paragraph("Oil Tank Transfer Box", title_style))
    story.append(Paragraph("Troubleshooting Guide", title_style))
    story.append(Spacer(1, 0.3*inch))

    # Metadata
    metadata = f"""
    <para align=center>
    <b>PLC Program #3201</b><br/>
    Schneider Electric Zelio Logic SR3B261FU<br/>
    Generated: {datetime.now().strftime('%B %d, %Y')}<br/>
    </para>
    """
    story.append(Paragraph(metadata, body_style))
    story.append(Spacer(1, 0.5*inch))

    # Problem statement
    problem_box = Paragraph(
        "<b>THE PROBLEM:</b> System works in Manual mode but fails in Automatic mode.",
        ParagraphStyle('ProblemBox', parent=body_style, backColor=colors.HexColor('#ffe6e6'),
                      borderPadding=10, fontSize=12, fontName='Helvetica-Bold')
    )
    story.append(problem_box)
    story.append(Spacer(1, 0.3*inch))

    story.append(PageBreak())

    # PHASE 1
    story.append(Paragraph("PHASE 1: Power & Hardware Check", heading1_style))
    story.append(Paragraph("What to verify:", heading3_style))

    phase1_items = [
        "Main module: <b>SR3B261FU</b> (100-240V AC supply)",
        "Expansion module: <b>SR3XT141FU</b>",
        "PLC cycle time: <b>20ms</b> (RUN light should be solid green)",
        "System clock accurate (for Daylight Saving logic)"
    ]
    for item in phase1_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph("<b>Action:</b> Verify power supply voltage and physical bus connection between modules.", body_style))
    story.append(Spacer(1, 0.3*inch))

    # PHASE 2
    story.append(Paragraph("PHASE 2: Critical Input Signals", heading1_style))
    story.append(Paragraph("These are your \"gatekeepers\" - if they fail, the system won't start.", body_style))
    story.append(Spacer(1, 0.1*inch))

    # Priority 1
    story.append(Paragraph("Priority 1: Input IL (System Ready)", heading2_style))
    priority1_items = [
        "<b>Most critical input</b> - appears in rungs 1, 3, 4, 6, 7, 9, 19",
        "Controls relay <b>M1</b> which gates both pumps Q1 and Q2",
        "<b>Test:</b> Use multimeter to verify signal at terminal IL",
        "<b>Fault Code:</b> FAULT: NO-RDY if M1 is OFF"
    ]
    for item in priority1_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))

    # Priority 2
    story.append(Paragraph("Priority 2: Directional Inputs (ID & IE)", heading2_style))
    priority2_items = [
        "<b>ID:</b> Triggers Tank A transfer (controls relay M4)",
        "<b>IE:</b> Triggers Tank B transfer (controls relay M5)",
        "<b>Test:</b> Check continuity on float switches",
        "<b>Fault Code:</b> BLOCK: DIR if both M4 and M5 are OFF"
    ]
    for item in priority2_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))

    # Note on filtering
    story.append(Paragraph("Note on Input Filtering:", heading3_style))
    filtering_items = [
        "System uses <b>3ms \"Slow\" filtering</b>",
        "Flickering sensors faster than 3ms will be ignored by PLC",
        "May cause intermittent failures if sensors are vibrating"
    ]
    for item in filtering_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # PHASE 3
    story.append(Paragraph("PHASE 3: Valve Timing & Sequencing", heading1_style))
    story.append(Paragraph("The 1.5-Second Window:", heading2_style))
    story.append(Paragraph(
        "Critical timers <b>T9</b> and <b>TA</b> are set to <b>1.5 seconds</b>. "
        "Valves must open fully within this window or pumps will shut down.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Test procedure:", heading3_style))
    test_items = [
        "Trigger a transfer in Auto mode",
        "Verify solenoids <b>Q6</b> (Pump 1) or <b>Q7</b> (Pump 2) fire immediately",
        "Measure time between valve opening and pump starting",
        "If time exceeds 1.5s → <b>TIMEOUT FAULT</b>"
    ]
    for i, item in enumerate(test_items, 1):
        story.append(Paragraph(f"{i}. {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Fault Codes:", heading3_style))
    fault_items = [
        "<b>FAULT: T-OUT 9</b> - Timer T9 expired, Pump Q1 blocked (check Q6 valve or feedback sensor IF)",
        "<b>FAULT: T-OUT A</b> - Timer TA expired, Pump Q2 blocked (check Q7 valve or feedback sensor IG)"
    ]
    for item in fault_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.3*inch))

    # PHASE 4
    story.append(Paragraph("PHASE 4: Safety Interlocks", heading1_style))

    story.append(Paragraph("Relay M3 (Safety Interlock)", heading2_style))
    m3_items = [
        "Prevents system from starting if conflicting outputs are active",
        "<b>Blocked if:</b> Any of q6, q7, q8 are stuck ON simultaneously",
        "<b>Test:</b> Monitor that no valves are stuck in active state",
        "<b>Fault Code:</b> BLOCK: SAFE if M3 is OFF"
    ]
    for item in m3_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Relay M6 (Emergency Stop)", heading2_style))
    m6_items = [
        "Acts as normally closed contact in pump circuit",
        "<b>If M6 activates</b> → breaks circuit and stops both pumps",
        "Often linked to E-Stop button or thermal overload"
    ]
    for item in m6_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # Quick Fault Diagnosis Table
    story.append(Paragraph("Quick Fault Diagnosis", heading1_style))

    fault_data = [
        ['Symptom', 'Likely Cause', 'Check This'],
        ['Pump won\'t start in Auto', 'Input IL open/flickering', 'Terminal IL voltage'],
        ['Pump starts then stops', '1.5s timer expired', 'Valves Q6/Q7 actuation speed'],
        ['No direction selected', 'Float switches failed', 'Inputs ID and IE continuity'],
        ['System "locked"', 'Safety interlock active', 'Relay M3 status'],
        ['Both pumps dead', 'Master gate blocked', 'Relay M1 and Input IL']
    ]

    fault_table = Table(fault_data, colWidths=[2.2*inch, 2*inch, 2.3*inch])
    fault_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('TOPPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))

    story.append(fault_table)
    story.append(PageBreak())

    # Field Inspection Checklist
    story.append(Paragraph("Field Inspection Checklist", heading1_style))

    checklist_sections = [
        ("Pre-Start", [
            "LOTO procedures completed",
            "Supply voltage confirmed (100-240V AC)",
            "PLC in RUN mode, 20ms cycle"
        ]),
        ("Input Tests", [
            "Input IL signal verified at terminal",
            "Inputs ID and IE continuity checked",
            "No flickering signals faster than 3ms"
        ]),
        ("Output/Timing Tests", [
            "Solenoids Q6, Q7, Q8 actuate within 1.5s",
            "Timers T9 and TA not timing out",
            "No conflicting outputs active simultaneously"
        ]),
        ("Internal Logic (via Zelio Soft or PLC display)", [
            "Relay M1 is ON (system ready)",
            "Relay M2 is ON (transfer requested)",
            "Relay M3 is ON (safety interlock clear)",
            "Relay M6 is OFF (no stop condition)",
            "Either M4 or M5 is ON (direction latched)"
        ]),
        ("Post-Test", [
            "All LOTO devices removed",
            "Enclosure secured"
        ])
    ]

    for section_title, items in checklist_sections:
        story.append(Paragraph(section_title, heading2_style))
        for item in items:
            story.append(Paragraph(f"☐ {item}", bullet_style))
        story.append(Spacer(1, 0.1*inch))

    story.append(PageBreak())

    # Most Likely Root Causes
    story.append(Paragraph("Most Likely Root Causes", heading1_style))
    story.append(Paragraph(
        "Based on \"works in Manual but not Auto\" behavior:",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))

    root_causes = [
        "<b>Input IL missing signal</b> (70% probability)",
        "<b>1.5s timer too short for valve actuation</b> (20% probability)",
        "<b>Input filtering rejecting fast signals</b> (10% probability)"
    ]

    for i, cause in enumerate(root_causes, 1):
        story.append(Paragraph(f"{i}. {cause}", bullet_style))

    story.append(Spacer(1, 0.5*inch))

    # Footer note
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "This document is for qualified personnel only. Follow all safety procedures and LOTO protocols.",
        footer_style
    ))

    # Build PDF
    doc.build(story)
    print(f"PDF generated successfully: {output_path}")
    return output_path

if __name__ == "__main__":
    # Output to project root directory
    output_file = "/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas/Oil_Tank_Transfer_Troubleshooting_Guide.pdf"
    create_troubleshooting_pdf(output_file)
