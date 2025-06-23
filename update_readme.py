# update_readme.py

import requests
from datetime import datetime

USERNAME = "gursmeep404"
BIRTHDATE = datetime(2004, 1, 16)

def get_github_stats(username):
    user = requests.get(f"https://api.github.com/users/{username}").json()
    repos = requests.get(f"https://api.github.com/users/{username}/repos?per_page=100").json()

    total_stars = sum(repo.get("stargazers_count", 0) for repo in repos)

    events = requests.get(f"https://api.github.com/users/{username}/events/public").json()
    total_commits = sum(1 for e in events if e["type"] == "PushEvent")

    return {
        "public_repos": user.get("public_repos", 0),
        "stars": total_stars,
        "commits": total_commits,
    }

def calculate_age(birthdate):
    today = datetime.utcnow()
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def build_readme(stats, age):
    content = f"""<!-- AUTO-GENERATED FILE. DO NOT EDIT DIRECTLY. -->

```bash
gurmeep@github
------------------------------
OS: Human Being 🧠
Age: {age}
Location: None
Languages: HTML, CSS, JS, Python, C, C++, SQL
Frameworks: Flask, React, PyTorch, scikit-learn
Tools: Linux, MSF, GitHub
------------------------------
Public Repos : {stats['public_repos']}
Total Commits: {stats['commits']}
Stars Given  : {stats['stars']}
Lines of Code: Unknown
------------------------------
💬 I build cool AI & cybersec projects!
"""