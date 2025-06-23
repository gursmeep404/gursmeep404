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
    content = f"""

```bash
gurmeep@github
------------------------------
OS: Human Being 
Age: {age}
Location: None
Languages: Python, C, C++, JS, SQL, HTML/CSS
Frameworks: Flask, React, PyTorch, scikit-learn
Tools: Linux, MSF, GitHub
------------------------------
Public Repos : {stats['public_repos']}
Total Commits: {stats['commits']}
Stars Given  : {stats['stars']}
Lines of Code: Unknown
------------------------------


---

Create the following folder and file in your repo:


Paste this in `update.yml`:

```yaml
name: Update README

on:
  schedule:
    - cron: "0 0 * * *"
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.10"

      - name: Install dependencies
        run: pip install requests

      - name: Run script
        run: python update_readme.py

      - name: Commit changes
        run: |
          git config --global user.name "github-actions[bot]"
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          git commit -m " Auto-update README" || echo "No changes to commit"
          git push
