from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import os
from meeting_assistant import MeetingAssistant

app = Flask(__name__)
app.secret_key = "meeting_ai_secret_key_123" # Session history ke liye zaroori hai

# Assistant instance
assistant = MeetingAssistant()

@app.route('/')
def home():
    # Agar history session mein nahi hai toh empty list banao
    if 'history' not in session:
        session['history'] = []
    return render_template('index.html', history=session['history'])

@app.route('/analyze', methods=['POST'])
def analyze():
    transcript = ""
    
    # Check if a file was uploaded
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            transcript = file.read().decode("utf-8")
    
    # Otherwise check for JSON text input
    if not transcript and request.is_json:
        data = request.get_json()
        transcript = data.get('transcript', '')

    if not transcript:
        return jsonify({"error": "No transcript content found"}), 400

    # NLP Analysis
    insights = assistant.analyze_meeting(transcript)
    
    # Report Data Bundle
    report_data = {
        "id": len(session.get('history', [])) + 1,
        "summary": insights.summary,
        "sentiment": insights.sentiment,
        "duration": insights.duration_estimate,
        "participants": insights.participants,
        "decisions": insights.decisions,
        "action_items": insights.action_items,
        "questions": insights.questions
    }

    # History update karein
    history = session.get('history', [])
    history.append(report_data)
    session['history'] = history
    session.modified = True

    return jsonify({"redirect": url_for('show_report', report_id=report_data['id'])})

@app.route('/report/<int:report_id>')
def show_report(report_id):
    history = session.get('history', [])
    report = next((item for item in history if item['id'] == report_id), None)
    
    if not report:
        return "Report not found", 404
        
    return render_template('report.html', report=report)

@app.route('/delete_history')
def delete_history():
    session['history'] = []
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)