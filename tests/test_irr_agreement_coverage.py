"""H4075 fix 2 (F2): partial second-annotation coverage must NOT stub the stats.

Regression for the S4 census F2 finding: file_first_verified.tsv grew 122 -> 200
rows while blind B annotations cover 122; irr_agreement.report_section used to
emit a SKIPPED stub and drop the kappas entirely. Stats must now be computed
over the covered overlap, with the uncovered rows reported, and a true stub
only on zero overlap.
"""
import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'detectors'))
import irr_agreement  # noqa: E402


def _a_rows(n):
    rows = []
    for i in range(1, n + 1):
        rows.append({'dict': 'MW', 'wrong': 'x', 'right': 'y',
                     'a': 'PASS' if i % 2 else 'DROP', 'row_id': '%03d' % i})
    return rows


class TestReportSectionCoverage(unittest.TestCase):
    def setUp(self):
        self.lines = []
        self.w = self.lines.append

    def test_partial_coverage_computes_stats(self):
        a_rows = _a_rows(200)                     # A grew to 200
        b_map = {r['row_id']: {'label': r['a'], 'reason': ''} for r in a_rows[:122]}
        irr_agreement.report_section(self.w, a_rows, b_map, 'B', 'test')
        text = '\n'.join(self.lines)
        self.assertNotIn('SKIPPED', text)
        self.assertIn('Coverage: 122 of 200', text)
        # kappa over fully-agreeing covered rows must be exactly 1
        self.assertIn("| Cohen's kappa | 1 | 1.0000 |", text)

    def test_partial_coverage_with_disagreements(self):
        a_rows = _a_rows(200)
        b_map = {r['row_id']: {'label': r['a'], 'reason': ''} for r in a_rows[:122]}
        b_map['005']['label'] = 'EDITORIAL'       # one disagreement inside the overlap
        irr_agreement.report_section(self.w, a_rows, b_map, 'B', 'test')
        text = '\n'.join(self.lines)
        self.assertNotIn('SKIPPED', text)
        self.assertIn('| 005 | MW | x | y | PASS | EDITORIAL |', text)

    def test_zero_coverage_stubs(self):
        a_rows = _a_rows(10)
        irr_agreement.report_section(self.w, a_rows, {}, 'B', 'test')
        text = '\n'.join(self.lines)
        self.assertIn('SKIPPED', text)


if __name__ == '__main__':
    unittest.main()
