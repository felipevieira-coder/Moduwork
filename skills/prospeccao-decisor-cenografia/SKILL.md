# SKILL — MODU Decision-Maker Intelligence para Cenografia & Live Marketing

Versão: 1.0 — 2026-10-04
Owner: MODU Cenografias

## Propósito

Encontrar **um único decisor principal por empresa** para contratação de cenografia, montagem de estandes, live marketing, ativações, produção e operação de eventos, usando somente fontes públicas/autorizadas e mantendo trilha de evidência.

## Entrada mínima

- Nome da empresa ou expositor
- Evento/feira/oportunidade, quando houver
- Edição/ano
- Fonte de descoberta

## Saída obrigatória

- `company_canonical_name`
- `company_entity_id`
- `official_domain`
- `event_name`
- `event_year`
- `exhibitor_confirmed`
- `opportunity_reason`
- `decision_maker_name`
- `original_title`
- `normalized_role`
- `seniority`
- `authority_class`
- `role_fit`
- `authority_evidence_score`
- `person_match`
- `current_employment`
- `freshness`
- `evidence_diversity`
- `negative_evidence`
- `decision_score`
- `decision_reason`
- `linkedin_or_professional_profile_url` apenas quando obtido por via permitida/manual/indexação pública
- `professional_email`
- `email_status`
- `email_verified_at`
- `professional_phone_or_whatsapp` apenas quando publicado profissionalmente, fornecido em assinatura/resposta própria ou fonte autorizada
- `source_urls`
- `verified_at`
- `record_status`

## Prioridade funcional MODU

1. Eventos / Feiras / Live Marketing / Experiential / Brand Experience
2. Trade Marketing / Field Marketing / Shopper Marketing
3. Marketing com evidência clara de responsabilidade por eventos
4. Procurement / Strategic Sourcing quando a categoria inclui marketing/eventos/serviços promocionais
5. Direção/fundador em PME sem estrutura especializada

Despriorizar: marketing genérico sem escopo de eventos, comunicação/PR sem produção, vendas, RH, financeiro, administrativo, SAC e caixas genéricas.

## Workflow obrigatório

### Etapa 1 — Confirmar oportunidade

1. Confirmar edição/ano do evento.
2. Confirmar exposição/patrocínio/participação em fonte oficial.
3. Capturar stand/localização/porte quando disponível.
4. Detectar cancelamento, mudança ou retirada.
5. Criar `ExhibitorConfidence`.

Falha crítica: sem evidência suficiente, manter `DISCOVERED` e não buscar contato em profundidade.

### Etapa 2 — Resolver empresa

1. Resolver domínio oficial.
2. Relacionar marca ↔ razão social ↔ CNPJ/registro quando público.
3. Mapear grupo, subsidiária, fabricante/distribuidor e unidade compradora.
4. Deduplicar contra `Expositores Feiras` e demais bases MODU.
5. Criar golden record com provenance.

Hard gate: `CompanyMatch >= 0.90`.

### Etapa 3 — Gerar candidatos

Buscar candidatos por múltiplas famílias de fonte:

- Página oficial da equipe
- Newsroom/releases
- Agenda/speakers
- Associações
- Cases de agência/fornecedor
- Job descriptions e vagas públicas
- Documentos públicos de contratação
- Mecanismos de busca e indexação pública
- Provedores B2B autorizados após company resolution
- Respostas e assinaturas da própria caixa MODU

Gerar Top-N; não escolher o primeiro resultado.

### Etapa 4 — Classificar stakeholder

Para cada candidato, atribuir uma classe:

- `BUDGET_OWNER`
- `DECISION_MAKER`
- `INFLUENCER`
- `EXECUTOR`
- `PROCUREMENT`
- `GATEKEEPER`
- `GENERIC/INVALID`

O objetivo é localizar `BUDGET_OWNER` ou `DECISION_MAKER`. `PROCUREMENT` pode ser top-1 apenas quando o escopo da categoria for diretamente relacionado a eventos/marketing/produção.

### Etapa 5 — Provar autoridade

Sinais fortes:

- Responsabilidade pública por budget
- Gestão de agências/fornecedores
- Planejamento anual de eventos/feiras
- Ownership de brand experience/trade activation
- Emissão/autoria de briefing/RFP/termo de referência público
- Liderança de evento/ativação atribuída em release/case
- Indicação direta recebida pela própria MODU (“fale com X”)
- Cargo de produção/operações/live em agência

Sinais fracos:

- Apenas senioridade
- Apenas localização
- Apenas aparição como speaker
- Apenas conexão com marketing
- Apenas perfil indexado

### Etapa 6 — Validar identidade e vínculo

Hard gates:

- `PersonMatch >= 0.90`
- `current_employment = confirmed`
- `RoleFit >= 0.80`
- sem homônimo não resolvido
- sem evidência negativa forte
- freshness dentro da política
- diversidade de evidência >= 2 famílias, salvo fonte primária excepcional

### Etapa 7 — Selecionar somente 1 decisor

Calcular `DecisionScore`:

- RoleFit: 30
- AuthorityEvidence: 25
- EventOwnership: 15
- Freshness: 10
- EvidenceDiversity: 10
- OpportunityContext: 10

Regras:

- >=80 e margem Top-1 vs Top-2 >=10: promover Top-1.
- 70–79 ou margem <10: `REVIEW_REQUIRED`.
- <70: manter secundário/rejeitar.

Desempate:

1. AuthorityEvidence
2. RoleFit
3. Recência
4. Diversidade de fontes
5. Proximidade com o evento específico
6. Persistindo empate: revisão humana

### Etapa 8 — Enriquecer contato

Somente após decisor resolvido:

1. Usar nome + domínio + empresa + IDs no provedor autorizado.
2. Preferir e-mail corporativo.
3. Inferir padrão de e-mail apenas quando demonstrado e sempre verificar.
4. Verificar sintaxe, MX e deliverability.
5. Tratar `ACCEPT_ALL`, `UNKNOWN`, `INVALID`, `DISPOSABLE` como estados distintos.
6. Não promover `UNKNOWN`, `INVALID` ou `DISPOSABLE` para envio automático.
7. Registrar data da verificação.

### Etapa 9 — Relationship Intelligence

Antes do envio, cruzar a própria operação MODU:

- Gmail enviados
- respostas recebidas
- encaminhamentos
- assinaturas profissionais
- “fale com X”
- último contato
- opt-out
- bounce
- duplicidade

Indicação direta e resposta positiva têm prioridade sobre cold discovery.

### Etapa 10 — READY_GMASS

Promover somente se:

- empresa e evento confirmados
- decisor validado
- contato profissional adequado
- sem supressão/opt-out
- e-mail válido e recente
- não enviado indevidamente em período incompatível
- evidências registradas

## Query recipes

### Cliente final

- `site:<dominio> eventos marketing`
- `site:<dominio> "trade marketing"`
- `site:<dominio> "brand experience"`
- `site:<dominio> feira OR congresso OR expo`
- `"<empresa>" "gerente de eventos"`
- `"<empresa>" "trade marketing" evento`
- `"<empresa>" "gestão de fornecedores" marketing`
- `"<empresa>" estande feira <ano>`
- `"<empresa>" stand feira <ano>`
- `"<empresa>" "live marketing"`
- `"<empresa>" "Head of Events"`

### Agência

- `"<agencia>" produção eventos`
- `"<agencia>" operações live marketing`
- `"<agencia>" experiential producer`
- `"<agencia>" case "<cliente>" evento`
- `"<agencia>" cenografia`
- `"<agencia>" montadora estande`

## Fontes de alta utilidade para a MODU

### Eventos e feiras
- diretório oficial
- mapa/planta
- manual do expositor
- catálogo/PDF
- agenda/speakers
- releases

### Empresa
- newsroom
- página de liderança/equipe
- cases
- vagas públicas
- portal de fornecedores
- políticas de compras

### Compra pública
- PNCP
- Compras.gov
- PCA
- editais/avisos
- atas de registro de preços
- contratos

### Primeira parte MODU
- Gmail
- Google Sheets
- CRM/histórico de prospecção
- respostas, encaminhamentos e assinaturas

## Proibições operacionais

- não contornar CAPTCHA/login/paywall
- não burlar rate limits
- não usar proxies/UA para mascarar violação de termos
- não automatizar scraping direto de LinkedIn sem autorização expressa
- não coletar dados pessoais sem necessidade operacional
- não coletar dados sensíveis
- não usar número privado descoberto fora de contexto profissional
- não disparar para contato genérico quando decisor nominal validado existe
- não compensar hard gate com score agregado
- não fazer merge irreversível

## Critério de qualidade

A skill é considerada bem-sucedida quando consegue responder, com fontes e datas:

> “Por que esta empresa é oportunidade agora, por que esta pessoa é o melhor decisor para cenografia/live marketing e quais evidências sustentam essa escolha?”

Sem essa resposta, o registro não deve ser promovido automaticamente.