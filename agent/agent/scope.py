import yaml, tldextract, re

def load_scope(path):
    with open(path,"r") as f:
        return yaml.safe_load(f)

def in_scope_url(scope, url):
    # basic domain/path checks
    ext = tldextract.extract(url)
    domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
    full = url.lower()
    allowed = False
    for item in scope.get("in_scope", []):
        if item["type"]=="domain":
            pat = item["value"].replace(".","\\.").replace("*",".*")
            if re.search(pat+"$", full):
                allowed = True
    if not allowed:
        return False
    for item in scope.get("out_of_scope", []):
        val = item["value"].rstrip("*").lower()
        if val and val in full:
            return False
    return True
