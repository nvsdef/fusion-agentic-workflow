"""Regression tests for output defects found in the SLAB rehearsal."""
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
import json
import make_drawing
import make_views
import pad_roi


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


class SheetTemplateTests(unittest.TestCase):
    """28 Oct 2026: a stale date/model and padded extents shipped as 'measured'."""

    def test_unfilled_template_rejected(self):
        spec = json.loads(Path(__file__).with_name('slab_sheet.json').read_text(encoding='utf-8'))
        with self.assertRaises(ValueError):
            make_drawing.check_filled(spec)

    def test_filled_template_accepted(self):
        spec = {'title_block': {'date': '28 OCT 2026', 'model': 'SLAB_TOP_v4  (289 bodies)'}}
        make_drawing.check_filled(spec)

    def test_template_uses_measured_extents_and_no_invented_material(self):
        spec = json.loads(Path(__file__).with_name('slab_sheet.json').read_text(encoding='utf-8'))
        texts = [d.get('text', '') for d in spec['dims']]
        self.assertIn('61.15 OVERALL', texts)
        self.assertNotIn('61.21 OVERALL', texts)
        self.assertTrue(all(r[4] == 'TBD' for r in spec['parts_list']['rows']))


class PadRoiTests(unittest.TestCase):
    """28 Oct 2026: colour thresholds counted orange knobs and the LED as pads."""

    def _frame(self, pad_rgb, decoy_rgb=(245, 122, 72)):
        img = np.full((600, 960, 3), 176, np.uint8)
        pads = []
        for i in range(10):
            x, y = 60 + i * 80, 300
            img[y - 12:y + 13, x - 12:x + 13] = pad_rgb
            pads.append([x, y])
        img[100:160, 100:160] = decoy_rgb          # a big orange 'knob' decoy
        return img, {'vp': [960, 600], 'pads': pads}

    def test_measures_only_projected_pads(self):
        img, rois = self._frame((255, 140, 70))
        r = pad_roi.measure(img, rois)
        self.assertAlmostEqual(r['gr_mean'], 140 / 255, places=3)
        self.assertTrue(r['pass_spread'])
        self.assertTrue(r['red_clipped'])

    def test_scales_with_render_height(self):
        img, rois = self._frame((250, 138, 60))
        big = np.asarray(Image.fromarray(img).resize((1920, 1200), Image.NEAREST))
        r = pad_roi.measure(big, rois)
        self.assertEqual(r['size'], [1920, 1200])
        self.assertAlmostEqual(r['gr_mean'], 138 / 250, places=3)
        self.assertTrue(r['pass_gr'])

    def test_wrong_pad_count_rejected(self):
        img, rois = self._frame((255, 140, 70))
        rois['pads'] = rois['pads'][:9]
        with self.assertRaises(ValueError):
            pad_roi.measure(img, rois)

    def test_aspect_mismatch_rejected(self):
        img, rois = self._frame((255, 140, 70))
        with self.assertRaises(ValueError):
            pad_roi.measure(img[:, :700], rois)


if __name__ == '__main__':
    unittest.main()
