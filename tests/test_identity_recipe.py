"""Exercise the skill's identity snippet without a live Autodesk mutation."""
import ast
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]

class IdentityRecipeTests(unittest.TestCase):
    def query(self,saved):
        text=(ROOT/'agents/cad-engineer/skills/fusion-mcp-driving/SKILL.md').read_text(encoding='utf-8')
        code=text.split('## 0 · Document identity')[1].split('```python')[1].split('```')[0]
        # Deliberately no name, product, id, or dataFile on Design/Product.
        design=SimpleNamespace(rootComponent=SimpleNamespace(bRepBodies=SimpleNamespace(count=0),occurrences=SimpleNamespace(count=0),allOccurrences=[]),timeline=SimpleNamespace(count=0))
        document=SimpleNamespace(name='Example',dataFile=SimpleNamespace(id='test-cloud-id') if saved else None)
        app=SimpleNamespace(activeDocument=document,activeProduct=SimpleNamespace(productType='DesignProductType'))
        ns={'app':app,'design':design}
        tree=ast.parse(code);last=tree.body.pop()
        exec(compile(tree,'skill','exec'),ns)
        return eval(compile(ast.Expression(last.value),'skill','eval'),ns)

    def test_unsaved_document(self):
        result=self.query(False)
        self.assertEqual(result['document'],'Example')
        self.assertFalse(result['saved'])
        self.assertIsNone(result['data_file_id'])

    def test_saved_document(self):
        result=self.query(True)
        self.assertTrue(result['saved'])
        self.assertEqual(result['data_file_id'],'test-cloud-id')

if __name__=='__main__':unittest.main()
