"""Scoped editor for `hermes config edit`; changes only skills.external_dirs."""
import json
import os
import sys
from pathlib import Path
import yaml

path=Path(sys.argv[-1])
config=yaml.safe_load(path.read_text(encoding='utf-8')) or {}
dirs=json.loads(os.environ['FUSION_SKILL_DIRS_JSON'])
if not isinstance(dirs,list) or not all(isinstance(v,str) for v in dirs):raise ValueError('Expected path list')
config.setdefault('skills',{})['external_dirs']=dirs
path.write_text(yaml.safe_dump(config,sort_keys=False,allow_unicode=True),encoding='utf-8')
