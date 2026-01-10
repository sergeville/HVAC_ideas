#!/usr/bin/env python3
"""
Generate a diagnostic PDF for Tank #1 auto-fill failure.
Specific troubleshooting guide based on the Oil Tank Transfer Box system.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from datetime import datetime

def create_tank1_diagnostic_pdf(output_path):
    """Generate Tank #1 diagnostic PDF document."""

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )

    story = []
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#c0392b'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2c3e50'),
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

    step_style = ParagraphStyle(
        'StepStyle',
        parent=styles['BodyText'],
        fontSize=11,
        leftIndent=15,
        spaceAfter=8,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#2980b9')
    )

    warning_style = ParagraphStyle(
        'Warning',
        parent=body_style,
        backColor=colors.HexColor('#fff3cd'),
        borderPadding=10,
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=colors.HexColor('#856404')
    )

    # Title page
    story.append(Paragraph("DIAGNOSTIC GUIDE", title_style))
    story.append(Paragraph("Tank #1 Auto-Fill Failure", subtitle_style))
    story.append(Spacer(1, 0.2*inch))

    # Problem box
    problem_box = Paragraph(
        "<b>PROBLEM:</b> Tank #1 does not fill automatically",
        ParagraphStyle('ProblemBox', parent=body_style, backColor=colors.HexColor('#ffe6e6'),
                      borderPadding=12, fontSize=13, fontName='Helvetica-Bold')
    )
    story.append(problem_box)
    story.append(Spacer(1, 0.3*inch))

    # System info
    info_text = f"""
    <para align=center>
    <b>System:</b> Oil Tank Transfer Box (Program #3201)<br/>
    <b>PLC:</b> Schneider Electric Zelio Logic SR3B261FU<br/>
    <b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}<br/>
    </para>
    """
    story.append(Paragraph(info_text, body_style))
    story.append(Spacer(1, 0.3*inch))

    # Safety warning
    story.append(Paragraph(
        "⚠️ WARNING: Follow all LOTO (Lockout/Tagout) procedures before working on this equipment. "
        "System operates at 240V AC. Qualified personnel only.",
        warning_style
    ))

    story.append(PageBreak())

    # Overview section
    story.append(Paragraph("Diagnostic Overview", heading1_style))
    story.append(Paragraph(
        "This guide provides a systematic approach to diagnose why Tank #1 fails to fill automatically "
        "while the system may work in manual mode or for other tanks.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    overview_items = [
        "<b>Time Required:</b> 15-30 minutes",
        "<b>Tools Needed:</b> Digital multimeter, Zelio Soft software (optional but helpful), laptop with PLC cable",
        "<b>Prerequisites:</b> System in safe state, LOTO applied, access to PLC terminals and display"
    ]
    for item in overview_items:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # STEP 1
    story.append(Paragraph("STEP 1: Identify Tank #1 Direction", heading1_style))
    story.append(Paragraph(
        "The PLC uses two directional inputs to control which tank receives oil. "
        "First, determine which input controls Tank #1.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))

    direction_data = [
        ['Input', 'Controls', 'PLC Relay', 'Function'],
        ['ID', 'Tank A (Direction 1)', 'M4', 'Latches when Tank A needs filling'],
        ['IE', 'Tank B (Direction 2)', 'M5', 'Latches when Tank B needs filling']
    ]

    direction_table = Table(direction_data, colWidths=[0.8*inch, 1.8*inch, 1.2*inch, 2.7*inch])
    direction_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c3e50')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))

    story.append(direction_table)
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("✓ ACTION: Determine if Tank #1 = Tank A (Input ID) or Tank B (Input IE)", step_style))
    story.append(Paragraph("Document here: Tank #1 is controlled by Input: ___________", body_style))

    story.append(PageBreak())

    # STEP 2
    story.append(Paragraph("STEP 2: Manual Mode Test", heading1_style))
    story.append(Paragraph(
        "This quick test determines if the problem is with automatic sensing or the physical pump/valve system.",
        body_style
    ))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("Procedure:", heading3_style))
    manual_steps = [
        "Switch control selector to <b>MANUAL</b> mode",
        "Manually activate the transfer to Tank #1",
        "Observe what happens"
    ]
    for i, step in enumerate(manual_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Result Interpretation:", heading3_style))

    result_data = [
        ['What Happens', 'What It Means', 'Go To'],
        ['Tank #1 fills successfully', 'Pump & valves work.\nProblem is AUTO sensing.', 'STEP 3'],
        ['Tank #1 does NOT fill', 'Physical problem with\npump, valves, or wiring.', 'STEP 5'],
        ['Pump starts but stops\nafter 1-2 seconds', 'Timer timeout fault.\nValve too slow.', 'STEP 6']
    ]

    result_table = Table(result_data, colWidths=[2.2*inch, 2.5*inch, 1.8*inch])
    result_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#27ae60')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.HexColor('#e8f8f5'), colors.white, colors.HexColor('#fff3e0')])
    ]))

    story.append(result_table)
    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ Document result: _______________________________", body_style))

    story.append(PageBreak())

    # STEP 3
    story.append(Paragraph("STEP 3: Check Tank #1 Level Sensor", heading1_style))
    story.append(Paragraph(
        "If manual works but auto doesn't, the level sensor (float switch) that triggers Tank #1 fill is likely failed.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("A. Visual Inspection:", heading2_style))
    visual_checks = [
        "Locate the level sensor/float switch for Tank #1",
        "Check for mechanical binding or debris preventing movement",
        "Verify float arm moves freely through full range",
        "Look for corrosion or damage on sensor body"
    ]
    for item in visual_checks:
        story.append(Paragraph(f"☐ {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("B. Electrical Continuity Test:", heading2_style))
    story.append(Paragraph(
        "Using a multimeter set to continuity mode:",
        body_style
    ))

    electrical_steps = [
        "Disconnect sensor wiring from PLC terminal (ID or IE)",
        "Test sensor continuity by moving float to \"low level\" position",
        "Sensor should <b>close contact</b> when Tank #1 is low (needs filling)",
        "Sensor should <b>open contact</b> when Tank #1 is full"
    ]
    for i, step in enumerate(electrical_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ Sensor operates correctly: ☐ YES  ☐ NO", step_style))
    story.append(Paragraph("If NO: Replace sensor and retest. If YES: Continue to STEP 4.", body_style))

    story.append(PageBreak())

    # STEP 4
    story.append(Paragraph("STEP 4: Verify PLC Input Signal", heading1_style))
    story.append(Paragraph(
        "Even if the sensor works, the signal must reach the PLC terminal. This checks wiring integrity.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("A. Terminal Voltage Check:", heading2_style))
    terminal_steps = [
        "Reconnect sensor wiring to PLC",
        "Set multimeter to DC voltage measurement",
        "Connect multimeter to Input <b>ID</b> (or <b>IE</b>) terminal and common ground",
        "Manually lower Tank #1 level to trigger \"needs filling\" condition",
        "Expected: You should see voltage (typically 12-24V DC) when sensor activates",
        "If NO voltage present → wiring problem between sensor and PLC"
    ]
    for i, step in enumerate(terminal_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ Voltage detected at PLC input: ☐ YES  ☐ NO", step_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("B. PLC Internal Logic Check:", heading2_style))
    story.append(Paragraph(
        "If you have Zelio Soft software or PLC display access:",
        body_style
    ))

    logic_checks = [
        "Monitor relay <b>M4</b> (for Tank A/ID) or <b>M5</b> (for Tank B/IE)",
        "Trigger the low-level condition for Tank #1",
        "The corresponding relay should turn <b>ON</b> and <b>LATCH</b>",
        "If relay doesn't activate → PLC input filtering or configuration issue"
    ]
    for item in logic_checks:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ Relay M4/M5 activates: ☐ YES  ☐ NO", step_style))

    story.append(PageBreak())

    # STEP 5
    story.append(Paragraph("STEP 5: System Ready Relay Check (M1)", heading1_style))
    story.append(Paragraph(
        "<b>Critical:</b> Relay M1 is the master \"System Ready\" gate. If M1 is OFF, NO pumps can run, even in auto mode.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Why M1 Might Be OFF:", heading3_style))
    m1_causes = [
        "<b>Input IL is open</b> - Most common cause (70% of failures)",
        "Safety condition detected by PLC",
        "PLC in STOP mode or fault state",
        "Power supply issue to control circuit"
    ]
    for item in m1_causes:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("Diagnostic Steps:", heading3_style))

    m1_steps = [
        "Check PLC display or Zelio Soft: Is relay <b>M1</b> active?",
        "If M1 is OFF, check terminal <b>IL</b> with multimeter for voltage",
        "Verify wiring from \"System Ready\" sensor to IL terminal",
        "Check for tripped safety devices (E-stops, thermal overloads)"
    ]
    for i, step in enumerate(m1_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ M1 relay status: ☐ ON  ☐ OFF", step_style))
    story.append(Paragraph("✓ Input IL voltage: __________ VDC", step_style))

    story.append(PageBreak())

    # STEP 6
    story.append(Paragraph("STEP 6: Check Safety Interlocks", heading1_style))
    story.append(Paragraph(
        "Several safety relays can prevent Tank #1 from filling even if all sensors are working.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    safety_data = [
        ['Relay', 'Required State', 'Function', 'Check If Wrong'],
        ['M1', 'ON', 'System Ready Gate', 'Input IL, safety devices'],
        ['M2', 'ON', 'Transfer Demand', 'Low-level sensor active'],
        ['M3', 'ON', 'Safety Interlock', 'Valves Q6/Q7/Q8 not stuck'],
        ['M6', 'OFF', 'Stop Command', 'E-Stop, thermal overload'],
        ['M4 or M5', 'ON', 'Direction Latched', 'Input ID or IE']
    ]

    safety_table = Table(safety_data, colWidths=[0.8*inch, 1.1*inch, 1.8*inch, 2.8*inch])
    safety_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#c0392b')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')])
    ]))

    story.append(safety_table)
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("✓ ACTION: Use PLC display/software to verify ALL relays are in correct state", step_style))

    story.append(PageBreak())

    # STEP 7
    story.append(Paragraph("STEP 7: Timer & Valve Sequencing", heading1_style))
    story.append(Paragraph(
        "If the system starts but stops immediately, the 1.5-second valve timing may be the issue.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("The Problem:", heading3_style))
    story.append(Paragraph(
        "Timers T9 and TA are set to <b>1.5 seconds</b>. If the solenoid valves don't fully open "
        "within this window, the PLC times out and shuts down the pump to prevent damage.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    story.append(Paragraph("Test Procedure:", heading3_style))
    timer_steps = [
        "Trigger Tank #1 fill in Auto mode",
        "Watch solenoid valve (Q6 or Q7 depending on Tank #1 assignment)",
        "Using a stopwatch, measure time from valve activation to full open",
        "Monitor pump output (Q1 or Q2) - does it start?",
        "If pump starts then stops immediately → Timer fault"
    ]
    for i, step in enumerate(timer_steps, 1):
        story.append(Paragraph(f"{i}. {step}", bullet_style))

    story.append(Spacer(1, 0.15*inch))
    story.append(Paragraph("✓ Valve actuation time: __________ seconds", step_style))
    story.append(Spacer(1, 0.1*inch))

    story.append(Paragraph("If time > 1.5 seconds:", heading3_style))
    timer_solutions = [
        "Check valve for mechanical binding or debris",
        "Verify valve receives full voltage (measure at valve terminals)",
        "Consider increasing timer setting in PLC program (requires programming access)",
        "Replace slow-acting valve with faster model"
    ]
    for item in timer_solutions:
        story.append(Paragraph(f"• {item}", bullet_style))

    story.append(PageBreak())

    # Troubleshooting flowchart summary
    story.append(Paragraph("Quick Troubleshooting Flowchart", heading1_style))

    flowchart_text = """
    <para>
    <b>START:</b> Tank #1 won't fill automatically<br/>
    ⬇<br/>
    <b>Try Manual Mode</b><br/>
    ⬇⬇<br/>
    Works? ➜ YES ➜ Problem is AUTO sensing ➜ Check Steps 3-4<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;➜ NO ➜ Physical problem ➜ Check Steps 5-7<br/>
    ⬇<br/>
    <b>Check Input IL (System Ready)</b><br/>
    ⬇<br/>
    Signal present? ➜ NO ➜ Fix IL wiring/sensor ➜ DONE<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;➜ YES ➜ Continue<br/>
    ⬇<br/>
    <b>Check Tank #1 direction input (ID or IE)</b><br/>
    ⬇<br/>
    Signal present? ➜ NO ➜ Fix level sensor/wiring ➜ DONE<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;➜ YES ➜ Continue<br/>
    ⬇<br/>
    <b>Check all safety relays (M1, M2, M3, M6)</b><br/>
    ⬇<br/>
    All correct? ➜ NO ➜ Investigate failed relay ➜ Fix root cause<br/>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;➜ YES ➜ Check valve timing (Step 7)<br/>
    </para>
    """

    flowchart_style = ParagraphStyle(
        'Flowchart',
        parent=body_style,
        backColor=colors.HexColor('#f0f0f0'),
        borderPadding=15,
        fontSize=9,
        fontName='Courier',
        leading=14
    )

    story.append(Paragraph(flowchart_text, flowchart_style))

    story.append(PageBreak())

    # Diagnostic worksheet
    story.append(Paragraph("Field Diagnostic Worksheet", heading1_style))
    story.append(Paragraph(
        "Complete this worksheet during troubleshooting. Record all findings for documentation.",
        body_style
    ))
    story.append(Spacer(1, 0.15*inch))

    worksheet_items = [
        ("Date/Time:", "_" * 40),
        ("Technician Name:", "_" * 40),
        ("Tank #1 corresponds to:", "☐ Tank A (Input ID)  ☐ Tank B (Input IE)"),
        ("Manual mode test result:", "☐ Works  ☐ Fails  ☐ Times out"),
        ("", ""),
        ("<b>Voltage Measurements:</b>", ""),
        ("Input IL voltage:", "__________ VDC"),
        ("Input ID voltage:", "__________ VDC"),
        ("Input IE voltage:", "__________ VDC"),
        ("", ""),
        ("<b>PLC Relay Status:</b>", ""),
        ("M1 (System Ready):", "☐ ON  ☐ OFF"),
        ("M2 (Demand):", "☐ ON  ☐ OFF"),
        ("M3 (Safety OK):", "☐ ON  ☐ OFF"),
        ("M4 (Direction A):", "☐ ON  ☐ OFF"),
        ("M5 (Direction B):", "☐ ON  ☐ OFF"),
        ("M6 (Stop):", "☐ ON  ☐ OFF"),
        ("", ""),
        ("<b>Timing Tests:</b>", ""),
        ("Valve actuation time:", "__________ seconds"),
        ("Timer fault observed:", "☐ T9  ☐ TA  ☐ None"),
        ("", ""),
        ("<b>Root Cause Identified:</b>", ""),
        ("", "_" * 60),
        ("", "_" * 60),
        ("", ""),
        ("<b>Corrective Action Taken:</b>", ""),
        ("", "_" * 60),
        ("", "_" * 60),
        ("", ""),
        ("<b>System tested and working:</b>", "☐ YES  ☐ NO"),
    ]

    for label, value in worksheet_items:
        if label == "":
            story.append(Spacer(1, 0.05*inch))
        else:
            story.append(Paragraph(f"{label} {value}", bullet_style))

    story.append(Spacer(1, 0.3*inch))

    # Footer
    footer_style = ParagraphStyle(
        'Footer',
        parent=body_style,
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER
    )
    story.append(Paragraph(
        "This diagnostic guide is for qualified personnel only. "
        "Always follow LOTO procedures and safety protocols.",
        footer_style
    ))

    # Build PDF
    doc.build(story)
    print(f"Tank #1 diagnostic PDF generated: {output_path}")
    return output_path

if __name__ == "__main__":
    output_file = "/Users/sergevilleneuve/Documents/MyExperiments/HVAC_ideas/Tank1_Auto_Fill_Diagnostic_Guide.pdf"
    create_tank1_diagnostic_pdf(output_file)
