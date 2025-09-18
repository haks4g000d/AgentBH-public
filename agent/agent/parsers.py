import json

def load_json_lines(path):
    with open(path, "r", errors="ignore") as f:
        for line in f:
            line=line.strip()
            if not line: 
                continue
            try:
                yield json.loads(line)
            except Exception:
                continue

def parse_httpx(path):
    alive = []
    for obj in load_json_lines(path):
        url = obj.get("url")
        tech = obj.get("tech", [])
        if url:
            alive.append({"url": url, "tech": tech})
    return alive

def parse_nuclei(path):
    findings = []
    for obj in load_json_lines(path):
        findings.append({
            "template": obj.get("template-id"),
            "name": obj.get("info", {}).get("name"),
            "severity": obj.get("info", {}).get("severity"),
            "matched": obj.get("matched-at"),
            "extracted": obj.get("extracted-results"),
            "curl": obj.get("curl-command"),
            "evidence": obj.get("matcher-name"),
        })
    return findings
