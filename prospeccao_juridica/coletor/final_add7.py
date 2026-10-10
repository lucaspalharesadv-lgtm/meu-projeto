# -*- coding: utf-8 -*-
"""Rodada 6/7 (CANDS=arquivo de candidatos, DRY=1 so mede, OUTROWS=saida): linhas novas de todos os candidatos + fila de conferencia (dominio diferente do site),
com filtros: escritorio ainda nao presente na base, texto juridico explicito, site brasileiro (para .com etc.)."""
import sys, os, re, json, csv, urllib.parse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cc_rows, pros2, web
from fixenc import fix
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
WEBMAIL = cc_rows.WEBMAIL
CF = os.environ.get('CANDS', 'cc_cands.json'); DRY = os.environ.get('DRY') == '1'
c = json.load(open(CF))
bysite = {}
for h, v in c.items():
    bysite[urllib.parse.urlsplit(v['site']).netloc.lower().replace('www.', '')] = v
out, review = cc_rows.rows(c)
print('rows brutas', len(out), '| fila de conferencia', len(review), flush=True)

# --- chaves de escritorios que ja estao na base (dominio do site e dominio do e-mail) ---
def nk(d): return (d or '').lower().split(':')[0].replace('www.', '')
base_keys = set()
for path in (pros2.P, pros2.OLD):
    rows = list(csv.reader(open(path, encoding='utf-8-sig'))); h = rows[0]
    ie, ifo = h.index('E-mail'), h.index('Fonte (link)')
    for r in rows[1:]:
        ed = r[ie].split('@')[-1].lower()
        if ed not in WEBMAIL: base_keys.add(ed)
        fd = nk(urllib.parse.urlsplit(r[ifo]).netloc)
        if fd and not re.search(r'jobijoba|indeed|gupy|linkedin|oab|rotajuridica|jurisvagas|nunchi|bne|infojobs|vagas|google|facebook|instagram', fd): base_keys.add(fd)

def sd_of(d):
    m = re.search(r'site oficial ([\w.-]+)', d['obs']); return nk(m.group(1)) if m else nk(urllib.parse.urlsplit(d['fonte']).netloc)

LEG = re.compile(r'advoc|advog|jur[ií]dic|oab', re.I)
BR = re.compile(r'OAB\s*[/-]?\s*[A-Z]{2}\b|\bCNPJ\b|\+\s?55\b|\(\d{2}\)\s?9?\d{4}[-\s]?\d{4}|CEP:?\s*\d{5}-?\d{3}|\bBrasil\b', re.I)
FOREIGN = re.compile(r'\+\s?351|\bPortugal\b|c[ée]dula profissional|\bLisboa\b|\+\s?34\b|\bEspaña\b|abogad|\+\s?54\b|\+\s?52\b|\+\s?57\b', re.I)
BAD_TLD = re.compile(r'\.(pt|es|ar|mx|co|cl|pe|uy|ao|mz|it|fr|us|uk)$', re.I)

def legal_ok(d, cand):
    txt = ' '.join([d['org'], (cand or {}).get('title', ''), ((cand or {}).get('perfil') or {}).get('frase', '') or ''])
    return bool(LEG.search(txt))

def brazil_ok(site, cand=None):
    dom = nk(urllib.parse.urlsplit(site).netloc)
    if dom.endswith('.br'): return True
    pg = web.fetch(site)
    if not pg: return False
    t = fix(web.text_of(pg['html']))[:60000]
    nbr = len(BR.findall(t)); nfo = len(FOREIGN.findall(t))
    cid = ((cand or {}).get('perfil') or {}).get('cidades') or []
    if cid and nbr >= nfo and not re.search(r'abogad|\bteus\b|\btuas?\b', t, re.I): return True
    return (nbr >= 1 and nfo == 0) or (nbr >= 3 and nbr > 2 * nfo)

DEV = re.compile(r'desenvolvid|criad[oa] por|ag[êe]ncia|webdesign|web design|site por|hospedagem|marketing digital|powered|design by|feito por', re.I)
CONTACT = re.compile(r'e-?mail|contato|fale|atendimento|telefone|whats|endere[çc]o|ligue', re.I)
GENW = re.compile(r'advocacia|advogados?|advogadas?|advoga|adv|juridicos?|associados|associadas|escritorio|sociedade|law|direito|oficial|site|br$', re.I)
def core(base):
    b = re.sub(r'[^a-z0-9]', '', base.lower())
    return GENW.sub('', b)
def same_name(ed, sd, org):
    a, b = core(ed.split('.')[0]), core(sd.split('.')[0])
    if len(a) >= 3 and len(b) >= 3 and (a == b or (len(a) >= 4 and a in b) or (len(b) >= 4 and b in a)): return True
    ot = {t for t in re.split(r'[^a-z0-9]+', fix(org).lower()) if len(t) >= 4 and not GENW.fullmatch(t)}
    return any(len(t) >= 4 and t in ed.split('.')[0] for t in ot)
LAWDOM = re.compile(r'adv|advoc|advog|jur|law|direito|oab', re.I)
def review_ok(d, cand):
    e = d['email']; ed = e.split('@')[1]
    if cc_rows.JUNK.search(e) or BAD_TLD.search(ed): return False, ''
    ctx = ''
    for pe, tipo, url, cx in (cand or {}).get('picked', []):
        if pe.lower() == e: ctx = cx; break
    sd = sd_of(d)
    if same_name(ed, sd, d['org']):
        return True, 'dominio do e-mail tem o mesmo nome do escritorio'
    if LAWDOM.search(ed.split('.')[0]) and ctx and CONTACT.search(ctx) and not DEV.search(ctx):
        return True, 'dominio do e-mail e de advocacia e aparece no bloco de contato da pagina'
    return False, ''

NONFIRM2 = re.compile(r'sistema|software|\bapp\b|marketing|cursos?\b|editora|jornal|revista|not[ií]cia|blog|portal|loja|store|m[oó]veis|tecnologia|plataforma|cont[aá]bil|contabilidade|imobili|seguros|cons[oó]rcio|faculdade|universidade|escola|instituto|associa[cç][aã]o|sindicato|concurso|\bead\b|consultoria empresarial|despachante|cart[oó]rio', re.I)
OKTLD = re.compile(r'\.(br|com|net|org|adv|law|legal|app|io|info|biz|me)$', re.I)

final, motivos = [], Counter()
def check(item):
    d, is_review = item
    sd = sd_of(d); cand = bysite.get(sd)
    ed = d['email'].split('@')[1].lower()
    if sd in base_keys or (ed not in WEBMAIL and ed in base_keys): return None, 'escritorio ja na base'
    if BAD_TLD.search(ed) or not OKTLD.search(ed): return None, 'e-mail estrangeiro ou invalido'
    if NONFIRM2.search(d['org'] + ' ' + sd + ' ' + ((cand or {}).get('title', '') or '')): return None, 'nao e escritorio (sistema, loja, curso, jornal etc.)'
    if not legal_ok(d, cand): return None, 'sem texto juridico explicito'
    if not brazil_ok((cand or {}).get('site') or d['fonte'], cand): return None, 'site nao brasileiro'
    if is_review:
        ok, why = review_ok(d, cand)
        if not ok: return None, 'dominio diferente sem confirmacao'
        d = dict(d); d['obs'] = d['obs'] + f" CONFERIDO: e-mail em dominio diferente do site ({why})."
    return d, 'ok'
items = [(d, False) for d in out] + [(d, True) for d in review]
with ThreadPoolExecutor(16) as ex:
    for d, m in ex.map(check, items):
        motivos[m] += 1
        if d: final.append(d)
# no maximo 2 por escritorio
porfirma = Counter(); f2 = []
for d in final:
    k = sd_of(d)
    if porfirma[k] >= 2: motivos['limite 2 por escritorio'] += 1; continue
    porfirma[k] += 1; f2.append(d)
json.dump(f2, open(os.environ.get('OUTROWS', 'cc_rows_out6.json'), 'w'), ensure_ascii=False)
print('motivos', dict(motivos), flush=True)
print('linhas finais', len(f2), Counter(x['prior'] for x in f2), flush=True)
if DRY:
    from collections import Counter as _C
    print('cats', _C((bysite.get(sd_of(x)) or {}).get('cat', '?') for x in f2))
    raise SystemExit
pros2.add(f2)
print('ADD OK', flush=True)
