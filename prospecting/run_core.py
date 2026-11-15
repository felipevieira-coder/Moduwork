"""Executor seguro do Decision Enricher canônico, sem expor leads em logs públicos.

O código/200 técnicas permanecem no repositório privado modu.
Este launcher opera somente sobre feiras de 2027 e não envia e-mails.
"""
from __future__ import annotations

import contextlib
import io
import os
import tempfile
from pathlib import Path


def main() -> int:
    from modu_enricher import engine as engine_module
    from modu_enricher.selector import select_queue as base_select_queue, event_year
    from modu_enricher.sheets import SheetsClient

    # Adaptador explícito: o seletor original prioriza datas, mas não restringe o ano.
    # Não alterar status/linhas de feiras de anos diferentes.
    def only_2027(rows, eligibility, today=None, excluded_events=()):
        applicable = [row for row in rows if event_year(row) == 2027]
        return base_select_queue(
            applicable, eligibility, today=today, excluded_events=excluded_events
        )

    engine_module.select_queue = only_2027

    max_rows = max(1, min(100, int(os.getenv("MODU_MAX_ROWS", "20"))))
    dry_run = os.getenv("MODU_DRY_RUN", "false").lower() == "true"
    spread_id = os.environ["SPREADSHEET_ID"]
    sheet_name = os.getenv("SHEET_NAME", "EXPOSITORES | BASE ÚNICA")

    # GitHub Actions e efêmero. A fila permanente é a planilha:
    # status VALIDADO/REVIEW_REQUIRED e datas são relidas no próximo ciclo.
    with tempfile.TemporaryDirectory(prefix="modu-worker-") as tmp:
        tmpdir = Path(tmp)
        private_module = Path(engine_module.__file__).resolve()
        repo_root = private_module.parents[2]  # .../prospecting/decision_enricher
        policy_file = repo_root / "config" / "policy.yaml"
        if not policy_file.exists():
            raise RuntimeError("Politica canonica nao encontrada")
        capture = io.StringIO()
        with contextlib.redirect_stdout(capture):
            sheet = SheetsClient(spread_id, sheet_name)
            engine = engine_module.Engine(
                sheets=sheet,
                policy_path=str(policy_file),
                state_db=str(tmpdir / "state.sqlite3"),
                audit_jsonl=str(tmpdir / "audit.jsonl"),
                model=os.getenv("OPENAI_MODEL"),
            )
            counts = engine.run(forever=False, dry_run=dry_run, max_rows=max_rows)

    # Nenhum nome, URL pessoal, dados de planilha ou payload de pesquisa nos logs.
    safe = {k: int(counts.get(k, 0)) for k in
            ("processed", "validated", "probable", "review", "errors")}
    print(f"MODU 2027 | dry_run={dry_run} | aggregate={safe}", flush=True)
    if safe["processed"] and safe["errors"] == safe["processed"]:
        raise RuntimeError("Todas as linhas processadas falharam; conferir credenciais e fontes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
