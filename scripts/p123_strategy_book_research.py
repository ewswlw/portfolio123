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
        "psr",
        "dsr",
        "inverse_weight",
        "weights",
    ]
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p_init = sub.add_parser("init-goal")
    p_init.add_argument("--run-date", default=TODAY)
    p_filter = sub.add_parser("filter-discovery")
    p_filter.add_argument("input", type=Path)
    p_filter.add_argument("--run-date", default=TODAY)
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
    args = parser.parse_args()
    if args.command == "init-goal":
        init_goal(args.run_date)
    elif args.command == "filter-discovery":
        filter_discovery(args.input, args.run_date)
    elif args.command == "strategy-feasibility":
        classify_strategy_feasibility(args.discovery, args.run_date)
    elif args.command == "validate-etfs":
        validate_etf_universe(args.run_date, args.start, args.end)
    elif args.command == "build-panel":
        price_returns(args.price_file, args.run_date)
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


if __name__ == "__main__":
    main()
