# AgentBH (public)

Minimal bug-bounty helper:
- Python pipeline: `python -m agent.cli scan --program <slug>`
- Wrapper: `bin/agentbh` (repo-relative, creates ephemeral program YAMLs)
- You bring your own tools (nuclei, naabu, ffuf, katana)

## Quickstart
\`\`\`bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install typer[all] rich pydantic pyyaml httpx aiosqlite tldextract python-slugify

# install Go tools if needed
# go install github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
# go install github.com/projectdiscovery/naabu/v2/cmd/naabu@latest
# go install github.com/ffuf/ffuf@latest
# go install github.com/projectdiscovery/katana/cmd/katana@latest
# export PATH="$HOME/go/bin:$PATH"

# example scan (full pipeline, ephemeral YAML)
bin/agentbh -a -d example.com -e
\`\`\`

## Example program file (optional)
See `config/programs/example.yaml`.
