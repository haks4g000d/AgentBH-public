import asyncio, shutil

def ensure_binaries(names):
    missing = [n for n in names if shutil.which(n) is None]
    if missing:
        raise RuntimeError(f"Missing binary/binaries: {', '.join(missing)}")

async def run(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return proc.returncode, out.decode(errors="ignore"), err.decode(errors="ignore")

async def subdomain_enum(root_domain, out_file):
    cmd = f"subfinder -d {root_domain} -silent | anew {out_file}"
    return await run(cmd)

async def probe_http(in_file, out_file, rps=50):
    cmd = f"httpx -silent -json -threads {rps} -l {in_file} > {out_file}"
    return await run(cmd)

async def crawl_urls(in_hosts_file, out_file):
    cmd = f"katana -silent -list {in_hosts_file} -json > {out_file}"
    return await run(cmd)

async def light_ports(hosts_file, out_file):
    cmd = f"naabu -list {hosts_file} -top-ports 100 -silent -json > {out_file}"
    return await run(cmd)

async def nuclei_scan(in_file, out_file, profile=None, rps=10):
    prof = f" -profile {profile}" if profile else ""
    cmd = f"nuclei -l {in_file} -json -rl {rps}{prof} > {out_file}"
    return await run(cmd)
