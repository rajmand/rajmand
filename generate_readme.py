import os
import json
import urllib.request
from datetime import datetime, timezone

TOKEN    = os.environ.get("GITHUB_TOKEN", "")
USERNAME = "rajmand"

def gh(url):
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def main():
    repos   = gh(f"https://api.github.com/user/repos?per_page=100&sort=pushed&affiliation=owner")
    total   = len(repos)
    public  = sum(1 for r in repos if not r["private"])
    private = total - public
    stars   = sum(r.get("stargazers_count", 0) for r in repos)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    top     = sorted(repos, key=lambda r: r.get("pushed_at") or "", reverse=True)[:6]

    lang_colors = {
        "Python": "3572A5", "Java": "b07219", "JavaScript": "f1e05a",
        "TypeScript": "2b7489", "HTML": "e34c26", "CSS": "563d7c",
        "C#": "178600", "Go": "00ADD8", "Rust": "dea584",
    }

    rows = ""
    for r in top:
        vis    = "🔒" if r["private"] else "🌐"
        lang   = r.get("language") or ""
        desc   = (r.get("description") or "No description")[:55]
        pushed = (r.get("pushed_at") or "")[:10]
        if lang and lang in lang_colors:
            lang_str = f"![{lang}](https://img.shields.io/badge/-{lang}-{lang_colors[lang]}?style=flat-square)"
        else:
            lang_str = lang
        rows += f"| {vis} [{r['name']}]({r['html_url']}) | {desc} | {lang_str} | {pushed} |\n"

    readme = f"""<div align=\"center\">

# Hi, I'm Rajmund Kovács 👋

**Software developer · Budapest, Hungary**

[![GitHub followers](https://img.shields.io/github/followers/rajmand?label=Followers&style=social)](https://github.com/rajmand)

</div>

---

## About me

I'm a software developer with a passion for tooling, backend systems and game-adjacent automation.
Building on GitHub since 2017.

- 🎮 Eve Online real-time tooling
- 🔧 Backend & REST API development
- 🗄️ Database design and practice
- 🔌 Socket / networking projects

---

## Stats

| Repos | Public | Private | Stars |
|:-----:|:------:|:-------:|:-----:|
| **{total}** | **{public}** | **{private}** | **{stars}** |

---

## Recent repositories

| | Name | Description | Language | Last push |
|--|------|-------------|----------|-----------|
{rows}
---

## Tech stack

**Languages:** Python · Java · SQL · JavaScript

**Frameworks & tools:** Spring Boot · Maven · Git · Jira

**Domains:** Eve Online tooling · REST APIs · Socket programming · Database design

---

![GitHub stats](https://github-readme-stats.vercel.app/api?username=rajmand&show_icons=true&hide_border=true&count_private=true&theme=default)

---

<sub>⚡ Auto-updated by GitHub Actions · {updated}</sub>
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"✅ README generated — {total} repos, updated at {updated}")

if __name__ == "__main__":
    main()
