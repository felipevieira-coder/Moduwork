"""Always-on orchestrator: one writer, durable SQLite checkpoint, no PII in telemetry."""
from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("America/Sao_Paulo")
DEFAULT_TOTALS = {"processed": 0, "validated": 0, "probable": 0, "review": 0, "errors": 0}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def local_day() -> str:
    return datetime.now(TZ).date().isoformat()


def bounded_int(name: str, default: int, lo: int, hi: int) -> int:
    try:
        return max(lo, min(hi, int(os.getenv(name, str(default)))))
    except (TypeError, ValueError):
        return default


class RuntimeState:
    def __init__(self, data_dir: str):
        self.lock = threading.RLock()
        self.path = Path(data_dir) / "metrics" / "status.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        saved = {}
        if self.path.exists():
            try:
                saved = json.loads(self.path.read_text(encoding="utf-8"))
            except (ValueError, OSError):
                saved = {}
        self.data = {
            "state": "starting",
            "started_at": utc_now(),
            "last_run_started_at": saved.get("last_run_started_at"),
            "last_run_finished_at": saved.get("last_run_finished_at"),
            "last_success_at": saved.get("last_success_at"),
            "last_discovery_at": saved.get("last_discovery_at"),
            "cycles": int(saved.get("cycles", 0)),
            "totals": {k: int(saved.get("totals", {}).get(k, 0)) for k in DEFAULT_TOTALS},
            "last_batch": saved.get("last_batch", dict(DEFAULT_TOTALS)),
            "today_date": saved.get("today_date", local_day()),
            "today_processed": int(saved.get("today_processed", 0)),
            "last_error_code": saved.get("last_error_code", ""),
            "mode": "dry-run" if os.getenv("MODU_DRY_RUN", "true").lower() == "true" else "write",
            "source": "private-modu",
            "target_year": 2027,
            "next_cycle_at": None,
        }
        self.rotate_day()
        self.save()

    def rotate_day(self):
        if self.data["today_date"] != local_day():
            self.data["today_date"] = local_day()
            self.data["today_processed"] = 0

    def save(self):
        with self.lock:
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self.data, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, self.path)

    def update(self, **kwargs):
        with self.lock:
            self.rotate_day()
            self.data.update(kwargs)
            self.save()

    def snapshot(self):
        with self.lock:
            self.rotate_day()
            copy = json.loads(json.dumps(self.data))
        copy["daily_limit"] = bounded_int("MAX_DAILY_ROWS", 100, 1, 2000)
        copy["cycle_interval_seconds"] = bounded_int("CYCLE_INTERVAL_SECONDS", 900, 60, 86400)
        copy["max_rows_per_cycle"] = bounded_int("MODU_MAX_ROWS", 10, 1, 100)
        return copy


def missing_config() -> list[str]:
    required = ["OPENAI_API_KEY", "MODU_SPREADSHEET_ID", "STATUS_TOKEN", "MODU_SOURCE_TOKEN"]
    missing = [name for name in required if not os.getenv(name)]
    if not (os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON") or os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE")):
        missing.append("GOOGLE_SERVICE_ACCOUNT_JSON")
    return missing


def configure_google_credentials():
    raw = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
    if raw:
        parsed = json.loads(raw)
        if parsed.get("type") != "service_account" or not parsed.get("client_email"):
            raise ValueError("GOOGLE_SERVICE_ACCOUNT_JSON_invalid")
        handle = tempfile.NamedTemporaryFile(
            mode="w", prefix="modu-google-", suffix=".json", delete=False
        )
        try:
            json.dump(parsed, handle)
            handle.close()
            os.chmod(handle.name, 0o600)
            os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"] = handle.name
        except BaseException:
            handle.close()
            raise
    elif not Path(os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "missing")).is_file():
        raise ValueError("GOOGLE_SERVICE_ACCOUNT_FILE_missing")


def run_private_engine(data_dir: str, max_rows: int, dry_run: bool) -> dict:
    from modu_enricher import engine as engine_module
    from modu_enricher.sheets import SheetsClient
    from modu_enricher.selector import select_queue as base_queue, event_year

    def queue_for_2027(rows, eligibility, today=None, excluded_events=()):
        return base_queue(
            [row for row in rows if event_year(row) == 2027],
            eligibility, today=today, excluded_events=excluded_events
        )

    engine_module.select_queue = queue_for_2027
    canonical_root = Path(engine_module.__file__).resolve().parents[2]
    policy = canonical_root / "config" / "policy.yaml"
    if not policy.is_file():
        raise RuntimeError("canonical_policy_missing")

    os.environ["EXCLUDED_EVENTS"] = os.getenv("EXCLUDED_EVENTS", "GL EVENTS")
    os.environ["RESEARCH_WORKERS"] = str(bounded_int("RESEARCH_WORKERS", 2, 1, 4))
    os.environ["RESEARCH_BATCH_SIZE"] = str(bounded_int("RESEARCH_BATCH_SIZE", 8, 1, 20))
    os.environ["REFRESH_AFTER_ROWS"] = str(bounded_int("REFRESH_AFTER_ROWS", 8, 1, 100))
    os.environ["STATE_DB"] = str(Path(data_dir) / "state" / "prospecting.sqlite3")
    os.environ["AUDIT_JSONL"] = str(Path(data_dir) / "audit" / "private-evidence.jsonl")
    Path(os.environ["STATE_DB"]).parent.mkdir(parents=True, exist_ok=True)
    Path(os.environ["AUDIT_JSONL"]).parent.mkdir(parents=True, exist_ok=True)

    # The upstream engine prints companies. Never forward that output to public logs.
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        sheets = SheetsClient(
            os.environ["MODU_SPREADSHEET_ID"],
            os.getenv("SHEET_NAME", "EXPOSITORES | BASE ÚNICA")
        )
        engine = engine_module.Engine(
            sheets=sheets,
            policy_path=str(policy),
            state_db=os.environ["STATE_DB"],
            audit_jsonl=os.environ["AUDIT_JSONL"],
            model=os.getenv("OPENAI_MODEL", "gpt-5.5")
        )
        counts = engine.run(forever=False, dry_run=dry_run, max_rows=max_rows)
    return {key: int(counts.get(key, 0)) for key in DEFAULT_TOTALS}


def run_discovery():
    import sys
    sys.path.insert(0, "/app")
    from prospecting import discover
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        discover.main()


def worker_loop(state: RuntimeState, stop: threading.Event):
    interval = bounded_int("CYCLE_INTERVAL_SECONDS", 900, 60, 86400)
    limit = bounded_int("MAX_DAILY_ROWS", 100, 1, 2000)
    max_batch = bounded_int("MODU_MAX_ROWS", 10, 1, 100)
    discovery_every = bounded_int("DISCOVERY_INTERVAL_SECONDS", 14400, 3600, 604800)

    while not stop.is_set():
        state.rotate_day()
        enabled = os.getenv("MODU_AUTOMATION_ENABLED", "false").lower() == "true"
        missing = missing_config()
        if not enabled:
            state.update(state="paused", last_error_code="", next_cycle_at=None)
            stop.wait(30)
            continue
        if missing:
            state.update(state="config_required", last_error_code="missing_secrets", next_cycle_at=None)
            stop.wait(60)
            continue
        if state.snapshot()["today_processed"] >= limit:
            state.update(state="daily_limit", last_error_code="", next_cycle_at=None)
            stop.wait(min(interval, 300))
            continue

        dry_run = os.getenv("MODU_DRY_RUN", "true").lower() == "true"
        remaining = limit - state.snapshot()["today_processed"]
        state.update(
            state="running", mode="dry-run" if dry_run else "write",
            last_run_started_at=utc_now(), last_error_code="", next_cycle_at=None
        )
        try:
            configure_google_credentials()
            counts = run_private_engine(os.getenv("DATA_DIR", "/data"), min(max_batch, remaining), dry_run)
            with state.lock:
                state.rotate_day()
                state.data["cycles"] += 1
                state.data["last_batch"] = counts
                state.data["today_processed"] += counts["processed"]
                for k in DEFAULT_TOTALS:
                    state.data["totals"][k] += counts[k]
                state.data["last_run_finished_at"] = utc_now()
                state.data["last_success_at"] = utc_now()
                state.data["state"] = "idle"
                state.save()

            # Discovery is explicitly opt-in and never runs while testing dry-run.
            if os.getenv("DISCOVERY_ENABLED", "false").lower() == "true" and not dry_run:
                last = state.snapshot()["last_discovery_at"]
                due = True
                if last:
                    try:
                        due = (datetime.now(timezone.utc) -
                               datetime.fromisoformat(last)).total_seconds() >= discovery_every
                    except ValueError:
                        pass
                if due:
                    try:
                        run_discovery()
                        state.update(last_discovery_at=utc_now())
                    except Exception as exc:
                        state.update(last_error_code="discovery_" + type(exc).__name__)
        except Exception as exc:
            # Never print raw exceptions: provider errors may embed contact details.
            state.update(state="error", last_run_finished_at=utc_now(),
                         last_error_code=type(exc).__name__)
        state.update(next_cycle_at=datetime.fromtimestamp(
            time.time() + interval, timezone.utc).isoformat(timespec="seconds"))
        stop.wait(interval)
