import os
import matplotlib.pyplot as plt
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# 1. Setup localized workspaces
os.makedirs('temp', exist_ok=True)
os.makedirs('generated', exist_ok=True)

# 2. Configure Frame-by-Frame Timeline Variables
fps = 60
total_frames = 180
frames = np.arange(1, total_frames + 1)
drop_frame = 60  # Network restriction hits precisely at 1.000 second

# Scenario A: WebRTC standard adaptation with a 12-frame RTCP feedback loop delay
webrtc_latency = np.ones(total_frames) * 16.67  # 16.67ms base frame-interval target
webrtc_status_log = []

for f in frames:
    if drop_frame <= f < (drop_frame + 12):
        webrtc_latency[f - 1] = 150.0  # Buffer starvation causes massive packet serialization delay
        status = "⚠️ Stalled / Dropped"
    else:
        webrtc_latency[f - 1] = 16.67
        status = "🟢 Smooth Playback"
    webrtc_status_log.append(status)

# Scenario B: AV1 SVC seamless layer drop
av1_latency = np.ones(total_frames) * 16.67
av1_status_log = []

for f in frames:
    if f == drop_frame:
        av1_latency[f - 1] = 22.0  # Minor sub-frame switch processing overhead
        status = "🟡 Resol. Drop (720p)"
    elif f > drop_frame:
        av1_latency[f - 1] = 16.67
        status = "🟢 Smooth (Lo-Fi Quality)"
    else:
        av1_latency[f - 1] = 16.67
        status = "🟢 Smooth Playback"
    av1_status_log.append(status)

# 3. Generate Micro-Level Latency Matplotlib Plot
plt.figure(figsize=(8, 4), dpi=200)
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')

plt.plot(frames, webrtc_latency, label="WebRTC (GCC) Render Latency", color="#ff4d4d", linewidth=2.2)
plt.plot(frames, av1_latency, label="AV1 (SVC) Render Latency", color="#2ecc71", linewidth=2.2, linestyle="--")
plt.axvline(x=drop_frame, color="#34495e", linestyle=":", alpha=0.8, linewidth=1.5)
plt.text(drop_frame + 1.5, 110, "Bandwidth Collapse\n(15 Mbps -> 3 Mbps)", color="#34495e", fontsize=8, weight="bold")

plt.title("Frame-by-Frame Playback Render Latency Spike Analysis", fontsize=11, pad=12, weight="bold")
plt.xlabel("Timeline (Frames Passed @ 60 FPS)", fontsize=9)
plt.ylabel("Frame Render Latency (ms)", fontsize=9)

# Zoom into the window surrounding the shock event for enhanced diagnostic clarity
plt.xlim(45, 85) 
plt.ylim(0, 180)
plt.legend(loc="upper right", fontsize=8.5)
plt.tight_layout()

chart_path = 'temp/latency_spike_comparison.png'
plt.savefig(chart_path, dpi=200)
plt.close()

# 4. Compile PDF Report Structure
pdf_path = 'generated/frame_breakdown_report.pdf'
doc = SimpleDocTemplate(
    pdf_path, 
    pagesize=letter, 
    rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54, 
    title="Frame-by-Frame Video Playback Degradation Analysis"
)

styles = getSampleStyleSheet()
title_style = ParagraphStyle('DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=22, leading=26, textColor=colors.HexColor('#1a365d'), spaceAfter=15)
heading_style = ParagraphStyle('SectionHeading', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, leading=17, textColor=colors.HexColor('#2b6cb0'), spaceBefore=12, spaceAfter=8)
body_style = ParagraphStyle('BodyTextCustom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=15, textColor=colors.HexColor('#2d3748'), spaceAfter=10)

elements = []
elements.append(Paragraph("Frame-by-Frame Video Playback Degradation Analysis", title_style))
elements.append(Paragraph("This report highlights the micro-level visual pacing anomalies and player buffer stalls that occur when a video streaming engine experiences sudden network congestion.", body_style))

# Section 1: Plot Image
elements.append(Paragraph("1. Frame Latency Under Network Shock", heading_style))
elements.append(Image(chart_path, width=450, height=225))
elements.append(Spacer(1, 10))

# Section 2: Precise Timeline Matrix Table
elements.append(Paragraph("2. Micro-Timeline Playback Log Snapshot", heading_style))
table_data = [
    ["Frame #", "Timestamp", "WebRTC Bitrate Target", "WebRTC Render Latency", "AV1 SVC Stratum", "AV1 Render Latency"],
    ["58", "0.966s", "10.00 Mbps", "16.67ms (Smooth)", "L2 Layer (1080p)", "16.67ms (Smooth)"],
    ["59", "0.983s", "10.00 Mbps", "16.67ms (Smooth)", "L2 Layer (1080p)", "16.67ms (Smooth)"],
    ["60 (Drop)", "1.000s", "10.00 Mbps (Overload)", "150.00ms (Stall Event)", "L0 Layer (720p)", "22.00ms (Resol. Drop)"],
    ["61", "1.016s", "10.00 Mbps (Overload)", "150.00ms (Dropped Frame)", "L0 Layer (720p)", "16.67ms (Smooth Log)"],
    ["62", "1.033s", "10.00 Mbps (Overload)", "150.00ms (Dropped Frame)", "L0 Layer (720p)", "16.67ms (Smooth Log)"],
    ["72 (Adjust)", "1.200s", "2.85 Mbps (Stable)", "16.67ms (Smooth Loop)", "L0 Layer (720p)", "16.67ms (Smooth Log)"]
]

log_table = Table(table_data, colWidths=[55, 60, 115, 115, 95, 100])
log_table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#2b6cb0')),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('GRID', (0,0), (-1,-1), 1, colors.HexColor('#e2e8f0')),
    ('FONTSIZE', (0,0), (-1,-1), 8.5),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#fed7d7'))  # Soft red accent coloring for the drop row
]))
elements.append(log_table)

doc.build(elements)
print("Framework compiled successfully.")
