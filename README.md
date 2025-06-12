# Twitter Account Analysis Tool

A web-based tool to analyze Twitter accounts, scrape tweets, detect threats, and generate PDF reports.

![Screenshot](screenshot.png) <!-- Add actual screenshot later -->

## Features
- Scrape tweets from public Twitter accounts
- Analyze tweets for threats and sentiment
- Generate professional PDF reports
- Web interface with report preview
- Downloadable reports

## Installation

### Prerequisites
- Python 3.8+
- Chrome browser
- Git

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   cd YOUR-REPO-NAME


2. Install dependencies:

     ```bash
     pip install -r requirements.txt
     ```
3. Download ChromeDriver:

   Automatically handled by webdriver-manager

4. Install fonts:

   -Download DejaVu Sans fonts from dejavu-fonts.github.io

   -Place these 4 files in fonts/ directory:

      -DejaVuSans.ttf
      
      -DejaVuSans-Bold.ttf
      
      -DejaVuSans-Oblique.ttf
      
      -DejaVuSans-BoldOblique.ttf

##Usage
   1. Start the application:
   
            ```bash
            python app.py
  2.  Open your browser to:
   
            text
            http://localhost:5000
   3. Enter a Twitter username and click "Analyze"
   
   4. View and download the generated report

##Project Structure
text
twitter-analysis-tool/
├── app.py                # Main application
├── scraper.py            # Twitter scraping functions
├── analyzer.py           # Tweet analysis
├── report_generator.py   # PDF report generation
├── requirements.txt      # Dependencies
├── .gitignore
├── README.md
├── fonts/                # Font files for PDF
├── static/               # CSS/JS assets
│   ├── styles.css
│   └── app.js
├── templates/            # HTML templates
│   └── index.html
├── data/                 # Scraped data (gitignored)
│   └── csv/
└── reports/              # Generated reports (gitignored)

##Dependencies
Flask (web framework)

Selenium (web scraping)

pandas (data analysis)

fpdf2 (PDF generation)

TextBlob (sentiment analysis)

webdriver-manager (ChromeDriver management)

##Contributing
Contributions are welcome! Please follow these steps:

Fork the repository

Create your feature branch (git checkout -b feature/your-feature)

Commit your changes (git commit -m 'Add some feature')

Push to the branch (git push origin feature/your-feature)

Open a pull request

##License
This project is licensed under the MIT License - see LICENSE file for details.

##Disclaimer
This tool is for educational purposes only. Use it responsibly and respect Twitter's Terms of Service. The developers are not responsible for any misuse of this tool.

