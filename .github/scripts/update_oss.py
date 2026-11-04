import json, re, subprocess

USER = "Gowtham1256"
ORG = "zephyrproject-rtos"


def prs(flag):
    out = subprocess.check_output(
        ["gh", "search", "prs", "--author", USER, flag, "--owner", ORG, "--limit", "100",
         "--json", "number,title,url,repository,createdAt"], text=True)
    return json.loads(out)


found = {p["url"]: p for f in ("--merged", "--state=open") for p in prs(f)}
rows = []
for p in sorted(found.values(), key=lambda p: p["createdAt"], reverse=True):
    repo = p["repository"]["nameWithOwner"]
    title = p["title"].replace("|", "\\|")
    badge = f"![](https://img.shields.io/github/issues/detail/state/{repo}/{p['number']}?label=)"
    rows.append(f"| [{repo.split('/')[1]}#{p['number']}]({p['url']}) | {title} | {badge} |")

table = "| PR | Change | Status |\n|----|--------|--------|\n" + "\n".join(rows)
text = open("README.md").read()
new = re.sub(r"(<!-- OSS:START -->\n).*?(\n<!-- OSS:END -->)",
             lambda m: m[1] + table + m[2], text, flags=re.S)
open("README.md", "w").write(new)
