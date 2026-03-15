import os
import json
import urllib.request
from datetime import datetime, timezone

TOKEN    = os.environ.get("GITHUB_TOKEN", "")
USERNAME = "rajmand"

def gh(url):
    headers = {"Accept": "application/vnd.github+json"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def lang_badge(lang):
    colors = {
        "Python": "3572A5", "Java": "b07219", "JavaScript": "f1e05a",
        "TypeScript": "2b7489", "HTML": "e34c26", "CSS": "563d7c",
        "C#": "178600", "Go": "00ADD8", "Rust": "dea584",
    }
    if not lang:
        return ""
    color = colors.get(lang, "888888")
    return f"![{lang}](https://img.shields.io/badge/-{lang.replace(' ', '%20')}-{color}?style=flat-square)"

def main():
    # Public endpoint - works with default GITHUB_TOKEN in Actions
    repos   = gh(f"https://api.github.com/users/{USERNAME}/repos?per_page=100&sort=pushed&type=owner")
    total   = len(repos)
    public  = sum(1 for r in repos if not r["private"])
    private = total - public
    stars   = sum(r.get("stargazers_count", 0) for r in repos)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    top     = sorted(repos, key=lambda r: r.get("pushed_at") or "", reverse=True)[:6]

    rows = ""
    for r in top:
        vis    = "\U0001f512" if r["private"] else "\U0001f310"
        lang   = r.get("language") or ""
        desc   = (r.get("description") or "No description")[:55]
        pushed = (r.get("pushed_at") or "")[:10]
        rows  += f"| {vis} [{r['name']}]({r['html_url']}) | {desc} | {lang_badge(lang)} | {pushed} |\n"

    readme = f"""<div align=\"center\">

# Rajmund Kov\u00e1cs

**Senior Software Engineer \u00b7 Budapest, Hungary**

[![GitHub followers](https://img.shields.io/github/followers/rajmand?label=Followers&style=social)](https://github.com/rajmand)
[![Email](https://img.shields.io/badge/email-kovacs.rajmund@gmail.com-blue?style=flat&logo=gmail&logoColor=white)](mailto:kovacs.rajmund@gmail.com)

</div>

---

## About me

Senior Software Engineer with 10+ years building scalable backend systems and microservice architectures. Recently specializing in **LLM-powered platforms**, AI agent frameworks, and RAG pipelines.

---

## What I do

- \U0001f916 Design and build **LLM-powered autonomous agent** systems
- \U0001f517 Implement **RAG pipelines** with vector & graph retrieval (Langchain4j)
- \U0001f3d7\ufe0f Architect **microservice backends** for large-scale production systems
- \u2601\ufe0f Deploy and optimize on **Azure, AWS, Oracle Cloud**
- \U0001f527 Lead **CI/CD, Docker, Kubernetes** workflows
- \U0001f9d1\u200d\U0001f3eb Mentor teams and coach Agile practices

---

## Tech stack

**Languages**
![Java](https://img.shields.io/badge/Java-b07219?style=flat-square&logo=openjdk&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-4479A1?style=flat-square&logo=postgresql&logoColor=white)
![C#](https://img.shields.io/badge/C%23-.NET-178600?style=flat-square&logo=dotnet&logoColor=white)

**Frameworks**
![Spring Boot](https://img.shields.io/badge/Spring_Boot-6DB33F?style=flat-square&logo=springboot&logoColor=white)
![Spring Security](https://img.shields.io/badge/Spring_Security-6DB33F?style=flat-square&logo=spring&logoColor=white)
![Spring Cloud](https://img.shields.io/badge/Spring_Cloud-6DB33F?style=flat-square&logo=spring&logoColor=white)

**AI / LLM**
![LangChain](https://img.shields.io/badge/Langchain4j-000000?style=flat-square&logo=chainlink&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI_SDK-412991?style=flat-square&logo=openai&logoColor=white)
![Claude](https://img.shields.io/badge/Claude_SDK-D4A96A?style=flat-square)
![RAG](https://img.shields.io/badge/RAG_Pipelines-informational?style=flat-square)
![MCP](https://img.shields.io/badge/MCP-Model_Context_Protocol-blueviolet?style=flat-square)

**Cloud & DevOps**
![Azure](https://img.shields.io/badge/Azure-0078D4?style=flat-square&logo=microsoftazure&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Kubernetes](https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=flat-square&logo=jenkins&logoColor=white)
![GitLab CI](https://img.shields.io/badge/GitLab_CI-FC6D26?style=flat-square&logo=gitlab&logoColor=white)

**Databases**
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat-square&logo=mysql&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle_SQL-F80000?style=flat-square&logo=oracle&logoColor=white)
![Elastic](https://img.shields.io/badge/Elasticsearch-005571?style=flat-square&logo=elasticsearch&logoColor=white)

**Orchestration**
![Temporal](https://img.shields.io/badge/Temporal-000000?style=flat-square)

---

## My repositories

| | Name | Description | Language | Last push |
|--|------|-------------|----------|-----------|
{rows}
---

![GitHub stats](https://github-readme-stats.vercel.app/api?username=rajmand&show_icons=true&hide_border=true&count_private=true&theme=default)

---

<sub>\u26a1 Auto-updated by GitHub Actions \u00b7 {updated}</sub>
"""

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme)
    print(f"\u2705 README generated \u2014 {total} repos, updated at {updated}")

if __name__ == "__main__":
    main()
