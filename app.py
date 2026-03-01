from flask import Flask, render_template,request,session,redirect

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
        "experience": "Frontend Developer"
    },
    {
        "name": "Priya",
        "skills": ["python", "machine learning", "sql"],
        "experience": "ML Engineer"
    },
    {
        "name": "Rahul",
        "skills": ["networking", "linux", "ethical hacking"],
        "experience": "Cyber Security Analyst"
    }
]
    
@app.route("/mentors")
def mentors():

    missing_skills = session.get("missing_skills", [])

    smart_matches = []

    for mentor in mentors_data:

     overlap = set(mentor["skills"]) & set(missing_skills)
     score = len(overlap)

     if score > 0:
        smart_matches.append({
            "name": mentor["name"],
            "experience": mentor["experience"],
            "match_score": score
        })

# Sort by best match first
    smart_matches.sort(key=lambda x: x["match_score"], reverse=True)

    return render_template(
        "mentors.html",
         mentors=smart_matches
    )
@app.route("/learn", methods=["GET", "POST"])
def learn():

    role_skills = {
        "web": ["html","css","javascript","react","git"],
        "data": ["python","pandas","numpy","machine learning","sql"],
        "ai": ["python","deep learning","tensorflow","nlp"],
        "cyber": ["networking","linux","ethical hacking","cryptography"],
        "mobile": ["flutter","dart","firebase","ui design"]
    }

    if request.method == "POST":
        role = request.form["role"]

        required_skills = role_skills.get(role, [])

        # Fresher has no skills
        session["missing_skills"] = required_skills
        session["role"] = role

        return redirect("/mentors")

    return render_template("learn.html", roles=role_skills)
 
            
    

if __name__ == "__main__":
    app.run(debug=True)

 