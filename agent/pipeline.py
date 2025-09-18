import os, asyncio
from agent.runners import subdomain_enum, probe_http, crawl_urls, light_ports, nuclei_scan
from agent.parsers import parse_httpx, parse_nuclei
from agent.db import insert_hosts, insert_findings
from agent.scope import in_scope_url
from agent.analysis import llm_triage, llm_report

async def run_pipeline(cfg, scope):
    program = scope["program"].lower().replace(" ","-")
    os.makedirs("data/scans", exist_ok=True)
    os.makedirs("data/reports", exist_ok=True)
    alive_file = f"data/scans/{program}_httpx.jsonl"
    nuclei_file = f"data/scans/{program}_nuclei.jsonl"
    hosts_list = f"data/raw/{program}_hosts.txt"

    # 1) subdomain enum for each in-scope domain
    with open(hosts_list, "w") as _:
        pass
    roots = []
    for item in scope.get("in_scope", []):
        if item["type"]=="domain":
            domain=item["value"].replace("*.","")
            await subdomain_enum(domain, hosts_list)
            roots.append(domain)
    # include root domains explicitly
    with open(hosts_list, "a") as f:
        for d in roots:
            f.write(d+"\n")

    # 2) probe alive
    rps = scope.get("rate_limits",{}).get("httpx_rps",50)
    await probe_http(hosts_list, alive_file, rps=rps)
    alive = parse_httpx(alive_file)
    alive = [a for a in alive if in_scope_url(scope, a["url"])]

    # 3) optional: crawl + ports (disabled by default)
    # await crawl_urls(hosts_list, f"data/scans/{program}_urls.jsonl")
    # await light_ports(hosts_list, f"data/scans/{program}_ports.jsonl")

    # 4) nuclei fast profile
    profile = cfg.get("defaults",{}).get("nuclei_profile")
    rl = scope.get("rate_limits",{}).get("nuclei_rps",10)
    await nuclei_scan(hosts_list, nuclei_file, profile=profile, rps=rl)
    nuclei = parse_nuclei(nuclei_file)

    # 5) persist
    await insert_hosts(cfg["storage"]["db_path"], program, alive)
    await insert_findings(cfg["storage"]["db_path"], program, nuclei)

    # 6) AI triage & reporting (top N)
    triaged = []
    for f in nuclei[:50]:
        t = llm_triage(cfg.get("llm",{}), f)
        triaged.append({"finding":f, "triage":t})

    report_md = llm_report(cfg.get("llm",{}), {"program": program, "triaged": triaged})
    out_md = f"data/reports/{program}_draft.md"
    with open(out_md,"w") as w:
        w.write(report_md)
    print(f"[OK] Draft report: {out_md}")
