# MODUWORK — Painel de automação da prospecção

Este repositório é o **agendador e painel de controle público** da prospecção 2027 da MODU. O repositório **privado** `felipevieira-coder/modu` continua sendo a fonte canônica dos playbooks, regras, testes e motor de enriquecimento (migração original de 2026-10-10). **Nenhuma lista de contatos, planilha, e-mail, credencial ou evidência pessoal deve ser commitada aqui.**

## O que foi preparado

- [Workflow automático](.github/workflows/modu-prospecting-autopilot.yml): a cada hora no minuto 17, além de execução manual pelo botão **Run workflow**.
- [Launcher do motor canônico](prospecting/run_core.py): pesquisa faltantes, filtra **somente edições de 2027**, aplica os validadores e atualiza a aba **EXPOSITORES | BASE ÚNICA**.
- [Radar de novos expositores](prospecting/discover.py): busca pública e incremental para feiras de 2027, deduplica e grava **somente pistas** na aba **NOVOS EXPOSITORES | REVISAO**. Não cria automaticamente expositor confirmado.
- [Índice das 200 técnicas](prospecting/INDICE_200_TECNICAS.md): catálogo de nomes e grupos; 127 técnicas do conjunto padrão, 73 adicionais sob demanda.
- [Skill do agente](skills/modu-prospecting-autopilot/SKILL.md): protocolo de decisão e operação.

## Configuração inicial (obrigatória)

Em `Settings > Secrets and variables > Actions` deste repositório:

| Tipo | Nome | Valor |
|---|---|---|
| Secret | `MODU_SOURCE_TOKEN` | GitHub fine-grained PAT com **Contents: Read-only** no repo privado `felipevieira-coder/modu`; sem permissão de escrita |
| Secret | `OPENAI_API_KEY` | Chave da API OpenAI, com limite de orçamento |
| Secret | `GOOGLE_SERVICE_ACCOUNT_JSON` | JSON completo de uma service account Google autorizada a editar o Sheets |
| Secret | `MODU_SPREADSHEET_ID` | ID da planilha `Expositores Feiras`, sem URL |
| Variable | `MODU_AUTOMATION_ENABLED` | `true` apenas quando tudo tiver sido testado |
| Variable | `MODU_DISCOVERY_ENABLED` | `true` para habilitar o radar de novos expositores; opcional |
| Variable | `MODU_MAX_ROWS` | `20` por ciclo inicialmente; limite rígido de 100 |
| Variable | `MODU_OPENAI_MODEL` | Modelo compatível com Responses API, web_search e JSON schema; padrão `gpt-5.5` |

**Importante:** a conta de serviço indicada no JSON tem um campo `client_email`. Compartilhe a planilha com esse e-mail como **Editor**. Nunca coloque o JSON em arquivos do repo nem em tickets do GitHub.

## Ativação sem risco de envio

1. Configure os quatro secrets e compartilhe a planilha com a service account.
2. Em **Actions > MODU | Prospeccao autonoma > Run workflow**, execute com `dry_run=true`. O radar fica desligado até que `MODU_DISCOVERY_ENABLED=true`.
3. Confirme que as linhas elegíveis são 2027, que o motor consegue ler os cabeçalhos e que os critérios de evidência são aplicados.
4. Rode manualmente com `dry_run=false` e `MODU_MAX_ROWS=3`, conferindo as alterações na planilha.
5. Defina `MODU_AUTOMATION_ENABLED=true`; inicie com 20 e só aumente após auditoria de qualidade.
6. Opcionalmente ative o radar. Ele cria fila de revisão, não aprova expositores por conta própria.

A execução agendada **não será processada** enquanto a variável `MODU_AUTOMATION_ENABLED` não for `true`. O código já está versionado, porém **não significa que o agendamento esteja operacional** até as credenciais serem configuradas e o primeiro ciclo ser validado.

## Fluxo e dashboard

```text
GitHub Actions (cron, manual)
  -> checkout do motor privado modu
  -> Google Sheets / EXPOSITORES | BASE ÚNICA
      -> seleção só 2027 -> busca pública -> score -> hard gates
      -> atualização serial e readback
  -> radar opcional -> NOVOS EXPOSITORES | REVISAO
  -> contagem agregada no Actions (sem dados pessoais)
```

Abra a aba **Actions** para ver execuções, falhas e um resumo agregado. O GitHub Actions não fornece atualização em tempo real contínua: ele agenda novos ciclos (inclusive com possível atraso). O botão **Run workflow** permite rodar um ciclo extra.

## Controles e restrições

- Nunca entrar ou automatizar scraping do LinkedIn; URL pode ser usada somente com procedência válida.
- Não ultrapassar termos de sites, robots, CAPTCHA, paywall, rate limits, opt-out ou controles de acesso.
- Não enviar e-mails/WhatsApp automaticamente neste projeto.
- Não publicar dados de decisores em repositório público nem nos logs.
- Classificação por fontes e validação crítica antes de promoção; novos expositores permanecem na fila de revisão.
- O token do repositório privado **não** precisa de permissões de escrita.

**Custo:** GitHub Actions e OpenAI API podem gerar cobranças. Controle o orçamento na conta da API e mantenha `MODU_MAX_ROWS` conservador.
