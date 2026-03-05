from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- ANALYZER PAGE ----------------

@app.route("/analyzer")
def analyzer():

    roles = {
        "Web": "Web Developer",
        "Data": "Data Scientist",
        "AI": "AI Engineer",
        "Cyber": "Cyber Security Analyst",
        "Mobile": "Mobile App Developer"
    }

    return render_template("analyzer.html", roles=roles)


# ---------------- ANALYZE SKILLS ----------------

@app.route("/analyze", methods=["POST"])
def analyze():

    role = request.form["role"]
    user_skills = request.form["skills"]

    user_skills_list = user_skills.split(",")
    user_skills_list = [skill.strip().lower() for skill in user_skills_list]

    role_skills = {
        "Web": ["html","css","javascript","react","git"],
        "Data": ["python","pandas","numpy","machine learning","sql"],
        "AI": ["python","deep learning","tensorflow","nlp"],
        "Cyber": ["networking","linux","ethical hacking","cryptography"],
        "Mobile": ["flutter","dart","firebase","ui design"]
    }

    required_skills = role_skills.get(role, [])

    missing_skills = []

    for skill in required_skills:
        if skill not in user_skills_list:
            missing_skills.append(skill)

    session["missing_skills"] = missing_skills
    session["role"] = role

    total_skills = len(required_skills)
    missing_count = len(missing_skills)
    matched_count = total_skills - missing_count

    percentage = int((matched_count / total_skills) * 100)

    session["percentage"] = percentage

    return redirect(url_for("skill_test"))


# ---------------- MENTOR DATA ----------------

mentors_data = [
    {
        "name": "Arjun",
        "skills": ["html", "css", "react", "git"],
        "experience": "Frontend Developer",
        "email": "arjun@skillbridge.com"
    },
    {
        "name": "Priya",
        "skills": ["python", "machine learning", "sql"],
        "experience": "ML Engineer",
        "email": "priya@skillbridge.com"
    },
    {
        "name": "Rahul",
        "skills": ["networking", "linux", "ethical hacking"],
        "experience": "Cyber Security Analyst",
        "email": "rahul@skillbridge.com"
    }
]


# ---------------- QUIZ QUESTIONS ----------------
quiz_questions = {

"Web": [

{
"question": "What does CSS stand for?",
"options": ["Cascading Style Sheets", "Computer Style Sheets", "Creative Style System"],
"answer": "Cascading Style Sheets"
},

{
"question": "Which language runs in the browser?",
"options": ["Python", "JavaScript", "C++"],
"answer": "JavaScript"
},

{
"question": "Which tag is used to create a hyperlink in HTML?",
"options": ["<a>", "<link>", "<href>"],
"answer": "<a>"
},

{
"question": "Which library is commonly used for building UI in modern web apps?",
"options": ["React", "NumPy", "TensorFlow"],
"answer": "React"
}

],


"Data": [

{
"question": "Which language is most used in Data Science?",
"options": ["Python", "PHP", "C++"],
"answer": "Python"
},

{
"question": "Which library is used for data analysis?",
"options": ["Pandas", "React", "Flutter"],
"answer": "Pandas"
},

{
"question": "Which library is used for numerical computing in Python?",
"options": ["NumPy", "Bootstrap", "Laravel"],
"answer": "NumPy"
},

{
"question": "Which query language is used to access databases?",
"options": ["SQL", "HTML", "CSS"],
"answer": "SQL"
}

],


"AI": [

{
"question": "Which language is widely used in AI development?",
"options": ["Python", "Java", "Swift"],
"answer": "Python"
},

{
"question": "Which framework is used for deep learning?",
"options": ["TensorFlow", "Bootstrap", "Django"],
"answer": "TensorFlow"
},

{
"question": "What does NLP stand for?",
"options": ["Natural Language Processing", "Network Layer Protocol", "Neural Link Program"],
"answer": "Natural Language Processing"
},

{
"question": "Which field focuses on training machines using data?",
"options": ["Machine Learning", "Web Design", "Cyber Security"],
"answer": "Machine Learning"
}

],


"Cyber": [

{
"question": "Which OS is commonly used by cybersecurity professionals?",
"options": ["Linux", "Windows XP", "DOS"],
"answer": "Linux"
},

{
"question": "What is ethical hacking?",
"options": ["Authorized security testing", "Illegal hacking", "Gaming"],
"answer": "Authorized security testing"
},

{
"question": "Which protocol secures websites?",
"options": ["HTTPS", "FTP", "SMTP"],
"answer": "HTTPS"
},

{
"question": "What does VPN stand for?",
"options": ["Virtual Private Network", "Verified Public Network", "Virtual Program Node"],
"answer": "Virtual Private Network"
}

],


"Mobile": [

{
"question": "Which language is used in Flutter development?",
"options": ["Dart", "Python", "C#"],
"answer": "Dart"
},

{
"question": "Which framework is used for cross-platform mobile apps?",
"options": ["Flutter", "React Native", "Both"],
"answer": "Both"
},

{
"question": "Which service is commonly used for mobile backend?",
"options": ["Firebase", "MongoDB Compass", "Photoshop"],
"answer": "Firebase"
},

{
"question": "Which component is used to design UI in Flutter?",
"options": ["Widgets", "Tables", "Layers"],
"answer": "Widgets"
}

]

}

# ---------------- SKILL TEST PAGE ----------------

@app.route("/skill_test")
def skill_test():

    role = session.get("role")

    questions = quiz_questions.get(role, [])

    return render_template("skill_test.html", questions=questions)


# ---------------- SUBMIT TEST ----------------

@app.route("/submit_test", methods=["POST"])
def submit_test():

    role = session.get("role")
    questions = quiz_questions.get(role, [])

    correct = 0

    for i, q in enumerate(questions):

        user_answer = request.form.get(f"q{i}")

        if user_answer == q["answer"]:
            correct += 1

    score = int((correct / len(questions)) * 100)

    session["test_score"] = score

    return redirect(url_for("result_after_test"))


# ---------------- RESULT AFTER TEST ----------------

@app.route("/result_after_test")
def result_after_test():

    test_score = session.get("test_score", 0)
    missing_skills = session.get("missing_skills", [])
    percentage = session.get("percentage", 0)

    if test_score < 75:

        message = "You should first improve your fundamentals."

        return render_template(
            "result.html",
            message=message,
            missing_skills=missing_skills,
            percentage=percentage,
            show_score=False
        )

    else:

        message = "Great! Let's analyze your skill gap."

        return render_template(
            "result.html",
            message=message,
            missing_skills=missing_skills,
            percentage=percentage,
            show_score=True
        )


# ---------------- MENTORS PAGE ----------------

@app.route("/mentors")
def mentors():

    missing_skills = session.get("missing_skills", [])
    selected_role = session.get("role", "").lower()

    smart_matches = []

    for mentor in mentors_data:

        mentor_skills = [s.lower() for s in mentor["skills"]]

        overlap = set(mentor_skills) & set(missing_skills)

        if not missing_skills:
            continue

        match_percentage = int((len(overlap) / len(missing_skills)) * 100)

        role_bonus = 0

        if selected_role in mentor["experience"].lower():
            role_bonus = 10

        final_score = match_percentage + role_bonus

        if final_score > 0:
            smart_matches.append({
                "name": mentor["name"],
                "experience": mentor["experience"],
                "match_score": final_score
            })

    smart_matches.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template("mentors.html", mentors=smart_matches)


# ---------------- LEARN PAGE ----------------

@app.route("/learn")
def learn():

    roles = {
        "web": "Web Developer",
        "data": "Data Scientist",
        "ai": "AI Engineer",
        "cyber": "Cyber Security Analyst",
        "mobile": "Mobile App Developer"
    }

    return render_template("learn.html", roles=roles)


# ---------------- START LEARNING ----------------

@app.route("/start_learning", methods=["POST"])
def start_learning():

    role = request.form["role"]

    role_skills = {
        "web": ["html","css","javascript","react","git"],
        "data": ["python","pandas","numpy","machine learning","sql"],
        "ai": ["python","deep learning","tensorflow","nlp"],
        "cyber": ["networking","linux","ethical hacking","cryptography"],
        "mobile": ["flutter","dart","firebase","ui design"]
    }

    required_skills = role_skills.get(role, [])

    session["missing_skills"] = required_skills
    session["role"] = role

    return redirect(url_for("mentors"))


# ---------------- CONNECT TO MENTOR ----------------

@app.route("/connect", methods=["POST"])
def connect():

    mentor_name = request.form["mentor_name"]

    selected_mentor = None

    for mentor in mentors_data:
        if mentor["name"] == mentor_name:
            selected_mentor = mentor
            break

    if not selected_mentor:
        return "Mentor not found"

    return render_template(
        "connection_success.html",
        mentor=selected_mentor
    )


# ---------------- RUN APP ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 10000))

    app.run(host="0.0.0.0", port=port)