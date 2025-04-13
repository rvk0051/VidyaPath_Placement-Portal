from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import os

app = Flask(__name__)
CORS(app)

# Knowledge base for placement-related queries
responses = {
    "what is vidyapath placement": "VidyaPath Placement is a platform that helps students connect with recruiters and simplifies the placement process with AI and ML features.",
    "how can i upload my resume": "You can upload your resume by logging into your VidyaPath profile and navigating to the 'Upload Resume' section.",
    "what companies visit for placements": "Major companies like TCS, Infosys, Wipro, and Accenture visit for placements. Check the platform for the full list.",
    "how to apply for a job": "Log into VidyaPath, browse through job listings, and click 'Apply' on jobs that match your profile.",
    "how can i prepare for interviews": "You can use resources like mock interviews and company-specific questions available on VidyaPath.",
    "does vidyapath offer internship opportunities": "Yes, VidyaPath also lists internship opportunities. Check the 'Internships' section for current openings.",
    "what is the eligibility for placement": "Eligibility criteria vary by company. Common criteria include a minimum GPA and no active backlogs.",
    "can i track my application status": "Yes, you can track your application status in the 'My Applications' section on VidyaPath.",
    "how does vidyapath use ai and ml": "VidyaPath uses AI and ML to recommend jobs based on your profile and predict placement trends.",
    "what is the placement success rate": "VidyaPath has a high success rate, with over 85% of students placed in top companies.",
    "how to schedule an interview": "Interview schedules are managed by the placement cell. Check your dashboard for updates.",
    "what documents are required for placement": "Typically, you need your resume, transcripts, and any certification relevant to the job.",
    "how to contact the placement cell": "You can contact the placement cell through the 'Contact Us' section on VidyaPath.",
    "are there placement preparation resources": "Yes, VidyaPath offers resources like coding challenges, aptitude tests, and mock interviews.",
    "is there a fee for placement services": "Placement services are free for registered students. Some advanced resources may have nominal charges.",
    "how to reset my vidyapath password": "Go to the login page and click 'Forgot Password' to reset your password.",
    "can alumni use vidyapath for placements": "Yes, VidyaPath also caters to alumni looking for job opportunities.",
    "what is the average salary package": "The average salary package depends on the company but ranges from 4 LPA to 10 LPA for freshers.",
    "how to improve my resume": "Use VidyaPath’s resume builder and ensure it highlights your skills and achievements relevant to the job.",
    "are off-campus jobs available": "Yes, VidyaPath lists both on-campus and off-campus job opportunities.",
    "what skills are companies looking for": "Skills like coding, problem-solving, communication, and knowledge of frameworks like Python and Java are in demand.",
    "can i get notifications for job openings": "Yes, you can enable job alerts in your VidyaPath profile settings.",
    "does vidyapath have a mobile app": "Currently, VidyaPath is web-based. A mobile app is under development.",
    "hello": "Welcome to VidyaPath Placement Website.",
    "thank you": "Thank you! We're thrilled to see you succeed. If you need any further assistance, feel free to reach out!"
}

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.json.get("message", "").lower()
    response = responses.get(user_message, "Sorry, I didn't understand that. Can you rephrase or contact the placement cell?")
    return jsonify({"response": response})

@app.route('/')
def index():
    return app.send_static_file('chatbot.html')

if __name__ == "__main__":
    
    if not os.environ.get('FLASK_RUN_FROM_CLI'):
        webbrowser.open("http://127.0.0.1:5000/")
    app.run(debug=True)