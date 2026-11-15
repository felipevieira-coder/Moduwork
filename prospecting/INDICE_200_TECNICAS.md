# MODU — Índice das 200 técnicas (referência)

Fonte canônica: `felipevieira-coder/modu/prospecting/PLAYBOOK_MODU_200_TECNICAS_SCRAPING_HQ_DECISION_INTELLIGENCE.md`.
Este índice é uma cópia **somente dos nomes** para facilitar consulta no Moduwork, sem registros pessoais.

**Status:** IDs **001–127** são o conjunto ativo padrão; **128–200** estão documentados mas são utilizados conforme a necessidade e revisão. A existência no catálogo **não significa que todos estejam implementados como código ou aplicados em cada pesquisa**.

**Restrições:** fontes permitidas, respeito a termos/robots, sem coleta automatizada não autorizada do LinkedIn, dois sinais independentes antes de promover decisores, prioridade a Eventos/Feiras/Brand Experience/Trade, um contato principal por empresa, consentimento e opt-out respeitados.

## 1–25 — Descoberta etica e coleta

- T001 — Checar robots.txt / REP
- T002 — Checar Termos de Uso
- T003 — Somente conteúdo público
- T004 — Hierarquia de autoridade da fonte
- T005 — Diretório oficial de expositores
- T006 — Sitemap do evento
- T007 — Catálogo/PDF oficial
- T008 — Lista oficial de patrocinadores
- T009 — Agenda e speakers
- T010 — Releases do organizador
- T011 — Newsroom do expositor
- T012 — Diretórios de associações
- T013 — Busca `site:domínio`
- T014 — Consultas evento+empresa+ano
- T015 — Structured data / JSON-LD
- T016 — Paginação explícita
- T017 — Canonicalização de URL
- T018 — Allowlist de domínios
- T019 — Orçamento de requisições por domínio
- T020 — Concorrência por domínio
- T021 — AutoThrottle
- T022 — Cache / conditional requests
- T023 — Retry com backoff
- T024 — User-Agent identificável
- T025 — Minimização e log de coleta

## 26–50 — Confirmacao de expositores e empresas

- T026 — Prova oficial de exposição
- T027 — Confirmar edição e ano
- T028 — Distinguir expositor/patrocinador/speaker
- T029 — Booth/stand/localização
- T030 — Marca x razão social
- T031 — Domínio oficial
- T032 — Registro/CNPJ quando público
- T033 — Cidade/UF da entidade
- T034 — Endereço corporativo
- T035 — Website corporativo oficial
- T036 — Landing page do expositor
- T037 — Release corporativo de participação
- T038 — Social corporativo como secundário
- T039 — Fabricante x distribuidor
- T040 — Grupo/subsidiária
- T041 — Redirect de domínio
- T042 — Título/logo/site consistency
- T043 — Domínio de e-mail corporativo
- T044 — Telefone/DDD como sinal fraco
- T045 — Segmento/taxonomia
- T046 — Histórico em múltiplas feiras
- T047 — Freshness da evidência
- T048 — Cancelamento/retirada
- T049 — Mudança de nome/aquisição
- T050 — ExhibitorConfidence

## 51–75 — Identificacao e validacao de decisores

- T051 — Taxonomia de cargos
- T052 — Prioridade por função MODU
- T053 — Senioridade
- T054 — Emprego atual
- T055 — Freshness do cargo
- T056 — Página oficial de equipe
- T057 — Bio de speaker
- T058 — Release com citação
- T059 — Agenda da edição
- T060 — Bio/autoria corporativa
- T061 — Perfil em associação
- T062 — Newsroom corporativo
- T063 — Resultados publicamente indexados
- T064 — Normalização de nome
- T065 — Acentos/diacríticos
- T066 — Desambiguação de homônimos
- T067 — Localização como sinal
- T068 — Timeline de carreira
- T069 — RoleFit
- T070 — Compras condicional
- T071 — Excluir SAC/genéricos
- T072 — Gerar múltiplos candidatos
- T073 — Triangulação de evidências
- T074 — Evidência negativa
- T075 — Limiar de revisão humana

## 76–100 — Entity resolution e deduplicacao

- T076 — Chave canônica da empresa
- T077 — IDs estáveis primeiro
- T078 — Normalizar domínio
- T079 — Aliases legal/comercial
- T080 — Blocking por domínio
- T081 — Blocking por registro
- T082 — Blocking cidade+nome
- T083 — Blocking por tokens normalizados
- T084 — Pessoa: sobrenome+empresa
- T085 — Pessoa: nome+domínio
- T086 — Sinal fonético
- T087 — Token-set similarity
- T088 — Edit distance
- T089 — Expansão de siglas
- T090 — Normalização de acentos
- T091 — Padronização de endereço
- T092 — Mudança de domínio
- T093 — Múltiplos domínios
- T094 — M&A e sucessão
- T095 — Mudança de emprego da pessoa
- T096 — Cluster, não só pares
- T097 — Probabilistic linkage
- T098 — Thresholds calibrados
- T099 — Undo/unmerge auditável
- T100 — Golden record + lineage

## 101–125 — Enriquecimento, atualidade e QA

- T101 — Enriquecer só após resolução
- T102 — Enviar múltiplos identificadores
- T103 — Provider match_confidence como sinal
- T104 — Bulk enrichment controlado
- T105 — Descoberta de padrão de e-mail
- T106 — Fonte pública do e-mail
- T107 — Validação sintática
- T108 — Checagem MX
- T109 — Verificação SMTP
- T110 — Accept-all/catch-all
- T111 — Unknown/blocked
- T112 — Invalid
- T113 — Disposable
- T114 — Webmail pessoal
- T115 — Data de verificação
- T116 — Reverificar antes de campanha
- T117 — Freshness do emprego
- T118 — Política de conflito de fontes
- T119 — Feedback de bounce
- T120 — Supressão de duplicados
- T121 — Opt-out / do-not-contact
- T122 — READY_GMASS gate
- T123 — QA por amostragem
- T124 — Métricas de precisão
- T125 — Feedback loop de aprendizado

## 126–140 — Inteligencia de oportunidade

- T126 — Calendário futuro de eventos da empresa
- T127 — Recorrência de exposição
- T128 — Porte aparente do stand
- T129 — Nível de patrocínio
- T130 — Lançamento de produto
- T131 — Entrada em novo mercado/região
- T132 — Rebranding / nova identidade
- T133 — Contratação de equipe de eventos/trade
- T134 — Renovação de fornecedor / fim de contrato
- T135 — Agency-of-record / agência parceira
- T136 — Créditos de campanha/produção
- T137 — Reverse case-study lookup
- T138 — Montadora oficial do evento
- T139 — Portal de fornecedores/homologação
- T140 — Inteligência de compras públicas

## 141–160 — Grafo de decisores

- T141 — Mapa de stakeholders
- T142 — Event Owner
- T143 — Brand Experience Owner
- T144 — Trade Marketing Owner
- T145 — Marketing Director fallback
- T146 — Procurement Category Owner
- T147 — Agência — produção/operações
- T148 — PME — fundador/diretor
- T149 — Regional vs HQ buyer
- T150 — Subsidiária vs grupo
- T151 — Budget-owner signal
- T152 — RFP/brief ownership
- T153 — Participação operacional no evento
- T154 — Aprovação/sign-off público
- T155 — Histórico de fornecedores
- T156 — Caminho de escalonamento
- T157 — Detecção de mudança de cargo
- T158 — Timestamp cross-source
- T159 — Top-3 candidate set
- T160 — Seleção 1-contato-por-empresa

## 161–175 — Provas de autoridade de compra

- T161 — Job description de responsabilidade
- T162 — Apresentação/palestra com escopo funcional
- T163 — Categoria em portal de fornecedores
- T164 — Autoria de edital/RFP/termo de referência público
- T165 — Citação em anúncio de parceria
- T166 — Gestor/fiscal de contrato público
- T167 — Comitê organizador interno
- T168 — Crédito em campanha experiencial
- T169 — Depoimento em case de fornecedor
- T170 — Project ownership signal
- T171 — Ownership de calendário de marca
- T172 — Responsabilidade por trade activation
- T173 — Field/Regional Marketing
- T174 — Negative authority signals
- T175 — Authority Evidence Diversity

## 176–188 — Contato e relacionamento

- T176 — Padrão de e-mail corporativo verificado
- T177 — Role mailbox flag
- T178 — WhatsApp profissional publicado
- T179 — Celular x PABX/switchboard
- T180 — Signature intelligence da própria caixa MODU
- T181 — Referral chaining
- T182 — Named handoff extraction
- T183 — Thread relationship graph
- T184 — Histórico de envio/supressão
- T185 — Last-touch recency
- T186 — Reply-intent classification
- T187 — Source-of-introduction
- T188 — Preferred-channel signal

## 189–200 — Priorizacao, aprendizado e governanca

- T189 — Evidence bundle
- T190 — Lead dossier
- T191 — Confidence decomposition
- T192 — TTL por fonte/atributo
- T193 — Event proximity score
- T194 — Opportunity value estimate
- T195 — Response propensity MODU
- T196 — Source precision tracking
- T197 — Error taxonomy
- T198 — Active-learning review queue
- T199 — Permitted monitoring
- T200 — Skill versioning & changelog
