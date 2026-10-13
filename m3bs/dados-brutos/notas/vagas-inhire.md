# M3BS Advogados — Dossiê de VAGAS (inHire + boards externos) — key: vagas-inhire
Data da coleta: 2026-10-13 (UTC). Fontes primárias: API pública inHire (api.inhire.app, tenant "m3bs"), páginas renderizadas de m3bs.inhire.app/vagas/<id>, carreira.inhire.com.br/carreiras/m3bs/, Indeed (MCP oficial), LinkedIn (API guest de vagas), buscadores.

## 0. RESUMO EXECUTIVO (para o sintetizador)
- O M3BS usa o ATS **inHire** (tenant id "m3bs", nome "M3Bs"). Página de carreiras: https://m3bs.inhire.app/vagas . Página institucional de carreiras (WordPress estático hospedado pela inHire): https://carreira.inhire.com.br/carreiras/m3bs/ (hashtag de employer branding **#VEMSERM3BS**).
- Config do tenant (https://api.inhire.app/tenants/public/config/m3bs?withFeatureFlags=true): linkedinUrl = https://www.linkedin.com/company/m3bsadvogados/ ; tenantDomains = https://m3bs.com.br ; integração de agenda de entrevistas = **Outlook** ("integrations.appointments.provider":"outlook") ; permissões do plano inHire incluem "screeningWithAi", "resumeAnalyzer", "scorecard", "hunting", "talentPool", "confidentialJob", "requisitions/approvalWorkflow" — ou seja, triagem de currículo com IA e scorecard de entrevista estão habilitados; vagas confidenciais possíveis.
- **10 vagas abertas** em 13/10/2026 (todas status "published", careerPageId "default"): 7 jurídicas de advogado(a), 2 estágios em Direito, 1 Analista de Comunicação e Marketing.
- Tipos de contrato (campo contractType da API): **"Associado"** (6 vagas de advogado), **"Cooperado"** (1 — Advogado Sênior Contencioso Cível Geral), **"CLT"** (1 — Analista de Comunicação e Marketing), **"Estágio"** (2). "Associado" = advogado associado (regime de associação previsto no Estatuto da OAB/Provimento 169/2015 do CFOAB: sem vínculo empregatício, o advogado participa dos resultados; na prática equivale a PJ/autônomo com contrato de associação; o formulário pede "Pretensão salarial como associado"). "Cooperado" = contratação via cooperativa de advogados (formulário pede "Pretensão salarial como cooperado"). A vaga Pleno Trabalhista diz explicitamente "🕒 Regime de associação". Nenhuma vaga de advogado é CLT.
- Modelos: Híbrido (SP) = 5 vagas de advogado; Remoto (location "BR") = 2 (Júnior Regulatório e Júnior Processos Administrativos ANS); Presencial = Analista Comunicação + 2 estágios.
- Todas as vagas estão replicadas automaticamente nos boards: activeJobBoards = ["indeedATSIntegration","linkedin","netVagas","jobBoardPool","talent"] (Indeed via integração ATS, LinkedIn, NetVagas, pool de job boards, Talent.com). Duas vagas (Sênior Cível Geral e Massificado) têm jobUrl do Indeed apontando para o Glassdoor (glassdoor.com.br/partner/jobListing...), indicando anúncio pago/patrocinado via Indeed-Glassdoor.
- Campos obrigatórios do formulário inHire: Nome, e-mail, celular, **LinkedIn (obrigatório em todas)**, currículo (anexo), e conforme a vaga: "Você tem disponibilidade para trabalhar no modelo híbrido/presencial em São Paulo?" (Sim/Não), "País de origem" + "Cidade", "Pretensão salarial como associado/cooperado/CLT". Nenhuma vaga tem perguntas de triagem dissertativas; não há nome de recrutador exposto na página pública.
- Etapas do processo seletivo (carreira.inhire.com.br/carreiras/m3bs/): 1) Inscrição – envio de currículo; 2) Triagem pela equipe de Recursos Humanos; 3) Entrevista técnica com Recursos Humanos; 4) Entrevista técnica com Coordenador(a) responsável do setor jurídico; 5) Prova prática ou estudo de caso; 6) Feedback e proposta de contratação.
- Benefícios internos (carreiras): Cartão Flash VR e VT; Plano de Saúde Amil; Parcerias Educacionais; TotalPass; Day off de aniversário; "Ambiente com estrutura moderna e tecnologia de TI segura"; "Oportunidades de aprendizado contínuo"; "Participação em projetos regulatórios de alto impacto"; "Participação em eventos, publicações e visibilidade profissional"; "Possibilidade de atuação em múltiplas frentes jurídicas". Nas vagas: Flash Benefícios (alimentação/refeição e mobilidade), AMIL com coparticipação, Seguro de vida Zurich, Plano de carreira, Programa de bônus, parcerias com IES/pós/idiomas, TotalPass.
- Indeed (dados da página da empresa via MCP Indeed): companyPageUrl https://br.indeed.com/cmp/M3bs-Advogados ; nota geral 5/5 (poucas avaliações), entrevista: dificuldade "EASY", experiência "EXCELLENT", duração do processo "TWO_WEEKS"; satisfação salarial 3 sim / 0 não.
- Glassdoor: ID E9182621 (página de vagas https://www.glassdoor.com.br/Vagas/M3BS-Advogados-Vagas-E9182621.htm e avaliações https://www.glassdoor.com.br/Avalia%C3%A7%C3%B5es/M3BS-S%C3%A3o-Paulo-Avalia%C3%A7%C3%B5es-EI_IE9182621.0,4_IL.5,14_IC2479061.htm) — bloqueado por Cloudflare para curl/Playwright/WebFetch nesta sessão.
- LinkedIn company ID numérico = **22331495** (link "Visualizar vagas": https://www.linkedin.com/jobs/m3bs-advogados-jobs-worldwide?f_C=22331495). 14.746 seguidores, 124 funcionários no LinkedIn, sede Av. Paulista 854, 3º andar.
- Histórico de vagas antigas (fechadas) encontradas: (a) Indeed "Advogado(a) Pleno - Saúde Suplementar e Regulatório ANS - São Paulo" (jk=fbf2f9ba176ecabc), ~165 dias antes da indexação (≈ abr/mai 2026), 100% presencial, mínimo 3 anos de regulatório ANS; (b) Indeed "Advogado(a) Pleno – Contencioso Cível Geral" (jk=36c669da948515c2); (c) Indeed "Advogado(a) Pleno - Contencioso Cível com experiência em Saúde Suplementar Massificado, M3Bs, Remoto" (snippet de busca); (d) LinkedIn — Renata Mellim (Coordenadora do Contencioso Cível) compartilhou vaga "Advogado(a) – Multidisciplinar Estratégico" no M3BS, São Paulo (snippet: "há cerca de 2 semanas", data da indexação desconhecida); (e) LinkedIn — Marcelo Alves (Advogado, M3BS) compartilhou anúncio "Advogado(a) Jr III e Pleno" com envio de currículo para **rh@m3bs.com.br**, assunto "Contencioso de Volume - Saúde Suplementar" (snippet: "cerca de 3 anos" em um resultado e "cerca de 5 anos" em outro → entre 2021 e 2023). Indica que o escritório usa níveis internos "Júnior I/II/III, Pleno, Sênior".
- devjobsscanner.com/company/m3bs-advogados/ lista "Analista de Comunicação e Marketing — M3BS Advogados — São Paulo — via LinkedIn" (página bloqueada por Cloudflare; só snippet).

---- 1. VAGAS ABERTAS: metadados da API inHire (api.inhire.app/job-posts/public/pages/<jobId>) e descrição completa ----

================================================================================
Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "jobBoardPool", "talent"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-07-07T12:56:34.529Z", "displayName": "Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos", "jobBoardsData": {"indeedATSIntegration": {"jobUrl": "https://m3bs.inhire.app/vagas/cccb84e1-daae-4702-a39d-88bcfdb0321a/advogado-pleno-recuperacao-de-credito-e-aquisicao-estrategica-de-creditos?source=indeed", "jobKey": "93ffdd9321e4f8c7"}}, "lastPublishedAt": "2026-07-07T12:56:34.529Z", "publishedAt": "2026-07-07T12:56:34.529Z", "settings": {"fields": ["linkedin", "curriculum", "workModel", "location"], "requiredFields": ["linkedin", "curriculum", "workModel", "location"]}, "status": "published", "updatedAt": "2026-10-06T14:29:32.057Z", "jobId": "cccb84e1-daae-4702-a39d-88bcfdb0321a", "workplaceType": "Hybrid", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos
Objetivo da posição:
Atuar na identificação, análise e estruturação de oportunidades de aquisição de créditos específicos com elevado potencial de recuperação financeira, especialmente aqueles relacionados a processos de recuperação judicial, falência, execuções, insolvência empresarial e leilões judiciais ou extrajudiciais. O profissional deverá avaliar a viabilidade jurídica, econômica e estratégica dos ativos, subsidiando decisões de investimento e conduzindo as medidas necessárias para maximizar sua recuperação.
Formação:
Graduação em Direito.
Inscrição ativa na OAB.
Pós-graduação em Direito Empresarial, Recuperação Judicial e Falências, Processo Civil ou áreas correlatas será considerada diferencial.
Experiência desejada:
Entre 4 e 8 anos de atuação.
Experiência em recuperação de crédito empresarial.
Atuação em execuções, cumprimento de sentença e medidas de constrição patrimonial.
Vivência em processos de recuperação judicial e falência.
Experiência na negociação ou cessão de créditos específicos será considerada diferencial.
Conhecimento na análise jurídica de ativos judiciais e extrajudiciais com potencial de aquisição.
Conhecimentos técnicos:
O profissional deverá possuir domínio de:
Lei nº 11.101/2005 (Recuperação Judicial e Falências), com as alterações da Lei nº 14.112/2020.
Código de Processo Civil.
Execução e recuperação de crédito.
Pesquisa patrimonial e localização de ativos.
Alienação judicial de bens.
Leilões judiciais e extrajudiciais.
Cessão de créditos.
Classificação e preferência de créditos em processos concursais.
Garantias reais e fidejussórias.
Due diligence jurídica de créditos.
Avaliação de risco jurídico.
Noções de análise econômico-financeira aplicadas à precificação de créditos.
Principais responsabilidades:
Prospectar oportunidades de aquisição de créditos específicos com elevado potencial de recuperação.
Monitorar processos de recuperação judicial, falência, insolvência civil, execuções relevantes e procedimentos de alienação de ativos.
Identificar créditos estratégicos passíveis de cessão ou aquisição.
Avaliar editais de leilões judiciais e extrajudiciais para identificação de oportunidades.
Elaborar pareceres jurídicos sobre a viabilidade de aquisição dos créditos.
Realizar due diligence jurídica dos ativos.
Analisar garantias, posição do crédito na ordem de preferência, riscos processuais e perspectivas de recuperação.
Participar de negociações para aquisição de créditos.
Estruturar estratégias jurídicas voltadas à maximização do valor recuperável.
Atuar nos processos relacionados aos créditos adquiridos, promovendo medidas para sua efetiva recuperação.
Desenvolver relacionamento com administradores judiciais, instituições financeiras, credores, leiloeiros, gestores judiciais e demais agentes do mercado, ampliando o acesso a oportunidades.
Competências comportamentais:
Visão estratégica e orientação para negócios.
Capacidade analítica.
Perfil investigativo.
Proatividade na identificação de oportunidades.
Capacidade de negociação.
Boa comunicação interpessoal.
Organização e gestão de múltiplas demandas.
Tomada de decisão baseada em análise de riscos.
Interesse pelo mercado de ativos judiciais e situações especiais.
Diferenciais:
Será considerado diferencial possuir experiência com:
Investimentos em ativos judiciais.
Créditos oriundos de recuperações judiciais e falências.
Leilões judiciais.
Operações de cessão de crédito.
Distressed Assets e Special Situations.
Ferramentas de pesquisa patrimonial.
Inteligência artificial aplicada à análise processual.
Excel, Power BI ou ferramentas de análise de dados.
Perfil esperado:
Profissional com sólida formação em recuperação de crédito e insolvência empresarial, capaz de combinar rigor técnico, visão de negócios e postura proativa para identificar ativos jurídicos de alto valor econômico. Mais do que conduzir processos, espera-se que o profissional desenvolva inteligência de mercado, identifique oportunidades de aquisição de créditos específicos e contribua para a estruturação de operações capazes de gerar resultados financeiros expressivos para clientes e para o escritório. Trata-se de uma atuação consultiva e estratégica, voltada à transformação de litígios e ativos em oportunidades de investimento e geração de valor.

================================================================================
Advogado(a)  – Contencioso Cível Saúde Suplementar
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "jobBoardPool", "talent"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-07-30T19:11:09.033Z", "displayName": "Advogado(a)  – Contencioso Cível Saúde Suplementar", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "0f8801b94c0145e6", "jobUrl": "https://m3bs.inhire.app/vagas/27dcffce-61e2-4c16-be1d-d8a16f532fed/advogadoa-contencioso-civel-saude-suplementar?source=indeed"}}, "lastPublishedAt": "2026-07-30T19:11:09.033Z", "publishedAt": "2026-07-30T19:11:09.033Z", "settings": {"fields": ["linkedin", "curriculum", "workModel"], "requiredFields": ["linkedin", "curriculum", "workModel"]}, "status": "published", "updatedAt": "2026-10-11T19:44:42.781Z", "jobId": "27dcffce-61e2-4c16-be1d-d8a16f532fed", "workplaceType": "Hybrid", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Advogado(a) – Contencioso Cível Saúde Suplementar
 Sobre a posição:
Oportunidade para Advogado(a) em Contencioso Cível, com experiência em Saúde Suplementar, vivência em gestão de carteira de processos e autonomia na condução de casos, boa redação jurídica e capacidade de análise crítica e disponibilidade para audiências e reuniões externas.
Principais responsabilidades:
Atuação em processos judiciais cíveis envolvendo operadoras de plano de saúde.
Elaboração de peças processuais (iniciais, contestações, recursos, manifestações diversas, memoriais etc.).
Análise de ações judiciais relacionadas a negativa de cobertura, fornecimento de medicamentos, procedimentos médicos e indenizações.
Atendimento a clientes e acompanhamento processual, prestando esclarecimentos técnicos e estratégicos.
Controle de prazos processuais e gestão de publicações.
Realização de audiências e sustentações orais, quando necessário.
Elaboração de relatórios jurídicos e pareceres para clientes internos e externos.
Apoio ao time estratégico na definição de teses jurídicas e medidas preventivas.
Acompanhamento de jurisprudência e legislação voltada ao direito da saúde.
Requisitos:
Graduação completa em Direito;
OAB ativa e regular.
Experiência em Saúde Suplementar, Contencioso cível (planos de saúde);
Experiência em análise de risco processual, relatórios gerenciais e estratégias jurídicas;
Habilidades Desejáveis:
Gestão autônoma de processos e cumprimento de prazos com organização e eficiência;
Redação jurídica clara e objetiva, com boa argumentação técnica;
Capacidade analítica para avaliação de risco processual e elaboração de estratégias jurídicas;
Tomada de decisão segura em situações de complexidade e urgência;
Boa comunicação interpessoal, com facilidade para se relacionar com clientes, pares e gestores;
Proatividade e iniciativa na resolução de problemas;
Trabalho em equipe, colaborando com colegas e áreas correlatas;
Gestão do tempo e prioridades, garantindo eficiência em múltiplas demandas simultâneas;
Visão estratégica voltada para resultados e alinhamento aos objetivos do cliente e do escritório.
Diferenciais:
Atuação em interface com contencioso cível, com foco em saúde suplementar.

================================================================================
Advogado(a) Júnior – Processos Administrativos | Saúde Suplementar (ANS)
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "talent", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-10-05T21:48:16.992Z", "displayName": "Advogado(a) Júnior – Processos Administrativos | Saúde Suplementar (ANS)", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "c3685ed1cc79a4fd", "jobUrl": "https://m3bs.inhire.app/vagas/e3103725-0afb-4ef8-8b63-239e465e8ce1/advogadoa-junior-processos-administrativos-or-saude-suplementar-ans?source=indeed"}}, "lastPublishedAt": "2026-10-05T21:48:16.992Z", "publishedAt": "2026-10-05T21:48:16.992Z", "settings": {"fields": ["linkedin", "salary", "curriculum", "location"], "requiredFields": ["linkedin", "salary", "curriculum", "location"]}, "status": "published", "updatedAt": "2026-10-13T01:28:29.478Z", "jobId": "e3103725-0afb-4ef8-8b63-239e465e8ce1", "workplaceType": "Remote", "location": "BR", "salaryCurrency": "BRL"}

Buscamos Advogado(a) Júnior para atuação com processos administrativos no âmbito da Agência Nacional de Saúde Suplementar (ANS).
Procuramos um profissional com experiência prévia em saúde suplementar, perfil analítico, organização e boa capacidade de comunicação, que tenha interesse em se desenvolver tecnicamente em um ambiente dinâmico e colaborativo.
Principais atividades
- 
Elaborar defesas, manifestações e recursos em processos administrativos no âmbito da ANS;
- 
Realizar análise jurídica e acompanhamento dos processos administrativos sob sua responsabilidade;
- 
Controlar prazos e acompanhar o andamento das demandas;
- 
Interagir com clientes para levantamento de informações, esclarecimento de dúvidas e suporte na condução dos processos;
- 
Acompanhar legislações, normas, resoluções e regulamentações aplicáveis à saúde suplementar;
- 
Apoiar a análise de alterações regulatórias e seus possíveis impactos nos processos e clientes;
- 
Contribuir para a qualidade técnica e o cumprimento dos padrões das entregas da área.
Requisitos
- 
Graduação completa em Direito;
- 
Registro ativo na OAB;
- 
Experiência prévia com Saúde Suplementar, especialmente em processos administrativos perante a ANS;
- 
Conhecimento da legislação e regulamentação aplicáveis ao setor de saúde suplementar;
- 
Boa capacidade de análise processual e jurídica;
- 
Boa comunicação oral e escrita;
- 
Organização e atenção aos detalhes;
- 
Comprometimento com prazos e qualidade das entregas;
- 
Perfil colaborativo e interesse em desenvolvimento contínuo.
Diferenciais
- 
Pós-graduação ou especialização em Direito da Saúde, Saúde Suplementar, Direito Administrativo ou áreas correlatas;
- 
Experiência com atendimento jurídico a operadoras de planos de saúde;
- 
Vivência com processos sancionadores e outros procedimentos administrativos regulados pela ANS.
O que oferecemos
- 
Remuneração compatível com o mercado;
- 
Benefícios de alimentação e/ou refeição e mobilidade por meio da Flash Benefícios;
- 
Assistência médica AMIL, em regime de coparticipação;
- 
Seguro de vida Zurich;
- 
Plano de carreira;
- 
Programa de bônus;
- 
Parcerias com instituições de ensino superior, cursos de pós-graduação e escolas de idiomas;
- 
Acesso ao TotalPass.

================================================================================
Advogado(a) Júnior – Regulatório Saúde Suplementar
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "talent", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-09-29T13:39:19.823Z", "displayName": "Advogado(a) Júnior – Regulatório Saúde Suplementar", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "3b0cfc075b613417", "jobUrl": "https://m3bs.inhire.app/vagas/7ead6544-fed6-4943-b660-587c63834865/advogadoa-junior-regulatorio-saude-suplementar?source=indeed"}}, "lastPublishedAt": "2026-09-29T13:39:19.823Z", "publishedAt": "2026-09-29T13:39:19.823Z", "settings": {"requiredFields": ["linkedin", "curriculum"], "fields": ["linkedin", "curriculum"]}, "status": "published", "updatedAt": "2026-10-13T01:00:02.504Z", "jobId": "7ead6544-fed6-4943-b660-587c63834865", "workplaceType": "Remote", "location": "BR", "salaryCurrency": "BRL"}

Sobre a oportunidade
Estamos em busca de uma pessoa organizada, proativa e comprometida para integrar o time regulatório, em regime de trabalho remoto. A atuação envolverá, principalmente, a elaboração de respostas de NIP, bem como o apoio às demais demandas da equipe regulatória, com interface interna e suporte às rotinas técnicas do escritório.
Principais atividades
§ Elaborar respostas de NIP, garantindo qualidade técnica, clareza e aderência às normas da ANS;
§ Apoiar a equipe regulatória em demandas diversas, além das respostas de NIP, conforme necessidade da área;
§ Auxiliar na análise e condução de questões regulatórias relacionadas à saúde suplementar;
§ Atuar em conjunto com diferentes equipes, contribuindo para o fluxo, organização e acompanhamento das demandas;
§ Participar de treinamentos, reuniões e alinhamentos promovidos pelo escritório;
§ Apoiar as rotinas operacionais e estratégicas da área regulatória;
§ Participar das atividades e iniciativas promovidas pelo escritório.
Requisitos mandatórios
§ OAB ativa;
§ Excelente redação jurídica e domínio da linguagem formal;
§ Boa comunicação verbal e habilidade para interação com equipes;
§ Perfil organizado, analítico e proativo;
§ Capacidade de gestão de demandas e cumprimento de prazos;
§ Autonomia, responsabilidade e atenção aos detalhes;
§ Facilidade para trabalho em equipe, inclusive em ambiente remoto.
Diferenciais
§ Experiência prévia com NIP ou demandas regulatórias em saúde suplementar;
§ Vivência em escritórios com atuação regulatória;
§ Interesse na área de saúde suplementar;
§ Conhecimento da legislação e normativas da ANS;
§ Familiaridade com sistemas de gestão de demandas e fluxos regulatórios.
O que oferecemos
§ Ambiente colaborativo, dinâmico e com constante troca de conhecimento;
§ Oportunidade de desenvolvimento técnico e profissional na área regulatória;
§ Atuação diversificada, com contato com diferentes frentes do regulatório.

================================================================================
Advogado(a) Pleno – Contencioso Trabalhista
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "talent", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-09-25T21:29:56.154Z", "displayName": "Advogado(a) Pleno – Contencioso Trabalhista", "lastPublishedAt": "2026-10-06T21:24:49.204Z", "publishedAt": "2026-09-25T21:29:56.154Z", "settings": {"fields": ["linkedin", "salary", "curriculum", "workModel"], "requiredFields": ["linkedin", "salary", "curriculum", "workModel"]}, "status": "published", "updatedAt": "2026-10-06T21:24:49.204Z", "jobId": "fff14670-f04c-4057-9aab-af089ceb4760", "workplaceType": "Hybrid", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Advogado(a) Pleno – Contencioso Trabalhista
📍 Modelo híbrido
🕒 Regime de associação
🏥 Atuação com foco no setor de Saúde Suplementar
Estamos em busca de um(a) Advogado(a) Júnior para atuar no contencioso trabalhista, com foco em demandas estratégicas, elaboração de peças de alta complexidade e relacionamento direto com clientes.
Procuramos um(a) profissional com sólida experiência em Direito do Trabalho, autonomia na condução de processos e visão estratégica para contribuir ativamente com os resultados da área.
Principais responsabilidades:
Elaboração e revisão de peças processuais de média e alta complexidade, incluindo contestações, recursos, contrarrazões, agravos, memoriais e manifestações diversas; 
Análise crítica de sentenças e acórdãos, com definição de estratégias processuais e recursais; 
Atuação em audiências presenciais e telepresenciais; 
Gestão integral de carteira de processos trabalhistas, incluindo acompanhamento processual e controle de prazos; 
Interface direta com clientes para alinhamentos técnicos e estratégicos; 
Elaboração de relatórios, pareceres e orientações jurídicas; 
Apoio técnico e orientação a estagiários(as) e profissionais em início de carreira; 
Acompanhamento de processos em todas as fases, desde o conhecimento até a execução. 
Atuação no setor de Saúde Suplementar
O profissional terá contato com demandas trabalhistas relacionadas a:
Profissionais da área da saúde (médicos, enfermeiros, técnicos e equipes administrativas); 
Escalas de trabalho, plantões, jornadas diferenciadas e banco de horas; 
Adicionais de insalubridade, periculosidade, trabalho noturno e horas extras; 
Contratos de trabalho e contratos de prestação de serviços médicos; 
Auditorias trabalhistas e ações de prevenção de passivos; 
Atualização e acompanhamento da jurisprudência dos Tribunais Trabalhistas e das alterações legislativas aplicáveis ao segmento. 
Perfil desejado:
Conhecimento sólido em Direito do Trabalho e Processo do Trabalho; 
Capacidade analítica e visão estratégica; 
Organização e excelência na gestão de prazos; 
Boa comunicação escrita e verbal; 
Postura profissional para atuação em audiências e no relacionamento com clientes; 
Interesse ou experiência prévia no segmento de Saúde Suplementar. 
Requisitos:
✅ Graduação em Direito e OAB ativa;
✅ Experiência compatível com posição de nível pleno;
✅ Excelente redação jurídica e capacidade de análise crítica;
✅ Organização, autonomia e proatividade.
Diferenciais:
⭐ Pós-graduação em Direito do Trabalho, Direito da Saúde ou áreas correlatas;
⭐ Experiência com operadoras de planos de saúde, hospitais ou escritórios especializados no setor;
⭐ Vivência em demandas trabalhistas estratégicas e consultivas.

================================================================================
Advogado(a) Sênior – Contencioso Cível Geral
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "indeedATSIntegration", "linkedin", "netVagas", "talent", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Cooperado"], "createdAt": "2026-10-06T21:21:49.220Z", "displayName": "Advogado(a) Sênior – Contencioso Cível Geral", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "f543534378e3bb96", "jobUrl": "https://www.glassdoor.com.br/partner/jobListing.htm?pos=108&ao=1136043&s=224&guid=000001a13190487098a9df92397f50b1&src=GD_JOB_AD&t=JA&vt=e&ja=405266878&uido=E01B9F2031D05DE4BBA97CAF102A2F3E&ea=1&cs=1_be91b142&cb=1791840937735&jobListingId=1010287536300&jrtk=5-yul1-3-1k4p0lm962h29i00-1k4ouckcoj73c805"}}, "lastPublishedAt": "2026-10-06T21:21:49.220Z", "publishedAt": "2026-10-06T21:21:49.220Z", "settings": {"fields": ["linkedin", "salary", "curriculum", "workModel", "location"], "requiredFields": ["linkedin", "salary", "curriculum", "workModel", "location"]}, "status": "published", "updatedAt": "2026-10-12T21:36:20.056Z", "jobId": "3dc83622-65ed-4767-a123-3ebcd8434044", "workplaceType": "Hybrid", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Oportunidade para Advogado(a) Sênior em Contencioso Cível Geral, com atuação em carteira diversificada e multitemática de processos, envolvendo demandas como Direito de Família, Recuperação de Crédito, questões contratuais, responsabilidade civil, obrigações e demais matérias relacionadas ao Direito Civil.
Busca-se profissional com sólida experiência contenciosa, elevada autonomia na condução de casos de média e alta complexidade, capacidade para definição de estratégias processuais, gestão de carteira, controle de prazos e agenda em sistema, além de atuação direta junto a clientes.
A posição exige domínio da rotina contenciosa, incluindo despachos com juízes e desembargadores, participação em audiências e reuniões externas, negociação de acordos, excelente redação jurídica e forte capacidade de análise crítica e avaliação de riscos.
Principais atribuições
· Atuação em processos de Contencioso Cível Geral, em todas as fases processuais, considerando uma carteira diversificada de matérias;
· Condução de demandas de média e alta complexidade, incluindo temas relacionados a Direito de Família, Recuperação de Crédito, Contratos, Responsabilidade Civil, Obrigações e matérias correlatas;
· Elaboração e revisão de peças processuais, incluindo petições iniciais, contestações, réplicas, recursos, manifestações e demais peças jurídicas;
· Acompanhamento processual e gestão de prazos em sistemas eletrônicos dos tribunais;
· Análise de publicações, decisões e sentenças, com definição e proposição de estratégias processuais;
· Avaliação de riscos, cenários e alternativas jurídicas para subsidiar a tomada de decisão dos clientes e do escritório;
· Participação em audiências de conciliação, instrução e julgamento;
· Realização de despachos com magistrados e demais interlocuções necessárias à condução estratégica dos processos;
· Atuação em negociações, composição de acordos e tratativas extrajudiciais;
· Elaboração de relatórios processuais e materiais executivos para acompanhamento da carteira;
· Contato direto com clientes para alinhamento de estratégias, apresentação de riscos e atualização sobre o andamento dos processos;
· Realização de pesquisas jurídicas e análise de jurisprudência e legislação aplicável;
· Apoio técnico e orientação de advogados menos experientes e estagiários, quando necessário;
· Identificação de oportunidades de melhoria na condução da carteira, buscando maior eficiência, qualidade técnica e melhores resultados.
Requisitos:
· Graduação completa em Direito;
· OAB ativa e regular;
· Experiência consolidada em Contencioso Cível Geral;
· Experiência na condução autônoma de processos de média e alta complexidade;
· Vivência com carteira diversificada de demandas cíveis;
· Experiência em relacionamento direto com clientes e definição de estratégias processuais.
Habilidades Desejáveis:
· Gestão autônoma de processos e carteira, com organização e eficiência no cumprimento de prazos;
· Redação jurídica clara, objetiva e tecnicamente consistente;
· Capacidade analítica para avaliação de riscos e construção de estratégias jurídicas;
· Segurança técnica e capacidade de tomada de decisão em situações de maior complexidade e urgência;
· Capacidade de transitar por diferentes matérias dentro do Direito Civil;
· Boa comunicação e habilidade para condução de reuniões e relacionamento com clientes;
· Capacidade de negociação e construção de soluções jurídicas;
· Proatividade e iniciativa na resolução de problemas;
· Capacidade de orientar e apoiar tecnicamente profissionais mais juniores;
· Trabalho em equipe e colaboração com demais profissionais e áreas do escritório;
· Gestão do tempo e de prioridades, garantindo eficiência diante de múltiplas demandas simultâneas;
· Visão estratégica e orientação para resultados, considerando os objetivos do cliente e do escritório.
O que oferecemos:
Remuneração compatível com o mercado;
Benefícios de alimentação e/ou refeição e mobilidade por meio da Flash Benefícios;
Assistência médica AMIL, em regime de coparticipação;
Seguro de vida Zurich;
Plano de carreira;
Programa de bônus;
Parcerias com instituições de ensino superior, cursos de pós-graduação e escolas de idiomas;
Acesso ao TotalPass.

================================================================================
Advogado(a) – Contencioso Cível Saúde Suplementar Massificado
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "talent", "netVagas", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Associado"], "createdAt": "2026-10-02T21:31:08.279Z", "displayName": "Advogado(a) – Contencioso Cível Saúde Suplementar Massificado", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "b1aef84347cec38d", "jobUrl": "https://www.glassdoor.com.br/partner/jobListing.htm?pos=108&ao=1136043&s=58&guid=000001a120ebc3f7a6431d1e3bbd97c6&src=GD_JOB_AD&t=SR&vt=w&uido=3A914EBCD923005458845D3E36525B66&ea=1&cs=1_dbdfbb5c&cb=1791554470681&jobListingId=1010283985233&jrtk=5-yul1-3-1k4gffeqn2bpth00-1k4genh6mgb0t801"}}, "lastPublishedAt": "2026-10-02T21:31:08.279Z", "publishedAt": "2026-10-02T21:31:08.279Z", "settings": {"requiredFields": ["linkedin", "curriculum", "workModel"], "fields": ["linkedin", "curriculum", "workModel"]}, "status": "published", "updatedAt": "2026-10-09T14:02:00.887Z", "jobId": "9e59208d-e92a-4311-8a44-a66f2d0985e5", "workplaceType": "Hybrid", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Sobre a posição:
Oportunidade para Advogado(a) em Contencioso Cível, com experiência em Saúde Suplementar, vivência em gestão de carteira de processos e autonomia na condução de casos, boa redação jurídica e capacidade de análise crítica e disponibilidade para audiências e reuniões externas.
Principais responsabilidades:
Atuação em processos judiciais cíveis envolvendo operadoras de plano de saúde.
Elaboração de peças processuais (iniciais, contestações, recursos, manifestações diversas, memoriais etc.).
Análise de ações judiciais relacionadas a negativa de cobertura, fornecimento de medicamentos, procedimentos médicos e indenizações.
Atendimento a clientes e acompanhamento processual, prestando esclarecimentos técnicos e estratégicos.
Controle de prazos processuais e gestão de publicações.
Realização de audiências e sustentações orais, quando necessário.
Elaboração de relatórios jurídicos e pareceres para clientes internos e externos.
Apoio ao time estratégico na definição de teses jurídicas e medidas preventivas.
Acompanhamento de jurisprudência e legislação voltada ao direito da saúde.
Requisitos:
Graduação completa em Direito;
OAB ativa e regular.
Experiência em Saúde Suplementar, Contencioso cível (planos de saúde);
Experiência em análise de risco processual, relatórios gerenciais e estratégias jurídicas;
Habilidades Desejáveis:
Gestão autônoma de processos e cumprimento de prazos com organização e eficiência;
Redação jurídica clara e objetiva, com boa argumentação técnica;
Capacidade analítica para avaliação de risco processual e elaboração de estratégias jurídicas;
Tomada de decisão segura em situações de complexidade e urgência;
Boa comunicação interpessoal, com facilidade para se relacionar com clientes, pares e gestores;
Proatividade e iniciativa na resolução de problemas;
Trabalho em equipe, colaborando com colegas e áreas correlatas;
Gestão do tempo e prioridades, garantindo eficiência em múltiplas demandas simultâneas;
Visão estratégica voltada para resultados e alinhamento aos objetivos do cliente e do escritório.
Diferenciais:
Atuação em interface com contencioso cível, com foco em saúde suplementar.

================================================================================
Analista de Comunicação e Marketing
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "netVagas", "jobBoardPool", "talent"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["CLT"], "createdAt": "2026-09-09T15:14:19.112Z", "displayName": "Analista de Comunicação e Marketing", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "37779a2ce6e07440", "jobUrl": "https://m3bs.inhire.app/vagas/a3e12a90-1819-4bd6-ba15-8211bac9a96d/analista-de-comunicacao-e-marketing?source=indeed"}}, "lastPublishedAt": "2026-09-09T15:14:19.112Z", "publishedAt": "2026-09-09T15:14:19.112Z", "settings": {"fields": ["linkedin", "salary", "curriculum", "workModel"], "requiredFields": ["linkedin", "salary", "workModel", "curriculum"]}, "status": "published", "updatedAt": "2026-10-13T01:41:32.307Z", "jobId": "a3e12a90-1819-4bd6-ba15-8211bac9a96d", "workplaceType": "On-site", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Analista de Comunicação e Marketing
Buscamos um profissional criativo, organizado, com perfil hands-on para integrar a área de Comunicação do Escritório de Advocacia M3BS.
A posição terá atuação dinâmica, envolvendo produções de conteúdos, criações de peças gráficas, redes sociais, comunicações internas, e-mail marketing, edições básicas de imagens e vídeos e apoio à realização de eventos internos e externos.
Alguém que possa transformar briefings e direcionamentos em entregas de comunicações claras, visualmente consistentes e adequadas aos diferentes canais do escritório.
Principais responsabilidades
Atuar na criação de peças gráficas e materiais de comunicação para as redes sociais, campanhas institucionais, comunicados internos, apresentações, eventos e demais demandas da área;
Dedicar apoio a gestão dos canais digitais e redes sociais do M3BS, incluindo a organização das pautas, produção, publicação e acompanhamento dos conteúdos;
Realizar edições de imagens e vídeos, cortes, ajustes, aplicações de identidade visual, legendas e adaptações para diferentes formatos;
Participar da organização de eventos internos e externos, acompanhando as diferentes etapas do projeto, desde o planejamento e preparação até a execução e o pós-evento;
Apoiar na produção de materiais para eventos, como convites, apresentações, sinalização, peças digitais, materiais impressos, brindes e conteúdos de divulgação;
Operar em outras iniciativas de comunicação institucional conforme as prioridades e direcionamentos da liderança.
Requisitos:
Formação em Publicidade e Propaganda, Comunicação Social, Marketing ou áreas correlatas;
Conhecimento em design gráfico e composição visual;
Domínio em Canva e conhecimento em ferramentas como Photoshop, Illustrator ou similares;
Conhecimento em ferramentas de edição de vídeo, como CapCut, Premiere ou similares;
Diferenciais:
Experiência anterior em agências, escritórios, empresas B2B ou ambientes corporativos;
Conhecimento em plataformas de e-mail marketing e automação de marketing;
Noções de fotografia e captação de vídeos;
Conhecimento básico de métricas e acompanhamento de desempenho de redes sociais e campanhas digitais;
Perfil que buscamos:
Um profissional organizado, com senso estético, boa escrita e disposição para atuar em uma rotina diversa, que possa envolver desde a criação de uma peça para redes sociais ou um e-mail marketing até a preparação dos materiais e acompanhamento de um evento institucional.

================================================================================
Estágio em Direito – Área Trabalhista
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "talent", "netVagas", "jobBoardPool"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Estágio"], "createdAt": "2026-10-07T12:42:47.196Z", "displayName": "Estágio em Direito – Área Trabalhista", "jobBoardsData": {"indeedATSIntegration": {"jobKey": "3aaf7e9fd1f1bbdd", "jobUrl": "https://m3bs.inhire.app/vagas/9919e925-2847-4e5d-a4a5-77a06a50f342/estagio-em-direito-area-trabalhista?source=indeed"}}, "lastPublishedAt": "2026-10-07T12:42:47.196Z", "publishedAt": "2026-10-07T12:42:47.196Z", "settings": {"fields": ["linkedin", "curriculum", "workModel"], "requiredFields": ["linkedin", "curriculum", "workModel"]}, "status": "published", "updatedAt": "2026-10-13T01:47:41.119Z", "jobId": "9919e925-2847-4e5d-a4a5-77a06a50f342", "workplaceType": "On-site", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Estamos em busca de um(a) estagiário(a) para integrar nossa equipe Trabalhista. Se você deseja desenvolver sua carreira em um ambiente dinâmico, com aprendizado constante e atuação prática na área, essa oportunidade pode ser para você.
Requisitos:
Estar regularmente matriculado(a) no curso de Direito, a partir do 6º semestre;
Preferencialmente estudar no período noturno;
Possuir experiência anterior em escritório de advocacia.
Principais atividades:
Acompanhamento e controle de processos judiciais e administrativos;
Atualização de sistemas internos e plataformas de clientes;
Apoio aos advogados na condução de demandas trabalhistas;
Elaboração de petições de baixa e média complexidade, sempre com supervisão;
Pesquisa de legislação, doutrina e jurisprudência;
Organização de documentos e suporte às rotinas da equipe.
Perfil que buscamos:
Boa comunicação oral e escrita;
Excelente redação jurídica e interpretação de textos;
Organização e atenção aos detalhes;
Proatividade e interesse em aprendizado contínuo;
Comprometimento com prazos e qualidade das entregas;
Facilidade para trabalhar em equipe e bom relacionamento interpessoal.
Benefícios:
🚌🚇🚆 Vale Transporte 
🍽️ Vale Alimentação/Refeição
🛡️ Seguro de Vida
🏋️‍♂️ Total Pass

================================================================================
Estágio – Contencioso Cível Geral
{"tenantName": "M3Bs", "activeJobBoards": ["indeedATSIntegration", "linkedin", "talent", "jobBoardPool", "netVagas"], "careerPageId": "default", "careerPageIds": ["default"], "contractType": ["Estágio"], "createdAt": "2026-09-15T19:32:32.049Z", "displayName": "Estágio – Contencioso Cível Geral", "jobBoardsData": {"indeedATSIntegration": {"jobUrl": "https://m3bs.inhire.app/vagas/ad9afe67-5986-4559-8f6f-3ca5198d5eed/estagio-contencioso-civel-geral?source=indeed", "jobKey": "94db6899a39d6ec1"}}, "lastPublishedAt": "2026-09-15T19:32:32.049Z", "publishedAt": "2026-09-15T19:32:32.049Z", "settings": {"requiredFields": ["linkedin", "curriculum", "workModel"], "fields": ["linkedin", "curriculum", "workModel"]}, "status": "published", "updatedAt": "2026-10-09T16:29:26.389Z", "jobId": "ad9afe67-5986-4559-8f6f-3ca5198d5eed", "workplaceType": "On-site", "location": "São Paulo, SP, BR", "locationComplement": "", "salaryCurrency": "BRL"}

Estágio – Contencioso Cível Geral
Local: São Paulo/SP
Modelo: Estágio | 100% Presencial
Estamos em busca de um(a) estudante de Direito, do 6º ao 7º semestre para integrar nossa equipe de Contencioso Cível Geral.
Se você possui boa comunicação, vontade de aprender e interesse em atuar no contencioso estratégico, essa oportunidade é para você!
Principais atividades:
• Auxílio na elaboração de minutas de peças processuais e relatórios;
• Pesquisas doutrinárias e jurisprudenciais;
• Acompanhamento processual em plataformas eletrônicas e controle de prazos;
• Organização de documentos e atualização de sistemas internos;
• Suporte em audiências, diligências e rotinas administrativas jurídicas.
Requisitos:
• Estar cursando Direito entre o 6º e 7º semestre;
• Disponibilidade para atuação presencial.
Benefícios:
Vale transporte;
Vale alimentação/refeição;
Seguro de vida.
Total Pass;
Parcerias acadêmicas.



---- 2. FORMULÁRIO DE INSCRIÇÃO DE CADA VAGA (páginas renderizadas com Playwright em 13/10/2026, m3bs.inhire.app/vagas/<id>) ----
Observação: a página pública de cada vaga mostra apenas: título, modelo (Híbrido/Remoto/Presencial), localização, descrição, "Sobre a empresa", botões de compartilhar (Facebook/LinkedIn/WhatsApp) e o formulário abaixo. NÃO há nome de recrutador, nome de gestor, salário, nem etapas na página da vaga. O botão final varia: "Continuar inscrição" (vagas com mais de uma etapa de formulário) ou "Candidatar-se para a vaga". Rodapé: "Ao fornecer seus dados pessoais, você concorda com o que está descrito nesta Política de Privacidade" (política da inHire). Acessibilidade: "Recursos Assistivos / Acessível em Libras" (Hand Talk).

Campos comuns a TODAS as vagas (obrigatórios, marcados com *): Nome completo; Seu melhor email; Celular com DDD; Linkedin ("Obtenha o link do seu perfil do linkedin — Copie o link do seu perfil do Linkedin e cole no campo acima"); Currículo (Anexar currículo).

Campos extras por vaga:
1) Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos (cccb84e1): País de origem* (Selecione o país) + Cidade*; "Você tem disponibilidade para trabalhar no modelo híbrido em São Paulo, São Paulo, Brasil?*" (Sim/Não). Botão: Continuar inscrição. (Sem pretensão salarial.)
2) Advogado(a) – Contencioso Cível Saúde Suplementar (27dcffce): "Você tem disponibilidade para trabalhar no modelo híbrido em São Paulo, São Paulo, Brasil?*" (Sim/Não). Botão: Continuar inscrição.
3) Advogado(a) Júnior – Processos Administrativos | Saúde Suplementar (ANS) (e3103725, remoto): País de origem* + Cidade*; "Pretensão salarial como associado*". Botão: Continuar inscrição.
4) Advogado(a) Júnior – Regulatório Saúde Suplementar (7ead6544, remoto): só os campos comuns. Botão: Continuar inscrição.
5) Advogado(a) Pleno – Contencioso Trabalhista (fff14670): disponibilidade híbrido SP* (Sim/Não); "Pretensão salarial como associado*". Botão: Candidatar-se para a vaga.
6) Advogado(a) Sênior – Contencioso Cível Geral (3dc83622): País de origem* + Cidade*; disponibilidade híbrido SP*; "Pretensão salarial como cooperado*". Botão: Candidatar-se para a vaga.
7) Advogado(a) – Contencioso Cível Saúde Suplementar Massificado (9e59208d): disponibilidade híbrido SP*. Botão: Continuar inscrição.
8) Analista de Comunicação e Marketing (a3e12a90): "Você tem disponibilidade para trabalhar no modelo presencial em São Paulo, São Paulo, Brasil?*"; "Pretensão salarial como CLT*". Botão: Continuar inscrição.
9) Estágio em Direito – Área Trabalhista (9919e925): disponibilidade presencial SP*. Botão: Continuar inscrição.
10) Estágio – Contencioso Cível Geral (ad9afe67): disponibilidade presencial SP*. Botão: Continuar inscrição.

Mapeamento do campo settings.fields da API → formulário: "linkedin" = campo LinkedIn obrigatório; "curriculum" = anexo; "workModel" = pergunta de disponibilidade híbrido/presencial; "location" = País de origem + Cidade; "salary" = Pretensão salarial (como associado / cooperado / CLT).

---- 3. PÁGINA INSTITUCIONAL DE CARREIRAS (https://carreira.inhire.com.br/carreiras/m3bs/ — renderizada 13/10/2026; site estático Elementor/Simply Static hospedado pela inHire; links para Facebook https://www.facebook.com/M3BSADV, Instagram https://www.instagram.com/m3bsadvogados, LinkedIn https://www.linkedin.com/company/m3bsadvogados; botão "Ver vagas" → https://m3bs.inhire.app/vagas) ----
TEXTO LITERAL:
"Sobre nós / Conheça o M3BS
Em atividade desde 2009, Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados é uma sociedade de advogados constituída por profissionais com ampla experiência no mercado, dedicada ao atendimento preventivo e contencioso de demandas jurídicas, em áreas diversas, a pessoas jurídicas e físicas, no Brasil e no exterior.
Compromisso permanente com o cliente e orientação jurídica de qualidade são atributos de Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados. Para que esses serviços alcancem elevados padrões de eficiência e resultado, o escritório busca conhecer profundamente os negócios e os mercados de seus clientes, com quem mantem um sólido relacionamento, se integrando ao seu cotidiano e contribuindo para a tomada de decisões estratégicas.
DNA M3BS (repete o texto acima)
Diferencial: Atuação moderna, objetiva e precisa. Capacidade de compreensão profunda das necessidades de seus clientes, o que permite estratégias diferenciadas e bons resultados. O cuidado, a eficiência e a performance no campo de consultoria preventiva e na solução de conflitos legais tornam o escritório plataforma de negócios para clientes que, após orientação, têm suas atividades acompanhadas de perto, desde a contratação até a efetiva solução.
Princípios: Atuar com responsabilidade social, contribuindo para uma sociedade melhor e mais justa, sempre à luz da ética. Manter equipe atualizada e na vanguarda na área jurídica.
Missão: Aprimorar o ecossistema de saúde brasileiro.
Visão: Ser referência jurídica no setor de saúde até 2025.
Valores: Conexão / Desenvolvimento de Pessoas / Diversidade / Foco no Cliente / Inovação / Integridade / Sustentabilidade
Benefícios internos: Cartão Flash VR e VT / Plano de Saúde Amil / Parcerias Educacionais / TotalPass / Day off de aniversário / Ambiente com estrutura moderna e tecnologia de TI segura / Oportunidades de aprendizado contínuo / Participação em projetos regulatórios de alto impacto / Participação em eventos, publicações e visibilidade profissional / Possibilidade de atuação em múltiplas frentes jurídicas
Etapas do processo seletivo: Inscrição – envio de currículo → Triagem pela equipe de Recursos Humanos → Entrevista técnica com Recursos Humanos → Entrevista técnica com Coordenador(a) responsável do setor jurídico → Prova prática ou estudo de caso → Feedback e proposta de contratação
#VEMSERM3BS — Confira nossas oportunidades: Ver vagas"
(Nota: a "Visão: Ser referência jurídica no setor de saúde até 2025" está desatualizada na página de carreiras — útil como gancho de conversa sobre próximos ciclos estratégicos.)

---- 4. PÁGINA DE LISTAGEM https://m3bs.inhire.app/vagas (renderizada) ----
Idiomas disponíveis: English / Português [PT] / Português [BR] / Español. Filtros: "Nome da Vaga", "Modelo de Atuação", "Localização". Texto "Sobre a empresa" (o mesmo "about" da API): "O M3BS Advogados é um escritório full service com especialização no setor da saúde. Atuamos com excelência técnica em diversas frentes jurídicas — consultiva, contenciosa e regulatória — atendendo operadoras de planos de saúde, hospitais, clínicas, startups, empresas contratadas pelo poder público e demais agentes do ecossistema da saúde suplementar. Com sede em São Paulo e abrangência nacional, o M3BS alia visão estratégica, domínio técnico e profundo conhecimento do setor para oferecer soluções jurídicas completas e alinhadas às necessidades de seus clientes. Nossa atuação é marcada pela integração entre áreas como contencioso cível, regulatório (ANS), contratos, societário, tributário, negócios públicos e compliance — tudo sob uma estrutura colaborativa, moderna e voltada para resultado."
Feature flags do tenant (datas de ativação, indicam uso recente do ATS): openPositions (2026-07-05), positionLeanTalent (2026-07-20), CalendarWebhookSync (2026-07-23), embeddedInhireDataViz (2026-08-19), requisitionAttachments (2026-08-19), jobCreationDraft (2026-08-27), customFieldsArchive (2026-09-02), includeCustomFieldsConditions (2026-09-21), jobAnalyticsFrame (2026-10-01), bulkEditApprovalWorkflows (2026-10-01), talentJobsHistory (2026-10-01), typesenseTenant (2026-10-05). Banner: https://files.inhire.app/pages/career/banner_m3bs.png ; logo: https://files.inhire.app/pages/career/logo_m3bs.png ; logo tenant: https://files.inhire.app/logos/mbs.png.

---- 5. TABELA-RESUMO DAS 10 VAGAS ABERTAS (13/10/2026) ----
| # | Título | Área | Senioridade | Modelo | Local | Contrato | Criada (createdAt) | Última republicação/atualização | Boards | Salário/benefícios no anúncio |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos | Recuperação de crédito / insolvência / special situations | Pleno (4–8 anos) | Híbrido | São Paulo, SP | Associado | 2026-07-07 | updatedAt 2026-10-06 | Indeed, LinkedIn, NetVagas, pool, Talent | não informa |
| 2 | Advogado(a) – Contencioso Cível Saúde Suplementar | Contencioso cível saúde suplementar (operadoras) | não especificada (exige experiência em saúde suplementar) | Híbrido | São Paulo, SP | Associado | 2026-07-30 | updatedAt 2026-10-11 | idem | não informa |
| 3 | Advogado(a) Júnior – Processos Administrativos / Saúde Suplementar (ANS) | Regulatório/contencioso administrativo ANS | Júnior | Remoto | BR | Associado | 2026-10-05 | updatedAt 2026-10-13 | idem | Flash, AMIL copart., Zurich, plano de carreira, bônus, parcerias, TotalPass |
| 4 | Advogado(a) Júnior – Regulatório Saúde Suplementar | Regulatório (respostas de NIP) | Júnior | Remoto | BR | Associado | 2026-09-29 | updatedAt 2026-10-13 | idem | só "ambiente colaborativo / desenvolvimento" |
| 5 | Advogado(a) Pleno – Contencioso Trabalhista | Trabalhista (foco saúde suplementar) | Pleno (texto do corpo diz "Júnior" — inconsistência no anúncio) | Híbrido | São Paulo, SP | Associado ("Regime de associação") | 2026-09-25 | republicada 2026-10-06 | Indeed, LinkedIn, NetVagas, Talent, pool (sem jobUrl Indeed) | não informa |
| 6 | Advogado(a) Sênior – Contencioso Cível Geral | Cível geral (família, recuperação de crédito, contratos, resp. civil) | Sênior | Híbrido | São Paulo, SP | **Cooperado** | 2026-10-06 | updatedAt 2026-10-12 | idem + anúncio Glassdoor patrocinado | Flash, AMIL copart., Zurich, plano de carreira, bônus, parcerias, TotalPass |
| 7 | Advogado(a) – Contencioso Cível Saúde Suplementar Massificado | Contencioso de volume saúde suplementar | não especificada | Híbrido | São Paulo, SP | Associado | 2026-10-02 | updatedAt 2026-10-09 | idem + anúncio Glassdoor patrocinado | não informa |
| 8 | Analista de Comunicação e Marketing | Comunicação/Marketing | Analista | Presencial | São Paulo, SP | CLT | 2026-09-09 | updatedAt 2026-10-13 | idem | não informa (pede pretensão CLT) |
| 9 | Estágio em Direito – Área Trabalhista | Trabalhista | Estágio (a partir do 6º semestre, pref. noturno, com experiência prévia em escritório) | Presencial | São Paulo, SP | Estágio | 2026-10-07 | updatedAt 2026-10-13 | idem | VT, VA/VR, seguro de vida, TotalPass |
| 10 | Estágio – Contencioso Cível Geral | Cível geral | Estágio (6º–7º semestre) | Presencial | São Paulo, SP | Estágio | 2026-09-15 | updatedAt 2026-10-09 | idem | VT, VA/VR, seguro de vida, TotalPass, parcerias acadêmicas |

Leitura das datas: o escritório abriu 8 das 10 vagas entre 09/09 e 07/10/2026 (ciclo de contratação forte no 2º semestre de 2026). As duas mais antigas (jul/2026) continuam abertas há ~3 meses (Recuperação de Crédito e Contencioso Cível Saúde Suplementar) → posições difíceis de preencher / contratação contínua. A vaga Trabalhista Pleno foi republicada em 06/10 (lastPublishedAt ≠ publishedAt).

Palavras-chave recorrentes nos anúncios jurídicos (úteis para ATS/currículo): "saúde suplementar", "operadoras de planos de saúde", "ANS", "NIP", "processos administrativos", "negativa de cobertura", "fornecimento de medicamentos", "gestão de carteira de processos", "controle de prazos", "gestão de publicações", "redação jurídica clara e objetiva", "análise de risco processual", "relatórios gerenciais", "estratégias jurídicas", "audiências e sustentações orais", "pareceres", "teses jurídicas", "jurisprudência e legislação voltada ao direito da saúde", "autonomia", "proatividade", "visão estratégica voltada para resultados", "trabalho em equipe", "gestão do tempo e prioridades", "atendimento a clientes", "relacionamento com clientes, pares e gestores", "Lei 11.101/2005", "Lei 14.112/2020", "CPC", "execução", "cumprimento de sentença", "pesquisa patrimonial", "leilões judiciais", "cessão de créditos", "due diligence", "distressed assets", "special situations", "Excel/Power BI", "inteligência artificial aplicada à análise processual", "Direito do Trabalho", "Processo do Trabalho", "escalas, plantões, banco de horas", "insalubridade", "contratos de prestação de serviços médicos", "auditorias trabalhistas", "Direito de Família", "responsabilidade civil", "despachos com magistrados", "negociação de acordos".


---- 6. AS MESMAS VAGAS NO LINKEDIN (página pública https://br.linkedin.com/jobs/m3bs-advogados-vagas e API guest jobs-guest/jobs/api/jobPosting/<id>, lidas em 13/10/2026) ----
Company ID LinkedIn = 22331495. Todas as 10 vagas aparecem como "M3BS Advogados", "Nível de experiência = Não aplicável", "Tipo de emprego = Tempo integral", "Setores = Atividades jurídicas" (campos genéricos preenchidos pela integração inHire→LinkedIn). Candidaturas = contador exibido pelo LinkedIn (sinal de concorrência):
| Vaga | LinkedIn job ID / URL | Publicada (LinkedIn) | Candidaturas (13/10/2026) |
|---|---|---|---|
| Advogado(a) – Contencioso Cível Saúde Suplementar Massificado | 4473808622 — https://br.linkedin.com/jobs/view/4473808622 | 2026-10-02 ("Há 1 semana") | 65 candidaturas |
| Advogado(a) – Contencioso Cível Saúde Suplementar | 4446947676 — https://br.linkedin.com/jobs/view/4446947676 | 2026-07-30 ("Há 2 meses") | Mais de 200 candidaturas |
| Advogado(a) Sênior – Contencioso Cível Geral | 4475127898 — https://br.linkedin.com/jobs/view/4475127898 | 2026-10-06 ("Há 1 semana") | 113 candidaturas |
| Analista de Comunicação e Marketing | 4463899958 — https://br.linkedin.com/jobs/view/4463899958 | 2026-09-09 ("Há 1 mês") | Mais de 200 candidaturas |
| Advogado(a) Júnior – Processos Administrativos / Saúde Suplementar (ANS) | 4474653285 — https://br.linkedin.com/jobs/view/4474653285 | 2026-10-05 ("Há 1 semana") | Mais de 200 candidaturas |
| Advogado(a) Júnior – Regulatório Saúde Suplementar | 4471929719 — https://br.linkedin.com/jobs/view/4471929719 | 2026-09-29 ("Há 2 semanas") | Mais de 200 candidaturas |
| Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos | 4436830551 — https://br.linkedin.com/jobs/view/4436830551 | 2026-07-07 ("Há 3 meses") | Mais de 200 candidaturas |
| Advogado(a) Pleno – Contencioso Trabalhista | 4470734672 — https://br.linkedin.com/jobs/view/4470734672 | 2026-09-25 ("Há 2 semanas") | 132 candidaturas |
| Estágio em Direito – Área Trabalhista | 4475471411 — https://br.linkedin.com/jobs/view/4475471411 | 2026-10-07 ("Há 6 dias") | 41 candidaturas |
| Estágio – Contencioso Cível Geral | 4466811348 — https://br.linkedin.com/jobs/view/4466811348 | 2026-09-15 ("Há 4 semanas") | 75 candidaturas |
Leitura: vagas remotas (Júnior Regulatório/ANS) e as mais antigas já passaram de 200 candidaturas; as menos concorridas são Massificado (65), Estágio Trabalhista (41), Estágio Cível (75), Sênior Cível Geral (113) e Pleno Trabalhista (132). Candidatar-se cedo (vagas publicadas em outubro) e pelo inHire + contato direto com coordenador(a) é a via de maior retorno.

---- 7. AS MESMAS VAGAS NO INDEED (MCP oficial do Indeed, busca "M3BS advogados" Brasil, 13/10/2026) ----
Empresa aparece como "M3BS advogados". Todas as 10 listadas, sem salário ("Compensation: N/A"), datas iguais ao createdAt do inHire: Contencioso Cível Saúde Suplementar (30/07/2026); Massificado (02/10/2026); Sênior Cível Geral (06/10/2026); Pleno Recuperação de Crédito (07/07/2026); Estágio Trabalhista (07/10/2026, "Internship"); Analista Comunicação (09/09/2026); Estágio Cível Geral (15/09/2026, "Internship"); Júnior Processos Administrativos ANS (05/10/2026, "Remoto"); Júnior Regulatório (29/09/2026, "Remoto"); Pleno Trabalhista (não apareceu na busca Indeed por "M3BS" — a API inHire também não traz jobBoardsData.indeedATSIntegration para ela). Página da empresa no Indeed: https://br.indeed.com/cmp/M3bs-Advogados (dados do MCP: overallRating 5, culture 5, jobSecurity 5, management 5, workLife 5, compensation 5 — amostra pequena; interview difficulty "EASY", experience "EXCELLENT", processLength "TWO_WEEKS"; salarySatisfaction yes=3/no=0; salaryCostOfLiving yes=1/no=0; ceo_approval 100% (1 voto)).

---- 8. OUTROS BOARDS (13/10/2026) ----
- Talent.com (br.talent.com/jobs?k=M3BS): 1 resultado — "Analista de Comunicação e Marketing – M3Bs – Vaga São Paulo, SP" https://br.talent.com/view?id=636490163456509508 (JSON-LD: datePosted 2026-09-16, employmentType FULL_TIME, hiringOrganization "M3Bs"; logo via feed "inhire-ats"). Busca "M3BS advogados" em SP traz só ruído de outros escritórios.
- Catho (catho.com.br/vagas/?q=M3BS): "1 resultado" mas é falso positivo (BK Consultoria – Engenheiro AVEVA E3D). Nenhuma vaga M3BS na Catho.
- Empregos.com.br (/vagas/m3bs): 0 vagas. Jobrapido: 0 (ruído). NetVagas (netvagas.com.br/vagas/m3bs): 404 — apesar de "netVagas" constar em activeJobBoards, não há página pública indexável. Jooble: 403 (Cloudflare). InfoJobs: sem página de empresa M3BS (o "BS Advogados" do InfoJobs é outro escritório, de Porto Alegre). Vagas.com.br: sem empresa M3BS (não usa Vagas For Business).
- Glassdoor (E9182621): bloqueado por Cloudflare nesta sessão (curl 403, Playwright "Somente humanos", WebFetch 403). Via snippets de busca (Google): página de vagas https://www.glassdoor.com.br/Vagas/M3BS-Advogados-Vagas-E9182621.htm lista as vagas remotas "Advogado(a) Júnior – Processos Administrativos | Saúde Suplementar (ANS)" e "Advogado(a) Júnior – Regulatório Saúde Suplementar" e "Advogado(a) – Contencioso Cível Saúde Suplementar" (nota da empresa exibida: 3,0 no snippet de vagas / 3,5 na página de avaliações). Página de avaliações: https://www.glassdoor.com.br/Avalia%C3%A7%C3%B5es/M3BS-S%C3%A3o-Paulo-Avalia%C3%A7%C3%B5es-EI_IE9182621.0,4_IL.5,14_IC2479061.htm — 12 avaliações, nota 3,5, 61% recomendariam a um amigo; snippets: coordenador jurídico atual elogia "ambiente e salário, sem contras"; advogado júnior cita como prós "remuneração, local, oportunidades de casos e colegas" e como contras "desorganização, fofoca, benefícios abaixo, falta de transparência e sócios egocêntricos" (texto do snippet: "bom, porém desorganizado"); estagiário relata "falta de organização no financeiro, especialmente em relação ao VR/VT". Página de salários: https://www.glassdoor.com.br/Sal%C3%A1rio/M3BS-Sal%C3%A1rios-E9182621.htm — "26 salários de 19 cargos"; faixas (1–3 envios cada): Estagiário ≈ R$ 18 mil–21 mil/ano; Advogado Júnior R$ 30 mil–42 mil/ano; Advogado / Advogado Pleno R$ 60 mil–72 mil/ano; **Advogado Pleno III R$ 81 mil–88 mil/ano**; Assistente Administrativo R$ 31 mil–34 mil/ano; remuneração e benefícios avaliados em 3,7/5. (Confiança: provável — snippets de buscador, não a página.)
- devjobsscanner.com/company/m3bs-advogados/ (Cloudflare 403): snippet lista "Analista de Comunicação e Marketing — M3BS Advogados — São Paulo — via LinkedIn — 4 days ago".
- Wayback Machine (web.archive.org): bloqueado pela política de egress do ambiente — não foi possível recuperar versões antigas de m3bs.inhire.app/vagas.

---- 9. HISTÓRICO DE VAGAS ANTIGAS/FECHADAS (evidências encontradas) ----
H1) Indeed jk=fbf2f9ba176ecabc — "Advogado(a) Pleno - Saúde Suplementar e Regulatório ANS - São Paulo, SP" (M3Bs). Snippets Google (página exige login/Cloudflare): "Local: São Paulo/SP — 100% presencial"; "graduação em Direito com OAB ativa e pelo menos 3 anos de experiência em saúde suplementar/regulatório ANS"; atribuição citada: "Ministrar treinamentos internos, para operadoras-cliente e para o público em geral sobre temas regulatórios relevantes"; "foco em assessoria a operadoras de planos de saúde junto à ANS"; idade no snippet "165 dias" (≈ abril/maio 2026). Status: não está mais no inHire → fechada/preenchida. Confiança: provável.
H2) Indeed jk=36c669da948515c2 — "Advogado(a) Pleno – Contencioso Cível Geral" (M3Bs). Snippet: "Graduação completa em Direito; OAB ativa e regular"; campo de tipo marcado "estágio" por erro de indexação. Hoje a vaga equivalente aberta é "Sênior – Contencioso Cível Geral" (criada 06/10/2026) → indício de que o escritório subiu a senioridade da posição ou abriu nova. Confiança: provável.
H3) Indeed (snippet) — "Advogado(a) Pleno - Contencioso Cível com experiência em Saúde Suplementar Massificado, M3Bs, Remoto" — versão anterior (remota, pleno) da vaga hoje aberta "Advogado(a) – Contencioso Cível Saúde Suplementar Massificado" (híbrida, criada 02/10/2026). Confiança: provável.
H4) LinkedIn — Renata Mellim (Coordenadora do Contencioso Cível / "Renata Mellim - M3BS Advogados", https://www.linkedin.com/in/renata-mellim-5a4a3a96/) compartilhou vaga "Advogado(a) – Multidisciplinar Estratégico", M3BS Advogados, São Paulo (snippet: "há cerca de 2 semanas" na data da indexação; não está no inHire hoje). Confiança: provável. → Renata Mellim é uma das pessoas que divulgam vagas da área cível.
H5) LinkedIn — Marcelo Alves ("Marcelo Alves - Advogado", https://www.linkedin.com/in/marcelo-alves-00022527/) compartilhou anúncio do M3BS: "Advogado(a) Jr III e Pleno" — "Enviem seus currículos para rh@m3bs.com.br" com assunto "Contencioso de Volume - Saúde Suplementar" e, em outra vaga do mesmo anúncio, assunto "Contencioso Regulatório Especializado - ANS". Idade nos snippets: "3 anos" (um resultado) / "5 anos" (outro) → publicado entre 2021 e 2023, antes da adoção do inHire. Confiança: provável. → Confirma: (i) e-mail rh@m3bs.com.br era o canal de candidatura; (ii) níveis internos "Júnior III" e "Pleno" (e Glassdoor registra "Advogado Pleno III"), ou seja, escala Júnior I–III / Pleno I–III / Sênior; (iii) áreas que mais contratam: contencioso de volume (saúde suplementar) e contencioso regulatório ANS.
H6) Pietra Almeida (https://www.linkedin.com/in/pietrapalmeida/ — "Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados") — post sobre "seis meses de trabalho no escritório" (snippet). Indica contratação de júnior/estagiária em ciclo recente. Confiança: incerto (sem data).
H7) Vagas abertas em jul/2026 ainda no ar em out/2026 (Recuperação de Crédito, Contencioso Cível Saúde Suplementar) → posições de contratação contínua / difícil preenchimento.

Síntese das áreas que mais contratam (abertas + histórico): 1º Contencioso cível saúde suplementar (volume/massificado e estratégico) — ≥4 vagas distintas (2 abertas + H3 + H5); 2º Regulatório/ANS (NIP, processos administrativos, contencioso regulatório) — 2 abertas + H1 + H5; 3º Contencioso cível geral — 1 aberta + 1 estágio + H2; 4º Trabalhista — 1 pleno + 1 estágio (ambas de set/out 2026, área em expansão); 5º Recuperação de crédito/special situations — 1 (nova frente de negócios, jul/2026); 6º áreas de apoio (Comunicação/Marketing CLT). Não há vagas abertas ou históricas encontradas para tributário, societário, licitações/negócios públicos, compliance, direito médico ou Fortaleza/RJ.


---- 10. QUEM PUBLICA / CONDUZ AS VAGAS (RH e divulgadores) ----
- **Lucas Almeida — head de RH do M3BS** [CONFIRMADO — fonte primária do escritório]. Post do site "2º fase da nossa Academia de Líderes" (https://m3bs.com.br/2o-fase-da-nossa-academia-de-lideres/, publicado 2025-09-17, autora "Letícia", categoria Eventos): "Acreditamos que liderar é um aprendizado contínuo. Depois de três meses intensos de troca e desenvolvimento, iniciamos a segunda fase da nossa Academia de Líderes — agora conduzida pelo nosso head de RH, Lucas Almeida. Essa etapa dá continuidade a uma jornada que fortalece competências, amplia perspectivas e reforça o compromisso de sempre olhar para as pessoas. No M3BS, cada fase é um passo a mais na construção de uma cultura de liderança sólida, humana e orientada a resultados." É a ÚNICA menção nominal a RH em todo o site (1.248 posts varridos). Perfil LinkedIn NÃO localizado por buscadores (tentativas: "Lucas Almeida" M3BS RH; "Lucas Almeida" "M3BS Advogados" site:linkedin.com/in; "Lucas Almeida" "head de RH"). Programa interno: "Academia de Líderes" (1ª fase ≈ jun–set/2025; 2ª fase a partir de set/2025, conduzida pelo RH) — bom gancho para e-mail ao RH ("cultura de liderança sólida, humana e orientada a resultados", "olhar para as pessoas").
- Equipe de RH (sem nomes): a página de carreiras cita "Triagem pela equipe de Recursos Humanos" e "Entrevista técnica com Recursos Humanos"; o ATS inHire tem integração de agenda via Outlook e triagem com IA ("screeningWithAi") → o currículo deve conter as palavras-chave do anúncio literalmente.
- E-mail histórico de candidatura: **rh@m3bs.com.br** (anúncio compartilhado por Marcelo Alves no LinkedIn, 2021–2023, assuntos "Contencioso de Volume - Saúde Suplementar" e "Contencioso Regulatório Especializado - ANS"). Hoje a candidatura formal é pelo inHire; o e-mail rh@ permanece plausível como canal de contato direto (não confirmado se ativo).
- Divulgadores de vagas no LinkedIn (empregados que compartilham): **Renata Mellim** (Coordenadora do Contencioso Cível; compartilhou "Advogado(a) – Multidisciplinar Estratégico") e **Marcelo Alves** (advogado; compartilhou "Jr III e Pleno" com rh@m3bs.com.br). A página da empresa no LinkedIn (14.746 seguidores) NÃO publica posts de vaga nos 10 posts mais recentes (out/2026: DICOL/ANS, clipping diário, ConJur, Convenção Unimed, Academia M3BS) — as vagas aparecem apenas na aba "Vagas" (integração inHire). Nenhum post de vaga encontrado no Instagram @m3bsadvogados via buscadores (Instagram exige login; não renderizado).
- Entrevistador técnico: "Coordenador(a) responsável do setor jurídico" → para as vagas abertas, os coordenadores prováveis (fontes públicas já no contexto do dossiê): Contencioso cível saúde suplementar → Renata Mellim; Trabalhista → Amanda Valentim; Contencioso → Eric Andrade; jurídico/coordenação → Willian Silva; Controladoria Jurídica, Projetos e Inovação → Eduardo Kairalla. (Associação vaga↔coordenador é inferência, confiança: incerto, exceto Renata Mellim ↔ cível, provável.)
- Funcionários exibidos publicamente na página LinkedIn da empresa (13/10/2026): Alessandro Gama, Luis Henrique Borrozzino, Marina Modelski, Juliana Antonangeli (função não identificada; busca "Juliana Antonangeli" M3BS sem resultado).
- Página afiliada "M3BS Licita" (https://www.linkedin.com/company/m3bs-licita/): sem vagas e sem posts públicos.

---- 11. LACUNAS (procurado e não encontrado / não confirmado) ----
- Nome do(s) recrutador(es)/analistas de RH além do head Lucas Almeida (buscas: "M3BS" "Analista de Recursos Humanos"/"Business Partner"/"Recrutadora"/"Talent Acquisition"/"Gente e Gestão"/"Departamento Pessoal" + linkedin; nada).
- LinkedIn de Lucas Almeida (head de RH) — não localizado.
- Salários das vagas abertas: nenhum anúncio informa valor; o inHire pede "pretensão salarial" (associado/cooperado/CLT). Só há faixas do Glassdoor (26 salários, amostras de 1–3) via snippets.
- Histórico completo de vagas fechadas no inHire: a API pública só retorna vagas "published"; parâmetros status=closed/includeClosed ignorados; Wayback Machine bloqueado pelo proxy; Glassdoor/Indeed (páginas) bloqueados por Cloudflare/login — o histórico vem apenas de snippets (H1–H6).
- Posts de vaga no Instagram (@m3bsadvogados) e no feed da página LinkedIn: não encontrados (Instagram exige login; buscadores não indexam).
- Vagas em Fortaleza (filial) ou outras cidades: nenhuma (todas SP ou remoto BR).
- Vagas de tributário, societário, negócios públicos/licitações (M3BS Licita), compliance, direito médico, seguros, M&A, relações governamentais: nenhuma aberta ou histórica encontrada.
- Perguntas dissertativas de triagem/testes online no formulário inHire: não existem na etapa pública (só Sim/Não de disponibilidade + pretensão + LinkedIn + CV); a "prova prática ou estudo de caso" ocorre após as entrevistas e seu conteúdo não é público.
- Avaliações do Glassdoor na íntegra (12) e relatos de entrevista: inacessíveis (Cloudflare); apenas snippets.
- Catho "1 resultado" para M3BS é falso positivo; NetVagas sem página pública apesar de constar como board ativo.

---- 12. ARQUIVOS BRUTOS DESTA MODALIDADE ----
/tmp/claude-0/-home-user-meu-projeto/50b5810c-d50f-5f3d-bd42-04896c103073/scratchpad/findings/vagas_render/ : vagas_list.txt (listagem inHire renderizada), carreira_inhire.txt (página de carreiras renderizada), job_*.txt (10 páginas de vaga renderizadas com formulário), li_job_<id>.html (10 páginas LinkedIn guest), li_*.html (listagens LinkedIn), www_linkedin_com_company_m3bsadvogados_jobs_.html / lic_*.html (páginas públicas da empresa), board_*.html (Talent, Catho, Jobrapido, Empregos.com.br), talent_636490163456509508.html, catho_render.txt, glassdoor_jobs.txt (bloqueio Cloudflare), indeed_*.html (401), devjobsscanner.html (403), linktr_ee_M3BSAdvogados.html.
Também: /tmp/claude-0/-home-user-meu-projeto/50b5810c-d50f-5f3d-bd42-04896c103073/scratchpad/site/jobs/*.json (JSON completo de cada vaga) e jobs_list.json, inhire_tenant.json.
