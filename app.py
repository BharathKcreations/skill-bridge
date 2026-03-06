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

    return redirect(url_for("skill_test"))


# ---------------- QUIZ QUESTIONS ----------------

quiz_questions = {

"Web": [

{"question": "What does CSS stand for?",
"options": ["Cascading Style Sheets","Computer Style Sheets","Creative Style System"],
"answer": "Cascading Style Sheets"},

{"question": "Which language runs in the browser?",
"options": ["Python","JavaScript","C++"],
"answer": "JavaScript"},

{"question": "Which tag creates a hyperlink?",
"options": ["<a>","<link>","<href>"],
"answer": "<a>"},

{"question": "Which library builds UI in web apps?",
"options": ["React","NumPy","TensorFlow"],
"answer": "React"}
],

"Data":[

{"question":"Most used language in data science?",
"options":["Python","PHP","C++"],
"answer":"Python"},

{"question":"Library for data analysis?",
"options":["Pandas","React","Flutter"],
"answer":"Pandas"},

{"question":"Library for numerical computing?",
"options":["NumPy","Bootstrap","Laravel"],
"answer":"NumPy"},

{"question":"Database query language?",
"options":["SQL","HTML","CSS"],
"answer":"SQL"}
],

"AI":[

{"question":"Most used language in AI?",
"options":["Python","Java","Swift"],
"answer":"Python"},

{"question":"Deep learning framework?",
"options":["TensorFlow","Bootstrap","Django"],
"answer":"TensorFlow"},

{"question":"What does NLP stand for?",
"options":["Natural Language Processing","Network Layer Protocol","Neural Link Program"],
"answer":"Natural Language Processing"},

{"question":"Field training machines using data?",
"options":["Machine Learning","Web Design","Cyber Security"],
"answer":"Machine Learning"}
],

"Cyber":[

{"question":"OS used by security professionals?",
"options":["Linux","Windows XP","DOS"],
"answer":"Linux"},

{"question":"Ethical hacking means?",
"options":["Authorized security testing","Illegal hacking","Gaming"],
"answer":"Authorized security testing"},

{"question":"Protocol securing websites?",
"options":["HTTPS","FTP","SMTP"],
"answer":"HTTPS"},

{"question":"VPN stands for?",
"options":["Virtual Private Network","Verified Public Network","Virtual Program Node"],
"answer":"Virtual Private Network"}
],

"Mobile":[

{"question":"Language used in Flutter?",
"options":["Dart","Python","C#"],
"answer":"Dart"},

{"question":"Cross platform framework?",
"options":["Flutter","React Native","Both"],
"answer":"Both"},

{"question":"Backend service for mobile apps?",
"options":["Firebase","Photoshop","MongoDB Compass"],
"answer":"Firebase"},

{"question":"UI building element in Flutter?",
"options":["Widgets","Tables","Layers"],
"answer":"Widgets"}
]

}


# ---------------- SKILL TEST ----------------

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
    attempted = 0
    results = []

    for i, q in enumerate(questions):

        user_answer = request.form.get(f"q{i}")
        correct_answer = q["answer"]

        if user_answer:
            attempted += 1

        is_correct = user_answer == correct_answer

        if is_correct:
            correct += 1

        results.append({
            "question": q["question"],
            "user_answer": user_answer,
            "correct_answer": correct_answer,
            "is_correct": is_correct
        })

    total_questions = len(questions)

    score = int((correct / total_questions) * 100)
    wrong_answers = [r for r in results if not r["is_correct"]]
    session["results"] = results
    session["wrong_answers"] = wrong_answers
    session["correct"] = correct
    session["attempted"] = attempted
    session["total"] = total_questions
    session["test_score"] = score

    return redirect(url_for("result_after_test"))

# ---------------- RESULT PAGE ----------------
@app.route("/result_after_test")
def result_after_test():

    score = session.get("test_score", 0)
    results = session.get("results", [])
    correct = session.get("correct", 0)
    attempted = session.get("attempted", 0)
    total = session.get("total", 0)

    missing_skills = session.get("missing_skills", [])
    role = session.get("role")
    wrong_answers = session.get("wrong_answers", [])

    if score < 60:
        message = f"You need to improve your {role} fundamentals."
    else:
        message = "Good job! Now focus on the remaining skills."

    return render_template(
        "result.html",
        score=score,
        results=results,
        wrong_answers=wrong_answers,
        correct=correct,
        attempted=attempted,
        total=total,
        missing_skills=missing_skills,
        message=message
    )
# ---------------- MENTOR DATA ----------------

mentors_data = [

{"name":"Arjun",
"skills":["html","css","react","git"],
"experience":"Frontend Developer",
"email":"Arjun@gmail.com"
},

{"name":"Priya",
"skills":["python","machine learning","sql"],
"experience":"ML Engineer",
"email":"Priya@gmail.com"
},

{"name":"Rahul",
"skills":["networking","linux","ethical hacking"],
"experience":"Cyber Security Analyst",
"email":"Rahul@gmail.com"
}

]

peer_mentors = []

@app.route("/mentors")
def mentors():

    selected_role = request.args.get("role")

    role_skills = {
        "web": ["html","css","javascript","react","git"],
        "data": ["python","pandas","numpy","machine learning","sql"],
        "ai": ["python","deep learning","tensorflow","nlp"],
        "cyber": ["networking","linux","ethical hacking","cryptography"],
        "mobile": ["flutter","dart","firebase","ui design"]
    }

    # If coming from Learn page
    if selected_role:
        missing_skills = role_skills.get(selected_role, [])
        session["missing_skills"] = missing_skills
        session["role"] = selected_role
    else:
        missing_skills = session.get("missing_skills", [])
        selected_role = session.get("role", "").lower()

    all_mentors = mentors_data + peer_mentors
    smart_matches = []

    for mentor in all_mentors:

        mentor_skills = [s.lower() for s in mentor["skills"]]

        overlap = set(mentor_skills) & set(missing_skills)

        if not missing_skills:
            continue

        match_percentage = int((len(overlap)/len(missing_skills))*100)

        role_bonus = 0

        if selected_role in mentor["experience"].lower():
            role_bonus = 10

        final_score = match_percentage + role_bonus

        matched_skills = list(overlap)

        smart_matches.append({
            "name": mentor["name"],
            "experience": mentor["experience"],
            "match_score": final_score,
            "matched_skills": matched_skills
        })

    smart_matches.sort(key=lambda x:x["match_score"], reverse=True)

    return render_template("mentors.html", mentors=smart_matches)

@app.route("/connect", methods=["POST"])
def connect():

    mentor_name = request.form["mentor_name"]

    selected_mentor = None

    all_mentors = mentors_data + peer_mentors

    for mentor in all_mentors:
        if mentor["name"] == mentor_name:
            selected_mentor = mentor
            break

    if not selected_mentor:
        return "Mentor not found"

    return render_template(
        "connection_success.html",
        mentor=selected_mentor
    )
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
@app.route("/peer_mentor")
def peer_mentor():
    return render_template("peer_mentor.html")
@app.route("/register_peer", methods=["POST"])
def register_peer():

    name = request.form["name"]
    skills = request.form["skills"]
    experience = request.form["experience"]
    email = request.form["email"]

    peer_mentors.append({
        "name": name,
        "skills": skills.lower().split(","),
        "experience": experience,
        "email": email
    })

    return redirect(url_for("mentors"))
# ---------------- RUN APP ----------------

if __name__ == "__main__":

    port = int(os.environ.get("PORT",10000))

    app.run(host="0.0.0.0", port=port)