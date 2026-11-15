# MODU Prospect Intelligence Cloud — v1.0

**Objetivo:** serviço persistente (24/7 enquanto o provedor o mantiver online), com pesquisa incremental de decisores, checkpoint persistido, limites de custo, dashboard protegido, atualização automática da base privada e retomada após falha.

## Arquitetura

- **Repositório público de implantação:** `felipevieira-coder/Moduwork` — Docker, painel sem dados pessoais, workflow CI, skill e índice das técnicas.
- **Repositório privado de inteligência:** `felipevieira-coder/modu` — código `prospecting/decision_enricher`, validação das evidências e playbook completo. Obtido no *startup*, não incluído na imagem Docker e não publicado.
- **Persistência:** volume montado em `/data`, contendo checkpoint SQLite, métricas agregadas, log privado de evidências. Faça backups do volume.
- **Fonte de verdade dos leads:** Google Sheets `Expositores Feiras` / aba `EXPOSITORES | BASE ÚNICA`. Radar opcional: aba `NOVOS EXPOSITORES | REVISAO`.
- **Cloud:** instância persistente Railway (ou outro host compatível com Docker e disco). Configure 1 réplica; restart policy `ALWAYS` disponível em plano compatível. Intervalo de trabalho: 15 minutos por padrão; dashboard atualiza a cada 20 segundos.
- **Observabilidade:** HTTP `GET /healthz` (apenas liveness), HTML `GET /` e `GET /api/status` com `Authorization: Bearer <STATUS_TOKEN>`. API retorna apenas estatísticas agregadas.

## Implantação no Railway

1. Crie um projeto Railway e um serviço a partir do repositório GitHub `felipevieira-coder/Moduwork`. O Dockerfile e o `railway.json` estão prontos.
2. Adicione um **Volume** ao serviço com caminho de montagem **/data** e habilite backups. Não escale acima de **1 réplica**, pois SQLite usa lock e há um único escritor.
3. Em Variables, cadastre os segredos, sem copiá-los para GitHub ou mensagens:
   - `MODU_SOURCE_TOKEN`: token GitHub fine-grained com permissão **Contents: Read** somente no repositório privado `felipevieira-coder/modu`.
   - `OPENAI_API_KEY`: chave da API OpenAI com teto de gasto configurado no provedor.
   - `GOOGLE_SERVICE_ACCOUNT_JSON`: conteúdo JSON integral de uma conta de serviço Google.
   - `MODU_SPREADSHEET_ID`: ID da planilha existente.
   - `STATUS_TOKEN`: segredo aleatório longo exclusivo do painel (recomenda-se >=32 caracteres).
4. Compartilhe **somente a planilha necessária** com o `client_email` da conta de serviço, como Editor. Teste o acesso com uma conta de baixo privilégio.
5. Defina `MODU_AUTOMATION_ENABLED=true` e **`MODU_DRY_RUN=true`** para execução inicial **sem gravar** na base. O teste ainda pode consumir pesquisas pagas.
6. Acesse a URL gerada pelo Railway e insira o `STATUS_TOKEN` no painel. Valide `/healthz` e veja as contagens do ciclo.
7. Após verificar 3 a 10 resultados, altere `MODU_DRY_RUN=false` para permitir **atualizar somente células faltantes e registros autorizados**, respeitando os validadores.
8. Ative `DISCOVERY_ENABLED=true` opcionalmente para criar pistas de expositores 2027 na aba de revisão.
9. No GitHub, em **Moduwork → Settings → Secrets and variables → Actions → Variables**, configure `MODU_CLOUD_PRIMARY=true` para que o agendador GitHub **não execute o segundo escritor** em paralelo com a cloud.

**Não crie o projeto Railway nem ative os secrets pelo chat sem verificar as permissões.** Não cole credenciais aqui: use o gestor de variáveis secretas do próprio host.

## Variáveis de operação

| Variável | Padrão | Efeito |
|---|---|---|
| `MODU_AUTOMATION_ENABLED` | `false` | Interruptor geral; sem `true` não há pesquisa |
| `MODU_DRY_RUN` | `true` | Pesquisa sem alterar Sheets |
| `CYCLE_INTERVAL_SECONDS` | `900` | Pausa entre ciclos (mín. 60 segundos) |
| `MODU_MAX_ROWS` | `10` | Limite de linhas pesquisadas por ciclo (máx. 100) |
| `MAX_DAILY_ROWS` | `100` | Limite de tentativas por dia (máx. 2000) |
| `RESEARCH_WORKERS` | `2` | Pesquisas simultâneas (1 a 4) |
| `DISCOVERY_ENABLED` | `false` | Radar adicional; sempre para revisão |
| `DISCOVERY_INTERVAL_SECONDS` | `14400` | Intervalo entre buscas de novos expositores |
| `OPENAI_MODEL` | `gpt-5.5` | Modelo compatível com web_search e JSON Schema |
| `STATUS_TOKEN` | obrigatório | Autentica leitura de estatísticas |
| `DATA_DIR` | `/data` | Volume persistente |
| `PORT` | `8080` | Servidor do dashboard |

Se o intervalo do ciclo for menor do que a duração da pesquisa, **não inicia outra pesquisa em paralelo**: a próxima execução começa após o término e o intervalo de descanso. Quando não houver novos itens, o ciclo permanece ativo e reconsulta a fonte de verdade, mas não inventa contatos.

## Auditoria e proteção

- Não opera o LinkedIn por automação não autorizada e não coleta números privados.
- Exige evidência de vínculo atual, fonte autorizada, validação da edição de 2027 e gates de confiança.
- Registra `VALIDADO`, `PROVÁVEL VALIDADO`, `REVIEW_REQUIRED`; não altera decisores existentes sem correspondência.
- Mantém um único escritor, limite diário, backup SQLite e `opt-out` como regras do core.
- O dashboard **não** retorna nomes, links pessoais, telefones ou evidências. A trilha detalhada fica no volume privado.
- O serviço tem capacidade de **retomar após reinícios**, não garantia literal de 100% de disponibilidade. Cloud, rede, APIs e credenciais podem falhar. Configure alertas externos em `/healthz` e backups de volume.
- O monitoramento `/healthz` confirma processo HTTP disponível, não garante que uma pesquisa foi concluída; consulte os timestamps e `last_error_code` no painel.

## Teste local

```bash
cp .env.cloud.example .env
# preencha .env localmente; não envie para o Git
docker compose up --build -d
# abra http://localhost:8080
```

Uma chamada local no Python sem docker pode testar o controle e dashboard, mas o engine real requer dependências e credenciais.

## Histórico da v1

- Worker contínuo gerenciado pela cloud.
- Retomada via SQLite, checkpoint e logs em volume persistente.
- Filtro **somente feiras 2027**, um decisor principal por empresa.
- Limites de consumo/dia e gates de revisão.
- Dashboard protegido com refresh automático (20 s).
- GitHub como fonte de código, não como repositório de dados pessoais.
