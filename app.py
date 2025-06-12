# app.py (Flask Backend)
from flask import Flask, render_template, request, send_file
import os
import threading
from scraper import scrape_x_profile
from report_generator import generate_report

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'reports'
app.config['SECRET_KEY'] = 'your-secret-key'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    username = request.form['username'].strip().replace('@', '')
    if not username:
        return {'status': 'error', 'message': 'Please enter a username'}
    
    def analysis_task():
        try:
            # Step 1: Scrape tweets
            scrape_x_profile(username)
            
            # Step 2: Generate report
            generate_report(username)
            
        except Exception as e:
            print(f"Error: {str(e)}")

    # Run in background thread
    thread = threading.Thread(target=analysis_task)
    thread.start()
    
    return {'status': 'processing', 'username': username}

@app.route('/preview/<username>')
def preview_report(username):
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{username}_analysis.pdf")
    if os.path.exists(report_path):
        response = send_file(
            report_path,
            mimetype='application/pdf',
            as_attachment=False,  # Crucial for preview
            conditional=True
        )
        response.headers['Content-Disposition'] = f'inline; filename="{username}_analysis.pdf"'
        return response
    return "Report not found", 404

@app.route('/report/<username>')
def get_report(username):
    report_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{username}_analysis.pdf")
    if os.path.exists(report_path):
        return send_file(report_path, as_attachment=True)
    return "Report not found", 404

if __name__ == '__main__':
    app.run(debug=True)