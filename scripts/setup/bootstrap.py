"""Host-local dependency setup. No CAD operations or global client writes."""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
TOOLS=['ping','get_design_type','execute_code','render_view','start_render','get_render_status','set_scene_environment','create_drawing']

def validate_lock(lock):
    if lock.get('repository')!='https://github.com/nvsdef/fusion360-mcp.git':
        raise ValueError('Unexpected MCP source; review lock changes before installation')
    if not re.fullmatch('[0-9a-f]{40}',lock.get('commit','')):
        raise ValueError('MCP must be pinned to a full commit SHA')
    return lock

def client_config(checkout):
    python=checkout/('.venv/Scripts/python.exe' if os.name=='nt' else '.venv/bin/python')
    return {'mcpServers':{'fusion360':{'command':str(python.resolve()),'args':['-m','fusion360_mcp','--mode','socket'],'env':{'FUSION_MCP_HOST':'127.0.0.1','FUSION_MCP_PORT':'9876'}}}}

def run(*args):
    subprocess.run([str(x) for x in args],check=True)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--skip-addin',action='store_true')
    p.add_argument('--replace-addin',action='store_true')
    p.add_argument('--addin-target',type=Path)
    p.add_argument('--cache-dir',type=Path)
    a=p.parse_args()
    if sys.platform!='win32' and not a.skip_addin and a.addin_target is None:
        p.error('Automatic add-in installation is supported on Windows only')
    for cmd in ['git','uv']:
        if not shutil.which(cmd):p.error(cmd+' is required; see SETUP.md')
    lock=validate_lock(json.loads((ROOT/'mcp.lock.json').read_text()))
    cache=a.cache_dir or Path(os.environ.get('LOCALAPPDATA',Path.home()/'.cache'))/'fusion-product-development'
    checkout=cache/('mcp-'+lock['commit'][:12])
    if not checkout.exists():
        cache.mkdir(parents=True,exist_ok=True)
        run('git','clone',lock['repository'],checkout)
        run('git','-C',checkout,'checkout','--detach',lock['commit'])
    head=subprocess.check_output(['git','-C',str(checkout),'rev-parse','HEAD'],text=True).strip()
    if head!=lock['commit']:raise RuntimeError('Cached MCP revision differs; refusing to overwrite')
    dirty=subprocess.check_output(['git','-C',str(checkout),'status','--porcelain','--untracked-files=no'],text=True).strip()
    if dirty:raise RuntimeError('Cached MCP contains tracked edits; refusing to install')
    run('uv','sync','--frozen','--project',checkout)
    run('uv','run','--frozen','--project',checkout,'python',checkout/'scripts/smoke.py')
    if not a.skip_addin:
        args=['uv','run','--frozen','--project',str(checkout),'python',str(checkout/'scripts/install_addin.py')]
        if a.addin_target:args+=['--target',str(a.addin_target.resolve())]
        if a.replace_addin:args+=['--replace']
        run(*args)
    out=ROOT/'.local';out.mkdir(exist_ok=True)
    config=client_config(checkout)
    (out/'mcp-client.json').write_text(json.dumps(config,indent=2),encoding='utf-8')
    (out/'installation.json').write_text(json.dumps({'checkout':str(checkout.resolve()),'commit':head,'addin_installed':not a.skip_addin,'addin_target':str(a.addin_target.resolve()) if a.addin_target else 'default','live_verified':False},indent=2),encoding='utf-8')
    print('PREPARED: '+str(out/'mcp-client.json'))
    print('Next: enable add-in in Fusion; close dialog; register MCP with client consent; run doctor --live.')
    print('No global Hermes configuration, identity, credentials or approval settings were modified.')

if __name__=='__main__':main()
