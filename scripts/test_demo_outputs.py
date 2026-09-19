"""Regression tests for output defects found in the SLAB rehearsal."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
import make_drawing
import make_views


class DrawingTests(unittest.TestCase):
    def test_preserve_calibrated_frame(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'view.png'
            im = Image.new('RGB', (100, 200), 'white')
            ImageDraw.Draw(im).rectangle((10, 20, 89, 179), outline='black')
            im.save(p)
            self.assertEqual(make_drawing.view_img(p).size, (100, 200))

    def test_blank_drawing_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / 'blank.png'
            Image.new('RGB', (100, 100), 'white').save(p)
            with self.assertRaises(ValueError):
                make_drawing.view_img(p)

    def test_blank_crop_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                make_views.save(np.zeros((100, 100)), (10, 90, 10, 90), str(Path(d)/'out.png'))

    def test_outside_crop_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):
                make_views.save(np.ones((100, 100)), (-5, 90, 10, 90), str(Path(d)/'out.png'))


if __name__ == '__main__':
    unittest.main()
