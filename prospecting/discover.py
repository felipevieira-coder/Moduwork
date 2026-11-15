"""Descoberta incremental de expositores 2027 para aba privada de revisao.

Sem scraping do LinkedIn, sem bypass, sem envio de mensagens e sem publicar leads
no repositorio. Os resultados da busca sao PISTAS: nao prova automatica de presenca.
"""
from __future__ import annotations

import json
import os
import re
import unicodedata
from datetime import datetime, timezone
from urllib.parse import urlparse
from zoneinfo import ZoneInfo

FAIRS = (
    "CIOSP 2027", "ABUP 2027", "ABCasa 2027", "Abrin 2027",
    "Plastico Brasil 2027", "FEICON 2027", "Wire Brasil 2027",
    "ABRH CONARH 2027", "SRE Trade Show 2027", "Full Face 2027",
    "InfraFM 2027",
)
HEADERS = [
    "Empresa", "Feira", "Ano", "Site", "Estande",
    "URL alegada da organizadora", "URL de corroboracao",
    "Motivo / evidencias", "Capturado em (UTC)", "Status",
]

RECORD = {
    "type": "object",
    "properties": {
        "company": {"type": "string"},
        "website": {"type": "string"},
        "booth": {"type": "string"},
        "organizer_url": {"type": "string"},
        "corroboration_url": {"type": "string"},
        "reason": {"type": "string"},
    },
    "required": [
        "company", "website", "booth", "organizer_url", "corroboration_url", "reason"
    ],
    "additionalProperties": False,
}
SCHEMA = {
    "type": "object",
    "properties": {"candidates": {"type": "array", "items": RECORD}},
    "required": ["candidates"],
    "additionalProperties": False,
}


def normalize(s: str) -> str:
    ascii_text = unicodedata.normalize("NFKD", str(s).casefold())
    ascii_text = "".join(ch for ch in ascii_text if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", ascii_text)


def source_url(url: str) -> str:
    try:
        p = urlparse(url.strip())
        host = (p.hostname or "").lower()
        if (p.scheme != "https" or not host or host in
            {"linkedin.com", "www.linkedin.com", "google.com", "www.google.com"}
            or host.endswith(".linkedin.com")):
            return ""
        if p.username or p.password:
            return ""
        return url.strip()
    except (TypeError, ValueError):
        return ""


def choose_fair(now: datetime) -> str:
    # Distribuicao deterministica sem checkpoint persistente.
    return FAIRS[(now.toordinal() * 24 + now.hour) % len(FAIRS)]


def search_exhibitors(fair: str) -> list[dict]:
    from openai import OpenAI
    model = os.getenv("OPENAI_MODEL", "gpt-5.5")
    prompt = (
        "Pesquise o diretorio de expositores e fontes OFICIAIS da feira "
        f"{fair}. Busque ate 12 empresas com provas datadas especificamente "
        "da edicao 2027. Priorize a organizadora, catalogo oficial e noticias "
        "corporativas. Nao confunda patrocinador, palestrante e expositor. "
        "Somente links https existentes; nao invente URLs, empresas, sites, "
        "numero de estande ou participacao. Se nenhuma prova acessivel "
        "existir, retorne candidates vazio. Retorne pistas para revisao "
        "humana, sem afirmar que foram verificadas por este programa. "
        "Nao automatize o LinkedIn, nao busque dados pessoais, nao contorne "
        "login, robots ou restricoes."
    )
    response = OpenAI().responses.create(
        model=model,
        tools=[{"type": "web_search", "search_context_size": "medium"}],
        tool_choice="required",
        input=prompt,
        text={"format": {
            "type": "json_schema",
            "name": "modu_fair_discovery",
            "schema": SCHEMA,
            "strict": True,
        }},
    )
    return json.loads(response.output_text).get("candidates", [])[:12]


def main() -> int:
    import gspread
    from modu_enricher.schema_bridge import SheetSchema

    now = datetime.now(ZoneInfo("America/Sao_Paulo"))
    fair = choose_fair(now)
    gc = gspread.service_account(filename=os.environ["GOOGLE_SERVICE_ACCOUNT_FILE"])
    workbook = gc.open_by_key(os.environ["SPREADSHEET_ID"])
    base = workbook.worksheet(os.getenv("SHEET_NAME", "EXPOSITORES | BASE ÚNICA"))
    target_name = os.getenv("DISCOVERY_SHEET_NAME", "NOVOS EXPOSITORES | REVISAO")

    try:
        staging = workbook.worksheet(target_name)
    except gspread.WorksheetNotFound:
        staging = workbook.add_worksheet(title=target_name, rows=500, cols=10)
        staging.update(range_name="A1:J1", values=[HEADERS])

    if staging.row_values(1) != HEADERS:
        raise RuntimeError("Cabeçalhos da fila de revisao divergentes; nenhuma escrita efetuada")

    base_rows = base.get_all_values()
    schema = SheetSchema.from_headers(base_rows[0])
    def fair_key(s: str) -> str:
        return re.sub(r"20\d{2}", "", normalize(s))

    known = set()
    for row in base_rows[1:]:
        year_and_fair = schema.get(row, "data_edicao") + " " + schema.get(row, "feira")
        if "2027" in year_and_fair:
            known.add((normalize(schema.get(row, "company")),
                       fair_key(schema.get(row, "feira"))))
    staged_rows = staging.get_all_values()
    known.update(
        (normalize(row[0]), fair_key(row[1]))
        for row in staged_rows[1:] if len(row) >= 2
    )
    candidates = search_exhibitors(fair)
    pending = []
    for c in candidates:
        company = str(c.get("company", "")).strip()
        organizer = source_url(str(c.get("organizer_url", "")))
        corroboration = source_url(str(c.get("corroboration_url", "")))
        if not company or not organizer or not corroboration:
            continue
        if normalize(company) in {"", "expositor", "patrocinador"}:
            continue
        key = (normalize(company), fair_key(fair))
        if key in known:
            continue
        known.add(key)
        pending.append([
            company[:240], fair, "2027", str(c.get("website", ""))[:300],
            str(c.get("booth", ""))[:80], organizer, corroboration,
            str(c.get("reason", ""))[:900],
            datetime.now(timezone.utc).isoformat(), "REVIEW_REQUIRED"
        ])
    if pending:
        staging.append_rows(pending, value_input_option="RAW")
    print(
        f"MODU discovery | fair={fair} | candidates={len(candidates)} "
        f"| review_rows_created={len(pending)} | verified_automatically=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
