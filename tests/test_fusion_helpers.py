"""Static checks on scripts/fusion/slab_helpers.py (it only runs inside Fusion).

The helper module is API vocabulary. It must never become a product build
script: no SLAB component names, dimensions or class geometry may live in it.
"""
import ast
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'scripts' / 'fusion' / 'slab_helpers.py'

REQUIRED = {
    'status', 'check_empty_design', 'guard', 'passed', 'health', 'save_new', 'save',
    'comp', 'plane', 'sketch', 'done', 'coll', 'allprof', 'extrude', 'fillet_edges',
    'vertical_edges', 'circles_above', 'face_at_z', 'shell', 'rect', 'circle', 'poly',
    'bar', 'profile_extent', 'reset_component', 'bbox', 'cbbox', 'radii', 'top_area',
    'make_appearance', 'find_appearance', 'assign', 'assign_component', 'appearance_tally',
    'render_setup', 'design_workspace', 'perspective_camera', 'ortho_camera',
    'project_tops', 'viewport_capture', 'capture_line_views', 'native_drawing',
}

# Product identifiers and SLAB dimensions that must stay in the spec skill.
FORBIDDEN_STRINGS = ('SLAB_Housing', 'SLAB_Panel', 'SLAB_Knob', 'SLAB_Keypad', 'SLAB_Power',
                     'SLAB_LED', 'SLAB_Gray', 'SLAB_Black', 'SLAB_Print', 'SLAB_Pointer',
                     'SLAB_Toggle', 'SLAB_Tick', 'Gfx_', 'Pad_', 'Tick_')
FORBIDDEN_NUMBERS = {195, 340, 97.5, 170, 46, 23, 3.5, 59.5, 137, 213, 135, 211, 13.5,
                     15.5, 32, 18.6, 173, 289, 1700, 152, 303}


class HelperModuleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = SRC.read_text(encoding='utf-8')
        cls.tree = ast.parse(cls.text)

    def test_compiles(self):
        compile(self.text, str(SRC), 'exec')

    def test_public_api_present(self):
        defined = {n.name for n in self.tree.body if isinstance(n, ast.FunctionDef)}
        self.assertEqual(REQUIRED - defined, set())

    def test_no_product_geometry_or_names(self):
        docstrings = set()
        for node in ast.walk(self.tree):
            if isinstance(node, (ast.Module, ast.FunctionDef)) and ast.get_docstring(node):
                docstrings.add(node.body[0].value)
        for node in ast.walk(self.tree):
            if isinstance(node, ast.Constant) and node not in docstrings:
                if isinstance(node.value, str):
                    for bad in FORBIDDEN_STRINGS:
                        self.assertNotIn(bad, node.value, 'product name in helper: %r' % node.value)
                elif isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
                    self.assertNotIn(node.value, FORBIDDEN_NUMBERS,
                                     'product dimension %r hard-coded in helper (keep it in the spec)' % node.value)

    def test_only_function_defaults_carry_tuning_values(self):
        """Exposure defaults are allowed only as keyword defaults the skill can override."""
        for node in self.tree.body:
            if isinstance(node, ast.Assign):
                for t in node.targets:
                    self.assertIn(getattr(t, 'id', ''), {'V', 'P3', 'EXPECT'})

    def test_drawing_keeps_auto_dimension_off_and_component_sheets_off(self):
        self.assertIn('g.isAutoDimensionEnabled = False', self.text)
        self.assertIn('g.isComponentSheetGenerated = False', self.text)
        self.assertNotIn('isAutoDimensionEnabled = True', self.text)


if __name__ == '__main__':
    unittest.main()
