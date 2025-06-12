from fpdf import FPDF, XPos, YPos
import pandas as pd
from datetime import datetime
import os
from analyzer import detect_threats
import warnings
import sys

warnings.filterwarnings("ignore", category=UserWarning, module="fpdf.ttfonts")

class TwitterReport(FPDF):
    def __init__(self):
        super().__init__()
        self.font_dir = os.path.join(os.path.dirname(__file__), "fonts")
        self.available_width = 190  # 210mm (A4) - 20mm margins
        self._load_fonts()
        self.set_margins(10, 10, 10)
        self.set_auto_page_break(True, margin=15)
        
    def _load_fonts(self):
        font_files = {
            'DejaVuSans.ttf': ('', 12),
            'DejaVuSans-Bold.ttf': ('B', 14),
            'DejaVuSans-Oblique.ttf': ('I', 12),
            'DejaVuSans-BoldOblique.ttf': ('BI', 12)
        }
        
        for file_name, (style, size) in font_files.items():
            font_path = os.path.join(self.font_dir, file_name)
            if not os.path.exists(font_path):
                raise RuntimeError(f"Missing font: {file_name}")
            self.add_font('DejaVu', style=style, fname=font_path)
        
        self.set_font('DejaVu', '', 12)

    def _write_header(self, text, level=1):
        self.set_font('DejaVu', 'B', 18 if level == 1 else 14)
        self.cell(self.available_width, 10, text, align='C')
        self.ln(15)

    def _write_tweet(self, number, text, threats):
        self.set_fill_color(245, 248, 250)  # Twitter background
        self.set_font('DejaVu', 'B', 10)
        
        # Tweet container
        self.multi_cell(
            w=self.available_width,
            h=6,
            text=f"Tweet #{number}",
            border=1,
            fill=True,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )
        
        # Content with proper wrapping
        self.set_font('DejaVu', '', 10)
        self.set_text_color(20, 23, 26)  # Twitter text color
        self.multi_cell(
            w=self.available_width,
            h=6,
            text=text,
            new_x=XPos.LMARGIN,
            new_y=YPos.NEXT
        )
        
        if threats:
            self.set_font('DejaVu', 'I', 8)
            self.set_text_color(220, 30, 30)  # Red for threats
            self.multi_cell(
                w=self.available_width,
                h=6,
                text=f"⚠️ Flags: {threats}",
                new_x=XPos.LMARGIN,
                new_y=YPos.NEXT
            )
            self.set_text_color(20, 23, 26)  # Reset color
            
        self.ln(4)

def generate_report(username):
    try:
        username = username.strip('@').split('_')[0]
        csv_path = os.path.join("data", "csv", f"{username}_tweets.csv")
        
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"Tweet data missing: {os.path.basename(csv_path)}")
            
        df = pd.read_csv(csv_path)
        if df.empty:
            raise ValueError("CSV file contains no tweets")
            
        pdf = TwitterReport()
        pdf.add_page()
        
        # Cover Page
        pdf._write_header("Twitter Analysis Report")
        pdf.set_font('DejaVu', '', 14)
        pdf.cell(pdf.available_width, 10, f"for @{username}", align='C')
        pdf.ln(20)
        
        # Analysis Section
        pdf.add_page()
        pdf._write_header("Detailed Analysis", level=2)
        
        for idx, row in df.iterrows():
            text = str(row['Text']).strip()[:280]  # Limit text length
            text = text.replace('\x00', '')  # Remove null bytes
            threats = detect_threats(text)
            
            pdf._write_tweet(
                number=idx+1,
                text=text,
                threats=threats.replace('|', ', ') if threats else ""
            )
            
            if pdf.y > 280:
                pdf.add_page()

        # Save output
        os.makedirs("reports", exist_ok=True)
        output_path = os.path.join("reports", f"{username}_analysis.pdf")
        pdf.output(output_path)
        print(f"✅ Report saved to: {os.path.abspath(output_path)}")
        return True
        
    except Exception as e:
        print(f"❌ Critical failure: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python report_generator.py <username>")
        sys.exit(1)
        
    success = generate_report(sys.argv[1])
    sys.exit(0 if success else 1)