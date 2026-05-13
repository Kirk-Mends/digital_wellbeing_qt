
# 5
# Upgraded 

# core/export_manager.py

import csv
import xlsxwriter
from reportlab.pdfgen import canvas
from datetime import datetime

class AnalyticsExportManager:
    def __init__(self, engine):
        self.engine = engine

    # ---------------- CSV EXPORT ----------------
    def export_csv(self, path):
        data = self.engine.export_all_data()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Section", "Key", "Value"])
            for section, values in data.items():
                for key, value in values.items():
                    writer.writerow([section, key, value])

    # ---------------- EXCEL EXPORT ----------------
    def export_excel(self, path):
        data = self.engine.export_all_data()
        workbook = xlsxwriter.Workbook(path)

        for section, values in data.items():
            sheet = workbook.add_worksheet(section[:31])
            sheet.write(0, 0, "Key")
            sheet.write(0, 1, "Value")
            row = 1
            for key, value in values.items():
                sheet.write(row, 0, key)
                sheet.write(row, 1, str(value))
                row += 1

        workbook.close()

    # ---------------- PDF EXPORT ----------------
    def export_pdf(self, path):
        data = self.engine.export_all_data()
        pdf = canvas.Canvas(path)
        pdf.setFont("Helvetica", 12)

        y = 800
        pdf.drawString(50, y, "Analytics Export")
        y -= 30

        for section, values in data.items():
            pdf.drawString(50, y, f"--- {section} ---")
            y -= 20
            for key, value in values.items():
                pdf.drawString(60, y, f"{key}: {value}")
                y -= 15
                if y < 50:
                    pdf.showPage()
                    y = 800

        pdf.save()
