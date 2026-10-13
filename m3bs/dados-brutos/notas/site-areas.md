# M3BS — Anotações brutas: modalidade "site-areas" (áreas de atuação, produtos e ferramentas do site)
Data da coleta: 2026-10-13. Método: curl (UA Chrome) + extração de texto com python3 -I. Todas as páginas abriram com HTTP 200 sem JS.
Arquivos brutos: findings/areas/*.html|txt (13 áreas + índice), findings/pages/*.html|txt (produtos, políticas, sitemaps), findings/responde/page-1..17 (FAQ completo), findings/posts/* (posts lidos), findings/cats/* (categorias do blog).

## 0. Fatos institucionais que aparecem em TODAS as páginas (rodapé/cabeçalho) — fonte: qualquer página do site, ex. https://m3bs.com.br/areas-de-atuacao/
- Tagline/slogan: "M3BS: Visão jurídica estratégica na saúde" (home) e "Visão jurídica estratégica na saúde." (rodapé).
- Sede: Avenida Paulista, 854 – 3º andar, Bela Vista – São Paulo/SP, CEP 01310-913. Acessos pedestres: Av. Paulista, 854 e Alameda Joaquim Eugênio de Lima, 424 (recepção). Estacionamento: Al. Joaquim Eugênio de Lima, 420/424 e Rua São Carlos do Pinhal, 241.
- Telefone 11 3115 2282; e-mail contato@m3bs.com.br (cabeçalho e página Contato). Rodapé traz erro de digitação "MBS3 © Todos os direitos reservados."
- Menu principal: O Escritório | Áreas de Atuação (13 subpáginas) | Profissionais | Notícias e Publicações | M3BS Responde | Jurisprudência (3 bases: "Jurisprudência em matéria de saúde suplementar", "Precedentes Regulatórios ANS", "Temas afetados pelo STJ/STF") | Chatbot | Contato.
- Rodapé "Mais Informações": Política de Privacidade, Política de Cookies, Código de Conduta (PDF https://m3bs.com.br/wp-content/uploads/2022/11/CODIGO-DE-CONDUTA-DO-M3BS-v.1.pdf), Contato. Redes: facebook.com/M3BSADV, linkedin.com/company/m3bsadvogados, instagram.com/m3bsadvogados.
- Newsletter: modal "Assine a Newsletter M3BS — Visão jurídica estratégica na saúde — Cadastre-se" (dados coletados: nome completo, e-mail, telefone, empresa; finalidade "envio de Newsletter e clippings").
- Site WordPress (tema "theme-m3bs", Elementor, Contact Form 7, Complianz cookies, The Events Calendar "tribe_events", Shield Security bloqueando REST). Fontes: EB Garamond + Montserrat.

## 1. Índice "Áreas de Atuação" — https://m3bs.com.br/areas-de-atuacao/ (texto literal)
"[H2] Áreas de Atuação
Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados atua na área de Direito Empresarial, com ênfase na assessoria a empresas e profissionais na área da Saúde privada.
Atualmente, se apresenta como um full service na área empresarial de Saúde, atuando para Operadoras de Planos de Saúde, Hospitais, Administradoras de Benefícios, Seguradoras, Centros Diagnósticos, Clínicas, Institutos de Saúde, Consultórios, Corretoras de Seguros e de Planos de Saúde, Médicos, Operadoras Odontológicas, Clínicas Odontológicas, Dentistas e demais profissionais da Saúde.
Confira nossas especialidades."
Ordem dos cards na home e no índice: Contencioso Regulatório, Regulatório, Direito Médico e Sanitário, Contencioso Judicial, Negócios Públicos, Governança Corporativa e Compliance, Societário, Relações de Trabalho, Consultivo Contratual, Tributário, Seguros, Relações Governamentais, Fusões e Aquisições.
OBS: nenhuma página de área cita sócio/advogado responsável (verificado no HTML — apenas o texto abaixo + cards "Outras áreas"). O mapeamento área→sócio vem da página Profissionais (seção 3).

## 2. As 13 páginas de área — TEXTO COMPLETO LITERAL (cada página tem só o título + 1–2 parágrafos; sem lista de serviços, sem nomes)
Todas em https://m3bs.com.br/areas-de-atuacao/<slug>/ ; og:type article; article:modified_time indicado.

### 2.1 Consultivo Contratual — /consultivo-contratual/ (modified 2023-02-09)
"Assessoria consultiva na definição estratégica, negociação, elaboração e análise contratual, no âmbito comercial e operacional. Revisão regulatória e elaboração de instrumentos jurídicos alinhados à regulamentação do setor."

### 2.2 Contencioso Judicial — /contencioso-judicial/ (modified 2024-01-29 — uma das 2 atualizadas em 2024)
Texto da página: "Gestão de carteira com ênfase na identificação de recorrência e causa raiz, buscando reduzir contingências e corrigir as eventuais não conformidades operacionais."
Texto do card (índice/outras áreas): "Atuação em carteira de ações judiciais e em casos estratégicos específicos, com abordagem alinhada a sua complexidade e particularidade."

### 2.3 Contencioso Regulatório — /contencioso-regulatorio/ (modified 2023-02-09)
"Atuação e gestão diferenciada e especializada em processos administrativos movidos pelo órgão regulador contra operadoras de planos de saúde, de forma estratégica com aplicação de visão do regulador, expertise de vivência no órgão regulador do escritório M3BS, para defesa da operadora frente à ANS."
(Jargão: "visão do regulador", "vivência no órgão regulador" — referência ao sócio Rogério Scarabel, ex-Diretor-Presidente substituto da ANS.)

### 2.4 Direito Médico e Sanitário — /direito-medico-e-sanitario/ (modified 2023-02-09)
"Atuação na representação de hospitais, clínicas, laboratórios e profissionais da saúde, no âmbito judicial, administrativo e de seus conselhos de classe.
Representação de empresas de prestação de serviços médicos junto a órgãos públicos na obtenção de autorizações legais."

### 2.5 Fusões e Aquisições — /fusoes-e-aquisicoes/ (modified 2023-02-09)
"Assessoria completa em operações de compra e venda de empresas, contemplando estruturação e reorganização societária, com abordagem multidisciplinar, regulatória e jurídica, para atendimento completo, eficiente e com soluções inovadoras de excelência reconhecida no mercado, oferecemos um atendimento completo e eficiente por meio de soluções especializadas e inovadoras."

### 2.6 Governança Corporativa e Compliance — /governanca-corporativa-e-compliance/ (modified 2023-02-09)
"Atuação multidisciplinar em Governança Corporativa, prestando consultoria na estruturação do sistema de direção, monitoramento e incentivo, convertendo princípios básicos em recomendações objetivas, alinhando interesses com a finalidade de preservar e otimizar o valor econômico de longo prazo da organização, facilitando seu acesso a recursos e contribuindo para a qualidade da gestão da organização, sua longevidade e o bem comum.
Desenvolvimento de programa de integridade, de acordo com a necessidade específica do cliente, com ênfase na gestão de riscos e no planejamento estratégico, abrangendo mapeamento e avaliação de riscos, adequação a leis, resoluções e normas, inclusive à Lei Geral de Proteção de Dados (LGPD) e à Normativa 518/2022 da Agência Nacional de Saúde Suplementar (ANS), criação de políticas e procedimentos internos, manuais e treinamento, além de consultoria na identificação e adoção de medidas reparatórias e de contingenciamento."

### 2.7 Negócios Públicos — /negocios-publicos/ (modified 2023-02-09)
"Atuação multidisciplinar em negócios públicos, prestando consultoria administrativa, judicial e estratégica, englobando análise de mercado, estruturação de canais de venda, relação governamental, capacitação e consultoria na captação de negócios, participação em licitação, prestação do serviço ou fornecimento."
(Ligado ao canal "M3BS Licita" — ver seção 5.)

### 2.8 Regulatório — /regulatorio/ (modified 2023-02-09)
"Assessoria regulatória multidisciplinar, com ênfase nas relações com a Agência Nacional de Saúde Suplementar (ANS) e Agência Nacional de Vigilância Sanitária (ANVISA)."

### 2.9 Relações de Trabalho — /relacoes-de-trabalho/ (modified 2024-01-29)
"Atuação na representação e defesa de empresas perante o Poder Judiciário, Ministério Público do Trabalho e Sindicatos.
Atuação consultiva patronal nas relações laborais entre empresas e seus colaboradores."

### 2.10 Relações Governamentais — /relacoes-governamentais/ (modified 2023-02-09)
"Acompanhamento de processos legislativos, da evolução legislativa e de reuniões colegiadas das agências reguladoras, emitindo parecer interpretativo; representação em audiências e consultas públicas, na elaboração de propostas, apresentação de considerações em procedimentos administrativos; assessoria jurídica-regulatória em pedidos de permissão e licenças administrativas; representação em ações judiciais, incluindo a revisão de regulamentação administrativa, contratos e atos ilegais do poder público"

### 2.11 Seguros — /seguros/ (modified 2023-02-09)
"Atuação na defesa dos interesses das seguradoras e resseguradoras, conforme as normas do setor, Código Civil e do Código de Defesa do Consumidor, em todos os tipos de apólices de seguro. Assessoria consultiva e jurídica nas diversas áreas envolvidas, com elaboração de pareceres, desenvolvimento de produtos e operações, e representação perante o judiciário e órgãos do poder, com especialistas no assunto e gerenciamento das demandas."

### 2.12 Societário — /societario/ (modified 2023-02-09)
"Atuação contenciosa estratégica em demandas que envolvem matéria societária, elém [sic] de consultoria especializada na criação e na implementação de estruturas societárias diversas, assessoria a investidores nacionais e estrangeiros, captação de recursos financeiros."
Card: "Atuação nas demandas judiciais e arbitrais relacionadas as relações societárias entre empresas e seus sócios."

### 2.13 Tributário — /tributario/ (modified 2023-02-09)
"Atuação judicial e extrajudicial visando redução de multas e passivo fiscal e tributário, de acordo com a necessidade específica do cliente."

### 2.14 Vocabulário/jargão recorrente nas áreas (para espelhar no currículo)
"full service na área empresarial de Saúde"; "operadoras de planos de saúde"; "visão do regulador"; "gestão de carteira"; "identificação de recorrência e causa raiz"; "reduzir contingências"; "não conformidades operacionais"; "assessoria regulatória multidisciplinar"; "ANS / ANVISA"; "programa de integridade"; "mapeamento e avaliação de riscos"; "RN 518/2022 (ANS)"; "LGPD"; "atuação consultiva patronal"; "defesa frente à ANS"; "processos administrativos movidos pelo órgão regulador"; "consultas públicas/audiências"; "reuniões colegiadas das agências" (DICOL); "estruturação e reorganização societária"; "soluções inovadoras"; "atendimento completo e eficiente"; "estratégico/estratégica" (palavra-chave da marca).
Vocabulário do blog/M3BS Responde: NIP, PAS (processo administrativo sancionador), DICOL, DIPRO, DIFIS, DIOPS, SIB, SIP, TISS, IDSS, IGR, PRASS, PLAEF, PAEF, TAOEF, TCAC, CBR/capital regulatório, ativos garantidores, provisões técnicas, PESL, PIC, Rol de Procedimentos, DUT, CPT/DLP, portabilidade, junta médica, ressarcimento ao SUS, garantia de atendimento (RN 566/2022), RN 623/2024, RN 593/2023, RN 489/2022 + RN 659/2025 (dosimetria de multas), RN 658/2025 (AFP – Ações de Fiscalização Planejada), RN 649/2025 (autogestões), RN 665/2026 (regiões de saúde), ADI 7.265 (extra-rol), Tema 1.309 STF (PIS/Cofins reservas técnicas), Reforma Tributária (CBS/IBS, DeRE, Decreto 12.955/2026), "judicialização extra-rol", "blindagem jurídica estruturada da carteira".

## 3. Página Profissionais — https://m3bs.com.br/profissionais/ (mapeamento sócio → áreas, texto literal dos modais)
Intro: "Com larga experiência jurídica e em gestão de equipes, sempre atentos aos progressos tecnológicos e às novas tendências do mercado global, os sócios de Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados estão presentes no dia-a-dia do escritório, com atuação direcionada ao cliente, que sempre recebe atendimento personalizado e eﬁcaz." Só os 5 sócios aparecem (nenhum associado/coordenador listado).
- Lucas Miglioli (Sócio): "Graduado em Direito em 1999. Pós-graduado (LLM) em Direito Empresarial pelo IBMEC, especialista em Direito Médico e da Saúde pela Universidade de Coimbra-PT e em Direito Processual Civil pela PUC-SP. Membro das Comissões Especiais de Estudos de Compliance; de Privacidade e Proteção de Dados; e de Direito Médico e de Saúde da OAB/SP e Coordenador do Grupo de Estudos de Compliance da Comissão de Direito Médico e da Saúde da OAB/SP, é autor de artigos jurídicos e palestrante. Responsável pelas áreas Direito Empresarial, Negócios Públicos, Governança, Compliance, Contencioso Especializado e Investimentos."
- Fernando Bianchi (Sócio): "Graduado em Direito em 1999. Pós-graduado em Direito Empresarial pela FGV, especialista em Direito Médico e da Saúde pela Universidade de Coimbra – PT, em Direito Processual Civil pela PUC-SP, em Direito Constitucional pela ESDC e Especialista em Direito Médico e de Planos de Saúde Privados. Membro da Comissão de Direito Médico e da Saúde da OAB/SP. Professor Universitário Licenciado de Processo Civil na Universidade de Guarulhos. Palestrante na área de Direito Médico e Planos de Saúde. Autor de artigos e estudos... Responsável pela área Médica e da Saúde."
- Luis Borrozzino (Sócio): "Graduado em Direito em 2006. Pós-graduado em Direito das Relações de Consumo pela PUC-SP e em Direito e Processo do Trabalho pelo Mackenzie, especialista em Direito Médico e da Saúde pela Universidade de Coimbra – PT. Membro das Comissões de Direito do Trabalho, de Direito Médico e de Saúde e da Comissão de Soluções Consensuais de Conflitos da OAB/SP. Membro da Associação dos Advogados Trabalhistas do Estado de São Paulo. Responsável pelas áreas de Direito do Trabalho, Direito do Consumidor e Recuperação de Crédito."
- Giuliano Bellinatti (Sócio): "Graduado em Direito em 2005 pela PUC-SP. Pós-graduado (LLM) em Direito Societário pelo INSPER. Especialista em Direito Médico e da Saúde pela Universidade de Coimbra – PT. Responsável pelas áreas de Contencioso Cível Especializado, Contratos e Direito Empresarial, com ênfase em Direito Societário." (Também é o contato LGPD — seção 7.)
- Rogério Scarabel (Sócio): "Atua no setor de Saúde desde 2004 e tem ampla experiência nos segmentos de Saúde Suplementar e Saúde Pública. Esteve à frente da ANS, de dezembro de 2019 à agosto de 2021, na condição de Diretor Presidente Substituto e como Diretor de Normas e Habilitação dos Produtos – DIPRO, no período de agosto de 2018 a agosto de 2021. Durante 14 anos, atuou como advogado na área de Direito da Saúde. Graduado em Direito pelo UNIVEM (Marília/SP). Especialização em Gestão Hospitalar e Organização da Saúde pela UFC e em Responsabilidade Civil e Direito do Consumidor pela Universidade de Fortaleza." (Sem linha "Responsável por"; na prática lidera Regulatório/Academia — ver posts.)

## 4. O Escritório — https://m3bs.com.br/o-escritorio/ (texto literal relevante)
"DNA M3BS — Em atividade desde 2009, Miglioli, Bianchi, Borrozzino, Bellinatti e Scarabel Advogados é uma sociedade de advogados constituída por proﬁssionais com ampla experiência no mercado, dedicada ao atendimento preventivo e contencioso de demandas jurídicas, em áreas diversas, a pessoas jurídicas e físicas, no Brasil e no exterior..."
"Diferencial: Atuação moderna, objetiva e precisa... tornam o escritório plataforma de negócios para clientes..."
"Princípios: Atuar com responsabilidade social...; Manter equipe atualizada e na vanguarda na área jurídica; Aplicar a melhor técnica...; Atender de forma ágil, eﬁciente e conﬁável..."
"Missão: Aprimorar o ecossistema de saúde brasileiro." "Visão: Ser referência jurídica no setor de saúde até 2025." "Valores: Conexão, Desenvolvimento de Pessoas, Diversidade, Foco no Cliente, Inovação, Integridade, Sustentabilidade."
"Estrutura: Localizado na Bela Vista... A sede é dotada de robusta e segura estrutura de TI... integralmente adequadas à legislação de proteção de dados. O M3BS conta com correspondentes em todos os Estados brasileiros."

## 5. PRODUTOS, CANAIS E FERRAMENTAS DE INOVAÇÃO (inventário)
### 5.1 M3BS Responde — https://m3bs.com.br/m3bs-responde/ (article:modified_time 2026-07-15; conteúdo ATUAL, cita RN 659/2025 em vigor desde 1º/5/2026 e RN 665/2026)
Texto: "Você gestor e técnico de operadoras de planos de saúde, tire suas dúvidas conosco! Temos um time de especialistas que podem te auxiliar." Formulário (CF7) + "Rol das principais dúvidas". 17 páginas (/m3bs-responde/page/2/ ... /page/17/), ~173 perguntas/respostas em formato FAQ, cada resposta termina com "O M3BS conta com equipe especializada em regulação da saúde suplementar... Quer saber mais? Entre em contato." ou "o M3BS recomenda...". Respostas com notas de rodapé citando RNs. Sem autor nominal nas respostas. E-mail do produto: m3bsresponde@m3bs.com.br (aparece nos posts de análise DICOL e nos eventos do calendário: "Contate-nos através do e-mail m3bsresponde@m3bs.com.br ou por telefone (11) 3115-2282").
Lista completa das perguntas (p1 = mais recentes) — ver anexo A no fim deste arquivo.
Temas mais recentes (p1): legitimidade de contratante em coletivo por adesão (RN 557/2022 + Entendimento DIFIS 02/2016); exclusão de beneficiário irrevogável (RN 561/2022); dosimetria de multas RN 489/2022 + RN 659/2025 (escalonamento 50% em 1/5/2026, 75% em 1/1/2027, 100% em 1/1/2028); Declaração de Saúde (RN 558/2022); TEA/CID F84 (RN 539/2022, Parecer Técnico 39/2024); RN 665/2026 regiões de saúde; seguro stop-loss (art. 35-M Lei 9.656); reembolso fora da rede (RN 566/2022); dependente nascido no exterior; recém-nascido/Súmula 25.

### 5.2 Chatbot — https://m3bs.com.br/chatbot/ (modified 2023-01-16)
Texto integral: "Esse é um canal de produção de conhecimento pra auxiliar o mercado sobre suas principais dúvidas." / "Estamos em manutenção do sistema para atualização e em breve retornaremos." — ou seja, FORA DO AR desde pelo menos jan/2023; sem iframe/embed de nenhum fornecedor.

### 5.3 E-book / Livro "O Aprimoramento do Ecossistema de Saúde Brasileiro" — https://m3bs.com.br/e-book/ (modified 2024-08-16)
Página = formulário de qualificação de lead (como conheceu o livro; motivo do interesse; interesse em eventos: webinars/workshops/palestras/conferências/networking; melhor horário; "principal interesse dentro do setor de saúde suplementar": Farmacêutico / Hospitais e Clínicas / Regulação e Políticas Públicas / Gestão de Planos de Saúde / Tecnologia e Inovação em Saúde / Atenção Domiciliar e Cuidados Continuados; segue LinkedIn/Instagram). A home diz "Acesse o link abaixo para fazer o download do nosso e-book — Clique aqui" (link para /e-book/). Nenhum PDF público localizado.
Post de lançamento (24/06/2024, https://m3bs.com.br/lancamento-do-livro-o-aprimoramento-do-ecossistema-de-saude-brasileiro/): "iniciativa do M3BS... prefácio de JOAO BARROCA... dividido em quatro grandes partes": (1) "Ecossistema de Saúde e como seus atores se articulam" — autores Paulo Rebello Filho, Marcus Vinicius Dias, Anderson Mendes, Renato Casarotti, Jamirson Avelar, Cassio Ide Alves, Lenise Barcellos de Mello Secchin, Ítalo Martins, Roberto Seme Cury, Paulo Marcos Senra Souza; (2) "Caminhos para a Gestão Estratégica dos Negócios" — Rogério Scarabel, Martha Oliveira, Maria Barreto, Carmen Ribeiro, Vanessa Teich, Farias Pereira de Sousa, Juliana Oliveira Domingues, Emanuele Pezati, Pietra Quinelato; (3) "Decisões Médicas e Empresariais Baseadas em Valor" — Fernando Bianchi, Clemente Nobrega, Adriano Londres, Medici Andre, César Luiz Abicalaffe, Clenio Schulze, Goldete Priszkulnik, Helena Maria Romcy; (4) "Novos Caminhos da Gestão" — Luis Henrique Borrozzino, Luiz Celso Dias Lopes, Carlito Marques, Tatiana Aranovich, Nathalia Pompeu, Vera Valente. "A publicação do Selo M3BS tem patrocínio da Libbs Farmacêutica e apoio institucional da Abramge, SINOG, UNIDAS Autogestão, IESS, CBEXS e Academia M3BS."

### 5.4 Podcasts — https://m3bs.com.br/podcast/ (modified 2024-06-11)
Quatro blocos (links para categorias do blog):
- "M3BS [Podcast]: Promovendo, de forma descomplicada, análises, debates instigantes, propostas para o setor, boas histórias e entrevistas exclusivas com os principais atores da saúde privada nacional." → /category/m3bs-podcast/ (só 2 posts: "Em breve: M3BS Podcast" 20/06/2023 e "Gravação do episódio piloto!" 22/06/2023 — "Lucas Miglioli, Fernando Bianchi, Luis Henrique Borrozzino, Giuliano Pretini Bellinatti e Rogério Scarabel inauguraram o estúdio M3BS").
- "Um podcast sobre Saúde Suplementar — Conhecimento, estratégia e saúde no mesmo lugar!" → /category/m3bs-ucast/ = M3BS UCA CAST (parceria com a UCA – Universidade Corporativa Abramge; 10 episódios out–dez/2022: 1º Paulo Rebello (presidente ANS), ... 7º Leandro Fonseca, 8º Roberto Seme Cury, 9º Luiz Paulo Tostes Coimbra, 10º Marcia Agosti).
- "O podcast oficial do Congresso Internacional UNIDAS — Conversando com os principais representantes das Autogestões" → /category/m3bs-talks-unidas/ = M3BS TALKS UNIDAS (47+ episódios gravados no 25º Congresso UNIDAS nov/2022 em Florianópolis e no 26º/27º/28º; convidados incluem sócios Fernando Bianchi, Giuliano Bellinatti, Lucas Miglioli, Luis Borrozzino, Rogério Scarabel e nomes como Leandro Karnal, Vera Valente, Nathalia Pompeu).
- "O podcast direto do 19ª SIMPLO — Conversando com os principais representantes das players do âmbito da Saúde Suplementar Odontológica" → /category/m3bs-podcast-simplo/ (entrevistas ago/2024; 19ª edição SIMPLO/SINOG).
- Home: "Minuto Regulatório M3BS — Análises, insights e debates sobre os conceitos, atualidades e perspectivas do mundo da Saúde Suplementar. Confira todos os episódios!" → Spotify https://open.spotify.com/show/6zNPBD1VunsFz9WulCzKEn . oEmbed/embed do Spotify: show "Minuto Regulatório M3BS", último episódio "Agenda Regulatória 2026" (2026-01-05, 3min54s, áudio). 
- Categoria /category/podcast/ = participações externas de sócios (ex.: "Os caminhos da saúde suplementar no Brasil: FIA | Diálogos ABIMED" 27/03/2026; "Rogério Scarabel no Videocast da ACB" 02/10/2024; "VBHCast" 05/09/2024; "Terapia CAR-T: podcast MIT Technology Review Brasil" 24/11/2023; "Rogério Scarabel estreia podcast Valor e Saúde" 26/06/2023).

### 5.5 Bases de "Jurisprudência" (3 produtos gated por formulário, mas o conteúdo abre sem login nas URLs "-pesquisa")
- Jurisprudência em matéria de saúde suplementar — https://m3bs.com.br/jurisprudencia-em-materia-de-saude-suplementar/ (modified 2024-07-30): "Rol de decisões judiciais tratando de matérias relacionadas a judicialização na saúde suplementar". 25 matérias: Carência; Co Participação; CPT/Doença Preexistente; Dano material contra operadora; Dano moral contra operadora; Telemedicina; Enunciados FONAJUS–CNJ; Fraudes Diversas; Judicialização de Multas/ANS; Judicialização do SUS/ANS; Lucro Cessante; Matérias em recurso repetitivo; Negativa de Cobertura (não previsto no Rol); Negativa por não cumprimento dos requisitos da Lei; Portabilidade; Rede: alteração sem aviso prévio; Reajuste anual individual; Reajuste coletivo; Reajuste coletivo por adesão; Reajuste faixa etária; Reembolso; Rescisão por fraude; Rescisão por inadimplência; "Responsabilidade Civil – erro médico – solidariedade (somente uma favorável, o tema já é sedimentado e contrário)"; "Ressarcimento ao SUS (não tem julgado favorável)". Modal: "Para acessar a página, preencha os dados abaixo". Conteúdo real em https://m3bs.com.br/jurisprudencia-em-materia-de-saude-suplementar-pesquisa/ (modified 2024-02): fichas com EMENTA + (Tribunal; processo; relator; órgão; datas) + "DESTAQUE DA JURISPRUDÊNCIA:" (comentário do escritório, viés pró-operadora). Entradas individuais (sitemap jurisprudencia-sitemap.xml, 26 itens, URLs /jurisprudencia-saude/<slug>/) assinadas pelo usuário "Letícia", datadas fev/2024 (ex.: https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-566-de29-12-22-lei-no-14-307-de-03-03-22/ — "Letícia, 14 fev de 2024").
- Precedentes Regulatórios ANS — https://m3bs.com.br/precedentes-regulatorios-ans/ (modified 2024-07-30): "Rol das principais decisões administrativas da ANS sobre matérias regulatórias". 8 categorias: Comunicados; Entendimentos da diretoria de fiscalização; Pareceres técnicos sobre temas de cobertura assistencial; Pareceres técnicos sobre temas econômico-financeiros; Resolução Administrativa – RA; RDC; Resolução CONSU; Súmulas Normativas. Conteúdo em /precedentes-regulatorios-ans-pesquisa/ (modified 2024-02-11): resumo + "Confira na íntegra acessando aqui". 93 entradas (precedente-sitemap.xml, URLs /precedentes-regulatorios-ans/<slug>/), autor "123esite" (conta da agência web), jan–fev/2024 (ex.: https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-11/ — "123esite, 24 jan de 2024").
- Temas afetados pelo STJ/STF — https://m3bs.com.br/temas-afetados-pelo-stj-stf/ (modified 2024-07-30): "Rol dos procecessos [sic] judiciais com materias afetadas nos Tribunais Superiores"; categorias STF e STJ. Conteúdo em /temas-afetados-pelo-stj-stf-pesquisa/: Súmulas STJ 597, 609, 608, 302; IAC 5; Temas Repetitivos 1123, 1034, 989, 610, 952, 1082, 1032, 1067, 990, 1069, 1047, 1016; STF ADI 7265, RE 948634 (Tema 123) etc. 22 entradas (temasafetadosstj-sitemap.xml, URLs /temas-afetados/<slug>/), autor "Letícia", mar/2024 (ex.: https://m3bs.com.br/temas-afetados/re-948634/ — "Letícia, 27 mar de 2024").
- Observação: as três bases foram montadas em jan–mar/2024 e as páginas-índice atualizadas em jul/2024; não há sinal de atualização posterior (ADI 7.265 de 2025/26 aparece só no blog).

### 5.6 Calendário Regulatório ANS — https://m3bs.com.br/calendario-regulatorio-ans/ (plugin The Events Calendar; eventos em /calendario-regulatorio/<slug>/)
Página mostra "35 eventos found" / "Não há eventos futuros" (visualizada em 13/10/2026). Últimos eventos: "DIOPS Mensal Simplificado – Outubro/2025" (30/11/2025), "SIP – 3º trimestre de 2025" (28/11/2025), "Padrão TISS competência 09/2025" (25/11/2025). Lista /calendario-regulatorio-ans/lista/ = "0 eventos found". Ou seja, o calendário cobre mar/2024 → nov/2025 e NÃO foi alimentado para 2026. Cada evento tem texto explicativo + CTA: "Tem dúvidas sobre o cumprimento dessa ou outra obrigação periódica? O M3BS possui um time de especialistas que pode atender à sua necessidade. Quer saber mais? Contate-nos através do e-mail m3bsresponde@m3bs.com.br ou por telefone (11) 3115-2282." Tipos de obrigação cobertos: SIB, SIP, DIOPS (trimestral/mensal simplificado), PPA (anexos I-IV), TISS, RPX/CNX, REA-Ouvidorias, relatório circunstanciado de auditoria, demonstrações financeiras.

### 5.7 Análises das Reuniões da DICOL (categoria "Reuniões DICOL", 16 páginas de posts) — produto editorial recorrente
Texto padrão (ex. https://m3bs.com.br/analise-da-644a-reuniao-da-diretoria-colegiada/ 09/10/2026): "O M3BS, com o compromisso de levar conhecimento regulatório aos seus clientes faz acompanhamento de todas as reuniões técnicas da ANS... o M3BS pontua sua análise, contendo: (i) sumário executivo e (ii) descrição aprofundada dos itens de pauta" + slides + "Nosso time de especialistas pode atender sua necessidade! Contate-nos através do e-mail m3bsresponde@m3bs.com.br ou por telefone (11) 3115-2282". Série vai da 584ª (2023) até a 644ª (09/10/2026) + reuniões extraordinárias (8ª, 10ª, 12ª de 2026).

### 5.8 Novidades ANS (categoria com 57 páginas) — clipping regulatório diário no site (ex.: "Padrão TISS ganha nova versão referente a setembro/2026" 07/10/2026; "Somatropina e cabozantinibe serão tema de audiência pública" 08/10/2026).

### 5.9 Academia M3BS (categoria "treinamentos" = "ACADEMIA M3BS", 18 páginas de posts)
Lançamento 27/02/2024 https://m3bs.com.br/academia-m3bs/: "apresentamos a Academia M3BS, um novo marco na excelência e inovação do setor da saúde suplementar... missão primordial a realização de pesquisa, estudos científicos, proposição de projetos, difusão de conhecimento e, acima de tudo, a capacitação de pessoas... parcerias estratégicas, colaborações com instituições acadêmicas..."
Post 29/05/2024 (Revista Insurance Corp com Lucas Miglioli e Fernando Bianchi): "A Academia M3BS é a consolidação de treinamentos acadêmicos e práticos, assim como do resultado de mesas redondas, discussão de análise de mercado, dinâmicas e de um programa interno de desenvolvimento de novos talentos, reciclagem e aperfeiçoamento".
Formatos: treinamentos regulatórios para clientes (in loco: Hapvida Fortaleza, Plena Saúde, Economus, Assefaz, Affix, Casembrapa, Unimed Jundiaí, Ipasgo), treinamentos internos (Processo Civil, coordenados por Alessandra Cherutti), "Treinamento Integrado" (reajuste, Rol, TGD), "Treinamento Contencioso" (série 2025–2026: internação psiquiátrica, descredenciamento, OPME/junta médica, medicamentos, produção probatória, execução), webinars (ADI 7.265 – 25/03/2026, 240+ participantes, com Clenio Schulze, Eric Andrade, mediação Rogério Scarabel), SUMMIT Academia M3BS (jun/2025 com Daniel Tostes – Procurador-Geral ANS, Juan Biazevic – TJSP, Fernando Bianchi, Breno Monteiro – CNSaúde; 2ª edição "SUMMIT Academia M3BS & Iter" 24/04/2026 em parceria com o Instituto Iter), "Academia de Líderes" (programa interno de liderança; 2ª fase 17/09/2025 "conduzida pelo nosso head de RH, Lucas Almeida"), workshop de IA no Ibmec para a liderança (01/07/2025). Treinamento mais recente: "Treinamento Estratégico de Contencioso Cível em Saúde" 06/10/2026 (VIII Jornada de Direito da Saúde) conduzido por Rogério Scarabel + "advogados especialistas Eric Andrade, Felipe Gomes e Abner Figueiredo".

### 5.10 COLLAB M3BS (categoria, 3 páginas) — "plataforma de comunicação criada para fomentar a inovação, o conhecimento e a troca de experiências" (post 16/03/2023). Eventos internos com colaboradores: Treinamento NIP (21/11/2022, "coordenadora da área do Regulatório, Marina Modelski"), Mulheres na Liderança (23/03/2023 com Vera Valente/FenaSaúde e Zélia Alves, no Ibmec), Marketing Pessoal com Núbia Tavares, Diversidade (30/08/2024, psicóloga Ester Meneses), Setembro Amarelo (13/09/2024, Ester Meneses).

### 5.11 M3BS Licita (categoria, 11 páginas; página afiliada no LinkedIn) — lançamento 28/07/2023 https://m3bs.com.br/m3bs-licita/: "nosso mais novo canal de informação, dedicado exclusivamente ao universo dos LEILÕES [sic]: O M3BS Licita! ... Informações atualizadas sobre negócios públicos, tanto licitações e contratações diretas, quanto dispensas; Dicas e estratégias...; Legislação e normativas explicadas..." Último post 30/04/2024 ("Visita a Phisalia!"). Ligado à área Negócios Públicos (Lucas Miglioli ministrou curso sobre a Lei 14.133/2021; palestra na Mapfre).

### 5.12 Esporte + Vida (categoria) — projeto lançado 16/11/2023: "inauguramos o Tatame M3BS... apoio à equipe Guigo Jiu-jitsu"; aulas de defesa pessoal, yoga (12/04/2024). Último post abr/2024.

### 5.13 M3BS Institucional / Desenvolvimento Organizacional — post 03/08/2023: palestra de Marcelo Rivani (FGV/Ibmec) sobre DHO; "investir no Desenvolvimento Organizacional é despertar o potencial dos colaboradores, gerando o fortalecimento da cultura de inovação e aprendizado contínuo". "Projetos M3BS 2023✨" (29/12/2023): "O M3BS fomentou diversos projetos inovadores que marcaram a saúde privada em 2023! De canais interativos a diálogos com os principais nomes do setor".

### 5.14 Outros "produtos"/ofertas vistos no blog
- "M3BS Descomplica" (hashtag; 15/09/2023): tabelas comparativas sobre alteração de rede hospitalar / RN 585.
- Solução ADI 7.265 (23/02/2026, https://m3bs.com.br/adi-7-265-no-stf-precedente-estrategico-para-a-judicializacao-extra-rol/): "M3BS GARANTE NO STF APLICAÇÃO DA ADI 7.265... o M3BS estruturou solução específica para operadoras: diagnóstico da carteira judicial extra-rol; identificação de casos com potencial de reversão no STF; padronização de protocolo interno com base na ADI 7.265; atuação direcionada em Reclamações Constitucionais; construção de precedentes estruturantes; monitoramento contínuo de julgamentos correlatos... blindagem jurídica estruturada da carteira extra-rol."
- Parceria SINOG (26/05/2026): "Programa de Adequação Prática ao Novo Modelo de Fiscalização da ANS"; entregas: "apoio jurídico em temas regulatórios e tributários, produção conjunta de conteúdo técnico, capacitação"; temas: adequação ao novo modelo de fiscalização, governança e segurança regulatória, capacitação de equipes, mapeamento de vulnerabilidades e riscos, soluções jurídico-tributárias.
- Reforma Tributária para saúde: artigos "DeRE e Reforma Tributária na Saúde Suplementar" (03/03/2026), "Reforma Tributária: A regulamentação da CBS e o risco oculto para cooperativas médicas e odontológicas" (01/09/2026, "Escrito por: Lucas Bianchi, coordenador tributário e Caio Azevedo, advogado tributário do M3BS"), ConJur "STF afasta PIS e Cofins sobre reservas técnicas" (02/10/2026, Lucas Bianchi e Caio Azevedo).
- Vídeo institucional: https://m3bs.com.br/wp-content/themes/theme-m3bs/assets/videos/video-institucional1.mp4 (home).
- Categorias do blog (category-sitemap.xml): treinamentos (ACADEMIA M3BS), artigo, collab-m3bs, esporte-vida, eventos (33 pág.), institucional, judicializacao, m3bs-licita, m3bs-podcast, m3bs-podcast-simplo, m3bs-talks-unidas (15 pág.), m3bs-ucast, na-midia (42 pág.), novidades-ans (57 pág.), palestras (15 pág.), podcast, reunioes-dicol (16 pág.), tributario, uncategorized. Blog com 208 páginas de posts; arquivos mensais contínuos até out/2026. Autores do site (author-sitemap.xml): "Letícia" (/author/leticia/ — assina praticamente todos os posts 2022→2026) e "Imprensa M3BS" (/author/imprensa-m3bs/ — posts de jun/2022); conta técnica "123esite".

## 6. Políticas — nomes, e-mails, CNPJ, endereços
### 6.1 Política de Privacidade — https://m3bs.com.br/politica-de-privacidade/ (modified 2023-09-06) — TEXTO LITERAL dos trechos-chave
"1. INTRODUÇÃO — Por este documento, o MIGLIOLI, BIANCHI, BORROZZINO, BELLINATTI E SCARABEL ADVOGADOS ("M3BS"), pessoa jurídica de direito privado, inscrito no CNPJ/MF sob o nº 07.848.463/0001-57, com sede na Alameda Jaú, 1.754, 8 e 11º andares, Jardim Paulista, CEP 01420-002, São Paulo/SP..." (endereço ANTIGO ainda na política).
"3.1. O M3BS tratará os dados pessoais de seus usuários na prestação de serviços integrados de saúde, incluindo... manter o sigilo e segurança dos dados coletados na atividade de prestação de serviços médicos" (texto aparentemente adaptado de modelo de prestador de saúde).
"4.2. ...poderá compartilhar os dados pessoais... entre seus colaboradores, departamentos, parceiros, conselho de classes, instituições médicas, profissionais de saúde e correlatos, laboratórios e operadoras de planos de saúde".
"5.5. No ambiente do M3BS, os dados são acessados somente por profissionais autorizados, como, mas não apenas, sócios, empregados, associados e colaboradores."
"5.7. Qualquer suspeita de acesso indevido, perda, roubo, desvio ou comprometimento de dados, deverá ser reportada ao M3BS, na pessoa do sócio Giuliano Bellinatti, através do telefone (11) 3115-2282 ou do e-mail (giuliano@m3bs.com.br)."
"6.2. Os pedidos deverão ser encaminhados a Giuliano Bellinatti, através do telefone (11) 3115-2282 ou do e-mail (giuliano@m3bs.com.br)."
"7.2. Qualquer dúvida relativa às disposições desta política, poderão ser direcionadas ao sócio, Giuliano Bellinatti..."
"8.1. ...Foro da Comarca de São Paulo/SP".
=> Não há a palavra "Encarregado"/"DPO"; o papel de contato LGPD é exercido pelo sócio Giuliano Bellinatti (giuliano@m3bs.com.br). Padrão de e-mail inferido: primeironome@m3bs.com.br (confirmado apenas para giuliano@).

### 6.2 Política de Privacidade e Proteção de Dados Pessoais (termo da newsletter) — https://m3bs.com.br/politica-de-privacidade-e-protecao-de-dados-pessoais/
"Os dados pessoais coletados são os seguintes: nome completo, endereço de e-mail, telefone e nome da empresa; A finalidade da coleta é o envio de Newsletter e clippings; ... A qualquer momento você poderá entrar em contato através do e-mail m3bsadvogados@m3bs.com.br para exercer seus direitos relacionados à proteção de dados pessoais..."

### 6.3 Política de Cookies — https://m3bs.com.br/politica-de-cookies/ ("atualizada pela última vez em outubro 31, 2023"; gerada pelo Complianz). Serviços: WordPress, Google Fonts, Google reCAPTCHA, YouTube, Facebook, WhatsApp. Sem nomes/e-mails.

### 6.4 Código de Conduta (PDF v.1, nov/2022; texto em site/codigo-conduta.txt)
"O Miglioli, Bianchi, Borrozzino, Bellinatti & Scarabel Advogados ("M3BS") tem a missão de aprimorar o ecossistema de saúde brasileiro, pautando sua atuação de acordo com seus valores: integridade, sustentabilidade, diversidade, inovação, conexão, desenvolvimento de pessoas e foco no cliente... fundamento... no Código de Ética e Disciplina da OAB, Estatuto da Advocacia (Lei 8.906/1994) e na Lei da Empresa Limpa (Lei 12.846/2013)... Qualquer violação deve ser reportada ao canal de denúncia etica@m3bs.com.br." Assinado: Lucas Miglioli, Fernando Bianchi, Luis Borrozzino, Giuliano Bellinatti, Rogério Scarabel. "Leia o Código com atenção. Se tiver dúvidas, consulte seu gestor." "Canal de Ética: etica@m3bs.com.br" (anônimo, confidencial, sem retaliação). Termos usados para pessoas: "associados e colaboradores".

## 7. Pessoas/cargos que apareceram incidentalmente nas páginas desta modalidade (com data mais recente)
- Lucas Almeida — "head de RH" (post 17/09/2025 https://m3bs.com.br/2o-fase-da-nossa-academia-de-lideres/: "segunda fase da nossa Academia de Líderes — agora conduzida pelo nosso head de RH, Lucas Almeida"). ATUAL (provável).
- Lucas (Bellinatti) Bianchi — "coordenador tributário do M3BS" (21/07/2026), "Lucas Bellinatti Bianchi, coordenador da área tributária" (22/07/2026), "advogado e coordenador das áreas Fiscal Consultiva e Contenciosa do M3BS Advogados" (15/09/2026), "coordenador da área Tributária" (08/10/2026). ATUAL.
- Caio Azevedo — "advogado tributário do M3BS" (01/09/2026; coautor ConJur 02/10/2026). ATUAL.
- Eric Andrade — "especialista em saúde suplementar" (webinar 25/03/2026); "advogados especialistas Eric Andrade, Felipe Gomes e Abner Figueiredo" (06/10/2026, contencioso cível saúde). ATUAIS.
- Marina Modelski — "coordenadora da área do Regulatório" (21/11/2022); "advogada do M3BS Advogados... docente no curso Imersão Regulatória (UCA), módulo NIP" (06/08/2024); destaque com Rogério Scarabel em matéria dos 20 anos do IESS (24/09/2026). ATUAL.
- Renata Mellim — "Coordenadora do Contencioso Cível" (14/08/2025, AB2L Lawtech Conference). ATUAL (provável).
- Eduardo Kairalla — "Coordenador da Controladoria" (14/08/2025). ATUAL (provável).
- Alessandra Cherutti (@alecherutti) — "coordenadora de Contencioso Cível Saúde" (04 e 06/02/2025). ATUAL (provável).
- Pâmela Sposito ("Pamela Reis" no título do post) — "advogada... consultora de assuntos regulatórios do M3BS" (12/07/2023 e 21/08/2023). Status atual desconhecido (último registro 2023).
- Sócios: Rogério Scarabel e Fernando Bianchi (55ª Convenção Unimed, 08/10/2026); Lucas Miglioli (almoço Eliane Medeiros 31/08/2026; lançamento livro 27/03/2026); Luis Henrique Borrozzino (TV Câmara Campinas, 07/01/2026; escala 6x1); Giuliano Bellinatti (AB2L 14/08/2025; contato LGPD).

## 8. Vagas abertas no inHire (contexto; lista já baixada em site/jobs_list.json — 10 vagas, todas "published")
URL base: https://m3bs.inhire.app/vagas ; IDs: Advogado Pleno – Recuperação de Crédito e Aquisição Estratégica de Créditos (cccb84e1-daae-4702-a39d-88bcfdb0321a, Hybrid SP); Advogado(a) – Contencioso Cível Saúde Suplementar (27dcffce-61e2-4c16-be1d-d8a16f532fed, Hybrid SP); Advogado(a) Júnior – Processos Administrativos | Saúde Suplementar (ANS) (e3103725-0afb-4ef8-8b63-239e465e8ce1, Remote BR); Advogado(a) Júnior – Regulatório Saúde Suplementar (7ead6544-fed6-4943-b660-587c63834865, Remote BR); Advogado(a) Pleno – Contencioso Trabalhista (fff14670-f04c-4057-9aab-af089ceb4760, Hybrid SP); Advogado(a) Sênior – Contencioso Cível Geral (3dc83622-65ed-4767-a123-3ebcd8434044, Hybrid SP); Advogado(a) – Contencioso Cível Saúde Suplementar Massificado (9e59208d-e92a-4311-8a44-a66f2d0985e5, Hybrid SP); Analista de Comunicação e Marketing (a3e12a90-1819-4bd6-ba15-8211bac9a96d, On-site SP); Estágio em Direito – Área Trabalhista (9919e925-2847-4e5d-a4a5-77a06a50f342, On-site); Estágio – Contencioso Cível Geral (ad9afe67-5986-4559-8f6f-3ca5198d5eed, On-site). Job boards ativos no tenant: indeedATSIntegration, linkedin, netVagas, jobBoardPool, talent. Mapeamento vaga→área do site: Contencioso Cível Saúde (Renata Mellim / Alessandra Cherutti / Giuliano Bellinatti), Regulatório e Processos Administrativos ANS (Marina Modelski / Rogério Scarabel), Trabalhista (Luis Borrozzino; coordenadora Amanda Valentim segundo contexto), Recuperação de Crédito (área de Luis Borrozzino na bio).

## ANEXO A — Todas as perguntas do M3BS Responde (p1 = mais recente; fonte https://m3bs.com.br/m3bs-responde/page/N/)
[p1]  Uma associação criada para oferecer benefícios como plano de saúde, seguro de vida e assistência pet pode contratar um plano coletivo por adesão? 
[p1]  O beneficiário que solicitou sua própria exclusão de um contrato coletivo por adesão pode se arrepender e cancelar o pedido? 
[p1]  Como a ANS calcula o valor das multas aplicadas às operadoras? 
[p1]  A Declaração de Saúde deve ter um número mínimo de perguntas? 
[p1]  A cobertura de terapias para pacientes com TEA pelos planos de saúde é irrestrita? 
[p1]  A RN/ANS nº 665/2026 altera a área de abrangência da operadora? 
[p1]  A Operadora pode contratar um seguro para cobrir internações de alto valor? 
[p1]  A operadora é obrigada a reembolsar despesas quando o beneficiário opta por atendimento fora da rede credenciada por iniciativa própria? 
[p1]  Dependente nascido no exterior pode ser incluído no plano de saúde? 
[p1]  Parto fora da rede impede a inclusão do recém-nascido no plano? 
[p2]  É válida a solicitação de cancelamento de contrato coletivo empresarial feita por terceiro sem comprovação de poderes de representação? 
[p2]  É possível transferir um beneficiário entre contratos coletivos empresariais da mesma empresa (matriz e filial) sem alterar o vínculo empregatício? 
[p2]  A operadora pode utilizar ferramentas tecnológicas para triagem e priorização de pedidos médicos? 
[p2]  A operadora pode substituir um hospital descredenciado por qualquer outro prestador da rede? 
[p2]  Atendimentos realizados por psicopedagogo sem habilitação como profissional de saúde possuem cobertura obrigatória? 
[p2]  Exames laboratoriais prescritos por cirurgião-dentista devem ser cobertos por plano exclusivamente médico-hospitalar? 
[p2]  A operadora pode exigir coparticipação no momento da realização do procedimento? 
[p2]  O descumprimento contratual do beneficiário pode justificar limitação assistencial? 
[p2]  O que mudará com relação ao pagamento de multas com desconto a partir da entrada em vigor da RN/ANS 657/25? 
[p2]  Como funciona o escalonamento temporal das multas conforme a RN/ANS 659/25? 
[p3]  Qual é o objetivo das Ações de Fiscalização Planejada (AFP) instituídas pela Resolução Normativa ANS nº 658/2025, quais princípios orientam a sua aplicação e quais são os efeitos jurídicos para as operadoras de planos de saúde, especialmente quanto às obrigações impostas e à possibilidade — ou não — de adesão voluntária? 
[p3]  A Operadora é obrigada a remover o beneficiário que estiver internado em hospital do SUS ou não credenciado à Operadora e localizado fora da área de abrangência do produto, para hospital credenciado dentro da área de abrangência do produto? 
[p3]  Como é calculado o capital necessário para constituir uma operadora de saúde? 
[p3]  Como saber se a operadora é obrigada a enviar o DIOPS mensal? 
[p3]  A Operadora pode determinar o tempo de duração do atendimento/sessão realizado pelo prestador? 
[p3]  Se o home care substitui a internação hospitalar, o plano de saúde também deve cobrir os insumos necessários ao tratamento? 
[p3]  A decisão do STF que proíbe o reajuste de planos de saúde por faixa etária para maiores de 60 anos ainda está valendo? 
[p3]  Durante um processo de incorporação societária, um hospital teve o CNPJ e o CNES alterados. A operadora pode atualizar a rede assistencial e manter o contrato ativo apenas com base na nova documentação societária (Ata e CNPJ)? 
[p3]  Qual a periodicidade do rodízio de auditores independentes e a sanção prevista se não observada? 
[p3]  Sua equipe conhece todas as dispensas, prazos e obrigações previstos na RN nº 527/2022? 
[p4]  É possível cobrar coparticipação sobre administração de medicamentos no âmbito da internação hospitalar? 
[p4]  Qual é o procedimento para realizar o resgate do valor excedente aplicado na Conta Garantia da ANS? É necessário comunicar previamente a ANS? 
[p4]  Você sabe quais são os impactos da RN nº 527/2022 no envio do DIOPS/ANS da sua operadora? 
[p4]  Como deve ser registrado no padrão TISS o atendimento eventual de um beneficiário realizado por prestador não credenciado, sem inclusão no RPS da operadora? 
[p4]  Como a ANS vai acompanhar a assistência prestada aos beneficiários com o fim do SIP? 
[p4]  A norma (IN nº 36) que trata do Monitoramento da Garantia de Atendimento foi suspensa? 
[p4]  O que a Operadora precisa providenciar para fazer jus à utilização de Fatores Reduzidos para Cálculo do Capital Regulatório? 
[p4]  Houve alguma alteração nos prazos máximos de garantia de atendimento após a publicação da RN/ANS nº 623/2024? 
[p4] Então, o que mudou com a RN/ANS nº 623/2024?
[p4]  O que mudou, na prática, para as operadoras com os ajustes nas metas de IGR Trimestral? 
[p5]  Houve alguma alteração no Rol de Procedimentos e Eventos em Saúde da ANS com relação ao rastreamento individualizado de câncer de mama (mamografia) para mulheres na faixa etária de 40 a 74 anos? 
[p5]  Quais são os critérios de equivalência exigidos pela ANS para a substituição de prestadores hospitalares, conforme a RN nº 585/2023? 
[p5]  Quais cuidados a operadora deve adotar para evitar autuações da ANS e prejuízos operacionais na condução de juntas médicas? 
[p5]  Com a revogação da RN 551/22, quais cuidados a operadora deve manter para garantir governança assistencial e evitar riscos regulatórios? 
[p5]  Quais são os novos requisitos de governança, para que uma operadora seja reconhecida no Programa de Acreditação? 
[p5]  Como a Pesquisa de Satisfação de Beneficiários impacta a pontuação da operadora no IDSS? 
[p5]  A área de comercialização de um produto pode ultrapassar a área de abrangência registrada? 
[p5]  Quais são os meios de comunicação aceitos pela ANS, para fins de comunicação de inadimplência e protocolos de atendimento? 
[p5]  A RN 623 exige que as operadoras disponibilizem atendimento presencial em todas as localidades? 
[p5]  Como a operadora pode transformar a ouvidoria em uma ferramenta de proteção regulatória e melhoria da gestão? 
[p6]  De que forma as operadoras podem se preparar para o acompanhamento econômico-financeiro da ANS e evitar enquadramentos que comprometam sua operação? 
[p6]  Como a operadora pode estruturar fluxos seguros para tratar pedidos de cancelamento e exclusão de beneficiários, evitando riscos regulatórios e perdas financeiras? 
[p6]  Junta médica como mecanismo de regulação assistencial. Você sabe como conduzir? 
[p6]  Como garantir a adequada gestão dos ativos garantidores, evitando penalidades e fortalecendo a sustentabilidade financeira da operadora? 
[p6]  Como as operadoras podem aprimorar o atendimento aos beneficiários, evitando desperdícios operacionais e assegurando a conformidade regulatória? 
[p6]  Como o Plano de Recuperação Assistencial (PRASS) pode evitar penalidades e garantir a continuidade das operações? 
[p6]  Como garantir que a operadora esteja em conformidade com a cobertura mínima obrigatória do Rol de Procedimentos da ANS, evitando desperdícios e oferecendo um atendimento seguro e sustentável? 
[p6]  Como a implementação de processos internos de governança e compliance contribui para a regularidade e sustentabilidade das entidades de autogestão perante a ANS? 
[p6]  Qual a importância da revisão contratual contínua para operadoras de planos de saúde? 
[p6]  Como a estruturação de processos e fluxos internos pode contribuir para a regularidade e sustentabilidade das operadoras de planos de saúde? 
[p7]  Qual a importância da classificação prudencial da operadora para a gestão e conformidade regulatória? 
[p7]  Indisponibilidade ou inexistência de prestadores na rede assistencial? Qual a melhor forma de garantir a assistência ao beneficiário e manter a sustentabilidade do produto? 
[p7]  Como as operadoras de planos de saúde podem otimizar o fluxo de reembolso visando o combate às fraudes dessas solicitações? 
[p7]  As operadoras de planos de saúde são obrigadas a cobrir atendimentos realizados por telemedicina? 
[p7]  Existe prazo para cobrança de coparticipação? 
[p7]  A operadora de planos de saúde é obrigada a ofertar o pagamento das mensalidades via cartão de crédito? 
[p7]  A operadora é obrigada a fornecer plano continuidade aos beneficiários demitidos e aposentados? 
[p7]  Os contratos de planos de saúde possuem cláusulas obrigatórias? 
[p7]  As operadoras de planos de saúde são obrigadas a aderir às práticas de gestão de riscos e controles internos? 
[p7]  Se decretado regime de Direção Fiscal pela ANS, o Administrador de uma operadora de planos de saúde é automaticamente afastado da gestão? 
[p8]  Existe limite de aplicação de imóveis assistenciais para fins de ativos garantidores de uma operadora de planos de saúde? 
[p8]  As Administradoras de Benefícios deverão observar a RN 593/23? 
[p8]  A operadora de planos de saúde é sempre obrigada a substituir prestadores não hospitalares? 
[p8]  As operadoras são obrigadas a garantir assistência domiciliar? 
[p8]  Qual a data-base que a Operadora deverá considerar para a aplicação do reajuste anual? 
[p8]  Quais informações sobre a rede de prestadores a que os beneficiários precisam ter acesso no site da operadora? 
[p8]  Quais são os fluxos e indicadores analisados pela ANS que sugerem anormalidades administrativas graves de natureza assistencial para que seja instaurado o PRASS? 
[p8]  Quando recepcionada a cobrança de Ressarcimento ao SUS, a operadora é obrigada a impugná-la? 
[p8]  Sempre que realizada uma alteração nos dados cadastrais de uma operadora de planos de saúde, será obrigatória a comunicação à ANS? 
[p8]  A operadora de planos de saúde pode rescindir um contrato coletivo de forma imotivada? 
[p9]  De que forma a operadora de planos de saúde deve realizar a cobrança de coparticipação? 
[p9]  A operadora de planos de saúde é obrigada a manter um prestador hospitalar de preferência de seus beneficiários? 
[p9]  Quais os meios de notificação são admitidos pela ANS para fins de comunicação de inadimplência? 
[p9]  Margem de solvência ou Capital Baseado em Risco, o que uma operadora de planos de saúde deverá observar? 
[p9]  O que é e para o que serve o plano de contas padrão da ANS? 
[p9]  A operadora de planos de saúde pode vender sua carteira de beneficiários? 
[p9]  O que é PESL? 
[p9]  O que é PIC? 
[p9]  O que são provisões técnicas de uma operadora de planos de saúde e quais são os seus tipos? 
[p9]  Qual a diferença entre capital regulatório, capital base e capital baseado em risco de uma operadora de planos de saúde? 
[p10]  Qual a diferença de ativo garantidor vinculado e cetipado? 
[p10]  Qual é a aplicação de um TAOEF e suas consequências? 
[p10]  A operadora de planos de saúde que estiver cumprindo plano de adequação econômico-financeira (PLAEF) pode solicitar seu encerramento antes do prazo final de vigência? 
[p10]  É possível a utilização de imóveis para compor o lastro de provisões técnicas das operadoras de planos de saúde junto à ANS? 
[p10]  A assinatura de um Termo de Compromisso de Ajuste de Conduta (TCAC) será considerada confissão de infração perante a ANS? 
[p10]  Quais as consequências em caso de descumprimento do TCAC? 
[p10]  É possível firmar um TCAC para solução de demandas NIPS junto à ANS? 
[p10]  Quais são os requisitos para celebração do TCAC? 
[p10]  O que é um Termo de Compromisso de Ajuste de Conduta (TCAC) perante a ANS? 
[p10]  Existem requisitos para que a execução de um Plano de Recuperação Assistencial (PRASS) seja aprovada? 
[p11]  O regime especial de Direção Técnica pode ser instaurado mais de uma vez pela ANS? 
[p11]  Como é realizada a apuração do Capital Baseado em Risco (CBR) de uma operadora de planos de saúde? 
[p11]  As operadoras de planos de saúde são sempre obrigadas a utilizar uma “Central de Custódia” em relação aos ativos garantidores? 
[p11]  Qual a função da formação do “capital regulatório” por uma operadora de planos de saúde? 
[p11]  Se a operadora de planos de saúde vinculou ativos garantidores junto à ANS, além do montante obrigatório, poderá reaver o valor em excesso? 
[p11] Diante da vinculação junto à ANS, é possível que a operadora exceda o valor de constituição obrigatório. Nesses casos, a operadora pode solicitar a movimentação dos ativos excedentes?
[p11]  Qual a diferença entre encerramento e cancelamento do Plano de Adequação Econômico-Financeira – PLAEF? 
[p11]  Em caso de constatação de anormalidades econômico-financeiras em uma operadora de planos de saúde, será instaurado imediatamente regime direção fiscal pela ANS? 
[p11]  A operadora de planos de saúde é obrigada a substituir um prestador não hospitalar, quando proceder com a sua exclusão, mesmo quando já possuir em sua rede assistencial, outro prestador equivalente ou superior? 
[p11]  A operadora de planos de saúde pode ofertar negociação ou parcelamento de débitos de mensalidades aos seus beneficiários? 
[p11]  Qual o prazo correto para início do envio DIOPS Mensal para as operadoras de planos de saúde enquadradas nos segmentos de classificação prudencial S1 e S2? 
[p12]  Com o cancelamento da Súmula nº 28 da ANS que previa a possibilidade de notificação de inadimplência por edital, as operadoras de planos de saúde poderão rescindir o contrato de forma tácita? 
[p12]  Qual o momento ideal para oferta de cobertura parcial temporária (CPT) em caso de doença ou lesão preexistente? 
[p12]  O plano de saúde sempre terá a vigência iniciada a partir da assinatura da proposta de adesão? 
[p12]  Quando o registro de um plano de saúde tem como área de abrangência “grupo de municípios” a operadora deverá vincular um hospital para cada município indicado no registro? 
[p12]  O reembolso de despesas ou atendimentos médicos é sempre obrigatório para operadoras de planos de saúde? 
[p12]  É possível registrar novos produtos na ANS quando a operadora de planos de saúde estiver em período de suspensão de comercialização? 
[p12]  A solicitação de medicamento antineoplásico deve ser atendida de forma imediata pelas operadoras de planos de saúde? 
[p12]  O que a ANS considera como “encerramento de atividades hospitalares” para fins de redimensionamento de rede assistencial? 
[p12]  Qual a forma correta de atualização de dados de uma operadora de planos de saúde junto à ANS? 
[p12]  Por qual meio a operadora de planos de saúde deve disponibilizar o guia médico assistencial? 
[p12] Assim, a operadora possui diversos meios de divulgação de sua rede, como por exemplo, via impressa, digital por aplicativo ou outros meios eletrônicos. Mas, a Agência Nacional de Saúde Suplementar (ANS) impõe um meio obrigatório para disponibilização aos beneficiários?
[p13]  Todas as operadoras devem oferecer planos individuais/familiares na ocorrência de cancelamento de um contrato coletivo? 
[p13]  Em caso de divergência técnico assistencial inicial, na análise do pedido de cobertura, pode ser aberto procedimento de tentativa de consenso entre médico auditor e médico assistente? 
[p13] “16) O meu médico ou dentista pode entrar em acordo com a operadora, sem ter que realizar a junta?
[p13]  Em caso de adaptação de “contrato antigo” à Lei 9.656/98, a operadora de planos de saúde pode aplicar reajustes de faixa etária, conforme as regras normativas vigentes para os planos novos? 
[p13]  A operadora pode aceitar pedido de portabilidade de beneficiário em remissão de plano de saúde? 
[p13]  Para a ANS, o Rol de Procedimentos e Eventos em Saúde é taxativo? 
[p13]  Qual a regra para movimentação cadastral dos beneficiários de planos de saúde coletivos? 
[p13]  A operadora é obrigada a credenciar profissionais enfermeiros obstétricos? 
[p13]  Qual a forma adequada de cobrança de coparticipação em internações psiquiátricas pelas operadoras de planos de saúde? 
[p13]  A operadora é obrigada a aceitar a portabilidade de carências de um plano de saúde em que o beneficiário esteja internado? 
[p13]  É possível utilizar a Súmula 21, que trata de eventual aproveitamento de carências, para realização de “downgrade” do plano de saúde? 
[p14]  É permitida a inclusão de netos na categoria de dependentes de um plano de saúde? 
[p14]  Existe um prazo limite para concessão do plano continuidade por parte das operadoras de planos de saúde? 
[p14]  A operadora de planos de saúde é obrigada, durante a realização do parto, a disponibilizar acompanhamento com enfermeiro obstétrico de preferência do beneficiário? 
[p14]  Operadoras de planos de saúde são obrigadas a garantir cobertura de consultas em determinada área de atuação ou subespecialidade médica? 
[p14]  Em caso de recusa de realização do procedimento pelo médico assistente, após realização de junta médica, o que a operadora deve fazer? 
[p14] Ao ser instaurada junta médica, se seu resultado ensejar opinião diferente da indicada pelo médico assistente do beneficiário, seja em relação à indicação do procedimento ou de seus respectivos materiais e tal fato levar o médico assistente do paciente (solicitante) a se negar a realizar o procedimento ou utilizar o material, qual a conduta correta a ser adotada pela operadora de planos de saúde?
[p14]  É obrigatória a cobertura, pelas operadoras de planos de saúde, de exames ou procedimentos prescritos por profissional cirurgião-dentista? 
[p14]  É permitida a negociação de períodos diferenciados de carência nos contratos de planos de saúde? 
[p14]  Para fins de registro de plano de saúde, a atenção primária (APS) é considerada cobertura adicional? 
[p14]  A operadora de planos de saúde pode cobrar coparticipação em produtos com formação de preço “pós pagamento”? 
[p14]  É obrigatória a isenção de carências para os dependentes de titulares vinculados a contratos empresariais de plano de saúde? 
[p15]  A operadora de planos de saúde é obrigada a cobrar um valor fixo de coparticipação? 
[p15]  Existe regra regulatória para nomeação de um produto a ser registrado na ANS? 
[p15]  A operadora de planos de saúde é obrigada a disponibilizar carteirinha de identificação do beneficiário na forma física ou digital? 
[p15]  Existe um “rol de dependentes” obrigatório para inclusão nos planos de saúde? 
[p15]  É possível estabelecer nos contratos coletivos empresariais a obrigatoriedade de um número mínimo de vidas? 
[p15]  É possível alterar a área de comercialização de um produto de plano de saúde posteriormente a data de seu registro? 
[p15]  É possível a prestação de “serviços médicos ocupacionais” pelas operadoras de planos de saúde? 
[p15]  As operadoras têm obrigação de aceitar “downgrade” de produto solicitado por contratantes de planos de saúde? 
[p15]  É possível a cobrança de coparticipação do beneficiário em internação psiquiátrica? 
[p16]  A operadora de planos de saúde é obrigada a acatar o pedido de portabilidade de carências assim que recepcionada a solicitação do beneficiário? 
[p16]  A operadora de planos de saúde é obrigada a ter unidade presencial de atendimento administrativo ao beneficiário? 
[p16]  A operadora tem obrigação de aceitar pedidos de portabilidade de planos de saúde por parte dos beneficiários em qualquer condição ou circunstância? 
[p16]  A operadora pode questionar a indicação do médico assistente do beneficiário sobre o procedimento médico e/ou indicação de materiais/medicamentos? 
[p16]  A operadora de plano de saúde é obrigada a reativar um contrato cancelado por solicitação do beneficiário nos termos da RN nº 561/22 que trata do cancelamento imediato? 
[p16] E no caso de arrependimento do beneficiário, que solicitou o cancelamento, a operadora deve reverter o cancelamento do plano de saúde ?
[p16] A operadora está obrigada a reverter a exclusão do beneficiário?
[p16]  Qual é o processo para movimentação dos ativos garantidores pelas Administradoras de Benefícios junto à ANS? 
[p16]  A ANS liberou a movimentação dos ativos garantidores para as Administradoras de Benefícios? 
[p16]  Você conhece as situações que autorizam o cancelamento do registro do plano de saúde? 
[p16]  É possível a cobrança de “consulta de retorno” pelas operadoras de planos de saúde? 
[p16]  É possível aplicar a Súmula 28 - ANS, que trata da notificação para o cancelamento dos contratos de planos individuais, para as rescisões por inadimplência em contratos coletivos? 
[p17]  A Carta de Orientação ao Beneficiário é obrigatória no ato da adesão ao plano de saúde? 
[p17]  Você sabe a diferença entre “área de atuação”, “área de abrangência” e “região de saúde”? 
[p17]  O beneficiário que teve seu vínculo extinto com o plano de saúde possui direito à portabilidade? 
[p17]  Um plano de saúde pode ser contratado de forma on-line? Como funciona? 
[p17]  Quais foram as atualizações normativas da ANS com vigência em 2023? 
[p17]  A operadora pode utilizar meios eletrônicos para notificações de inadimplência de beneficiários do plano individual? 
[p17]  É possível reajustar os percentuais de coparticipação mais de uma vez ao ano? 
[p17]  A operadora de plano de saúde é obrigada a acatar a solicitação de exclusão de beneficiário de plano coletivo empresarial realizada por parte da empresa contratante, sem o envio de informações sobre a extinção de vínculo do beneficiário? 

## ANEXO B — Sitemaps (contagens)
page-sitemap.xml: 32 páginas (listadas na seção 0/5). precedente-sitemap.xml: 93; jurisprudencia-sitemap.xml: 26; temasafetadosstj-sitemap.xml: 22; tribe_events-sitemap.xml: 80+ eventos (mar/2024–nov/2025); post-sitemap.xml + post-sitemap2.xml: 1.248 posts; post_tag: eventos, leis, licitacoes, novidades, palestras, saude; author: imprensa-m3bs, leticia.
### Matérias das bases (materias_*-sitemap.xml)
- materias_precedente:
    https://m3bs.com.br/materias-precedente/comunicados/
    https://m3bs.com.br/materias-precedente/entendimentos-da-diretoria-de-fiscalizacao/
    https://m3bs.com.br/materias-precedente/pareceres-tecnicos-sobre-temas-de-cobertura-assistencial/
    https://m3bs.com.br/materias-precedente/pareceres-tecnicos-sobre-temas-economico-financeiros/
    https://m3bs.com.br/materias-precedente/resolucao-administrativa-ra/
    https://m3bs.com.br/materias-precedente/resolucao-de-diretoria-colegiada-rdc/
    https://m3bs.com.br/materias-precedente/resolucao-do-conselho-de-saude-suplementar-consu/
    https://m3bs.com.br/materias-precedente/sumulas-normativas/
- materias_jurisprudencia:
    https://m3bs.com.br/materias-jurisprudencia/carencia/
    https://m3bs.com.br/materias-jurisprudencia/co-participacao/
    https://m3bs.com.br/materias-jurisprudencia/cobertura-parcial-temporaria-cpt-doenca-preexistente/
    https://m3bs.com.br/materias-jurisprudencia/dano-material-contra-operadora/
    https://m3bs.com.br/materias-jurisprudencia/dano-moral-contra-operadora/
    https://m3bs.com.br/materias-jurisprudencia/direitos-e-responsabilidades-das-partes-envolvidas-na-telemedicina/
    https://m3bs.com.br/materias-jurisprudencia/enunciados-fonajus-cnj/
    https://m3bs.com.br/materias-jurisprudencia/fraudes-diversas/
    https://m3bs.com.br/materias-jurisprudencia/judicializacao-de-multas-ans/
    https://m3bs.com.br/materias-jurisprudencia/judicializacao-do-sus-ans/
    https://m3bs.com.br/materias-jurisprudencia/lucro-cessante-contra-operadora/
    https://m3bs.com.br/materias-jurisprudencia/materias-de-judicializacao-da-saude-em-recurso-repetitivo/
    https://m3bs.com.br/materias-jurisprudencia/1-negativa-de-cobertura-procedimento-nao-previsto-no-rol/
    https://m3bs.com.br/materias-jurisprudencia/negativa-de-cobertura-por-nao-cumprimento-dos-requisitos-da-lei/
    https://m3bs.com.br/materias-jurisprudencia/portabilidade/
    https://m3bs.com.br/materias-jurisprudencia/questoes-relacionadas-a-rede-alteracao-de-rede-sem-aviso-previo/
    https://m3bs.com.br/materias-jurisprudencia/reajuste-anual-contrato-individual/
    https://m3bs.com.br/materias-jurisprudencia/reajuste-contrato-coletivo/
    https://m3bs.com.br/materias-jurisprudencia/reajuste-contrato-coletivo-por-adesao/
    https://m3bs.com.br/materias-jurisprudencia/reajuste-faixa-etaria-contrato-individual/
    https://m3bs.com.br/materias-jurisprudencia/reembolso/
    https://m3bs.com.br/materias-jurisprudencia/rescisao-por-fraude/
    https://m3bs.com.br/materias-jurisprudencia/rescisao-por-inadimplencia/
    https://m3bs.com.br/materias-jurisprudencia/o-tema-ja-e-sedimentado-e-contrario/
    https://m3bs.com.br/materias-jurisprudencia/ressarcimento-ao-sus-nao-tem-julgado-favoravel/
- materias_temas:
    https://m3bs.com.br/materias-temas/stf/
    https://m3bs.com.br/materias-temas/stj/
### URLs das 26 fichas de jurisprudência
- https://m3bs.com.br/jurisprudencia-saude/cobertura-assistencial-resolucao-normativa-ans-rn-no-566-de29-12-22-lei-no-14-307-de-03-03-22-resolucao-normativa-ans-rn-no-395-de14-01-16-sumula-normativa-n-11-de-20-08-07revogada/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-566-de29-12-22-lei-no-14-307-de-03-03-22/
- https://m3bs.com.br/jurisprudencia-saude/entendimento-ans-difis-no-01-de07-04-16/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-565-de-16-12-22-instrucao-normativa-ans-in-dicol-no-30-de-16-12-22-instrucao-normativa-ans-in-dicol-no-29-de-16-12-22-resolucao-normativa-ans-rn-no-557-de-14-12/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-561-de-15-12-22-sistema-de-reajuste-de-planos-coletivos-rpc-resolucao-normativa-ans-rn-no-580-de-14-06-23-resolucao-normativa-ans-rn-no-559-de-14-12-22/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-561-de-15-12-22-sistema-de-reajuste-de-planos-coletivos-rpc-resolucao-normativa-ans-rn-no-580-de-14-06-23-resolucao-normativa-ans-rn-no-559-de-14-12-22-2/
- https://m3bs.com.br/jurisprudencia-saude/suspensao-e-rescisao-unilateral-de-contrato-individual-entendimento-difis-no-13-de-06-12-19-sumula-normativa-ans-sn-no-28-de-30-11-15/
- https://m3bs.com.br/jurisprudencia-saude/doencas-e-lesoes-preexistentes/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-585-de-18-08-23-resolucao-normativa-ans-rn-no-557-de-14-12-22-instrucao-normativa-ans-in-dipro-no-56-de-03-12-18-resolucao-normativa-ans-rn-n-438-de-03-1/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-558-de-14-12-22/
- https://m3bs.com.br/jurisprudencia-saude/entendimento-ans-difis-no-08-de-21-02-17/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-558-de14-12-22/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-585-de-18-08-23-instrucao-normativa-ans-in-dipro-no-56-de-03-12-18-resolucao-normativa-ans-rn-n-438-de-03-12-18-resolucao-normativa-ans-rn-no-431-de-08-1/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-consu-no-8-de-03-11-98/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-488-de-29-03-22/
- https://m3bs.com.br/jurisprudencia-saude/dano-moral-contra-operadora/
- https://m3bs.com.br/jurisprudencia-saude/dano-material-contra-operadora/
- https://m3bs.com.br/jurisprudencia-saude/lucro-cessante-contra-operadora/
- https://m3bs.com.br/jurisprudencia-saude/responsabilidade-civil-erro-medico-solidariedade-somente-uma-favoravel-o-tema-ja-e-sedimentado-e-contrario/
- https://m3bs.com.br/jurisprudencia-saude/judicializacao-do-sus-ans/
- https://m3bs.com.br/jurisprudencia-saude/jurisprudencia-judicializacao-de-multas-ans/
- https://m3bs.com.br/jurisprudencia-saude/jurisprudencia-enunciados-fonajus-cnj/
- https://m3bs.com.br/jurisprudencia-saude/jurisprudencia-materias-de-judicializacao-da-saude-em-recurso-repetitivo/
- https://m3bs.com.br/jurisprudencia-saude/resolucao-normativa-ans-rn-no-585-de-18-08-23-resolucao-normativa-ans-rn-no-568-de-19-12-22-resolucao-normativa-ans-rn-no-486-de-29-03-22-entendimento-ans-difis-no-05-de-07-04-16/
- https://m3bs.com.br/jurisprudencia-saude/direitos-e-responsabilidades-das-partes-envolvidas-na-telemedicina/
- https://m3bs.com.br/jurisprudencia-saude/ressarcimento-ao-sus-nao-tem-julgado-favoravel/
### URLs dos 22 temas STJ/STF
- https://m3bs.com.br/temas-afetados/re-597064/
- https://m3bs.com.br/temas-afetados/re-948634/
- https://m3bs.com.br/temas-afetados/re-651703/
- https://m3bs.com.br/temas-afetados/re-630852/
- https://m3bs.com.br/temas-afetados/adi-7265/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1016/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1047/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1069/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-990/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1067/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1032/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1082/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-952/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-610/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-989/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1034/
- https://m3bs.com.br/temas-afetados/tema-repetitivo-1123/
- https://m3bs.com.br/temas-afetados/tema-iac-5/
- https://m3bs.com.br/temas-afetados/sumula-302/
- https://m3bs.com.br/temas-afetados/sumula-608/
- https://m3bs.com.br/temas-afetados/sumula-609/
- https://m3bs.com.br/temas-afetados/sumula-597/
### URLs dos 93 precedentes ANS
- https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-83/
- https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-92/
- https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-95/
- https://m3bs.com.br/precedentes-regulatorios-ans/comunicado-no-98/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-01-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-02-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-03-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-n-04-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-05-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-06-16/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-08-17/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-09-19/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-10-19/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-11-19/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-12-19/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-no-13-19/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-05-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-03-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-02-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-01-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-04-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-06-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-07-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-08-202/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-10-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-11-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-12-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-14-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-15-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-16-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-17-2020/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-18-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-19-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-20-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-21-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-22-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-23-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-24-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-25-2022/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-26-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-27-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-28-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-29-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-30-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-31-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-32-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-33-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-34-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-35-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-36-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-37-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-38-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-39-2022/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-40-2022/
- https://m3bs.com.br/precedentes-regulatorios-ans/formacao-de-precos-e-faixa-etaria/
- https://m3bs.com.br/precedentes-regulatorios-ans/parecer-tecnico-no-09-2021/
- https://m3bs.com.br/precedentes-regulatorios-ans/entendimento-difis-decidido-na-599a-dicol/
- https://m3bs.com.br/precedentes-regulatorios-ans/reajuste-em-planos-coletivos/
- https://m3bs.com.br/precedentes-regulatorios-ans/reajuste-em-planos-individuais/
- https://m3bs.com.br/precedentes-regulatorios-ans/reajuste-dos-termos-de-compromisso/
- https://m3bs.com.br/precedentes-regulatorios-ans/rdc-no-07-00/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-25-08/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-82-23/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-34-10/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-49-12/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-80-22/
- https://m3bs.com.br/precedentes-regulatorios-ans/ra-no-81-23/
- https://m3bs.com.br/precedentes-regulatorios-ans/consu-no-15-99/
- https://m3bs.com.br/precedentes-regulatorios-ans/consu-no-19-98/
- https://m3bs.com.br/precedentes-regulatorios-ans/consu-no-13-98/
- https://m3bs.com.br/precedentes-regulatorios-ans/consu-no-08-98/
- https://m3bs.com.br/precedentes-regulatorios-ans/consu-no-06-98/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-02-02/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-03-01/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-04-03/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-05-03/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-07-05/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-09-05/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-12-10/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-13-10/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-14-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-16-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-17-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-19-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-21-11/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-22-12/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-23-12/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-25-12/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-26-15/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-27-15/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-29-15/
- https://m3bs.com.br/precedentes-regulatorios-ans/sumula-no-30-22/
