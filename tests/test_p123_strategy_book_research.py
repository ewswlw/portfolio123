import copy
import json
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from scripts import p123_strategy_book_research as research


class P123StrategyBookResearchTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.old_output = research.OUTPUT_DIR
        self.old_iteration = research.ITERATION_LOG
        self.old_today = research.TODAY
        research.OUTPUT_DIR = self.root / "p123-output"
        research.ITERATION_LOG = self.root / "iteration.md"
        research.TODAY = "20260522"
        research.ITERATION_LOG.write_text("# Iteration\n", encoding="utf-8")

    def tearDown(self):
        research.OUTPUT_DIR = self.old_output
        research.ITERATION_LOG = self.old_iteration
        research.TODAY = self.old_today
        self.tmp.cleanup()

    def output_path(self, stem: str, suffix: str = "csv") -> Path:
        return research.output_dir_for_stem(stem) / f"{stem}_20260522.{suffix}"

    def write_return_panel(self) -> Path:
        dates = pd.bdate_range("2006-01-02", periods=360)
        rows = []
        for i, dt in enumerate(dates):
            rows.append(
                {
                    "date": dt.date().isoformat(),
                    "SPY": 0.001 if i < 240 else -0.0005,
                    "QQQ": 0.0012 if i < 240 else -0.0007,
                    "SHY": 0.00005,
                    "IEF": 0.0001,
                    "SH": -0.001 if i < 240 else 0.0005,
                    "DOG": -0.0009 if i < 240 else 0.0004,
                    "PSQ": -0.0011 if i < 240 else 0.0006,
                    "strategy_1": 0.0015 if i < 240 else -0.001,
                }
            )
        path = self.output_path("return_panel")
        path.parent.mkdir(parents=True, exist_ok=True)
        pd.DataFrame(rows).to_csv(path, index=False)
        return path

    def test_dynamic_goal_requires_all_survivors_and_excludes_leverage(self):
        research.validate_dynamic_goal(research.DYNAMIC_GOAL)
        missing = copy.deepcopy(research.DYNAMIC_GOAL)
        missing["survivor_ideas"] = missing["survivor_ideas"][:-1]
        with self.assertRaises(ValueError):
            research.validate_dynamic_goal(missing)
        leveraged = copy.deepcopy(research.DYNAMIC_GOAL)
        leveraged["constraints"]["allow_leveraged_etfs"] = True
        with self.assertRaises(ValueError):
            research.validate_dynamic_goal(leveraged)

    def test_init_dynamic_goal_writes_artifact_and_iteration_entry(self):
        research.init_dynamic_goal("20260522")
        path = self.output_path("dynamic_goal_strategy_book", "json")
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["thresholds"]["sharpe_min"], 2.0)
        self.assertIn("U1 Dynamic Goal", research.ITERATION_LOG.read_text(encoding="utf-8"))

    def test_build_timing_signals_uses_shifted_benchmark_data(self):
        return_file = self.write_return_panel()
        research.build_timing_signals(return_file, "20260522")
        signal_path = self.output_path("timing_signal_panel")
        summary_path = self.output_path("timing_signal_summary", "json")
        signals = pd.read_csv(signal_path)
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
        self.assertFalse(signals.empty)
        self.assertIn("ensemble_exposure", signals.columns)
        self.assertEqual(summary["benchmark_column"], "SPY")
        self.assertIn("shifted one bar", summary["lookahead_guard"])

    def test_build_dynamic_panel_adds_timed_and_tactical_components(self):
        return_file = self.write_return_panel()
        research.build_timing_signals(return_file, "20260522")
        timing_file = self.output_path("timing_signal_panel")
        research.build_dynamic_panel(return_file, timing_file, "20260522")
        dynamic = pd.read_csv(self.output_path("dynamic_return_panel"))
        candidates = pd.read_csv(self.output_path("tactical_etf_component_candidates"))
        self.assertIn("strategy_1_timed_200d", dynamic.columns)
        self.assertIn("strategy_1_timed_ensemble", dynamic.columns)
        self.assertIn("conditional_inverse_sleeve", dynamic.columns)
        self.assertIn("tactical_etf_component", dynamic.columns)
        self.assertFalse(candidates.empty)

    def test_latest_file_prefers_task_folder_and_falls_back_to_flat_root(self):
        research.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        subdir = research.output_dir_for_stem("return_panel")
        subdir.mkdir(parents=True, exist_ok=True)
        flat = research.OUTPUT_DIR / "return_panel_20260521.csv"
        nested = subdir / "return_panel_20260522.csv"
        flat.write_text("flat\n", encoding="utf-8")
        nested.write_text("nested\n", encoding="utf-8")
        self.assertEqual(research.latest_file("return_panel", "csv"), nested)

        nested.unlink()
        self.assertEqual(research.latest_file("return_panel", "csv"), flat)


if __name__ == "__main__":
    unittest.main()
