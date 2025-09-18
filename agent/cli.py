from typer import Typer, Option
from rich import print
import asyncio, yaml
from agent.pipeline import run_pipeline
from agent.db import init_db
from agent.scope import load_scope
from agent.runners import ensure_binaries

app = Typer(help="Bug Bounty AI Agent")

def load_agent_cfg():
    with open("config/agent.yaml", "r") as f:
        return yaml.safe_load(f)

@app.command()
def init():
    """Initialize DB and sanity-check tool binaries."""
    cfg = load_agent_cfg()
    init_db(cfg["storage"]["db_path"])
    ensure_binaries(["subfinder","httpx","nuclei","naabu","dnsx","katana"])
    print("[green]DB ready & binaries OK.[/green]")

@app.command()
def scan(program: str = Option(..., help="Program slug, e.g., exoscale")):
    """Run full pipeline for a program."""
    cfg = load_agent_cfg()
    scope = load_scope(f"config/programs/{program}.yaml")
    asyncio.run(run_pipeline(cfg, scope))

if __name__ == "__main__":
    app()
