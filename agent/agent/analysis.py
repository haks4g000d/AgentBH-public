import json, subprocess

def _ollama_chat(model, system, user):
    prompt = f"<<SYS>>{system}\n<<USER>>{user}"
    out = subprocess.check_output(["ollama","run",model], input=prompt.encode(), stderr=subprocess.DEVNULL)
    return out.decode()

def llm_triage(llm_cfg, finding):
    system = "You strictly follow instructions and output compact JSON only."
    user = json.dumps(finding) + "\nReturn ONLY JSON following schema in prompt."
    if llm_cfg.get("provider")=="ollama":
        raw = _ollama_chat(llm_cfg.get("model","llama3.1:8b"), system, user)
        try:
            s = raw.find("{"); e = raw.rfind("}")
            return json.loads(raw[s:e+1])
        except Exception:
            return {"validity":"unsure","reality_severity":"low","manual_steps":[],"notes":"parse error"}
    else:
        # placeholder for other providers
        return {"validity":"unsure","reality_severity":"low","manual_steps":[],"notes":"no provider configured"}

def llm_report(llm_cfg, finding_bundle):
    system = "You output only valid GitHub-Flavored Markdown."
    user = json.dumps(finding_bundle)
    if llm_cfg.get("provider")=="ollama":
        return _ollama_chat(llm_cfg.get("model","llama3.1:8b"), system, user)
    return "# Report\n\nLLM not configured."
