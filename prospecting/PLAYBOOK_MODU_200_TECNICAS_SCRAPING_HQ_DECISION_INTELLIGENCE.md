# MODU — Playbook 200 Técnicas de Scraping HQ & Decision Intelligence

Versão: 1.0 — 2026-10-04
Escopo: prospecção B2B para cenografia, montadoras, live marketing, brand experience, trade marketing, feiras e ativações.
Origem canônica: planilha Google Sheets `MODU — 125 Técnicas de Scraping Ético — Master` + expansão de 75 técnicas orientadas à identificação do verdadeiro decisor.

## Objetivo

Transformar pesquisa pública e enriquecimento autorizado em um sistema de alta precisão para responder quatro perguntas:

1. A empresa realmente participa ou investe em eventos/feiras/ativações?
2. Qual unidade/empresa do grupo efetivamente compra?
3. Quem de fato possui autoridade, influência ou responsabilidade operacional sobre a contratação?
4. Existe um canal profissional válido, atual e adequado para contato?

A prioridade é **precision over volume**. Um falso decisor é mais caro do que um registro ainda não resolvido.

## Regras não negociáveis

- Apenas conteúdo público, autorizado ou proveniente de contas/arquivos da própria MODU.
- Respeitar robots.txt/REP, Termos de Uso, rate limits, 429, paywalls, autenticação e controles de acesso.
- Não contornar CAPTCHA, login, bloqueios técnicos ou limites de plataforma.
- Não fazer scraping automatizado não autorizado de LinkedIn. Usar fontes primárias, indexação pública, pesquisa manual e/ou provedores autorizados.
- Coletar somente dados profissionais necessários à finalidade comercial.
- Não inferir nem armazenar dados sensíveis.
- Registrar URL/fonte, data, evidência e motivo da decisão.
- Respeitar opt-out, do-not-contact, histórico de envio e supressão.
- Regra MODU: **1 decisor principal por empresa**, preservando candidatos secundários somente para auditoria/revisão.

## Modelo operacional

Estado do registro:

`DISCOVERED → EXHIBITOR_CONFIRMED → COMPANY_RESOLVED → CANDIDATES_FOUND → DECISOR_VALIDATED → ENRICHED → EMAIL_VERIFIED → READY_GMASS`

Estados de exceção: `REVIEW_REQUIRED`, `STALE`, `REJECTED`.

---

# CAMADA 1 — DESCOBERTA ÉTICA & COLETA (1–25)

| ID | Técnica | Aplicação MODU | Evidência / Gate |
|---:|---|---|---|
|1|Checar robots.txt / REP|Antes de qualquer crawler, registrar o que o domínio permite ou restringe.|Hard gate; bloqueio explícito = não coletar por crawler.|
|2|Checar Termos de Uso|Verificar restrições contratuais, licenças e usos permitidos.|Hard gate; proibição explícita = fonte alternativa/autorizada.|
|3|Somente conteúdo público|Limitar coleta a páginas acessíveis sem login/paywall.|Hard gate; nunca contornar autenticação/CAPTCHA.|
|4|Hierarquia de autoridade da fonte|Priorizar evento/empresa oficial sobre agregadores.|Fonte secundária isolada não fecha decisão.|
|5|Diretório oficial de expositores|Fonte primária para confirmar participação na edição.|Hard gate para `EXHIBITOR_CONFIRMED`.|
|6|Sitemap do evento|Descobrir páginas de expositores/evento com baixo ruído.|Validar se a página ainda pertence à edição atual.|
|7|Catálogo/PDF oficial|Recuperar expositores quando não há HTML estruturado.|Ano/edição precisam estar explícitos.|
|8|Lista oficial de patrocinadores|Gerar candidatos e classificar tipo de presença.|Patrocinador não é automaticamente expositor.|
|9|Agenda e speakers|Descobrir pessoas, empresas e contexto funcional.|Speaker ajuda a validar identidade, não autoridade de compra.|
|10|Releases do organizador|Confirmar participantes, parceiros, alterações e cancelamentos.|Release deve ser datado e da edição correta.|
|11|Newsroom do expositor|Confirmar participação pela própria empresa.|Forte triangulação com fonte do evento.|
|12|Diretórios de associações|Resolver identidade corporativa e setor.|Diretório antigo exige revalidação.|
|13|Busca `site:domínio`|Localizar páginas específicas sem crawling amplo.|Snippet é pista; página acessível é evidência.|
|14|Consultas evento+empresa+ano|Encontrar confirmação cruzada de alta precisão.|Correspondência temporal obrigatória.|
|15|Structured data / JSON-LD|Extrair organização, pessoa, evento e URLs de marcação pública.|Schema incoerente vai para review.|
|16|Paginação explícita|Cobrir todas as páginas de diretórios sem loop.|Registrar número de páginas e última página processada.|
|17|Canonicalização de URL|Evitar duplicidade por parâmetros, UTM e aliases.|Preservar URL original + URL canônica.|
|18|Allowlist de domínios|Restringir automação a fontes previamente aprovadas.|Hard gate; não seguir domínio externo automaticamente.|
|19|Orçamento de requisições por domínio|Impor limite total de chamadas e janela de coleta.|Hard gate; excedeu, pausa.|
|20|Concorrência por domínio|Evitar rajadas e sobrecarga.|Hard gate; concorrência conservadora.|
|21|AutoThrottle|Adaptar velocidade à latência e saúde do servidor.|Aumento de latência/erro = desacelerar.|
|22|Cache / conditional requests|Evitar baixar conteúdo inalterado.|Usar ETag/Last-Modified quando disponível.|
|23|Retry com backoff|Tratar 429/5xx sem martelar servidor.|Hard gate; 429 repetido = parar/adiar.|
|24|User-Agent identificável|Evitar mascaramento da identidade do crawler.|UA enganoso é reprovado.|
|25|Minimização e log de coleta|Coletar apenas campos necessários e manter provenance.|Hard gate; fonte + timestamp por registro.|

# CAMADA 2 — CONFIRMAÇÃO DO EXPOSITOR & EMPRESA (26–50)

| ID | Técnica | Aplicação MODU | Evidência / Gate |
|---:|---|---|---|
|26|Prova oficial de exposição|Confirmar que a empresa realmente expõe na edição.|Hard gate; sem prova = `DISCOVERED`.|
|27|Confirmar edição e ano|Evitar reaproveitar presença antiga.|Hard gate; ano divergente = rejeitar.|
|28|Distinguir expositor/patrocinador/speaker|Classificar corretamente o relacionamento.|Hard gate para status de expositor.|
|29|Booth/stand/localização|Reforçar presença física e estimar porte.|Número/localização é evidência de alta utilidade.|
|30|Marca x razão social|Relacionar brand ao ente jurídico certo.|Ambiguidade = review.|
|31|Domínio oficial|Resolver o site corporativo correto.|Hard gate antes de enriquecer pessoa.|
|32|Registro/CNPJ quando público|Usar identificador estável para desambiguação.|CNPJ conflitante é forte evidência negativa.|
|33|Cidade/UF da entidade|Distinguir homônimos, matriz e filiais.|Sinal auxiliar, não único.|
|34|Endereço corporativo|Reforçar entity resolution.|Endereço desatualizado tem peso menor.|
|35|Website corporativo oficial|Definir fonte raiz da empresa.|Hard gate; agregador não substitui fonte oficial.|
|36|Landing page do expositor|Extrair descrição, stand, categoria e URLs do evento.|Validar edição.|
|37|Release corporativo de participação|Triangular presença com fonte independente.|Data obrigatória.|
|38|Social corporativo como secundário|Adicionar recência e contexto.|Nunca usar post isolado como confirmação única.|
|39|Fabricante x distribuidor|Saber quem expõe e quem compra.|Mapear ambos sem presumir mesma autoridade.|
|40|Grupo/subsidiária|Evitar abordar holding errada.|Grupo ≠ unidade compradora.|
|41|Redirect de domínio|Detectar rebranding/aquisição.|Redirect persistente e coerente.|
|42|Título/logo/site consistency|Comparar marca visual e texto institucional.|Sinal fraco, útil em conjunto.|
|43|Domínio de e-mail corporativo|Reforçar identidade empresa-contato.|Domínio divergente = review.|
|44|Telefone/DDD como sinal fraco|Ajudar desambiguação geográfica.|Nunca usar isoladamente.|
|45|Segmento/taxonomia|Confirmar fit comercial e resolver homônimos.|Segmento incompatível = review.|
|46|Histórico em múltiplas feiras|Identificar expositor recorrente e maturidade de eventos.|Não substitui confirmação da edição atual.|
|47|Freshness da evidência|Medir atualidade de cada confirmação.|Hard gate por atributo.|
|48|Cancelamento/retirada|Detectar saída de expositor ou mudança do evento.|Hard gate; fonte mais recente prevalece.|
|49|Mudança de nome/aquisição|Atualizar entidade canônica sem perder lineage.|Não fundir por semelhança sem prova.|
|50|ExhibitorConfidence|Consolidar sinais de participação.|Hard gate; baseline auto-pass >=0,90.|

# CAMADA 3 — IDENTIFICAÇÃO & VALIDAÇÃO DO DECISOR (51–75)

| ID | Técnica | Aplicação MODU | Evidência / Gate |
|---:|---|---|---|
|51|Taxonomia de cargos|Normalizar títulos equivalentes em áreas comparáveis.|Manter título original e normalizado.|
|52|Prioridade por função MODU|Eventos/Feiras/Brand Experience > Trade > Marketing > Compras relevante.|Hard gate de aderência funcional.|
|53|Senioridade|Separar executor, influenciador e decisor.|Júnior isolado vira candidato secundário.|
|54|Emprego atual|Confirmar vínculo atual pessoa-empresa.|Hard gate; sem vínculo atual = stale/review.|
|55|Freshness do cargo|Evitar cargo antigo.|Hard gate; data recente exigida.|
|56|Página oficial de equipe|Validar nome e função institucionalmente.|Fonte primária forte.|
|57|Bio de speaker|Confirmar empresa/cargo por fonte do evento.|Secundária se antiga.|
|58|Release com citação|Validar liderança e escopo funcional.|Data + cargo obrigatórios.|
|59|Agenda da edição|Detectar profissionais envolvidos em evento/tema.|Envolvimento não prova autoridade de compra.|
|60|Bio/autoria corporativa|Extrair contexto e função de autores internos.|Recência importa.|
|61|Perfil em associação|Validar liderança setorial.|Mandato expirado = stale.|
|62|Newsroom corporativo|Capturar nomeações, promoções e mudanças.|Forte para current employment.|
|63|Resultados publicamente indexados|Gerar candidatos sem automatizar plataforma restrita.|Snippet não valida sozinho.|
|64|Normalização de nome|Unificar abreviações e ordem de nomes.|Preservar variante original.|
|65|Acentos/diacríticos|Melhorar matching de nomes brasileiros.|Apenas feature, nunca prova.|
|66|Desambiguação de homônimos|Evitar pessoa errada com mesmo nome.|Hard gate; empresa+cargo+outro sinal.|
|67|Localização como sinal|Ajudar a distinguir candidatos.|Nunca decide sozinha.|
|68|Timeline de carreira|Detectar sobreposição, saída ou emprego anterior.|Conflito temporal = review.|
|69|RoleFit|Pontuar aderência à compra de eventos/cenografia.|Hard gate; baseline auto-pass >=0,80.|
|70|Compras condicional|Usar procurement só quando escopo inclui eventos/marketing.|Compras genéricas = baixa prioridade.|
|71|Excluir SAC/genéricos|Bloquear info@, contato@, suporte e atendimento como decisor.|Hard gate.|
|72|Gerar múltiplos candidatos|Evitar escolher o primeiro resultado.|Preservar top-N para comparação.|
|73|Triangulação de evidências|Exigir sinais independentes de identidade/função.|Hard gate; ideal >=2 famílias.|
|74|Evidência negativa|Registrar saída, cargo incompatível, cancelamento etc.|Hard gate; negativo forte vence positivo fraco.|
|75|Limiar de revisão humana|Não forçar decisão automática em zona cinzenta.|Hard gate; ambiguidade = `REVIEW_REQUIRED`.|

# CAMADA 4 — ENTITY RESOLUTION & DEDUPLICAÇÃO (76–100)

| ID | Técnica | Aplicação MODU | Evidência / Gate |
|---:|---|---|---|
|76|Chave canônica da empresa|Criar ID interno persistente.|Hard gate para consolidar histórico.|
|77|IDs estáveis primeiro|CNPJ/registro/domínio antes de fuzzy text.|Hard gate; conflito = review.|
|78|Normalizar domínio|Remover protocolo/www/path e tratar aliases.|Preservar original.|
|79|Aliases legal/comercial|Guardar razão social, marca e abreviações.|Alias provável não é alias confirmado.|
|80|Blocking por domínio|Gerar candidatos em blocos plausíveis.|Serve para geração, não decisão final.|
|81|Blocking por registro|Reduzir universo via identificador estável.|Cuidado com jurisdição.|
|82|Blocking cidade+nome|Recuperar empresa sem domínio conhecido.|Nomes comuns exigem mais sinais.|
|83|Blocking por tokens normalizados|Capturar variações ortográficas.|Termos genéricos recebem peso baixo.|
|84|Pessoa: sobrenome+empresa|Gerar candidatos com contexto.|Homônimo requer sinais adicionais.|
|85|Pessoa: nome+domínio|Gerar candidato de alta precisão.|Ainda exige validação.|
|86|Sinal fonético|Capturar grafias próximas.|Nunca decidir por fonética.|
|87|Token-set similarity|Comparar nomes com ordem/ruído diferentes.|Feature auxiliar.|
|88|Edit distance|Detectar typos simples.|Distância pequena sem contexto é insuficiente.|
|89|Expansão de siglas|Relacionar sigla a nome completo.|Exigir vínculo explícito.|
|90|Normalização de acentos|Reduzir falhas de matching.|Nunca usar isoladamente.|
|91|Padronização de endereço|Comparar logradouro/número/cidade.|Mudança pode ser legítima.|
|92|Mudança de domínio|Tratar migração/rebranding.|Exigir prova corporativa.|
|93|Múltiplos domínios|Mapear país/produto/domínio principal.|Branding parecido não basta.|
|94|M&A e sucessão|Manter linhagem pós-fusão/aquisição.|Preservar histórico pré-evento societário.|
|95|Mudança de emprego da pessoa|Evitar anexar contato a empresa antiga.|Hard gate.|
|96|Cluster, não só pares|Resolver grupos de registros de forma consistente.|Inconsistência transitiva = review.|
|97|Probabilistic linkage|Combinar sinais com pesos discriminantes.|Não substitui hard gates.|
|98|Thresholds calibrados|Separar auto-match, review e non-match.|Hard gate; calibrar por QA real.|
|99|Undo/unmerge auditável|Permitir desfazer falso merge.|Hard gate de governança.|
|100|Golden record + lineage|Manter melhor valor por campo e todas as origens.|Hard gate; valor sem provenance não é promovido.|

# CAMADA 5 — ENRIQUECIMENTO, FRESHNESS & QA (101–125)

| ID | Técnica | Aplicação MODU | Evidência / Gate |
|---:|---|---|---|
|101|Enriquecer só após resolução|Evitar crédito gasto e contato anexado à pessoa errada.|Hard gate.|
|102|Enviar múltiplos identificadores|Nome+empresa+domínio/ID aumenta match do provedor.|Nome sozinho = baixa confiança.|
|103|Provider match_confidence como sinal|Usar confiança do Apollo/provedor como feature.|Nunca terceirizar decisão ao provedor.|
|104|Bulk enrichment controlado|Preservar correlação entrada-saída por ID.|Resposta sem chave = review.|
|105|Descoberta de padrão de e-mail|Gerar candidato de e-mail por padrão corporativo.|Inferência exige verificação.|
|106|Fonte pública do e-mail|Guardar URL/data quando e-mail profissional é publicado.|Sem origem = `provider-only`.|
|107|Validação sintática|Bloquear e-mail malformado.|Hard gate.|
|108|Checagem MX|Confirmar que domínio recebe e-mail.|Hard gate; sem MX = não enviar.|
|109|Verificação SMTP|Testar deliverability com verificador permitido.|Blocked = UNKNOWN, não VALID.|
|110|Accept-all/catch-all|Tratar domínio catch-all como incerto.|Hard gate; não equiparar a valid.|
|111|Unknown/blocked|Separar falta de verificação de validade.|Hard gate; não envio automático.|
|112|Invalid|Bloquear endereço inválido.|Hard gate; nunca `READY_GMASS`.|
|113|Disposable|Excluir e-mails temporários.|Hard gate.|
|114|Webmail pessoal|Preferir e-mail corporativo.|Pessoal só quando adequado/autorizado.|
|115|Data de verificação|Registrar timestamp de deliverability.|Hard gate de freshness.|
|116|Reverificar antes de campanha|Atualizar listas antigas.|Hard gate para lotes antigos/grandes.|
|117|Freshness do emprego|Validar vínculo antes do envio.|Hard gate.|
|118|Política de conflito de fontes|Resolver divergência por autoridade+recência.|Hard gate; conflito forte = review.|
|119|Feedback de bounce|Hard bounce degrada e bloqueia o endereço.|Hard gate.|
|120|Supressão de duplicados|Evitar múltiplos envios à mesma pessoa/empresa.|Hard gate conforme regra MODU.|
|121|Opt-out / do-not-contact|Respeitar oposição e descadastro.|Hard gate absoluto.|
|122|READY_GMASS gate|Liberar apenas registro aprovado em todos os gates críticos.|Hard gate final.|
|123|QA por amostragem|Auditar manualmente lotes e medir precisão.|Erro acima do limite bloqueia lote.|
|124|Métricas de precisão|Medir falso positivo, falso merge, bounce e stale.|Recalibrar fonte/técnica.|
|125|Feedback loop de aprendizado|Atualizar regras com erros e sucessos observados.|Toda mudança deve ser versionada e datada.|

---

# EXPANSÃO MODU — DECISION INTELLIGENCE & PROSPECÇÃO PROFUNDA (126–200)

Estas técnicas não substituem as 125. Elas entram **depois da confirmação da empresa** e servem para responder: *quem realmente compra cenografia/live marketing e por quê?*

## CAMADA 6 — Opportunity Intelligence (126–140)

| ID | Técnica | Como usar | Sinal de alta qualidade |
|---:|---|---|---|
|126|Calendário futuro de eventos da empresa|Mapear feiras, congressos, lançamentos e ativações anunciadas para 3–12 meses.|Evento futuro confirmado + empresa participante.|
|127|Recorrência de exposição|Contar participações em 2+ edições/eventos distintos.|Recorrência mostra budget e processo de contratação repetitivo.|
|128|Porte aparente do stand|Usar planta/mapa/stand number/categoria para estimar complexidade e valor potencial.|Ilha, múltiplas frentes, área grande, mezanino ou ativações.|
|129|Nível de patrocínio|Patrocínio premium/diamond/master sugere budget de experiência superior.|Categoria oficial + presença física.|
|130|Lançamento de produto|Cruzar release de lançamento com feira/evento próximo.|Produto novo + evento = probabilidade alta de investimento em experiência.|
|131|Entrada em novo mercado/região|Detectar expansão comercial, nova filial ou operação nacional.|Expansão costuma exigir feiras, eventos e brand activation.|
|132|Rebranding / nova identidade|Identificar troca de marca, embalagem ou posicionamento.|Rebrand recente aumenta demanda por cenografia e PDV/eventos.|
|133|Contratação de equipe de eventos/trade|Vagas públicas de eventos, field marketing ou trade indicam crescimento operacional.|Vaga recente com gestão de fornecedores/budget.|
|134|Renovação de fornecedor / fim de contrato|Em fontes públicas, identificar contrato/ata próximo do vencimento.|Janela de recontratação documentada.|
|135|Agency-of-record / agência parceira|Mapear agência responsável por campanhas/eventos quando pública.|Permite prospectar agência e cliente final sem duplicar contato.|
|136|Créditos de campanha/produção|Ler cases, premiações e releases que citam agência, produtora e fornecedores.|Crédito explícito liga ecossistema de compra.|
|137|Reverse case-study lookup|Partir de um case de montadora/agência e recuperar marca, evento e decisores envolvidos.|Case datado + nomes/funções.|
|138|Montadora oficial do evento|Separar expositor que é obrigado a usar fornecedor oficial de áreas em que pode contratar livremente.|Manual do expositor/regulamento.|
|139|Portal de fornecedores/homologação|Descobrir cadastro, requisitos e janela de homologação da empresa.|Portal oficial + categoria relevante.|
|140|Inteligência de compras públicas|Usar PNCP/Compras.gov para editais, PCA, contratos, atas e histórico de fornecedores em eventos/stands.|Objeto, órgão, fornecedor, valor, vigência e datas oficiais.|

## CAMADA 7 — Decision-Maker Graph (141–160)

| ID | Técnica | Como usar | Regra de decisão |
|---:|---|---|---|
|141|Mapa de stakeholders|Classificar candidatos em Budget Owner, Decision Maker, Influencer, Executor, Procurement e Gatekeeper.|Nunca tratar todos como “decisor”.|
|142|Event Owner|Priorizar quem responde pelo calendário/execução de eventos.|RoleFit máximo quando função é atual e específica.|
|143|Brand Experience Owner|Priorizar liderança de experiência de marca/experiential.|Excelente fit para ativações e cenografia.|
|144|Trade Marketing Owner|Priorizar trade quando evento/feira é canal de sell-in/sell-out.|Alta prioridade MODU.|
|145|Marketing Director fallback|Usar diretor/gerente de marketing quando não há área dedicada.|Precisa de evidência de eventos no escopo.|
|146|Procurement Category Owner|Usar compras quando categoria inclui marketing, eventos, serviços promocionais ou produção.|Compras genéricas não recebe prioridade.|
|147|Agência — produção/operações|Em agências, priorizar Head/Director/Manager de Produção, Operações, Eventos, Live/Experiential.|Frequentemente escolhe/indica montadora.|
|148|PME — fundador/diretor|Em empresas menores sem estrutura de eventos, owner/diretor pode ser comprador real.|Usar somente quando organograma/porte sustenta.|
|149|Regional vs HQ buyer|Determinar se decisão é local, nacional ou LATAM/global.|Prospectar unidade que controla o evento brasileiro.|
|150|Subsidiária vs grupo|Identificar qual CNPJ/unidade possui budget e contrato.|Não subir para holding sem necessidade.|
|151|Budget-owner signal|Buscar descrição pública de responsabilidade por orçamento, fornecedores ou planejamento anual.|Sinal forte de autoridade.|
|152|RFP/brief ownership|Em documentos públicos, identificar área/autoria que emite briefing ou contratação.|Sinal direto de processo de compra.|
|153|Participação operacional no evento|Pessoa aparece organizando booth, ativação, lançamento ou agenda corporativa.|Aumenta RoleFit, mas não prova budget sozinho.|
|154|Aprovação/sign-off público|Em compras públicas ou documentos autorizados, mapear responsável por aprovação/fiscalização/gestão.|Sinal forte, respeitando escopo público.|
|155|Histórico de fornecedores|Mapear fornecedores anteriores da empresa/evento em cases, editais ou créditos.|Ajuda entender cadeia decisória e maturidade.|
|156|Caminho de escalonamento|Definir quem é contato principal e quem seria fallback caso o primeiro não responda.|Não enviar em paralelo automaticamente.|
|157|Detecção de mudança de cargo|Comparar fontes recentes e antigas antes de promover o contato.|Saída recente derruba `current_employment`.|
|158|Timestamp cross-source|Exigir datas compatíveis entre cargo, empresa e evento.|Contradição temporal = review.|
|159|Top-3 candidate set|Manter até 3 candidatos com scores e evidências para auditoria.|Somente top-1 é exportado quando margem for clara.|
|160|Seleção 1-contato-por-empresa|Aplicar regra final MODU com desempate por autoridade, fit, recência e evidência.|Top-1 validado; demais ficam como backup interno.|

## CAMADA 8 — Provas de Autoridade de Compra (161–175)

| ID | Técnica | Como usar | Força |
|---:|---|---|---|
|161|Job description de responsabilidade|Vaga/bio que cita budget, vendor management, agencies, events ou activations.|Alta quando atual e da própria empresa.|
|162|Apresentação/palestra com escopo funcional|Slides/bio pública descreve responsabilidade por eventos/trade/brand experience.|Média-alta.|
|163|Categoria em portal de fornecedores|Identificar área/categoria responsável por marketing/eventos.|Alta para procurement fit.|
|164|Autoria de edital/RFP/termo de referência público|Extrair unidade requisitante, gestor ou responsável técnico.|Alta em órgãos/entidades públicas.|
|165|Citação em anúncio de parceria|Quote do executivo sobre evento, experiência de marca ou agência.|Média-alta.|
|166|Gestor/fiscal de contrato público|Quando legalmente publicado, usar como evidência de responsabilidade operacional — não como contato automático.|Alta para conhecimento do processo.|
|167|Comitê organizador interno|Identificar representantes oficiais em comitês/conselhos de evento.|Média-alta.|
|168|Crédito em campanha experiencial|Pessoa citada como marketing/event lead em case/premiação.|Alta se cargo atual confirmado.|
|169|Depoimento em case de fornecedor|Quote do cliente em case de agência/montadora revela sponsor interno.|Alta, mas checar atualidade.|
|170|Project ownership signal|Post/release corporativo atribui liderança de ativação/evento à pessoa.|Média-alta.|
|171|Ownership de calendário de marca|Descrição de função inclui planejamento anual de feiras/eventos.|Alta.|
|172|Responsabilidade por trade activation|Cargo/escopo inclui ativações, canais, lançamentos, materiais e eventos.|Alta.|
|173|Field/Regional Marketing|Para roadshows/eventos regionais, identificar quem controla budget local.|Média-alta.|
|174|Negative authority signals|Excluir assessor, estagiário, social-only, RH, SAC, financeiro genérico, vendas sem escopo de eventos.|Hard negative para RoleFit.|
|175|Authority Evidence Diversity|Para `DECISOR_VALIDATED`, exigir ao menos duas evidências independentes de função/autoridade ou uma primária muito forte + vínculo atual.|Hard gate recomendado.|

## CAMADA 9 — Contact & Relationship Intelligence (176–188)

| ID | Técnica | Como usar | Regra |
|---:|---|---|---|
|176|Padrão de e-mail corporativo verificado|Inferir apenas após resolver pessoa+domínio e confirmar padrão real.|Sempre verificar antes de envio.|
|177|Role mailbox flag|Marcar marketing@, eventos@, compras@ etc. como caixa funcional.|Nunca substituir decisor nominal quando ele existir.|
|178|WhatsApp profissional publicado|Usar apenas número publicado para finalidade profissional, fornecido em assinatura/contato da própria relação ou fonte autorizada.|Não buscar/expor número privado.|
|179|Celular x PABX/switchboard|Classificar telefone para não tratar central como contato pessoal.|Sinal de qualidade de canal.|
|180|Signature intelligence da própria caixa MODU|Extrair de respostas recebidas nome, cargo, e-mail, telefone/WhatsApp profissional e empresa.|Fonte de primeira parte; registrar thread/data.|
|181|Referral chaining|Quando alguém responde “fale com X”, promover X como candidato e validar identidade/cargo.|Indicação é evidência forte, não dispensa current employment.|
|182|Named handoff extraction|Extrair nome/e-mail explicitamente encaminhado por contato real.|Alta prioridade de prospecção.|
|183|Thread relationship graph|Mapear quem encaminhou para quem e qual área assumiu a conversa.|Revela cadeia real de decisão.|
|184|Histórico de envio/supressão|Cruzar Gmail/CRM para não repetir contato já acionado sem motivo.|Hard gate de operação.|
|185|Last-touch recency|Registrar último envio, resposta e próximo passo.|Evita spam e permite follow-up contextual.|
|186|Reply-intent classification|Classificar resposta: positivo, pedir portfólio, encaminhou, timing futuro, não interessado, opt-out.|Alimenta prioridade e aprendizado.|
|187|Source-of-introduction|Distinguir descoberta fria, indicação, resposta, evento, cliente/parceiro.|Indicação real recebe peso superior.|
|188|Preferred-channel signal|Se o próprio contato indicar canal preferido, registrar e respeitar.|Não migrar para canal invasivo sem contexto.|

## CAMADA 10 — Scoring, Learning & Automation (189–200)

| ID | Técnica | Como usar | Resultado |
|---:|---|---|---|
|189|Evidence bundle|Cada lead precisa de pacote com URLs, datas, snippets e motivo da decisão.|Auditoria reproduzível.|
|190|Lead dossier|Resumo de 5 linhas: empresa, evento, oportunidade, decisor, por que ele é o correto.|Pronto para abordagem contextual.|
|191|Confidence decomposition|Separar CompanyMatch, PersonMatch, RoleFit, Authority, Freshness e ContactQuality.|Evita score opaco.|
|192|TTL por fonte/atributo|Evento, cargo, e-mail e CNPJ envelhecem em ritmos diferentes.|Revalidação seletiva.|
|193|Event proximity score|Aumentar prioridade conforme evento confirmado se aproxima, sem sacrificar validação.|Radar comercial.|
|194|Opportunity value estimate|Estimar valor potencial por área/porte do stand, recorrência, patrocínio e complexidade.|Ranking comercial, não orçamento final.|
|195|Response propensity MODU|Usar histórico próprio para aprender quais cargos/segmentos respondem melhor.|Somente dados internos e agregados.|
|196|Source precision tracking|Medir taxa de acerto por fonte: diretório, release, provider, indicação etc.|Cortar fontes de baixa precisão.|
|197|Error taxonomy|Classificar erros: empresa errada, cargo stale, homônimo, e-mail inválido, contato genérico, evento antigo.|Facilita correção sistêmica.|
|198|Active-learning review queue|Revisar primeiro casos de alta oportunidade e alta incerteza.|Melhora o modelo mais rápido.|
|199|Permitted monitoring|Monitorar mudanças em páginas oficiais, eventos, releases, vagas e fontes públicas permitidas.|Sem bypass/automação proibida.|
|200|Skill versioning & changelog|Toda alteração de regra, peso ou gate vira versão com data, motivo e impacto.|Aprendizado contínuo auditável.|

---

# Modelo de scoring MODU — Decisor v1

## Hard gates

Um contato não pode ser promovido para `DECISOR_VALIDATED` se qualquer um falhar:

- CompanyMatch >= 0,90
- Current employment confirmado
- PersonMatch >= 0,90 (review 0,80–0,89)
- RoleFit >= 0,80
- EvidenceDiversity >= 2 famílias, salvo evidência primária excepcional
- Nenhuma evidência negativa forte
- Não é canal genérico
- Freshness >= 0,85 para atributos críticos

## DecisionScore 0–100

- RoleFit: 0–30
- AuthorityEvidence: 0–25
- Event/Activation Ownership: 0–15
- Freshness: 0–10
- Evidence Diversity: 0–10
- Opportunity Context: 0–10

Critério recomendado:

- `>= 80` e diferença Top-1 vs Top-2 >= 10 pontos: promover Top-1.
- `70–79` ou margem < 10: `REVIEW_REQUIRED`.
- `< 70`: candidato secundário/rejeitado para decisão.

### RoleFit sugerido

1. Eventos / Live Marketing / Experiential / Brand Experience: 1,00
2. Trade Marketing / Field Marketing / Shopper: 0,90
3. Marketing com responsabilidade por eventos: 0,85
4. Procurement/Strategic Sourcing de marketing/eventos: 0,80
5. Marketing genérico sem evidência de eventos: 0,65
6. Comunicação/PR sem produção/eventos: 0,55
7. Vendas/RH/Financeiro/Admin/SAC sem escopo: <0,40

## Desempate para a regra “1 contato por empresa”

1. Maior AuthorityEvidence.
2. Maior RoleFit.
3. Maior recência.
4. Maior diversidade de fontes.
5. Maior proximidade com o evento específico.
6. Se persistir empate: revisão humana; não escolher automaticamente.

---

# Query Bank — descoberta permitida de decisores

Usar em mecanismos de busca e fontes públicas, sem automatizar plataformas restritas:

- `site:empresa.com eventos marketing`
- `site:empresa.com "trade marketing"`
- `site:empresa.com "brand experience"`
- `site:empresa.com feira OR congresso OR expo`
- `site:empresa.com fornecedores marketing eventos`
- `site:empresa.com newsroom feira <ano>`
- `"Empresa" "gerente de eventos"`
- `"Empresa" "trade marketing" evento`
- `"Empresa" "brand experience"`
- `"Empresa" "gestão de fornecedores" marketing`
- `"Empresa" "agência" ativação`
- `"Empresa" "stand" feira <ano>`
- `"Empresa" "estande" feira <ano>`
- `"Empresa" "live marketing"`
- `"Empresa" "experiential"`
- `"Empresa" "RFP" eventos`
- `"Empresa" "fornecedores" "eventos"`
- `"Empresa" "Head of Events"`
- `"Empresa" "Marketing Manager" "events"`
- `"Empresa" "Trade Marketing Manager"`

Para agências:

- `"Agência" produção eventos diretor`
- `"Agência" operações live marketing`
- `"Agência" experiential producer`
- `"Agência" case "Cliente" evento`
- `"Agência" montadora estande`
- `"Agência" produção cenografia`

---

# Fontes de evidência prioritárias

## Tier A — primárias

- Site oficial do evento
- Site/newsroom da empresa
- Manual/regulamento oficial do expositor
- Portal oficial de fornecedores
- PNCP/Compras.gov/portais oficiais
- Resposta ou assinatura recebida pela própria MODU

## Tier B — autorizadas/semiprivadas

- Provedores B2B autorizados (ex.: Apollo) usados após entity resolution
- Associações setoriais
- Premiações/cases de agência com autoria clara

## Tier C — descoberta, não validação única

- Mecanismos de busca
- Snippets indexados
- Redes sociais corporativas públicas
- Agregadores

---

# Compliance de referência

- RFC 9309 — Robots Exclusion Protocol: https://www.rfc-editor.org/rfc/rfc9309.html
- LGPD — Lei 13.709/2018: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709compilado.htm
- ANPD — Guia de Legítimo Interesse: https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia_orientativo_hipoteses_legais_tratamento_de_dados_pessoais_legitimo_interesse
- LinkedIn User Agreement: https://www.linkedin.com/legal/user-agreement
- LinkedIn Crawling Terms: https://www.linkedin.com/legal/crawling-terms
- PNCP: https://www.gov.br/pncp/pt-br/

## Princípio central

O objetivo não é construir a maior base. É construir a **base mais defensável, atual, deduplicada e acionável**, na qual cada decisão comercial possa ser explicada com evidências.