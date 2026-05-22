"""
API-only Portfolio123 Strategy Book candidate research pipeline.

This script is intentionally artifact-first: each command writes dated CSV/JSON
outputs under p123-output so the research can be audited and resumed.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "p123-output"
ITERATION_LOG = ROOT / "iteration.md"
TODAY = date.today().strftime("%Y%m%d")


GOAL = {
    "name": "api_only_p123_strategy_book",
    "created_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),
    "description": (
        "Design an API-estimated Portfolio123 Strategy Book candidate from eligible "
        "simulated strategies and pre-2007 ETFs, including inverse ETFs."
    ),
    "thresholds": {
        "cagr_min": 0.20,
        "sharpe_min": 1.60,
        "psr_min": 0.95,
        "dsr_min": 0.95,
    },
    "constraints": {
        "candidate_strategy_sharpe_gt": 1.0,
        "candidate_strategy_inception_before": "2007-01-01",
        "max_component_weight": 0.25,
        "max_inverse_sleeve_weight": 0.35,
        "allow_inverse_etfs": True,
        "allow_leveraged_etfs": False,
        "api_credit_stop": 250,
        "final_label": "API-estimated candidate research, not native Tier 1 Strategy Book validation",
    },
    "optimizer_ladder": [
        "equal_weight",
        "inverse_volatility",
        "hrp",
        "constrained_ensemble",
    ],
}

DYNAMIC_GOAL = {
    "name": "dynamic_p123_strategy_book",
    "created_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),
    "description": (
        "Design API-estimated dynamic Portfolio123 Strategy Book candidates using "
        "expanded pre-2007 strategy discovery, P123-native timing signals, "
        "conditional inverse ETF exposure, and a tactical ETF component."
    ),
    "thresholds": {
        "cagr_min": 0.20,
        "sharpe_min": 2.00,
        "max_drawdown_min": -0.25,
        "psr_min": 0.95,
        "dsr_min": 0.95,
    },
    "constraints": {
        "candidate_strategy_sharpe_gt": 1.0,
        "candidate_strategy_inception_before": "2007-01-01",
        "allow_inverse_etfs": True,
        "allow_leveraged_etfs": False,
        "final_label": "API-estimated nomination only; native P123 Strategy Book validation required",
        "object_prefix": "codex_",
    },
    "survivor_ideas": [
        "risk_on_risk_off_overlay",
        "conditional_inverse_bear_sleeve",
        "codex_tactical_etf_rotation_component",
        "expanded_pre_2007_strategy_discovery",
        "macro_stress_gate_with_p123_fred_constants",
        "api_screening_then_native_tier_1_validation",
        "small_timing_signal_ensemble",
    ],
    "trial_accounting": {
        "discovery_source": "each distinct SIM/category/source inspected",
        "timing_rule": "each binary timing rule variant tested",
        "timing_ensemble": "each ensemble exposure rule tested",
        "etf_component": "each tactical ETF component variant tested",
        "allocation": "each optimizer row tested",
    },
}

TECHNICAL_TIMING_RULES = [
    {
        "name": "bench_above_200d",
        "formula_intent": "Close(0,#Bench) > SMA(200,0,#Bench)",
        "warmup_bars": 200,
        "trial_count": 1,
    },
    {
        "name": "bench_50d_above_200d",
        "formula_intent": "SMA(50,0,#Bench) > SMA(200,0,#Bench)",
        "warmup_bars": 200,
        "trial_count": 1,
    },
    {
        "name": "bench_12m_momentum_positive",
        "formula_intent": "Close(0,#Bench) / Close(251,#Bench) - 1 > 0",
        "warmup_bars": 252,
        "trial_count": 1,
    },
    {
        "name": "bench_drawdown_under_20pct",
        "formula_intent": "Close(0,#Bench) / HiValue(252,0,#Bench) > 0.80",
        "warmup_bars": 252,
        "trial_count": 1,
    },
    {
        "name": "bench_volatility_below_median",
        "formula_intent": "Volatility(63,#Bench) below trailing median",
        "warmup_bars": 252,
        "trial_count": 1,
    },
]

MACRO_STRESS_CANDIDATES = [
    {
        "name": "yield_curve_not_inverted",
        "formula_intent": "##UST10YR - ##UST2YR > 0",
        "status": "requires_p123_macro_series_confirmation",
        "trial_count": 0,
    },
    {
        "name": "credit_spread_not_widening",
        "formula_intent": "##CORPBBOAS below trailing stress threshold",
        "status": "requires_p123_macro_series_confirmation",
        "trial_count": 0,
    },
    {
        "name": "inflation_pressure_not_rising",
        "formula_intent": "##CPI trend not accelerating",
        "status": "requires_p123_macro_series_confirmation",
        "trial_count": 0,
    },
]


ETF_SEEDS = [
    # Broad US equity
    {"ticker": "SPY", "family": "us_broad_equity", "inverse": False, "leveraged": False},
    {"ticker": "DIA", "family": "us_broad_equity", "inverse": False, "leveraged": False},
    {"ticker": "QQQ", "family": "us_growth_equity", "inverse": False, "leveraged": False},
    {"ticker": "IWM", "family": "us_small_cap", "inverse": False, "leveraged": False},
    {"ticker": "IWB", "family": "us_large_cap", "inverse": False, "leveraged": False},
    {"ticker": "IWD", "family": "us_value", "inverse": False, "leveraged": False},
    {"ticker": "IWF", "family": "us_growth", "inverse": False, "leveraged": False},
    {"ticker": "MDY", "family": "us_mid_cap", "inverse": False, "leveraged": False},
    {"ticker": "IJR", "family": "us_small_cap", "inverse": False, "leveraged": False},
    # Sectors
    {"ticker": "XLB", "family": "sector_materials", "inverse": False, "leveraged": False},
    {"ticker": "XLE", "family": "sector_energy", "inverse": False, "leveraged": False},
    {"ticker": "XLF", "family": "sector_financials", "inverse": False, "leveraged": False},
    {"ticker": "XLI", "family": "sector_industrials", "inverse": False, "leveraged": False},
    {"ticker": "XLK", "family": "sector_technology", "inverse": False, "leveraged": False},
    {"ticker": "XLP", "family": "sector_staples", "inverse": False, "leveraged": False},
    {"ticker": "XLU", "family": "sector_utilities", "inverse": False, "leveraged": False},
    {"ticker": "XLV", "family": "sector_healthcare", "inverse": False, "leveraged": False},
    {"ticker": "XLY", "family": "sector_discretionary", "inverse": False, "leveraged": False},
    # International
    {"ticker": "EFA", "family": "international_developed", "inverse": False, "leveraged": False},
    {"ticker": "EEM", "family": "international_emerging", "inverse": False, "leveraged": False},
    {"ticker": "EWJ", "family": "country_japan", "inverse": False, "leveraged": False},
    {"ticker": "EWG", "family": "country_germany", "inverse": False, "leveraged": False},
    {"ticker": "EWU", "family": "country_uk", "inverse": False, "leveraged": False},
    {"ticker": "EWC", "family": "country_canada", "inverse": False, "leveraged": False},
    {"ticker": "EWA", "family": "country_australia", "inverse": False, "leveraged": False},
    {"ticker": "EWH", "family": "country_hong_kong", "inverse": False, "leveraged": False},
    {"ticker": "FXI", "family": "country_china", "inverse": False, "leveraged": False},
    # Fixed income
    {"ticker": "AGG", "family": "bond_aggregate", "inverse": False, "leveraged": False},
    {"ticker": "SHY", "family": "bond_short_treasury", "inverse": False, "leveraged": False},
    {"ticker": "IEF", "family": "bond_intermediate_treasury", "inverse": False, "leveraged": False},
    {"ticker": "TLT", "family": "bond_long_treasury", "inverse": False, "leveraged": False},
    {"ticker": "LQD", "family": "bond_investment_grade_credit", "inverse": False, "leveraged": False},
    # Real assets
    {"ticker": "GLD", "family": "gold", "inverse": False, "leveraged": False},
    {"ticker": "SLV", "family": "silver", "inverse": False, "leveraged": False},
    {"ticker": "DBC", "family": "commodities", "inverse": False, "leveraged": False},
    {"ticker": "IYR", "family": "real_estate", "inverse": False, "leveraged": False},
    {"ticker": "VNQ", "family": "real_estate", "inverse": False, "leveraged": False},
    # Inverse ETFs. Leveraged inverse ETFs are deliberately excluded.
    {"ticker": "SH", "family": "inverse_sp500", "inverse": True, "leveraged": False},
    {"ticker": "DOG", "family": "inverse_dow", "inverse": True, "leveraged": False},
    {"ticker": "PSQ", "family": "inverse_nasdaq100", "inverse": True, "leveraged": False},
]


@dataclass
class SimStrategyRow:
    strategy_id: str
    name: str
    displayed_sharpe: float | None
    inception_date: str | None
    included: bool
    reason: str
    raw_text: str = ""


def ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def dated_path(stem: str, suffix: str, run_date: str = TODAY) -> Path:
    ensure_output_dir()
    return OUTPUT_DIR / f"{stem}_{run_date}.{suffix}"


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True, default=str), encoding="utf-8")


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    rows = list(rows)
    if fieldnames is None:
        fieldnames = sorted({key for row in rows for key in row.keys()})
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def append_iteration(section: str, lines: list[str]) -> None:
    timestamp = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z")
    body = [f"\n## {section}", "", f"Updated: {timestamp}", *lines, ""]
    ITERATION_LOG.write_text(ITERATION_LOG.read_text(encoding="utf-8") + "\n".join(body), encoding="utf-8")


def init_goal(run_date: str = TODAY) -> None:
    ensure_output_dir()
    goal_path = dated_path("goal_api_only_strategy_book", "json", run_date)
    credit_path = dated_path("api_credit_budget", "json", run_date)
    budget = {
        "created_at": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M %Z"),
        "credit_stop": GOAL["constraints"]["api_credit_stop"],
        "stoplights": {
            "green": {
                "description": "Minimal auth, quota, config, and metadata checks",
                "estimated_credits": "0-25",
            },
            "yellow": {
                "description": "Targeted strategy detail and ETF price-history pulls",
                "estimated_credits": "26-250",
            },
            "red": {
                "description": "Broad/repeated calls or any run estimated above the stop threshold",
                "requires_user_confirmation": True,
            },
        },
        "actual_calls": [],
    }
    write_json(goal_path, GOAL)
    write_json(credit_path, budget)
    append_iteration(
        "U1 Goal And Credit Scaffold",
        [
            f"- Wrote `{goal_path.as_posix()}`.",
            f"- Wrote `{credit_path.as_posix()}`.",
            "- Credit stop remains 250 estimated Portfolio123 API credits before asking for confirmation.",
        ],
    )


def validate_dynamic_goal(goal: dict[str, Any]) -> None:
    required_ideas = {
        "risk_on_risk_off_overlay",
        "conditional_inverse_bear_sleeve",
        "codex_tactical_etf_rotation_component",
        "expanded_pre_2007_strategy_discovery",
        "macro_stress_gate_with_p123_fred_constants",
        "api_screening_then_native_tier_1_validation",
        "small_timing_signal_ensemble",
    }
    missing = required_ideas - set(goal.get("survivor_ideas", []))
    if missing:
        raise ValueError(f"Dynamic goal missing survivor ideas: {', '.join(sorted(missing))}")
    constraints = goal.get("constraints", {})
    if constraints.get("allow_leveraged_etfs"):
        raise ValueError("Dynamic plan excludes leveraged and leveraged-inverse ETFs")
    thresholds = goal.get("thresholds", {})
    for key in ["cagr_min", "sharpe_min", "max_drawdown_min", "psr_min", "dsr_min"]:
        if key not in thresholds:
            raise ValueError(f"Dynamic goal missing threshold: {key}")


def init_dynamic_goal(run_date: str = TODAY) -> None:
    ensure_output_dir()
    validate_dynamic_goal(DYNAMIC_GOAL)
    goal_path = dated_path("dynamic_goal_strategy_book", "json", run_date)
    write_json(goal_path, DYNAMIC_GOAL)
    append_iteration(
        "U1 Dynamic Goal And Trial Accounting",
        [
            f"- Wrote `{goal_path.as_posix()}`.",
            "- Captured all seven dynamic ideation survivors.",
            "- Trial accounting now explicitly includes discovery sources, timing rules, timing ensembles, ETF component variants, and allocation rows.",
            "- Dynamic results remain API-estimated nominations until native Portfolio123 Strategy Book validation.",
        ],
    )


def parse_float(text: str | None) -> float | None:
    if text is None:
        return None
    cleaned = re.sub(r"[^0-9.\-]", "", text)
    if cleaned in {"", ".", "-", "-."}:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None


def normalize_date(text: str | None) -> str | None:
    if not text:
        return None
    text = text.strip()
    patterns = [
        ("%Y-%m-%d", r"\d{4}-\d{2}-\d{2}"),
        ("%m/%d/%Y", r"\d{1,2}/\d{1,2}/\d{4}"),
        ("%m/%d/%y", r"\d{1,2}/\d{1,2}/\d{2}"),
    ]
    for fmt, regex in patterns:
        m = re.search(regex, text)
        if not m:
            continue
        try:
            return datetime.strptime(m.group(0), fmt).date().isoformat()
        except ValueError:
            continue
    return None


def include_strategy(sharpe: float | None, inception: str | None) -> tuple[bool, str]:
    if sharpe is None:
        return False, "missing_sharpe"
    if sharpe <= GOAL["constraints"]["candidate_strategy_sharpe_gt"]:
        return False, "sharpe_not_gt_1"
    if inception is None:
        return False, "missing_inception"
    if inception >= GOAL["constraints"]["candidate_strategy_inception_before"]:
        return False, "inception_not_before_2007"
    return True, "included"


def load_discovery_rows(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(payload, dict) and "rows" in payload:
        rows = payload["rows"]
    elif isinstance(payload, list):
        rows = payload
    else:
        raise ValueError("Discovery JSON must be a list or an object with a rows key")
    if not isinstance(rows, list):
        raise ValueError("Discovery rows must be a list")
    return rows


def filter_discovery(input_path: Path, run_date: str = TODAY) -> None:
    rows = load_discovery_rows(input_path)
    output: list[SimStrategyRow] = []
    for row in rows:
        text = str(row.get("raw_text") or row.get("text") or "")
        strategy_id = str(row.get("strategy_id") or row.get("id") or "")
        name = str(row.get("name") or row.get("strategy_name") or "")
        sharpe = parse_float(str(row.get("sharpe") or row.get("displayed_sharpe") or ""))
        inception = normalize_date(str(row.get("inception_date") or row.get("inception") or ""))
        included, reason = include_strategy(sharpe, inception)
        output.append(
            SimStrategyRow(
                strategy_id=strategy_id,
                name=name,
                displayed_sharpe=sharpe,
                inception_date=inception,
                included=included,
                reason=reason,
                raw_text=text[:500],
            )
        )
    fieldnames = [
        "strategy_id",
        "name",
        "displayed_sharpe",
        "inception_date",
        "included",
        "reason",
        "raw_text",
    ]
    csv_path = dated_path("candidate_strategy_discovery", "csv", run_date)
    json_path = dated_path("candidate_strategy_discovery", "json", run_date)
    rows_out = [asdict(row) for row in output]
    write_csv(csv_path, rows_out, fieldnames)
    write_json(json_path, {"rows": rows_out})
    included_count = sum(1 for row in output if row.included)
    append_iteration(
        "U2 Candidate Strategy Discovery",
        [
            f"- Read discovery rows from `{input_path.as_posix()}`.",
            f"- Wrote `{csv_path.as_posix()}` and `{json_path.as_posix()}`.",
            f"- Included {included_count} strategies with displayed Sharpe > 1 and inception before 2007.",
            "- Browser/table values remain discovery-only and do not feed final performance metrics.",
        ],
    )


def merge_expanded_discovery(input_paths: list[Path], run_date: str = TODAY) -> None:
    if not input_paths:
        raise SystemExit("At least one discovery JSON file is required")
    by_id: dict[str, dict[str, Any]] = {}
    for input_path in input_paths:
        source = input_path.stem
        for raw in load_discovery_rows(input_path):
            strategy_id = str(raw.get("strategy_id") or raw.get("id") or "").strip()
            if not strategy_id:
                continue
            name = str(raw.get("name") or raw.get("strategy_name") or "")
            sharpe = parse_float(str(raw.get("sharpe") or raw.get("displayed_sharpe") or ""))
            inception = normalize_date(str(raw.get("inception_date") or raw.get("inception") or ""))
            included, reason = include_strategy(sharpe, inception)
            existing = by_id.get(strategy_id)
            if existing is None:
                by_id[strategy_id] = {
                    "strategy_id": strategy_id,
                    "name": name,
                    "displayed_sharpe": sharpe,
                    "inception_date": inception,
                    "included": included,
                    "reason": reason,
                    "sources": source,
                    "source_count": 1,
                    "raw_text": str(raw.get("raw_text") or raw.get("text") or "")[:500],
                }
            else:
                sources = set(str(existing.get("sources", "")).split("|"))
                sources.add(source)
                existing["sources"] = "|".join(sorted(filter(None, sources)))
                existing["source_count"] = len(sources)
                if existing.get("displayed_sharpe") is None and sharpe is not None:
                    existing["displayed_sharpe"] = sharpe
                if existing.get("inception_date") is None and inception is not None:
                    existing["inception_date"] = inception
                included, reason = include_strategy(existing.get("displayed_sharpe"), existing.get("inception_date"))
                existing["included"] = included
                existing["reason"] = reason
    rows_out = sorted(by_id.values(), key=lambda row: row["strategy_id"])
    fieldnames = [
        "strategy_id",
        "name",
        "displayed_sharpe",
        "inception_date",
        "included",
        "reason",
        "sources",
        "source_count",
        "raw_text",
    ]
    csv_path = dated_path("expanded_strategy_discovery", "csv", run_date)
    json_path = dated_path("expanded_strategy_discovery", "json", run_date)
    write_csv(csv_path, rows_out, fieldnames)
    write_json(
        json_path,
        {
            "rows": rows_out,
            "input_files": [path.as_posix() for path in input_paths],
            "discovery_sources_count": len(input_paths),
            "included_count": sum(1 for row in rows_out if row.get("included")),
            "trial_count_contribution": len(input_paths),
            "note": "Browser/SIM values are discovery-only; performance validation must use API or native P123 outputs.",
        },
    )
    append_iteration(
        "U2 Expanded Strategy Discovery",
        [
            f"- Merged {len(input_paths)} discovery sources into `{csv_path.as_posix()}` and `{json_path.as_posix()}`.",
            f"- Unique strategies discovered: {len(rows_out)}.",
            f"- Included strategies after displayed Sharpe > 1 and inception before 2007 filter: {sum(1 for row in rows_out if row.get('included'))}.",
            "- Discovery-source count is recorded as part of dynamic trial accounting.",
        ],
    )


class ApiUnavailable(RuntimeError):
    pass


def get_p123_client() -> Any:
    api_id = os.environ.get("P123_API_ID")
    api_key = os.environ.get("P123_API_KEY")
    if not api_id or not api_key:
        raise ApiUnavailable("P123_API_ID and P123_API_KEY must be set in the environment")
    try:
        import p123api  # type: ignore
    except ImportError as exc:
        raise ApiUnavailable("p123api is not installed in this Python environment") from exc
    return p123api.Client(api_id=api_id, api_key=api_key)


def latest_file(stem: str, suffix: str) -> Path:
    matches = sorted(OUTPUT_DIR.glob(f"{stem}_*.{suffix}"))
    if not matches:
        raise FileNotFoundError(f"No output matching {stem}_*.{suffix}")
    return matches[-1]


def record_credit(call_log: list[dict[str, Any]], label: str, response: Any) -> None:
    if isinstance(response, dict):
        call_log.append(
            {
                "label": label,
                "cost": response.get("cost"),
                "quotaRemaining": response.get("quotaRemaining"),
            }
        )


def dataframe_from_response(response: Any) -> pd.DataFrame:
    if isinstance(response, pd.DataFrame):
        return response
    if isinstance(response, dict):
        for key in ["data", "rows", "results"]:
            value = response.get(key)
            if isinstance(value, list):
                return pd.DataFrame(value)
    if isinstance(response, list):
        return pd.DataFrame(response)
    return pd.DataFrame()


def daily_perf_returns(strategy_id: int, summary: Any) -> pd.DataFrame:
    if not isinstance(summary, dict) or not isinstance(summary.get("dailyPerf"), dict):
        return pd.DataFrame()
    daily = summary["dailyPerf"]
    if "date" not in daily or "ret" not in daily:
        return pd.DataFrame()
    frame = pd.DataFrame({"date": daily["date"], f"strategy_{strategy_id}": daily["ret"]})
    frame["date"] = pd.to_datetime(frame["date"]).dt.date
    frame[f"strategy_{strategy_id}"] = pd.to_numeric(frame[f"strategy_{strategy_id}"], errors="coerce")
    frame = frame.dropna().sort_values("date")
    frame[f"strategy_{strategy_id}"] = frame[f"strategy_{strategy_id}"].pct_change()
    return frame.dropna()


def classify_strategy_feasibility(discovery_path: Path | None = None, run_date: str = TODAY) -> None:
    discovery_path = discovery_path or latest_file("candidate_strategy_discovery", "json")
    discovery = json.loads(discovery_path.read_text(encoding="utf-8"))["rows"]
    candidates = [row for row in discovery if row.get("included") and row.get("strategy_id")]
    estimated_credits = len(candidates) * 3 + 1
    if estimated_credits > GOAL["constraints"]["api_credit_stop"]:
        raise SystemExit(
            f"Estimated strategy feasibility cost {estimated_credits} exceeds stop threshold; ask user first."
        )
    client = get_p123_client()
    rows: list[dict[str, Any]] = []
    return_frames: list[pd.DataFrame] = []
    call_log: list[dict[str, Any]] = []
    with client:
        for row in candidates:
            sid = int(row["strategy_id"])
            out = {
                "strategy_id": sid,
                "name": row.get("name"),
                "lane": "api_failed",
                "reason": "",
                "summary_keys": "",
                "holdings_rows": None,
                "transactions_rows": None,
            }
            try:
                summary = client.strategy(strategy_id=sid)
                record_credit(call_log, f"strategy:{sid}", summary)
                out["summary_keys"] = ",".join(sorted(summary.keys())) if isinstance(summary, dict) else type(summary).__name__
                return_frame = daily_perf_returns(sid, summary)
                transactions = client.strategy_transactions(
                    strategy_id=sid,
                    start="1900-01-01",
                    end=datetime.now().date().isoformat(),
                    to_pandas=True,
                )
                record_credit(call_log, f"strategy_transactions:{sid}", transactions if isinstance(transactions, dict) else {})
                trans_df = dataframe_from_response(transactions)
                out["transactions_rows"] = int(len(trans_df))
                out["lane"] = "metadata_only"
                out["reason"] = "api_summary_available_return_stream_not_confirmed"
                if not return_frame.empty:
                    out["lane"] = "tradable_stream"
                    out["reason"] = "dailyPerf_ret_stream_available"
                    return_frames.append(return_frame.set_index("date"))
                elif not trans_df.empty and {"date", "type", "shares", "price"}.intersection(set(map(str.lower, trans_df.columns))):
                    out["lane"] = "metadata_only"
                    out["reason"] = "transactions_available_but_daily_return_stream_missing"
            except Exception as exc:  # noqa: BLE001 - capture API failure as artifact data
                out["lane"] = "api_failed"
                out["reason"] = type(exc).__name__
            rows.append(out)
    csv_path = dated_path("strategy_return_feasibility", "csv", run_date)
    json_path = dated_path("strategy_return_feasibility", "json", run_date)
    write_csv(csv_path, rows)
    write_json(json_path, {"rows": rows, "api_calls": call_log, "estimated_credits": estimated_credits})
    if return_frames:
        strategy_returns = pd.concat(return_frames, axis=1).sort_index()
        strategy_returns.to_csv(dated_path("strategy_daily_returns", "csv", run_date), index_label="date")
    append_iteration(
        "U3 API Strategy Feasibility",
        [
            f"- Read candidates from `{discovery_path.as_posix()}`.",
            f"- Estimated strategy API feasibility credits: {estimated_credits}.",
            f"- Wrote `{csv_path.as_posix()}` and `{json_path.as_posix()}`.",
            f"- Saved API-derived strategy daily return streams for {len(return_frames)} strategies when available.",
            f"- Lane counts: {pd.Series([r['lane'] for r in rows]).value_counts().to_dict() if rows else {}}.",
        ],
    )


def validate_etf_universe(run_date: str = TODAY, start: str = "1900-01-01", end: str | None = None) -> None:
    seeds = [seed for seed in ETF_SEEDS if GOAL["constraints"]["allow_leveraged_etfs"] or not seed["leveraged"]]
    estimated_credits = len(seeds)
    if estimated_credits > GOAL["constraints"]["api_credit_stop"]:
        raise SystemExit(f"Estimated ETF API cost {estimated_credits} exceeds stop threshold; ask user first.")
    client = get_p123_client()
    rows: list[dict[str, Any]] = []
    price_frames: list[pd.DataFrame] = []
    call_log: list[dict[str, Any]] = []
    with client:
        for seed in seeds:
            row = dict(seed)
            row.update({"eligible": False, "reason": "", "first_date": None, "last_date": None, "rows": 0})
            try:
                response = client.data_prices(seed["ticker"], start=start, end=end, to_pandas=True)
                record_credit(call_log, f"data_prices:{seed['ticker']}", response if isinstance(response, dict) else {})
                df = dataframe_from_response(response)
                if df.empty:
                    row["reason"] = "api_empty"
                else:
                    lower_cols = {str(col).lower(): col for col in df.columns}
                    date_col = lower_cols.get("date") or lower_cols.get("dt")
                    close_col = lower_cols.get("close") or lower_cols.get("adjclose") or lower_cols.get("adj_close")
                    if date_col is None or close_col is None:
                        row["reason"] = "missing_date_or_close_column"
                    else:
                        frame = df[[date_col, close_col]].copy()
                        frame.columns = ["date", seed["ticker"]]
                        frame["date"] = pd.to_datetime(frame["date"]).dt.date
                        frame = frame.dropna().sort_values("date")
                        row["rows"] = int(len(frame))
                        if frame.empty:
                            row["reason"] = "empty_after_cleaning"
                        else:
                            row["first_date"] = frame["date"].iloc[0].isoformat()
                            row["last_date"] = frame["date"].iloc[-1].isoformat()
                            if row["first_date"] >= GOAL["constraints"]["candidate_strategy_inception_before"]:
                                row["reason"] = "post_2007_inception"
                            else:
                                row["eligible"] = True
                                row["reason"] = "eligible"
                                price_frames.append(frame.set_index("date"))
            except Exception as exc:  # noqa: BLE001
                row["reason"] = f"api_failed:{type(exc).__name__}"
            rows.append(row)
    csv_path = dated_path("etf_universe_candidates", "csv", run_date)
    json_path = dated_path("etf_universe_candidates", "json", run_date)
    write_csv(csv_path, rows)
    write_json(json_path, {"rows": rows, "api_calls": call_log, "estimated_credits": estimated_credits})
    if price_frames:
        prices = pd.concat(price_frames, axis=1).sort_index()
        prices.to_csv(dated_path("etf_prices", "csv", run_date), index_label="date")
    append_iteration(
        "U4 ETF Family Funnel",
        [
            f"- Validated {len(rows)} ETF seeds, including inverse ETFs and excluding leveraged ETFs.",
            f"- Estimated ETF API credits: {estimated_credits}.",
            f"- Wrote `{csv_path.as_posix()}` and `{json_path.as_posix()}`.",
            f"- Eligible ETF count: {sum(1 for row in rows if row.get('eligible'))}.",
        ],
    )


def price_returns(price_file: Path | None = None, run_date: str = TODAY) -> None:
    price_file = price_file or latest_file("etf_prices", "csv")
    prices = pd.read_csv(price_file, parse_dates=["date"]).set_index("date").sort_index()
    returns = prices.pct_change(fill_method=None).dropna(how="all")
    strategy_file = None
    try:
        strategy_file = latest_file("strategy_daily_returns", "csv")
        strategy_returns = pd.read_csv(strategy_file, parse_dates=["date"]).set_index("date").sort_index()
        returns = pd.concat([strategy_returns, returns], axis=1).sort_index()
    except FileNotFoundError:
        strategy_returns = pd.DataFrame()
    returns = returns.dropna(axis=1, how="all").dropna(how="any")
    returns.to_csv(dated_path("return_panel", "csv", run_date), index_label="date")
    summary = {
        "source": price_file.as_posix(),
        "start": returns.index.min().date().isoformat() if not returns.empty else None,
        "end": returns.index.max().date().isoformat() if not returns.empty else None,
        "rows": int(len(returns)),
        "components": list(returns.columns),
        "missing_by_component": {col: int(returns[col].isna().sum()) for col in returns.columns},
        "strategy_return_source": strategy_file.as_posix() if strategy_file else None,
        "strategy_components": list(strategy_returns.columns) if not strategy_returns.empty else [],
        "note": "Combined panel uses API-derived strategy dailyPerf returns plus API ETF price returns, synchronized by dropping rows with missing component returns.",
    }
    write_json(dated_path("return_panel_summary", "json", run_date), summary)
    append_iteration(
        "U5 Return Panel",
        [
            f"- Built ETF return panel from `{price_file.as_posix()}`.",
            f"- Return window: {summary['start']} to {summary['end']} across {len(summary['components'])} components.",
            f"- Included {len(summary['strategy_components'])} API-derived strategy return streams.",
        ],
    )


def load_return_panel(path: Path | None = None) -> pd.DataFrame:
    path = path or latest_file("return_panel", "csv")
    returns = pd.read_csv(path, parse_dates=["date"]).set_index("date").sort_index()
    returns = returns.apply(pd.to_numeric, errors="coerce")
    return returns.dropna(axis=1, how="all").dropna(how="all")


def choose_benchmark_column(returns: pd.DataFrame) -> str:
    for candidate in ["SPY", "IWB", "QQQ"]:
        if candidate in returns.columns:
            return candidate
    equity_cols = [col for col in returns.columns if not col.startswith("strategy_")]
    if equity_cols:
        return equity_cols[0]
    raise ValueError("No ETF/benchmark-like column is available for timing signals")


def equity_curve(return_series: pd.Series) -> pd.Series:
    return (1 + return_series.fillna(0)).cumprod()


def build_timing_signals(return_file: Path | None = None, run_date: str = TODAY) -> None:
    return_file = return_file or latest_file("return_panel", "csv")
    returns = load_return_panel(return_file)
    benchmark = choose_benchmark_column(returns)
    close = equity_curve(returns[benchmark])
    prior_close = close.shift(1)
    sma_50 = close.rolling(50, min_periods=50).mean().shift(1)
    sma_200 = close.rolling(200, min_periods=200).mean().shift(1)
    mom_252 = close.pct_change(252).shift(1)
    high_252 = close.rolling(252, min_periods=252).max().shift(1)
    drawdown = prior_close / high_252 - 1
    vol_63 = returns[benchmark].rolling(63, min_periods=63).std().shift(1) * math.sqrt(252)
    vol_median = vol_63.rolling(252, min_periods=126).median().shift(1)
    signals = pd.DataFrame(index=returns.index)
    signals["bench_above_200d"] = (prior_close > sma_200).where(prior_close.notna() & sma_200.notna())
    signals["bench_50d_above_200d"] = (sma_50 > sma_200).where(sma_50.notna() & sma_200.notna())
    signals["bench_12m_momentum_positive"] = (mom_252 > 0).where(mom_252.notna())
    signals["bench_drawdown_under_20pct"] = (drawdown > -0.20).where(drawdown.notna())
    signals["bench_volatility_below_median"] = (vol_63 < vol_median).where(vol_63.notna() & vol_median.notna())
    signals = signals.dropna(how="all")
    signals = signals.astype("boolean")
    valid = signals.notna().all(axis=1)
    signals = signals.loc[valid].astype(int)
    signal_cols = [rule["name"] for rule in TECHNICAL_TIMING_RULES]
    signals["risk_on_votes"] = signals[signal_cols].sum(axis=1)
    signals["ensemble_exposure"] = signals["risk_on_votes"].map(
        lambda votes: 1.0 if votes >= 4 else 0.6 if votes == 3 else 0.3 if votes == 2 else 0.0
    )
    signals["inverse_enabled"] = (signals["risk_on_votes"] <= 2).astype(int)
    signals.to_csv(dated_path("timing_signal_panel", "csv", run_date), index_label="date")
    summary = {
        "source_return_panel": return_file.as_posix(),
        "benchmark_column": benchmark,
        "start": signals.index.min().date().isoformat() if not signals.empty else None,
        "end": signals.index.max().date().isoformat() if not signals.empty else None,
        "rows": int(len(signals)),
        "technical_rules": TECHNICAL_TIMING_RULES,
        "macro_candidates": MACRO_STRESS_CANDIDATES,
        "trial_count_contribution": sum(rule["trial_count"] for rule in TECHNICAL_TIMING_RULES) + 1,
        "lookahead_guard": "Signals are shifted one bar so date t allocation uses information available before date t return.",
        "macro_note": "Macro candidates are documented but not activated until P123 macro series availability and point-in-time behavior are confirmed.",
    }
    write_json(dated_path("timing_signal_summary", "json", run_date), summary)
    append_iteration(
        "U3 P123-Native Timing Signal Panel",
        [
            f"- Built timing signals from `{return_file.as_posix()}` using `{benchmark}` as benchmark proxy.",
            f"- Signal window: {summary['start']} to {summary['end']} across {summary['rows']} rows.",
            "- Technical timing rules are shifted one bar to avoid same-day look-ahead.",
            "- Macro stress candidates are documented but not activated pending P123 macro-series confirmation.",
        ],
    )


def defensive_proxy(returns: pd.DataFrame) -> pd.Series:
    for candidate in ["SHY", "IEF", "AGG"]:
        if candidate in returns.columns:
            return returns[candidate].fillna(0)
    return pd.Series(0.0, index=returns.index)


def average_available(returns: pd.DataFrame, columns: list[str]) -> pd.Series:
    available = [col for col in columns if col in returns.columns]
    if not available:
        return pd.Series(0.0, index=returns.index)
    return returns[available].mean(axis=1).fillna(0)


def tactical_rotation_returns(returns: pd.DataFrame, signals: pd.DataFrame) -> tuple[pd.Series, pd.DataFrame]:
    risk_on_bucket = [col for col in ["SPY", "QQQ", "IWM", "EFA", "EEM", "MDY", "IWF"] if col in returns.columns]
    defensive_bucket = [col for col in ["SHY", "IEF", "TLT", "AGG", "LQD", "GLD"] if col in returns.columns]
    inverse_bucket = [col for col in ["SH", "DOG", "PSQ"] if col in returns.columns]
    candidate_cols = sorted(set(risk_on_bucket + defensive_bucket + inverse_bucket))
    if not candidate_cols:
        return pd.Series(0.0, index=returns.index, name="tactical_etf_component"), pd.DataFrame()
    momentum = (1 + returns[candidate_cols].fillna(0)).rolling(252, min_periods=126).apply(np.prod, raw=True) - 1
    momentum = momentum.shift(1)
    vol = returns[candidate_cols].rolling(63, min_periods=42).std().shift(1) * math.sqrt(252)
    score = momentum - vol
    picks: list[dict[str, Any]] = []
    component = pd.Series(0.0, index=returns.index, name="tactical_etf_component")
    aligned_signals = signals.reindex(returns.index).ffill()
    for dt in returns.index:
        row_signal = aligned_signals.loc[dt]
        if row_signal.get("inverse_enabled", 0) == 1 and inverse_bucket:
            bucket_name = "inverse"
            bucket = inverse_bucket
        elif row_signal.get("ensemble_exposure", 0) >= 0.6 and risk_on_bucket:
            bucket_name = "risk_on"
            bucket = risk_on_bucket
        else:
            bucket_name = "defensive"
            bucket = defensive_bucket or risk_on_bucket
        score_row = score.loc[dt, bucket].dropna()
        if score_row.empty:
            picked = bucket[0] if bucket else None
        else:
            picked = str(score_row.idxmax())
        component.loc[dt] = returns.at[dt, picked] if picked in returns.columns else 0.0
        picks.append({"date": dt.date().isoformat(), "bucket": bucket_name, "ticker": picked})
    picks_frame = pd.DataFrame(picks)
    return component, picks_frame


def build_dynamic_panel(
    return_file: Path | None = None,
    timing_file: Path | None = None,
    run_date: str = TODAY,
) -> None:
    return_file = return_file or latest_file("return_panel", "csv")
    timing_file = timing_file or latest_file("timing_signal_panel", "csv")
    returns = load_return_panel(return_file)
    signals = pd.read_csv(timing_file, parse_dates=["date"]).set_index("date").sort_index()
    common_index = returns.index.intersection(signals.index)
    returns = returns.loc[common_index]
    signals = signals.loc[common_index]
    defensive = defensive_proxy(returns)
    dynamic = pd.DataFrame(index=common_index)
    strategy_cols = [col for col in returns.columns if col.startswith("strategy_")]
    for col in strategy_cols:
        dynamic[col] = returns[col]
        dynamic[f"{col}_timed_200d"] = np.where(
            signals["bench_above_200d"].astype(bool),
            returns[col],
            defensive,
        )
        exposure = signals["ensemble_exposure"].astype(float)
        dynamic[f"{col}_timed_ensemble"] = exposure * returns[col] + (1 - exposure) * defensive
    inverse_avg = average_available(returns, ["SH", "DOG", "PSQ"])
    dynamic["conditional_inverse_sleeve"] = np.where(
        signals["inverse_enabled"].astype(bool),
        inverse_avg,
        defensive,
    )
    tactical, picks = tactical_rotation_returns(returns, signals)
    dynamic["tactical_etf_component"] = tactical
    dynamic["defensive_proxy_component"] = defensive
    dynamic = dynamic.dropna(how="any")
    dynamic.to_csv(dated_path("dynamic_return_panel", "csv", run_date), index_label="date")
    candidate_rows = []
    if not picks.empty:
        pick_counts = picks.groupby(["bucket", "ticker"]).size().reset_index(name="days")
        candidate_rows = pick_counts.to_dict(orient="records")
    candidate_rows.append(
        {
            "bucket": "conditional_inverse",
            "ticker": "SH|DOG|PSQ",
            "days": int(signals["inverse_enabled"].sum()),
            "signal_dependency": "inverse_enabled",
        }
    )
    write_csv(dated_path("tactical_etf_component_candidates", "csv", run_date), candidate_rows)
    summary = {
        "source_return_panel": return_file.as_posix(),
        "source_timing_panel": timing_file.as_posix(),
        "start": dynamic.index.min().date().isoformat() if not dynamic.empty else None,
        "end": dynamic.index.max().date().isoformat() if not dynamic.empty else None,
        "rows": int(len(dynamic)),
        "components": list(dynamic.columns),
        "raw_strategy_components": strategy_cols,
        "conditional_inverse_days": int(signals["inverse_enabled"].sum()),
        "tactical_component": "tactical_etf_component",
        "defensive_component": "defensive_proxy_component",
        "trial_count_contribution": len(strategy_cols) * 2 + 2,
    }
    write_json(dated_path("dynamic_return_panel_summary", "json", run_date), summary)
    append_iteration(
        "U4-U5 Dynamic Panel And Tactical ETF Component",
        [
            f"- Built dynamic panel from `{return_file.as_posix()}` and `{timing_file.as_posix()}`.",
            f"- Dynamic window: {summary['start']} to {summary['end']} across {summary['rows']} rows.",
            f"- Added timed variants for {len(strategy_cols)} strategy streams, one conditional inverse sleeve, and one tactical ETF component.",
            "- Conditional inverse exposure is active only when the timing ensemble marks inverse-enabled risk-off days.",
        ],
    )


def annualized_metrics(returns: pd.Series, periods_per_year: int = 252) -> dict[str, float]:
    clean = returns.dropna()
    if clean.empty:
        return {"cagr": math.nan, "sharpe": math.nan, "max_drawdown": math.nan}
    equity = (1 + clean).cumprod()
    years = len(clean) / periods_per_year
    cagr = float(equity.iloc[-1] ** (1 / years) - 1) if years > 0 else math.nan
    vol = clean.std(ddof=1) * math.sqrt(periods_per_year)
    sharpe = float(clean.mean() * periods_per_year / vol) if vol and not math.isnan(vol) else math.nan
    drawdown = equity / equity.cummax() - 1
    return {"cagr": cagr, "sharpe": sharpe, "max_drawdown": float(drawdown.min())}


def walk_forward_positive_rate(returns: pd.Series, window: int = 252) -> float:
    clean = returns.dropna()
    if len(clean) < window:
        return math.nan
    positives = []
    for start in range(0, len(clean) - window + 1, window):
        chunk = clean.iloc[start : start + window]
        positives.append(annualized_metrics(chunk)["cagr"] > 0)
    return float(sum(positives) / len(positives)) if positives else math.nan


def crisis_window_drawdowns(returns: pd.Series) -> dict[str, float]:
    windows = {
        "crisis_2008": ("2008-01-01", "2009-03-31"),
        "crisis_2011": ("2011-07-01", "2011-12-31"),
        "crisis_2018q4": ("2018-10-01", "2018-12-31"),
        "crisis_2020": ("2020-02-01", "2020-04-30"),
        "crisis_2022": ("2022-01-01", "2022-12-31"),
    }
    out: dict[str, float] = {}
    clean = returns.dropna()
    for name, (start, end) in windows.items():
        window = clean.loc[(clean.index >= pd.Timestamp(start)) & (clean.index <= pd.Timestamp(end))]
        out[f"{name}_drawdown"] = annualized_metrics(window)["max_drawdown"] if not window.empty else math.nan
    return out


def normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def psr(returns: pd.Series, target_sharpe: float = 0.0, periods_per_year: int = 252) -> float:
    clean = returns.dropna()
    n = len(clean)
    if n < 30 or clean.std(ddof=1) == 0:
        return math.nan
    sr = annualized_metrics(clean, periods_per_year)["sharpe"]
    skew = float(clean.skew())
    kurt = float(clean.kurtosis() + 3)
    denom = math.sqrt(max(1e-12, 1 - skew * sr + ((kurt - 1) / 4) * sr * sr))
    return normal_cdf((sr - target_sharpe) * math.sqrt(n - 1) / denom)


def dsr(returns: pd.Series, n_trials: int, periods_per_year: int = 252) -> float:
    clean = returns.dropna()
    if n_trials <= 1:
        return psr(clean, 0.0, periods_per_year)
    # Conservative approximation: require observed Sharpe to beat an expected
    # maximum Sharpe from n independent zero-skill trials.
    expected_max_sr = math.sqrt(2 * math.log(n_trials)) / math.sqrt(max(len(clean) - 1, 1) / periods_per_year)
    return psr(clean, expected_max_sr, periods_per_year)


def inverse_vol_weights(returns: pd.DataFrame) -> pd.Series:
    vol = returns.std(ddof=1).replace(0, np.nan)
    weights = (1 / vol).replace([np.inf, -np.inf], np.nan).dropna()
    weights = weights / weights.sum()
    return weights.reindex(returns.columns).fillna(0)


def equal_weights(returns: pd.DataFrame) -> pd.Series:
    return pd.Series(1 / returns.shape[1], index=returns.columns)


def hrp_weights(returns: pd.DataFrame) -> pd.Series:
    try:
        from scipy.cluster.hierarchy import linkage
        from scipy.spatial.distance import squareform
    except ImportError:
        return inverse_vol_weights(returns)
    corr = returns.corr().fillna(0).clip(-1, 1)
    cov = returns.cov()
    if corr.shape[0] < 2:
        return equal_weights(returns)
    dist = ((1 - corr) / 2.0) ** 0.5
    link = linkage(squareform(dist.values, checks=False), method="single")
    link = link.astype(int)
    sort_ix = pd.Series([link[-1, 0], link[-1, 1]])
    num_items = link[-1, 3]
    while sort_ix.max() >= num_items:
        sort_ix.index = range(0, sort_ix.shape[0] * 2, 2)
        bigger = sort_ix[sort_ix >= num_items]
        i = bigger.index
        j = bigger.values - num_items
        sort_ix[i] = link[j, 0]
        sort_ix = pd.concat([sort_ix, pd.Series(link[j, 1], index=i + 1)]).sort_index()
        sort_ix.index = range(sort_ix.shape[0])
    ordered = corr.index[sort_ix.tolist()].tolist()
    weights = pd.Series(1.0, index=ordered)
    clusters = [ordered]
    while clusters:
        clusters = [
            cluster[start:end]
            for cluster in clusters
            for start, end in ((0, len(cluster) // 2), (len(cluster) // 2, len(cluster)))
            if len(cluster) > 1
        ]
        for i in range(0, len(clusters), 2):
            if i + 1 >= len(clusters):
                break
            left, right = clusters[i], clusters[i + 1]
            left_var = cluster_variance(cov, left)
            right_var = cluster_variance(cov, right)
            alpha = 1 - left_var / (left_var + right_var) if left_var + right_var else 0.5
            weights[left] *= alpha
            weights[right] *= 1 - alpha
    return weights.reindex(returns.columns).fillna(0)


def cluster_variance(cov: pd.DataFrame, assets: list[str]) -> float:
    slice_cov = cov.loc[assets, assets]
    ivp = 1 / np.diag(slice_cov.values)
    ivp = ivp / ivp.sum()
    return float(ivp.T @ slice_cov.values @ ivp)


def apply_component_cap(weights: pd.Series, cap: float, total: float = 1.0) -> pd.Series:
    positive = weights.clip(lower=0).astype(float)
    if positive.sum() <= 0:
        positive = pd.Series(1.0, index=weights.index)
    remaining = positive / positive.sum()
    result = pd.Series(0.0, index=weights.index)
    remaining_total = total
    while not remaining.empty:
        scaled = remaining / remaining.sum() * remaining_total
        over_cap = scaled > cap
        if not over_cap.any():
            result[scaled.index] = scaled
            break
        capped_names = scaled[over_cap].index
        result[capped_names] = cap
        remaining_total -= cap * len(capped_names)
        remaining = remaining.drop(index=capped_names)
        if remaining_total <= 0:
            break
    return result


def cap_weights(weights: pd.Series, inverse_flags: dict[str, bool]) -> pd.Series:
    max_component = GOAL["constraints"]["max_component_weight"]
    max_inverse = GOAL["constraints"]["max_inverse_sleeve_weight"]
    capped = apply_component_cap(weights, max_component)
    inverse_cols = [col for col, flag in inverse_flags.items() if flag and col in capped.index]
    inv_sum = capped[inverse_cols].sum() if inverse_cols else 0
    if inverse_cols and inv_sum > max_inverse:
        non_inverse = [col for col in capped.index if col not in inverse_cols]
        inverse_part = capped[inverse_cols] / inv_sum * max_inverse
        non_inverse_part = apply_component_cap(capped[non_inverse], max_component, 1 - max_inverse)
        capped = pd.concat([inverse_part, non_inverse_part]).reindex(weights.index).fillna(0)
    return capped / capped.sum()


def output_stem(prefix: str, stem: str) -> str:
    return f"{prefix}{stem}" if prefix else stem


def optimize_panel(
    return_file: Path | None = None,
    etf_file: Path | None = None,
    run_date: str = TODAY,
    periods_per_year: int = 252,
    cagr_min: float | None = None,
    sharpe_min: float | None = None,
    max_drawdown_min: float | None = None,
    artifact_prefix: str = "",
) -> None:
    thresholds = {
        "cagr_min": GOAL["thresholds"]["cagr_min"] if cagr_min is None else cagr_min,
        "sharpe_min": GOAL["thresholds"]["sharpe_min"] if sharpe_min is None else sharpe_min,
        "psr_min": GOAL["thresholds"]["psr_min"],
        "dsr_min": GOAL["thresholds"]["dsr_min"],
        "max_drawdown_min": max_drawdown_min,
    }
    return_file = return_file or latest_file("return_panel", "csv")
    etf_file = etf_file or latest_file("etf_universe_candidates", "json")
    returns = pd.read_csv(return_file, parse_dates=["date"]).set_index("date").sort_index()
    returns = returns.dropna(axis=1, how="all").dropna(how="all")
    if returns.shape[1] < 2:
        raise SystemExit("Need at least two return streams to optimize")
    etfs = json.loads(etf_file.read_text(encoding="utf-8"))["rows"]
    inverse_flags = {row["ticker"]: bool(row.get("inverse")) for row in etfs}
    for col in returns.columns:
        if col.startswith("conditional_inverse"):
            inverse_flags[col] = True
    trials: list[dict[str, Any]] = []
    n = 0
    methods = [
        ("equal_weight", equal_weights(returns)),
        ("inverse_volatility", inverse_vol_weights(returns)),
        ("hrp", hrp_weights(returns)),
    ]
    # Small constrained ensemble: blend inverse-vol and HRP across five weights.
    iv = methods[1][1]
    hrp = methods[2][1]
    for alpha in [0.0, 0.25, 0.5, 0.75, 1.0]:
        methods.append((f"constrained_ensemble_iv_{alpha:.2f}_hrp_{1-alpha:.2f}", alpha * iv + (1 - alpha) * hrp))
    strategies = [col for col in returns.columns if col.startswith("strategy_")]
    inverse_etfs = [col for col in ["SH", "DOG", "PSQ"] if col in returns.columns]
    bond_etfs = [col for col in ["SHY", "IEF", "TLT", "AGG", "LQD"] if col in returns.columns]
    real_asset_etfs = [col for col in ["GLD", "DBC", "SLV", "VNQ"] if col in returns.columns]
    equity_etfs = [col for col in ["SPY", "QQQ", "IWM", "EFA", "EEM"] if col in returns.columns]
    for strategy_total in [0.70, 0.75, 0.80, 0.85, 0.90]:
        for inverse_total in [0.00, 0.05, 0.10, 0.125, 0.15, 0.20]:
            for bond_total in [0.00, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25, 0.30]:
                for real_total in [0.00, 0.025, 0.05]:
                    equity_total = 1 - strategy_total - inverse_total - bond_total - real_total
                    if equity_total < -1e-9:
                        continue
                    sleeves = [
                        (strategies, strategy_total),
                        (inverse_etfs, inverse_total),
                        (bond_etfs, bond_total),
                        (real_asset_etfs, real_total),
                        (equity_etfs, max(0.0, equity_total)),
                    ]
                    weights = pd.Series(0.0, index=returns.columns)
                    for cols, total in sleeves:
                        if not cols or total <= 0:
                            continue
                        weights[cols] = weights[cols] + total / len(cols)
                    if weights.sum() <= 0:
                        continue
                    methods.append(
                        (
                            (
                                f"strategy_sleeve_grid_s{strategy_total:.3f}_"
                                f"inv{inverse_total:.3f}_bond{bond_total:.3f}_"
                                f"real{real_total:.3f}_equity{max(0.0, equity_total):.3f}"
                            ),
                            weights,
                        )
                    )
    strict_mode = thresholds["sharpe_min"] >= 2.0 or thresholds["max_drawdown_min"] is not None
    if strict_mode:
        strategy_templates: list[tuple[str, pd.Series]] = []
        if strategies:
            equal_strategy = pd.Series(1 / len(strategies), index=strategies)
            strategy_templates.append(("eqstrat", equal_strategy))
            strategy_metrics = {
                col: annualized_metrics(returns[col], periods_per_year)
                for col in strategies
            }
            cagr_scores = pd.Series(
                {col: max(0.0, strategy_metrics[col]["cagr"]) for col in strategies}
            )
            sharpe_scores = pd.Series(
                {col: max(0.0, strategy_metrics[col]["sharpe"]) for col in strategies}
            )
            drawdown_scores = pd.Series(
                {col: max(0.0, 1 + strategy_metrics[col]["max_drawdown"]) for col in strategies}
            )
            for name, scores in [
                ("cagrstrat", cagr_scores),
                ("sharpestrat", sharpe_scores),
                ("ddstrat", drawdown_scores),
                ("blendstrat", cagr_scores * sharpe_scores * drawdown_scores),
            ]:
                if scores.sum() > 0:
                    strategy_templates.append((name, scores / scores.sum()))
        inverse_totals = [round(x, 3) for x in np.arange(0.00, 0.351, 0.025)]
        bond_totals = [round(x, 3) for x in np.arange(0.00, 0.501, 0.025)]
        real_totals = [0.00, 0.025, 0.05, 0.075, 0.10]
        equity_totals = [0.00, 0.025, 0.05, 0.075, 0.10]
        strategy_totals = [round(x, 3) for x in np.arange(0.45, 0.901, 0.025)]
        for template_name, template_weights in strategy_templates:
            for strategy_total in strategy_totals:
                for inverse_total in inverse_totals:
                    for bond_total in bond_totals:
                        for real_total in real_totals:
                            for equity_total in equity_totals:
                                total = strategy_total + inverse_total + bond_total + real_total + equity_total
                                if total > 1 + 1e-9 or total < 0.999 - 1e-9:
                                    continue
                                weights = pd.Series(0.0, index=returns.columns)
                                weights[template_weights.index] = template_weights * strategy_total
                                for cols, sleeve_total in [
                                    (inverse_etfs, inverse_total),
                                    (bond_etfs, bond_total),
                                    (real_asset_etfs, real_total),
                                    (equity_etfs, equity_total),
                                ]:
                                    if cols and sleeve_total > 0:
                                        weights[cols] = weights[cols] + sleeve_total / len(cols)
                                methods.append(
                                    (
                                        (
                                            f"strict_risk_grid_{template_name}_s{strategy_total:.3f}_"
                                            f"inv{inverse_total:.3f}_bond{bond_total:.3f}_"
                                            f"real{real_total:.3f}_equity{equity_total:.3f}"
                                        ),
                                        weights,
                                    )
                                )
    for method, raw_weights in methods:
        n += 1
        weights = cap_weights(raw_weights, inverse_flags)
        port = returns[weights.index].mul(weights, axis=1).sum(axis=1)
        metrics = annualized_metrics(port, periods_per_year)
        crisis = crisis_window_drawdowns(port)
        worst_crisis_drawdown = min([value for value in crisis.values() if not math.isnan(value)], default=math.nan)
        walk_forward_positive = walk_forward_positive_rate(port, periods_per_year)
        psr_value = psr(port, 0.0, periods_per_year)
        dsr_value = dsr(port, n, periods_per_year)
        inverse_weight = float(sum(weights.get(col, 0.0) for col, flag in inverse_flags.items() if flag))
        gate_status = (
            "pass"
            if metrics["cagr"] > thresholds["cagr_min"]
            and metrics["sharpe"] > thresholds["sharpe_min"]
            and (thresholds["max_drawdown_min"] is None or metrics["max_drawdown"] > thresholds["max_drawdown_min"])
            and psr_value >= thresholds["psr_min"]
            and dsr_value >= thresholds["dsr_min"]
            else "fail"
        )
        failure_reasons = []
        if not metrics["cagr"] > thresholds["cagr_min"]:
            failure_reasons.append("cagr")
        if not metrics["sharpe"] > thresholds["sharpe_min"]:
            failure_reasons.append("sharpe")
        if thresholds["max_drawdown_min"] is not None and not metrics["max_drawdown"] > thresholds["max_drawdown_min"]:
            failure_reasons.append("max_drawdown")
        if not psr_value >= thresholds["psr_min"]:
            failure_reasons.append("psr")
        if not dsr_value >= thresholds["dsr_min"]:
            failure_reasons.append("dsr")
        trials.append(
            {
                "n_trials_index": n,
                "optimizer_family": method,
                "components": "|".join(weights.index),
                "weights": json.dumps({k: round(float(v), 6) for k, v in weights.items()}, sort_keys=True),
                "inverse_weight": inverse_weight,
                "cagr": metrics["cagr"],
                "sharpe": metrics["sharpe"],
                "max_drawdown": metrics["max_drawdown"],
                "walk_forward_positive_rate": walk_forward_positive,
                "worst_crisis_drawdown": worst_crisis_drawdown,
                "psr": psr_value,
                "dsr": dsr_value,
                "gate_status": gate_status,
                "decision_reason": "all_gates_pass" if gate_status == "pass" else "failed_" + "_".join(failure_reasons),
                "validation_tier": "API-estimated",
                "cagr_gate": thresholds["cagr_min"],
                "sharpe_gate": thresholds["sharpe_min"],
                "max_drawdown_gate": thresholds["max_drawdown_min"],
            }
        )
    ledger_csv = dated_path(output_stem(artifact_prefix, "trial_ledger"), "csv", run_date)
    ledger_json = dated_path(output_stem(artifact_prefix, "trial_ledger"), "json", run_date)
    write_csv(ledger_csv, trials)
    write_json(ledger_json, {"rows": trials, "source_return_panel": return_file.as_posix(), "n_trials": n, "thresholds": thresholds})
    append_iteration(
        "U9 Strict Optimizer And Validation" if strict_mode else "U6-U7 Optimizer And Validation",
        [
            f"- Optimized `{return_file.as_posix()}` using the pre-registered ladder.",
            f"- Wrote `{ledger_csv.as_posix()}` and `{ledger_json.as_posix()}`.",
            f"- Trials: {n}; passing allocations: {sum(1 for trial in trials if trial['gate_status'] == 'pass')}.",
            f"- Gates: CAGR > {thresholds['cagr_min']:.2%}, Sharpe > {thresholds['sharpe_min']:.2f}, max drawdown > {thresholds['max_drawdown_min'] if thresholds['max_drawdown_min'] is not None else 'not gated'}.",
        ],
    )


def generate_report(ledger_file: Path | None = None, run_date: str = TODAY, artifact_prefix: str = "") -> None:
    ledger_file = ledger_file or latest_file(output_stem(artifact_prefix, "trial_ledger"), "csv")
    ledger = pd.read_csv(ledger_file)
    if ledger.empty:
        raise SystemExit("Trial ledger is empty")
    sort_cols = ["sharpe", "cagr"]
    best = ledger.sort_values(sort_cols, ascending=[False, False]).head(10).copy()
    winners = ledger[ledger["gate_status"] == "pass"].copy()
    if not winners.empty:
        winners = winners.sort_values(sort_cols, ascending=[False, False]).head(10).copy()
    display_cols = [
        "n_trials_index",
        "optimizer_family",
        "cagr",
        "sharpe",
        "max_drawdown",
        "walk_forward_positive_rate",
        "worst_crisis_drawdown",
        "psr",
        "dsr",
        "inverse_weight",
        "weights",
    ]
    display_cols = [col for col in display_cols if col in ledger.columns]
    for frame in [best, winners]:
        if frame.empty:
            continue
        frame["weights"] = frame["weights"].map(
            lambda raw: json.dumps(
                {key: value for key, value in json.loads(raw).items() if abs(float(value)) > 1e-9},
                sort_keys=True,
            )
        )
    if not winners.empty:
        report_path = dated_path(output_stem(artifact_prefix, "api_estimated_strategy_book_report"), "md", run_date)
        title = "Strict API-Estimated Strategy Book Candidate Report" if artifact_prefix else "API-Estimated Strategy Book Candidate Report"
        body = [
            f"Created: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
            "",
            f"# {title}",
            "",
            "This is API-estimated candidate research, not native Portfolio123 Tier 1 Strategy Book validation.",
            "",
            "## Passing Candidates",
            "",
            winners[display_cols].to_string(index=False),
            "",
            "## Required Next Step",
            "",
            "Run native Portfolio123 Strategy Book validation before making final performance claims.",
        ]
    else:
        report_path = dated_path(output_stem(artifact_prefix, "no_winner_report"), "md", run_date)
        title = "Strict No-Winner Report" if artifact_prefix else "No-Winner Report"
        body = [
            f"Created: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
            "",
            f"# {title}",
            "",
            "No API-estimated allocation passed every pre-registered gate.",
            "",
            "## Nearest Misses",
            "",
            best[display_cols].to_string(index=False),
            "",
            "## Next API-Cheap Iteration",
            "",
            "- Inspect failed gates and expand only the most relevant ETF family or strategy return-stream source.",
            "- Do not loosen CAGR, Sharpe, PSR, or DSR thresholds without a new approved plan.",
        ]
    report_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    append_iteration(
        "U8 Report Generation",
        [
            f"- Read trial ledger `{ledger_file.as_posix()}`.",
            f"- Wrote `{report_path.as_posix()}`.",
            f"- Passing candidates: {len(winners)}.",
        ],
    )


def dynamic_optimize(
    return_file: Path | None = None,
    etf_file: Path | None = None,
    run_date: str = TODAY,
) -> None:
    return_file = return_file or latest_file("dynamic_return_panel", "csv")
    returns = load_return_panel(return_file)
    if returns.shape[1] < 2:
        raise SystemExit("Need at least two dynamic return streams to optimize")
    inverse_flags = {col: col.startswith("conditional_inverse") for col in returns.columns}
    methods: list[tuple[str, pd.Series]] = [
        ("dynamic_equal_weight", equal_weights(returns)),
        ("dynamic_inverse_volatility", inverse_vol_weights(returns)),
        ("dynamic_hrp", hrp_weights(returns)),
    ]
    strategy_modes = {
        "raw": [col for col in returns.columns if col.startswith("strategy_") and "_timed_" not in col],
        "timed_200d": [col for col in returns.columns if col.endswith("_timed_200d")],
        "timed_ensemble": [col for col in returns.columns if col.endswith("_timed_ensemble")],
    }
    tactical_cols = [col for col in ["tactical_etf_component"] if col in returns.columns]
    inverse_cols = [col for col in ["conditional_inverse_sleeve"] if col in returns.columns]
    defensive_cols = [col for col in ["defensive_proxy_component"] if col in returns.columns]
    for mode_name, strategy_cols in strategy_modes.items():
        if not strategy_cols:
            continue
        for strategy_total in [round(x, 2) for x in np.arange(0.55, 0.901, 0.05)]:
            for inverse_total in [round(x, 3) for x in np.arange(0.00, 0.151, 0.025)]:
                for tactical_total in [round(x, 2) for x in np.arange(0.00, 0.201, 0.05)]:
                    defensive_total = 1 - strategy_total - inverse_total - tactical_total
                    if defensive_total < -1e-9:
                        continue
                    weights = pd.Series(0.0, index=returns.columns)
                    weights[strategy_cols] = strategy_total / len(strategy_cols)
                    if inverse_cols and inverse_total > 0:
                        weights[inverse_cols] = inverse_total / len(inverse_cols)
                    if tactical_cols and tactical_total > 0:
                        weights[tactical_cols] = tactical_total / len(tactical_cols)
                    if defensive_cols and defensive_total > 0:
                        weights[defensive_cols] = defensive_total / len(defensive_cols)
                    methods.append(
                        (
                            (
                                f"dynamic_grid_{mode_name}_s{strategy_total:.2f}_"
                                f"inv{inverse_total:.2f}_taa{tactical_total:.2f}_"
                                f"def{max(0.0, defensive_total):.2f}"
                            ),
                            weights,
                        )
                    )
    thresholds = DYNAMIC_GOAL["thresholds"]
    trials: list[dict[str, Any]] = []
    for n, (method, raw_weights) in enumerate(methods, start=1):
        weights = cap_weights(raw_weights, inverse_flags)
        port = returns[weights.index].mul(weights, axis=1).sum(axis=1)
        metrics = annualized_metrics(port)
        crisis = crisis_window_drawdowns(port)
        worst_crisis_drawdown = min([value for value in crisis.values() if not math.isnan(value)], default=math.nan)
        psr_value = psr(port, 0.0)
        dsr_value = dsr(port, n)
        walk_forward_positive = walk_forward_positive_rate(port)
        inverse_weight = float(sum(weights.get(col, 0.0) for col, flag in inverse_flags.items() if flag))
        failure_reasons = []
        if not metrics["cagr"] > thresholds["cagr_min"]:
            failure_reasons.append("cagr")
        if not metrics["sharpe"] > thresholds["sharpe_min"]:
            failure_reasons.append("sharpe")
        if not metrics["max_drawdown"] > thresholds["max_drawdown_min"]:
            failure_reasons.append("max_drawdown")
        if not psr_value >= thresholds["psr_min"]:
            failure_reasons.append("psr")
        if not dsr_value >= thresholds["dsr_min"]:
            failure_reasons.append("dsr")
        gate_status = "pass" if not failure_reasons else "fail"
        trials.append(
            {
                "n_trials_index": n,
                "optimizer_family": method,
                "components": "|".join(weights.index),
                "weights": json.dumps({k: round(float(v), 6) for k, v in weights.items()}, sort_keys=True),
                "inverse_weight": inverse_weight,
                "cagr": metrics["cagr"],
                "sharpe": metrics["sharpe"],
                "max_drawdown": metrics["max_drawdown"],
                "walk_forward_positive_rate": walk_forward_positive,
                "worst_crisis_drawdown": worst_crisis_drawdown,
                "psr": psr_value,
                "dsr": dsr_value,
                "gate_status": gate_status,
                "decision_reason": "all_gates_pass" if gate_status == "pass" else "failed_" + "_".join(failure_reasons),
                "validation_tier": "API-estimated",
                "cagr_gate": thresholds["cagr_min"],
                "sharpe_gate": thresholds["sharpe_min"],
                "max_drawdown_gate": thresholds["max_drawdown_min"],
            }
        )
    ledger_csv = dated_path("dynamic_trial_ledger", "csv", run_date)
    ledger_json = dated_path("dynamic_trial_ledger", "json", run_date)
    write_csv(ledger_csv, trials)
    write_json(
        ledger_json,
        {
            "rows": trials,
            "source_return_panel": return_file.as_posix(),
            "n_trials": len(trials),
            "thresholds": thresholds,
            "search_shape": "Narrow pre-registered dynamic grid across raw/timed strategy modes, conditional inverse sleeve, tactical ETF component, and defensive proxy.",
        },
    )
    append_iteration(
        "U6 Dynamic Optimizer And Promotion Gates",
        [
            f"- Optimized `{return_file.as_posix()}` using a narrow pre-registered dynamic grid.",
            f"- Wrote `{ledger_csv.as_posix()}` and `{ledger_json.as_posix()}`.",
            f"- Trials: {len(trials)}; passing allocations: {sum(1 for trial in trials if trial['gate_status'] == 'pass')}.",
            f"- Gates: CAGR > {thresholds['cagr_min']:.2%}, Sharpe > {thresholds['sharpe_min']:.2f}, max drawdown > {thresholds['max_drawdown_min']:.2%}.",
        ],
    )


def generate_dynamic_report(ledger_file: Path | None = None, run_date: str = TODAY) -> None:
    ledger_file = ledger_file or latest_file("dynamic_trial_ledger", "csv")
    ledger = pd.read_csv(ledger_file)
    if ledger.empty:
        raise SystemExit("Dynamic trial ledger is empty")
    winners = ledger[ledger["gate_status"] == "pass"].copy()
    sort_cols = ["sharpe", "cagr"]
    if not winners.empty:
        winners = winners.sort_values(sort_cols, ascending=[False, False]).head(10)
        report_path = dated_path("dynamic_candidate_promotion_report", "md", run_date)
        title = "Dynamic Candidate Promotion Report"
        body = [
            f"Created: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
            "",
            f"# {title}",
            "",
            "These are API-estimated nominations only. Native Portfolio123 Strategy Book validation is required before final performance claims.",
            "",
            "## Promoted Candidates",
            "",
            winners[
                [
                    "n_trials_index",
                    "optimizer_family",
                    "cagr",
                    "sharpe",
                    "max_drawdown",
                    "walk_forward_positive_rate",
                    "worst_crisis_drawdown",
                    "psr",
                    "dsr",
                    "inverse_weight",
                    "weights",
                ]
            ].to_string(index=False),
            "",
            "## Required Native Validation",
            "",
            "- Create `codex_` native component strategies only after user confirmation.",
            "- Validate the final Strategy Book in native P123 before declaring the target met.",
        ]
    else:
        best = ledger.sort_values(sort_cols, ascending=[False, False]).head(10)
        report_path = dated_path("dynamic_no_winner_report", "md", run_date)
        body = [
            f"Created: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
            "",
            "# Dynamic No-Winner Report",
            "",
            "No API-estimated dynamic candidate passed every pre-registered gate.",
            "",
            "## Nearest Misses",
            "",
            best[
                [
                    "n_trials_index",
                    "optimizer_family",
                    "cagr",
                    "sharpe",
                    "max_drawdown",
                    "walk_forward_positive_rate",
                    "worst_crisis_drawdown",
                    "psr",
                    "dsr",
                    "inverse_weight",
                    "weights",
                ]
            ].to_string(index=False),
            "",
            "## Interpretation",
            "",
            "- Do not loosen CAGR, Sharpe, drawdown, PSR, or DSR gates without a new approved plan.",
            "- Inspect whether the failure is ingredient-limited, timing-limited, or native-translation-limited before the next iteration.",
        ]
    report_path.write_text("\n".join(body) + "\n", encoding="utf-8")
    append_iteration(
        "U6 Dynamic Candidate Promotion Funnel",
        [
            f"- Read dynamic trial ledger `{ledger_file.as_posix()}`.",
            f"- Wrote `{report_path.as_posix()}`.",
            f"- Promoted API-estimated candidates: {len(winners)}.",
        ],
    )


def native_validation_package(ledger_file: Path | None = None, run_date: str = TODAY) -> None:
    ledger_file = ledger_file or latest_file("dynamic_trial_ledger", "csv")
    ledger = pd.read_csv(ledger_file)
    winners = ledger[ledger["gate_status"] == "pass"].sort_values(["sharpe", "cagr"], ascending=[False, False])
    path = dated_path("native_validation_package", "md", run_date)
    body = [
        f"Created: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}",
        "",
        "# Native Portfolio123 Validation Package",
        "",
        "This package prepares native validation only. It does not claim the Strategy Book target was met.",
        "",
        f"Source ledger: `{ledger_file.as_posix()}`",
        "",
    ]
    if winners.empty:
        body.extend(
            [
                "## Status",
                "",
                "No API-estimated dynamic candidate passed every promotion gate, so no native `codex_` object creation is recommended yet.",
            ]
        )
    else:
        winner = winners.iloc[0]
        weights = json.loads(winner["weights"])
        active_components = {component: float(weight) for component, weight in weights.items() if abs(float(weight)) > 1e-9}
        proposed_objects = ["codex_dynamic_strategy_book_candidate"]
        if any(component.endswith("_timed_200d") for component in active_components):
            proposed_objects.append("codex_dynamic_200d_timing_overlay_components")
        if active_components.get("tactical_etf_component", 0.0) > 0:
            proposed_objects.append("codex_dynamic_tactical_etf_component")
        if active_components.get("conditional_inverse_sleeve", 0.0) > 0:
            proposed_objects.append("codex_dynamic_conditional_inverse_component")
        body.extend(
            [
                "## Candidate To Validate",
                "",
                f"- Trial: `{int(winner['n_trials_index'])}`",
                f"- Optimizer family: `{winner['optimizer_family']}`",
                f"- API-estimated CAGR: {winner['cagr']:.2%}",
                f"- API-estimated Sharpe: {winner['sharpe']:.2f}",
                f"- API-estimated max drawdown: {winner['max_drawdown']:.2%}",
                "",
                "## Proposed Native Objects",
                "",
                *[f"- `{name}`" for name in proposed_objects],
                "",
                "## Allocation Weights",
                "",
            ]
        )
        for component, weight in sorted(active_components.items()):
            body.append(f"- `{component}`: {weight:.2%}")
        if not any(component in active_components for component in ["conditional_inverse_sleeve", "tactical_etf_component"]):
            body.extend(
                [
                    "",
                    "## Dynamic Component Note",
                    "",
                    "The promoted API-estimated candidate uses the 200-day timing overlay and defensive proxy. Conditional inverse and tactical ETF components were tested but did not appear in the promoted row.",
                ]
            )
        body.extend(
            [
                "",
                "## Confirmation Gate",
                "",
                "Ask the user before creating or modifying any native Portfolio123 object or running credit-heavy native validation.",
            ]
        )
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    append_iteration(
        "U7 Native Validation Package",
        [
            f"- Wrote `{path.as_posix()}`.",
            "- Package is a handoff for native P123 validation and makes no final performance claim.",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_init = sub.add_parser("init-goal")
    p_init.add_argument("--run-date", default=TODAY)
    p_dynamic_init = sub.add_parser("init-dynamic-goal")
    p_dynamic_init.add_argument("--run-date", default=TODAY)
    p_filter = sub.add_parser("filter-discovery")
    p_filter.add_argument("input", type=Path)
    p_filter.add_argument("--run-date", default=TODAY)
    p_expanded = sub.add_parser("merge-expanded-discovery")
    p_expanded.add_argument("inputs", nargs="+", type=Path)
    p_expanded.add_argument("--run-date", default=TODAY)
    p_feas = sub.add_parser("strategy-feasibility")
    p_feas.add_argument("--discovery", type=Path)
    p_feas.add_argument("--run-date", default=TODAY)
    p_etf = sub.add_parser("validate-etfs")
    p_etf.add_argument("--run-date", default=TODAY)
    p_etf.add_argument("--start", default="1900-01-01")
    p_etf.add_argument("--end")
    p_panel = sub.add_parser("build-panel")
    p_panel.add_argument("--price-file", type=Path)
    p_panel.add_argument("--run-date", default=TODAY)
    p_timing = sub.add_parser("build-timing-signals")
    p_timing.add_argument("--return-file", type=Path)
    p_timing.add_argument("--run-date", default=TODAY)
    p_dynamic_panel = sub.add_parser("build-dynamic-panel")
    p_dynamic_panel.add_argument("--return-file", type=Path)
    p_dynamic_panel.add_argument("--timing-file", type=Path)
    p_dynamic_panel.add_argument("--run-date", default=TODAY)
    p_opt = sub.add_parser("optimize")
    p_opt.add_argument("--return-file", type=Path)
    p_opt.add_argument("--etf-file", type=Path)
    p_opt.add_argument("--run-date", default=TODAY)
    p_opt.add_argument("--cagr-min", type=float)
    p_opt.add_argument("--sharpe-min", type=float)
    p_opt.add_argument("--max-drawdown-min", type=float)
    p_opt.add_argument("--artifact-prefix", default="")
    p_report = sub.add_parser("report")
    p_report.add_argument("--ledger-file", type=Path)
    p_report.add_argument("--run-date", default=TODAY)
    p_report.add_argument("--artifact-prefix", default="")
    p_dynamic_opt = sub.add_parser("dynamic-optimize")
    p_dynamic_opt.add_argument("--return-file", type=Path)
    p_dynamic_opt.add_argument("--etf-file", type=Path)
    p_dynamic_opt.add_argument("--run-date", default=TODAY)
    p_dynamic_report = sub.add_parser("dynamic-report")
    p_dynamic_report.add_argument("--ledger-file", type=Path)
    p_dynamic_report.add_argument("--run-date", default=TODAY)
    p_native_package = sub.add_parser("native-package")
    p_native_package.add_argument("--ledger-file", type=Path)
    p_native_package.add_argument("--run-date", default=TODAY)
    args = parser.parse_args()
    if args.command == "init-goal":
        init_goal(args.run_date)
    elif args.command == "init-dynamic-goal":
        init_dynamic_goal(args.run_date)
    elif args.command == "filter-discovery":
        filter_discovery(args.input, args.run_date)
    elif args.command == "merge-expanded-discovery":
        merge_expanded_discovery(args.inputs, args.run_date)
    elif args.command == "strategy-feasibility":
        classify_strategy_feasibility(args.discovery, args.run_date)
    elif args.command == "validate-etfs":
        validate_etf_universe(args.run_date, args.start, args.end)
    elif args.command == "build-panel":
        price_returns(args.price_file, args.run_date)
    elif args.command == "build-timing-signals":
        build_timing_signals(args.return_file, args.run_date)
    elif args.command == "build-dynamic-panel":
        build_dynamic_panel(args.return_file, args.timing_file, args.run_date)
    elif args.command == "optimize":
        optimize_panel(
            args.return_file,
            args.etf_file,
            args.run_date,
            cagr_min=args.cagr_min,
            sharpe_min=args.sharpe_min,
            max_drawdown_min=args.max_drawdown_min,
            artifact_prefix=args.artifact_prefix,
        )
    elif args.command == "report":
        generate_report(args.ledger_file, args.run_date, args.artifact_prefix)
    elif args.command == "dynamic-optimize":
        dynamic_optimize(args.return_file, args.etf_file, args.run_date)
    elif args.command == "dynamic-report":
        generate_dynamic_report(args.ledger_file, args.run_date)
    elif args.command == "native-package":
        native_validation_package(args.ledger_file, args.run_date)


if __name__ == "__main__":
    main()
