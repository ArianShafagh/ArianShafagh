import urllib.request
import json
import re

USERNAME = "ArianShafagh"

def fetch_repos():
    url = f"https://api.github.com/users/{USERNAME}/repos?sort=updated&per_page=100"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    try:
        with urllib.request.urlopen(req) as response:
            repos = json.loads(response.read().decode())
    except Exception as e:
        print(f"Error fetching repos: {e}")
        return "- 🤖 *Repositories auto-sync pending...*"
    
    formatted_list = []
    for repo in repos:
        # Exclude profile repository itself and forks
        if repo['name'].lower() == USERNAME.lower() or repo['fork']:
            continue
        
        desc = repo['description'] if repo['description'] else "No description provided."
        lang = f" | `{repo['language']}`" if repo['language'] else ""
        stars = f" | ⭐ {repo['stargazers_count']}" if repo['stargazers_count'] > 0 else ""
        
        entry = f"- 🚀 **[{repo['name']}]({repo['html_url']})** — {desc}{lang}{stars}"
        formatted_list.append(entry)
        
    if not formatted_list:
        return "- 🤖 *No secondary public repositories found yet. New repos will show up here automatically!*"
        
    return "\n".join(formatted_list)

def update_readme():
    repo_content = fetch_repos()
    
    with open("README.md", "r", encoding="utf-8") as file:
        readme = file.read()
        
    pattern = r"<!-- REPOS-START -->.*?<!-- REPOS-END -->"
    replacement = f"<!-- REPOS-START -->\n{repo_content}\n<!-- REPOS-END -->"
    
    updated_readme = re.sub(pattern, replacement, readme, flags=re.DOTALL)
    
    with open("README.md", "w", encoding="utf-8") as file:
        file.write(updated_readme)
        
    print("README.md successfully updated.")

if __name__ == "__main__":
    update_readme()
