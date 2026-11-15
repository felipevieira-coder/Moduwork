---
name: modu-prospecting-autopilot
description: Orquestra pesquisa B2B etica de expositores 2027 e validacao de decisores na base MODU; sem automacao do LinkedIn, sem divulgacao de PII e com QA.
---

# MODU — Skill Prospecting Autopilot

## Fonte de verdade

- Motor privado: `felipevieira-coder/modu/prospecting/decision_enricher`.
- Regras completas: `felipevieira-coder/modu/prospecting/PLAYBOOK_MODU_200_TECNICAS_SCRAPING_HQ_DECISION_INTELLIGENCE.md`.
- Manifesto: `felipevieira-coder/modu/prospecting/ETHICAL_SCRAPING_ACTIVE_127_MANIFEST.yaml`.
- Controle e agenda: `felipevieira-coder/Moduwork/.github/workflows/modu-prospecting-autopilot.yml`.
- Índice consultável: `prospecting/INDICE_200_TECNICAS.md`.

## Objetivo

A cada execução agendada:

1. Conectar à planilha privada `Expositores Feiras`, aba `EXPOSITORES | BASE ÚNICA`.
2. Filtrar feiras com edição confirmada em 2027, privilegiando as próximas datas.
3. Verificar empresas sem decisor/cargo/LinkedIn completo.
4. Pesquisar fontes públicas autorizadas e usar apenas técnicas pertinentes, registrando IDs aplicados.
5. Priorizar responsáveis por Eventos/Feiras/Brand Experience, depois Trade, Marketing com responsabilidade por eventos e Procurement pertinente; CEO apenas fallback excepcional para PME.
6. Exigir vínculo atual, boa evidência, identidade corroborada e aprovação dos hard gates existentes.
7. Atualizar células vazias com readback antes de concluir, sem substituir um decisor melhor já registrado.
8. Marcar ambiguidade como `REVIEW_REQUIRED`; não inventar perfis, nem enviar mensagens.
9. Para novos expositores, pesquisar exclusivamente a edição 2027 e criar pistas na aba `NOVOS EXPOSITORES | REVISAO`; não promover automaticamente a lista oficial.
10. Registrar apenas contagens agregadas no GitHub Actions; todas as evidências e nomes permanecem no Sheets privado.

## Guardrails

- Não automatizar acesso, navegação, extração ou login no LinkedIn. Consultar URL apenas quando legitimamente disponível por fonte autorizada e corroborada.
- Respeitar robots.txt, termos, autorização, quotas, rate limit, 429, opt-out, LGPD e sigilo comercial.
- Usar identificadores corporativos e profissionais; não buscar telefone privado, dados sensíveis nem contatos genéricos como decisor.
- Não duplicar empresa+feira e não iniciar envio de e-mails/WhatsApp.
- Falha de autenticação, conflito de identidade ou evidência insuficiente bloqueia promoção automática.
- Alterar técnicas, regras ou limiares apenas com revisão e teste; o agente não muda as próprias proteções.

## Execução

O agendamento é GitHub Actions, não uma habilidade permanente do ChatGPT.
Workflow agendado: minuto 17 de cada hora, sujeito a atrasos do GitHub. Um disparo manual suporta `dry_run`. O estado durável reside no Google Sheets, não na máquina efêmera.

Ativar somente após configurar secrets e variável indicados no README, conceder acesso à planilha para a conta de serviço e validar manualmente `dry_run`.
