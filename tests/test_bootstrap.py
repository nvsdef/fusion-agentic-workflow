import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

def load():
    p=ROOT/'scripts/setup/bootstrap.py'
    assert p.exists(), 'Bootstrap must be present'
    spec=importlib.util.spec_from_file_location('bootstrap',p)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    return m

class BootstrapTests(unittest.TestCase):
    def test_generate_portable_config_without_global_writes(self):
        m=load()
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)
            cfg=m.client_config(path/'mcp')
            self.assertTrue(Path(cfg['mcpServers']['fusion360']['command']).is_absolute())
            self.assertEqual(cfg['mcpServers']['fusion360']['args'],['-m','fusion360_mcp','--mode','socket'])
            self.assertFalse((path/'config.yaml').exists())

    def test_lock_rejects_moving_branch(self):
        m=load()
        with self.assertRaises(ValueError):m.validate_lock({'repository':'https://github.com/nvsdef/fusion360-mcp.git','commit':'main'})
        self.assertEqual(m.validate_lock(json.loads((ROOT/'mcp.lock.json').read_text()))['commit'],json.loads((ROOT/'mcp.lock.json').read_text())['commit'])

if __name__=='__main__':unittest.main()
