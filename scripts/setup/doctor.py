"""Read-only readiness checks. --live exercises the installed Fusion connection."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--live',action='store_true');a=p.parse_args()
    failures=[]
    for name in ['numpy','PIL','reportlab','pymupdf']:
        if importlib.util.find_spec(name) is None:failures.append('Missing dependency '+name)
    state=ROOT/'.local/installation.json'
    if not state.exists():failures.append('Run setup.ps1 first')
    else:
        data=json.loads(state.read_text());checkout=Path(data['checkout'])
        if not checkout.exists():failures.append('MCP cache missing; rerun setup')
        if a.live and not failures:
            r=subprocess.run(['uv','run','--frozen','--project',str(checkout),'python',str(checkout/'scripts/smoke.py'),'--live'])
            if r.returncode:failures.append('Live MCP/API probe failed; check active Design and add-in')
    print(json.dumps({'local_ready':not failures,'live_requested':a.live,'issues':failures,'note':'Does not verify full CAD campaign or client skill discovery.'},indent=2))
    return 1 if failures else 0

if __name__=='__main__':sys.exit(main())
