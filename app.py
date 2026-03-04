from flask import Flask, render_template,request,session,redirect,url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template("index.html")
@app.route("/analyzer")
def analyzer():
     roles = {
        "web": "Web Developer",
        "data": "Data Scientist",
        "ai": "AI Engineer",
        "cyber": "Cyber Security Analyst", 
        "mobile": "Mobile App Developer"

    }

     return render_template("analyzer.html", roles=roles)
@app.route("/analyze", methods=["POST"])
def analyze():

    role = request.form["role"]
    user_skills = request.form["skills"]

    user_skills_list = user_skills.split(",")
    user_skills_list = [skill.strip().lower() for skill in user_skills_list]

    role_skills = {
        "web": ["html","css","javascript","react","git"],
        "data": ["python","pandas","numpy","machine learning","sql"],
        "ai": ["python","deep learning","tensorflow","nlp"],
        "cyber": ["networking","linux","ethical hacking","cryptography"],
        "mobile": ["flutter","dart","firebase","ui design"]
    }

    required_skills = role_skills.get(role, [])

    missing_skills = []

    for skill in required_skills:
        if skill not in user_skills_list:
            missing_skills.append(skill)
    session["missing_skills"] = missing_skills
    session["role"] = role        

    total_skills=len(required_skills)
    missing_count=len(missing_skills)
    matched_count=total_skills-missing_count
    percentage=int((matched_count/total_skills)*100)     
    is_perfect_match = False

    if percentage == 100:
     is_perfect_match = True
    return render_template("result.html", missing_skills=missing_skills,percentage=percentage,is_perfect_match=is_perfect_match,selected_role=role)
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
            role_bonus = 10   # small intelligent boost

        final_score = match_percentage + role_bonus

        if final_score > 0:
            smart_matches.append({
                "name": mentor["name"],
                "experience": mentor["experience"],
                "match_score": final_score
            })

    smart_matches.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template("mentors.html", mentors=smart_matches)
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
@app.route("/connect", methods=["POST"])
def connect():
    mentor_name = request.form["mentor_name"]

    # find mentor details
    selected_mentor = None
    for mentor in mentors_data:
        if mentor["name"] == mentor_name:
            selected_mentor = mentor
            break

    if not selected_mentor:
        return "Mentor not found"

    # Here you could store request in DB later
    # For now just simulate request success

    return render_template(
        "connection_success.html",
        mentor=selected_mentor
    )
if __name__ == "__main__":
    app.run(debug=True)
