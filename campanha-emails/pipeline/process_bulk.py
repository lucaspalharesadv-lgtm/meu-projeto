# -*- coding: utf-8 -*-
"""Turn crawl_*.jsonl into campaign rows (same 24 columns as the sheet) with salutation, template and automatic personalization."""
import json, glob, re, sys, os, csv, collections, random, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import names as NM
random.seed(7)
LAWDOM = re.compile(r"adv|advoc|advog|law|legal|jur|abogad|avvocat|avocat|solicitor|immigra|imigra|migra|visa|visto|cidadania|citizen|nacionalid|sociedade", re.I)
WEBMAIL = re.compile(r"@(gmail|hotmail|outlook|yahoo|live|msn|icloud|uol|terra|bol|globo|ig|aol|protonmail|proton|me|yandex|gmx|web|libero|virgilio|tiscali|orange|wanadoo|free|sapo|netcabo|clix|zoho|mail)\.", re.I)
ROLE_BAD = re.compile(r"^(marketing|press|media|imprensa|financeiro|finance|suporte|support|vendas|sales|newsletter|sac|ouvidoria|dpo|privacidade|privacy|cobranca|cobrança|nfe|fiscal|contabil|contabilidade|contador|ti|tecnologia|webmaster|admin|administrator|billing|faturamento|compras|purchasing|eventos|events|comunicacao|comunicação|midia|mídia|social|blog|site|web|info-|noreply|no-reply|nao-responda|naoresponda|unsubscribe|descadastr|reclamacoes|denuncia|denúncia|compliance|canal|etica|ética|lgpd|dados|data|seguranca|security|ti@|rh|recursoshumanos|careers|jobs|vagas|trabalheconosco|talentos|recruiting|recrutamento|membership|newstips|news|editor|editorial|subscribe|subscriptions|tips|donate|donations|volunteer|giving|alumni|admissions|registrar|students|library|tickets|orders|order|reservations|booking|bookings|customerservice|customer|helpdesk|abuse|postmaster|hostmaster|noc|root|test|example|user|username|yourname|firstname|lastname|someone|nobody|null|spam|junk|sample|demo|domain|website|webdesign|seo|dev|developer|developers|designer|studio|photo|photos|foto|video|seguro|seguros|insurance|pr@|publicidade|anuncie|anuncios|ads|advertising|parcerias|partnerships|fornecedores|suppliers|licitacao|ouvidoria)", re.I)
ROLE_RH = re.compile(r"^(rh|recursoshumanos|careers|jobs|vagas|trabalheconosco|talentos|recruiting|recrutamento|hr|humanresources|people|talent)", re.I)
GENERIC = re.compile(r"^(contato|contact|contacto|contatti|info|infos|informacoes|informações|atendimento|escritorio|escritório|adv|advocacia|advogados|advogado|juridico|jurídico|legal|office|geral|secretaria|recepcao|recepção|faleconosco|fale|mail|email|e-mail|hello|hi|olá|ola|bonjour|ciao|hola|studio|cabinet|law|lawfirm|firm|team|equipe|equipa|sociedade|sac|central|comercial|administrativo|adm|direcao|direção|diretoria|contatos|contacts|reception|enquiries|enquiry|inquiries|inquiry|consulta|consultas|consultation|consultations|immigration|imigracao|imigração|visas|vistos|clientes|clients|novosclientes|newclients|intake|assistant|assistente|secretary|secretário|secretaria|paralegal|advogada)$", re.I)
AREA_PT = {"cível":"direito cível","consumidor":"direito do consumidor","bancário":"direito bancário","previdenciário":"direito previdenciário","trabalhista":"direito do trabalho","família":"direito de família","empresarial":"direito empresarial","tributário":"direito tributário","imobiliário":"direito imobiliário","criminal":"direito penal","imigração":"imigração e nacionalidade","saúde":"direito da saúde","digital":"direito digital","ambiental":"direito ambiental","agrário":"direito agrário","administrativo":"direito administrativo","eleitoral":"direito eleitoral","corporate":"direito societário","real estate":"direito imobiliário","family":"direito de família","personal injury":"responsabilidade civil","criminal defense":"direito penal","employment":"direito do trabalho","wills":"sucessões"}
AREA_EN = {"cível":"civil litigation","consumidor":"consumer law","bancário":"banking law","previdenciário":"social security law","trabalhista":"employment law","família":"family law","empresarial":"business law","tributário":"tax law","imobiliário":"real estate law","criminal":"criminal law","imigração":"immigration law","saúde":"health law","digital":"data and technology law","ambiental":"environmental law","agrário":"agribusiness law","administrativo":"administrative law","eleitoral":"election law","corporate":"corporate law","real estate":"real estate law","family":"family law","personal injury":"personal injury","criminal defense":"criminal defense","employment":"employment law","wills":"estate planning"}
TITLE_SPLIT = re.compile(r"\s*[|│┃║]\s*|\s+[-–—]\s+|\s*(?:::|•|·|»|//)\s*|:\s+")
HOMEWORDS = re.compile(r"^(home|home page|início|inicio|inici|página inicial|pagina inicial|página principal|pagina principal|bem-vindo|bem vindo|bem-vindos|welcome|homepage|site oficial|official site|principal|main|accueil|startseite|inizio|home br|home page br)$", re.I)
COUNTRY_NAME = {"US":"EUA","CA":"Canadá","UK":"Reino Unido","IE":"Irlanda","AU":"Austrália","NZ":"Nova Zelândia","PT":"Portugal","ES":"Espanha","IT":"Itália","FR":"França","DE":"Alemanha","NL":"Países Baixos","BE":"Bélgica","CH":"Suíça","LU":"Luxemburgo","JP":"Japão","AE":"Emirados Árabes","BR":"Brasil"}
EN_CC = {"US","CA","UK","IE","AU","NZ","DE","NL","BE","CH","LU","AE","JP"}

def fixmoji(s):
    if not s or "Ã" not in s and "â€" not in s: return s
    try:
        t = s.encode("cp1252", "ignore").decode("utf-8", "ignore")
        return t if t and t.count("�") == 0 else s
    except Exception: return s

def smart_title(s):
    out = []
    for w in s.split():
        if w.isupper() and len(w) > 4: out.append(w.capitalize())
        elif w.lower() in ("e","de","da","do","dos","das","em","y","and","of","the","&"): out.append(w.lower() if out else w)
        else: out.append(w)
    return " ".join(out)

NONLAW = re.compile(r"curso|faculdade|universidade|escola|concurso|licita|contab|sindicat|tribunal|prefeitura|camara|assembleia|seguro|imobiliari|corretor|financeir|banco|clinica|hospital|odonto|igreja|noticia|jornal|portal|revista|editora|livraria|loja|store|shop|gran|estacio|uninove|unip|anhanguera|cruzeiro|unopar|descomplica|qconcursos|estrategia|damasio|lfg|cers|ead|academy|academia|treinamento|training|coworking|sebrae|sesi|senac|senai|fundacao|instituto|ong|associacao|cooperativa|conselho|ministerio|secretaria|defensoria|procuradoria|mpf|mpt|mpe", re.I)
SEO_TITLE = re.compile(r"^(advogad[oa]s?|lawyer|attorney|abogad[oa]s?|avvocat[oa]|avocat|solicitor|escrit[oó]rio de advocacia|advocacia)\s+(especialista|especializad|em |de |para |no |na |online|24h|\d)", re.I)

def firm_name(r):
    t = fixmoji((r.get("title") or "").strip())
    cands = [c.strip() for c in TITLE_SPLIT.split(t) if c.strip()]
    cands = [c for c in cands if not HOMEWORDS.match(c) and len(c) >= 4 and not SEO_TITLE.match(c)]
    best = ""
    for c in cands:
        if re.search(r"advoga|advocacia|law|legal|abogad|avvocat|avocat|solicitor|immigra|imigra|migration|sociedade|associados|consultoria|escrit", c, re.I):
            best = c; break
    if not best and cands: best = min(cands, key=len) if len(cands) > 1 else cands[0]
    GEN = re.compile(r"^(advogados associados|sociedade de advogados|escrit[óo]rio de advocacia|advocacia|advogados|advogado|law firm|law office|law offices|attorneys at law|lawyers|abogados|avvocati|avocats|sociedade individual de advocacia)$", re.I)
    if best and GEN.match(best.strip()):
        others = [c for c in cands if c != best and len(c) <= 45]
        if others: best = others[0] + " " + best
    city = (r.get("city") or "").strip()
    if city: best = re.sub(r"\s+(em|in|de|at|a)\s+" + re.escape(city) + r"(/[A-Z]{2})?\s*$", "", best, flags=re.I)
    best = re.sub(r"\s+(em|in)\s+[A-ZÀ-Ý][\wÀ-ÿ]+(\s+[A-ZÀ-Ý][\wÀ-ÿ]+)?(/[A-Z]{2})?\s*$", "", best)
    best = re.sub(r"\s+", " ", best).strip(" .,-–|")
    if len(best) > 70 or not best:
        d = r["domain"].split(".")[0]
        best = d.replace("-", " ").title()
    return smart_title(best)

# ---------- quality helpers (v2) ----------
NONLAW_B = re.compile(r"(?<![a-z])(curso|cursos|faculdade|universidade|escola|concurso|concursos|licita|licitacoes|licitacao|contab|contabil|contabilidade|sindicat|sindicato|tribunal|prefeitura|camara|assembleia|seguro|seguros|imobiliaria|imobiliarias|imoveis|corretor|corretora|financeira|banco|clinica|hospital|odonto|igreja|noticia|noticias|jornal|portal|revista|editora|livraria|loja|store|shop|estacio|uninove|unip|anhanguera|cruzeiro|unopar|descomplica|qconcursos|estrategia|damasio|lfg|cers|ead|academy|academia|treinamento|training|coworking|sebrae|sesi|senac|senai|fundacao|instituto|ong|associacao|cooperativa|conselho|ministerio|secretaria|defensoria|procuradoria|mpf|mpt|mpe|consulado|consulate|embassy|embaixada|notary|notario|cartorio|translation|translations|traducao|traducoes|tradutor|news|times|herald|gazette|tribune|tv|radio|magazine|journal|press|university|college|school|institute|foundation|church|clinic|dental|realty|realtor|insurance|mortgage|technologies|software|marketing|agency|agencia|design|jiujitsu|jiu-jitsu|gym|fitness|hotel|restaurant|pizza|moto|auto|car|cars)(?![a-z])", re.I)
DIRECTORY_SUB = re.compile(r"lookup|director(y|ies|io)|diretorio|annuaire|elenco|listado|mejores|melhores|lawyersearch|legalsearch|lawyerfinder|findanattorney|attorneyfinder|legalfinder|findalawyer|find-a-lawyer|ranking|lawrank|legalrank|top10|toplawyers|listing|listed|yellowpages|paginasamarelas|guiamais|guialocal|guiajus|listaadvogados|probono|lawhelp|legalaid|legal-aid|immigrationadvocates|cliniclegal|coalition|alliance|bestlawyers|lawlists|lawbamba|beforeattorney|attorneyslisted|citizenshipquest|legalgiant|allusinjury|thesolicitordirectory|consulto\.pt|wiki|forum", re.I)
DIRECTORY_LABEL = re.compile(r"(^|\.)(avvo|justia|findlaw|nolo|hg|martindale|superlawyers|lawyers|attorneys|legal500|chambers|lawtally|lawinfo|upcounsel|legalmatch|justanswer|expertise|jusbrasil|escavador|ilrc|nilc|aila|here|blog|news|oab[a-z0-9-]*|esa|guia[a-z0-9-]*|lista[a-z0-9-]*)\.|[a-z]*bar\.org", re.I)
DIR_TITLE = re.compile(r"\bfind (a|an|the|&|and|your|local|best|top)\b|near you|compare (lawyers|attorneys|solicitors)|lawyer directory|attorney directory|solicitor directory|directory of|\bdirectory\b|best lawyers|top \d+|law lists|legal network|lawyers? network|attorney network|official website|technologies|the world's|newspaper|magazine|university|school of law|law school|bar association|state bar\b|the [a-z]+ bar\b|ordem dos advogados|law society|legal aid|pro bono|nonprofit|non-profit|coalition|advocates network|guia de advogados|lista de advogados|encontre (um|o|seu) advogado|melhores advogados|advocacias top|onde .* encontra|jiu-jitsu|jiu jitsu|academy|\bgym\b|fitness|dental|dentist|realty|realtor|insurance agency|mortgage|translation|interpretation|interpreters|language solutions|notary|not[áa]rio|cart[óo]rio|consulado|consulate|embassy|embaixada|sindicato|prefeitura|tribunal|faculdade|unifanap|cursos? (de|online|para|preparat)|preparat[óo]rio|apostila|simulado|not[íi]cias|portal de not|supply chain|manufacturing|engineering|software|marketing agency|web design|seo agency|guia comercial|contabilidade|cont[áa]bil|accounting|bookkeeping|marketing jur[íi]dico|marketing para advogados|software jur[íi]dico|sistema jur[íi]dico|sites? para advogados|cria[çc][ãa]o de sites|ag[êe]ncia|r[áa]dio|radio station|community center|centro comunit[áa]rio", re.I)
DIR_DESC = re.compile(r"directory of|find (a|an|the) (lawyer|attorney|solicitor)|compare (lawyers|attorneys)|lawyers? network|bar association|legal aid|pro bono|nonprofit|non-profit|501\(c\)|coalition|portal de not[íi]cias|guia comercial|lista de advogados|encontre advogados|advogados (qualificados|recomendados|verificados)", re.I)
CRAWL_LAW = re.compile(r"advogad|advocacia|\boab\b|attorney|law firm|law office|lawyer|solicitor|barrister|avvocat|abogad|avocat|rechtsanwalt|paralegal|migration agent|immigration consultant|rcic|escrit[óo]rio de advocacia|jur[íi]dic|studio legale|despacho", re.I)
LAWDOM_STRICT = re.compile(r"adv|advoc|advog|law|legal|jur|abogad|avvocat|avocat|solicitor|immigra|imigra|migra|visa|visto|cidadania|citizen|nacionalid|sociedade", re.I)

def law_signal(r):
    lh = r.get("law_hits", 0) or 0
    title = fixmoji(r.get("title") or ""); desc = fixmoji(r.get("desc") or "")
    dom = r["domain"].lower()
    if DIRECTORY_SUB.search(dom) or DIRECTORY_LABEL.search(dom): return False
    if DIR_TITLE.search(title) or DIR_DESC.search(desc): return False
    if NONLAW_B.search(dom) and lh < 8: return False
    if re.search(r"\.org(\.[a-z]{2})?$", dom) and lh < 15: return False
    return lh >= 3 or bool(CRAWL_LAW.search(title + " " + desc)) or bool(LAWDOM_STRICT.search(dom))

ACR_KEEP = set("LLP LLC PC PLLC LTD LTDA OAB USA NYC UK EUA SA S/A DC CT NY NJ MA RI PA FL TX CA AL SC RJ SP MG RS PR BA PE CE GO DF ES MT MS PB RN PI SE TO RO AC RR AP AM INSS RCIC CPA QC BC ON AB NSW VIC QLD WA ACT NT II III IV JD LLM PHD MBA LLB KC APC LPA PLC PLLP LLLP P.A. P.C. S.C. SRL SPA EOOD GMBH AG".split())
COMMON_UPPER = set("law firm legal office offices group immigration lawyers lawyer attorney attorneys advogados advogado advocacia associados sociedade abogados avvocati avvocato studio legale juridico jurídico consultoria escritorio escritório services solicitors partners associates novo nova advogada advogadas assessoria direito trabalhista previdenciario previdenciário civel cível familia família empresarial tributario tributário imobiliario imobiliário criminal penal bancario bancário consumidor".split())
def smart_title(s):
    out = []
    for w in s.split():
        core = w.strip(".,;:()®™")
        if core.isupper() and len(core) >= 3 and core not in ACR_KEEP and re.search(r"[AEIOUÁÉÍÓÚÀÂÊÔÃÕ]", core) and (len(core) > 4 or core.lower() in COMMON_UPPER):
            out.append(w.replace(core, core.capitalize()))
        elif w.lower() in ("e","de","da","do","dos","das","em","y","and","of","the","&","di","del","della","des","du"): out.append(w.lower() if out else w)
        elif w.islower() and w in COMMON_UPPER: out.append(w.capitalize())
        else: out.append(w)
    return " ".join(out)

LAWWORD_RE = re.compile(r"\b(lawyers?|attorneys?|solicitors?|barristers?|law firm|law offices?|law group|law practice|legal services|legal|advogad[oa]s?|advocacia|escrit[óo]rio de advocacia|escrit[óo]rio jur[íi]dico|abogad[oa]s?|despacho de abogados|avvocat[oi]|studio legale|avocats?|cabinet d'avocats?|rechtsanw[äa]lte?|migration agents?|immigration consultants?|immigration)\b", re.I)
PRACTICE_W = set("""immigration immigrant immigrants family criminal defense defence personal injury injuries injured business corporate employment divorce dui estate estates bankruptcy tax real civil litigation commercial property accident accidents workers compensation disability visa visas citizenship nationality asylum deportation green card cards naturalization naturalisation residency sponsorship international wills probate planning appeals trabalhista trabalhistas previdenciário previdenciario previdenciária previdenciaria cível civel cíveis civeis consumidor família familia empresarial empresariais tributário tributario tributária imobiliário imobiliario imobiliária criminalista criminal criminais bancário bancario bancária digital ambiental saúde saude inss aposentadoria aposentadorias contratos sucessões sucessoes público publico administrativo eleitoral militar penal trabalho trabalhador trabalhadores direito direitos jurídico juridico jurídica juridica ações acoes indenização indenizações indenizacao pensões pensoes benefícios beneficios revisão revisao divórcio divorcio inventário inventario usucapião usucapiao despejo acidente acidentes extranjería extranjeria nacionalidad inmigración inmigracion residencia arraigo reagrupación reagrupacion lesiones defensa immigrazione cittadinanza famiglia penale civile lavoro droit étrangers etrangers famille travail pénal affaires rights consultivo contencioso recuperação recuperacao judicial médico medico condominial""".split())
GENERIC_W = set("""best top rated local experienced affordable leading trusted skilled affirmative flat fee fees call now today free can trust you your yours me the and & of for in at serving from with a an on by to no na em de do da das dos e para com en y el la los las le les des du et il lo gli i un una uno home page online 24h 24 horas hours firm office offices group practice services service solutions solution specialist specialists especialista especialistas especializado especializada especializados especializadas qualificados qualificado recomendados verificados avaliado avaliados google whatsapp experts expert professional professionals team legal law lawyer lawyers attorney attorneys solicitor solicitors barrister barristers notaries notary notários notarios advogado advogada advogados advogadas advocacia abogado abogada abogados avvocato avvocati avocat avocats studio legale escritório escritorio sociedade associados associates assessoria consultoria jurídica juridica despacho cabinet área áreas area areas city county greater metro bay valley north south east west central downtown suburbs beach beaches coast island town village new york jersey england london ontario quebec texas florida california massachusetts pennsylvania connecticut maryland virginia georgia illinois michigan ohio washington oregon arizona nevada colorado utah carolina dakota minnesota wisconsin missouri kentucky tennessee alabama louisiana oklahoma kansas nebraska iowa indiana vermont maine hampshire rhode delaware hawaii alaska columbia mexico arkansas mississippi montana wyoming idaho dc usa us uk eua brasil brazil portugal canada canadá australia austrália ireland irlanda italia itália italy espanha spain españa france frança deutschland germany alemanha nyc nj ny ma ct ri pa fl tx ga nc sc va md wa or az nv co ut mn wi mo ky tn al ok ks ne ia vt nh hi ak sp rj mg rs pr ba pe ce go df es mt ms pb rn pi se ro ac rr ap am ltd ltda inc llc llp nationwide statewide national nacional internacional international global worldwide mundo todo toda todos todas país pais estado estados cidade cidades região regiao zona metropolitana grande capital interior litoral norte sul leste oeste centro help helping helps since desde anos years yrs experience experiência experiencia comprehensive excellence excelência excelencia ética etica ethics integrity justice justiça justica results representation advocacy expertise passion dedicated committed quality qualidade compromisso soluções solucoes atendimento defesa bilingual bilíngue canadian australian american british irish european brazilian brasileiros brasileiras brasileiro brasileira português portugues portuguese spanish español espanhol italian italiano french français francês welcome bem-vindo bemvindo seu sua seus suas nosso nossa nossos nossas our we ste suite st ave avenue street road blvd floor andar sala edifício edificio torre bairro rua av phone tel fone ligue llame consultation consultations consulta consultas gratuita gratis grátis ranked award winning award-winning reviews review stars 5-star amp virtual remoto remota remote partner partners pc pllc apc company co corp corporation sociedad chinese korean japanese russian arabic hispanic latino latina asian indian vietnamese polish ukrainian turkish persian farsi mandarin cantonese gestoría gestoria gestión gestion asesoría asesoria consultoría altamente highly muito very mais more most migration agent agents consultant consultants adviser advisers advisor advisors registered licensed certified rcic mara unity richiedi consulenza una contatti contattaci prenota richiesta gratuita permanent residence residência residencia temporary visitor work study student students spouse spousal sponsorship appeal appeals refused refusal""".split())
ENTITY_RE = re.compile(r"(\bLLP\b|\bLLC\b|\bPC\b|\bPLLC\b|\bP\.C\.|\bP\.A\.|\bLtd\b|\bLtda\b|\bInc\b|\bGroup\b|\bAssociates\b|\bAssociados\b|\bSociedade\b|\bPartners\b|\bLaw Offices? of\b|\bEscrit[óo]rio\b|\bStudio\b|\bCabinet\b|\bDespacho\b|\bSRL\b|\bGmbH\b|\bLLLP\b|\bAPC\b|\bAdvogados\b|\bAdvocacia\b|\bAbogados\b|\bSolicitors\b|\bAvvocati\b)", re.I)
SEO_START = re.compile(r"^(find|best|top|your|rated|local|experienced|affordable|leading|trusted|skilled|the best|top rated|advogad[oa]s?\s+(em|especialista|especializad|online|24h|\d)|escrit[óo]rio de advocacia em|advocacia em|lawyers? in|attorneys? in|solicitors? in|immigration lawyer|immigration attorney|immigration solicitor|abogados? (en|de extranjer)|avvocat[oi] (a|in|per)|avocats? (à|a|en))", re.I)
HOME_PREFIX = re.compile(r"^(welcome to( the)?|bem[- ]vindos?( (ao|à|a|aos|às))?|home( page)?|in[íi]cio|p[áa]gina inicial)\s*[-:|]?\s*", re.I)

def _tokens(s):
    toks = [t.strip(".,'’®™()") for t in re.findall(r"[\w'’&.®™()-]+", s)]
    return [t.lower() for t in toks if t]

def _known(t):
    return t in GENERIC_W or t in PRACTICE_W or t.rstrip("s") in GENERIC_W or t.rstrip("s") in PRACTICE_W
def _unknown(low, city, uf):
    ctoks = set(w.lower() for w in re.findall(r"\w+", city or "")) | ({uf.lower()} if uf else set())
    return [t for t in low if not _known(t) and t not in ctoks and not t.isdigit() and len(t) > 1 and t != "&"]

def seo_like(seg, city, uf):
    s0 = HOME_PREFIX.sub("", seg.strip()).strip()
    if not s0: return True
    if SEO_TITLE.match(s0) or SEO_START.match(s0): return True
    if re.search(r"\d{3,}|\(\d{2,3}\)|\bcall\b|\bligue\b|\bwhatsapp\b|!|\?|@", s0, re.I): return True
    if re.search(r"[\u3040-\u30ff\u3400-\u9fff\uac00-\ud7af\u0400-\u04ff\u0600-\u06ff\u0590-\u05ff\u0e00-\u0e7f]", s0): return True
    low = _tokens(s0)
    if not low: return True
    unknown = _unknown(low, city, uf)
    if not unknown: return True
    has_law = bool(LAWWORD_RE.search(s0)) or any(t in PRACTICE_W for t in low)
    if not has_law: return len(low) > 8
    if re.search(r"\b(lawyers?|attorneys?|solicitors?|law firm|law offices?|advogad[oa]s?|advocacia|abogad[oa]s?|avvocat[oi]|avocats?|consultants?)\s+(in|serving|near|em|para|en|de|da|do|no|na|à|a|di|per|pour)\s", s0, re.I): return True
    if re.search(r"\b(lawyers?|attorneys?|solicitors?|law firm|law offices?|advogad[oa]s?|advocacia|abogad[oa]s?|avvocat[oi]|avocats?)(\s+[\wÀ-ÿ&]+){1,3}\s+(in|serving|near|em|en|à|per|pour)\s+[A-ZÀ-Ý]", s0): return True
    if len(low) > 7 and not ENTITY_RE.search(s0): return True
    if ENTITY_RE.search(s0): return False
    has_practice = any(t in PRACTICE_W for t in low) or bool(re.search(r"^(best|top|rated|local|experienced|affordable|leading|trusted|skilled|bilingual)\b", s0, re.I))
    if has_practice and len(unknown) <= 1 and re.search(r"(lawyers?|attorneys?|solicitors?|law firm|law offices?|law group|advogad[oa]s?|advocacia|abogad[oa]s?|avvocat[oi]|avocats?|consultants?)(\s+(in|em|de|serving|near)\s+[\w\s,./]+|\s+[A-Z]{2}|,?\s+[A-Z][\w]+(\s+[A-Z]{2})?)?$", s0, re.I): return True
    return False

def domain_name(r):
    host = ""
    try: host = urllib.parse.urlparse(r.get("final_url") or "").netloc.lower().replace("www.", "")
    except Exception: pass
    stem = (host or r["domain"]).split(".")[0]
    if "-" in stem: words = stem.split("-")
    else: words = re.sub(r"(advogadosassociados|advogados|advogado|advocacia|adv|lawfirm|lawyers|lawyer|lawoffice|law|legal|attorneys|attorney|immigration|abogados|avvocato|avvocati|solicitors|group|firm|offices|office|associados|sociedade|studio|legale)", r" \1 ", stem).split()
    return smart_title(" ".join(w.capitalize() for w in words if w))

GEN_TAIL = re.compile(r"^(advogados associados|sociedade de advogados|escrit[óo]rio de advocacia|escrit[óo]rio de advogados|advocacia|advogados|law firm|law offices?|attorneys at law|solicitors( and notaries)?|abogados|despacho de abogados|studio legale|avvocati|cabinet d'avocats)\b", re.I)
GEN_ONLY = re.compile(r"^(advogados associados|sociedade de advogados|escrit[óo]rio de advocacia|escrit[óo]rio de advogados|advocacia|advogados|advogado|law firm|law office|law offices|attorneys at law|lawyers|abogados|despacho de abogados|avvocati|avocats|studio legale|cabinet d'avocats|sociedade individual de advocacia|the law firm|the law office|solicitors|solicitors and notaries)$", re.I)

def _cand_score(c):
    low = _tokens(c)
    unknown = [t for t in low if not _known(t) and not t.isdigit() and len(t) > 1]
    law = bool(re.search(r"advoga|advocacia|law|legal|abogad|avvocat|avocat|solicitor|immigra|imigra|migration|sociedade|associados|consultoria|escrit|studio|&|\bllp\b|\bllc\b|\bpc\b|\bpllc\b", c, re.I))
    return (1 if unknown else 0, 1 if law else 0, -len(c))

def firm_name2(r):
    """returns (name, ok). ok=False means the site title was SEO-style and the name is only a guess from the domain."""
    t = fixmoji((r.get("title") or "").strip())
    city = (r.get("city") or "").strip(); uf = (r.get("uf") or "").strip()
    cands = [HOME_PREFIX.sub("", c).strip(" .,-–|:") for c in TITLE_SPLIT.split(t) if c.strip()]
    cands = [c for c in cands if c and not HOMEWORDS.match(c) and len(c) >= 3]
    good, gen_tail = [], ""
    def strip_geo(c):
        if city and len(c.split()) > 2: c = re.sub(r"\s*[,/|-]?\s*(em|in|de|at|a|en|à|di)?\s*" + re.escape(city) + r"(\s*[,/-]?\s*[A-Z]{2})?\s*$", "", c, flags=re.I)
        c = re.sub(r"\s+(em|in|en|à|a)\s+[A-ZÀ-Ý][\wÀ-ÿ]+(\s+[A-ZÀ-Ý][\wÀ-ÿ]+)?(/[A-Z]{2})?\s*$", "", c)
        return c.strip(" .,-–|:")
    for c in cands:
        c = strip_geo(c) if not GEN_TAIL.match(c) else c
        if seo_like(c, city, uf):
            m = GEN_TAIL.match(c)
            if m and not gen_tail: gen_tail = m.group(1)
            continue
        parts = [p.strip() for p in c.split(",") if p.strip()]
        while len(parts) > 1 and seo_like(parts[-1], city, uf): parts.pop()
        c = ", ".join(parts)
        m = re.search(r"^(.{4,}?\b(?:LLP|LLC|PC|PLLC|Ltd|Inc|Group|Associates|Associados|Advogados|Advocacia|Abogados|Avvocati|Solicitors|Law|Legal))\s+(?:(?:immigration|family|criminal|defense|personal|injury|business|employment|trabalhista|previdenci[áa]rio|c[íi]vel|empresarial|tribut[áa]rio|imobili[áa]rio|and|&|e)\s+)*(?:lawyers?|attorneys?|solicitors?|law firm|law offices?|advogad[oa]s?|advocacia|abogad[oa]s?|avvocat[oi])\b.*$", c, re.I)
        if m and len(m.group(1).split()) >= 2: c = m.group(1)
        if city and len(c.split()) > 2: c = re.sub(r"\s*[,/|-]?\s*(em|in|de|at|a|en|à|di)?\s*" + re.escape(city) + r"(\s*[,/-]?\s*[A-Z]{2})?\s*$", "", c, flags=re.I)
        c = re.sub(r"\s+(em|in|en|à|a)\s+[A-ZÀ-Ý][\wÀ-ÿ]+(\s+[A-ZÀ-Ý][\wÀ-ÿ]+)?(/[A-Z]{2})?\s*$", "", c)
        c = re.sub(r"\s*\b(h[áa]\s+)?(mais de\s+)?\d+\+?\s*(anos|years|yrs)( de experi[êe]ncia| of experience)?\b", "", c, flags=re.I)
        c = re.sub(r"\s+", " ", c).strip(" .,-–|:")
        if len(c) >= 3 and not seo_like(c, city, uf): good.append(c)
    best = max(good, key=_cand_score) if good else ""
    if best and GEN_ONLY.match(best): best = ""
    if best and gen_tail and not _cand_score(best)[1]:
        gl = gen_tail.lower()
        if gl.startswith(("escrit", "sociedade de")): best = best + " Advocacia"
        elif gl.startswith("despacho"): best = best + " Abogados"
        elif gl.startswith("studio"): best = "Studio Legale " + best
        elif gl.startswith("cabinet"): best = "Cabinet " + best
        else: best = best + " " + gen_tail
    if best.startswith(("&", "e ", "and ")): best = ""
    if best and len(best) <= 70: return smart_title(best), True
    return domain_name(r), False

PERSON_BAD = set("general inquiries inquiry place review challenges one suite street avenue road office team group firm services law legal center centre department division immigration intake support contact info new clients client free consultation home page main about us the and of for attorney attorneys lawyer lawyers solicitor solicitors advogado advogada advogados advocacia abogado abogados avvocato partner partners associate associates staff member members senior junior managing founding founder director directors chief executive officer president secretary paralegal assistant reception receptionist admin administrator manager marketing media press careers jobs privacy policy terms conditions cookies copyright rights reserved all read more learn click here email e-mail phone fax address location locations hours map directions pay bill payment portal login judicial escritório escritorio sociedade equipe equipa time nossa nosso".split())
def valid_person(n):
    if not n: return ""
    toks = n.split()
    if not (2 <= len(toks) <= 4): return ""
    low = [t.lower().strip(".,") for t in toks]
    if any(t in NM.STOP or t in PERSON_BAD or t in PRACTICE_W for t in low): return ""
    if any(t.isupper() and len(t) > 2 for t in toks): return ""
    if re.search(r"\d", n): return ""
    first = low[0]
    if first in NM.FEMALE or first in NM.MALE: return n
    conn = ("de","da","do","dos","das","e","y","van","von","del","della","di","la","le","du","des")
    if all(t[:1].isupper() for t in toks if t.lower() not in conn) and not any(t in GENERIC_W for t in low): return n
    return ""

SOLO_RE = re.compile(r"^(?:Avvocato|Avv\.|Abogad[oa]|Advogad[oa]|Dr\.?a?\.?|Dra\.|Attorney|Atty\.?|Maître|Me\.?|Rechtsanwalt|Rechtsanwältin|Solicitor|Lic\.)\s+([A-ZÀ-Ý][\w'’À-ÿ-]+)(?:\s+[A-ZÀ-Ý][\w'’À-ÿ.-]*)?(?:\s+(?:de|da|do|dos|das|di|del|della|van|von|la|le|du|des)\s+)?\s+([A-ZÀ-Ý][\w'’À-ÿ-]+)\s*(?:Advogad[oa]s?|Advocacia|Avvocato|Abogad[oa]|Law|Legal|Attorney at Law)?$", re.I)
SOLO_RE2 = re.compile(r"^([A-ZÀ-Ý][\w'’À-ÿ-]+)(?:\s+[A-ZÀ-Ý][\w'’À-ÿ.-]*)?(?:\s+(?:de|da|do|dos|das|di|del|della|van|von|la|le|du|des)\s+)?\s+([A-ZÀ-Ý][\w'’À-ÿ-]+)\s+(?:Advogad[oa]|Attorney at Law|Avvocato|Abogad[oa]|Solicitor|Lawyer|Attorney|Advocacia|Law)$")
NAME_ONLY = re.compile(r"^([A-ZÀ-Ý][\w'’À-ÿ-]+)(?:\s+[A-ZÀ-Ý][\w'’À-ÿ.-]*)?(?:\s+(?:de|da|do|dos|das|di|del|della|van|von|la|le|du|des)\s+)?\s+([A-ZÀ-Ý][\w'’À-ÿ-]+)$")
def person_from_title(firm):
    m = SOLO_RE.match(firm) or SOLO_RE2.match(firm) or NAME_ONLY.match(firm)
    if not m: return ""
    first, last = m.group(1), m.group(2)
    fl, ll = first.lower(), last.lower()
    if fl in NM.STOP or ll in NM.STOP or ll in GENERIC_W or ll in PRACTICE_W or fl in GENERIC_W or fl in PRACTICE_W: return ""
    if fl in NM.FEMALE or fl in NM.MALE: return f"{first} {last}"
    return ""

def personalization2(lang, tpl, person, sex, firm, firm_ok, solo, city, uf, cc, areas, pt_hits, city_ok):
    ap = areas_phrase(areas, lang)
    loc = ""
    if city_ok and city: loc = f"{city}/{uf}" if (cc == "BR" and uf) else city
    pron = {"M":"o senhor","F":"a senhora","M?":"o senhor","F?":"a senhora"}.get(sex, "")
    v = random.random()
    if tpl == "BR_PT":
        if person and pron and not solo:
            team = f"a equipe de {firm}" if firm_ok else "a equipe"
            if loc and ap: return f"Vi no site do escritório que {pron} integra {team}, em {loc}, com atuação em {ap}."
            if loc: return f"Vi no site do escritório que {pron} integra {team}, em {loc}."
            if ap: return f"Vi no site do escritório que {pron} integra {team}, com atuação em {ap}."
            return f"Vi no site do escritório que {pron} integra {team}."
        subj = firm if (firm_ok and not solo) else ("o seu escritório" if solo else "o escritório")
        if loc and ap: return (f"Vi no site que {subj} atua em {loc}, com {ap}." if v < 0.5 else f"Notei que {subj}, em {loc}, atende demandas de {ap}.")
        if loc: return f"Vi no site que {subj} atende em {loc}."
        if ap: return (f"Vi no site que {subj} atua em {ap}." if v < 0.5 else f"Notei que {subj} atende demandas de {ap}.")
        return (f"Vi o site de {firm} e a forma como o escritório apresenta sua atuação." if (firm_ok and not solo) else "Vi o site do escritório e a forma como ele apresenta sua atuação.")
    if tpl in ("EN", "OPS_EN"):
        pt = " and serves Portuguese-speaking clients" if pt_hits >= 2 else ""
        a = ap if ap else ("immigration matters" if tpl == "EN" else "legal matters")
        if person and not solo:
            team = f"the team at {firm}" if firm_ok else "the team"
            if loc: return f"I saw on your website that you are part of {team} in {loc}, working on {a}{pt}."
            return f"I saw on your website that you are part of {team}, working on {a}{pt}."
        subj = firm if (firm_ok and not solo) else ("your practice" if solo else "your firm")
        if loc: return f"I saw on your website that {subj} handles {a} in {loc}{pt}."
        return f"I saw on your website that {subj} handles {a}{pt}."
    a = ap if ap else ("imigração e nacionalidade" if tpl == "PT" else "assessoria jurídica")
    country = COUNTRY_NAME.get(cc, "")
    where = (f"em {loc}" if loc else (f"em {country}" if country else "")).strip()
    if person and pron and not solo:
        team = f"a equipe de {firm}" if firm_ok else "a equipe"
        return f"Vi no site do escritório que {pron} integra {team}{(' ' + where) if where else ''}, com atuação em {a}."
    subj = firm if (firm_ok and not solo) else ("o seu escritório" if solo else "o escritório")
    if pt_hits >= 2: return f"Vi no site que {subj}{(' ' + where) if where else ''} atende clientes brasileiros em {a}."
    return f"Vi no site que {subj}{(' ' + where) if where else ''} atua em {a}."

def salutation2(lang, person, firm, firm_ok, sex):
    if person: return salutation(lang, person, firm, sex)
    if firm_ok: return f"Dear {firm} team," if lang == "EN" else "Prezados,"
    return "Dear team," if lang == "EN" else "Prezados,"
# ---------- end helpers v2 ----------

def person_from_email(local):
    parts = [p for p in re.split(r"[._\-]", local) if p.isalpha() and len(p) >= 3]
    if len(parts) >= 2 and (parts[0].lower() in NM.FEMALE or parts[0].lower() in NM.MALE):
        return " ".join(p.capitalize() for p in parts[:3])
    return ""

def gender(first):
    f = first.lower().strip(".")
    if f in NM.FEMALE and f not in NM.MALE: return "F"
    if f in NM.MALE and f not in NM.FEMALE: return "M"
    if f in NM.MALE and f in NM.FEMALE: return "?"
    if f.endswith("a") and not f.endswith(("ista","ca")) and len(f) > 3: return "F?"
    if f.endswith(("o","or","io")) and len(f) > 3: return "M?"
    return "?"

def clean_person(n):
    n = re.sub(r"^(Dr\.?a?\.?|Dra\.?|Adv\.?|Mr\.?|Ms\.?|Mrs\.?|Atty\.?|Esq\.?)\s+", "", n.strip())
    n = re.sub(r",?\s*(Esq\.?|Jr\.?|OAB.*|LL\.?M\.?|J\.?D\.?|Ph\.?D\.?|MBA|P\.?C\.?)\s*$", "", n, flags=re.I)
    n = re.sub(r"\s+", " ", n).strip()
    if n.isupper(): n = n.title()
    return n

def salutation(lang, person, firm, sex):
    if person:
        parts = person.split(); first, last = parts[0], parts[-1]
        if lang == "EN":
            if sex in ("M", "M?"): return f"Dear Mr. {last},"
            if sex in ("F", "F?"): return f"Dear Ms. {last},"
            return f"Dear {person},"
        else:
            if sex in ("M", "M?"): return f"Prezado Dr. {first},"
            if sex in ("F", "F?"): return f"Prezada Dra. {first},"
            return f"Prezado(a) Dr(a). {first},"
    return f"Dear {firm} team," if lang == "EN" else "Prezados,"

def areas_phrase(areas, lang):
    m = AREA_PT if lang != "EN" else AREA_EN
    xs = [m[a] for a in areas if a in m][:3]
    xs = list(dict.fromkeys(xs))
    if not xs: return ""
    if len(xs) == 1: return xs[0]
    return (", ".join(xs[:-1]) + (" e " if lang != "EN" else " and ") + xs[-1])

def personalization(lang, tpl, person, sex, firm, city, uf, cc, areas, pt_hits, city_ok):
    ap = areas_phrase(areas, lang)
    loc = ""
    if city_ok and city:
        loc = f"{city}/{uf}" if (cc == "BR" and uf) else city
    pron = {"M":"o senhor","F":"a senhora","M?":"o senhor","F?":"a senhora"}.get(sex, "")
    if tpl == "BR_PT":
        v = random.random()
        if person and pron:
            if loc and ap: return f"Vi no site do escritório que {pron} integra a equipe de {firm}, em {loc}, com atuação em {ap}."
            if loc: return f"Vi no site do escritório que {pron} integra a equipe de {firm}, em {loc}."
            if ap: return f"Vi no site do escritório que {pron} integra a equipe de {firm}, com atuação em {ap}."
            return f"Vi no site do escritório que {pron} integra a equipe de {firm}."
        if loc and ap: return (f"Vi no site que {firm} atua em {loc}, com {ap}." if v < 0.5 else f"Notei que {firm}, em {loc}, atende demandas de {ap}.")
        if loc: return f"Vi no site que {firm} atende em {loc}."
        if ap: return (f"Vi no site que {firm} atua em {ap}." if v < 0.5 else f"Notei que {firm} atende demandas de {ap}.")
        return f"Vi o site de {firm} e a forma como o escritório apresenta sua atuação."
    if tpl in ("EN", "OPS_EN"):
        pt = " and serves Portuguese-speaking clients" if pt_hits >= 2 else ""
        a = ap if ap else ("immigration matters" if tpl == "EN" else "legal matters")
        if person:
            if loc: return f"I saw on your website that you are part of the team at {firm} in {loc}, working on {a}{pt}."
            return f"I saw on your website that you are part of the team at {firm}, working on {a}{pt}."
        if loc: return f"I saw on your website that {firm} handles {a} in {loc}{pt}."
        return f"I saw on your website that {firm} handles {a}{pt}."
    # PT / OPS_PT (Portugal, Spain, Italy, France, lusophone firms abroad)
    a = ap if ap else ("imigração e nacionalidade" if tpl == "PT" else "assessoria jurídica")
    country = COUNTRY_NAME.get(cc, "")
    where = (f"em {loc}" if loc else (f"em {country}" if country else "")).strip()
    if person and pron:
        return f"Vi no site do escritório que {pron} integra a equipe de {firm}{(' ' + where) if where else ''}, com atuação em {a}."
    if pt_hits >= 2: return f"Vi no site que {firm}{(' ' + where) if where else ''} atende clientes brasileiros em {a}."
    return f"Vi no site que {firm}{(' ' + where) if where else ''} atua em {a}."

def choose_template(cc, lang_site, areas, q, pt_hits, text_lang_guess):
    if cc == "BR": return "BR_PT", "PT"
    immig = ("imigração" in areas) or re.search(r"immigra|imigra|migration|nacionalid|cidadania|citizen|extranjer|immigrazione|cittadinanza|étrangers", q or "", re.I)
    site_pt = (lang_site or "").lower().startswith("pt") or text_lang_guess == "pt"
    if cc == "PT" or site_pt:
        return ("PT" if immig else "OPS_PT"), "PT"
    if cc in EN_CC:
        return ("EN" if immig else "OPS_EN"), "EN"
    return ("EN" if immig else "OPS_EN"), "EN"  # ES/IT/FR firms: write in English

def main(files, out_prefix, existing_emails, existing_domains, cap_br=5, cap_int=4):
    rows = []; stats = collections.Counter()
    for f in files:
        for l in open(f, encoding="utf-8"):
            try: r = json.loads(l)
            except Exception: continue
            if r.get("status") != "ok": stats["site_falhou"] += 1; continue
            if r["domain"] in existing_domains: stats["dominio_ja_na_lista"] += 1; continue
            if not law_signal(r): stats["nao_advocacia"] += 1; continue
            if re.search(r"\.(gov|edu|mil)(\.[a-z]{2})?$|\.(jus|mp|leg|def)\.br$|\.gob\.[a-z]{2}$|\.gouv\.fr$", r["domain"].lower()): stats["nao_advocacia"] += 1; continue
            for e in r.get("emails") or []: e["name"] = fixmoji(e.get("name") or "")
            emails = r.get("emails") or []
            if not emails: stats["sem_email"] += 1; continue
            firm, firm_ok = firm_name2(r); cc = r.get("cc") or "BR"
            solo = person_from_title(firm) if firm_ok else ""
            if not firm_ok: stats["nome_deduzido_dominio"] += 1
            own = []; other = []
            for e in emails:
                em = e["email"].lower().replace("@www.", "@"); e["email"] = em; local, dom = em.split("@")
                if em in existing_emails: continue
                if re.search(r"\.(gov|edu|mil)(\.[a-z]{2})?$|\.(jus|mp|leg|def)\.br$|\.gob\.[a-z]{2}$|\.gouv\.fr$", dom): continue
                if ROLE_BAD.search(local) and not ROLE_RH.search(local): continue
                sitedom = r["domain"].lower()
                same = dom == sitedom or dom.endswith("." + sitedom) or sitedom.endswith("." + dom)
                if same: own.append(e)
                elif WEBMAIL.search("@" + dom): other.append(e)
                elif LAWDOM.search(dom): other.append(e)
            pool = own if own else other[:2]
            if not pool: stats["sem_email_valido"] += 1; continue
            # classify
            named, general, rh = [], [], []
            for e in pool:
                local = e["email"].split("@")[0]
                person = valid_person(clean_person(e.get("name") or "")) or person_from_email(local)
                if person and (person.lower().split()[0] in NM.STOP): person = ""
                if ROLE_RH.search(local): rh.append((e, ""))
                elif person and not GENERIC.match(local): named.append((e, person))
                elif GENERIC.match(local) or not person: general.append((e, ""))
                else: named.append((e, person))
            cap = cap_br if cc == "BR" else cap_int
            chosen = named[:cap - 1] + general[:1] + rh[:1]
            if not chosen: chosen = general[:1] or rh[:1]
            chosen = chosen[:cap]
            tl = "pt" if re.search(r"advoga|advocacia", (r.get("title") or "") + (r.get("desc") or ""), re.I) else ""
            tpl, lang = choose_template(cc, r.get("lang"), r.get("areas") or [], r.get("q"), r.get("pt_hits", 0) or 0, tl)
            for e, person in chosen:
                is_solo = False
                if not person and solo:
                    person, is_solo = solo, True
                sex = gender(person.split()[0]) if person else ""
                local = e["email"].split("@")[0]
                row = {
                    "saudacao": salutation2(lang, person, firm, firm_ok, sex), "nome_contato": person or (f"Equipe {firm}" if firm_ok else "Equipe do escritório"),
                    "tratamento": ("Dr." if sex in ("M","M?") else "Dra." if sex in ("F","F?") else "") if person else "",
                    "escritorio": firm, "cidade": r.get("city") or "", "estado": r.get("uf") or cc, "email": e["email"],
                    "tipo_email": "rh" if ROLE_RH.search(local) else ("pessoal" if (person and not is_solo) else "geral"),
                    "idioma_email": lang, "modelo": tpl,
                    "personalizacao": personalization2(lang, tpl, person, sex, firm, firm_ok, is_solo, r.get("city") or "", r.get("uf") or "", cc, r.get("areas") or [], r.get("pt_hits", 0) or 0, bool(r.get("city_in_text"))),
                    "telefone": (r.get("phones") or [""])[0], "site": r.get("final_url") or f"https://{r['domain']}",
                    "areas": ", ".join(r.get("areas") or []), "idiomas": "", "fonte_url": e.get("page") or r.get("final_url") or "",
                    "regiao": ("Brasil " + (r.get("uf") or "")).strip() if cc == "BR" else COUNTRY_NAME.get(cc, cc),
                    "prioridade": "3" if ROLE_RH.search(local) else ("1" if (person and not is_solo) else "2"),
                    "status": "", "enviado_em": "", "follow_up_1": "", "follow_up_2": "", "resposta": "",
                    "observacoes": "; ".join(x for x in [
                        "e-mail lido na página " + ("de contato/equipe" if e.get("page") != r.get("final_url") else "inicial"),
                        ("webmail é o e-mail publicado pelo escritório" if WEBMAIL.search(e["email"]) else ""),
                        ("nome deduzido do e-mail" if (person and not is_solo and not clean_person(e.get("name") or "")) else ""),
                        ("titular do escritório lido no título do site" if is_solo else ""),
                        ("gênero incerto" if person and sex in ("?","M?","F?") else ""),
                        ("nome do escritório deduzido do domínio (título do site é genérico); confira antes de citar" if not firm_ok else ""),
                        ("cidade não confirmada no site" if not r.get("city_in_text") else "")] if x),
                    "_domain": r["domain"], "_cc": cc}
                rows.append(row); stats["linhas"] += 1
    return rows, stats

COLS = ["saudacao","nome_contato","tratamento","escritorio","cidade","estado","email","tipo_email","idioma_email","modelo","personalizacao","telefone","site","areas","idiomas","fonte_url","regiao","prioridade","status","enviado_em","follow_up_1","follow_up_2","resposta","observacoes"]
if __name__ == "__main__":
    files = sys.argv[1:]
    ex_e, ex_d = set(), set()
    p = "/tmp/claude-0/-home-user-meu-projeto/e6925dc5-ccb5-56d3-90f7-9e38f32b3a69/scratchpad/emails/lista_final.csv"
    for r in csv.DictReader(open(p, encoding="utf-8", newline=""), delimiter=";"):
        ex_e.add(r["email"].lower()); ex_d.add(r["email"].lower().split("@")[1]); 
        try: ex_d.add(urllib.parse.urlparse(r["site"] if r["site"].startswith("http") else "https://" + r["site"]).netloc.lower().replace("www.", ""))
        except Exception: pass
    rows, stats = main(files, "bulk", ex_e, ex_d)
    # dedupe by email
    seen = set(); out = []
    for r in rows:
        if r["email"] in seen: continue
        seen.add(r["email"]); out.append(r)
    with open("bulk_rows.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS + ["_domain", "_cc"], delimiter=";"); w.writeheader(); w.writerows(out)
    print(dict(stats)); print("linhas únicas:", len(out))
    print("por modelo:", collections.Counter(r["modelo"] for r in out)); print("por tipo:", collections.Counter(r["tipo_email"] for r in out))
    for r in random.sample(out, min(12, len(out))): print(" ", r["modelo"], "|", r["saudacao"], "|", r["email"], "|", r["personalizacao"][:150])
