# -*- coding: utf-8 -*-
"""cc_cands.json -> linhas para pros2.add() com prioridade, modelo e gancho de personalizacao."""
import re, json, sys, os, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perfil as PF
from fixenc import fix
from pros2 import seen_all, BLOQUEADOS
WEBMAIL = {'gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com.br', 'yahoo.com', 'live.com', 'uol.com.br', 'bol.com.br', 'terra.com.br', 'icloud.com', 'hotmail.com.br', 'outlook.com.br', 'ig.com.br'}
JUNK = re.compile(r'^(seu|your|exemplo|example|email|nome|teste|test|usuario|user|fulano|contato@seudominio)|@(seudominio|dominio|exemplo|example|email|meusite|seusite|site|hub|domain|empresa|suaempresa|mysite|company|yourdomain|mail)\.|sentry|wixpress|wordpress|\.(png|jpg|jpeg|gif|webp)$', re.I)
CORE = {'Previdenciario', 'Saude / planos de saude', 'Bancario', 'Consumidor', 'Trabalhista'}
NEAR = {'RO', 'AC', 'AM', 'MT', 'RR', 'PA', 'AP', 'TO', 'MS'}
TITLE_CUT = re.compile(r'\s*[|–—-]\s*(home|in[ií]cio|p[aá]gina inicial|bem[- ]vindo.*)\s*$', re.I)

def base(d):
    d = d.lower().replace('www.', '')
    return re.sub(r'\.(adv|com|net|org|jus|blog)?\.?br$|\.com$|\.net$|\.adv$', '', d)

def nome(title, host):
    t = fix(title or '')
    t = re.sub(r'^\s*(home|in[ií]cio|p[aá]gina inicial)\s*[|–—-]\s*', '', t, flags=re.I)
    t = TITLE_CUT.sub('', t).strip()
    parts = [p.strip() for p in re.split(r'\s[|–—-]\s', t) if p.strip()]
    for p in parts:
        if re.search(r'advog|advocacia|associad|sociedade|escrit[oó]rio|law', p, re.I) and len(p) < 70:
            return p
    if parts and 3 < len(parts[0]) < 60 and not re.search(r'^(home|in[ií]cio)$', parts[0], re.I):
        return parts[0]
    return host.replace('www.', '').split('.')[0].upper() + ' (site ' + host.replace('www.', '') + ')'

GENERIC = re.compile(r'^(advogados?( associados)?|advocacia( e consultoria)?( jur[ií]dica)?|escrit[oó]rio( de advocacia)?|sociedade de advogados|home|in[ií]cio|site|contato)$', re.I)

def nome2(title, host):
    n = nome(title, host)
    if GENERIC.search(n.strip()) or len(n) < 4 or n.lower() == host.replace('www.', '').split('.')[0]:
        return host.replace('www.', '').split('.')[0].upper() + ' Advocacia (site ' + host.replace('www.', '') + ')'
    return n

import unicodedata
from bs4 import BeautifulSoup
import web
GW = set("""advocacia advogado advogados advogada advogadas associados associadas associado escritorio escritório consultoria juridica jurídica juridico jurídico
especializada especializado especialista especialistas em de do da dos das e & direito direitos empresarial corporativa corporativo solucao solução solucoes soluções
pagina página inicial quem somos home inicio início previdenciario previdenciário previdenciaria previdenciária criminal criminalista trabalhista civil cível civel tributario tributário
familia família cobranca cobrança experiencia experiência com sobre nos nós contato site oficial online sociedade individual assessoria bem vindo vinda ao seu sua para
o a os as no na nos nas por seus suas atendimento proteja garanta conheca conheça fale conosco agende consulta voce você nosso nossa nossos especializados escritorios escritórios melhor melhores servicos serviços area áreas área areas atuacao atuação the law firm office""".split())
NONFIRM = re.compile(r'associa[cç][aã]o (brasileira|nacional|dos|das|de)|instituto|sindicato|federa[cç][aã]o|ordem dos advogados|comiss[aã]o|congresso|semin[aá]rio|evento|revista|curso(s)? (de|preparat)|faculdade|escola (de|superior)|abrat|abracrim|abradt|ibdp|ieprev', re.I)

def _city(tok):
    return tok.lower() in PF._MUN

SLOGAN = re.compile(r"\b(para|que|voc[eê]|seus?|suas?|n[aã]o|sem|mais|melhor(es)?|quando|como|aqui|agora|sempre|nunca|est[aá]|precisa)\b", re.I)


def _valid_name(n):
    if len(n.split()) >= 5 and SLOGAN.search(n):   # frase de efeito do site, nao nome do escritorio
        return False
    toks = re.findall(r"[A-Za-zÀ-ÿ]{3,}", n)
    good = [t for t in toks if t.lower() not in GW and not _city(t) and t[0].isupper()]
    return bool(good) and 3 < len(n) < 70

def best_name(c, host):
    dom = host.replace('www.', '')
    d = web.fetch(c['site'])
    if d:
        sp = BeautifulSoup(d['html'], 'lxml')
        m = sp.find('meta', attrs={'property': 'og:site_name'})
        if m and m.get('content'):
            n = fix(m['content']).strip()
            if _valid_name(n): return n
    t = fix(c.get('title', '') or '')
    t = re.sub(r'\s+â\S*\s+', ' - ', t)
    for p in [x.strip() for x in re.split(r'\s[|–—-]\s|\s[|–—-]|[|–—]\s|:\s', t) if x.strip()]:
        if _valid_name(p):
            return p
    lab = dom.split('.')[0]
    return lab.upper() + ' (' + dom + ')'

def rows(cands, limit_per_firm=2):
    seen = seen_all(); out = []; review = []
    for h, c in cands.items():
        try:
            p = c.get('perfil') or PF.perfil(c['site']) or {}   # perfil ja calculado na visita (mesma funcao); so recalcula se faltar
        except Exception:
            p = c.get('perfil') or {}
        sd = urllib.parse.urlsplit(c['site']).netloc
        org = best_name(c, sd)
        if NONFIRM.search(org + ' ' + (c.get('title') or '') + ' ' + ((p or {}).get('frase') or '')):
            continue
        if '(' not in org: org = org + ' (' + sd.replace('www.', '') + ')'
        if BLOQUEADOS.search(org + ' ' + sd):
            continue
        ufs = [x.split('/')[-1] for x in p.get('cidades', [])]
        cidade, uf = (p['cidades'][0].rsplit('/', 1) if p.get('cidades') else ('', 'BR'))
        areas = p.get('areas', [])
        core = CORE.intersection(areas)
        sig = p.get('carreiras') or p.get('parceria') or p.get('volume')
        if (sig and core) or (uf in NEAR and core):
            prior = 'Alta'
        elif sig or core:
            prior = 'Media'
        else:
            prior = 'Baixa'
        if p.get('carreiras'):
            modelo, oport = 'Associado / banco de talentos', "Banco de talentos (site tem 'trabalhe conosco')"
        elif p.get('parceria') or p.get('volume'):
            modelo, oport = 'Correspondencia / parceria', 'Rede de correspondentes / parceiros'
        else:
            modelo, oport = 'Parceria (divisao de honorarios)', 'Parceria entre escritorios'
        g = PF.gancho(p)
        n = 0
        for e, tipo, page, ctx in c['picked']:
            e = e.lower().strip()
            if e in seen or JUNK.search(e) or BLOQUEADOS.search(e):
                continue
            ed = e.split('@')[1]
            ok = ed in WEBMAIL or base(ed) == base(sd) or base(ed) in base(sd) or base(sd) in base(ed)
            trecho = re.sub(r'\s+', ' ', fix(ctx))[:170]
            d = dict(org=org, email=e, tipo=(tipo + (' (webmail publicado no site)' if ed in WEBMAIL else '')), modelo=modelo,
                     remoto='Nao informado', areas=', '.join(areas[:5]) or 'Juridico', cidade=cidade, uf=uf, oport=oport,
                     fonte=page, prior=prior,
                     obs=(f"Escritorio com site oficial {sd} ({'dominio de advocacia .adv.br' if sd.endswith('.adv.br') else 'nome do dominio indica advocacia'}; localizado pelo indice publico Common Crawl). "
                          f"{g} E-mail lido no site. Trecho: \"{trecho}\""))
            if not ok:
                review.append(d); continue
            out.append(d); seen.add(e); n += 1
            if n >= limit_per_firm:
                break
    return out, review

if __name__ == '__main__':
    c = json.load(open('cc_cands.json'))
    o, r = rows(c)
    from collections import Counter
    print(len(c), 'firmas ->', len(o), 'linhas |', Counter(x['prior'] for x in o), '| revisar', len(r))
    for x in o[:12]:
        print(f"{x['prior']:5} {x['email']:40} {x['org'][:40]:40} {x['cidade']}/{x['uf']} | {x['areas'][:50]} | {x['modelo']}")
    print('--- revisar'); [print(x['email'], x['org'][:40], x['fonte'][:60]) for x in r[:10]]
