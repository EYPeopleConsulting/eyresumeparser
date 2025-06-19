import os
import socket
import threading
import webbrowser
from flask import Flask, request, render_template, send_from_directory
from utils.extract import extract_jd_text, extract_resumes
from utils.scorer import compute_scores
from utils.excel_report import export_to_excel

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        jd_text = extract_jd_text(request)
        if not jd_text:
            return render_template('index.html', error="Please upload or paste a JD.", results=[], excel_filename=None)

        mandatory_skills = [s.strip() for s in request.form['mandatory_skills'].split(',') if s.strip()]
        must_have_skills = [s.strip() for s in request.form['must_have_skills'].split(',') if s.strip()]

        resumes = extract_resumes('resumes')[:10]  # Max 10 resumes
        if not resumes:
            return render_template('index.html', error="No valid resumes found.", results=[], excel_filename=None)

        results = compute_scores(jd_text, resumes, mandatory_skills, must_have_skills)
        excel_filename = export_to_excel(results)

        return render_template('results.html', results=results, excel_filename=excel_filename)

    # For GET request
    return render_template('index.html', results=[], excel_filename=None)

@app.route('/outputs/<filename>')
def download_excel(filename):
    return send_from_directory('outputs', filename, as_attachment=True)

def run_app():
    sock = socket.socket()
    sock.bind(('', 0))
    _, port = sock.getsockname()
    sock.close()

    url = f'http://localhost:{port}'
    threading.Thread(target=lambda: app.run(port=port, debug=False, use_reloader=False)).start()
    print(f"\n🚀 Opening in browser: {url}")
    webbrowser.open(url)

if __name__ == '__main__':
    run_app()
